"""What changes between programming languages: starter code and how values are written.

Exercises in compiled languages describe their function with a signature
instead of Python's {"name", "params"}:

    {"name": "two_sum",
     "params": [["nums", "array[int]"], ["target", "int"]],   # optional 3rd item: a default value
     "returns": "array[int]"}

Types:  int  long  float  bool  str  char  array[T]  list[T]  dict[K,V]  set[T]
(array is a fixed-size input, list a growable result - the same in C++, different in Java)
"""
import json

LANGUAGES = {
    "python": {"name": "Python", "extension": ".py", "comment": "#"},
    "cpp": {"name": "C++", "extension": ".cpp", "comment": "//"},
    "java": {"name": "Java", "extension": ".java", "comment": "//"},
}

CPP_HEADER = """#include <algorithm>
#include <cctype>
#include <climits>
#include <cmath>
#include <iostream>
#include <map>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <vector>
using namespace std;
"""

# Names Python tests use for errors, as the other languages spell them
EXCEPTIONS = {
    "cpp": {"ValueError": "invalid_argument", "IndexError": "out_of_range", "KeyError": "out_of_range"},
    "java": {"ValueError": "IllegalArgumentException", "IndexError": "IndexOutOfBoundsException",
             "KeyError": "NoSuchElementException"},
}


def parse_type(text):
    """'dict[char,list[str]]' -> ('dict', [('char', []), ('list', [('str', [])])])"""
    text = text.replace(" ", "")
    if "[" not in text:
        return (text, [])
    name, inner = text[:text.index("[")], text[text.index("[") + 1:-1]
    parts, depth, current = [], 0, ""
    for ch in inner:
        if ch == "," and depth == 0:
            parts.append(current)
            current = ""
            continue
        depth += ch == "["
        depth -= ch == "]"
        current += ch
    parts.append(current)
    return (name, [parse_type(part) for part in parts])


# ---------------------------------------------------------------------------
# C++
# ---------------------------------------------------------------------------

CPP_SCALARS = {"int": "int", "long": "long long", "float": "double", "bool": "bool", "str": "string", "char": "char"}


def cpp_type(t):
    name, args = t
    if name in CPP_SCALARS:
        return CPP_SCALARS[name]
    if name in ("array", "list"):
        return f"vector<{cpp_type(args[0])}>"
    if name == "set":
        return f"set<{cpp_type(args[0])}>"
    if name == "dict":
        return f"map<{cpp_type(args[0])}, {cpp_type(args[1])}>"
    raise ValueError(f"unknown type {name}")


def cpp_value(value, t):
    name, args = t
    if name == "bool":
        return "true" if value else "false"
    if name == "str":
        return json.dumps(value)
    if name == "char":
        return "'" + value + "'"
    if name == "float":
        return repr(float(value))
    return str(value)


def cpp_param(param):
    name, type_text, *default = param
    t = parse_type(type_text)
    written = cpp_type(t)
    # Text and containers are passed by const reference: no copy, and no changing the caller's value
    text = f"const {written}& {name}" if t[0] not in CPP_SCALARS or t[0] == "str" else f"{written} {name}"
    return text + (f" = {cpp_value(default[0], t)}" if default else "")


def cpp_default_return(t):
    name = t[0]
    return {"int": "0", "long": "0", "float": "0.0", "bool": "false", "str": '""', "char": "' '"}.get(name, "{}")


def cpp_starter(signature):
    returns = parse_type(signature["returns"])
    params = ", ".join(cpp_param(p) for p in signature["params"])
    return (
        f"{CPP_HEADER}\n"
        f"{cpp_type(returns)} {signature['name']}({params}) {{\n"
        f"    // your code here\n"
        f"    return {cpp_default_return(returns)};\n"
        f"}}\n"
    )


# ---------------------------------------------------------------------------
# Writing values and calls the way each language reads
# ---------------------------------------------------------------------------

def display_value(value, language, t=None):
    """repr in Python; JSON-like elsewhere ("text", true, [1, 2]), with 'c' for single characters."""
    if language == "python":
        return repr(value)
    if t is not None and t[0] == "char":
        return f"'{value}'"
    return json.dumps(value, ensure_ascii=False)


def function_name(name, language):
    if language == "java":
        first, *rest = name.split("_")
        return first + "".join(word[:1].upper() + word[1:] for word in rest)
    return name


def exception_name(raises, language):
    return EXCEPTIONS.get(language, {}).get(raises, raises)
