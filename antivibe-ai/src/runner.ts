import { spawn } from 'child_process';
import { TestCase } from './api/antivibeClient';

export interface TestSpec {
    /** The function called by `args` tests; null for problems tested only through snippets */
    function: string | null;
    /** Names the solution has to define */
    requires: string[];
    compare: 'exact' | 'unordered';
    tests: TestCase[];
}

export type CaseStatus = 'pass' | 'fail' | 'error' | 'timeout' | 'not_run';

export interface CaseResult {
    index: number;
    status: CaseStatus;
    /** The code that was run, e.g. `two_sum([2, 7], 9)`; several lines for snippet tests */
    call: string;
    expected: string;
    got?: string;
    error?: string;
    /** Line in the solution file an error came from */
    line?: number;
    /** Whatever the solution printed while this case ran */
    printed?: string;
    note?: string;
}

export interface RunResult {
    /** The solution could not even be loaded (syntax error, missing function, ...) */
    loadError?: { message: string; line?: number };
    cases: CaseResult[];
    passed: number;
    total: number;
    allPassed: boolean;
    timedOut: boolean;
}

export interface RunOptions {
    pythonPath: string;
    /** Path to runner/run_tests.py */
    runnerScript: string;
    solutionPath: string;
    spec: TestSpec;
    timeoutMs: number;
}

/** Python could not be started, or the harness itself broke. */
export class RunnerError extends Error {}

/**
 * Run a solution file against a problem's tests in a separate Python process.
 * The process is killed if it runs longer than `timeoutMs` in total.
 */
export function runTests(options: RunOptions): Promise<RunResult> {
    const { pythonPath, runnerScript, solutionPath, spec, timeoutMs } = options;

    return new Promise((resolve, reject) => {
        const child = spawn(pythonPath, [runnerScript, solutionPath], {
            env: { ...process.env, PYTHONIOENCODING: 'utf-8', PYTHONDONTWRITEBYTECODE: '1' },
            windowsHide: true
        });

        let stdout = '';
        let stderr = '';
        let timedOut = false;

        const timer = setTimeout(() => {
            timedOut = true;
            child.kill();
        }, timeoutMs);

        child.stdout.on('data', chunk => { stdout += chunk; });
        child.stderr.on('data', chunk => { stderr += chunk; });

        child.on('error', error => {
            clearTimeout(timer);
            reject(new RunnerError(
                `Could not start Python ("${pythonPath}"): ${error.message}. ` +
                'Install Python 3 or set the "antivibe.pythonPath" setting.'
            ));
        });

        child.on('close', () => {
            clearTimeout(timer);
            try {
                resolve(collectResults(spec, stdout, stderr, timedOut));
            } catch (error) {
                reject(error);
            }
        });

        // The harness may exit before reading the spec (e.g. bad interpreter); don't crash on EPIPE
        child.stdin.on('error', () => undefined);
        child.stdin.end(JSON.stringify(spec));
    });
}

/** How a test reads when the harness never got far enough to describe it itself. */
function describeCall(spec: TestSpec, test: TestCase): string {
    if (test.args) {
        return `${spec.function}(${test.args.map(arg => JSON.stringify(arg)).join(', ')})`;
    }
    return [test.setup, test.check].filter(Boolean).join('\n');
}

function collectResults(spec: TestSpec, stdout: string, stderr: string, timedOut: boolean): RunResult {
    const messages: any[] = [];
    for (const line of stdout.split(/\r?\n/)) {
        if (line.trim()) {
            try {
                messages.push(JSON.parse(line));
            } catch {
                // a line cut off when the process was killed
            }
        }
    }

    const total = spec.tests.length;
    const loadError = messages.find(m => m.type === 'load_error');
    if (loadError) {
        return {
            loadError: { message: loadError.message, line: loadError.line ?? undefined },
            cases: [], passed: 0, total, allPassed: false, timedOut: false
        };
    }

    const finished = messages.some(m => m.type === 'done');
    if (!finished && !timedOut) {
        throw new RunnerError(`The test runner stopped unexpectedly.\n${stderr.trim()}`.trim());
    }

    const cases = spec.tests.map((test, index): CaseResult => {
        const start = messages.find(m => m.type === 'start' && m.index === index);
        const result = messages.find(m => m.type === 'case' && m.index === index);
        const display = {
            index,
            call: start?.call ?? describeCall(spec, test),
            expected: start?.expected ?? (test.raises ? `raises ${test.raises}` : JSON.stringify(test.expected))
        };

        if (!result) {
            // Started but never finished: this is the case that was running when time ran out
            return { ...display, status: start ? 'timeout' : 'not_run' };
        }
        return {
            ...display,
            status: result.status,
            got: result.got,
            error: result.error,
            line: result.line ?? undefined,
            printed: result.printed || undefined,
            note: result.note
        };
    });

    const passed = cases.filter(c => c.status === 'pass').length;
    return { cases, passed, total, allPassed: passed === total, timedOut };
}
