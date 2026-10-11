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
    {"type": "done"}
"""
import copy
import io
import json
import os
import runpy
import sys
import traceback
import types

REAL_STDOUT = sys.stdout
MAX_REPR = 300
MAX_PRINTED = 2000


def emit(message):
    REAL_STDOUT.write(json.dumps(message) + "\n")
    REAL_STDOUT.flush()


def short_repr(value):
    text = repr(value)
    return text if len(text) <= MAX_REPR else text[:MAX_REPR] + "..."


def normalize(value):
    """Treat tuples as lists so returning (0, 1) is as good as [0, 1]."""
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    return value


def same(got, expected):
    # bool is a subclass of int in Python; don't let 1 pass for True
    if isinstance(got, bool) or isinstance(expected, bool):
        return type(got) is type(expected) and got == expected
    if isinstance(expected, list):
        return (
            isinstance(got, list)
            and len(got) == len(expected)
            and all(same(g, e) for g, e in zip(got, expected))
        )
    return got == expected


def matches(got, expected, compare):
    got, expected = normalize(got), normalize(expected)
    if compare == "unordered" and isinstance(got, list) and isinstance(expected, list):
        try:
            return same(sorted(got), sorted(expected))
        except TypeError:
            return False
    return same(got, expected)


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


def explain_mismatch(got, expected):
    """A plain-language note for wrong answers that are really a wrong kind of value."""
    if got is None:
        return "Your code returned None - did you forget a `return` statement?"
    if isinstance(got, types.GenericAlias):
        # e.g. `return list[a, b]`, which looks like a list when printed but is a type description
        name = got.__origin__.__name__
        return (
            f"`{short_repr(got)}` is not a {name} - putting square brackets straight after the word "
            f"`{name}` describes a type instead of making a value. "
            f"Write the values without the word `{name}` in front."
        )
    got, expected = normalize(got), normalize(expected)
    both_numbers = isinstance(got, (int, float)) and isinstance(expected, (int, float))
    if type(got) is not type(expected) and not both_numbers:
        return (
            f"The test expects a {type(expected).__name__}, "
            f"but your code returned a {type(got).__name__}."
        )
    return None


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

    emit({"type": "done"})


if __name__ == "__main__":
    main()
