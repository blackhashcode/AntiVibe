"""Code review for a learner's solution.

Passing the tests is not the same as writing good code. This looks for
habits that make code longer, more fragile or harder to read than it needs
to be, and explains each one in plain language. It never rewrites the code.

    review(source) -> [{"line": 12, "message": "..."}]
"""
import ast

# Built-in names a beginner is likely to reuse for a variable
BUILTINS = {
    "sum", "list", "str", "max", "min", "len", "dict", "set", "input", "print",
    "int", "float", "type", "id", "range", "sorted", "map", "filter", "tuple", "all", "any",
}
LIST_MUTATORS = {"append", "insert", "remove", "pop", "sort", "reverse", "extend", "clear"}
OPPOSITE = {ast.Lt: ast.GtE, ast.GtE: ast.Lt, ast.Gt: ast.LtE, ast.LtE: ast.Gt}


def review(source):
    if not hasattr(ast, "unparse"):  # Python 3.8 and older
        return []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []

    notes = []
    seen = set()
    shadowed = set()

    def note(node, message):
        key = (node.lineno, message)
        if key not in seen:
            seen.add(key)
            notes.append({"line": node.lineno, "message": message})

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            check_function(node, note)
            check_bool_return_after_if(node.body, note)
        elif isinstance(node, ast.If):
            check_bool_if_else(node, note)
            check_redundant_elif(node, note)
        elif isinstance(node, ast.For):
            check_range_len(node, note)
            check_counting_loop(node, note)
        elif isinstance(node, ast.BoolOp) and isinstance(node.op, ast.Or):
            check_or_chain(node, note)
        elif isinstance(node, ast.Call):
            check_int_division(node, note)
        if isinstance(node, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
            check_shadowed_builtin(node, note, shadowed)
        if isinstance(node, ast.Raise):
            check_bare_raise(node, note)

    notes.sort(key=lambda n: n["line"])
    return notes


# ---------------------------------------------------------------------------

def is_bool(node, value=None):
    return (
        isinstance(node, ast.Constant)
        and isinstance(node.value, bool)
        and (value is None or node.value is value)
    )


def returns_bool(statements):
    """The bool a block returns if it is exactly `return True` / `return False`."""
    if len(statements) == 1 and isinstance(statements[0], ast.Return) and is_bool(statements[0].value):
        return statements[0].value.value
    return None


RETURN_CONDITION = (
    "`if ...: return True` / `return False` can be shortened to `return <the condition>` - "
    "a comparison already is True or False."
)


def check_bool_if_else(node, note):
    """if cond: return True  else: return False"""
    body, orelse = returns_bool(node.body), returns_bool(node.orelse)
    if body is not None and orelse is not None and body != orelse:
        note(node, RETURN_CONDITION)


def check_bool_return_after_if(statements, note):
    """if cond: return True  (no else)  return False"""
    for current, following in zip(statements, statements[1:]):
        if not isinstance(current, ast.If) or current.orelse:
            continue
        body = returns_bool(current.body)
        after = returns_bool([following])
        if body is not None and after is not None and body != after:
            note(current, RETURN_CONDITION)


def check_redundant_elif(node, note):
    """if x >= 90: ...  elif x >= 80 and x < 90: ...   (x < 90 is already known)"""
    known = []
    current = node
    while True:
        test = current.test
        if isinstance(test, ast.Compare) and len(test.ops) == 1:
            known.append(test)
        elif isinstance(test, ast.BoolOp) and isinstance(test.op, ast.And):
            parts = [p for p in test.values if isinstance(p, ast.Compare) and len(p.ops) == 1]
            for part in parts:
                if any(is_opposite(part, earlier) for earlier in known):
                    note(part, (
                        f"`{ast.unparse(part)}` is always true here: an earlier branch already "
                        "handled the other case, and Python only reaches an elif when every "
                        "branch above it was False. You can leave that part out."
                    ))
            known.extend(parts)
        if len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
            current = current.orelse[0]
        else:
            break


def is_opposite(a, b):
    op_a, op_b = type(a.ops[0]), type(b.ops[0])
    return (
        OPPOSITE.get(op_b) is op_a
        and ast.dump(a.left) == ast.dump(b.left)
        and ast.dump(a.comparators[0]) == ast.dump(b.comparators[0])
    )


def range_len_target(node):
    """For `for i in range(len(x))` or `range(0, len(x))`, the dump of x."""
    call = node.iter
    if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == "range"):
        return None
    args = call.args
    if len(args) == 2 and isinstance(args[0], ast.Constant) and args[0].value == 0:
        args = args[1:]
    if len(args) != 1:
        return None
    inner = args[0]
    if (isinstance(inner, ast.Call) and isinstance(inner.func, ast.Name)
            and inner.func.id == "len" and len(inner.args) == 1):
        return inner.args[0]
    return None


def check_range_len(node, note):
    """for i in range(len(xs)): ... only ever xs[i] ..."""
    sequence = range_len_target(node)
    if sequence is None or not isinstance(node.target, ast.Name):
        return
    index = node.target.id
    uses = [n for stmt in node.body for n in ast.walk(stmt) if isinstance(n, ast.Name) and n.id == index]
    lookups = [
        n for stmt in node.body for n in ast.walk(stmt)
        if isinstance(n, ast.Subscript) and isinstance(n.ctx, ast.Load)
        and ast.dump(n.value) == ast.dump(sequence)
        and isinstance(n.slice, ast.Name) and n.slice.id == index
    ]
    if uses and len(uses) == len(lookups):
        name = ast.unparse(sequence)
        note(node, (
            f"You only use `{index}` to read `{name}[{index}]`. Loop over the items directly - "
            f"`for item in {name}:` - and the index disappears, along with any chance of "
            "an off-by-one mistake."
        ))


