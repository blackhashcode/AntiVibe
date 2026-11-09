import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import * as vscode from 'vscode';
import {
    AntivibeClient, BackendUnavailableError, HintRequest, HintResponse, Milestone, Problem, ProblemHints, Track
} from './api/antivibeClient';
import {
    blockingMilestone, findMilestone, findProblem, isMilestoneComplete, IsSolved, milestoneAfter, nextProblem,
    solvedCount
} from './curriculum';
import { checkEvent, History, problemFields } from './history';
import { isLanguage, Language, languageOfFile, LANGUAGES, practiceFolder, progressKey } from './languages';
import { buildStarter, fileNameFor, findProblemId } from './problemFile';
import { RunnerError, RunResult, runTests } from './runner';
import { CurriculumNode, CurriculumTreeProvider } from './tree';
import { renderFreeformHint, renderLesson, renderProblemHints, renderResults } from './views';

const PRACTICE_FOLDER = 'antivibe-practice';
const PROGRESS_KEY = 'antivibe.progress';
const HISTORY_FILE = 'history.jsonl';
// An insert this big at once is most likely a paste (or a large autocomplete)
const LARGE_INSERT_CHARS = 80;

interface ProblemProgress {
    hintsRevealed: number;
    solved: boolean;
    /** How many times "Check My Solution" has been run */
    checks?: number;
}

let antivibeClient: AntivibeClient;
let extensionContext: vscode.ExtensionContext;
let curriculumTree: CurriculumTreeProvider;
let curriculumView: vscode.TreeView<CurriculumNode>;
let history: History;
// Kept in memory and written through to globalState: reading globalState back
// straight after an update can briefly return the previous value.
// Keys are progressKey(problem id, language).
let progress: Record<string, ProblemProgress> = {};
// Fetched once per language and reused; "Antivibe: Refresh Learning Path" fetches again
const curricula = new Map<Language, Track[]>();
let lessonPanel: vscode.WebviewPanel | undefined;
let hintPanel: vscode.WebviewPanel | undefined;
let resultsPanel: vscode.WebviewPanel | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('Antivibe.ai extension is now active!');

    extensionContext = context;
    progress = { ...context.globalState.get<Record<string, ProblemProgress>>(PROGRESS_KEY, {}) };
    antivibeClient = new AntivibeClient(() => getConfig().get<string>('apiUrl', 'http://localhost:8000/api'));

    history = new History(historyFile);

    curriculumTree = new CurriculumTreeProvider({
        load: loadCurriculumForTree,
        isSolved: problemId => isSolved(problemId, currentLanguage()),
        lockingEnabled
    });
    curriculumView = vscode.window.createTreeView('antivibe.curriculum', { treeDataProvider: curriculumTree });
    showLanguageInView();

    // Register commands
    context.subscriptions.push(
        curriculumView,
        vscode.commands.registerCommand('antivibe.continue', () => guarded(continueLearning)),
        vscode.commands.registerCommand('antivibe.startProblem', (problemId?: string) => guarded(() => startProblem(problemId))),
        vscode.commands.registerCommand('antivibe.openLesson', (milestoneId?: string) => guarded(() => openLesson(milestoneId))),
        vscode.commands.registerCommand('antivibe.getHint', () => guarded(getHint)),
        vscode.commands.registerCommand('antivibe.checkSolution', () => guarded(checkSolution)),
        vscode.commands.registerCommand('antivibe.refresh', () => guarded(refreshCurriculum)),
        vscode.commands.registerCommand('antivibe.resetProgress', () => guarded(resetProgress)),
        vscode.commands.registerCommand('antivibe.openHistory', () => guarded(openHistory)),
        vscode.commands.registerCommand('antivibe.chooseLanguage', () => guarded(chooseLanguage)),
        vscode.workspace.onDidChangeTextDocument(recordLargeInserts),
        vscode.workspace.onDidChangeConfiguration(event => {
            if (event.affectsConfiguration('antivibe')) {
                if (event.affectsConfiguration('antivibe.apiUrl')) {
                    curricula.clear();
                }
                showLanguageInView();
                curriculumTree.refresh();
            }
        })
    );
}

