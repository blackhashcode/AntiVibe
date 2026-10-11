"""The Antivibe curriculum: tracks -> milestones -> problems.

Tracks are studied in order, and so are the milestones inside them. A milestone
has a short lesson and a few problems; finishing all its problems unlocks the
next milestone.

A milestone is a dict:

    id        unique slug
    title     display name
    summary   one sentence on what it teaches
    lesson    [{"heading": ..., "text": ..., "code": ...}] - code is optional.
              In text, blank lines separate paragraphs and `backticks` mark code.
    problems  list of problem dicts, easiest first

A problem is a dict:

    id          unique slug, used in the `# antivibe-problem: <id>` file marker
    title       display name
    difficulty  "warm-up" | "easy" | "medium"
    description what the learner has to write
    function    {"name": ..., "params": [...]} - for problems solved by one function
    starter     starter code - for problems that need classes instead (see requires)
    requires    names the solution must define (defaults to the function's name)
    compare     "exact" or "unordered" (result order doesn't matter)
    tests       the first two double as examples. Each test is one of:
                  {"args": [...], "expected": ...}        call the function
                  {"setup": code, "check": expr, "expected": ...}
                  {"setup": code, "check": expr, "raises": "ValueError"}
                setup is optional and runs before check is evaluated.
    hints       exactly four, from conceptual nudge to code structure.
                Hints must never contain a complete solution.
    questions   things to think about while (and after) solving
    resources   optional links for further reading

To add content, edit the curriculum_*.py files and add a reference solution to
tests/reference_solutions.py; pytest checks the rest.
"""
import curriculum_dsa
import curriculum_oop
import curriculum_python

HINT_LABELS = {
    1: "Conceptual nudge",
    2: "Approach",
    3: "Implementation hint",
    4: "Code structure",
}

TRACKS = [curriculum_python.TRACK, curriculum_oop.TRACK, curriculum_dsa.TRACK]

# Every milestone and problem in learning order, each knowing where it belongs
MILESTONES = []
PROBLEMS = []
for _track in TRACKS:
    for _milestone in _track["milestones"]:
        _milestone.update(track_id=_track["id"], track=_track["title"])
        MILESTONES.append(_milestone)
        for _problem in _milestone["problems"]:
            _problem.update(
                track_id=_track["id"],
                track=_track["title"],
                milestone_id=_milestone["id"],
                milestone=_milestone["title"],
            )
            PROBLEMS.append(_problem)


def starter_code(problem: dict) -> str:
    """The code a learner starts from: the given starter, or an empty function."""
    if "starter" in problem:
        return problem["starter"]
    function = problem["function"]
    return f"def {function['name']}({', '.join(function['params'])}):\n    pass\n"


def required_names(problem: dict) -> list:
    return problem.get("requires") or [problem["function"]["name"]]


def format_example(problem: dict, test: dict) -> str:
    """A test written the way a learner would type it."""
    if "args" in test:
        args = ", ".join(repr(arg) for arg in test["args"])
        call = f"{problem['function']['name']}({args})"
    else:
        call = "\n".join(filter(None, [test.get("setup"), test["check"]]))
    outcome = f"raises {test['raises']}" if "raises" in test else repr(test["expected"])
    return f"{call} -> {outcome}"
