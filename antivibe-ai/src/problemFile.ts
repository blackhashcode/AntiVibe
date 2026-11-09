import { Problem } from './api/antivibeClient';
import { Language, LANGUAGES } from './languages';

// A practice file is recognised by this comment near its top (# in Python, // in C++ and Java)
const MARKER = /^(?:#|\/\/)\s*antivibe-problem:\s*([a-z0-9-]+)\s*$/m;
const MARKER_SEARCH_LINES = 5;
const WRAP_WIDTH = 76;

/** The problem id a practice file belongs to, or undefined for any other file. */
export function findProblemId(text: string): string | undefined {
    const head = text.split(/\r?\n/, MARKER_SEARCH_LINES).join('\n');
    return MARKER.exec(head)?.[1];
}

export function fileNameFor(problem: { id: string }, language: Language = 'python'): string {
    return `${problem.id.replace(/-/g, '_')}${LANGUAGES[language].extension}`;
}

function wrap(text: string, width: number): string[] {
    const lines: string[] = [];
    let current = '';
    for (const word of text.split(/\s+/)) {
        if (current && current.length + 1 + word.length > width) {
            lines.push(current);
            current = word;
        } else {
            current = current ? `${current} ${word}` : word;
        }
    }
    if (current) {
        lines.push(current);
    }
    return lines;
}

/** The file a learner starts from: problem statement as comments, then the starter code. */
export function buildStarter(problem: Problem, language: Language = 'python'): string {
    const marker = LANGUAGES[language].comment;
    const comment = (line: string) => (line ? `${marker} ${line}` : marker);

    // An example can span several lines (setup code, then the checked expression)
    const examples = problem.examples.flatMap((example, index) => [
        ...(index > 0 && example.includes('\n') ? [comment('')] : []),
        ...example.split('\n').map(line => comment(`  ${line}`))
    ]);

    return [
        `${marker} antivibe-problem: ${problem.id}`,
        comment(''),
        comment(`${problem.title}  (${problem.track} - ${problem.milestone})`),
        comment(''),
        ...wrap(problem.description, WRAP_WIDTH).map(comment),
        comment(''),
        comment('Examples:'),
        ...examples,
        comment(''),
        comment('Plan - before any code, write the steps in plain words:'),
        comment('  1.'),
        comment('  2.'),
        comment('  3.'),
        comment('If you cannot write the plan, solve example 1 by hand first and note'),
        comment('what you did. Still stuck? Re-read the lesson, then ask for hint 1.'),
        comment(''),
        comment('Write your solution below. No AI, no copy-paste - that is the point.'),
        comment('  Antivibe: Check My Solution  (Ctrl+Alt+T)    run the tests'),
        comment('  Antivibe: Get Hint           (Ctrl+Shift+H)  reveal the next hint'),
        '',
        problem.starter.trimEnd(),
        ''
    ].join('\n');
}
