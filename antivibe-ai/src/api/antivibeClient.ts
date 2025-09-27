import * as vscode from 'vscode';

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

export class AntivibeClient {
    private baseUrl: string;

    constructor() {
        // Use localhost for development
        this.baseUrl = 'http://localhost:8000/api';
    }

    async getHint(request: HintRequest): Promise<HintResponse> {
        try {
            console.log('Sending request to Antivibe API:', request);
            
            const response = await fetch(`${this.baseUrl}/hint`, {
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

            console.log('API response status:', response.status);
            
            if (!response.ok) {
                const errorText = await response.text();
                console.error('API error details:', errorText);
                throw new Error(`API error: ${response.status} - ${errorText}`);
            }

            const data = await response.json();
            console.log('API response data:', data);
            return data;
            
        } catch (error) {
            console.error('Error calling Antivibe API:', error);
            vscode.window.showWarningMessage(
                'Antivibe API not available. Using fallback hints. Make sure the backend server is running on localhost:8000'
            );
            return this.getFallbackHint();
        }
    }

    // Test if API is available
    async testConnection(): Promise<boolean> {
        try {
            const response = await fetch(`${this.baseUrl}/health`);
            return response.ok;
        } catch (error) {
            return false;
        }
    }

    private getFallbackHint(): HintResponse {
        return {
            hint: "Try breaking the problem down into smaller subproblems. What's the simplest case you can solve first?",
            questions: ["What part of the problem is most challenging right now?"],
            resources: ["https://leetcode.com/explore/learn/"],
            next_step: "Start with a brute force solution, then optimize."
        };
    }
}