import { HintResponse, Milestone, Problem, ProblemHints } from './api/antivibeClient';
import { CaseResult, RunResult } from './runner';

export function escapeHtml(value: unknown): string {
    return String(value)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
}

function page(title: string, body: string): string {
    return `<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline';">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>${escapeHtml(title)}</title>
        <style>
            body {
                font-family: var(--vscode-font-family);
                font-size: var(--vscode-font-size);
                color: var(--vscode-foreground);
                padding: 20px;
                line-height: 1.5;
            }
            h1 { font-size: 1.5em; }
            h2 { font-size: 1.1em; margin: 0 0 8px 0; }
            code, pre {
                font-family: var(--vscode-editor-font-family);
                font-size: var(--vscode-editor-font-size);
            }
            pre { margin: 4px 0 0 0; white-space: pre-wrap; word-break: break-word; }
            .card {
                background: var(--vscode-editorWidget-background);
                border: 1px solid var(--vscode-editorWidget-border, transparent);
                border-left-width: 4px;
                padding: 12px 16px;
                border-radius: 6px;
                margin-bottom: 12px;
            }
            .card.pass { border-left-color: var(--vscode-testing-iconPassed, #2ea043); }
            .card.fail, .card.error, .card.timeout { border-left-color: var(--vscode-testing-iconFailed, #f85149); }
            .card.not_run { opacity: 0.6; }
            .edge {
                font-size: 0.8em;
                font-weight: normal;
                color: var(--vscode-descriptionForeground);
                border: 1px solid var(--vscode-editorWidget-border, var(--vscode-descriptionForeground));
                border-radius: 10px;
                padding: 1px 8px;
                margin-left: 6px;
            }
            .card.review { border-left-color: var(--vscode-textLink-foreground); }
            .card.review li { margin: 6px 0; }
            div.quiz {
                background: var(--vscode-editorWidget-background);
                border: 1px solid var(--vscode-editorWidget-border, transparent);
                border-radius: 6px;
                padding: 10px 14px;
                margin: 10px 0;
            }
            div.quiz summary { cursor: pointer; color: var(--vscode-textLink-foreground); margin-top: 8px; }
            div.quiz .answer { margin-top: 6px; }
            .muted { color: var(--vscode-descriptionForeground); }
            .label { color: var(--vscode-descriptionForeground); display: inline-block; min-width: 5.5em; }
            .next-step {
                background: var(--vscode-textBlockQuote-background);
                border-left: 4px solid var(--vscode-textLink-foreground);
                padding: 10px 16px;
                border-radius: 4px;
                margin-top: 15px;
            }
            a { color: var(--vscode-textLink-foreground); }
            code {
                background: var(--vscode-textCodeBlock-background);
                padding: 1px 4px;
                border-radius: 3px;
            }
            pre.block {
                background: var(--vscode-textCodeBlock-background);
                padding: 10px 14px;
                border-radius: 6px;
                margin: 8px 0 0 0;
                overflow-x: auto;
                white-space: pre;
            }
            .lesson h2 { font-size: 1.2em; margin-top: 28px; }
            .lesson p { margin: 8px 0; }
        </style>
    </head>
    <body>
        ${body}
    </body>
    </html>`;
}

function list(items: string[]): string {
    return `<ul>${items.map(item => `<li>${escapeHtml(item)}</li>`).join('')}</ul>`;
}

function resourceList(resources: string[]): string {
    const links = resources.map(r => `<li><a href="${escapeHtml(r)}">${escapeHtml(r)}</a></li>`);
    return `<ul>${links.join('')}</ul>`;
}

function extras(questions: string[], resources: string[], nextStep: string): string {
    return `
        <div class="card">
            <h2>🤔 Questions to Consider</h2>
            ${list(questions)}
        </div>

        ${resources.length > 0 ? `
        <div class="card">
            <h2>📚 Learning Resources</h2>
            ${resourceList(resources)}
        </div>
        ` : ''}

        <div class="next-step">
            <strong>Next Step:</strong> ${escapeHtml(nextStep)}
        </div>`;
}

/** Hints revealed so far for a practice problem. */
export function renderProblemHints(data: ProblemHints): string {
    const hints = data.hints.map(h => `
        <div class="card">
            <h2>💡 Hint ${h.level} of ${data.total}: ${escapeHtml(h.label)}</h2>
            <p>${escapeHtml(h.hint)}</p>
        </div>`).join('');

    return page('Antivibe.ai Hint', `
        <h1>🎯 ${escapeHtml(data.title)}</h1>
        ${hints}
        ${extras(data.questions, data.resources, data.next_step)}`);
}

/** A single hint for code that isn't one of the practice problems. */
export function renderFreeformHint(response: HintResponse): string {
    return page('Antivibe.ai Hint', `
        <h1>🎯 Antivibe.ai Hint</h1>

        <div class="card">
            <h2>💡 Hint</h2>
            <p>${escapeHtml(response.hint)}</p>
        </div>
        ${extras(response.questions, response.resources, response.next_step)}`);
}

