// End-to-end test, run inside a real VS Code window by scripts/run-integration.mjs.
// Needs the backend running on the configured apiUrl and Python on the PATH.
import * as assert from 'assert';
import * as vscode from 'vscode';
import { Milestone, ProblemHints } from '../../api/antivibeClient';
import { RunResult } from '../../runner';

const BANK_ACCOUNT = [
    'class BankAccount:',
    '    def __init__(self, owner, balance=0):',
    '        self.owner = owner',
    '        self.balance = balance',
    '',
    '    def deposit(self, amount):',
    '        if amount <= 0:',
    '            raise ValueError("amount must be positive")',
    '        self.balance += amount',
    '',
    '    def withdraw(self, amount):',
    '        if amount <= 0 or amount > self.balance:',
    '            raise ValueError("invalid amount")',
    '        self.balance -= amount'
].join('\n');

function activeEditor(): vscode.TextEditor {
    const editor = vscode.window.activeTextEditor;
    assert.ok(editor, 'an editor should be open');
    return editor;
}

async function replaceInEditor(from: string, to: string) {
    const editor = activeEditor();
    const start = editor.document.getText().indexOf(from);
    assert.ok(start >= 0, `"${from}" not found in the practice file`);
    const range = new vscode.Range(editor.document.positionAt(start), editor.document.positionAt(start + from.length));
    assert.ok(await editor.edit(edit => edit.replace(range, to)));
}

const check = () => vscode.commands.executeCommand<RunResult>('antivibe.checkSolution');
const start = (id: string) => vscode.commands.executeCommand<vscode.Uri | undefined>('antivibe.startProblem', id);

