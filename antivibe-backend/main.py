from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import enum
import random

app = FastAPI(title="Antivibe.ai API", version="0.1.0")

# CORS middleware to allow VS Code extension to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class HintLevel(int, enum.Enum):
    CONCEPTUAL = 1
    ALGORITHM = 2
    IMPLEMENTATION = 3
    CODE_STRUCTURE = 4

class HintRequest(BaseModel):
    code: str
    problem_description: str
    error_message: Optional[str] = None
    hint_level: HintLevel

class HintResponse(BaseModel):
    hint: str
    questions: List[str]
    resources: List[str]
    next_step: str

# Add a general hints fallback
GENERAL_HINTS = {
    1: ["Think about the problem step by step. What's the simplest case?", "Consider the time and space complexity of your approach."],
    2: ["Break the problem into smaller subproblems.", "What data structures might be useful here?"],
    3: ["Start with a brute force solution and then optimize.", "Consider edge cases and boundary conditions."],
    4: ["Write pseudocode before implementing.", "Test your solution with sample inputs first."]
}

# Problem type classification (simple keyword matching)
def classify_problem(description: str, code: str) -> str:
    if not description:
        return "general"
    
    description_lower = description.lower()
    
    if any(word in description_lower for word in ['sum', 'add', 'two numbers', 'target']):
        return "two_sum"
    elif any(word in description_lower for word in ['reverse', 'palindrome', 'string']):
        return "string_reversal"
    elif any(word in description_lower for word in ['binary', 'search', 'sorted', 'array']):
        return "binary_search"
    elif any(word in description_lower for word in ['linked list', 'node', 'pointer']):
        return "linked_list"
    else:
        return "general"

# Hard-coded hints database
HINT_DATABASE = {
    "two_sum": {
        1: [
            "Think about how you can efficiently find if a number's complement exists in the array.",
            "Consider what data structure allows fast lookups.",
            "What's the time complexity of checking every pair?"
        ],
        2: [
            "A hash map can reduce the lookup time from O(n) to O(1).",
            "Try storing each number's index as you iterate through the array.",
            "For each number, calculate what other number you need to reach the target."
        ],
        3: [
            "Initialize an empty dictionary. For each number, check if (target - current) exists in the dictionary.",
            "Iterate with enumerate to get both index and value. Return indices when complement is found.",
            "Handle edge cases: empty array, no solution, duplicate numbers."
        ],
        4: [
            "Algorithm: 1) Create hash map, 2) For i, num in enumerate(nums), 3) complement = target - num, 4) If complement in map, return [map[complement], i], 5) Else map[num] = i",
            "Time: O(n), Space: O(n). Consider what happens with duplicates and why the order matters."
        ]
    },
    "binary_search": {
        1: [
            "This problem can be solved efficiently using divide and conquer.",
            "Think about how you can repeatedly halve the search space.",
            "What condition tells you which half to search next?"
        ],
        2: [
            "The array must be sorted for binary search to work.",
            "Use two pointers: left (start) and right (end) of the search space.",
            "Calculate the middle index and compare with target."
        ],
        3: [
            "Initialize left=0, right=len(arr)-1. While left <= right, calculate mid = (left+right)//2.",
            "If arr[mid] == target: return mid. If arr[mid] < target: left = mid+1, else right = mid-1.",
            "Handle cases where target is not found and avoid integer overflow with mid calculation."
        ],
        4: [
            "Template: left, right = 0, n-1; while left <= right: mid = left + (right-left)//2; if nums[mid]==target: return mid; elif nums[mid]<target: left=mid+1; else: right=mid-1; return -1",
            "Consider variations: first/last occurrence, search in rotated array, infinite array."
        ]
    },
    "string_reversal": {
        1: [
            "Think about different ways to reverse a string without built-in functions.",
            "Consider the time and space complexity of each approach.",
            "How would you handle Unicode characters or special cases?"
        ],
        2: [
            "You can use two pointers: one starting from beginning, one from end.",
            "A stack data structure naturally reverses order (LIFO).",
            "Recursion can also reverse strings by processing substrings."
        ],
        3: [
            "Two-pointer: convert to list (strings immutable), left=0, right=len-1, swap until left>=right.",
            "Stack: push all chars, then pop to build reversed string.",
            "Pythonic: s[::-1] but understand how it works internally."
        ],
        4: [
            "Two-pointer: def reverse_string(s): chars = list(s); l, r = 0, len(chars)-1; while l < r: chars[l], chars[r] = chars[r], chars[l]; l += 1; r -= 1; return ''.join(chars)",
            "Consider edge cases: empty string, single char, palindrome, Unicode characters."
        ]
    },
    "general": GENERAL_HINTS
}

