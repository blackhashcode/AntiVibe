# AntiVibe
### SAY RIP TO VIBE CODING

# Antivibe.ai VS Code Extension

🚀 **Learn to code, don't just copy-paste!** Antivibe.ai takes you from your first Python function to data structures and algorithms, one milestone at a time. You write every line; it gives you lessons, tests your code, and nudges you with hints instead of solutions.

## Features

- 🗺️ **A Learning Path**: three tracks - Python Fundamentals, Object-Oriented Programming, Data Structures & Algorithms - split into 19 milestones
- 📖 **Lessons**: each milestone starts with a short lesson - the concept, examples, and the mistakes beginners make - and ends with "Check yourself" questions: predict what a piece of code does, then reveal the answer
- 🏋️ **81 Exercises**: each opens as a starter file with a Plan section and an empty function or class to fill in. "Debug" exercises start from buggy code for you to fix
- 🔒 **Milestones Unlock in Order**: solve every exercise in a milestone to open the next one
- 🧪 **Check My Solution**: runs your code against test cases and shows the code that ran, the expected value and what you returned
- 🧑‍🏫 **Code Review**: after each check, notes on how the code is written - looping over positions instead of items, `if ...: return True else: return False`, changing a list you were given, and more
- 🧱 **Edge Cases Called Out**: tests that cover an edge case - empty input, zero, negative numbers, a single item, invalid input, a brand-new object - are labelled in the results, so you learn to think of them yourself
- 📈 **Learning History**: every exercise opened, lesson read, hint revealed and check run is appended to `antivibe-practice/history.jsonl`, with your code and the results, for analysing your progress later
- 💡 **Progressive Hints**: four hints per exercise, unlocked one at a time - from a conceptual nudge to the code structure, never the full solution
- 🔍 **Free-form Hints**: select any code, describe the problem, and get a hint even outside the learning path

Solutions can be written in **Python** or **C++** (Java is planned). Each language has its own learning path - fundamentals, OOP and DSA - with lessons written for that language, and progress is kept separately for each. Pick one with the 🌐 button at the top of the Learning Path.

## Quick Start

### Prerequisites

- VS Code 1.85 or newer
- Node.js (to build the VS Code extension)
- Python 3.9+ (for the backend server and for running your solutions)
- For C++: g++ (or clang++) on the PATH - on Windows, for example from MSYS2

### Installation & Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd AntiVibe
```

2. **Setup Backend Server**
```bash
cd antivibe-backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Setup VS Code Extension**
```bash
cd antivibe-ai
npm install
```

### Running the Application

1. **Start the Backend Server** (Terminal 1):
```bash
cd antivibe-backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
uvicorn main:app --reload --port 8000
```

2. **Run the VS Code Extension**: open the `antivibe-ai` folder in VS Code, run `npm run compile`, then press `F5` to launch the extension development window. Open a folder in that window so your practice files have somewhere to live.

### Usage

1. Click the **Antivibe flag** in the activity bar (far left) to open the **Learning Path**. It shows every track and milestone, what you have solved, and what is still locked.
2. Press the **▶ Continue Learning** button at the top of the Learning Path (or run `Antivibe: Continue Learning` from the Command Palette, `Ctrl+Shift+P`). It opens your next unsolved exercise - and the lesson, when you start a new milestone.
3. **Read the lesson** and answer its "Check yourself" questions, then **write a plan and your solution** in the exercise file. Keep the function and class names from the starter code. Exercise files live in `antivibe-practice/` and are never overwritten.
4. **Antivibe: Check My Solution** (`Ctrl+Alt+T`) - runs the tests and opens a results panel. Syntax errors, exceptions (with line numbers), infinite loops and a forgotten `return` are all reported.
5. **Antivibe: Get Hint** (`Ctrl+Shift+H`) - reveals the next hint for the exercise:
   - 🚀 Hint 1: Conceptual nudge
   - 💡 Hint 2: Approach
   - 🔧 Hint 3: Implementation hint
   - 🎯 Hint 4: Code structure