function getConfig(): vscode.WorkspaceConfiguration {
    return vscode.workspace.getConfiguration('antivibe');
}

/** The language the Learning Path shows. Checks and hints use the language of the file instead. */
function currentLanguage(): Language {
    const value = getConfig().get<string>('language', 'python');
    return isLanguage(value) ? value : 'python';
}

function showLanguageInView() {
    curriculumView.description = LANGUAGES[currentLanguage()].name;
}

/** Run a command, turning known failures into a readable message instead of a stack trace. */
async function guarded<T>(command: () => Promise<T>): Promise<T | undefined> {
    try {
        return await command();
    } catch (error) {
        if (error instanceof BackendUnavailableError) {
            vscode.window.showErrorMessage(
                `Antivibe can't reach its backend at ${error.baseUrl}. ` +
                'Start it from the antivibe-backend folder with: uvicorn main:app --port 8000'
            );
        } else if (error instanceof RunnerError) {
            vscode.window.showErrorMessage(error.message);
        } else {
            vscode.window.showErrorMessage(`Antivibe: ${error instanceof Error ? error.message : String(error)}`);
            console.error(error);
        }
        return undefined;
    }
}

// ---------------------------------------------------------------------------
// History
// ---------------------------------------------------------------------------

/** The history lives next to the practice files, so it can be read (and analysed) like any file. */
function historyFile(): string | undefined {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (workspaceFolder) {
        return path.join(workspaceFolder.uri.fsPath, PRACTICE_FOLDER, HISTORY_FILE);
    }
    return path.join(extensionContext.globalStorageUri.fsPath, HISTORY_FILE);
}

async function openHistory() {
    const file = history.file;
    if (!file || !fs.existsSync(file)) {
        vscode.window.showInformationMessage('No history yet. It starts with the first exercise you open or check.');
        return;
    }
    await vscode.window.showTextDocument(vscode.Uri.file(file));
}

/** Note large inserts into exercise files: pasting a solution is worth knowing about later. */
function recordLargeInserts(event: vscode.TextDocumentChangeEvent) {
    if (event.reason !== undefined || event.document.uri.scheme !== 'file') {
        return; // undo / redo, or not a file on disk
    }
    const inserted = event.contentChanges.filter(change => change.text.length >= LARGE_INSERT_CHARS);
    if (inserted.length === 0) {
        return;
    }
    const problemId = findProblemId(event.document.getText());
    if (!problemId) {
        return;
    }
    const language = languageOfFile(event.document.fileName, event.document.languageId) ?? 'python';
    for (const change of inserted) {
        void history.record({
            event: 'large_insert',
            problem: problemId,
            language,
            chars: change.text.length,
            lines: change.text.split('\n').length,
            text: change.text
        });
    }
}

// ---------------------------------------------------------------------------
// Curriculum and progress
// ---------------------------------------------------------------------------

async function getCurriculum(language: Language = currentLanguage()): Promise<Track[]> {
    let tracks = curricula.get(language);
    if (!tracks) {
        tracks = await antivibeClient.getCurriculum(language);
        curricula.set(language, tracks);
    }
    return tracks;
}

/** For the sidebar: an unreachable backend shows the "start the backend" message instead of an error. */
async function loadCurriculumForTree(): Promise<Track[] | undefined> {
    let tracks: Track[] | undefined;
    try {
        tracks = await getCurriculum();
    } catch (error) {
        if (!(error instanceof BackendUnavailableError)) {
            console.error(error);
            vscode.window.showErrorMessage(`Antivibe: ${error instanceof Error ? error.message : String(error)}`);
        }
    }
    await vscode.commands.executeCommand('setContext', 'antivibe.backendDown', tracks === undefined);
    return tracks;
}