export async function run(): Promise<void> {
    // Later milestones are locked for a new learner: no exercises, no lessons
    assert.strictEqual(await start('two-sum'), undefined);
    assert.strictEqual(await start('is-even'), undefined);
    assert.strictEqual(await vscode.commands.executeCommand('antivibe.openLesson', 'oop-classes'), undefined);

    // "Continue Learning" opens the very first exercise, as a file in antivibe-practice/
    await vscode.commands.executeCommand('antivibe.continue');
    let editor = activeEditor();
    assert.match(editor.document.uri.fsPath, /antivibe-practice[\\/]rectangle_area\.py$/);
    assert.match(editor.document.getText(), /^# antivibe-problem: rectangle-area/);
    assert.match(editor.document.getText(), /def rectangle_area\(width, height\):\n {4}pass/);

    // The first milestone's lesson can be read
    const lesson = await vscode.commands.executeCommand<Milestone>('antivibe.openLesson', 'py-basics');
    assert.strictEqual(lesson.title, 'Values, Variables & Functions');
    assert.ok(lesson.lesson.length >= 3);
    await vscode.window.showTextDocument(editor.document);

    // The untouched starter fails every test
    let result = await check();
    assert.strictEqual(result.allPassed, false);
    assert.strictEqual(result.passed, 0);
    assert.match(result.cases[0].note ?? '', /return/);

    // A syntax error is reported, not thrown
    await replaceInEditor('    pass', '    return width *');
    result = await check();
    assert.match(result.loadError?.message ?? '', /SyntaxError/);

    // A correct solution passes
    await replaceInEditor('    return width *', '    return width * height');
    result = await check();
    assert.strictEqual(result.allPassed, true, JSON.stringify(result.cases));

    // Starting the same exercise again reopens the attempt instead of overwriting it
    await editor.document.save();
    await start('rectangle-area');
    assert.ok(activeEditor().document.getText().includes('return width * height'));

    // One solved exercise does not unlock the next milestone...
    assert.strictEqual(await start('is-even'), undefined);

    // ...finishing the milestone does
    await start('full-name');
    await replaceInEditor('    pass', '    return f"{first} {last}"');
    assert.strictEqual((await check()).allPassed, true);
    await start('hours-and-minutes');
    await replaceInEditor('    pass', '    return [total_minutes // 60, total_minutes % 60]');
    assert.strictEqual((await check()).allPassed, true);

    // A Debug exercise starts from buggy code that fails until it is fixed
    await start('average-of-two');
    assert.match(activeEditor().document.getText(), /# Plan - before any code/);
    assert.strictEqual((await check()).passed, 0);
    await replaceInEditor('    print(total / 2)', '    return total / 2');
    assert.strictEqual((await check()).allPassed, true);

    assert.ok(await start('is-even'), 'the second milestone should be unlocked now');
    assert.strictEqual(await start('sum-to'), undefined, 'the third milestone should still be locked');

    // "Continue Learning" now lands on the first exercise of the second milestone
    await vscode.commands.executeCommand('antivibe.continue');
    assert.match(activeEditor().document.uri.fsPath, /is_even\.py$/);

    // With locking switched off, any exercise opens - here a class-based one
    await vscode.workspace.getConfiguration('antivibe').update('lockMilestones', false, vscode.ConfigurationTarget.Workspace);
    assert.ok(await start('bank-account'));
    editor = activeEditor();
    assert.match(editor.document.getText(), /#   a = BankAccount\('Ann', 100\)\n#   a\.deposit\(50\)\n#   a\.balance -> 150/);

    // An empty class fails; tests that expect an error are among them
    result = await check();
    assert.strictEqual(result.passed, 0);
    assert.strictEqual(result.cases[1].expected, 'raises ValueError');

    await replaceInEditor('class BankAccount:\n    pass', BANK_ACCOUNT);
    result = await check();
    assert.strictEqual(result.allPassed, true, JSON.stringify(result.cases));

    // Hints unlock one level at a time and stop at the last one
    const revealed: number[] = [];
    for (let i = 0; i < 5; i++) {
        await vscode.window.showTextDocument(editor.document);
        const hints = await vscode.commands.executeCommand<ProblemHints>('antivibe.getHint');
        revealed.push(hints.hints.length);
    }
    assert.deepStrictEqual(revealed, [1, 2, 3, 4, 4]);

    // Everything above was written to the history file, next to the practice files
    const historyPath = vscode.Uri.joinPath(vscode.workspace.workspaceFolders![0].uri, 'antivibe-practice', 'history.jsonl');
    const events = Buffer.from(await vscode.workspace.fs.readFile(historyPath)).toString('utf8')
        .trim().split('\n').map(line => JSON.parse(line));
    const kinds = new Set(events.map(e => e.event));
    for (const kind of ['open', 'lesson', 'check', 'hint']) {
        assert.ok(kinds.has(kind), `no "${kind}" event in the history`);
    }
    const checks = events.filter(e => e.event === 'check' && e.problem === 'rectangle-area');
    assert.deepStrictEqual(checks.map(e => e.attempt), [1, 2, 3]);
    assert.deepStrictEqual(checks.map(e => e.all_passed), [false, false, true]);
    assert.strictEqual(checks[2].first_solve, true);
    assert.match(checks[2].code, /return width \* height/);
    assert.ok(events.some(e => e.event === 'large_insert' && e.problem === 'bank-account'));
    assert.ok(events.some(e => e.event === 'check' && e.cases.some((c: any) => c.edge === 'invalid input')));

    // Switching to C++: its own folder, its own progress, compiled tests
    await vscode.workspace.getConfiguration('antivibe').update('lockMilestones', true, vscode.ConfigurationTarget.Workspace);
    await vscode.workspace.getConfiguration('antivibe').update('language', 'cpp', vscode.ConfigurationTarget.Workspace);
    await vscode.commands.executeCommand('antivibe.continue');
    editor = activeEditor();
    assert.match(editor.document.uri.fsPath, /antivibe-practice[\\/]cpp[\\/]rectangle_area\.cpp$/);
    assert.match(editor.document.getText(), /^\/\/ antivibe-problem: rectangle-area/);
    assert.strictEqual(await start('is-even'), undefined, 'C++ progress is separate, so its milestone 2 is locked');

    result = await check();
    assert.strictEqual(result.loadError, undefined, JSON.stringify(result.loadError));
    assert.strictEqual(result.allPassed, false);
    await replaceInEditor('    // your code here\n    return 0.0;', '    return width * height;');
    result = await check();
    assert.strictEqual(result.allPassed, true, JSON.stringify(result.cases));

    await replaceInEditor('return width * height;', 'return width * height');
    result = await check();
    assert.match(result.loadError?.message ?? '', /does not compile/);

    await vscode.commands.executeCommand('antivibe.continue');
    assert.match(activeEditor().document.uri.fsPath, /cpp[\\/]full_name\.cpp$/);
    const cppEvents = Buffer.from(await vscode.workspace.fs.readFile(historyPath)).toString('utf8')
        .trim().split('\n').map(line => JSON.parse(line)).filter(e => e.language === 'cpp');
    assert.ok(cppEvents.some(e => e.event === 'check' && e.problem === 'rectangle-area' && e.all_passed));

    // Checking a file that isn't an exercise is refused politely
    const other = await vscode.workspace.openTextDocument({ language: 'python', content: 'x = 1\n' });
    await vscode.window.showTextDocument(other);
    assert.strictEqual(await check(), undefined);
}
