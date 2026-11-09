"""Language-neutral types for exercise signatures.

A signature describes the function a learner writes in a compiled language:

    {"name": "two_sum", "params": [["nums", "array[int]"], ["target", "int"]],
     "returns": "array[int]"}

Types:  int  long  float  bool  str  char
        array[T]   a fixed-size sequence (C++ vector, Java T[])
        list[T]    a growable sequence   (C++ vector, Java List<T>)
        dict[K,V]  a map                 (C++ map, Java Map<K,V>)
        set[T]
"""


def parse(text):
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
    return (name, [parse(part) for part in parts])


def camel_case(name):
    """two_sum -> twoSum (Java naming)."""
    first, *rest = name.split("_")
    return first + "".join(word[:1].upper() + word[1:] for word in rest)