/** Fetch the curriculum again and say so, so a refresh that changes nothing still visibly happened. */
async function refreshCurriculum() {
    curricula.clear();
    const tracks = await vscode.window.withProgress(
        { location: { viewId: 'antivibe.curriculum' } },
        loadCurriculumForTree
    );
    curriculumTree.refresh();
    if (tracks) {
        const language = currentLanguage();
        const problems = tracks.flatMap(track => track.milestones).flatMap(milestone => milestone.problems);
        vscode.window.setStatusBarMessage(
            `$(check) Antivibe: ${LANGUAGES[language].name} Learning Path refreshed - ` +
            `${solvedCount(problems, solvedIn(language))} of ${problems.length} exercises solved`,
            5000
        );
    }
}

async function chooseLanguage() {
    const available = await antivibeClient.getLanguages();
    const current = currentLanguage();
    const picked = await vscode.window.showQuickPick(
        available.filter(l => isLanguage(l.id)).map(l => {
            const language = l.id as Language;
            return {
                label: l.name,
                description: language === current ? 'current' : undefined,
                detail: `Exercises are ${LANGUAGES[language].extension} files in ${practiceFolder(language).join('/')}`,
                language
            };
        }),
        { placeHolder: 'Which language do you want to practise in? Progress is kept separately for each.' }
    );
    if (picked && picked.language !== current) {
        await getConfig().update('language', picked.language, vscode.ConfigurationTarget.Global);
        await history.record({ event: 'language', language: picked.language });
    }
}

function lockingEnabled(): boolean {
    return getConfig().get<boolean>('lockMilestones', true);
}

function isSolved(problemId: string, language: Language): boolean {
    return progress[progressKey(problemId, language)]?.solved ?? false;
}

function solvedIn(language: Language): IsSolved {
    return problemId => isSolved(problemId, language);
}

function getProblemProgress(problemId: string, language: Language): ProblemProgress {
    return progress[progressKey(problemId, language)] ?? { hintsRevealed: 0, solved: false };
}

async function updateProblemProgress(problemId: string, language: Language, change: Partial<ProblemProgress>) {
    progress[progressKey(problemId, language)] = { ...getProblemProgress(problemId, language), ...change };
    await extensionContext.globalState.update(PROGRESS_KEY, progress);
    curriculumTree.refresh();
}

/** Start the current language's learning path again from the first exercise. */
async function resetProgress() {
    const language = currentLanguage();
    const name = LANGUAGES[language].name;
    const resetOnly = 'Reset Progress';
    const resetAndArchive = 'Reset and Archive My Solutions';
    const folder = practiceFolder(language).join('/');
    const answer = await vscode.window.showWarningMessage(
        `Start the ${name} learning path again from the first exercise?`,
        {
            modal: true,
            detail: `${name} solved marks and revealed hints are cleared, and every ${name} milestone after the first ` +
                'locks again. Other languages and your history file are not touched.\n\n' +
                `"${resetAndArchive}" also moves your ${name} exercise files into ${folder}/archive, ` +
                'so every exercise starts again from a fresh file. Nothing is deleted.'
        },
        resetOnly,
        resetAndArchive
    );
    if (!answer) {
        return;
    }

    const archivedTo = answer === resetAndArchive ? await archiveSolutions(language) : undefined;
    for (const key of Object.keys(progress)) {
        const isThisLanguage = language === 'python' ? !key.includes(':') : key.startsWith(`${language}:`);
        if (isThisLanguage) {
            delete progress[key];
        }
    }
    await extensionContext.globalState.update(PROGRESS_KEY, progress);
    await history.record({ event: 'reset_progress', language, archived_to: archivedTo ?? null });
    curriculumTree.refresh();
    vscode.window.showInformationMessage(
        archivedTo
            ? `${name} progress reset. Your old solutions are in ${archivedTo}. Press ▶ in the Learning Path to begin.`
            : `${name} progress reset. Press ▶ in the Learning Path to begin again from the first exercise.`
    );
}

