# AntiVibe
### SAY RIP TO VIBE CODING

# Antivibe.ai VS Code Extension

🚀 **Learn to code, don't just copy-paste!** Antivibe.ai takes you from your first Python function to data structures and algorithms, one milestone at a time. You write every line; it gives you lessons, tests your code, and nudges you with hints instead of solutions.

## Features

- 🗺️ **A Learning Path**: three tracks - Python Fundamentals, Object-Oriented Programming, Data Structures & Algorithms - split into 17 milestones
- 📖 **Lessons**: each milestone starts with a short lesson: the concept, examples, and the mistakes beginners make
- 🏋️ **45 Exercises**: each opens as a starter file with an empty function or class for you to fill in
- 🔒 **Milestones Unlock in Order**: solve every exercise in a milestone to open the next one
- 🧪 **Check My Solution**: runs your code against test cases and shows the code that ran, the expected value and what you returned
- 💡 **Progressive Hints**: four hints per exercise, unlocked one at a time - from a conceptual nudge to the code structure, never the full solution
- 🔍 **Free-form Hints**: select any code, describe the problem, and get a hint even outside the learning path

Solutions are written in **Python**.

## Quick Start

### Prerequisites

- VS Code 1.85 or newer
- Node.js (to build the VS Code extension)
- Python 3.8+ (for the backend server and for running your solutions)

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
3. **Read the lesson**, then **write your solution** in the exercise file. Keep the function and class names from the starter code. Exercise files live in `antivibe-practice/` and are never overwritten.
4. **Antivibe: Check My Solution** (`Ctrl+Alt+T`) - runs the tests and opens a results panel. Syntax errors, exceptions (with line numbers), infinite loops and a forgotten `return` are all reported.
5. **Antivibe: Get Hint** (`Ctrl+Shift+H`) - reveals the next hint for the exercise:
   - 🚀 Hint 1: Conceptual nudge
   - 💡 Hint 2: Approach
   - 🔧 Hint 3: Implementation hint
   - 🎯 Hint 4: Code structure
6. When every exercise in a milestone passes, the next milestone unlocks.

Other commands: **Antivibe: Pick an Exercise** (any exercise in an unlocked milestone), **Antivibe: Open Lesson**, **Antivibe: Refresh Learning Path** and **Antivibe: Reset Progress**.

**Free-form hints:** in any file that is not an exercise, select some code and run **Antivibe: Get Hint**. Choose a hint level and describe the problem to get a general hint.

### Settings

- `antivibe.apiUrl` - backend address (default `http://localhost:8000/api`)
- `antivibe.pythonPath` - Python interpreter used to run your solutions (default `python`)
- `antivibe.lockMilestones` - keep milestones locked until the previous one is finished (default on; turn off to open any exercise)

## The Learning Path

### Track 1: Python Fundamentals

| # | Milestone | Exercises |
| --- | --- | --- |
| 1 | Values, Variables & Functions | Rectangle Area, Full Name, Hours and Minutes |
| 2 | Making Decisions | Even or Odd, Sign of a Number, Letter Grade, Leap Year |
| 3 | Loops | Sum to N, Count the Vowels, Fizz Buzz, Reverse a String |
| 4 | Lists | Largest Number, Keep the Evens, Average, Running Total |
| 5 | Strings | Count the Words, Initials, Valid Palindrome |
| 6 | Dictionaries & Sets | Character Count, Contains Duplicate, First Unique Character, Valid Anagram |
| 7 | Functions, Recursion & Errors | Factorial, Safe Divide, Text to Number |

### Track 2: Object-Oriented Programming

| # | Milestone | Exercises |
| --- | --- | --- |
| 1 | Classes & Objects | Counter, Rectangle |
| 2 | Protecting State & Special Methods | Bank Account, Point |
| 3 | Inheritance & Polymorphism | Animal Sounds, Shapes |
| 4 | Building Data Structures | Stack, Queue |

### Track 3: Data Structures & Algorithms

| # | Milestone | Exercises |
| --- | --- | --- |
| 1 | Complexity, Arrays & Hashing | Two Sum, Missing Number |
| 2 | Two Pointers | Merge Two Sorted Lists, Is Subsequence |
| 3 | Stacks in Action | Valid Parentheses, Reverse Polish Notation |
| 4 | Binary Search | Binary Search, First Element At Least X |
| 5 | Linked Lists | Linked List, Reverse a Linked List |
| 6 | From Recursion to Dynamic Programming | Climbing Stairs, Maximum Subarray |

**Adding content:** the tracks live in `antivibe-backend/curriculum_python.py`, `curriculum_oop.py` and `curriculum_dsa.py`; the format is described at the top of `problems.py`. Add a reference solution to `tests/reference_solutions.py`, and `pytest` checks that the lesson and exercise are complete, that the starter code fails, and that the tests can actually be passed.

## API Endpoints

- `GET /api/curriculum` - Tracks, milestones and exercise titles in learning order
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
