/** The programming languages Antivibe teaches, and what differs between them. */
export type Language = 'python' | 'cpp' | 'java';

export interface LanguageInfo {
    name: string;
    extension: string;
    /** Line comment marker, used for the problem statement in starter files */
    comment: string;
    /** VS Code language ids of files in this language */
    vscodeIds: string[];
    /** Run time allowed for a whole check, including compiling */
    timeoutMs: number;
}

export const LANGUAGES: Record<Language, LanguageInfo> = {
    python: { name: 'Python', extension: '.py', comment: '#', vscodeIds: ['python'], timeoutMs: 10000 },
    cpp: { name: 'C++', extension: '.cpp', comment: '//', vscodeIds: ['cpp', 'c'], timeoutMs: 90000 },
    java: { name: 'Java', extension: '.java', comment: '//', vscodeIds: ['java'], timeoutMs: 90000 }
};

export function isLanguage(value: unknown): value is Language {
    return typeof value === 'string' && value in LANGUAGES;
}

/** The language of a file, from its extension (or VS Code's language id for unsaved files). */
export function languageOfFile(fileName: string, languageId?: string): Language | undefined {
    const lower = fileName.toLowerCase();
    for (const [language, info] of Object.entries(LANGUAGES) as [Language, LanguageInfo][]) {
        if (lower.endsWith(info.extension) || (languageId && info.vscodeIds.includes(languageId))) {
            return language;
        }
    }
    return undefined;
}

/** Progress is kept per language. Python keeps plain ids so earlier progress still counts. */
export function progressKey(problemId: string, language: Language): string {
    return language === 'python' ? problemId : `${language}:${problemId}`;
}

/** Where a language's exercise files live, relative to the workspace folder. */
export function practiceFolder(language: Language): string[] {
    return language === 'python' ? ['antivibe-practice'] : ['antivibe-practice', language];
}
