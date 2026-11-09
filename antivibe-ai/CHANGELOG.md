# Change Log

All notable changes to the "antivibe-ai" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

## [0.4.0]

### Added

- C++: a full learning path - C++ Fundamentals, Object-Oriented C++, and DSA in C++ - with lessons, quizzes and 82 exercises
- C++-specific Debug exercises (integer division, `=` vs `==`, copies vs references, name hiding, missing `virtual`)
- C++ solutions are compiled with g++ and each test runs in its own process, so a crash fails only that test
- "Antivibe: Choose Language" and the `antivibe.language` setting; progress is kept separately per language
- A Binary Search Trees milestone in the Python and C++ DSA tracks: insert and search, in-order traversal, height, validating a BST (Debug) and removal

### Fixed

- The Fibonacci test used fib(80), which JavaScript rounds; it now uses fib(70), and a test guards against unsafe numbers

## [0.3.0]

### Added

- Code review in the results panel: notes on how the code is written, with line numbers
- "Check yourself" questions at the end of every lesson
- "Debug" exercises that start from buggy code
- A Plan section in every starter file, and a problem-solving method in the first lesson
- A Recursion milestone and 31 new exercises, mostly small steps in the Python track
- Edge-case labels on tests, shown in the results panel; every exercise tests at least one edge case
- A learning history in `antivibe-practice/history.jsonl`, and "Antivibe: Open My History"

### Changed

- Exercises added to earlier milestones no longer re-lock milestones you have already reached
- Hints for Reverse a String, Valid Palindrome and Valid Anagram now use only what the lessons teach

## [0.2.0]

### Added

- Milestone-based learning path: Python Fundamentals, Object-Oriented Programming, and Data Structures & Algorithms
- "Learning Path" sidebar showing tracks, milestones, lessons, exercises and progress
- Lessons for every milestone ("Antivibe: Open Lesson")
- "Antivibe: Continue Learning" jumps to the next unsolved exercise
- Milestones unlock in order (`antivibe.lockMilestones` turns this off)
- Class-based exercises, and tests that expect an error to be raised

### Changed

- "Antivibe: Start Practice Problem" is now "Antivibe: Pick an Exercise"
- Practice files are named after the exercise instead of its function

## [0.1.0]

### Added

- Practice problems: "Antivibe: Start Practice Problem" opens a starter file from the backend's problem bank
- "Antivibe: Check My Solution" runs a solution against the problem's tests
- Progressive hints for practice problems, unlocked one level at a time
- Progress tracking and "Antivibe: Reset Progress"
- `antivibe.apiUrl` and `antivibe.pythonPath` settings

### Fixed

- "Next Step" in the hint panel showed `undefined`
- Hint text is now escaped before being shown

### Removed

- "Antivibe: Analyze Code" placeholder command

## [0.0.1]

- Initial release
