"""Run a C++ solution against an exercise's tests.

A test driver is generated next to the learner's file: it #includes the
solution, and for test number i runs that test only and writes the outcome to
a result file. Every test runs in its own process, so a crash (a bad pointer,
an index out of range) only fails that test.

Tests are the usual Antivibe tests. `args` tests call the function described
by spec["signature"]; snippet tests hold C++ code: `setup` statements and a
`check` expression. `raises` names a standard exception type, e.g.
"invalid_argument" (Python names like ValueError are translated).
"""
import json
import os
import re
import subprocess
import tempfile
import time

import typespec
from judge import MAX_PRINTED, display, emit, judge

COMPILE_TIMEOUT = 60
CASE_TIMEOUT = 3
TOTAL_BUDGET = 40

PYTHON_EXCEPTIONS = {
    "ValueError": "invalid_argument",
    "IndexError": "out_of_range",
    "KeyError": "out_of_range",
}

SCALARS = {"int": "int", "long": "long long", "float": "double", "bool": "bool", "str": "std::string", "char": "char"}

SUPPORT = r'''
#include <cstdio>
#include <cstdlib>
#include <exception>
#include <fstream>
#include <map>
#include <set>
#include <stdexcept>
#include <string>
#include <type_traits>
#include <typeinfo>
#include <unordered_map>
#include <unordered_set>
#include <utility>
#include <vector>
#if defined(__GNUG__)
#include <cxxabi.h>
#endif

namespace antivibe {

inline std::string json(const std::string& s) {
    std::string out = "\"";
    for (unsigned char c : s) {
        switch (c) {
            case '"': out += "\\\""; break;
            case '\\': out += "\\\\"; break;
            case '\n': out += "\\n"; break;
            case '\r': out += "\\r"; break;
            case '\t': out += "\\t"; break;
            default:
                if (c < 0x20) { char buf[8]; std::snprintf(buf, sizeof buf, "\\u%04x", c); out += buf; }
                else out += static_cast<char>(c);
        }
    }
    return out + "\"";
}
inline std::string json(const char* s) { return json(std::string(s)); }
inline std::string json(char c) { return json(std::string(1, c)); }
inline std::string json(bool b) { return b ? "true" : "false"; }
inline std::string json(std::nullptr_t) { return "null"; }
inline std::string json(double d) {
    if (d != d || d == 1.0 / 0.0 || d == -1.0 / 0.0) return "null";
    char buf[40];
    std::snprintf(buf, sizeof buf, "%.17g", d);
    return buf;
}
inline std::string json(float f) { return json(static_cast<double>(f)); }
template <class T>
typename std::enable_if<std::is_integral<T>::value && !std::is_same<T, bool>::value && !std::is_same<T, char>::value, std::string>::type
json(T v) { return std::to_string(v); }

template <class T> std::string json(const std::vector<T>& v);
template <class T> std::string json(const std::set<T>& v);
template <class T> std::string json(const std::unordered_set<T>& v);
template <class K, class V> std::string json(const std::map<K, V>& m);
template <class K, class V> std::string json(const std::unordered_map<K, V>& m);
template <class A, class B> std::string json(const std::pair<A, B>& p);
inline std::string json(const std::vector<bool>& v) {
    std::string out = "[";
    for (std::size_t i = 0; i < v.size(); ++i) out += (i ? "," : "") + json(static_cast<bool>(v[i]));
    return out + "]";
}

template <class It> std::string json_items(It first, It last) {
    std::string out = "[";
    for (bool start = true; first != last; ++first, start = false) out += (start ? "" : ",") + json(*first);
    return out + "]";
}
template <class T> std::string json(const std::vector<T>& v) { return json_items(v.begin(), v.end()); }
template <class T> std::string json(const std::set<T>& v) { return json_items(v.begin(), v.end()); }
template <class T> std::string json(const std::unordered_set<T>& v) { return json_items(v.begin(), v.end()); }
template <class A, class B> std::string json(const std::pair<A, B>& p) { return "[" + json(p.first) + "," + json(p.second) + "]"; }

// JSON object keys are always strings
inline std::string key(const std::string& k) { return json(k); }
inline std::string key(char k) { return json(k); }
template <class K> std::string key(const K& k) { return "\"" + json(k) + "\""; }
template <class It> std::string json_object(It first, It last) {
    std::string out = "{";
    for (bool start = true; first != last; ++first, start = false)
        out += (start ? "" : ",") + key(first->first) + ":" + json(first->second);
    return out + "}";
}
template <class K, class V> std::string json(const std::map<K, V>& m) { return json_object(m.begin(), m.end()); }
template <class K, class V> std::string json(const std::unordered_map<K, V>& m) { return json_object(m.begin(), m.end()); }

static std::string result_path;
inline void write(const std::string& body) {
    std::ofstream out(result_path.c_str(), std::ios::binary);
    out << body;
}
inline std::string type_name(const std::exception& e) {
    const char* name = typeid(e).name();
#if defined(__GNUG__)
    int status = 0;
    char* readable = abi::__cxa_demangle(name, nullptr, nullptr, &status);
    if (status == 0 && readable) { std::string result(readable); std::free(readable); return result; }
#endif
    return name;
}

}  // namespace antivibe
'''


