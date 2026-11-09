import * as assert from 'assert';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { test } from 'node:test';
import { Problem } from '../../api/antivibeClient';
import { checkEvent, History } from '../../history';
import { RunResult } from '../../runner';

const PROBLEM = {
    id: 'average', title: 'Average', track_id: 'python', milestone_id: 'py-lists'
} as Problem;

const RESULT: RunResult = {
    cases: [
        { index: 0, status: 'pass', call: 'average([1, 2])', expected: '1.5', got: '1.5' },
        { index: 1, status: 'fail', call: 'average([-2, -4])', expected: '-3.0', got: '0', edge: 'negative numbers' },
        { index: 2, status: 'error', call: 'average([])', expected: '0', error: 'ZeroDivisionError', line: 4, edge: 'empty input' }
    ],
    passed: 1, total: 3, allPassed: false, timedOut: false,
    review: [{ line: 2, message: 'note' }]
};

test('a check event keeps failures in detail and passes in brief', () => {
    const event = checkEvent(PROBLEM, RESULT, 'def average(nums): ...', { attempt: 3, hintsRevealed: 1, firstSolve: false });

    assert.strictEqual(event.event, 'check');
    assert.strictEqual(event.problem, 'average');
    assert.strictEqual(event.milestone, 'py-lists');
    assert.strictEqual(event.attempt, 3);
    assert.strictEqual(event.hints_revealed, 1);
    assert.strictEqual(event.code, 'def average(nums): ...');
    assert.deepStrictEqual(event.cases, [
        { index: 0, status: 'pass', edge: null },
        { index: 1, status: 'fail', edge: 'negative numbers', call: 'average([-2, -4])', expected: '-3.0', got: '0', error: null, line: null },
        { index: 2, status: 'error', edge: 'empty input', call: 'average([])', expected: '0', got: null, error: 'ZeroDivisionError', line: 4 }
    ]);
    assert.deepStrictEqual(event.review, [{ line: 2, message: 'note' }]);
});

test('the history appends one JSON line per event, creating its folder', async () => {
    const dir = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'antivibe-history-'));
    const file = path.join(dir, 'nested', 'history.jsonl');
    const history = new History(() => file);

    await history.record({ event: 'open', problem: 'a' });
    await history.record({ event: 'hint', problem: 'a', level: 1 });

    const lines = (await fs.promises.readFile(file, 'utf8')).trim().split('\n').map(line => JSON.parse(line));
    assert.deepStrictEqual(lines.map(l => l.event), ['open', 'hint']);
    assert.ok(!Number.isNaN(Date.parse(lines[0].time)));
    await fs.promises.rm(dir, { recursive: true, force: true });
});

test('a history that cannot be written does not throw', async () => {
    const history = new History(() => path.join(__filename, 'not-a-folder', 'history.jsonl'));
    const original = console.error;
    console.error = () => undefined;
    try {
        await history.record({ event: 'open' });
    } finally {
        console.error = original;
    }
    await new History(() => undefined).record({ event: 'open' });
});