/** Move a language's exercise files into <its folder>/archive/<date-time>. Returns that folder, if anything moved. */
async function archiveSolutions(language: Language): Promise<string | undefined> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        return undefined;
    }
    const folder = vscode.Uri.joinPath(workspaceFolder.uri, ...practiceFolder(language));
    let entries: [string, vscode.FileType][];
    try {
        entries = await vscode.workspace.fs.readDirectory(folder);
    } catch {
        return undefined; // no practice folder yet
    }
    const files = entries
        .filter(([name, type]) => type === vscode.FileType.File && name.endsWith(LANGUAGES[language].extension))
        .map(([name]) => vscode.Uri.joinPath(folder, name));
    if (files.length === 0) {
        return undefined;
    }

    // Save unsaved work and close the tabs, so nothing is lost or left pointing at a moved file
    const moving = new Set(files.map(uri => uri.toString()));
    for (const document of vscode.workspace.textDocuments) {
        if (document.isDirty && moving.has(document.uri.toString())) {
            await document.save();
        }
    }
    const tabs = vscode.window.tabGroups.all
        .flatMap(group => group.tabs)
        .filter(tab => tab.input instanceof vscode.TabInputText && moving.has(tab.input.uri.toString()));
    await vscode.window.tabGroups.close(tabs);

    const stamp = new Date().toISOString().slice(0, 16).replace(/[:T]/g, '-');
    const target = vscode.Uri.joinPath(folder, 'archive', stamp);
    await vscode.workspace.fs.createDirectory(target);
    for (const file of files) {
        await vscode.workspace.fs.rename(file, vscode.Uri.joinPath(target, path.basename(file.fsPath)));
    }
    return `${practiceFolder(language).join('/')}/archive/${stamp}`;
}

/**
 * True if the milestone is open. Otherwise tells the learner which milestone
 * to finish first and returns false.
 */
function checkUnlocked(tracks: Track[], milestoneId: string, language: Language): boolean {
    const solved = solvedIn(language);
    const blocker = lockingEnabled() ? blockingMilestone(tracks, milestoneId, solved) : undefined;
    if (!blocker) {
        return true;
    }
    const target = findMilestone(tracks, milestoneId);
    const left = blocker.problems.length - solvedCount(blocker.problems, solved);
    vscode.window.showWarningMessage(
        `"${target?.title}" is locked. Finish "${blocker.title}" first ` +
        `(${left} ${left === 1 ? 'exercise' : 'exercises'} left).`
    );
    return false;
}

// ---------------------------------------------------------------------------
// Lessons
// ---------------------------------------------------------------------------

async function openLesson(milestoneId?: string): Promise<Milestone | undefined> {
    const language = currentLanguage();
    const tracks = await getCurriculum(language);
    if (!milestoneId) {
        const picked = await vscode.window.showQuickPick(
            tracks.flatMap(track => track.milestones.map(milestone => ({
                label: milestone.title,
                description: track.title,
                detail: milestone.summary,
                id: milestone.id
            }))),
            { placeHolder: 'Which lesson do you want to read?' }
        );
        if (!picked) {
            return undefined;
        }
        milestoneId = picked.id;
    }

    if (!findMilestone(tracks, milestoneId)) {
        throw new Error(`Unknown milestone: ${milestoneId}`);
    }
    if (!checkUnlocked(tracks, milestoneId, language)) {
        return undefined;
    }

    const milestone = await antivibeClient.getMilestone(milestoneId, language);
    lessonPanel = showPanel(lessonPanel, 'antivibeLesson', 'Antivibe.ai Lesson', renderLesson(milestone), () => { lessonPanel = undefined; });
    await history.record({ event: 'lesson', language, milestone: milestone.id, track: milestone.track_id });
    return milestone;
}

// ---------------------------------------------------------------------------
// Start a practice problem
// ---------------------------------------------------------------------------

