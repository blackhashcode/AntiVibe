from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Any, Dict, List, Optional
import enum
import random
import re

from problems import (
    HINT_LABELS, MILESTONES, PROBLEMS, TRACKS, format_example, required_names, starter_code
)

app = FastAPI(title="Antivibe.ai API", version="0.3.0")

# No CORS middleware on purpose: the VS Code extension calls this API from the
# extension host (not a browser page), so it doesn't need CORS, and leaving it
# out stops arbitrary websites from reading this local server.

PROBLEMS_BY_ID = {problem["id"]: problem for problem in PROBLEMS}
MILESTONES_BY_ID = {milestone["id"]: milestone for milestone in MILESTONES}


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

class ProblemSummary(BaseModel):
    id: str
    title: str
    difficulty: str
    track_id: str
    track: str
    milestone_id: str
    milestone: str

class ProblemList(BaseModel):
    problems: List[ProblemSummary]

class FunctionSpec(BaseModel):
    name: str
    params: List[str]

class ProblemDetail(ProblemSummary):
    description: str
    function: Optional[FunctionSpec] = None
    starter: str
    requires: List[str]
    compare: str
    examples: List[str]
    tests: List[Dict[str, Any]]
    hint_count: int

class ProblemHint(BaseModel):
    level: int
    label: str
    hint: str

class ProblemHints(BaseModel):
    problem_id: str
    title: str
    total: int
    hints: List[ProblemHint]
    questions: List[str]
    resources: List[str]
    next_step: str

class LessonSection(BaseModel):
    heading: str
    text: str
    code: Optional[str] = None

class MilestoneSummary(BaseModel):
    id: str
    title: str
    summary: str
    track_id: str
    track: str
    problems: List[ProblemSummary]

class MilestoneDetail(MilestoneSummary):
    lesson: List[LessonSection]

class TrackSummary(BaseModel):
    id: str
    title: str
    description: str
    milestones: List[MilestoneSummary]

class Curriculum(BaseModel):
    tracks: List[TrackSummary]


# ---------------------------------------------------------------------------
# Curriculum
# ---------------------------------------------------------------------------

@app.get("/api/curriculum", response_model=Curriculum)
async def get_curriculum():
    """Tracks, milestones and problem titles, in learning order (no lessons, tests or hints)."""
    return {"tracks": TRACKS}

@app.get("/api/milestones/{milestone_id}", response_model=MilestoneDetail)
async def get_milestone(milestone_id: str):
    milestone = MILESTONES_BY_ID.get(milestone_id)
    if milestone is None:
        raise HTTPException(status_code=404, detail=f"Unknown milestone: {milestone_id}")
    return milestone


# ---------------------------------------------------------------------------
# Practice problems
# ---------------------------------------------------------------------------

# What to do after reading the hint at each level
PROBLEM_NEXT_STEPS = {
    1: "Sit with this idea and try again before asking for more. Sketching an example on paper helps.",
    2: "Try to turn this approach into code on your own. Run the tests to see how far you get.",
    3: "You have the key details now. Write it out and use the failing test cases to guide you.",
    4: "That was the last hint - there is no full solution here. Translate the structure into code line by line.",
}

def get_problem_or_404(problem_id: str) -> dict:
    problem = PROBLEMS_BY_ID.get(problem_id)
    if problem is None:
        raise HTTPException(status_code=404, detail=f"Unknown problem: {problem_id}")
    return problem

@app.get("/api/problems", response_model=ProblemList)
async def list_problems():
    return {"problems": PROBLEMS}

@app.get("/api/problems/{problem_id}", response_model=ProblemDetail)
async def get_problem(problem_id: str):
    problem = get_problem_or_404(problem_id)
    return {
        **problem,
        "starter": starter_code(problem),
        "requires": required_names(problem),
        "examples": [format_example(problem, test) for test in problem["tests"][:2]],
        "hint_count": len(problem["hints"]),
    }

@app.get("/api/problems/{problem_id}/hints", response_model=ProblemHints)
async def get_problem_hints(problem_id: str, upto: int = Query(1, ge=1)):
    """Return hints 1..upto for a problem. Hints are revealed in order."""
    problem = get_problem_or_404(problem_id)
    total = len(problem["hints"])
    upto = min(upto, total)

    return {
        "problem_id": problem["id"],
        "title": problem["title"],
        "total": total,
        "hints": [
            {"level": level, "label": HINT_LABELS[level], "hint": problem["hints"][level - 1]}
            for level in range(1, upto + 1)
        ],
        "questions": problem["questions"],
        "resources": problem.get("resources", []),
        "next_step": PROBLEM_NEXT_STEPS[upto],
    }


# ---------------------------------------------------------------------------
# Free-form hints (for code that isn't one of the practice problems)
# ---------------------------------------------------------------------------

