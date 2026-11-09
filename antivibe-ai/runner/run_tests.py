"""Antivibe test harness.

Usage:  python run_tests.py <solution.py>      (test spec as JSON on stdin)

The spec looks like:
    {"function": "two_sum" | null, "requires": ["two_sum"],
     "compare": "exact" | "unordered", "tests": [...]}

A test is one of:
    {"args": [...], "expected": ...}                 call spec["function"] with args
    {"setup": "code", "check": "expr", "expected": ...}   run setup, evaluate check
    {"setup": "code", "check": "expr", "raises": "ValueError"}

One JSON object per line is written to stdout, flushed as it happens so the
extension still has partial results if the solution hangs and gets killed:

    {"type": "load_error", "message": ..., "line": ...}
    {"type": "start", "index": i, "call": ..., "expected": ...}
    {"type": "case", "index": i, "status": "pass" | "fail" | "error", ...}
    {"type": "review", "notes": [{"line": ..., "message": ...}]}   style advice, see review.py
    {"type": "done"}
"""
import copy
import io
import json
import os
import runpy
import sys
import traceback

from judge import (
    MAX_PRINTED, emit, explain_mismatch, matches, short_repr,
)
from review import review

def user_line(exc, solution_path):
    """Line number in the learner's file where the exception came from."""
    if isinstance(exc, SyntaxError) and exc.filename and os.path.samefile(exc.filename, solution_path):
        return exc.lineno
    line = None
    for frame in traceback.extract_tb(exc.__traceback__):
        if os.path.exists(frame.filename) and os.path.samefile(frame.filename, solution_path):
            line = frame.lineno
    return line


def describe(exc):
    message = str(exc)
    return f"{type(exc).__name__}: {message}" if message else type(exc).__name__


def is_instance_of_named(exc, class_name):
    """True if exc is an instance of the exception called class_name (or a subclass of it)."""
    return any(cls.__name__ == class_name for cls in type(exc).__mro__)


def display_call(test, function_name):
    if "args" in test:
        return f"{function_name}({', '.join(short_repr(arg) for arg in test['args'])})"
    lines = [test["setup"]] if test.get("setup") else []
    return "\n".join(lines + [test["check"]])


def evaluate(test, function, namespace):
    """Run one test and return the value it produced."""
    if "args" in test:
        return function(*copy.deepcopy(test["args"]))
    scope = dict(namespace)
    if test.get("setup"):
        exec(test["setup"], scope)
    return eval(test["check"], scope)


def main():
    solution_path = sys.argv[1]
    spec = json.load(sys.stdin)
    language = spec.get("language", "python")
    if language == "cpp":
        import cpp_runner
        cpp_runner.run(spec, solution_path)
        return
    if language == "java":
        import java_runner
        java_runner.run(spec, solution_path)
        return
    function_name = spec.get("function")
    compare = spec.get("compare", "exact")

    # Anything the solution prints or reads must not touch the protocol streams
    sys.stdin = io.StringIO("")
    sys.stdout = io.StringIO()

    try:
        namespace = runpy.run_path(solution_path, run_name="antivibe_solution")
    except KeyboardInterrupt:
        raise
    except BaseException as exc:
        emit({
            "type": "load_error",
            "message": f"Your file could not be run. {describe(exc)}",
            "line": user_line(exc, solution_path),
        })
        return

    for name in spec.get("requires", []):
        if not callable(namespace.get(name)):
            emit({
                "type": "load_error",
                "message": f"Could not find a function or class named `{name}`. "
                           "Keep the names from the starter code.",
                "line": None,
            })
            return

    function = namespace.get(function_name) if function_name else None

    for index, test in enumerate(spec["tests"]):
        raises = test.get("raises")
        emit({
            "type": "start",
            "index": index,
            "call": display_call(test, function_name),
            "expected": f"raises {raises}" if raises else short_repr(test["expected"]),
        })

        sys.stdout = printed = io.StringIO()
        result = {"type": "case", "index": index}
        try:
            got = evaluate(test, function, namespace)
        except KeyboardInterrupt:
            raise
        except BaseException as exc:
            if raises and is_instance_of_named(exc, raises):
                result.update(status="pass", got=f"raised {type(exc).__name__}")
            else:
                result.update(status="error", error=describe(exc), line=user_line(exc, solution_path))
        else:
            if raises:
                result.update(status="fail", got=short_repr(got))
                result["note"] = f"This call should raise {raises}, but it returned normally."
            else:
                passed = matches(got, test["expected"], compare)
                result.update(status="pass" if passed else "fail", got=short_repr(got))
                note = None if passed else explain_mismatch(got, test["expected"])
                if note:
                    result["note"] = note

        result["printed"] = printed.getvalue()[:MAX_PRINTED]
        emit(result)

    try:
        notes = review(open(solution_path, encoding="utf-8").read())
    except Exception:  # a review must never break the test run
        notes = []
    emit({"type": "review", "notes": notes})
    emit({"type": "done"})


if __name__ == "__main__":
    main()