def increments_by_one(statement):
    """The name a statement adds 1 to (`c += 1` or `c = c + 1`), else None."""
    if (isinstance(statement, ast.AugAssign) and isinstance(statement.op, ast.Add)
            and isinstance(statement.target, ast.Name)
            and isinstance(statement.value, ast.Constant) and statement.value.value == 1):
        return statement.target.id
    if (isinstance(statement, ast.Assign) and len(statement.targets) == 1
            and isinstance(statement.targets[0], ast.Name)
            and isinstance(statement.value, ast.BinOp) and isinstance(statement.value.op, ast.Add)):
        name = statement.targets[0].id
        left, right = statement.value.left, statement.value.right
        if (isinstance(left, ast.Name) and left.id == name
                and isinstance(right, ast.Constant) and right.value == 1):
            return name
    return None


def check_counting_loop(node, note):
    """for _ in xs: count += 1   - that is len(xs)"""
    if len(node.body) != 1 or increments_by_one(node.body[0]) is None:
        return
    target_names = {n.id for n in ast.walk(node.target) if isinstance(n, ast.Name)}
    used = {n.id for n in ast.walk(node.body[0]) if isinstance(n, ast.Name)}
    if target_names & used:
        return
    sequence = range_len_target(node)
    counted = ast.unparse(sequence if sequence is not None else node.iter)
    note(node, (
        f"This loop only counts how many items there are. `len({counted})` gives you "
        "that number directly, without a loop."
    ))


def check_or_chain(node, note):
    """x == 'a' or x == 'e' or x == 'i' ..."""
    compares = node.values
    if len(compares) < 3:
        return
    if not all(isinstance(c, ast.Compare) and len(c.ops) == 1 and isinstance(c.ops[0], ast.Eq)
               for c in compares):
        return
    lefts = {ast.dump(c.left) for c in compares}
    if len(lefts) == 1:
        subject = ast.unparse(compares[0].left)
        note(node, (
            f"Comparing `{subject}` with {len(compares)} values one by one is long and easy to get "
            f"wrong. The `in` operator checks them all at once: `{subject} in (...)`, or for "
            "single characters, `ch in \"aeiou\"`."
        ))


def check_int_division(node, note):
    """int(a / b)  ->  a // b"""
    if (isinstance(node.func, ast.Name) and node.func.id == "int" and len(node.args) == 1
            and isinstance(node.args[0], ast.BinOp) and isinstance(node.args[0].op, ast.Div)):
        division = node.args[0]
        note(node, (
            f"`int({ast.unparse(division)})` divides and then chops off the decimals. "
            f"`{ast.unparse(division.left)} // {ast.unparse(division.right)}` does whole-number "
            "division in one step (and stays exact for very large numbers)."
        ))


def check_shadowed_builtin(node, note, shadowed):
    targets = node.targets if isinstance(node, ast.Assign) else [node.target]
    for target in targets:
        for name in ast.walk(target):
            if (isinstance(name, ast.Name) and isinstance(name.ctx, ast.Store)
                    and name.id in BUILTINS and name.id not in shadowed):
                shadowed.add(name.id)
                note(node, (
                    f"`{name.id}` is the name of one of Python's built-in functions. After "
                    f"`{name.id} = ...` you can no longer call `{name.id}()` in this function. "
                    "Pick a different name, such as `total` or `result`."
                ))


def check_bare_raise(node, note):
    if isinstance(node.exc, ast.Name) and node.exc.id.endswith("Error"):
        note(node, (
            f"`raise {node.exc.id}` works, but the person who sees the error gets no explanation. "
            f"Add a message: `raise {node.exc.id}(\"amount must be positive\")`."
        ))


def check_function(func, note):
    params = {arg.arg for arg in func.args.args + func.args.kwonlyargs} - {"self", "cls"}
    if not params:
        return

    for node in ast.walk(func):
        # a parameter reassigned inside a loop: `for i in range(n): n = n + i`
        if isinstance(node, (ast.For, ast.While)):
            for inner in ast.walk(node):
                if isinstance(inner, (ast.Assign, ast.AugAssign)):
                    targets = inner.targets if isinstance(inner, ast.Assign) else [inner.target]
                    for target in targets:
                        if isinstance(target, ast.Name) and target.id in params:
                            note(inner, (
                                f"You change the parameter `{target.id}` inside a loop. Even when "
                                "the answer comes out right, it is hard to follow, because "
                                f"`{target.id}` no longer means what the caller passed in. Keep "
                                "parameters unchanged and build the answer in a new variable."
                            ))

        # changing a list the caller passed in
        mutated = None
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr in LIST_MUTATORS
                and isinstance(node.func.value, ast.Name) and node.func.value.id in params):
            mutated = node.func.value.id
        elif isinstance(node, (ast.Assign, ast.AugAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                if (isinstance(target, ast.Subscript) and isinstance(target.value, ast.Name)
                        and target.value.id in params):
                    mutated = target.value.id
        if mutated:
            note(node, (
                f"This changes `{mutated}`, the list the caller passed in - their list changes "
                "too, because both names refer to the same list. Callers rarely expect that. "
                "Build a new list for your answer instead."
            ))
