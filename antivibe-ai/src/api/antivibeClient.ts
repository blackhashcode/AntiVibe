export interface HintRequest {
    code: string;
    problemDescription: string;
    errorMessage?: string;
    hintLevel: number;
}

export interface HintResponse {
    hint: string;
    questions: string[];
    resources: string[];
    next_step: string;
}

export interface ProblemSummary {
    id: string;
    title: string;
    difficulty: string;
    track_id: string;
    track: string;
    milestone_id: string;
    milestone: string;
}

/**
 * Either a call of the problem's function (`args`), or a snippet: optional
 * `setup` code followed by a `check` expression. A test expects a value
 * (`expected`) or an exception (`raises`).
 */
export interface TestCase {
    args?: unknown[];
    setup?: string;
    check?: string;
    expected?: unknown;
    raises?: string;
    /** What kind of edge case this test covers, e.g. "empty input" */
    edge?: string;
}

/** The function a learner writes in a compiled language. Types are described in the backend's languages.py */
export interface Signature {
    name: string;
    /** [name, type] or [name, type, default value] */
    params: unknown[][];
    returns: string;
}

export interface Problem extends ProblemSummary {
    language: string;
    description: string;
    /** Set for C++ and Java problems solved by one function */
    signature?: Signature | null;
    /** Set for problems solved by a single function; null for class-based problems */
    function: { name: string; params: string[] } | null;
    /** The code a learner starts from */
    starter: string;
    /** Names the solution has to define */
    requires: string[];
    compare: 'exact' | 'unordered';
    examples: string[];
    tests: TestCase[];
    hint_count: number;
}

export interface ProblemHints {
    problem_id: string;
    title: string;
    total: number;
    hints: { level: number; label: string; hint: string }[];
    questions: string[];
    resources: string[];
    next_step: string;
}

export interface MilestoneSummary {
    id: string;
    title: string;
    summary: string;
    track_id: string;
    track: string;
    problems: ProblemSummary[];
}

export interface LessonSection {
    heading: string;
    text: string;
    code?: string | null;
}

/** A "predict the output" question shown after a lesson, with the answer hidden */
export interface QuizItem {
    question: string;
    code?: string | null;
    answer: string;
}

export interface Milestone extends MilestoneSummary {
    lesson: LessonSection[];
    quiz: QuizItem[];
}

export interface Track {
    id: string;
    title: string;
    description: string;
    milestones: MilestoneSummary[];
}

/** The backend server could not be reached at all (as opposed to returning an error). */
export class BackendUnavailableError extends Error {
    constructor(public readonly baseUrl: string) {
        super(`Antivibe backend is not reachable at ${baseUrl}`);
    }
}

export class AntivibeClient {
    constructor(private readonly getBaseUrl: () => string) {}

    /** Tracks, milestones and problem titles in learning order. */
    async getCurriculum(language: string): Promise<Track[]> {
        const data = await this.request<{ tracks: Track[] }>(`/curriculum?language=${language}`);
        return data.tracks;
    }

    /** The languages the backend has a curriculum for. */
    async getLanguages(): Promise<{ id: string; name: string }[]> {
        const data = await this.request<{ languages: { id: string; name: string }[] }>('/languages');
        return data.languages;
    }

    /** A milestone including its lesson. */
    async getMilestone(milestoneId: string, language: string): Promise<Milestone> {
        return this.request<Milestone>(`/milestones/${encodeURIComponent(milestoneId)}?language=${language}`);
    }

    async getProblem(problemId: string, language: string): Promise<Problem> {
        return this.request<Problem>(`/problems/${encodeURIComponent(problemId)}?language=${language}`);
    }

    /** Hints 1..upTo for a practice problem. */
    async getProblemHints(problemId: string, upTo: number, language: string): Promise<ProblemHints> {
        return this.request<ProblemHints>(
            `/problems/${encodeURIComponent(problemId)}/hints?upto=${upTo}&language=${language}`
        );
    }

    /** Hint for code that isn't one of the practice problems. */
    async getHint(request: HintRequest): Promise<HintResponse> {
        return this.request<HintResponse>('/hint', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                code: request.code,
                problem_description: request.problemDescription,
                error_message: request.errorMessage,
                hint_level: request.hintLevel
            })
        });
    }

    // Test if API is available
    async testConnection(): Promise<boolean> {
        try {
            await this.request('/health');
            return true;
        } catch (error) {
            return false;
        }
    }

    private async request<T>(path: string, init?: RequestInit): Promise<T> {
        const baseUrl = this.getBaseUrl().replace(/\/+$/, '');

        let response: Response;
        try {
            response = await fetch(`${baseUrl}${path}`, init);
        } catch (error) {
            throw new BackendUnavailableError(baseUrl);
        }

        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Antivibe API error: ${response.status} - ${errorText}`);
        }

        return await response.json() as T;
    }
}
