import * as fs from 'fs';
import * as path from 'path';
import { Problem } from './api/antivibeClient';
import { RunResult } from './runner';

/**
 * A learning history: one JSON object per line, appended as things happen,
 * so it can be analysed later (attempts per exercise, which edge cases fail,
 * hint use, time taken, large pastes...). Every line has `time` and `event`.
 */
export class History {
    constructor(private readonly getFile: () => string | undefined) {}

    /** The file the history is written to, if there is one. */
    get file(): string | undefined {
        return this.getFile();
    }

    /** Append an event. Never throws: a broken history must not break a check. */
    async record(event: Record<string, unknown>): Promise<void> {
        const file = this.getFile();
        if (!file) {
            return;
        }
        try {
            await fs.promises.mkdir(path.dirname(file), { recursive: true });
            await fs.promises.appendFile(file, JSON.stringify({ time: new Date().toISOString(), ...event }) + '\n', 'utf8');
        } catch (error) {
            console.error('Antivibe could not write its history', error);
        }
    }
}

/** Where a problem sits in the curriculum, for every event about it. */
export function problemFields(problem: Pick<Problem, 'id' | 'title' | 'track_id' | 'milestone_id'>) {
    return { problem: problem.id, title: problem.title, track: problem.track_id, milestone: problem.milestone_id };
}

/** The history entry for one run of "Check My Solution". */
export function checkEvent(
    problem: Problem, result: RunResult, code: string,
    context: { attempt: number; hintsRevealed: number; firstSolve: boolean }
): Record<string, unknown> {
    return {
        event: 'check',
        ...problemFields(problem),
        attempt: context.attempt,
        hints_revealed: context.hintsRevealed,
        passed: result.passed,
        total: result.total,
        all_passed: result.allPassed,
        first_solve: context.firstSolve,
        timed_out: result.timedOut,
        load_error: result.loadError ?? null,
        // Passing tests only need their label; failures keep the details for analysis
        cases: result.cases.map(c => c.status === 'pass'
            ? { index: c.index, status: c.status, edge: c.edge ?? null }
            : {
                index: c.index, status: c.status, edge: c.edge ?? null, call: c.call, expected: c.expected,
                got: c.got ?? null, error: c.error ?? null, line: c.line ?? null
            }),
        review: result.review,
        code
    };
}
