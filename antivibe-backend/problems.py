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
    quiz      [{"question": ..., "code": ..., "answer": ...}] - "predict the output"
              questions shown after the lesson with the answer hidden. code is optional.
    problems  list of problem dicts, easiest first

A problem is a dict:

    id          unique slug, used in the `# antivibe-problem: <id>` file marker
    title       display name
    difficulty  "warm-up" | "easy" | "medium"
    description what the learner has to write
    function    {"name": ..., "params": [...]} - for problems solved by one function
    starter     starter code. Needed for class-based problems (see requires); for a
                function problem it replaces the empty function - "Debug:" exercises
                start from code with a bug in it.
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

Other languages: an exercise in C++ or Java has a "signature" (see languages.py)
instead of "function", and its snippet tests and starters are written in that
language. Each language has its own curriculum (CURRICULA below); exercises
that exist in several languages share an id.

To add content, edit the curriculum_*.py files and add a reference solution to
tests/reference_solutions*.py; pytest checks the rest.
"""
from typing import Optional

import curriculum_cpp
import curriculum_dsa
import curriculum_oop
import curriculum_python
from languages import cpp_starter, display_value, exception_name, function_name, parse_type

HINT_LABELS = {
    1: "Conceptual nudge",
    2: "Approach",
    3: "Implementation hint",
    4: "Code structure",
}



def assemble(tracks: list) -> dict:
    """Every milestone and problem in learning order, each knowing where it belongs."""
    milestones, problems = [], []
    for track in tracks:
        for milestone in track["milestones"]:
            milestone.update(track_id=track["id"], track=track["title"])
            milestones.append(milestone)
            for problem in milestone["problems"]:
                problem.update(
                    track_id=track["id"],
                    track=track["title"],
                    milestone_id=milestone["id"],
                    milestone=milestone["title"],
                )
                problems.append(problem)
    return {
        "tracks": tracks,
        "milestones": milestones,
        "problems": problems,
        "milestones_by_id": {m["id"]: m for m in milestones},
        "problems_by_id": {p["id"]: p for p in problems},
    }


CURRICULA = {
    "python": assemble([curriculum_python.TRACK, curriculum_oop.TRACK, curriculum_dsa.TRACK]),
    "cpp": assemble(curriculum_cpp.TRACKS),
}

# The Python curriculum, under the names used before there were other languages
TRACKS = CURRICULA["python"]["tracks"]
MILESTONES = CURRICULA["python"]["milestones"]
PROBLEMS = CURRICULA["python"]["problems"]


def starter_code(problem: dict, language: str = "python") -> str:
    """The code a learner starts from: the given starter, or an empty function."""
    if "starter" in problem:
        return problem["starter"].lstrip("\n")
    if language == "cpp":
        return cpp_starter(problem["signature"])
    function = problem["function"]
    return f"def {function['name']}({', '.join(function['params'])}):\n    pass\n"


def required_names(problem: dict) -> list:
    """Names a Python solution must define (compiled languages check this themselves)."""
    if "function" not in problem and "requires" not in problem:
        return []
    return problem.get("requires") or [problem["function"]["name"]]


def _numbers(value):
    if isinstance(value, (list, tuple)):
        for item in value:
            yield from _numbers(item)
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        yield value


def edge_case(test: dict) -> Optional[str]:
    """What kind of edge case a test is, if any.

    A test's own "edge" label wins. Otherwise simple inputs are recognised
    automatically; tests built from setup code need a written label.
    """
    if test.get("edge"):
        return test["edge"]
    if "raises" in test:
        return "invalid input"
    if "args" not in test:
        return None

    args = test["args"]
    if any(arg in ("", [], {}) for arg in args):
        return "empty input"
    if args and isinstance(args[0], str) and not args[0].strip():
        return "only spaces"
    if any(arg == 0 for arg in args if not isinstance(arg, (bool, str, list, dict))):
        return "zero"
    if any(number < 0 for number in _numbers(args)):
        return "negative numbers"
    if any(isinstance(arg, list) and len(arg) == 1 for arg in args) or (
        len(args) == 1 and isinstance(args[0], str) and len(args[0]) == 1
    ):
        return "single item"
    if any(isinstance(arg, list) and len({repr(item) for item in arg}) < len(arg) for arg in args):
        return "repeated values"
    return None


def with_edge_labels(tests: list) -> list:
    """The tests, each carrying its edge-case label (if any) under "edge"."""
    labelled = []
    for test in tests:
        label = edge_case(test)
        labelled.append({**test, "edge": label} if label else test)
    return labelled


def format_example(problem: dict, test: dict, language: str = "python") -> str:
    """A test written the way a learner would type it."""
    signature = problem.get("signature")
    returns = parse_type(signature["returns"]) if signature else None
    if "args" in test:
        if signature:
            types = [parse_type(param[1]) for param in signature["params"]]
            args = ", ".join(display_value(arg, language, types[i]) for i, arg in enumerate(test["args"]))
            call = f"{function_name(signature['name'], language)}({args})"
        else:
            args = ", ".join(repr(arg) for arg in test["args"])
            call = f"{problem['function']['name']}({args})"
    else:
        call = "\n".join(filter(None, [test.get("setup"), test["check"]]))
    if "raises" in test:
        verb = "raises" if language == "python" else "throws"
        return f"{call} -> {verb} {exception_name(test['raises'], language)}"
    return f"{call} -> {display_value(test['expected'], language, returns if 'args' in test else None)}"