# Add a general hints fallback
GENERAL_HINTS = {
    1: ["Think about the problem step by step. What's the simplest case?", "Consider the time and space complexity of your approach."],
    2: ["Break the problem into smaller subproblems.", "What data structures might be useful here?"],
    3: ["Start with a brute force solution and then optimize.", "Consider edge cases and boundary conditions."],
    4: ["Write pseudocode before implementing.", "Test your solution with sample inputs first."]
}

# Problem type classification: weighted phrases, highest score wins
PROBLEM_KEYWORDS = {
    "two_sum": {"two sum": 3, "two numbers": 2, "add up": 2, "complement": 2, "pair": 1, "target": 1},
    "string_reversal": {"reverse": 2, "reversed": 2, "palindrome": 2, "string": 1},
    "binary_search": {"binary search": 3, "log n": 2, "sorted": 1, "search": 1, "rotated": 1},
    "linked_list": {"linked list": 3, "node": 1, "pointer": 1, "cycle": 1},
}

# A problem type needs at least this score, otherwise the hints are general
MIN_CLASSIFY_SCORE = 2

def classify_problem(description: str) -> str:
    if not description:
        return "general"

    description_lower = description.lower()

    best_type, best_score = "general", 0
    for problem_type, keywords in PROBLEM_KEYWORDS.items():
        score = sum(
            weight for phrase, weight in keywords.items()
            if re.search(rf"\b{re.escape(phrase)}", description_lower)
        )
        if score > best_score:
            best_type, best_score = problem_type, score

    return best_type if best_score >= MIN_CLASSIFY_SCORE else "general"

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
            "Structure: 1) Create a hash map, 2) Loop over the numbers with their indices, 3) Work out the complement of the current number, 4) If the complement is in the map you have your pair, 5) Otherwise remember the current number and its index.",
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
            "Start with left at the first index and right at the last. Loop while the range is non-empty and look at the middle element.",
            "Each comparison with the middle element should discard half the range - make sure you also discard the middle itself.",
            "Handle cases where target is not found, and check your loop on lists of length 0, 1 and 2."
        ],
        4: [
            "Structure: keep left and right; while left <= right: compute mid; if the middle value is the target you're done; if it's too small move left past mid; otherwise move right before mid; if the loop ends the target isn't there.",
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
            "Structure (two pointers): turn the string into a list of characters; put one index at each end; while they haven't met, swap the two characters and move both inwards; join the list back into a string.",
            "Consider edge cases: empty string, single char, palindrome, Unicode characters."
        ]
    },
    "linked_list": {
        1: [
            "Draw the list as boxes and arrows. Which arrows have to change, and in what order?",
            "Think about what you lose access to the moment you overwrite a node's next pointer."
        ],
        2: [
            "Most linked list problems come down to walking the list with one or two pointers.",
            "Two pointers moving at different speeds can find the middle of a list or detect a cycle.",
            "A dummy node in front of the head often removes special cases for the first element."
        ],
        3: [
            "Before changing node.next, save the old next node in a variable so you can keep walking.",
            "Check your loop condition against an empty list and a single-node list.",
            "For fast/slow pointers, make sure fast and fast.next both exist before advancing two steps."
        ],
        4: [
            "Structure for a traversal that rewires pointers: keep prev and current; loop while current exists: remember current.next, repoint current.next, then advance prev and current.",
            "Structure for fast/slow: both start at the head; loop while fast and fast.next exist: slow moves one step, fast moves two; inspect where they end up."
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
    "linked_list": [
        "What happens to your code on an empty list?",
        "Which pointers change, and which node becomes the new head?",
        "Can you solve it with O(1) extra space?",
        "How would you test it without a debugger?"
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
    "linked_list": [
        "https://leetcode.com/explore/learn/card/linked-list/",
        "https://www.geeksforgeeks.org/data-structures/linked-list/",
    ],
    "general": [
        "https://leetcode.com/explore/learn/",
        "https://www.geeksforgeeks.org/data-structures/"
    ]
}

@app.get("/")
async def root():
    return {"message": "Antivibe.ai API is running!", "version": app.version}

@app.post("/api/hint", response_model=HintResponse)
async def get_hint(request: HintRequest):
    # Classify the problem type
    problem_type = classify_problem(request.problem_description)

    # Get hints for the problem type and level
    level_hints = HINT_DATABASE[problem_type][request.hint_level.value]

    # Get questions and resources
    questions = QUESTION_DATABASE[problem_type]
    resources = RESOURCE_DATABASE[problem_type]

    # Next step suggestion
    next_steps = [
        "Try implementing this approach with sample inputs.",
        "Test your solution with edge cases.",
        "Consider how you would explain this solution to someone else.",
        "Think about alternative approaches and compare them."
    ]

    return HintResponse(
        hint=random.choice(level_hints),
        questions=random.sample(questions, min(2, len(questions))),
        resources=random.sample(resources, min(2, len(resources))),
        next_step=random.choice(next_steps)
    )

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "API is working"}

@app.get("/api/problem-types")
async def get_problem_types():
    return {"problem_types": list(HINT_DATABASE.keys())}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
