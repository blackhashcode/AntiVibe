"""Comparing results and explaining wrong answers - shared by every language's runner."""
import json
import sys
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


def case_difference(got, expected):
    """The first pair of strings that differ only in upper/lower case, if that is the only difference."""
    if isinstance(got, str) and isinstance(expected, str):
        return (got, expected) if got != expected and got.lower() == expected.lower() else None
    if isinstance(got, list) and isinstance(expected, list) and len(got) == len(expected):
        found = None
        for g, e in zip(got, expected):
            if same(g, e):
                continue
            pair = case_difference(g, e)
            if pair is None:
                return None  # some other difference too
            found = found or pair
        return found
    return None


def explain_mismatch(got, expected):
    """A plain-language note for wrong answers that are really a wrong kind of value."""
    if got is None:
        return "Your code returned None - did you forget a `return` statement?"
    pair = case_difference(normalize(got), normalize(expected))
    if pair:
        return (
            f"Almost: the only difference is upper/lower case. You wrote {pair[0]!r} where the test "
            f"expects {pair[1]!r}. Python compares text exactly, so these are different strings."
        )
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


def display(value, language="python"):
    """A value written the way the learner's language would show it (JSON-like outside Python)."""
    if language == "python":
        return short_repr(value)
    text = json.dumps(value, ensure_ascii=False)
    return text if len(text) <= MAX_REPR else text[:MAX_REPR] + "..."


def judge(test, outcome, compare, language="python"):
    """Turn what a test produced into a "case" message (without type/index).

    outcome is one of {"got": value} {"raised": name} {"error": text, "line": n} {"timeout": True}
    """
    raises = test.get("raises")
    if "timeout" in outcome:
        return {"status": "timeout"}
    if "error" in outcome:
        return {"status": "error", "error": outcome["error"], "line": outcome.get("line")}
    if "raised" in outcome:
        if raises:
            return {"status": "pass", "got": f"raised {outcome['raised']}"}
        return {"status": "error", "error": f"raised {outcome['raised']}"}
    got = outcome["got"]
    if raises:
        return {
            "status": "fail", "got": display(got, language),
            "note": f"This call should raise {raises}, but it returned normally.",
        }
    passed = matches(got, test["expected"], compare)
    result = {"status": "pass" if passed else "fail", "got": display(got, language)}
    note = None if passed else explain_mismatch(got, test["expected"])
    if note:
        result["note"] = note
    return result
