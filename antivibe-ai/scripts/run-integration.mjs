// Runs the end-to-end test (out/test/integration) inside your installed VS Code,
// using a throwaway profile so it doesn't touch your settings or extensions.
//
// Before running: start the backend (uvicorn main:app --port 8000).
// Set VSCODE_EXE if VS Code isn't found automatically.
import { execFileSync, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const extensionRoot = resolve(dirname(fileURLToPath(import.meta.url)), '..');

function findVsCode() {
    if (process.env.VSCODE_EXE) {
        return process.env.VSCODE_EXE;
    }
    if (process.platform === 'win32') {
        // `code` on PATH is <install>\bin\code.cmd; the real executable sits one level up
        const launcher = execFileSync('where', ['code.cmd'], { encoding: 'utf8' }).split(/\r?\n/)[0];
        return join(dirname(dirname(launcher)), 'Code.exe');
    }
    if (process.platform === 'darwin') {
        return '/Applications/Visual Studio Code.app/Contents/MacOS/Electron';
    }
    return execFileSync('which', ['code'], { encoding: 'utf8' }).trim();
}

const vscode = findVsCode();
if (!existsSync(vscode)) {
    console.error(`VS Code not found at ${vscode}. Set VSCODE_EXE to its executable.`);
    process.exit(1);
}

const profile = mkdtempSync(join(tmpdir(), 'antivibe-vscode-'));
const workspace = join(profile, 'workspace');
mkdirSync(workspace);
const result = spawnSync(vscode, [
    workspace,
    `--extensionDevelopmentPath=${extensionRoot}`,
    `--extensionTestsPath=${join(extensionRoot, 'out', 'test', 'integration', 'index.js')}`,
    `--user-data-dir=${join(profile, 'user-data')}`,
    `--extensions-dir=${join(profile, 'extensions')}`,
    '--disable-workspace-trust',
    '--skip-welcome',
    '--skip-release-notes'
], { stdio: 'inherit' });

rmSync(profile, { recursive: true, force: true, maxRetries: 5, retryDelay: 200 });

if (result.status === 0) {
    console.log('Integration test passed.');
} else {
    console.error(`Integration test FAILED (exit code ${result.status}).`);
}
process.exit(result.status ?? 1);
