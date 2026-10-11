import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import * as vscode from 'vscode';
import {
    AntivibeClient, BackendUnavailableError, HintRequest, HintResponse, Milestone, Problem, ProblemHints, Track
} from './api/antivibeClient';
import {
    blockingMilestone, findMilestone, findProblem, isMilestoneComplete, milestoneAfter, nextProblem, solvedCount
} from './curriculum';
import { buildStarter, fileNameFor, findProblemId } from './problemFile';
import { RunnerError, RunResult, runTests } from './runner';
import { CurriculumTreeProvider } from './tree';
import { renderFreeformHint, renderLesson, renderProblemHints, renderResults } from './views';

const PRACTICE_FOLDER = 'antivibe-practice';
const PROGRESS_KEY = 'antivibe.progress';
const TEST_TIMEOUT_MS = 10000;

interface ProblemProgress {
    hintsRevealed: number;
    solved: boolean;
}

let antivibeClient: AntivibeClient;
let extensionContext: vscode.ExtensionContext;
let curriculumTree: CurriculumTreeProvider;
// Kept in memory and written through to globalState: reading globalState back
// straight after an update can briefly return the previous value.
let progress: Record<string, ProblemProgress> = {};
// Fetched once and reused; "Antivibe: Refresh Learning Path" fetches it again
let curriculum: Track[] | undefined;
let lessonPanel: vscode.WebviewPanel | undefined;
let hintPanel: vscode.WebviewPanel | undefined;
let resultsPanel: vscode.WebviewPanel | undefined;

export function activate(context: vscode.ExtensionContext) {
    console.log('Antivibe.ai extension is now active!');

    extensionContext = context;
    progress = { ...context.globalState.get<Record<string, ProblemProgress>>(PROGRESS_KEY, {}) };
    antivibeClient = new AntivibeClient(() => getConfig().get<string>('apiUrl', 'http://localhost:8000/api'));

    curriculumTree = new CurriculumTreeProvider({
        load: loadCurriculumForTree,
        isSolved,
        lockingEnabled
    });

    // Register commands
    context.subscriptions.push(
        vscode.window.registerTreeDataProvider('antivibe.curriculum', curriculumTree),
        vscode.commands.registerCommand('antivibe.continue', () => guarded(continueLearning)),
        vscode.commands.registerCommand('antivibe.startProblem', (problemId?: string) => guarded(() => startProblem(problemId))),
        vscode.commands.registerCommand('antivibe.openLesson', (milestoneId?: string) => guarded(() => openLesson(milestoneId))),
        vscode.commands.registerCommand('antivibe.getHint', () => guarded(getHint)),
        vscode.commands.registerCommand('antivibe.checkSolution', () => guarded(checkSolution)),
        vscode.commands.registerCommand('antivibe.refresh', () => guarded(refreshCurriculum)),
        vscode.commands.registerCommand('antivibe.resetProgress', () => guarded(resetProgress)),
        vscode.workspace.onDidChangeConfiguration(event => {
            if (event.affectsConfiguration('antivibe')) {
                curriculum = undefined;
                curriculumTree.refresh();
            }
        })
    );
}