/** Jump to wherever the learner is: the next unsolved exercise, with its lesson if the milestone is new. */
async function continueLearning(): Promise<vscode.Uri | undefined> {
    const language = currentLanguage();
    const tracks = await getCurriculum(language);
    const solved = solvedIn(language);
    const next = nextProblem(tracks, solved);
    if (!next) {
        vscode.window.showInformationMessage(
            `🎓 You have completed every ${LANGUAGES[language].name} milestone. Nothing left to unlock!`
        );
        return undefined;
    }

    const uri = await startProblem(next.id);
    const milestone = findMilestone(tracks, next.milestone_id);
    if (milestone && solvedCount(milestone.problems, solved) === 0) {
        await openLesson(milestone.id);
    }
    return uri;
}

async function startProblem(problemId?: string): Promise<vscode.Uri | undefined> {
    const language = currentLanguage();
    const tracks = await getCurriculum(language);

    if (!problemId) {
        const picked = await pickProblem(tracks, language);
        if (!picked) {
            return undefined;
        }
        problemId = picked;
    }

    const summary = findProblem(tracks, problemId);
    if (!summary) {
        throw new Error(`Unknown problem: ${problemId}`);
    }
    if (!checkUnlocked(tracks, summary.milestone_id, language)) {
        return undefined;
    }

    const problem = await antivibeClient.getProblem(problemId, language);
    const document = await openPracticeDocument(problem, language);
    await vscode.window.showTextDocument(document, vscode.ViewColumn.One);
    await history.record({ event: 'open', language, ...problemFields(problem), solved: isSolved(problem.id, language) });
    return document.uri;
}

/** Quick pick of every exercise in the unlocked milestones, grouped by milestone. */
async function pickProblem(tracks: Track[], language: Language): Promise<string | undefined> {
    type Item = vscode.QuickPickItem & { id?: string };
    const solved = solvedIn(language);
    const items: Item[] = [];
    for (const milestone of tracks.flatMap(track => track.milestones)) {
        if (lockingEnabled() && blockingMilestone(tracks, milestone.id, solved)) {
            continue;
        }
        items.push({ label: `${milestone.track}: ${milestone.title}`, kind: vscode.QuickPickItemKind.Separator });
        for (const problem of milestone.problems) {
            items.push({
                label: `${solved(problem.id) ? '$(pass-filled)' : '$(circle-large-outline)'} ${problem.title}`,
                description: problem.difficulty,
                id: problem.id
            });
        }
    }

    const picked = await vscode.window.showQuickPick(items, {
        placeHolder: 'Pick an exercise (locked milestones are hidden until you reach them)'
    });
    return picked?.id;
}

/** Open the learner's file for a problem, creating it from the starter if it doesn't exist yet. */
async function openPracticeDocument(problem: Problem, language: Language): Promise<vscode.TextDocument> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        return vscode.workspace.openTextDocument({
            language: LANGUAGES[language].vscodeIds[0],
            content: buildStarter(problem, language)
        });
    }

    const folder = vscode.Uri.joinPath(workspaceFolder.uri, ...practiceFolder(language));
    const file = vscode.Uri.joinPath(folder, fileNameFor(problem, language));
    try {
        await vscode.workspace.fs.stat(file);
    } catch {
        // Never overwrite an existing attempt - only write the starter the first time
        await vscode.workspace.fs.createDirectory(folder);
        await vscode.workspace.fs.writeFile(file, Buffer.from(buildStarter(problem, language), 'utf8'));
    }
    return vscode.workspace.openTextDocument(file);
}

/** The exercise and language of an editor's file, if it is an Antivibe exercise. */
function exerciseOf(document: vscode.TextDocument): { problemId: string; language: Language } | undefined {
    const problemId = findProblemId(document.getText());
    if (!problemId) {
        return undefined;
    }
    return { problemId, language: languageOfFile(document.fileName, document.languageId) ?? 'python' };
}

