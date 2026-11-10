# Antivibe.ai

Learn Python, object-oriented programming and data structures & algorithms inside VS Code, one milestone at a time. Read a short lesson, write the solution yourself, run the tests, and unlock hints one level at a time. Antivibe never shows a full solution.

## Features

- **Learning Path** sidebar (the flag in the activity bar) - tracks, milestones, lessons and exercises, with your progress and what is still locked
- **Antivibe: Continue Learning** - opens your next unsolved exercise, and the lesson when a milestone is new
- **Antivibe: Check My Solution** (`Ctrl+Alt+T`) - runs your code against the exercise's tests and shows what passed and what didn't, plus a code review
- **Antivibe: Get Hint** (`Ctrl+Shift+H`) - reveals the next of four hints; in other files, gives a general hint for selected code
- **Antivibe: Choose Language** - switch the Learning Path between Python and C++ (progress is kept per language)
- **Antivibe: Open My History** - opens `antivibe-practice/history.jsonl`, a record of every exercise opened, hint revealed and check run (with your code)
- **Antivibe: Pick an Exercise**, **Antivibe: Open Lesson**, **Antivibe: Refresh Learning Path**, **Antivibe: Reset Progress**

## Requirements

- The Antivibe backend running locally (see the [project README](../README.md))
- Python 3.9+ (it also runs the tests for other languages)
- For C++ exercises: g++ or clang++

## Extension Settings

- `antivibe.apiUrl`: Base URL of the Antivibe backend API (default `http://localhost:8000/api`)
- `antivibe.pythonPath`: Python interpreter used to run your solutions (default `python`)
- `antivibe.lockMilestones`: Keep each milestone locked until the one before it is finished (default `true`)
- `antivibe.language`: `python` or `cpp`
- `antivibe.cppCompiler`: C++ compiler (default `g++`)
- `antivibe.autoSave`: Save exercise files automatically (default `true`)
- `antivibe.practiceFolder`: Where to keep `antivibe-practice/` - default: the open folder, or `~/antivibe` when none is open

## Known Issues

- Solutions can be written in Python and C++; Java is planned.
- Python 3.9 or newer is needed for the code review.
- A solution that takes more than 10 seconds in total is stopped, and the remaining tests are not run.