# ---------------------------------------------------------------------------
# Turning test data into C++
# ---------------------------------------------------------------------------

def cpp_type(t):
    name, args = t
    if name in SCALARS:
        return SCALARS[name]
    if name in ("array", "list"):
        return f"std::vector<{cpp_type(args[0])}>"
    if name == "set":
        return f"std::set<{cpp_type(args[0])}>"
    if name == "dict":
        return f"std::map<{cpp_type(args[0])}, {cpp_type(args[1])}>"
    raise ValueError(f"unknown type {name}")


def char_literal(ch):
    escapes = {"'": "\\'", "\\": "\\\\", "\n": "\\n", "\t": "\\t"}
    return "'" + escapes.get(ch, ch) + "'"


def literal(value, t):
    name, args = t
    if name == "int":
        return str(int(value))
    if name == "long":
        return f"{int(value)}LL"
    if name == "float":
        return repr(float(value))
    if name == "bool":
        return "true" if value else "false"
    if name == "str":
        return f"std::string({json.dumps(value)})"
    if name == "char":
        return char_literal(value)
    if name in ("array", "list", "set"):
        return cpp_type(t) + "{" + ", ".join(literal(item, args[0]) for item in value) + "}"
    if name == "dict":
        key_type, value_type = args
        items = []
        for k, v in value.items():
            k = int(k) if key_type[0] in ("int", "long") else k
            items.append("{" + literal(k, key_type) + ", " + literal(v, value_type) + "}")
        return cpp_type(t) + "{" + ", ".join(items) + "}"
    raise ValueError(f"unknown type {name}")


def display_arg(value, t):
    return f"'{value}'" if t[0] == "char" else display(value, "cpp")


def exception_name(raises):
    name = PYTHON_EXCEPTIONS.get(raises, raises)
    return name if "::" in name else f"std::{name}"


def case_code(index, test, signature):
    """The body of `case index:` in the driver."""
    write_got = 'antivibe::write(std::string("{\\"got\\":") + antivibe::json(antivibe_result) + "}");'
    if "args" in test:
        params = [(p[0], typespec.parse(p[1])) for p in signature["params"]]
        lines = [f"auto antivibe_arg{i} = {literal(value, params[i][1])};" for i, value in enumerate(test["args"])]
        call = f"{signature['name']}({', '.join(f'antivibe_arg{i}' for i in range(len(test['args'])))})"
    else:
        lines = [test["setup"]] if test.get("setup") else []
        call = f"({test['check']})"

    if test.get("raises"):
        exception = exception_name(test["raises"])
        short = exception.split("::")[-1]
        lines += [
            "try {",
            f"    (void){call};",
            f"}} catch (const {exception}&) {{",
            f'    antivibe::write("{{\\"raised\\":\\"{short}\\"}}");',
            "    break;",
            "}",
            'antivibe::write("{\\"returned\\":true}");',
        ]
    else:
        lines += [f"auto&& antivibe_result = {call};", write_got]
    body = "\n".join("            " + line for part in lines for line in part.split("\n"))
    return f"        case {index}: {{\n{body}\n            break;\n        }}"


def driver_source(spec):
    cases = "\n".join(case_code(i, test, spec.get("signature")) for i, test in enumerate(spec["tests"]))
    return f'''// Generated by Antivibe - runs one test per process
#define main antivibe_learner_main
#include "solution.cpp"
#undef main
{SUPPORT}
int main(int argc, char** argv) {{
    if (argc < 3) return 2;
    antivibe::result_path = argv[2];
    try {{
        switch (std::atoi(argv[1])) {{
{cases}
        }}
    }} catch (const std::exception& e) {{
        antivibe::write("{{\\"exception\\":" + antivibe::json(antivibe::type_name(e)) + ",\\"what\\":" + antivibe::json(std::string(e.what())) + "}}");
    }} catch (...) {{
        antivibe::write("{{\\"exception\\":\\"an unknown exception\\",\\"what\\":\\"\\"}}");
    }}
    return 0;
}}
'''


def display_call(test, signature):
    if "args" in test:
        params = [typespec.parse(p[1]) for p in signature["params"]]
        return f"{signature['name']}({', '.join(display_arg(v, params[i]) for i, v in enumerate(test['args']))})"
    return "\n".join(filter(None, [test.get("setup"), test["check"]]))


# ---------------------------------------------------------------------------
# Compiling and running
# ---------------------------------------------------------------------------

ERROR_LINE = re.compile(r"^(.*?):(\d+):(?:\d+:)? (?:fatal )?error: (.*)$")


