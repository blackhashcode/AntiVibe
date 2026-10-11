import * as assert from 'assert';
import { test } from 'node:test';
import { Milestone, Problem } from '../../api/antivibeClient';
import { buildStarter, fileNameFor, findProblemId } from '../../problemFile';
import { escapeHtml, renderLesson, renderResults } from '../../views';

const PLACE = {
    track_id: 'dsa',
    track: 'Data Structures & Algorithms',
    milestone_id: 'dsa-hashing',
    milestone: 'Complexity, Arrays & Hashing'
};

const PROBLEM: Problem = {
    ...PLACE,
    id: 'two-sum',
    title: 'Two Sum',
    difficulty: 'easy',
    description: 'Given a list of integers nums and an integer target, return the indices of the two numbers that add up to target.',
    function: { name: 'two_sum', params: ['nums', 'target'] },
    starter: 'def two_sum(nums, target):\n    pass\n',
    requires: ['two_sum'],
    compare: 'unordered',
    examples: ['two_sum([2, 7, 11, 15], 9) -> [0, 1]'],
    tests: [{ args: [[2, 7, 11, 15], 9], expected: [0, 1] }],
    hint_count: 4
};

const CLASS_PROBLEM: Problem = {
    ...PLACE,
    id: 'bank-account',
    title: 'Bank Account',
    difficulty: 'easy',
    description: 'Write a class BankAccount.',
    function: null,
    starter: 'class BankAccount:\n    pass\n',
    requires: ['BankAccount'],
    compare: 'exact',
    examples: [
        "a = BankAccount('Ann', 100)\na.deposit(50)\na.balance -> 150",
        "a = BankAccount('Ann', 100)\na.withdraw(500) -> raises ValueError"
    ],
    tests: [{ setup: "a = BankAccount('Ann', 100)\na.deposit(50)", check: 'a.balance', expected: 150 }],
    hint_count: 4
};

test('the starter file is recognised as its problem', () => {
    const starter = buildStarter(PROBLEM);
    assert.strictEqual(findProblemId(starter), 'two-sum');
    assert.ok(starter.endsWith('\ndef two_sum(nums, target):\n    pass\n'));
    assert.ok(starter.includes('#   two_sum([2, 7, 11, 15], 9) -> [0, 1]'));
    assert.ok(starter.includes('# Two Sum  (Data Structures & Algorithms - Complexity, Arrays & Hashing)'));
});

test('practice files are named after the problem', () => {
    assert.strictEqual(fileNameFor(PROBLEM), 'two_sum.py');
    assert.strictEqual(fileNameFor(CLASS_PROBLEM), 'bank_account.py');
});

test('a class exercise starts from its class and shows multi-line examples as comments', () => {
    const starter = buildStarter(CLASS_PROBLEM);
    assert.strictEqual(findProblemId(starter), 'bank-account');
    assert.ok(starter.endsWith('\nclass BankAccount:\n    pass\n'));
    assert.ok(starter.includes("#   a = BankAccount('Ann', 100)\n#   a.deposit(50)\n#   a.balance -> 150\n#\n#   a = BankAccount('Ann', 100)"));

    // everything above the code must be a comment, or the file would not run
    const header = starter.slice(0, starter.indexOf('class BankAccount'));
    for (const line of header.split('\n')) {
        assert.ok(line === '' || line.startsWith('#'), `not a comment: ${line}`);
    }
});

test('long descriptions are wrapped into comment lines', () => {
    for (const line of buildStarter(PROBLEM).split('\n')) {
        assert.ok(line.length <= 80, `line too long: ${line}`);
    }
});

test('files without the marker near the top are not practice files', () => {
    assert.strictEqual(findProblemId('def two_sum(nums, target):\n    pass\n'), undefined);
    assert.strictEqual(findProblemId('\n'.repeat(20) + '# antivibe-problem: two-sum\n'), undefined);
    assert.strictEqual(findProblemId('# antivibe-problem: two-sum\r\nx = 1\r\n'), 'two-sum');
});

test('learner output is escaped in the results page', () => {
    assert.strictEqual(escapeHtml('<b>"x" & \'y\'</b>'), '&lt;b&gt;&quot;x&quot; &amp; &#39;y&#39;&lt;/b&gt;');

    const html = renderResults(PROBLEM, {
        cases: [{
            index: 0, status: 'fail', call: 'two_sum([2, 7, 11, 15], 9)', expected: '[0, 1]',
            got: "'<script>alert(1)</script>'"
        }],
        passed: 0, total: 1, allPassed: false, timedOut: false
    });
    assert.ok(!html.includes('<script>'));
    assert.ok(html.includes('0 of 1 tests passed'));
});

test('multi-line test code is shown as a block in the results page', () => {
    const html = renderResults(CLASS_PROBLEM, {
        cases: [{ index: 0, status: 'pass', call: 'a = BankAccount(1)\na.balance', expected: '1', got: '1' }],
        passed: 1, total: 1, allPassed: true, timedOut: false
    });
    assert.ok(html.includes('<pre class="block">a = BankAccount(1)\na.balance</pre>'));
});

test('a lesson renders paragraphs, inline code and code blocks, all escaped', () => {
    const milestone: Milestone = {
        id: 'py-loops',
        title: 'Loops',
        summary: 'Repeat work.',
        track_id: 'python',
        track: 'Python Fundamentals',
        problems: [{ ...PLACE, id: 'sum-to', title: 'Sum to N', difficulty: 'warm-up' }],
        lesson: [{
            heading: 'for loops',
            text: 'Use `range(n)` when a < b.\n\nSecond paragraph.',
            code: 'for i in range(3):\n    print(i < 2)'
        }, {
            heading: 'No code here',
            text: 'Just text.',
            code: null
        }]
    };
    const html = renderLesson(milestone);

    assert.ok(html.includes('<p>Use <code>range(n)</code> when a &lt; b.</p><p>Second paragraph.</p>'));
    assert.ok(html.includes('<pre class="block">for i in range(3):\n    print(i &lt; 2)</pre>'));
    assert.strictEqual(html.match(/<pre class="block">/g)?.length, 1);
    assert.ok(html.includes('<li>Sum to N</li>'));
});
