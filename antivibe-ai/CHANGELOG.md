# Change Log

All notable changes to the "antivibe-ai" extension will be documented in this file.

Check [Keep a Changelog](http://keepachangelog.com/) for recommendations on how to structure this file.

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
