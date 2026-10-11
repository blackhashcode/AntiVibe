import { MilestoneSummary, ProblemSummary, Track } from './api/antivibeClient';

/** Answers "has this problem been solved?" */
export type IsSolved = (problemId: string) => boolean;

export function allMilestones(tracks: Track[]): MilestoneSummary[] {
    return tracks.flatMap(track => track.milestones);
}

export function findMilestone(tracks: Track[], milestoneId: string): MilestoneSummary | undefined {
    return allMilestones(tracks).find(milestone => milestone.id === milestoneId);
}

export function findProblem(tracks: Track[], problemId: string): ProblemSummary | undefined {
    return allMilestones(tracks).flatMap(milestone => milestone.problems).find(problem => problem.id === problemId);
}

export function solvedCount(problems: ProblemSummary[], isSolved: IsSolved): number {
    return problems.filter(problem => isSolved(problem.id)).length;
}

export function isMilestoneComplete(milestone: MilestoneSummary, isSolved: IsSolved): boolean {
    return milestone.problems.every(problem => isSolved(problem.id));
}

/**
 * The milestone that has to be finished before `milestoneId` opens up, or
 * undefined if it is already unlocked. Milestones unlock strictly in order,
 * across tracks: the first OOP milestone needs the last Python one.
 */
export function blockingMilestone(tracks: Track[], milestoneId: string, isSolved: IsSolved): MilestoneSummary | undefined {
    for (const milestone of allMilestones(tracks)) {
        if (milestone.id === milestoneId) {
            return undefined;
        }
        if (!isMilestoneComplete(milestone, isSolved)) {
            return milestone;
        }
    }
    return undefined;
}

/** The first milestone that still has unsolved problems, i.e. where the learner currently is. */
export function currentMilestone(tracks: Track[], isSolved: IsSolved): MilestoneSummary | undefined {
    return allMilestones(tracks).find(milestone => !isMilestoneComplete(milestone, isSolved));
}

/** The next problem to work on, or undefined once everything is solved. */
export function nextProblem(tracks: Track[], isSolved: IsSolved): ProblemSummary | undefined {
    return currentMilestone(tracks, isSolved)?.problems.find(problem => !isSolved(problem.id));
}

/** The milestone that follows `milestoneId` in learning order, if any. */
export function milestoneAfter(tracks: Track[], milestoneId: string): MilestoneSummary | undefined {
    const milestones = allMilestones(tracks);
    const index = milestones.findIndex(milestone => milestone.id === milestoneId);
    return index >= 0 ? milestones[index + 1] : undefined;
}
