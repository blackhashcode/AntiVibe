import * as assert from 'assert';
import { test } from 'node:test';
import { MilestoneSummary, Track } from '../../api/antivibeClient';
import {
    blockingMilestone, currentMilestone, findMilestone, findProblem, isMilestoneComplete, milestoneAfter,
    nextProblem, solvedCount
} from '../../curriculum';

function milestone(track: string, id: string, problemIds: string[]): MilestoneSummary {
    return {
        id, title: id, summary: '', track_id: track, track,
        problems: problemIds.map(problemId => ({
            id: problemId, title: problemId, difficulty: 'easy',
            track_id: track, track, milestone_id: id, milestone: id
        }))
    };
}

const TRACKS: Track[] = [
    { id: 'python', title: 'Python', description: '', milestones: [milestone('python', 'basics', ['a', 'b']), milestone('python', 'loops', ['c'])] },
    { id: 'oop', title: 'OOP', description: '', milestones: [milestone('oop', 'classes', ['d', 'e'])] }
];

const solved = (...ids: string[]) => (problemId: string) => ids.includes(problemId);

test('a new learner starts at the first problem of the first milestone', () => {
    assert.strictEqual(currentMilestone(TRACKS, solved())?.id, 'basics');
    assert.strictEqual(nextProblem(TRACKS, solved())?.id, 'a');
    assert.strictEqual(blockingMilestone(TRACKS, 'basics', solved()), undefined);
});

test('later milestones are blocked by the first unfinished one', () => {
    assert.strictEqual(blockingMilestone(TRACKS, 'loops', solved('a'))?.id, 'basics');
    assert.strictEqual(blockingMilestone(TRACKS, 'classes', solved('a'))?.id, 'basics');
});

test('finishing a milestone unlocks only the next one', () => {
    const isSolved = solved('a', 'b');
    assert.strictEqual(isMilestoneComplete(TRACKS[0].milestones[0], isSolved), true);
    assert.strictEqual(blockingMilestone(TRACKS, 'loops', isSolved), undefined);
    assert.strictEqual(blockingMilestone(TRACKS, 'classes', isSolved)?.id, 'loops');
    assert.strictEqual(nextProblem(TRACKS, isSolved)?.id, 'c');
});

test('the next track opens once the previous track is finished', () => {
    const isSolved = solved('a', 'b', 'c');
    assert.strictEqual(blockingMilestone(TRACKS, 'classes', isSolved), undefined);
    assert.strictEqual(currentMilestone(TRACKS, isSolved)?.id, 'classes');
});

test('solving out of order does not skip the unsolved problem', () => {
    assert.strictEqual(nextProblem(TRACKS, solved('b'))?.id, 'a');
    assert.strictEqual(solvedCount(TRACKS[0].milestones[0].problems, solved('b')), 1);
});

test('when everything is solved there is nothing next', () => {
    const isSolved = solved('a', 'b', 'c', 'd', 'e');
    assert.strictEqual(currentMilestone(TRACKS, isSolved), undefined);
    assert.strictEqual(nextProblem(TRACKS, isSolved), undefined);
});

test('lookups and ordering work across tracks', () => {
    assert.strictEqual(findMilestone(TRACKS, 'classes')?.track_id, 'oop');
    assert.strictEqual(findProblem(TRACKS, 'd')?.milestone_id, 'classes');
    assert.strictEqual(findProblem(TRACKS, 'zzz'), undefined);
    assert.strictEqual(milestoneAfter(TRACKS, 'loops')?.id, 'classes');
    assert.strictEqual(milestoneAfter(TRACKS, 'classes'), undefined);
});
