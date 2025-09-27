import axios from 'axios';

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
    nextStep: string;
}

export class AntivibeClient {
    private baseUrl: string;

    constructor() {
        // For now, we'll use a mock URL. Replace with your actual API URL later.
        this.baseUrl = 'http://localhost:8000/api'; // Local development
    }

    async getHint(request: HintRequest): Promise<HintResponse> {
        try {
            // For Day 1, we'll mock the response
            // Replace this with actual API call tomorrow
            return this.mockHintResponse(request);
            
            // Actual implementation (commented out for now):
            // const response = await axios.post(`${this.baseUrl}/hint`, request);
            // return response.data;
        } catch (error) {
            console.error('Error getting hint from Antivibe API:', error);
            return this.getFallbackHint();
        }
    }

    private mockHintResponse(request: HintRequest): HintResponse {
        // Mock responses for testing
        const mockHints = [
            "Think about the time complexity of your current approach. What's the bottleneck?",
            "Consider using a hash map to optimize lookups in this scenario.",
            "Have you considered edge cases like empty input or duplicate values?",
            "This problem pattern is similar to the two-pointer technique. How could you apply it here?"
        ];

        const mockQuestions = [
            "What data structure would help optimize this solution?",
            "How does your solution scale with large inputs?",
            "What's the base case for this recursive approach?"
        ];

        return {
            hint: mockHints[request.hintLevel - 1] || mockHints[0],
            questions: mockQuestions,
            resources: [
                "https://leetcode.com/problems/two-sum/discuss/",
                "https://www.geeksforgeeks.org/data-structures/"
            ],
            nextStep: "Try breaking the problem into smaller subproblems."
        };
    }

    private getFallbackHint(): HintResponse {
        return {
            hint: "Try approaching the problem step by step. What's the simplest case you can solve?",
            questions: ["What part of the problem is most challenging?"],
            resources: [],
            nextStep: "Break the problem down into smaller pieces."
        };
    }
}