// ---------------------------------------------------------------------------
// Hints
// ---------------------------------------------------------------------------

async function getHint(): Promise<ProblemHints | HintResponse | undefined> {
    const editor = vscode.window.activeTextEditor;

    if (!editor) {
        vscode.window.showWarningMessage('No active editor found!');
        return undefined;
    }

    const exercise = exerciseOf(editor.document);
    return exercise ? getProblemHint(exercise.problemId, exercise.language) : getFreeformHint(editor);
}

/** Reveal the next hint for a practice problem. Hints unlock one level at a time. */
async function getProblemHint(problemId: string, language: Language): Promise<ProblemHints> {
    const revealed = getProblemProgress(problemId, language).hintsRevealed;
    const data = await antivibeClient.getProblemHints(problemId, revealed + 1, language);
    await updateProblemProgress(problemId, language, { hintsRevealed: data.hints.length });
    if (data.hints.length > revealed) {
        await history.record({ event: 'hint', language, problem: problemId, level: data.hints.length, total: data.total });
    }

    hintPanel = showPanel(hintPanel, 'antivibeHint', 'Antivibe.ai Hint', renderProblemHints(data), () => { hintPanel = undefined; });
    if (revealed >= data.total) {
        vscode.window.showInformationMessage(
            "You've seen every hint for this problem. Antivibe never shows full solutions - the rest is yours to work out."
        );
    }
    return data;
}

async function getFreeformHint(editor: vscode.TextEditor): Promise<HintResponse | undefined> {
    const selection = editor.selection;
    const selectedCode = editor.document.getText(selection);

    if (!selectedCode.trim()) {
        vscode.window.showWarningMessage(
            'Select some code first, or run "Antivibe: Continue Learning" to work on a guided exercise.'
        );
        return undefined;
    }

    // Show quick pick for hint level
    const hintLevel = await vscode.window.showQuickPick([
        { label: '🚀 Level 1: Conceptual Nudge', level: 1 },
        { label: '💡 Level 2: Algorithm Suggestion', level: 2 },
        { label: '🔧 Level 3: Implementation Hint', level: 3 },
        { label: '🎯 Level 4: Code Structure', level: 4 }
    ], {
        placeHolder: 'Select hint level (higher numbers give more specific hints)'
    });

    if (!hintLevel) {
        return undefined;
    }

    // Get problem description from user
    const problemDescription = await vscode.window.showInputBox({
        prompt: 'Briefly describe the coding problem you\'re solving',
        placeHolder: 'e.g., "Find two numbers that add up to target"'
    });

    if (!problemDescription) {
        return undefined;
    }

    // Show progress notification
    return vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Antivibe.ai is thinking...",
        cancellable: false
    }, async () => {
        const request: HintRequest = {
            code: selectedCode,
            problemDescription: problemDescription,
            hintLevel: hintLevel.level
        };

        const response = await antivibeClient.getHint(request);

        // Display the hint in a new panel
        hintPanel = showPanel(hintPanel, 'antivibeHint', 'Antivibe.ai Hint', renderFreeformHint(response), () => { hintPanel = undefined; });
        return response;
    });
}

// ---------------------------------------------------------------------------
// Check a solution
// ---------------------------------------------------------------------------

