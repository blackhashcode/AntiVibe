"""Checks on the curriculum content itself."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

from problems import HINT_LABELS, MILESTONES, PROBLEMS, TRACKS, required_names, starter_code
from reference_solutions import SOLUTIONS

# The harness the VS Code extension uses to run a learner's code
RUNNER = Path(__file__).resolve().parents[2] / "antivibe-ai" / "runner" / "run_tests.py"

PROBLEM_IDS = [problem["id"] for problem in PROBLEMS]
MILESTONE_IDS = [milestone["id"] for milestone in MILESTONES]


def run_harness(problem, source, tmp_path):
    solution = tmp_path / "solution.py"
    solution.write_text(source)
    spec = {
        "function": problem["function"]["name"] if "function" in problem else None,
        "requires": required_names(problem),
        "compare": problem["compare"],
        "tests": problem["tests"],
    }
    completed = subprocess.run(
        [sys.executable, str(RUNNER), str(solution)],
        input=json.dumps(spec), capture_output=True, text=True, timeout=30,
    )
    return [json.loads(line) for line in completed.stdout.splitlines()]


def test_ids_are_unique_and_usable_in_the_file_marker():
    assert len(set(PROBLEM_IDS)) == len(PROBLEM_IDS)
    assert len(set(MILESTONE_IDS)) == len(MILESTONE_IDS)
    for problem_id in PROBLEM_IDS:
        assert problem_id == problem_id.lower()
        assert all(ch.isalnum() or ch == "-" for ch in problem_id)


def test_tracks_run_from_python_to_oop_to_dsa():
    assert [track["id"] for track in TRACKS] == ["python", "oop", "dsa"]


@pytest.mark.parametrize("milestone", MILESTONES, ids=MILESTONE_IDS)
def test_milestone_is_complete(milestone):
    assert milestone["title"] and milestone["summary"]
    assert len(milestone["problems"]) >= 2
    assert len(milestone["lesson"]) >= 3
    for section in milestone["lesson"]:
        assert section["heading"] and section["text"]
        # backticks mark inline code, so they must come in pairs
        assert section["text"].count("`") % 2 == 0, section["heading"]


@pytest.mark.parametrize("problem", PROBLEMS, ids=PROBLEM_IDS)
def test_problem_is_complete(problem):
    assert len(problem["hints"]) == len(HINT_LABELS)
    assert problem["compare"] in ("exact", "unordered")
    assert problem["difficulty"] in ("warm-up", "easy", "medium")
    assert problem["description"] and problem["questions"]
    assert ("function" in problem) != ("starter" in problem)
    assert len(problem["tests"]) >= 5

    for test in problem["tests"]:
        assert ("expected" in test) != ("raises" in test)
        if "args" in test:
            assert len(test["args"]) <= len(problem["function"]["params"])
        else:
            assert test["check"]


@pytest.mark.parametrize("problem", PROBLEMS, ids=PROBLEM_IDS)
def test_starter_is_valid_python_that_defines_what_is_required(problem):
    namespace = {}
    exec(starter_code(problem), namespace)

    for name in required_names(problem):
        assert callable(namespace[name])


@pytest.mark.parametrize("problem", PROBLEMS, ids=PROBLEM_IDS)
def test_reference_solution_passes_every_test(problem, tmp_path):
    messages = run_harness(problem, SOLUTIONS[problem["id"]], tmp_path)
    cases = [m for m in messages if m["type"] == "case"]

    assert messages[-1] == {"type": "done"}, messages
    assert len(cases) == len(problem["tests"])
    assert [c["status"] for c in cases] == ["pass"] * len(cases), cases


@pytest.mark.parametrize("problem", PROBLEMS, ids=PROBLEM_IDS)
def test_untouched_starter_does_not_pass(problem, tmp_path):
    messages = run_harness(problem, starter_code(problem), tmp_path)
    cases = [m for m in messages if m["type"] == "case"]

    assert len(cases) == len(problem["tests"])
    assert any(c["status"] != "pass" for c in cases)
    # the two tests shown as examples must not pass by accident
    assert all(c["status"] != "pass" for c in cases[:2])
