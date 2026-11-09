"""C++ track 1: C++ Fundamentals. The format is described in problems.py and porting.py."""
from languages import CPP_HEADER
from porting import fn, port

TRACK = {
    "id": "cpp-fundamentals",
    "title": "C++ Fundamentals",
    "description": "The C++ language: types, decisions, loops, vectors, strings, maps, functions, exceptions and recursion.",
    "milestones": [
        # ------------------------------------------------------------------
        {
            "id": "cpp-basics",
            "title": "Programs, Types & Functions",
            "summary": "How a C++ file is built, why every value has a type, and functions that return a result.",
            "lesson": [
                {
                    "heading": "From Python to C++",
                    "text": "C++ asks you to say more up front. Every variable and every function has a declared type, statements end with `;`, and blocks are wrapped in `{ }` instead of being marked by indentation. In return, the compiler checks your whole program before it runs and catches many mistakes that Python only finds when that line executes.\n\nThe problem-solving method is exactly the same as before: understand, solve an example by hand, plan, code one step at a time, and trace when a test fails. A compile error is not a failure - it is the compiler doing the first round of checking for you. Read it: it names the line.",
                },
                {
                    "heading": "The parts of a file",
                    "text": "Each exercise file starts with `#include` lines, which bring in parts of the standard library (strings, vectors, maps...), and `using namespace std;`, which lets you write `string` instead of `std::string`. Below that come your functions. A stand-alone program would also need a `main` function where it starts, but in Antivibe the tests call your functions directly, so you never need one.",
                    "code": "#include <string>\nusing namespace std;\n\nint double_it(int n) {\n    return n * 2;\n}",
                },
                {
                    "heading": "Types",
                    "text": "`int` holds whole numbers (up to about 2.1 billion), `long long` bigger whole numbers, `double` decimals, `bool` is `true` or `false`, `char` is one character in single quotes, and `string` is text in double quotes. A variable is declared with its type, and it keeps that type forever. `auto` asks the compiler to work the type out from the value.",
                    "code": "int age = 21;\ndouble price = 2.5;\nbool done = false;\nchar initial = 'A';\nstring name = \"Ada\";\nauto total = age + 1;      // an int",
                },
                {
                    "heading": "Arithmetic - watch the division",
                    "text": "`+ - * %` work as in Python. Division is the big difference: if both sides of `/` are whole numbers, C++ does whole-number division and throws the remainder away, so `7 / 2` is `3`. Make one side a `double` to get `3.5`: write `7 / 2.0`, or convert a variable with `static_cast<double>(a)`. There is no `**`; `pow(2, 3)` from `<cmath>` returns a double.",
                    "code": "int a = 7 / 2;                   // 3\ndouble b = 7 / 2;                // 3.0 - the division already happened in ints\ndouble c = 7 / 2.0;              // 3.5\ndouble d = static_cast<double>(7) / 2;   // 3.5\nint r = 7 % 2;                   // 1",
                },
                {
                    "heading": "Functions",
                    "text": "A function names the type it returns, then each parameter with its type. `return` hands the result back. A function that returns nothing has the return type `void`.\n\nText and containers are usually passed as `const string& s`: the `&` avoids copying the text, and `const` promises the function will not change it. You will see this in the starter code.",
                    "code": "double average(int a, int b) {\n    return (a + b) / 2.0;\n}\n\nstring greet(const string& name) {\n    return \"Hello, \" + name + \"!\";\n}",
                },
                {
                    "heading": "Building strings",
                    "text": "Strings join with `+` and grow with `+=`. A number has to be turned into text first with `to_string`. You can add a `char` to a string, but `\"a\" + \"b\"` on its own does not work - at least one side must be a `string`, not just two literals.",
                    "code": "string first = \"Ada\";\nstring full = first + \" \" + \"Lovelace\";   // fine: first is a string\nstring label = \"Item \" + to_string(3);       // \"Item 3\"\nfull += '!';",
                },
                {
                    "heading": "Common mistakes",
                    "text": "A missing `;` - the compiler often reports it on the next line.\n\nWhole-number division when you wanted a decimal.\n\nForgetting `return` in a function that should return a value. It may still compile, but the result is undefined - it can be any value at all. Turn every path through your function into a `return`.\n\n`cout << x;` prints; it does not return anything to the caller.",
                },
            ],
            "quiz": [
                {
                    "question": "What are `a`, `b` and `c`?",
                    "code": "int a = 7 / 2;\ndouble b = 7 / 2;\ndouble c = 7 / 2.0;",
                    "answer": "`a` is `3`, `b` is `3.0` (the int division happened first, then 3 was turned into 3.0), and `c` is `3.5`.",
                },
                {
                    "question": "What is `x` at the end?",
                    "code": "int x = 5;\nx = x + 2;\nx *= 2;",
                    "answer": "`14`. `x *= 2` is short for `x = x * 2`.",
                },
                {
                    "question": "What is `s` at the end?",
                    "code": "string s = \"ab\";\ns += 'c';\ns = s + to_string(4);",
                    "answer": "`\"abc4\"`. A char can be added to a string, and to_string(4) turns the number into the text \"4\".",
                },
                {
                    "question": "What is `c`?",
                    "code": "char c = 'a' + 1;",
                    "answer": "`'b'`. A char is stored as a small number (its character code), so adding 1 gives the next character.",
                },
            ],
            "problems": [
                port(
                    "rectangle-area",
                    signature=fn("rectangle_area", "float", width="float", height="float"),
                    hints=[
                        "The area of a rectangle is a single arithmetic operation on its two sides.",
                        "Your function already receives both numbers as parameters. Combine them and send the result back.",
                        "`*` multiplies. The function's return type is double, so the result is returned as a decimal number.",
                        "Structure: one line - return width * height;",
                    ],
                ),
                port(
                    "full-name",
                    signature=fn("full_name", "str", first="str", last="str"),
                    hints=[
                        "You are building one string out of three pieces: the first name, a space, and the last name.",
                        "Strings join with + in C++ too.",
                        "first is a string, so first + \" \" works, and adding last to that works as well. A space is written \" \".",
                        "Structure: return first + \" \" + last;",
                    ],
                ),
                {
                    "id": "average-of-two",
                    "title": "Debug: Average of Two",
                    "difficulty": "warm-up",
                    "description": "This function should return the average of a and b as a decimal number, but most tests fail. Find the bug - it is the most common C++ arithmetic mistake - and fix it.",
                    "signature": fn("average_of_two", "float", a="int", b="int"),
                    "starter": CPP_HEADER + "\ndouble average_of_two(int a, int b) {\n    return (a + b) / 2;\n}\n",
                    "compare": "exact",
                    "tests": [
                        {"args": [1, 2], "expected": 1.5},
                        {"args": [3, 4], "expected": 3.5},
                        {"args": [2, 4], "expected": 3.0},
                        {"args": [0, 0], "expected": 0.0},
                        {"args": [-2, 2], "expected": 0.0},
                        {"args": [10, 5], "expected": 7.5},
                    ],
                    "hints": [
                        "Look at which tests pass and which fail. What do the passing ones have in common?",
                        "The answer is right whenever a + b is even. Something is throwing away the .5.",
                        "a + b is an int and 2 is an int, so / does whole-number division - before the result is turned into a double. One side of the division has to be a double already.",
                        "Structure: divide by 2.0 instead of 2 (or convert a + b with static_cast<double> first).",
                    ],
                    "questions": [
                        "Why does the return type double not fix the problem on its own?",
                        "Which tests passed even with the bug, and why?",
                    ],
                },
                port(
                    "hours-and-minutes",
                    signature=fn("hours_and_minutes", "array[int]", total_minutes="int"),
                    description="Convert a number of minutes into whole hours and leftover minutes. Return the two numbers as a vector: {hours, minutes}.",
                    hints=[
                        "How many full groups of 60 fit into the total? And what is left over once you take those groups out?",
                        "With two ints, / already does whole-number division in C++ - for once that is exactly what you want. % gives the remainder.",
                        "135 / 60 is 2 and 135 % 60 is 15. A vector can be returned straight from a list of values in braces.",
                        "Structure: return {total_minutes / 60, total_minutes % 60};",
                    ],
                    questions=[
                        "Why is whole-number division helpful here but a bug in Average of Two?",
                        "How would you also split out the days?",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-conditionals",
            "title": "Making Decisions",
            "summary": "Compare values and choose what to do with if, else if and else.",
            "lesson": [
                {
                    "heading": "Comparisons and bool",
                    "text": "Comparisons give a `bool`: `true` or `false` (lower case). The operators are the same as Python's: `== != < > <= >=`. Combine conditions with `&&` (and), `||` (or) and `!` (not).",
                    "code": "int age = 20;\nbool adult = age >= 18;              // true\nbool working_age = age >= 18 && age < 65;\nbool child_or_senior = age < 18 || age >= 65;",
                },
                {
                    "heading": "if, else if, else",
                    "text": "The condition goes in round brackets and the block in braces. Exactly like Python's elif chain, C++ checks from the top and runs only the first branch that matches.",
                    "code": "string describe(int temperature) {\n    if (temperature > 30) {\n        return \"hot\";\n    } else if (temperature > 15) {\n        return \"mild\";\n    } else {\n        return \"cold\";\n    }\n}",
                },
                {
                    "heading": "= is not ==",
                    "text": "`=` assigns and `==` compares. Python refuses `if x = 0:`, but C++ accepts `if (x = 0)`: it sets x to 0 and then treats 0 as false. The code compiles and quietly does the wrong thing. Whenever a condition misbehaves, check for a single `=`.",
                },
                {
                    "heading": "Remainders of negative numbers",
                    "text": "In C++, the result of `%` takes the sign of the left side: `-7 % 2` is `-1`, not `1` as in Python. So `n % 2 == 1` is false for odd negative numbers. `n % 2 == 0` and `n % 2 != 0` work for every sign.",
                },
                {
                    "heading": "Common mistakes",
                    "text": "Order matters: put the most specific condition first.\n\nA comparison is already a bool, so `return n % 2 == 0;` replaces an if that returns true and an else that returns false.\n\nA function returning a value must return on every path - an if without an else at the end can fall off the end of the function.",
                },
            ],
            "quiz": [
                {
                    "question": "What is `r` at the end?",
                    "code": "int n = 15;\nstring r = \"\";\nif (n % 3 == 0) r += \"A\";\nif (n % 5 == 0) r += \"B\";",
                    "answer": "`\"AB\"`. Two separate ifs are both checked. With `else if` for the second, r would be just \"A\".",
                },
                {
                    "question": "What are these two values?",
                    "code": "-7 % 2\n7 > 5 && 7 % 2 == 0",
                    "answer": "`-1` (the sign follows the left side in C++) and `false` (7 % 2 is 1).",
                },
                {
                    "question": "What does `check(5)` return?",
                    "code": "string check(int x) {\n    if (x = 0) {\n        return \"zero\";\n    }\n    return \"not zero\";\n}",
                    "answer": "`\"not zero\"` - and it would return that for every input, including 0. `x = 0` assigns 0 and the condition is 0, which counts as false. It should be `x == 0`.",
                },
            ],
            "problems": [
                port(
                    "is-even",
                    signature=fn("is_even", "bool", n="int"),
                    description="Return true if n is an even number and false if it is odd. n may be negative.",
                    hints=[
                        "What is special about an even number when you divide it by 2?",
                        "The remainder operator tells you what is left over. For an even number that leftover is always the same value.",
                        "Compare n % 2 with 0, not with 1: in C++, -3 % 2 is -1, so a 'remainder is 1' test gets negative odd numbers wrong.",
                        "Structure: return n % 2 == 0;",
                    ],
                    questions=[
                        "Why does `n % 2 == 1` fail for -3 in C++?",
                        "Why is no if statement needed?",
                    ],
                ),
                port(
                    "sign-of",
                    signature=fn("sign_of", "str", n="float"),
                    hints=[
                        "There are three possible situations, and exactly one of them is true for any number.",
                        "Three exclusive cases map onto if / else if / else.",
                        "Compare n with 0 using > and <. If neither is true, only one possibility is left, so the last branch needs no condition.",
                        "Structure: if (n > 0) return \"positive\"; else if (n < 0) return \"negative\"; else return \"zero\";",
                    ],
                ),
                {
                    "id": "classify-number",
                    "title": "Debug: Classify a Number",
                    "difficulty": "warm-up",
                    "description": "classify(n) should return \"zero\", \"positive\" or \"negative\". It compiles, but it gets most numbers wrong. Find the one-character bug.",
                    "signature": fn("classify", "str", n="int"),
                    "starter": CPP_HEADER + "\nstring classify(int n) {\n    if (n = 0) {\n        return \"zero\";\n    } else if (n > 0) {\n        return \"positive\";\n    } else {\n        return \"negative\";\n    }\n}\n",
                    "compare": "exact",
                    "tests": [
                        {"args": [0], "expected": "zero"},
                        {"args": [5], "expected": "positive"},
                        {"args": [-3], "expected": "negative"},
                        {"args": [100], "expected": "positive"},
                        {"args": [-1], "expected": "negative"},
                    ],
                    "hints": [
                        "Trace classify(5) by hand. What is n after the first condition has been evaluated?",
                        "Every input comes out as \"negative\". Something in the first condition changes n.",
                        "`n = 0` is an assignment: it sets n to 0, and the value of the whole expression is 0, which counts as false. Comparing needs two equals signs.",
                        "Structure: change the first condition to n == 0.",
                    ],
                    "questions": [
                        "Why did the -3 and -1 tests pass with the bug?",
                        "Why does Python refuse `if n = 0:` while C++ accepts it?",
                    ],
                },
                port(
                    "letter-grade",
                    signature=fn("letter_grade", "str", score="int"),
                    hints=[
                        "The score falls into exactly one of five bands. You need to find which one.",
                        "An if / else if chain checks conditions from top to bottom and stops at the first true one.",
                        "Test the highest band first, so each later branch already knows the score was too low for the bands above it - one comparison per condition is enough.",
                        "Structure: if (score >= 90) return \"A\"; else if (score >= 80) return \"B\"; ... down to 60; else return \"F\";",
                    ],
                ),
                port(
                    "leap-year",
                    signature=fn("is_leap_year", "bool", year="int"),
                    description="Return true if the year is a leap year, otherwise false. A year is a leap year if it is divisible by 4 - except years divisible by 100, which are not leap years unless they are also divisible by 400.",
                    hints=[
                        "The rule has three layers: a general rule, an exception, and an exception to the exception.",
                        "'Divisible by' is a remainder check. With exceptions, test the most specific case first.",
                        "year % 400 == 0 settles it at once; otherwise year % 100 == 0 settles it the other way; only then does divisible-by-4 decide.",
                        "Structure: if (year % 400 == 0) return true; if (year % 100 == 0) return false; return year % 4 == 0;",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-loops",
            "title": "Loops",
            "summary": "Counting loops, while loops, range-based for loops and the accumulator pattern.",
            "lesson": [
                {
                    "heading": "The counting for loop",
                    "text": "C++'s classic for loop has three parts in its brackets: where the counter starts, the condition to keep going, and how the counter changes after each pass. `i++` adds one. `for (int i = 1; i <= n; i++)` visits 1 to n inclusive - note the `<=`.",
                    "code": "for (int i = 0; i < 3; i++) {\n    // i is 0, 1, 2\n}\nfor (int i = 1; i <= 3; i++) {\n    // i is 1, 2, 3\n}\nfor (int i = 10; i > 0; i -= 3) {\n    // i is 10, 7, 4, 1\n}",
                },
                {
                    "heading": "Looping over the characters",
                    "text": "A range-based for loop visits every item directly - like Python's `for ch in s`. Use it whenever you do not need the position.",
                    "code": "string word = \"hey\";\nfor (char ch : word) {\n    // 'h', 'e', 'y'\n}",
                },
                {
                    "heading": "Character helpers",
                    "text": "`<cctype>` has tests and conversions for single characters: `isdigit`, `isalpha`, `isalnum`, `isspace`, `tolower`, `toupper`. The conversions return an int (the character's code), so convert back when you need a char: `char up = toupper(c);`. To check whether a character is one of several, search a string for it: `string(\"aeiou\").find(c) != string::npos`.",
                    "code": "char c = 'E';\nisalpha(c)          // true (non-zero)\nchar low = tolower(c);   // 'e'\nbool vowel = string(\"aeiou\").find(low) != string::npos;   // true",
                },
                {
                    "heading": "The accumulator pattern",
                    "text": "Exactly as in Python: create the variable before the loop, update it inside, return it after.",
                    "code": "int sum_to(int n) {\n    int total = 0;\n    for (int i = 1; i <= n; i++) {\n        total += i;\n    }\n    return total;\n}",
                },
                {
                    "heading": "while loops",
                    "text": "`while (condition) { ... }` repeats as long as the condition holds. Peeling digits off a number works the same as in Python: `n % 10` is the last digit and `n / 10` (whole-number division!) removes it.",
                    "code": "int n = 472;\nwhile (n > 0) {\n    int digit = n % 10;   // 2, then 7, then 4\n    n = n / 10;           // 47, then 4, then 0\n}",
                },
                {
                    "heading": "Return inside a loop",
                    "text": "Same rule as Python: a `return` inside the loop ends the function on the spot. That is right for a search that has found its answer, wrong for anything that needs every item. And a search that finds nothing must still return something after the loop - otherwise the function falls off its end and returns garbage.",
                },
                {
                    "heading": "Common mistakes",
                    "text": "`<` versus `<=` in the loop condition (off by one).\n\n`int` overflows silently above about 2.1 billion - the value wraps around to a negative number. Use `long long` for big totals.\n\n`cout << toupper('a');` prints 65, not A, because toupper returns an int.",
                },
            ],
            "quiz": [
                {
                    "question": "What is `total` at the end?",
                    "code": "int total = 0;\nfor (int i = 1; i < 4; i++) {\n    total += i * i;\n}",
                    "answer": "`14`: i is 1, 2 and 3 (the loop stops when i reaches 4), so 1 + 4 + 9.",
                },
                {
                    "question": "What are `n` and `s` at the end?",
                    "code": "int n = 305;\nint s = 0;\nwhile (n > 0) {\n    s += n % 10;\n    n = n / 10;\n}",
                    "answer": "`n` is `0` and `s` is `8`: 5, then 0, then 3 are added, while n goes 30, 3, 0.",
                },
                {
                    "question": "What does this print?",
                    "code": "cout << toupper('a');",
                    "answer": "`65`, the character code of 'A'. toupper returns an int; `char up = toupper('a');` gives the letter.",
                },
                {
                    "question": "What does `f(\"x7\")` return?",
                    "code": "bool f(const string& s) {\n    for (char c : s) {\n        if (isdigit(c)) {\n            return true;\n        }\n        return false;\n    }\n    return false;\n}",
                    "answer": "`false`. The second `return false` is inside the loop, so the function gives up after looking at the 'x'.",
                },
            ],
            "problems": [
                port(
                    "sum-to",
                    signature=fn("sum_to", "int", n="int"),
                    description="Return the sum of all whole numbers from 1 to n inclusive. For n = 0 the sum is 0. Use a loop.",
                    hints=[
                        "Visit each number from 1 to n once and keep a running total.",
                        "The accumulator pattern: a total that starts at 0 before the loop and grows inside it.",
                        "for (int i = 1; i <= n; i++) visits 1 to n inclusive. Keep the return after the closing brace of the loop.",
                        "Structure: int total = 0; loop i from 1 to n adding i to total; return total;",
                    ],
                ),
                port(
                    "sum-of-evens",
                    signature=fn("sum_of_evens", "int", n="int"),
                    hints=[
                        "This is Sum to N with one extra question for every number: should it be added?",
                        "Loop over 1..n and use an if inside the loop.",
                        "Even means i % 2 == 0. (Or start at 2 and step by 2 with i += 2, and you need no if at all.)",
                        "Structure: int total = 0; for (int i = 1; i <= n; i++) if (i % 2 == 0) total += i; return total;",
                    ],
                ),
                port(
                    "count-char",
                    signature=fn("count_char", "int", s="str", ch="char"),
                    hints=[
                        "Look at the characters of s one at a time and keep a tally.",
                        "Use a counter that starts at 0 and a range-based for loop over s.",
                        "Compare each character with ch using == (they are both chars).",
                        "Structure: int count = 0; for (char c : s) if (c == ch) count++; return count;",
                    ],
                    questions=[
                        "Why is a range-based for loop simpler here than a counting loop?",
                        "std::count from <algorithm> does this in one line. Why practise without it?",
                    ],
                ),
                port(
                    "count-vowels",
                    signature=fn("count_vowels", "int", s="str"),
                    hints=[
                        "For each character the question is: is this a vowel?",
                        "Loop over the string with a counter, and lower-case each character so one check covers both cases.",
                        "char low = tolower(c); then string(\"aeiou\").find(low) != string::npos is true for a vowel.",
                        "Structure: int count = 0; for (char c : s) { char low = tolower(c); if (\"aeiou\" contains low) count++; } return count;",
                    ],
                ),
                {
                    "id": "has-digit",
                    "title": "Debug: Has a Digit",
                    "difficulty": "easy",
                    "description": "has_digit should return true if s contains at least one digit (0-9) and false otherwise. Some tests pass, some fail. Trace a failing case by hand, find the bug and fix it.",
                    "signature": fn("has_digit", "bool", s="str"),
                    "starter": CPP_HEADER + "\nbool has_digit(const string& s) {\n    for (char ch : s) {\n        if (isdigit(ch)) {\n            return true;\n        } else {\n            return false;\n        }\n    }\n}\n",
                    "compare": "exact",
                    "tests": [
                        {"args": ["abc1"], "expected": True},
                        {"args": ["x7"], "expected": True},
                        {"args": ["7up"], "expected": True},
                        {"args": ["hello"], "expected": False},
                        {"args": [""], "expected": False},
                        {"args": ["a b 9"], "expected": True},
                    ],
                    "hints": [
                        "Trace has_digit(\"abc1\"). Which character is the loop looking at when the function returns?",
                        "The function decides 'no digit' after looking at one character. When can you actually conclude there is no digit?",
                        "Finding a digit settles it, so return true inside the loop is fine. 'No digit' is only known after the loop - and right now the function has no return after the loop at all, so an empty string returns garbage.",
                        "Structure: delete the else branch, and add return false; after the loop's closing brace.",
                    ],
                    "questions": [
                        "Why did \"7up\" pass with the bug?",
                        "The compiler can warn 'control reaches end of non-void function'. What does that mean here?",
                    ],
                },
                port(
                    "sum-of-digits",
                    signature=fn("sum_of_digits", "int", n="int"),
                    description="Return the sum of the digits of the whole number n (n is 0 or more). Use a while loop with % and / - do not convert n to a string.",
                    hints=[
                        "Peel digits off the right-hand end of the number one at a time until nothing is left.",
                        "One operator gives you the last digit, the other removes it. Keep going while the number is above 0.",
                        "n % 10 is the last digit; n / 10 (int division) removes it. Copy n into another variable first if you want to keep n unchanged.",
                        "Structure: int total = 0; int rest = n; while (rest > 0) { total += rest % 10; rest /= 10; } return total;",
                    ],
                ),
                port(
                    "reverse-string",
                    signature=fn("reverse_string", "str", s="str"),
                    description="Return the characters of s in reverse order. For practice, do it with a loop - not std::reverse or reverse iterators.",
                    hints=[
                        "The last character becomes the first. Where does each new character have to go as you build the answer?",
                        "Either walk s from the front and put each character in FRONT of what you have, or walk s from the back and add each character to the END.",
                        "Walking backwards: for (int i = (int)s.size() - 1; i >= 0; i--) result += s[i]; - the (int) matters, because s.size() is unsigned and size() - 1 on an empty string becomes a huge number.",
                        "Structure: string result = \"\"; loop i from the last index down to 0, adding s[i]; return result;",
                    ],
                    questions=[
                        "Why does `s.size() - 1` misbehave for an empty string?",
                        "Which is faster in C++: adding to the end, or putting characters in front?",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-vectors",
            "title": "Vectors",
            "summary": "Store many values in order with vector, and learn when C++ copies and when it shares.",
            "lesson": [
                {
                    "heading": "vector",
                    "text": "`vector<int>` is C++'s growable list of ints (any type goes in the angle brackets). Read and write with `v[i]`, add to the end with `push_back`, remove the last item with `pop_back`, and get the count with `size()`.",
                    "code": "vector<int> scores = {70, 85};\nscores.push_back(90);       // {70, 85, 90}\nscores[0] = 75;             // {75, 85, 90}\nint last = scores.back();   // 90\nscores.pop_back();          // {75, 85}\nint n = scores.size();      // 2",
                },
                {
                    "heading": "Looping",
                    "text": "A range-based for loop reads every item. When you need positions, use a counting loop over the indexes. `size()` is unsigned (it can never be negative), which is why the starter code and many examples compare with `(int)v.size()` or use `size_t i`.",
                    "code": "int total = 0;\nfor (int x : scores) {\n    total += x;\n}\nfor (int i = 0; i < (int)scores.size(); i++) {\n    // scores[i] and its position i\n}",
                },
                {
                    "heading": "Copies versus references - the big difference from Python",
                    "text": "In Python, `b = a` makes a second name for the same list. In C++, `vector<int> b = a;` makes a full, separate copy. The same goes for parameters: a parameter declared `vector<int> v` receives a copy, so changes inside the function never reach the caller. Declare it `vector<int>& v` (a reference) to work on the caller's vector itself, or `const vector<int>& v` to read it without copying and without being allowed to change it.\n\nThe same applies inside range-based for loops: `for (int x : v)` gives you a copy of each item; `for (int& x : v)` lets you change the items.",
                    "code": "vector<int> a = {1, 2};\nvector<int> b = a;        // a copy\nb.push_back(3);           // a is still {1, 2}\n\nfor (int& x : a) {\n    x *= 10;              // a is now {10, 20}\n}",
                },
                {
                    "heading": "Building and returning a new vector",
                    "text": "Start with an empty vector, `push_back` what you want to keep, and return it - the accumulator pattern. Returning a vector does not copy it in modern C++, so it is cheap.",
                    "code": "vector<int> doubled(const vector<int>& nums) {\n    vector<int> result;\n    for (int n : nums) {\n        result.push_back(n * 2);\n    }\n    return result;\n}",
                },
                {
                    "heading": "Common mistakes",
                    "text": "`v[i]` with an index that does not exist is not an error you get told about - it reads or writes some other memory, and the program may crash or carry on with garbage. `v.at(i)` checks the index and throws `out_of_range` instead.\n\nAn empty vector has no `v[0]` and no `v.back()`, and `v.size() - 1` is a huge number when the size is 0.\n\nErasing items while walking forwards through the same vector skips the item after each one you erase.",
                },
            ],
            "quiz": [
                {
                    "question": "What is `a.size()` at the end?",
                    "code": "vector<int> a = {1, 2};\nvector<int> b = a;\nb.push_back(3);",
                    "answer": "`2`. b is a copy, so a is unchanged. (In Python the answer would be 3.)",
                },
                {
                    "question": "What is `v` after calling `add_nine(v)`?",
                    "code": "void add_nine(vector<int> nums) {\n    nums.push_back(9);\n}\n\nvector<int> v = {1};\nadd_nine(v);",
                    "answer": "Still `{1}`. The parameter is a copy. With `vector<int>& nums` the caller's v would become {1, 9}.",
                },
                {
                    "question": "What is `v` at the end?",
                    "code": "vector<int> v = {1, 2, 3};\nfor (int x : v) {\n    x *= 2;\n}",
                    "answer": "Still `{1, 2, 3}`. Each x is a copy of an item. `for (int& x : v)` would double the items.",
                },
                {
                    "question": "What is `big`?",
                    "code": "vector<int> v;\nsize_t big = v.size() - 1;",
                    "answer": "A huge number (18446744073709551615 on a 64-bit machine). size() is unsigned, so 0 - 1 wraps around instead of becoming -1.",
                },
            ],
            "problems": [
                port(
                    "largest-number",
                    signature=fn("largest", "int", nums="array[int]"),
                    description="Return the largest number in the non-empty vector nums. Do not use std::max_element - write the loop yourself.",
                    hints=[
                        "Read the numbers one by one while remembering only the biggest so far.",
                        "Keep a 'best so far' variable. Each new number either beats it and replaces it, or does not.",
                        "Start best at nums[0], not 0 - a list of negative numbers would break a start at 0.",
                        "Structure: int best = nums[0]; for (int x : nums) if (x > best) best = x; return best;",
                    ],
                ),
                port(
                    "index-of",
                    signature=fn("index_of", "int", nums="array[int]", target="int"),
                    description="Return the index of the first occurrence of target in nums, or -1 if it is not there. Do not use std::find.",
                    hints=[
                        "The answer is a position, so you need to know where you are as you loop.",
                        "Use a counting loop over the indexes and look at nums[i]. The first match settles the answer.",
                        "Return i as soon as nums[i] == target. If the loop finishes, the target is not there.",
                        "Structure: for (int i = 0; i < (int)nums.size(); i++) if (nums[i] == target) return i; return -1;",
                    ],
                ),
                port(
                    "only-evens",
                    signature=fn("only_evens", "list[int]", nums="array[int]"),
                    description="Return a new vector containing only the even numbers from nums, in their original order.",
                    hints=[
                        "You are filtering: every number is either kept or skipped.",
                        "Build a new vector and push_back only the numbers that pass the test.",
                        "Even means n % 2 == 0 - which also works for negative numbers in C++.",
                        "Structure: vector<int> result; for (int n : nums) if (n % 2 == 0) result.push_back(n); return result;",
                    ],
                ),
                port(
                    "average",
                    signature=fn("average", "float", nums="array[int]"),
                    description="Return the average (mean) of the numbers in nums as a double. If the vector is empty, return 0.",
                    hints=[
                        "An average is the total divided by how many values there are.",
                        "Add everything up, then divide by the size. Deal with the empty vector before dividing.",
                        "The total and the size are both whole numbers, so dividing them directly is whole-number division. Convert one of them to double first.",
                        "Structure: if (nums.empty()) return 0; int total = 0; add each number; return static_cast<double>(total) / nums.size();",
                    ],
                    questions=[
                        "Which test fails if you forget the static_cast, and why?",
                        "Why check nums.empty() rather than whether the total is 0?",
                    ],
                ),
                port(
                    "fizz-buzz",
                    signature=fn("fizz_buzz", "list[str]", n="int"),
                    description="Return a vector of strings for the numbers 1 to n inclusive: \"Fizz\" for multiples of 3, \"Buzz\" for multiples of 5, \"FizzBuzz\" for multiples of both, and otherwise the number itself as a string. If n is 0, return an empty vector.",
                    hints=[
                        "Look at every number from 1 to n once and decide which of four strings to add.",
                        "% tells you whether one number divides another. Build the result vector as you loop.",
                        "Test 'multiple of both' first, or 15 is caught by the 'multiple of 3' branch. to_string(i) turns a number into text.",
                        "Structure: vector<string> result; for i from 1 to n: if both push \"FizzBuzz\", else if 3 push \"Fizz\", else if 5 push \"Buzz\", else push to_string(i); return result;",
                    ],
                ),
                port(
                    "running-total",
                    signature=fn("running_total", "list[int]", nums="array[int]"),
                    description="Return a new vector in which each position holds the sum of all the numbers up to and including that position in nums.",
                    hints=[
                        "Each output value is the previous output value plus one new number.",
                        "Keep two accumulators: a running sum and the result vector.",
                        "Update the sum first, then push_back its current value. nums is const, so the compiler will stop you from writing into it.",
                        "Structure: int total = 0; vector<int> result; for (int n : nums) { total += n; result.push_back(total); } return result;",
                    ],
                ),
                {
                    "id": "without-negatives",
                    "title": "Debug: Remove the Negatives",
                    "difficulty": "easy",
                    "description": "This function should return the numbers of nums without the negative ones, in the original order. It looks reasonable but gets several tests wrong. Trace without_negatives({-1, -2, 3}) by hand to see why, then fix it.",
                    "signature": fn("without_negatives", "list[int]", nums="list[int]"),
                    "starter": CPP_HEADER + "\nvector<int> without_negatives(vector<int> nums) {\n    for (int i = 0; i < (int)nums.size(); i++) {\n        if (nums[i] < 0) {\n            nums.erase(nums.begin() + i);\n        }\n    }\n    return nums;\n}\n",
                    "compare": "exact",
                    "tests": [
                        {"args": [[-1, -2, 3]], "expected": [3]},
                        {"args": [[1, -5, -6, 2]], "expected": [1, 2]},
                        {"args": [[]], "expected": []},
                        {"args": [[4, 5]], "expected": [4, 5]},
                        {"args": [[-1]], "expected": []},
                    ],
                    "hints": [
                        "Trace it: at i = 0 the loop erases -1, and everything shifts left one place. Then i becomes 1. Which number is at index 1 now - and which number was never looked at?",
                        "Erasing while walking forward through the same vector skips the item right after each erased one.",
                        "The simplest fix avoids erasing altogether: build a separate result vector and push_back only the numbers you want to keep.",
                        "Structure: vector<int> result; for (int n : nums) if (n >= 0) result.push_back(n); return result;",
                    ],
                    "questions": [
                        "Why did {-1} and {4, 5} pass with the bug?",
                        "How could you fix it while still erasing (hint: when should i not move forward)?",
                    ],
                },
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-strings",
            "title": "Strings",
            "summary": "Index, slice, search, split and rebuild std::string.",
            "lesson": [
                {
                    "heading": "string basics",
                    "text": "`s[i]` is the character at position i (a `char`), `s.size()` the length, `s.empty()` checks for the empty string. Unlike Python strings, a C++ string can be changed in place: `s[0] = 'J';` works.",
                    "code": "string word = \"python\";\nchar first = word[0];      // 'p'\nchar last = word.back();   // 'n'\nword[0] = 'P';             // \"Python\"",
                },
                {
                    "heading": "substr and find",
                    "text": "`s.substr(start, length)` copies part of a string - careful, the second number is a length, not an end position. `s.substr(start)` takes everything from start. `s.find(text)` returns the position of the first match, or the special value `string::npos` if there is none.",
                    "code": "string s = \"python\";\ns.substr(1, 3)       // \"yth\"\ns.substr(2)          // \"thon\"\ns.find(\"th\")         // 2\ns.find(\"z\") == string::npos   // true",
                },
                {
                    "heading": "Changing characters - use a reference",
                    "text": "To change every character of a string with a range-based for loop, the loop variable must be a reference, `char&`. With plain `char`, each c is a copy and the string itself never changes.",
                    "code": "string s = \"hey\";\nfor (char& c : s) {\n    c = toupper(c);\n}\n// s is \"HEY\"",
                },
                {
                    "heading": "Splitting into words",
                    "text": "C++ strings have no split method. The usual way is an `istringstream` (from `<sstream>`): reading from it with `>>` gives one word at a time and skips any amount of spaces. To split at a different character, use `getline(stream, piece, ',')`.",
                    "code": "istringstream in(\"  lots   of space \");\nstring word;\nwhile (in >> word) {\n    // \"lots\", then \"of\", then \"space\"\n}\n\nistringstream csv(\"1,2,3\");\nstring piece;\nwhile (getline(csv, piece, ',')) {\n    // \"1\", then \"2\", then \"3\"\n}",
                },
                {
                    "heading": "Comparing and building",
                    "text": "`==` compares string contents (unlike Java). Build strings with `+=` - adding a char or another string to the end is fast. Reversing is a loop from the back, or `string(s.rbegin(), s.rend())`.",
                },
                {
                    "heading": "Common mistakes",
                    "text": "Reading `s[0]` of an empty string, or any index past the end.\n\n`substr(start, end)` - the second argument is a length.\n\n`for (char c : s) c = toupper(c);` changes copies; the string is untouched.",
                },
            ],
            "quiz": [
                {
                    "question": "What are these three values?",
                    "code": "string s = \"python\";\ns.substr(1, 3)\ns.find(\"th\")\ns.substr(4)",
                    "answer": "`\"yth\"` (3 characters starting at index 1), `2`, and `\"on\"`.",
                },
                {
                    "question": "What is `s` at the end?",
                    "code": "string s = \"ab\";\nfor (char c : s) {\n    c = toupper(c);\n}",
                    "answer": "Still `\"ab\"`. c is a copy of each character. `for (char& c : s)` would change the string.",
                },
                {
                    "question": "How many times does the loop body run?",
                    "code": "istringstream in(\"  a   b  \");\nstring w;\nwhile (in >> w) {\n    // body\n}",
                    "answer": "`2` times: once for \"a\" and once for \"b\". Reading with >> skips any amount of whitespace.",
                },
            ],
            "problems": [
                port(
                    "count-words",
                    signature=fn("count_words", "int", s="str"),
                    hints=[
                        "If you could take the words out one at a time, you would just count them.",
                        "An istringstream hands you one word at a time and ignores extra spaces.",
                        "istringstream in(s); string word; while (in >> word) - the loop runs once per word.",
                        "Structure: int count = 0; istringstream in(s); string word; while (in >> word) count++; return count;",
                    ],
                    questions=[
                        "Why does reading with >> handle the extra spaces for you?",
                        "How would you count words with a loop over the characters and no stream?",
                    ],
                ),
                port(
                    "capitalize-words",
                    signature=fn("capitalize_words", "str", s="str"),
                    description="Return s with the first letter of every word in upper case and the rest of each word unchanged. Words are separated by single spaces.",
                    hints=[
                        "A word starts at position 0 and right after every space.",
                        "C++ strings can be changed in place, so you can make a copy of s and capitalise the right characters in it.",
                        "Character i starts a word when i == 0 or s[i - 1] == ' '. Use toupper on just those characters.",
                        "Structure: string result = s; for each index i: if (i == 0 || result[i - 1] == ' ') result[i] = toupper(result[i]); return result;",
                    ],
                    questions=[
                        "Why must you check i == 0 before looking at result[i - 1]?",
                        "How would the solution change if words could be separated by several spaces?",
                    ],
                ),
                port(
                    "initials",
                    signature=fn("initials", "str", name="str"),
                    hints=[
                        "Two smaller jobs: get the words, then take one letter from each.",
                        "An istringstream gives you the words one at a time, skipping extra spaces.",
                        "word[0] is the first character and toupper capitalises it. Add each one to a result string.",
                        "Structure: string result; istringstream in(name); string word; while (in >> word) result += (char)toupper(word[0]); return result;",
                    ],
                ),
                port(
                    "is-palindrome-word",
                    signature=fn("is_palindrome_word", "bool", word="str"),
                    description="Return true if word reads the same forwards and backwards, treating upper and lower case as the same, and false otherwise. An empty string counts as a palindrome.",
                    hints=[
                        "A palindrome matches itself when reversed - or, equivalently, its first and last characters match, then the second and second-to-last, and so on.",
                        "Compare characters from both ends, moving inwards, after making the case the same.",
                        "Use two indexes, left = 0 and right = size - 1, and compare tolower(word[left]) with tolower(word[right]). Stop when they meet. Careful with an empty word: use int for right.",
                        "Structure: int left = 0, right = (int)word.size() - 1; while (left < right) { if (tolower(word[left]) != tolower(word[right])) return false; left++; right--; } return true;",
                    ],
                ),
                port(
                    "longest-word",
                    signature=fn("longest_word", "str", s="str"),
                    hints=[
                        "Largest Number again, but comparing the lengths of words.",
                        "Read the words one at a time and keep a 'best so far' word that is replaced only by a strictly longer one.",
                        "Start best as \"\": every real word is longer, and with no words \"\" is already the answer. Use > so the first of equally long words wins.",
                        "Structure: string best; istringstream in(s); string word; while (in >> word) if (word.size() > best.size()) best = word; return best;",
                    ],
                ),
                {
                    "id": "shout",
                    "title": "Debug: Shout",
                    "difficulty": "easy",
                    "description": "shout(s) should return s with every letter in upper case. It compiles and runs, but returns the text unchanged. Find out why and fix it.",
                    "signature": fn("shout", "str", s="str"),
                    "starter": CPP_HEADER + "\nstring shout(string s) {\n    for (char c : s) {\n        c = toupper(c);\n    }\n    return s;\n}\n",
                    "compare": "exact",
                    "tests": [
                        {"args": ["hello"], "expected": "HELLO"},
                        {"args": ["Hi there"], "expected": "HI THERE"},
                        {"args": [""], "expected": ""},
                        {"args": ["ABC"], "expected": "ABC"},
                        {"args": ["a1!"], "expected": "A1!"},
                    ],
                    "hints": [
                        "toupper is called on every character - so where do the upper-case letters go?",
                        "Re-read 'Changing characters - use a reference' in the lesson.",
                        "`for (char c : s)` makes c a copy of each character, so changing c changes nothing in s.",
                        "Structure: make the loop variable a reference - for (char& c : s).",
                    ],
                    "questions": [
                        "Why did \"\" and \"ABC\" pass with the bug?",
                        "s is a parameter passed by value. Why is it fine to change it here?",
                    ],
                },
                port(
                    "valid-palindrome",
                    signature=fn("is_palindrome", "bool", s="str"),
                    description="Return true if s reads the same forwards and backwards once you ignore upper/lower case and skip every character that is not a letter or a digit. Otherwise return false. An empty string counts as a palindrome.",
                    hints=[
                        "Two jobs: throw away what does not count, then check what is left reads the same both ways.",
                        "Build a cleaned string with only letters and digits, lower-cased, then compare it from both ends.",
                        "isalnum(c) is true for letters and digits; tolower lower-cases. Then use the two-index comparison from Palindrome Word on the cleaned string.",
                        "Structure: string cleaned; for (char c : s) if (isalnum(c)) cleaned += (char)tolower(c); then compare cleaned[left] and cleaned[right] moving inwards; return true if no mismatch.",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-maps",
            "title": "Maps & Sets",
            "summary": "Count, group and look things up with map, unordered_map, set and unordered_set.",
            "lesson": [
                {
                    "heading": "map and unordered_map",
                    "text": "`map<string, int>` maps keys to values like a Python dictionary, keeping the keys sorted. `unordered_map` does the same without sorting and is usually faster. Both are used with square brackets.",
                    "code": "map<string, int> ages;\nages[\"Ada\"] = 36;\nages[\"Alan\"] = 41;\nint a = ages[\"Ada\"];          // 36\nbool known = ages.count(\"Grace\") > 0;   // false",
                },
                {
                    "heading": "[] creates missing keys",
                    "text": "Here C++ differs from Python: reading `m[key]` for a key that is not there does not raise an error - it quietly inserts the key with a default value (0 for numbers, \"\" for strings, an empty vector for vectors). That makes counting very short, but it also means a lookup can add keys by accident. To check without inserting, use `m.count(key)` or `m.find(key)`; `m.at(key)` throws `out_of_range` for a missing key.",
                    "code": "map<char, int> counts;\nfor (char c : string(\"hello\")) {\n    counts[c]++;            // a missing key starts at 0\n}\n// {'e': 1, 'h': 1, 'l': 2, 'o': 1}",
                },
                {
                    "heading": "Looping over a map",
                    "text": "Each item of a map is a key and a value. A structured binding names both parts. A `map` gives the keys in sorted order; an `unordered_map` in no particular order.",
                    "code": "for (const auto& [name, age] : ages) {\n    // name and age\n}",
                },
                {
                    "heading": "Grouping",
                    "text": "Because `[]` creates a missing entry, a map of vectors needs no 'create the list first' step: `groups[key].push_back(item)` works for new keys too.",
                    "code": "map<char, vector<string>> by_initial;\nfor (const string& name : vector<string>{\"Ann\", \"Bob\", \"Amy\"}) {\n    by_initial[name[0]].push_back(name);\n}\n// {'A': {\"Ann\", \"Amy\"}, 'B': {\"Bob\"}}",
                },
                {
                    "heading": "Sets",
                    "text": "`set` and `unordered_set` hold each value at most once. `insert` adds, `count(x)` is 1 if x is there and 0 if not. A set can be built straight from a vector: `set<int> s(v.begin(), v.end());`.",
                    "code": "unordered_set<int> seen;\nseen.insert(3);\nseen.insert(3);            // no effect\nbool has = seen.count(3) > 0;   // true\nint n = seen.size();       // 1",
                },
                {
                    "heading": "Common mistakes",
                    "text": "Checking `if (m[key] > 0)` to see whether a key exists - it inserts the key. Use `count`.\n\nExpecting an `unordered_map` to come out in any particular order.",
                },
            ],
            "quiz": [
                {
                    "question": "What is `m.size()` at the end?",
                    "code": "map<string, int> m;\nm[\"a\"]++;\nint x = m[\"b\"];",
                    "answer": "`2`. Just reading m[\"b\"] inserted the key \"b\" with value 0.",
                },
                {
                    "question": "What is `s.size()`, and in what order does a loop visit s?",
                    "code": "set<int> s = {3, 1, 3, 2};",
                    "answer": "`3` - duplicates are dropped - and a set visits its values in sorted order: 1, 2, 3.",
                },
                {
                    "question": "What does the last line do?",
                    "code": "map<string, int> m = {{\"x\", 1}};\nint v = m.at(\"y\");",
                    "answer": "It throws `out_of_range`. at() never inserts; only [] does.",
                },
            ],
            "problems": [
                port(
                    "char-count",
                    signature=fn("char_count", "dict[char,int]", s="str"),
                    description="Return a map from each character in s to the number of times it appears. Upper and lower case are different characters, and spaces count too.",
                    hints=[
                        "For every character you need to remember one number: how many times you have seen it.",
                        "A map<char, int> holds exactly that.",
                        "counts[c]++ works even the first time you meet c, because [] creates the entry with 0.",
                        "Structure: map<char, int> counts; for (char c : s) counts[c]++; return counts;",
                    ],
                    questions=[
                        "How is counting in C++ different from Python's counts.get(c, 0) + 1?",
                        "Why does the result come out sorted by character?",
                    ],
                ),
                port(
                    "unique-count",
                    signature=fn("unique_count", "int", nums="array[int]"),
                    hints=[
                        "Duplicates should only be counted once. Which container ignores duplicates?",
                        "Put every value into a set and look at its size.",
                        "set<int> s(nums.begin(), nums.end()); builds the set in one step.",
                        "Structure: build a set from nums and return its size().",
                    ],
                ),
                port(
                    "contains-duplicate",
                    signature=fn("contains_duplicate", "bool", nums="array[int]"),
                    description="Return true if any value appears at least twice in nums, and false if every element is distinct.",
                    hints=[
                        "As you walk through the vector, the question for each number is: have I seen it before?",
                        "Comparing every pair is O(n^2). A container with fast membership checks makes it O(n).",
                        "unordered_set<int> seen: seen.count(x) tells you whether x is there; insert adds it.",
                        "Structure: unordered_set<int> seen; for (int x : nums) { if (seen.count(x)) return true; seen.insert(x); } return false;",
                    ],
                ),
                port(
                    "first-unique-char",
                    signature=fn("first_unique_char", "str", s="str"),
                    description="Return the first character in s that appears exactly once, as a one-character string. If every character repeats (or s is empty), return an empty string.",
                    hints=[
                        "You cannot know whether a character is unique until you have seen the whole string.",
                        "Go through the string twice: once to count, once to find.",
                        "First pass: counts[c]++ into a map. Second pass: walk s in order and look each count up. string(1, c) makes a one-character string.",
                        "Structure: count every character; for (char c : s) if (counts[c] == 1) return string(1, c); return \"\";",
                    ],
                ),
                port(
                    "most-common-char",
                    signature=fn("most_common_char", "str", s="str"),
                    description="Return the character that appears most often in s, as a one-character string. If several share the highest count, return the one that appears first in s. Return an empty string for an empty s.",
                    hints=[
                        "Two things you have done before, glued together: count, then find the largest.",
                        "First pass: count into a map. Second pass: a 'best so far' search over s, comparing counts.",
                        "To get the earliest on a tie, walk s itself in order and replace the best only on a strictly greater count.",
                        "Structure: count; string best; for (char c : s) if (best.empty() || counts[c] > counts[best[0]]) best = string(1, c); return best;",
                    ],
                ),
                port(
                    "valid-anagram",
                    signature=fn("is_anagram", "bool", s="str", t="str"),
                    description="Return true if t is an anagram of s - the same characters, the same number of times each, in any order. Otherwise return false.",
                    hints=[
                        "Anagrams contain the same letters the same number of times; only the order differs.",
                        "Count the characters of both strings.",
                        "Two maps are == when they hold exactly the same keys and values.",
                        "Structure: build map<char, int> counts for s and for t; return whether they are equal.",
                    ],
                ),
                port(
                    "group-by-first-letter",
                    signature=fn("group_by_first_letter", "dict[char,list[str]]", words="array[str]"),
                    description="words is a vector of non-empty lower-case words. Return a map from each first letter to the vector of words starting with it, keeping the words in their original order.",
                    hints=[
                        "Each first letter needs its own vector. A map from char to vector<string> holds that.",
                        "For each word, find its group and add the word to it.",
                        "groups[word[0]].push_back(word) - [] creates an empty vector the first time a letter appears.",
                        "Structure: map<char, vector<string>> groups; for (const string& w : words) groups[w[0]].push_back(w); return groups;",
                    ],
                    questions=[
                        "Why does C++ need no 'create the list first' step here, when Python did?",
                        "How would you group by word length instead?",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-functions",
            "title": "Functions & Exceptions",
            "summary": "Split problems into small functions, use default arguments, and throw and catch exceptions.",
            "lesson": [
                {
                    "heading": "Small functions that call each other",
                    "text": "Decomposition works the same in every language: name a piece of the problem, solve it in its own function, then use it. In C++ a function has to be declared before the code that calls it, so helpers go above the functions that use them.",
                    "code": "bool is_vowel(char c) {\n    return string(\"aeiou\").find(tolower(c)) != string::npos;\n}\n\nint count_vowels(const string& s) {\n    int count = 0;\n    for (char c : s) {\n        if (is_vowel(c)) count++;\n    }\n    return count;\n}",
                },
                {
                    "heading": "Default arguments",
                    "text": "A parameter can have a default value used when the caller leaves it out.",
                    "code": "string greet(const string& name, const string& greeting = \"Hello\") {\n    return greeting + \", \" + name + \"!\";\n}\n\ngreet(\"Ada\");               // \"Hello, Ada!\"\ngreet(\"Ada\", \"Welcome\");    // \"Welcome, Ada!\"",
                },
                {
                    "heading": "Throwing exceptions",
                    "text": "`throw` stops the function and reports an error. The standard library has ready-made exception types in `<stdexcept>`: `invalid_argument` for a bad value (Python's ValueError), `out_of_range` for an index or key that does not exist. Give it a message.",
                    "code": "double square_root(double n) {\n    if (n < 0) {\n        throw invalid_argument(\"n must not be negative\");\n    }\n    return sqrt(n);\n}",
                },
                {
                    "heading": "Catching exceptions",
                    "text": "`try { ... } catch (const invalid_argument& e) { ... }` runs the try block and jumps to the catch block if that exception is thrown. `stoi(text)` converts text to an int and throws `invalid_argument` if the text does not start with a number.\n\nCareful: stoi reads as much of a number as it can and ignores the rest, so `stoi(\"12abc\")` is 12. Its optional second argument tells you how many characters it used, which lets you check that the whole text was a number.",
                    "code": "int number;\ntry {\n    number = stoi(\"abc\");\n} catch (const invalid_argument& e) {\n    number = 0;\n}\n\nsize_t used = 0;\nint value = stoi(\"12abc\", &used);   // value 12, used 2",
                },
                {
                    "heading": "Common mistakes",
                    "text": "Catching with `catch (...)` hides every error, including real bugs - name the exception you expect.\n\nUsing a helper that is defined below the function that calls it - move it above.",
                },
            ],
            "quiz": [
                {
                    "question": "What do these two calls return?",
                    "code": "int f(int x, int y = 2) {\n    return x * y;\n}\n\nf(3)\nf(3, 3)",
                    "answer": "`6` and `9`.",
                },
                {
                    "question": "What are `a` and `used`?",
                    "code": "size_t used = 0;\nint a = stoi(\"42 apples\", &used);",
                    "answer": "`a` is `42` and `used` is `2`: stoi stopped at the space, and only the first two characters were part of the number.",
                },
                {
                    "question": "What is `result`?",
                    "code": "int parse(const string& t) {\n    try {\n        return stoi(t);\n    } catch (const invalid_argument& e) {\n        return -1;\n    }\n}\n\nvector<int> result = {parse(\"12\"), parse(\"x\"), parse(\"7\")};",
                    "answer": "`{12, -1, 7}`. stoi(\"x\") throws invalid_argument, which the catch turns into -1.",
                },
            ],
            "problems": [
                port(
                    "safe-divide",
                    signature=fn("safe_divide", "float", a="float", b="float"),
                    description="Return a divided by b. If b is zero, throw invalid_argument.",
                    hints=[
                        "There is one input your function must refuse. Everything else is an ordinary division.",
                        "Check for the bad input first.",
                        "throw invalid_argument(\"b must not be zero\"); stops the function with an error.",
                        "Structure: if (b == 0) throw invalid_argument(...); return a / b;",
                    ],
                    questions=[
                        "What does dividing a double by zero do in C++ if you do not check?",
                        "Why is an exception better than returning 0?",
                    ],
                ),
                port(
                    "to-int",
                    signature=fn("to_int", "int", text="str", fallback=("int", 0)),
                    description="Convert text to a whole number. If text is not entirely a whole number (an optional sign and digits, possibly after leading spaces), return fallback instead - which is 0 unless the caller passes something else.",
                    tests=[
                        {"args": ["42"], "expected": 42},
                        {"args": ["abc", -1], "expected": -1},
                        {"args": ["-7"], "expected": -7},
                        {"args": ["abc"], "expected": 0},
                        {"args": ["", 5], "expected": 5},
                        {"args": ["3.5"], "expected": 0, "edge": "text after the number"},
                        {"args": ["12abc"], "expected": 0, "edge": "text after the number"},
                        {"args": [" 12"], "expected": 12},
                    ],
                    hints=[
                        "stoi already converts text. Your job is the cases where it refuses - and the case where it only reads part of the text.",
                        "stoi throws invalid_argument when the text does not start with a number. Catch that.",
                        "stoi(text, &used) also tells you how many characters it used. If used is less than text.size(), there was something after the number.",
                        "Structure: try { size_t used = 0; int value = stoi(text, &used); if (used != text.size()) return fallback; return value; } catch (const invalid_argument&) { return fallback; }",
                    ],
                    questions=[
                        "Why is \"12abc\" a trap with stoi?",
                        "stoi can also throw out_of_range. For which input?",
                    ],
                ),
                port(
                    "parse-scores",
                    signature=fn("parse_scores", "list[int]", text="str"),
                    description="text holds scores separated by commas, like \"90,80,abc,70\". Return a vector of the pieces that are whole numbers, as ints, in order - skip every piece that is not entirely a number.",
                    tests=[
                        {"args": ["90,80,abc,70"], "expected": [90, 80, 70]},
                        {"args": ["1,2,3"], "expected": [1, 2, 3]},
                        {"args": [""], "expected": []},
                        {"args": ["x,y"], "expected": []},
                        {"args": ["7"], "expected": [7]},
                        {"args": ["10,,20"], "expected": [10, 20]},
                        {"args": ["5x,6"], "expected": [6], "edge": "text after the number"},
                    ],
                    hints=[
                        "Plan: cut the text into pieces at the commas, try to turn each piece into a number, keep the ones that work.",
                        "getline(stream, piece, ',') reads one comma-separated piece at a time from an istringstream.",
                        "Turning a piece into a number is To Int again: stoi with the used-characters check, inside try/catch. Write it as a helper function above parse_scores.",
                        "Structure: istringstream in(text); string piece; while (getline(in, piece, ',')) { if piece is a whole number, push_back it } return the vector.",
                    ],
                ),
                port(
                    "primes",
                    starter=CPP_HEADER + "\nbool is_prime(int n) {\n    // your code here\n    return false;\n}\n\nvector<int> primes_up_to(int n) {\n    // your code here\n    return {};\n}\n",
                    hints=[
                        "Solve the small problem first: write is_prime on its own. Then primes_up_to is the filtering pattern with is_prime as the test.",
                        "Numbers below 2 are never prime. Otherwise n is prime if no d from 2 to n - 1 divides it evenly - and the first divisor you find settles the answer.",
                        "A divisor test is n % d == 0. Return false inside the loop, true after it. is_prime must be above primes_up_to so it can be called.",
                        "Structure: is_prime: if (n < 2) return false; for (int d = 2; d < n; d++) if (n % d == 0) return false; return true. primes_up_to: vector<int> result; for k from 2 to n: if (is_prime(k)) result.push_back(k); return result;",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-recursion",
            "title": "Recursion",
            "summary": "Solve a problem by solving a smaller version of the same problem.",
            "lesson": [
                {
                    "heading": "The same idea as in Python",
                    "text": "A recursive function calls itself on a smaller problem until it reaches a base case it can answer directly. Every recursive function needs both parts: a base case, and a recursive case that makes the input smaller.",
                    "code": "long long factorial(int n) {\n    if (n == 0) {\n        return 1;                    // base case\n    }\n    return n * factorial(n - 1);     // smaller problem\n}",
                },
                {
                    "heading": "No slicing: pass a position instead",
                    "text": "Python's `nums[1:]` makes a new, shorter list. In C++ you can do the same with `vector<int>(nums.begin() + 1, nums.end())`, but copying at every step is slow. The usual C++ way is a helper function with an extra parameter that says where 'the rest' starts.",
                    "code": "int total_from(const vector<int>& nums, int start) {\n    if (start == (int)nums.size()) {\n        return 0;                                   // nothing left\n    }\n    return nums[start] + total_from(nums, start + 1);\n}\n\nint total(const vector<int>& nums) {\n    return total_from(nums, 0);\n}",
                },
                {
                    "heading": "Strings",
                    "text": "For strings, `s.substr(1)` is 'everything after the first character' - a smaller string to recurse on, like Python's `s[1:]`.",
                },
                {
                    "heading": "When it goes wrong",
                    "text": "If the input never gets smaller, or the base case is never reached, the calls pile up until the program runs out of stack space and crashes. Antivibe reports this as a stack overflow. Python stops with a RecursionError; C++ just crashes.",
                },
                {
                    "heading": "Trust the recursion",
                    "text": "As in Python: get the base case right, assume the call on the smaller input already works, and ask only how to turn that answer into the answer for the whole.",
                },
            ],
            "quiz": [
                {
                    "question": "What does `r(3)` return?",
                    "code": "int r(int n) {\n    if (n == 0) return 0;\n    return n + r(n - 1);\n}",
                    "answer": "`6`: 3 + 2 + 1 + 0.",
                },
                {
                    "question": "What does `w(\"abc\")` return?",
                    "code": "string w(const string& s) {\n    if (s.empty()) return \"\";\n    return w(s.substr(1)) + s[0];\n}",
                    "answer": "`\"cba\"`: w(\"abc\") = w(\"bc\") + 'a' = (w(\"c\") + 'b') + 'a' = ((\"\" + 'c') + 'b') + 'a'.",
                },
                {
                    "question": "What happens when you call `h(3)`?",
                    "code": "int h(int n) {\n    if (n == 0) return 0;\n    return h(n) + 1;\n}",
                    "answer": "The program crashes with a stack overflow: h(3) calls h(3) forever, because the input never gets smaller.",
                },
            ],
            "problems": [
                port(
                    "factorial",
                    signature=fn("factorial", "long", n="int"),
                    hints=[
                        "5! is 5 x 4 x 3 x 2 x 1. The part after the 5 is 4!.",
                        "The factorial of n is n times the factorial of n - 1.",
                        "The chain has to stop: the factorial of 0 is 1 with no calculation. The return type is long long because factorials grow very fast.",
                        "Structure: if (n == 0) return 1; return n * factorial(n - 1);",
                    ],
                    questions=[
                        "What happens if you leave out the base case?",
                        "For which n does the answer stop fitting in a long long?",
                    ],
                ),
                port(
                    "power",
                    signature=fn("power", "long", base="int", exp="int"),
                    description="Return base raised to the power exp, where exp is a whole number 0 or greater. Write it recursively, without pow().",
                    hints=[
                        "2 to the power 10 is 2 times 2 to the power 9 - the same shape as factorial.",
                        "Find the smallest exponent whose answer needs no multiplication. That is the base case.",
                        "Anything to the power 0 is 1. Otherwise multiply base by power(base, exp - 1).",
                        "Structure: if (exp == 0) return 1; return base * power(base, exp - 1);",
                    ],
                ),
                {
                    "id": "count-down",
                    "title": "Debug: Count Down",
                    "difficulty": "easy",
                    "description": "count_down(n) should return {n, n - 1, ..., 1, 0}. Instead the program crashes for most inputs. Find the bug and fix it.",
                    "signature": fn("count_down", "list[int]", n="int"),
                    "starter": CPP_HEADER + "\nvector<int> count_down(int n) {\n    if (n == 0) {\n        return {0};\n    }\n    vector<int> result = {n};\n    vector<int> rest = count_down(n);\n    result.insert(result.end(), rest.begin(), rest.end());\n    return result;\n}\n",
                    "compare": "exact",
                    "tests": [
                        {"args": [3], "expected": [3, 2, 1, 0]},
                        {"args": [1], "expected": [1, 0]},
                        {"args": [0], "expected": [0]},
                        {"args": [5], "expected": [5, 4, 3, 2, 1, 0]},
                        {"args": [2], "expected": [2, 1, 0]},
                    ],
                    "hints": [
                        "The results panel says 'stack overflow'. Write out the calls by hand for count_down(1). What does the second call receive?",
                        "Every recursive call must get a smaller problem, so it eventually reaches the base case.",
                        "The base case is fine. The recursive call passes n unchanged, so n never reaches 0.",
                        "Structure: the recursive call should count down from n - 1.",
                    ],
                    "questions": [
                        "Why did count_down(0) pass with the bug?",
                        "What does result.insert(result.end(), rest.begin(), rest.end()) do?",
                    ],
                },
                port(
                    "sum-list",
                    signature=fn("sum_list", "int", nums="array[int]"),
                    description="Return the sum of the numbers in nums, recursively - no loops and no std::accumulate. You may write a helper function.",
                    hints=[
                        "The lesson's 'pass a position instead' example is exactly this problem. Try it without looking back.",
                        "The sum is the first item plus the sum of the rest. With no slicing, 'the rest' means 'from the next position onwards'.",
                        "Write a helper sum_from(nums, start). Its base case is start == size: nothing left, so 0.",
                        "Structure: int sum_from(const vector<int>& nums, int start) { if (start == (int)nums.size()) return 0; return nums[start] + sum_from(nums, start + 1); } and sum_list returns sum_from(nums, 0).",
                    ],
                ),
                port(
                    "reverse-recursive",
                    signature=fn("reverse_recursive", "str", s="str"),
                    description="Return s reversed, using recursion - no loops and no std::reverse.",
                    hints=[
                        "Split the string into its first character and the rest. If the rest were already reversed, where does the first character go?",
                        "Reverse of \"abc\" = (reverse of \"bc\") followed by 'a'.",
                        "s[0] is the first character and s.substr(1) the rest. The empty string is its own reverse.",
                        "Structure: if (s.empty()) return \"\"; return reverse_recursive(s.substr(1)) + s[0];",
                    ],
                ),
            ],
        },
    ],
}
