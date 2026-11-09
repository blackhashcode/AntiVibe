import * as assert from 'assert';
import { execFileSync } from 'child_process';
import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import { test } from 'node:test';
import { Problem } from '../../api/antivibeClient';
import { languageOfFile, practiceFolder, progressKey } from '../../languages';
import { buildStarter, fileNameFor, findProblemId } from '../../problemFile';
import { runTests, TestSpec } from '../../runner';

const CPP_PROBLEM = {
    language: 'cpp',
    id: 'two-sum',
    title: 'Two Sum',
    difficulty: 'easy',
    track_id: 'cpp-dsa',
    track: 'Data Structures & Algorithms in C++',
    milestone_id: 'cpp-dsa-hashing',
    milestone: 'Complexity, Arrays & Hashing',
    description: 'Return the indices of the two numbers that add up to target.',
    function: null,
    signature: { name: 'two_sum', params: [['nums', 'array[int]'], ['target', 'int']], returns: 'array[int]' },
    starter: '#include <vector>\nusing namespace std;\n\nvector<int> two_sum(const vector<int>& nums, int target) {\n    return {};\n}\n',
    requires: [],
    compare: 'unordered',
    examples: ['two_sum([2, 7, 11, 15], 9) -> [0, 1]'],
    tests: [{ args: [[2, 7, 11, 15], 9], expected: [0, 1] }],
    hint_count: 4
} as Problem;

test('files are recognised by extension or VS Code language id', () => {
    assert.strictEqual(languageOfFile('C:\\x\\two_sum.cpp'), 'cpp');
    assert.strictEqual(languageOfFile('/x/Two.java'), 'java');
    assert.strictEqual(languageOfFile('/x/two_sum.py'), 'python');
    assert.strictEqual(languageOfFile('Untitled-1', 'cpp'), 'cpp');
    assert.strictEqual(languageOfFile('notes.txt', 'plaintext'), undefined);
});

test('progress and folders are kept apart per language, with Python unchanged', () => {
    assert.strictEqual(progressKey('two-sum', 'python'), 'two-sum');
    assert.strictEqual(progressKey('two-sum', 'cpp'), 'cpp:two-sum');
    assert.deepStrictEqual(practiceFolder('python'), ['antivibe-practice']);
    assert.deepStrictEqual(practiceFolder('cpp'), ['antivibe-practice', 'cpp']);
});

test('a C++ starter uses // comments and is recognised as its problem', () => {
    const starter = buildStarter(CPP_PROBLEM, 'cpp');
    assert.ok(starter.startsWith('// antivibe-problem: two-sum\n//\n'));
    assert.strictEqual(findProblemId(starter), 'two-sum');
    assert.ok(starter.includes('//   two_sum([2, 7, 11, 15], 9) -> [0, 1]'));
    assert.ok(starter.endsWith('vector<int> two_sum(const vector<int>& nums, int target) {\n    return {};\n}\n'));
    for (const line of starter.slice(0, starter.indexOf('#include')).split('\n')) {
        assert.ok(line === '' || line.startsWith('//'), `not a comment: ${line}`);
    }
    assert.strictEqual(fileNameFor(CPP_PROBLEM, 'cpp'), 'two_sum.cpp');
});

function hasCompiler(): boolean {
    try {
        execFileSync('g++', ['--version'], { stdio: 'ignore' });
        return true;
    } catch {
        return false;
    }
}

test('a C++ solution is compiled and tested', { skip: !hasCompiler() && 'g++ is not installed' }, async () => {
    const dir = await fs.promises.mkdtemp(path.join(os.tmpdir(), 'antivibe-cpp-unit-'));
    const solutionPath = path.join(dir, 'two_sum.cpp');
    await fs.promises.writeFile(solutionPath, [
        '#include <vector>',
        '#include <stdexcept>',
        'using namespace std;',
        'vector<int> two_sum(const vector<int>& nums, int target) {',
        '    for (int i = 0; i < (int)nums.size(); i++)',
        '        for (int j = i + 1; j < (int)nums.size(); j++)',
        '            if (nums[i] + nums[j] == target) return {i, j};',
        '    throw invalid_argument("no pair");',
        '}',
        ''
    ].join('\n'));
    const spec: TestSpec = {
        language: 'cpp',
        signature: CPP_PROBLEM.signature,
        function: null,
        requires: [],
        compare: 'unordered',
        tests: [
            { args: [[2, 7, 11, 15], 9], expected: [0, 1] },
            { args: [[1, 2], 99], expected: [] },
            { args: [[3, 3], 6], expected: [1, 0], edge: 'repeated values' }
        ]
    };
    try {
        const result = await runTests({
            pythonPath: process.env.ANTIVIBE_PYTHON ?? 'python',
            runnerScript: path.resolve(__dirname, '..', '..', '..', 'runner', 'run_tests.py'),
            solutionPath,
            spec,
            timeoutMs: 90000
        });
        assert.strictEqual(result.loadError, undefined, JSON.stringify(result));
        assert.deepStrictEqual(result.cases.map(c => c.status), ['pass', 'error', 'pass']);
        assert.match(result.cases[1].error ?? '', /invalid_argument: no pair/);
        assert.strictEqual(result.cases[0].call, 'two_sum([2, 7, 11, 15], 9)');
        assert.strictEqual(result.cases[2].edge, 'repeated values');

        await fs.promises.writeFile(solutionPath, 'int two_sum( {\n');
        const broken = await runTests({
            pythonPath: process.env.ANTIVIBE_PYTHON ?? 'python',
            runnerScript: path.resolve(__dirname, '..', '..', '..', 'runner', 'run_tests.py'),
            solutionPath,
            spec,
            timeoutMs: 90000
        });
        assert.match(broken.loadError?.message ?? '', /does not compile/);
        assert.strictEqual(broken.loadError?.line, 1);
    } finally {
        await fs.promises.rm(dir, { recursive: true, force: true });
    }
});
