import * as assert from 'assert';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { after, before, test } from 'node:test';
import { RunnerError, RunResult, runTests, TestSpec } from '../../runner';

// out/test/unit -> extension root
const RUNNER_SCRIPT = path.resolve(__dirname, '..', '..', '..', 'runner', 'run_tests.py');
const PYTHON = process.env.ANTIVIBE_PYTHON ?? 'python';

const ADD_SPEC: TestSpec = {
    function: 'add',
    requires: ['add'],
    compare: 'exact',
    tests: [
        { args: [1, 2], expected: 3 },
        { args: [-1, 1], expected: 0 }
    ]
};

let tempDir: string;

before(() => {
    tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'antivibe-test-'));
});

after(() => {
    fs.rmSync(tempDir, { recursive: true, force: true });
});

function run(source: string, spec: TestSpec = ADD_SPEC, timeoutMs = 10000): Promise<RunResult> {
    const solutionPath = path.join(tempDir, `solution_${Math.random().toString(36).slice(2)}.py`);
    fs.writeFileSync(solutionPath, source);
    return runTests({ pythonPath: PYTHON, runnerScript: RUNNER_SCRIPT, solutionPath, spec, timeoutMs });
}

test('a correct solution passes every case', async () => {
    const result = await run('def add(a, b):\n    return a + b\n');
    assert.strictEqual(result.allPassed, true);
    assert.strictEqual(result.passed, 2);
    assert.strictEqual(result.cases[0].call, 'add(1, 2)');
    assert.strictEqual(result.cases[0].expected, '3');
});

test('the untouched starter fails with a hint about the missing return', async () => {
    const result = await run('def add(a, b):\n    pass\n');
    assert.strictEqual(result.allPassed, false);
    assert.strictEqual(result.cases[0].status, 'fail');
    assert.strictEqual(result.cases[0].got, 'None');
    assert.match(result.cases[0].note ?? '', /return/);
});

test('a wrong answer reports what was returned', async () => {
    const result = await run('def add(a, b):\n    return a - b\n');
    assert.deepStrictEqual(result.cases.map(c => c.status), ['fail', 'fail']);
    assert.strictEqual(result.cases[0].got, '-1');
});

test('a value of the wrong kind gets a note saying so', async () => {
    const spec: TestSpec = { function: 'pair', requires: ['pair'], compare: 'exact', tests: [{ args: [], expected: [2, 15] }] };

    // looks identical to the expected list when printed, but is a type description
    const alias = (await run('def pair():\n    return list[2, 15]\n', spec)).cases[0];
    assert.strictEqual(alias.status, 'fail');
    assert.strictEqual(alias.got, 'list[2, 15]');
    assert.match(alias.note ?? '', /without the word `list`/);

    const text = (await run('def pair():\n    return "[2, 15]"\n', spec)).cases[0];
    assert.match(text.note ?? '', /expects a list, but your code returned a str/);

    const wrongValues = (await run('def pair():\n    return [2, 16]\n', spec)).cases[0];
    assert.strictEqual(wrongValues.note, undefined);

    const decimal = (await run('def add(a, b):\n    return a + b + 0.5\n')).cases[0];
    assert.strictEqual(decimal.note, undefined);
});

test('an exception reports its type and the line in the solution', async () => {
    const result = await run('def add(a, b):\n    total = a + b\n    return total / 0\n');
    assert.strictEqual(result.cases[0].status, 'error');
    assert.match(result.cases[0].error ?? '', /ZeroDivisionError/);
    assert.strictEqual(result.cases[0].line, 3);
});

test('a syntax error is a load error with a line number', async () => {
    const result = await run('def add(a, b)\n    return a + b\n');
    assert.match(result.loadError?.message ?? '', /SyntaxError/);
    assert.strictEqual(result.loadError?.line, 1);
    assert.strictEqual(result.allPassed, false);
});

test('a renamed function is a load error', async () => {
    const result = await run('def plus(a, b):\n    return a + b\n');
    assert.match(result.loadError?.message ?? '', /add/);
});

test('print() in the solution is captured, not mistaken for results', async () => {
    const result = await run('print("loading")\ndef add(a, b):\n    print("adding", a, b)\n    return a + b\n');
    assert.strictEqual(result.allPassed, true);
    assert.strictEqual(result.cases[0].printed, 'adding 1 2\n');
});

test('an infinite loop is stopped and reported as a timeout', async () => {
    const source = 'def add(a, b):\n    if a == -1:\n        while True:\n            pass\n    return a + b\n';
    const result = await run(source, ADD_SPEC, 3000);
    assert.strictEqual(result.timedOut, true);
    assert.deepStrictEqual(result.cases.map(c => c.status), ['pass', 'timeout']);
    assert.strictEqual(result.cases[1].call, 'add(-1, 1)');
});