# Common questions and resources
QUESTION_DATABASE = {
    "two_sum": [
        "What's the time complexity of the brute force approach?",
        "How does the hash map solution improve performance?",
        "What if the array has duplicate numbers?",
        "How would you handle multiple solutions?"
    ],
    "binary_search": [
        "Why must the array be sorted for binary search?",
        "What's the difference between iterative and recursive binary search?",
        "How do you avoid integer overflow when calculating mid?",
        "What are the edge cases for binary search?"
    ],
    "string_reversal": [
        "What's the most efficient way to reverse a string?",
        "How does string immutability affect the solution?",
        "What's the time and space complexity of each approach?",
        "How would you reverse words in a sentence?"
    ],
    "general": [
        "What's the time complexity of your approach?",
        "How would you handle edge cases?",
        "What's the most challenging part of this problem?",
        "How could you test your solution?"
    ]
}

RESOURCE_DATABASE = {
    "two_sum": [
        "https://leetcode.com/problems/two-sum/",
        "https://www.geeksforgeeks.org/given-an-array-a-and-a-number-x-check-for-pair-in-a-with-sum-as-x/",
    ],
    "binary_search": [
        "https://leetcode.com/explore/learn/card/binary-search/",
        "https://www.geeksforgeeks.org/binary-search/",
    ],
    "string_reversal": [
        "https://leetcode.com/problems/reverse-string/",
        "https://www.geeksforgeeks.org/reverse-string-python-5-different-ways/",
    ],
    "general": [
        "https://leetcode.com/explore/learn/",
        "https://www.geeksforgeeks.org/data-structures/"
    ]
}

@app.get("/")
async def root():
    return {"message": "Antivibe.ai API is running!", "version": "0.1.0"}

@app.post("/api/hint", response_model=HintResponse)
async def get_hint(request: HintRequest):
    try:
        print(f"Received request: {request}")  # Debug log
        
        # Classify the problem type
        problem_type = classify_problem(request.problem_description, request.code)
        print(f"Classified as: {problem_type}")  # Debug log
        
        # Get hints for the problem type and level
        hints = HINT_DATABASE.get(problem_type, HINT_DATABASE["general"])
        level_hints = hints.get(request.hint_level.value, hints[1])  # Use .value for enum
        
        # Select a random hint
        selected_hint = random.choice(level_hints) if level_hints else "Think about the problem step by step."
        
        # Get questions and resources
        questions = QUESTION_DATABASE.get(problem_type, QUESTION_DATABASE["general"])
        resources = RESOURCE_DATABASE.get(problem_type, RESOURCE_DATABASE["general"])
        
        # Next step suggestion
        next_steps = [
            "Try implementing this approach with sample inputs.",
            "Test your solution with edge cases.",
            "Consider how you would explain this solution to someone else.",
            "Think about alternative approaches and compare them."
        ]
        
        response = HintResponse(
            hint=selected_hint,
            questions=random.sample(questions, min(2, len(questions))),
            resources=random.sample(resources, min(2, len(resources))),
            next_step=random.choice(next_steps)
        )
        
        print(f"Sending response: {response}")  # Debug log
        return response
        
    except Exception as e:
        print(f"Error: {str(e)}")  # Debug log
        raise HTTPException(status_code=500, detail=f"Error generating hint: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is working"}

@app.get("/api/problem-types")
async def get_problem_types():
    return {"problem_types": list(HINT_DATABASE.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)