def compile_error(output):
    """(message, line in the learner's file or None) for the first compiler error.

    An error in the learner's own file wins over one in the generated driver: a
    missing bracket in the solution often shows up as errors further on, too.
    """
    errors = []
    for raw in output.splitlines():
        match = ERROR_LINE.match(raw.strip())
        if match:
            path, line, message = match.groups()
            errors.append((os.path.basename(path) == "solution.cpp", int(line), message))
    for in_solution, line, message in errors:
        if in_solution:
            return f"Your code does not compile: {message}", line
    if errors:
        return (
            "The tests could not call your code - check that the names, parameter types and "
            f"return types match the starter code. The compiler said: {errors[0][2]}"
        ), None
    tail = output.strip().splitlines()[-5:]
    return "Your code does not compile:\n" + "\n".join(tail), None


CRASHES = {
    3221225477: "crashed: memory access violation - often an index out of range or a null pointer",
    3221225725: "crashed: stack overflow - is a recursion missing its base case?",
    3221225620: "crashed: integer division by zero",
    3221226505: "crashed: the program aborted (std::terminate or a failed check)",
    3: "crashed: the program aborted (std::terminate or a failed check)",
    -11: "crashed: segmentation fault - often an index out of range or a null pointer",
    -6: "crashed: the program aborted",
    -8: "crashed: arithmetic error (division by zero?)",
}


def crash_message(returncode):
    if returncode in CRASHES:
        return CRASHES[returncode]
    if returncode < 0 or returncode > 255:
        return f"crashed (exit code {returncode}) - often an index out of range or a null pointer"
    return f"stopped with exit code {returncode} before finishing the test"


def run_case(executable, index, workdir):
    """(outcome, printed) for one test."""
    result_file = os.path.join(workdir, f"result{index}.json")
    try:
        completed = subprocess.run(
            [executable, str(index), result_file], cwd=workdir, stdin=subprocess.DEVNULL,
            capture_output=True, timeout=CASE_TIMEOUT,
        )
    except subprocess.TimeoutExpired as timeout:
        printed = (timeout.stdout or b"").decode("utf-8", "replace")
        return {"timeout": True}, printed
    printed = completed.stdout.decode("utf-8", "replace")

    if not os.path.exists(result_file):
        return {"error": crash_message(completed.returncode)}, printed
    with open(result_file, encoding="utf-8") as f:
        data = json.load(f)
    if "got" in data:
        return {"got": data["got"]}, printed
    if "raised" in data:
        return {"raised": data["raised"]}, printed
    if "returned" in data:
        return {"got": None, "returned": True}, printed
    what = f": {data['what']}" if data.get("what") else ""
    return {"error": f"threw {data['exception']}{what}"}, printed


def run(spec, solution_path):
    started = time.monotonic()
    compiler = spec.get("compiler") or "g++"
    signature = spec.get("signature")
    compare = spec.get("compare", "exact")

    with tempfile.TemporaryDirectory(prefix="antivibe-cpp-") as workdir:
        with open(solution_path, encoding="utf-8") as source, \
                open(os.path.join(workdir, "solution.cpp"), "w", encoding="utf-8") as copy:
            copy.write(source.read())
        with open(os.path.join(workdir, "tests.cpp"), "w", encoding="utf-8") as driver:
            driver.write(driver_source(spec))

        executable = os.path.join(workdir, "tests.exe" if os.name == "nt" else "tests")
        try:
            completed = subprocess.run(
                [compiler, "-std=c++17", "-O0", "-fmax-errors=3", "-static-libstdc++", "-static-libgcc",
                 "-o", executable, "tests.cpp"],
                cwd=workdir, capture_output=True, timeout=COMPILE_TIMEOUT,
            )
        except FileNotFoundError:
            emit({"type": "load_error", "line": None, "message":
                  f'Could not start the C++ compiler "{compiler}". Install g++ (or set "antivibe.cppCompiler").'})
            return
        except subprocess.TimeoutExpired:
            emit({"type": "load_error", "line": None, "message": "Compiling took too long."})
            return
        if completed.returncode != 0:
            message, line = compile_error(completed.stderr.decode("utf-8", "replace"))
            emit({"type": "load_error", "message": message, "line": line})
            return

        for index, test in enumerate(spec["tests"]):
            if time.monotonic() - started > TOTAL_BUDGET:
                break  # the rest show as "not run"
            raises = test.get("raises")
            emit({
                "type": "start", "index": index,
                "call": display_call(test, signature),
                "expected": f"raises {exception_name(raises)}" if raises else display(test["expected"], "cpp"),
            })
            outcome, printed = run_case(executable, index, workdir)
            result = judge({**test, "raises": raises and exception_name(raises)}, outcome, compare, "cpp")
            if outcome.get("returned"):
                result["got"] = "returned normally"
            if result["status"] == "timeout":
                result["note"] = "This test did not finish within 3 seconds. Look for a loop that never ends."
            emit({"type": "case", "index": index, **result, "printed": printed[:MAX_PRINTED]})

    emit({"type": "review", "notes": []})
    emit({"type": "done"})