function getConfig(): vscode.WorkspaceConfiguration {
    return vscode.workspace.getConfiguration('antivibe');
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
// Curriculum and progress
// ---------------------------------------------------------------------------

async function getCurriculum(): Promise<Track[]> {
    if (!curriculum) {
        curriculum = await antivibeClient.getCurriculum();
    }
    return curriculum;
}

/** For the sidebar: an unreachable backend shows the "start the backend" message instead of an error. */
async function loadCurriculumForTree(): Promise<Track[] | undefined> {
    let tracks: Track[] | undefined;
    try {
        tracks = await getCurriculum();
    } catch (error) {
        if (!(error instanceof BackendUnavailableError)) {
            console.error(error);
        }
    }
    await vscode.commands.executeCommand('setContext', 'antivibe.backendDown', tracks === undefined);
    return tracks;
}

async function refreshCurriculum() {
    curriculum = undefined;
    curriculumTree.refresh();
}

function lockingEnabled(): boolean {
    return getConfig().get<boolean>('lockMilestones', true);
}

function isSolved(problemId: string): boolean {
    return progress[problemId]?.solved ?? false;
}

function getProblemProgress(problemId: string): ProblemProgress {
    return progress[problemId] ?? { hintsRevealed: 0, solved: false };
}

async function updateProblemProgress(problemId: string, change: Partial<ProblemProgress>) {
    progress[problemId] = { ...getProblemProgress(problemId), ...change };
    await extensionContext.globalState.update(PROGRESS_KEY, progress);
    curriculumTree.refresh();
}

async function resetProgress() {
    const answer = await vscode.window.showWarningMessage(
        'Reset all Antivibe progress? Solved marks and revealed hints will be cleared, and milestones lock again. Your solution files are not touched.',
        { modal: true },
        'Reset'
    );
    if (answer === 'Reset') {
        progress = {};
        await extensionContext.globalState.update(PROGRESS_KEY, undefined);
        curriculumTree.refresh();
        vscode.window.showInformationMessage('Antivibe progress has been reset.');
    }
}

/**
 * True if the milestone is open. Otherwise tells the learner which milestone
 * to finish first and returns false.
 */
function checkUnlocked(tracks: Track[], milestoneId: string): boolean {
    const blocker = lockingEnabled() ? blockingMilestone(tracks, milestoneId, isSolved) : undefined;
    if (!blocker) {
        return true;
    }
    const target = findMilestone(tracks, milestoneId);
    const left = blocker.problems.length - solvedCount(blocker.problems, isSolved);
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
    const tracks = await getCurriculum();
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
    if (!checkUnlocked(tracks, milestoneId)) {
        return undefined;
    }

    const milestone = await antivibeClient.getMilestone(milestoneId);
    lessonPanel = showPanel(lessonPanel, 'antivibeLesson', 'Antivibe.ai Lesson', renderLesson(milestone), () => { lessonPanel = undefined; });
    return milestone;
}

// ---------------------------------------------------------------------------
// Start a practice problem
// ---------------------------------------------------------------------------

/** Jump to wherever the learner is: the next unsolved exercise, with its lesson if the milestone is new. */
async function continueLearning(): Promise<vscode.Uri | undefined> {
    const tracks = await getCurriculum();
    const next = nextProblem(tracks, isSolved);
    if (!next) {
        vscode.window.showInformationMessage('🎓 You have completed every milestone. Nothing left to unlock!');
        return undefined;
    }

    const uri = await startProblem(next.id);
    const milestone = findMilestone(tracks, next.milestone_id);
    if (milestone && solvedCount(milestone.problems, isSolved) === 0) {
        await openLesson(milestone.id);
    }
    return uri;
}

async function startProblem(problemId?: string): Promise<vscode.Uri | undefined> {
    const tracks = await getCurriculum();

    if (!problemId) {
        const picked = await pickProblem(tracks);
        if (!picked) {
            return undefined;
        }
        problemId = picked;
    }

    const summary = findProblem(tracks, problemId);
    if (!summary) {
        throw new Error(`Unknown problem: ${problemId}`);
    }
    if (!checkUnlocked(tracks, summary.milestone_id)) {
        return undefined;
    }

    const problem = await antivibeClient.getProblem(problemId);
    const document = await openPracticeDocument(problem);
    await vscode.window.showTextDocument(document, vscode.ViewColumn.One);
    return document.uri;
}

/** Quick pick of every exercise in the unlocked milestones, grouped by milestone. */
async function pickProblem(tracks: Track[]): Promise<string | undefined> {
    type Item = vscode.QuickPickItem & { id?: string };
    const items: Item[] = [];
    for (const milestone of tracks.flatMap(track => track.milestones)) {
        if (lockingEnabled() && blockingMilestone(tracks, milestone.id, isSolved)) {
            continue;
        }
        items.push({ label: `${milestone.track}: ${milestone.title}`, kind: vscode.QuickPickItemKind.Separator });
        for (const problem of milestone.problems) {
            items.push({
                label: `${isSolved(problem.id) ? '$(pass-filled)' : '$(circle-large-outline)'} ${problem.title}`,
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
async function openPracticeDocument(problem: Problem): Promise<vscode.TextDocument> {
    const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
    if (!workspaceFolder) {
        return vscode.workspace.openTextDocument({ language: 'python', content: buildStarter(problem) });
    }

    const folder = vscode.Uri.joinPath(workspaceFolder.uri, PRACTICE_FOLDER);
    const file = vscode.Uri.joinPath(folder, fileNameFor(problem));
    try {
        await vscode.workspace.fs.stat(file);
    } catch {
        // Never overwrite an existing attempt - only write the starter the first time
        await vscode.workspace.fs.createDirectory(folder);
        await vscode.workspace.fs.writeFile(file, Buffer.from(buildStarter(problem), 'utf8'));
    }
    return vscode.workspace.openTextDocument(file);
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

    const problemId = findProblemId(editor.document.getText());
    return problemId ? getProblemHint(problemId) : getFreeformHint(editor);
}

/** Reveal the next hint for a practice problem. Hints unlock one level at a time. */
async function getProblemHint(problemId: string): Promise<ProblemHints> {
    const revealed = getProblemProgress(problemId).hintsRevealed;
    const data = await antivibeClient.getProblemHints(problemId, revealed + 1);
    await updateProblemProgress(problemId, { hintsRevealed: data.hints.length });

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
    const problemId = editor && findProblemId(editor.document.getText());

    if (!editor || !problemId) {
        vscode.window.showWarningMessage(
            'This file is not an Antivibe exercise. Run "Antivibe: Continue Learning" first.'
        );
        return undefined;
    }

    const problem = await antivibeClient.getProblem(problemId);
    const result = await vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: `Antivibe: running ${problem.tests.length} tests...`,
        cancellable: false
    }, () => runSolution(problem, editor.document.getText()));

    resultsPanel = showPanel(resultsPanel, 'antivibeResults', 'Antivibe.ai Results', renderResults(problem, result), () => { resultsPanel = undefined; });

    if (result.allPassed) {
        await celebrate(problem, result);
    } else if (result.loadError) {
        vscode.window.showWarningMessage(`${problem.title}: your code could not be run. See the results panel.`);
    } else {
        vscode.window.showWarningMessage(`${problem.title}: ${result.passed} of ${result.total} tests passed.`);
    }
    return result;
}

/** Record a solved problem and say what it unlocked. */
async function celebrate(problem: Problem, result: RunResult) {
    const tracks = await getCurriculum();
    const milestone = findMilestone(tracks, problem.milestone_id);
    const wasComplete = milestone !== undefined && isMilestoneComplete(milestone, isSolved);

    await updateProblemProgress(problem.id, { solved: true });

    const passed = `🎉 ${problem.title}: all ${result.total} tests passed!`;
    if (!milestone || wasComplete || !isMilestoneComplete(milestone, isSolved)) {
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
async function runSolution(problem: Problem, source: string): Promise<RunResult> {
    const tempDir = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'antivibe-'));
    const solutionPath = path.join(tempDir, fileNameFor(problem));
    try {
        await fs.promises.writeFile(solutionPath, source, 'utf8');
        return await runTests({
            pythonPath: getConfig().get<string>('pythonPath', 'python'),
            runnerScript: extensionContext.asAbsolutePath(path.join('runner', 'run_tests.py')),
            solutionPath,
            spec: {
                function: problem.function?.name ?? null,
                requires: problem.requires,
                compare: problem.compare,
                tests: problem.tests
            },
            timeoutMs: TEST_TIMEOUT_MS
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
