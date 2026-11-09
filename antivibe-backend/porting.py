"""Building other languages' exercises from the Python ones.

An exercise that exists in several languages shares its id, title, difficulty
and - for function exercises - its test data. What has to be written per
language is everything that mentions syntax: the description, the hints and
the starter code (generated from a signature, or written out for classes).
"""
import copy
import re

import curriculum_dsa
import curriculum_oop
import curriculum_python

PYTHON = {
    problem["id"]: problem
    for track in (curriculum_python.TRACK, curriculum_oop.TRACK, curriculum_dsa.TRACK)
    for milestone in track["milestones"]
    for problem in milestone["problems"]
}

# A Python snippet test like `safe_divide(1, 0)` is valid in any language
PLAIN_CALL = re.compile(r"^[a-z_]+\([^\[\]{}'=]*\)$")


def fn(function_name, returns, /, **params):
    """A signature. A parameter is a type, or (type, default value)."""
    return {
        "name": function_name,
        "returns": returns,
        "params": [[p, *t] if isinstance(t, tuple) else [p, t] for p, t in params.items()],
    }


def port(problem_id, *, hints, description=None, signature=None, tests=None,
         extra_tests=(), drop=(), questions=None, **overrides):
    """A copy of the Python exercise problem_id for another language.

    Its argument tests (and plain-call snippet tests) are kept unless `tests`
    replaces them; `drop` removes kept tests by index and `extra_tests` adds
    tests written in the other language.
    """
    base = PYTHON[problem_id]
    if tests is None:
        tests = [
            copy.deepcopy(test) for test in base["tests"]
            if "args" in test or (not test.get("setup") and PLAIN_CALL.match(test["check"]))
        ]
        tests = [test for i, test in enumerate(tests) if i not in drop]
    assert len(hints) == 4, problem_id

    problem = {
        "id": problem_id,
        "title": base["title"],
        "difficulty": base["difficulty"],
        "description": description or base["description"],
        "compare": base["compare"],
        "tests": list(tests) + list(extra_tests),
        "hints": hints,
        "questions": questions or copy.deepcopy(base["questions"]),
    }
    if base.get("resources"):
        problem["resources"] = list(base["resources"])
    if signature:
        problem["signature"] = signature
    problem.update(overrides)
    return problem