async function checkSolution(): Promise<RunResult | undefined> {
    const editor = vscode.window.activeTextEditor;
    const exercise = editor && exerciseOf(editor.document);

    if (!editor || !exercise) {
        vscode.window.showWarningMessage(
            'This file is not an Antivibe exercise. Run "Antivibe: Continue Learning" first.'
        );
        return undefined;
    }

    const { language } = exercise;
    const problem = await antivibeClient.getProblem(exercise.problemId, language);
    const code = editor.document.getText();
    const result = await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: language === 'python'
            ? `Antivibe: running ${problem.tests.length} tests...`
            : `Antivibe: compiling and running ${problem.tests.length} tests...`,
        cancellable: false
    }, () => runSolution(problem, code, language));

    const before = getProblemProgress(problem.id, language);
    const attempt = (before.checks ?? 0) + 1;
    await updateProblemProgress(problem.id, language, { checks: attempt });
    await history.record({
        ...checkEvent(problem, result, code, {
            attempt,
            hintsRevealed: before.hintsRevealed,
            firstSolve: result.allPassed && !before.solved
        }),
        language
    });

    resultsPanel = showPanel(resultsPanel, 'antivibeResults', 'Antivibe.ai Results', renderResults(problem, result), () => { resultsPanel = undefined; });

    if (result.allPassed) {
        await celebrate(problem, result, language);
    } else if (result.loadError) {
        vscode.window.showWarningMessage(`${problem.title}: your code could not be run. See the results panel.`);
    } else {
        vscode.window.showWarningMessage(`${problem.title}: ${result.passed} of ${result.total} tests passed.`);
    }
    return result;
}

/** Record a solved problem and say what it unlocked. */
async function celebrate(problem: Problem, result: RunResult, language: Language) {
    const tracks = await getCurriculum(language);
    const solved = solvedIn(language);
    const milestone = findMilestone(tracks, problem.milestone_id);
    const wasComplete = milestone !== undefined && isMilestoneComplete(milestone, solved);

    await updateProblemProgress(problem.id, language, { solved: true });

    const passed = `🎉 ${problem.title}: all ${result.total} tests passed!`;
    if (!milestone || wasComplete || !isMilestoneComplete(milestone, solved)) {
        // Not awaited: the message stays up until dismissed
        vscode.window.showInformationMessage(passed, 'Next Exercise').then(choice => {
            if (choice) {
                vscode.commands.executeCommand('antivibe.continue');
            }
        });
        return;
    }

    const next = milestoneAfter(tracks, milestone.id);
    const unlocked = next
        ? `Milestone complete: "${milestone.title}". Unlocked: "${next.title}".`
        : `Milestone complete: "${milestone.title}". That was the last one - you finished the whole path! 🎓`;
    vscode.window.showInformationMessage(`${passed} ${unlocked}`, ...(next ? ['Continue'] : [])).then(choice => {
        if (choice) {
            vscode.commands.executeCommand('antivibe.continue');
        }
    });
}

/** Run the editor's current text (saved or not) against the problem's tests. */
async function runSolution(problem: Problem, source: string, language: Language): Promise<RunResult> {
    const tempDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'antivibe-'));
    const solutionPath = path.join(tempDir, fileNameFor(problem, language));
    try {
        await fs.promises.writeFile(solutionPath, source, 'utf8');
        return await runTests({
            pythonPath: getConfig().get<string>('pythonPath', 'python'),
            runnerScript: extensionContext.asAbsolutePath(path.join('runner', 'run_tests.py')),
            solutionPath,
            spec: {
                language,
                signature: problem.signature,
                compiler: getConfig().get<string>('cppCompiler', 'g++'),
                function: problem.function?.name ?? null,
                requires: problem.requires,
                compare: problem.compare,
                tests: problem.tests
            },
            timeoutMs: LANGUAGES[language].timeoutMs
        });
    } finally {
        await fs.promises.rm(tempDir, { recursive: true, force: true });
    }
}

// ---------------------------------------------------------------------------
// Panels
// ---------------------------------------------------------------------------

/** Show html in a side panel, reusing the panel if it is already open. */
function showPanel(
    panel: vscode.WebviewPanel | undefined, viewType: string, title: string, html: string, onDispose: () => void
): vscode.WebviewPanel {
    if (!panel) {
        panel = vscode.window.createWebviewPanel(
            viewType,
            title,
            { viewColumn: vscode.ViewColumn.Beside, preserveFocus: true },
            {}
        );
        panel.onDidDispose(onDispose);
    } else {
        panel.reveal(undefined, true);
    }
    panel.webview.html = html;
    return panel;
}

export function deactivate() {}
