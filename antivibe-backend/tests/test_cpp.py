"""Checks on the C++ curriculum. The compile-and-run tests need g++ on the PATH."""
import json
import re
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from languages import CPP_HEADER
from problems import CURRICULA, HINT_LABELS, edge_case, format_example, starter_code
from reference_solutions_cpp import SOLUTIONS

RUNNER = Path(__file__).resolve().parents[2] / "antivibe-ai" / "runner" / "run_tests.py"

CPP = CURRICULA["cpp"]
PROBLEMS = CPP["problems"]
PROBLEM_IDS = [p["id"] for p in PROBLEMS]
MILESTONES = CPP["milestones"]
PYTHON_ONLY = [re.compile(p) for p in (r"\.append\(", r"\bNone\b", r"\bself\.", r"\belif\b", r"(?<!_)\brange\(")]
needs_compiler = pytest.mark.skipif(shutil.which("g++") is None, reason="g++ is not installed")


def test_ids_are_unique():
    assert len(set(PROBLEM_IDS)) == len(PROBLEM_IDS)
    milestone_ids = [m["id"] for m in MILESTONES]
    assert len(set(milestone_ids)) == len(milestone_ids)
    # C++ milestone ids must not collide with Python ones
    assert not set(milestone_ids) & set(CURRICULA["python"]["milestones_by_id"])


def test_tracks_run_from_fundamentals_to_oop_to_dsa():
    assert [t["id"] for t in CPP["tracks"]] == ["cpp-fundamentals", "cpp-oop", "cpp-dsa"]


@pytest.mark.parametrize("milestone", MILESTONES, ids=[m["id"] for m in MILESTONES])
def test_milestone_is_complete(milestone):
    assert milestone["title"] and milestone["summary"]
    assert len(milestone["problems"]) >= 2
    assert len(milestone["lesson"]) >= 3
    assert len(milestone["quiz"]) >= 2
    for section in milestone["lesson"]:
        assert section["text"].count("`") % 2 == 0, section["heading"]
    for item in milestone["quiz"]:
        assert item["question"].count("`") % 2 == 0 and item["answer"].count("`") % 2 == 0


@pytest.mark.parametrize("problem", PROBLEMS, ids=PROBLEM_IDS)
def test_problem_is_complete(problem):
    assert len(problem["hints"]) == len(HINT_LABELS)
    assert problem["description"] and problem["questions"]
    assert "signature" in problem or "starter" in problem
    assert "function" not in problem
    assert len(problem["tests"]) >= 4
    assert any(edge_case(test) for test in problem["tests"])
    if problem["title"].startswith("Debug:"):
        assert "starter" in problem
    for test in problem["tests"]:
        assert ("expected" in test) != ("raises" in test)
        if "args" in test:
            assert "signature" in problem
            required = [p for p in problem["signature"]["params"] if len(p) == 2]
            assert len(required) <= len(test["args"]) <= len(problem["signature"]["params"])
    # Python syntax must not leak into C++ hints
    for hint in problem["hints"]:
        for python_only in PYTHON_ONLY:
            assert not python_only.search(hint), (problem["id"], hint)


@pytest.mark.parametrize("problem", PROBLEMS, ids=PROBLEM_IDS)
def test_examples_are_written_for_cpp(problem):
    for test in problem["tests"][:2]:
        example = format_example(problem, test, "cpp")
        assert "True" not in example and "False" not in example and "None" not in example


def test_every_cpp_exercise_has_a_reference_solution():
    assert set(SOLUTIONS) == set(PROBLEM_IDS)


# ---------------------------------------------------------------------------
# Compiling and running (all at once, in parallel, because g++ is slow)
# ---------------------------------------------------------------------------

def run_harness(problem, source, workdir):
    workdir.mkdir(parents=True, exist_ok=True)
    solution = workdir / "solution.cpp"
    solution.write_text(source, encoding="utf-8")
    spec = {
        "language": "cpp",
        "signature": problem.get("signature"),
        "compare": problem["compare"],
        "tests": problem["tests"],
    }
    completed = subprocess.run(
        [sys.executable, str(RUNNER), str(solution)],
        input=json.dumps(spec), capture_output=True, text=True, timeout=300,
    )
    return [json.loads(line) for line in completed.stdout.splitlines()]


@pytest.fixture(scope="module")
def runs(tmp_path_factory):
    root = tmp_path_factory.mktemp("cpp")
    jobs = {}
    for problem in PROBLEMS:
        jobs[(problem["id"], "reference")] = (problem, CPP_HEADER + SOLUTIONS[problem["id"]])
        jobs[(problem["id"], "starter")] = (problem, starter_code(problem, "cpp"))
    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = {
            key: pool.submit(run_harness, problem, source, root / f"{key[0]}-{key[1]}")
            for key, (problem, source) in jobs.items()
        }
        return {key: future.result() for key, future in futures.items()}


@needs_compiler
@pytest.mark.parametrize("problem", PROBLEMS, ids=PROBLEM_IDS)
def test_reference_solution_passes_every_test(problem, runs):
    messages = runs[(problem["id"], "reference")]
    cases = [m for m in messages if m["type"] == "case"]

    assert messages[-1] == {"type": "done"}, messages
    assert [c["status"] for c in cases] == ["pass"] * len(problem["tests"]), cases


@needs_compiler
@pytest.mark.parametrize("problem", PROBLEMS, ids=PROBLEM_IDS)
def test_starter_compiles_but_does_not_pass(problem, runs):
    messages = runs[(problem["id"], "starter")]
    cases = [m for m in messages if m["type"] == "case"]

    assert not any(m["type"] == "load_error" for m in messages), messages
    assert len(cases) == len(problem["tests"])
    assert any(c["status"] != "pass" for c in cases)
    if problem["title"].startswith("Debug:"):
        # a Debug exercise's bug must show in its first example
        assert cases[0]["status"] != "pass"
