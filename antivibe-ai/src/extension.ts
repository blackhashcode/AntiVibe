import * as vscode from 'vscode';
import { AntivibeClient, HintRequest } from './api/antivibeClient';

let antivibeClient: AntivibeClient;

export function activate(context: vscode.ExtensionContext) {
    console.log('Antivibe.ai extension is now active!');
    
    antivibeClient = new AntivibeClient();

    // Register commands
    let getHintCommand = vscode.commands.registerCommand('antivibe.getHint', async () => {
        await getHint();
    });

    let analyzeCodeCommand = vscode.commands.registerCommand('antivibe.analyzeCode', async () => {
        await analyzeCode();
    });

    context.subscriptions.push(getHintCommand, analyzeCodeCommand);
}

async function getHint() {
    const editor = vscode.window.activeTextEditor;
    
    if (!editor) {
        vscode.window.showWarningMessage('No active editor found!');
        return;
    }

    const selection = editor.selection;
    const selectedCode = editor.document.getText(selection);
    
    if (!selectedCode.trim()) {
        vscode.window.showWarningMessage('Please select some code first!');
        return;
    }

    // Show quick pick for hint level
    const hintLevel = await vscode.window.showQuickPick([
        { label: '🚀 Level 1: Conceptual Nudge', level: 1 },
        { label: '💡 Level 2: Algorithm Suggestion', level: 2 },
        { label: '🔧 Level 3: Implementation Hint', level: 3 },
        { label: '🎯 Level 4: Code Structure', level: 4 }
    ], {
        placeHolder: 'Select hint level (higher numbers give more specific hints)'
    });

    if (!hintLevel) {
        return;
    }

    // Get problem description from user
    const problemDescription = await vscode.window.showInputBox({
        prompt: 'Briefly describe the coding problem you\'re solving',
        placeHolder: 'e.g., "Find two numbers that add up to target"'
    });

    if (!problemDescription) {
        return;
    }

    // Show progress notification
    vscode.window.withProgress({
        location: vscode.ProgressLocation.Notification,
        title: "Antivibe.ai is thinking...",
        cancellable: false
    }, async (progress) => {
        progress.report({ increment: 0 });

        try {
            const request: HintRequest = {
                code: selectedCode,
                problemDescription: problemDescription,
                hintLevel: hintLevel.level
            };

            const response = await antivibeClient.getHint(request);
            
            // Display the hint in a new panel
            showHintPanel(response);
            
        } catch (error) {
            vscode.window.showErrorMessage('Failed to get hint from Antivibe.ai');
            console.error(error);
        }
    });
}

async function analyzeCode() {
    vscode.window.showInformationMessage('Code analysis feature coming soon!');
}

function showHintPanel(response: any) {
    // Create and show a new webview panel
    const panel = vscode.window.createWebviewPanel(
        'antivibeHint',
        'Antivibe.ai Hint',
        vscode.ViewColumn.Beside,
        {}
    );

    panel.webview.html = getWebviewContent(response);
}

function getWebviewContent(response: any): string {
    return `
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Antivibe.ai Hint</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                padding: 20px;
                background: #1e1e1e;
                color: #ffffff;
            }
            .hint-container {
                background: #2d2d30;
                padding: 20px;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .questions-section {
                background: #252526;
                padding: 15px;
                border-radius: 8px;
                margin: 15px 0;
            }
            .resource-link {
                color: #4ec9b0;
                text-decoration: none;
            }
            .next-step {
                background: #0e639c;
                padding: 10px;
                border-radius: 4px;
                margin-top: 15px;
            }
        </style>
    </head>
    <body>
        <h1>🎯 Antivibe.ai Hint</h1>
        
        <div class="hint-container">
            <h2>💡 Hint</h2>
            <p>${response.hint}</p>
        </div>

        <div class="questions-section">
            <h2>🤔 Questions to Consider</h2>
            <ul>
                ${response.questions.map((q: string) => `<li>${q}</li>`).join('')}
            </ul>
        </div>

        ${response.resources.length > 0 ? `
        <div class="questions-section">
            <h2>📚 Learning Resources</h2>
            <ul>
                ${response.resources.map((r: string) => `<li><a href="${r}" class="resource-link">${r}</a></li>`).join('')}
            </ul>
        </div>
        ` : ''}

        <div class="next-step">
            <strong>Next Step:</strong> ${response.nextStep}
        </div>
    </body>
    </html>`;
}

export function deactivate() {}