test('"unordered" accepts any order, and tuples count as lists', async () => {
    const spec: TestSpec = {
        function: 'pair',
        requires: ['pair'],
        compare: 'unordered',
        tests: [{ args: [], expected: [0, 1] }]
    };
    assert.strictEqual((await run('def pair():\n    return (1, 0)\n', spec)).allPassed, true);
    assert.strictEqual((await run('def pair():\n    return [0, 2]\n', spec)).allPassed, false);
});

test('"exact" cares about order and does not accept 1 for True', async () => {
    const ordered: TestSpec = { function: 'f', requires: ['f'], compare: 'exact', tests: [{ args: [], expected: [0, 1] }] };
    assert.strictEqual((await run('def f():\n    return [1, 0]\n', ordered)).allPassed, false);

    const truthy: TestSpec = { function: 'f', requires: ['f'], compare: 'exact', tests: [{ args: [], expected: true }] };
    assert.strictEqual((await run('def f():\n    return 1\n', truthy)).allPassed, false);
    assert.strictEqual((await run('def f():\n    return True\n', truthy)).allPassed, true);
});

test('a solution cannot change the inputs of later cases', async () => {
    const spec: TestSpec = {
        function: 'first',
        requires: ['first'],
        compare: 'exact',
        tests: [{ args: [[3, 1, 2]], expected: 3 }]
    };
    const result = await run('def first(nums):\n    value = nums[0]\n    nums.clear()\n    return value\n', spec);
    assert.strictEqual(result.allPassed, true);
    assert.strictEqual(result.cases[0].call, 'first([3, 1, 2])');
});

const ACCOUNT_SPEC: TestSpec = {
    function: null,
    requires: ['Account'],
    compare: 'exact',
    tests: [
        { setup: 'a = Account(100)\na.deposit(50)', check: 'a.balance', expected: 150 },
        { setup: 'a = Account(100)', check: 'a.withdraw(500)', raises: 'ValueError' },
        { check: 'Account(7).balance', expected: 7 }
    ]
};

const ACCOUNT = [
    'class Account:',
    '    def __init__(self, balance):',
    '        self.balance = balance',
    '',
    '    def deposit(self, amount):',
    '        self.balance += amount',
    '',
    '    def withdraw(self, amount):',
    '        if amount > self.balance:',
    '            raise ValueError("not enough money")',
    '        self.balance -= amount',
    ''
].join('\n');

test('class exercises are tested with setup code and a checked expression', async () => {
    const result = await run(ACCOUNT, ACCOUNT_SPEC);
    assert.strictEqual(result.allPassed, true, JSON.stringify(result.cases));
    assert.strictEqual(result.cases[0].call, 'a = Account(100)\na.deposit(50)\na.balance');
    assert.strictEqual(result.cases[1].expected, 'raises ValueError');
    assert.strictEqual(result.cases[1].got, 'raised ValueError');
    assert.strictEqual(result.cases[2].call, 'Account(7).balance');
});

test('a test that expects an error fails when nothing is raised', async () => {
    const result = await run(ACCOUNT.replace('raise ValueError("not enough money")', 'return'), ACCOUNT_SPEC);
    assert.deepStrictEqual(result.cases.map(c => c.status), ['pass', 'fail', 'pass']);
    assert.match(result.cases[1].note ?? '', /should raise ValueError/);
});

test('the wrong kind of error is reported as an error, with its line', async () => {
    const result = await run(ACCOUNT.replace('ValueError', 'KeyError'), ACCOUNT_SPEC);
    assert.strictEqual(result.cases[1].status, 'error');
    assert.match(result.cases[1].error ?? '', /KeyError/);
    assert.strictEqual(result.cases[1].line, 10);
});

test('an empty class fails each test instead of stopping the run', async () => {
    const result = await run('class Account:\n    pass\n', ACCOUNT_SPEC);
    assert.strictEqual(result.loadError, undefined);
    assert.deepStrictEqual(result.cases.map(c => c.status), ['error', 'error', 'error']);
});

test('a missing class is a load error', async () => {
    const result = await run('class Acount:\n    pass\n', ACCOUNT_SPEC);
    assert.match(result.loadError?.message ?? '', /Account/);
});

test('a missing Python interpreter gives a readable error', async () => {
    const solutionPath = path.join(tempDir, 'unused.py');
    fs.writeFileSync(solutionPath, '');
    await assert.rejects(
        runTests({
            pythonPath: 'antivibe-no-such-python',
            runnerScript: RUNNER_SCRIPT,
            solutionPath,
            spec: ADD_SPEC,
            timeoutMs: 5000
        }),
        (error: unknown) => error instanceof RunnerError && /antivibe\.pythonPath/.test(error.message)
    );
});
