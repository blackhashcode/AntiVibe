import * as vscode from 'vscode';
import { MilestoneSummary, ProblemSummary, Track } from './api/antivibeClient';
import { blockingMilestone, currentMilestone, isMilestoneComplete, IsSolved, solvedCount } from './curriculum';

type Node =
    | { kind: 'track'; track: Track }
    | { kind: 'milestone'; milestone: MilestoneSummary; number: number }
    | { kind: 'lesson'; milestone: MilestoneSummary }
    | { kind: 'problem'; problem: ProblemSummary };

export interface CurriculumSource {
    /** The curriculum, or undefined when the backend can't be reached. */
    load(): Promise<Track[] | undefined>;
    isSolved: IsSolved;
    lockingEnabled(): boolean;
}

/** The "Learning Path" sidebar: tracks > milestones > lesson and exercises. */
export class CurriculumTreeProvider implements vscode.TreeDataProvider<Node> {
    private readonly changed = new vscode.EventEmitter<void>();
    readonly onDidChangeTreeData = this.changed.event;
    private tracks: Track[] = [];

    constructor(private readonly source: CurriculumSource) {}

    refresh(): void {
        this.changed.fire();
    }

    async getChildren(node?: Node): Promise<Node[]> {
        if (!node) {
            this.tracks = await this.source.load() ?? [];
            return this.tracks.map(track => ({ kind: 'track', track }));
        }
        if (node.kind === 'track') {
            return node.track.milestones.map((milestone, index) => ({ kind: 'milestone', milestone, number: index + 1 }));
        }
        if (node.kind === 'milestone' && !this.isLocked(node.milestone)) {
            return [
                { kind: 'lesson', milestone: node.milestone },
                ...node.milestone.problems.map((problem): Node => ({ kind: 'problem', problem }))
            ];
        }
        return [];
    }

    getTreeItem(node: Node): vscode.TreeItem {
        const { isSolved } = this.source;
        const current = currentMilestone(this.tracks, isSolved);

        switch (node.kind) {
            case 'track': {
                const problems = node.track.milestones.flatMap(milestone => milestone.problems);
                const isCurrentTrack = current?.track_id === node.track.id;
                const item = new vscode.TreeItem(
                    node.track.title,
                    isCurrentTrack ? vscode.TreeItemCollapsibleState.Expanded : vscode.TreeItemCollapsibleState.Collapsed
                );
                item.id = `track:${node.track.id}`;
                item.description = `${solvedCount(problems, isSolved)}/${problems.length}`;
                item.tooltip = node.track.description;
                return item;
            }
            case 'milestone': {
                const { milestone } = node;
                const label = `${node.number}. ${milestone.title}`;
                if (this.isLocked(milestone)) {
                    const item = new vscode.TreeItem(label, vscode.TreeItemCollapsibleState.None);
                    item.id = `milestone:${milestone.id}`;
                    item.iconPath = new vscode.ThemeIcon('lock');
                    item.description = 'locked';
                    item.tooltip = milestone.summary;
                    // Opening a locked lesson explains what has to be finished first
                    item.command = { command: 'antivibe.openLesson', title: 'Open Lesson', arguments: [milestone.id] };
                    return item;
                }
                const complete = isMilestoneComplete(milestone, isSolved);
                const item = new vscode.TreeItem(
                    label,
                    milestone.id === current?.id ? vscode.TreeItemCollapsibleState.Expanded : vscode.TreeItemCollapsibleState.Collapsed
                );
                item.id = `milestone:${milestone.id}`;
                item.iconPath = new vscode.ThemeIcon(complete ? 'pass-filled' : 'circle-large-outline');
                item.description = `${solvedCount(milestone.problems, isSolved)}/${milestone.problems.length}`;
                item.tooltip = milestone.summary;
                return item;
            }
            case 'lesson': {
                const item = new vscode.TreeItem('Lesson', vscode.TreeItemCollapsibleState.None);
                item.id = `lesson:${node.milestone.id}`;
                item.iconPath = new vscode.ThemeIcon('book');
                item.command = { command: 'antivibe.openLesson', title: 'Open Lesson', arguments: [node.milestone.id] };
                return item;
            }
            case 'problem': {
                const item = new vscode.TreeItem(node.problem.title, vscode.TreeItemCollapsibleState.None);
                item.id = `problem:${node.problem.id}`;
                item.iconPath = new vscode.ThemeIcon(isSolved(node.problem.id) ? 'pass-filled' : 'circle-large-outline');
                item.description = node.problem.difficulty;
                item.command = { command: 'antivibe.startProblem', title: 'Start Problem', arguments: [node.problem.id] };
                return item;
            }
        }
    }

    private isLocked(milestone: MilestoneSummary): boolean {
        return this.source.lockingEnabled()
            && blockingMilestone(this.tracks, milestone.id, this.source.isSolved) !== undefined;
    }
}