6. When every exercise in a milestone passes, the next milestone unlocks.

Other commands: **Antivibe: Pick an Exercise** (any exercise in an unlocked milestone), **Antivibe: Open Lesson**, **Antivibe: Open My History**, **Antivibe: Refresh Learning Path** and **Antivibe: Reset Progress**.

**Your history:** `antivibe-practice/history.jsonl` gets one line (a JSON object) per event: `open`, `lesson`, `hint`, `check` (attempt number, hints used so far, each test's result and edge case, the code-review notes and your code) and `large_insert` (80+ characters arriving in one go, which is usually a paste). It stays on your machine; delete the file to start a fresh history.

**Free-form hints:** in any file that is not an exercise, select some code and run **Antivibe: Get Hint**. Choose a hint level and describe the problem to get a general hint.

### Settings

- `antivibe.apiUrl` - backend address (default `http://localhost:8000/api`)
- `antivibe.pythonPath` - Python interpreter used to run your solutions (default `python`)
- `antivibe.lockMilestones` - keep milestones locked until the previous one is finished (default on; turn off to open any exercise)
- `antivibe.language` - the language the Learning Path shows: `python` or `cpp`
- `antivibe.cppCompiler` - the C++ compiler (default `g++`)

## The Learning Path

### Track 1: Python Fundamentals

| # | Milestone | Exercises |
| --- | --- | --- |
| 1 | Values, Variables & Functions | Rectangle Area, Full Name, Debug: Average of Two, Hours and Minutes |
| 2 | Making Decisions | Even or Odd, Sign of a Number, Letter Grade, Leap Year |
| 3 | Loops | Sum to N, Sum of the Evens, Count a Character, Count the Vowels, Debug: Has a Digit, Sum of Digits, Reverse a String |
| 4 | Lists | Largest Number, Index Of, Keep the Evens, Average, Fizz Buzz, Running Total, Debug: Remove the Negatives |
| 5 | Strings | Count the Words, Capitalise Each Word, Initials, Palindrome Word, Longest Word, Debug: Remove the Spaces, Valid Palindrome |
| 6 | Dictionaries & Sets | Character Count, Count the Different Values, Contains Duplicate, First Unique Character, Most Common Character, Valid Anagram, Group by First Letter |
| 7 | Functions & Errors | Safe Divide, Text to Number, Parse the Scores, Primes (Two Functions) |
| 8 | Recursion | Factorial, Power, Debug: Count Down, Sum a List Recursively, Reverse a String Recursively |

### Track 2: Object-Oriented Programming

| # | Milestone | Exercises |
| --- | --- | --- |
| 1 | Classes & Objects | Counter, Debug: Light Switch, Rectangle, Playlist |
| 2 | Protecting State & Special Methods | Bank Account, Point, Inventory |
| 3 | Inheritance & Polymorphism | Animal Sounds, Debug: Vehicles, Shapes |
| 4 | Building Data Structures | Stack, Queue, Text Editor with Undo |

### Track 3: Data Structures & Algorithms

| # | Milestone | Exercises |
| --- | --- | --- |
| 1 | Complexity, Arrays & Hashing | Pair With Sum, Two Sum, Missing Number |
| 2 | Two Pointers | Pair Sum in a Sorted List, Merge Two Sorted Lists, Is Subsequence |
| 3 | Stacks in Action | Valid Parentheses, Remove Adjacent Duplicates, Reverse Polish Notation |
| 4 | Binary Search | Binary Search, Whole Square Root, First Element At Least X |
| 5 | Linked Lists | Search a Linked List, Linked List, Reverse a Linked List |
| 6 | Binary Search Trees | Insert and Search, In-Order Traversal, Height, Minimum and Maximum, Debug: Is It a BST?, Remove a Value |
| 7 | From Recursion to Dynamic Programming | Fibonacci, Fast, Climbing Stairs, Maximum Subarray |

**Debug exercises** start from code that almost works. Your job is to trace it, find the bug and fix it - the skill you need most when your own code fails.

**Adding content:** the tracks live in `antivibe-backend/curriculum_python.py`, `curriculum_oop.py` and `curriculum_dsa.py`; the format is described at the top of `problems.py`. Add a reference solution to `tests/reference_solutions.py`, and `pytest` checks that the lesson and exercise are complete, that the starter code fails, and that the tests can actually be passed.

## API Endpoints

- `GET /api/languages` - Languages with a curriculum
- `GET /api/curriculum?language=cpp` - Tracks, milestones and exercise titles in learning order (all exercise routes take `?language=`, default `python`)
- `GET /api/milestones/{id}` - A milestone with its lesson
- `GET /api/problems` - List all exercises
- `GET /api/problems/{id}` - Statement, starter code, examples and test cases
- `GET /api/problems/{id}/hints?upto=N` - Hints 1 to N for an exercise
- `POST /api/hint` - Free-form hint for a described problem
- `GET /api/health` - Check server status
- `GET /api/problem-types` - Problem types the free-form hints recognise

## Project Structure

```
AntiVibe/
├── antivibe-backend/           # FastAPI server
│   ├── main.py                 # API
│   ├── problems.py             # Assembles the curriculum; describes the content format
│   ├── curriculum_python.py    # Track 1: lessons, exercises, tests, hints
│   ├── curriculum_oop.py       # Track 2
│   ├── curriculum_dsa.py       # Track 3
│   ├── classic_problems.py     # Classic algorithm problems used by the tracks
│   ├── tests/                  # pytest suite
│   └── requirements.txt        # Python dependencies
└── antivibe-ai/                # VS Code extension
    ├── src/
    │   ├── extension.ts        # Commands
    │   ├── api/                # Backend client
    │   ├── curriculum.ts       # Milestone progress and locking rules
    │   ├── tree.ts             # Learning Path sidebar
    │   ├── problemFile.ts      # Starter files
    │   ├── runner.ts           # Runs solutions against tests
    │   ├── views.ts            # Lesson, hint and results panels
    │   └── test/               # Unit and end-to-end tests
    ├── runner/run_tests.py     # Python test harness
    └── package.json            # Extension config
```

Your solution runs on your own machine, in a separate Python process started by the extension (stopped after 10 seconds). The backend never executes code. Progress is stored by VS Code on your machine.

## Development

**Backend:**
```bash
cd antivibe-backend
pip install -r requirements-dev.txt
pytest
```

**Extension:**
```bash
cd antivibe-ai
npm run watch              # Auto-compile on changes, press F5 to debug
npm test                   # Unit tests
npm run test:integration   # End-to-end test in a real VS Code window (backend must be running)
```

## Troubleshooting

**"Antivibe can't reach its backend"?**
- Check if backend is running on port 8000
- Verify `curl http://localhost:8000/api/health` works
- If it runs elsewhere, set `antivibe.apiUrl`
- Press the refresh button at the top of the Learning Path once it is running

**"Could not start Python"?**
- Make sure `python --version` works in a terminal
- Otherwise set `antivibe.pythonPath` to your interpreter (e.g. `python3` or a full path)

**A lesson, hint or results panel is blank?**
- Run `Developer: Reload Window`, or close every VS Code window and start again

**Extension not working?**
- Check Developer Tools (Help → Toggle Developer Tools)
- Verify `npm run compile` succeeds

## What's Next

- More milestones (trees, graphs, sorting, file handling)
- Hints that react to your code and your failing tests
- More programming languages

## Contributing

This is an early prototype! Feel free to suggest features or report issues.

---

**Remember**: The goal is understanding, not just solving! 🧠

*Backend server must be running for lessons, exercises and hints to work!*