/** Escaped text in which `backticks` become inline code. */
function inlineCode(text: string): string {
    return escapeHtml(text).replace(/`([^`]+)`/g, '<code>$1</code>');
}

/** A milestone's lesson, followed by the exercises it leads into. */
export function renderLesson(milestone: Milestone): string {
    const sections = milestone.lesson.map(section => `
        <h2>${escapeHtml(section.heading)}</h2>
        ${section.text.split(/\n\s*\n/).map(paragraph => `<p>${inlineCode(paragraph)}</p>`).join('')}
        ${section.code ? `<pre class="block">${escapeHtml(section.code)}</pre>` : ''}`).join('');

    const paragraphs = (text: string) =>
        text.split(/\n\s*\n/).map(paragraph => `<p>${inlineCode(paragraph)}</p>`).join('');
    // Only the answer sits inside <details>, so the question stays visible while it is closed
    const quiz = milestone.quiz.length === 0 ? '' : `
        <h2>✍️ Check yourself</h2>
        <p class="muted">Work each one out in your head or on paper <em>before</em> opening the answer. Don't run the code - predicting what code does is the skill.</p>
        ${milestone.quiz.map((item, index) => `
            <div class="quiz">
                <strong>${index + 1}.</strong> ${inlineCode(item.question)}
                ${item.code ? `<pre class="block">${escapeHtml(item.code)}</pre>` : ''}
                <details>
                    <summary>Show answer</summary>
                    <div class="answer">${paragraphs(item.answer)}</div>
                </details>
            </div>`).join('')}`;

    return page(milestone.title, `
        <div class="lesson">
            <div class="muted">${escapeHtml(milestone.track)}</div>
            <h1>📖 ${escapeHtml(milestone.title)}</h1>
            <p>${escapeHtml(milestone.summary)}</p>
            ${sections}

            ${quiz}

            <h2>Exercises</h2>
            ${list(milestone.problems.map(problem => problem.title))}
            <div class="next-step">
                <strong>Next Step:</strong> open the first unsolved exercise from the Antivibe sidebar, or run "Antivibe: Continue Learning". Finish every exercise here to unlock the next milestone.
            </div>
        </div>`);
}

const STATUS_TITLES: Record<CaseResult['status'], string> = {
    pass: '✅ Passed',
    fail: '❌ Wrong answer',
    error: '💥 Error',
    timeout: '⏱️ Timed out',
    not_run: '⏭️ Not run'
};

function renderCase(result: CaseResult): string {
    const row = (label: string, value: string) =>
        `<div><span class="label">${label}</span><code>${escapeHtml(value)}</code></div>`;

    // Snippet tests run several lines of code; show those as a block
    const call = result.call.includes('\n')
        ? `<div class="label">Code</div><pre class="block">${escapeHtml(result.call)}</pre>`
        : row('Call', result.call);
    const rows = [call, row('Expected', result.expected)];
    if (result.got !== undefined) {
        rows.push(row('Got', result.got));
    }
    if (result.error) {
        rows.push(row('Error', result.line ? `${result.error} (line ${result.line})` : result.error));
    }
    if (result.status === 'timeout') {
        rows.push('<p class="muted">Your code did not finish in time. Look for a loop that never ends, or an approach that is too slow.</p>');
    }
    if (result.note) {
        rows.push(`<p>💬 ${escapeHtml(result.note)}</p>`);
    }
    if (result.printed) {
        rows.push(`<div class="muted">Your code printed:</div><pre>${escapeHtml(result.printed)}</pre>`);
    }

    return `
        <div class="card ${result.status}">
            <h2>Test ${result.index + 1}: ${STATUS_TITLES[result.status]}${result.edge ? ` <span class="edge">edge case: ${escapeHtml(result.edge)}</span>` : ''}</h2>
            ${rows.join('')}
        </div>`;
}

/** Results of running a solution against a problem's tests. */
export function renderResults(problem: Problem, result: RunResult): string {
    let body: string;

    if (result.loadError) {
        const where = result.loadError.line ? ` (line ${result.loadError.line})` : '';
        body = `
            <div class="card error">
                <h2>💥 Your code could not be run</h2>
                <p><code>${escapeHtml(result.loadError.message)}${where}</code></p>
            </div>`;
    } else {
        const summary = result.allPassed
            ? `🎉 All ${result.total} tests passed!`
            : `${result.passed} of ${result.total} tests passed`;
        const stopped = result.timedOut
            ? '<p class="muted">The run was stopped because it took too long, so some tests did not run.</p>'
            : '';
        body = `
            <p><strong>${summary}</strong></p>
            ${stopped}
            ${result.cases.map(renderCase).join('')}`;
    }

    if (result.review.length > 0) {
        const intro = result.allPassed
            ? 'Your code works. These changes would make it clearer - try them, then check again:'
            : 'Separate from the failing tests, a few things about how the code is written:';
        body += `
            <div class="card review">
                <h2>🧑‍🏫 Code review</h2>
                <p class="muted">${intro}</p>
                <ul>${result.review.map(n => `<li><strong>Line ${n.line}:</strong> ${inlineCode(n.message)}</li>`).join('')}</ul>
            </div>`;
    }

    if (result.allPassed) {
        body += `
            <div class="next-step">
                <strong>Before you move on:</strong> can you explain why your solution works, and what its time and space complexity are?
            </div>`;
    }

    return page('Antivibe.ai Results', `<h1>🧪 ${escapeHtml(problem.title)}</h1>${body}`);
}
