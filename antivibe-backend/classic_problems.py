"""Classic algorithm problems that the curriculum tracks place into milestones.

The problem format is described in problems.py. Look problems up by id:

    CLASSIC["two-sum"]
"""

_PROBLEMS = [
    {
        "id": "fizz-buzz",
        "title": "Fizz Buzz",
        "difficulty": "warm-up",
        "description": (
            "Return a list of strings for the numbers 1 to n (inclusive). "
            "For multiples of 3 use \"Fizz\", for multiples of 5 use \"Buzz\", "
            "for multiples of both use \"FizzBuzz\", and otherwise use the number "
            "itself as a string. If n is 0, return an empty list."
        ),
        "function": {"name": "fizz_buzz", "params": ["n"]},
        "compare": "exact",
        "tests": [
            {"args": [3], "expected": ["1", "2", "Fizz"]},
            {"args": [5], "expected": ["1", "2", "Fizz", "4", "Buzz"]},
            {"args": [1], "expected": ["1"]},
            {"args": [0], "expected": []},
            {
                "args": [15],
                "expected": [
                    "1", "2", "Fizz", "4", "Buzz", "Fizz", "7", "8", "Fizz", "Buzz",
                    "11", "Fizz", "13", "14", "FizzBuzz",
                ],
            },
        ],
        "hints": [
            "You need to look at every number from 1 to n once and decide which of four things to add to your answer.",
            "The remainder operator (%) tells you whether one number divides another evenly. Build the result list as you loop.",
            "The order of your checks matters: a number like 15 is a multiple of 3 and of 5. Which check has to come first so it isn't caught by a less specific one?",
            "Structure: create an empty list; loop i from 1 to n inclusive; use an if / elif / elif / else chain that tests 'both' first; append a string each time (convert plain numbers with str); return the list after the loop.",
        ],
        "questions": [
            "Why does range(1, n) give the wrong answer here?",
            "What happens if you check 'multiple of 3' before 'multiple of both'?",
        ],
        "resources": [
            "https://docs.python.org/3/tutorial/controlflow.html",
        ],
    },
    {
        "id": "reverse-string",
        "title": "Reverse a String",
        "difficulty": "warm-up",
        "description": (
            "Return the characters of the string s in reverse order. "
            "For practice, try to do it without slicing (s[::-1]) or reversed()."
        ),
        "function": {"name": "reverse_string", "params": ["s"]},
        "compare": "exact",
        "tests": [
            {"args": ["hello"], "expected": "olleh"},
            {"args": ["ab"], "expected": "ba"},
            {"args": [""], "expected": ""},
            {"args": ["a"], "expected": "a"},
            {"args": ["racecar"], "expected": "racecar"},
            {"args": ["Hello, World!"], "expected": "!dlroW ,olleH"},
        ],
        "hints": [
            "Reversing means the last character becomes the first, the second-to-last becomes the second, and so on. How could you visit the characters in that order?",
            "Two common approaches: walk the string from the last index down to 0 collecting characters, or swap characters from both ends moving inwards (two pointers).",
            "Strings in Python are immutable, so you can't swap characters in place. Either collect characters in a list and join them at the end, or convert the string to a list first.",
            "Structure (two pointers): chars = list of the characters; left starts at 0 and right at the last index; while left < right, swap the two and move both inwards; finally join chars back into a string.",
        ],
        "questions": [
            "What is the time and space complexity of your approach?",
            "Why is building a string with += inside a loop slower than joining a list?",
        ],
        "resources": [
            "https://leetcode.com/problems/reverse-string/",
        ],
    },
    {
        "id": "valid-palindrome",
        "title": "Valid Palindrome",
        "difficulty": "easy",
        "description": (
            "Return True if s reads the same forwards and backwards once you ignore "
            "upper/lower case and skip every character that is not a letter or a digit. "
            "Otherwise return False. An empty string counts as a palindrome."
        ),
        "function": {"name": "is_palindrome", "params": ["s"]},
        "compare": "exact",
        "tests": [
            {"args": ["A man, a plan, a canal: Panama"], "expected": True},
            {"args": ["race a car"], "expected": False},
            {"args": [""], "expected": True},
            {"args": [" "], "expected": True},
            {"args": ["0P"], "expected": False},
            {"args": ["ab_a"], "expected": True},
            {"args": ["No lemon, no melon"], "expected": True},
        ],
        "hints": [
            "A palindrome mirrors around its centre: the first meaningful character must match the last, the second must match the second-to-last, and so on.",
            "Either clean the string first (keep only letters and digits, lower-cased) and compare it with its reverse, or use two pointers moving inwards and skip the characters that don't count.",
            "str.isalnum() tells you whether a character is a letter or digit, and str.lower() removes case differences. With two pointers, advance each pointer past characters that fail isalnum() before comparing.",
            "Structure (two pointers): left = 0, right = last index; while left < right: move left forward while it points at a non-alphanumeric character, move right backward likewise; if the lower-cased characters differ return False; otherwise step both inwards. Return True after the loop.",
        ],
        "questions": [
            "Which of the two approaches uses extra memory, and how much?",
            "What should happen for a string made only of punctuation?",
        ],
        "resources": [
            "https://leetcode.com/problems/valid-palindrome/",
        ],
    },
    {
        "id": "contains-duplicate",
        "title": "Contains Duplicate",
        "difficulty": "easy",
        "description": (
            "Return True if any value appears at least twice in the list nums, "
            "and False if every element is distinct."
        ),
        "function": {"name": "contains_duplicate", "params": ["nums"]},
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 3, 1]], "expected": True},
            {"args": [[1, 2, 3, 4]], "expected": False},
            {"args": [[]], "expected": False},
            {"args": [[7]], "expected": False},
            {"args": [[0, 0]], "expected": True},
            {"args": [[-1, 1, 2, -2]], "expected": False},
            {"args": [[5, 4, 3, 2, 1, 5]], "expected": True},
        ],
        "hints": [
            "As you walk through the list, the only question for each number is: 'have I seen this one before?'",
            "Comparing every pair works but takes O(n^2) time. A data structure with fast membership checks lets you answer 'seen before?' in constant time.",
            "A set is exactly that structure: `x in my_set` is O(1) on average. Add each number to the set after checking it.",
            "Structure: start with an empty set; for each number, if it is already in the set return True, otherwise add it; if the loop finishes, return False.",
        ],
        "questions": [
            "What is the time complexity of the brute-force (every pair) approach?",
            "What do you trade away to get the faster solution?",
            "Could you solve it by sorting first? What would that cost?",
        ],
        "resources": [
            "https://leetcode.com/problems/contains-duplicate/",
        ],
    },
    {
        "id": "two-sum",
        "title": "Two Sum",
        "difficulty": "easy",
        "description": (
            "Given a list of integers nums and an integer target, return the indices "
            "of the two numbers that add up to target. Exactly one pair works, and you "
            "may not use the same element twice. The two indices can be in any order."
        ),
        "function": {"name": "two_sum", "params": ["nums", "target"]},
        "compare": "unordered",
        "tests": [
            {"args": [[2, 7, 11, 15], 9], "expected": [0, 1]},
            {"args": [[3, 2, 4], 6], "expected": [1, 2]},
            {"args": [[3, 3], 6], "expected": [0, 1]},
            {"args": [[-1, -2, -3, -4, -5], -8], "expected": [2, 4]},
            {"args": [[0, 4, 3, 0], 0], "expected": [0, 3]},
            {"args": [[1, 5, 8, 13], 14], "expected": [0, 3]},
        ],
        "hints": [
            "For any number x in the list, there is exactly one partner value that would complete the pair. What is it, in terms of x and target?",
            "Checking every pair is O(n^2). If you could ask 'have I already seen the partner of this number?' in constant time, one pass would be enough.",
            "A dictionary mapping each value you've seen to its index gives you that lookup. Check for the partner before you store the current number, so an element is never paired with itself.",
            "Structure: empty dict; loop over the list with enumerate to get index and value; compute the partner; if the partner is a key in the dict, return its stored index together with the current index; otherwise store value -> index and continue.",
        ],
        "questions": [
            "Why does [3, 2, 4] with target 6 trip up a solution that pairs an element with itself?",
            "What are the time and space complexities of the brute-force and the dictionary approach?",
            "How does your solution behave when the list contains duplicate numbers?",
        ],
        "resources": [
            "https://leetcode.com/problems/two-sum/",
        ],
    },
    {
        "id": "valid-anagram",
        "title": "Valid Anagram",
        "difficulty": "easy",
        "description": (
            "Return True if t is an anagram of s - that is, t uses exactly the same "
            "characters as s, the same number of times each, in any order. "
            "Otherwise return False."
        ),
        "function": {"name": "is_anagram", "params": ["s", "t"]},
        "compare": "exact",
        "tests": [
            {"args": ["anagram", "nagaram"], "expected": True},
            {"args": ["rat", "car"], "expected": False},
            {"args": ["", ""], "expected": True},
            {"args": ["a", "ab"], "expected": False},
            {"args": ["aacc", "ccac"], "expected": False},
            {"args": ["listen", "silent"], "expected": True},
        ],
        "hints": [
            "Two words are anagrams when they contain the same letters in the same quantities. Order is the only thing allowed to differ.",
            "You can either put both strings into a canonical order and compare, or count how often each character appears in each string and compare the counts.",
            "A dictionary from character to count works well: dict.get(ch, 0) + 1 increments a count that may not exist yet. Strings of different lengths can be rejected immediately.",
            "Structure (counting): if the lengths differ return False; build a count dict from s; for each character in t, decrement its count and return False if the character is missing or its count would go below zero; return True at the end.",
        ],
        "questions": [
            "Why is the length check enough to make the one-dictionary approach correct?",
            "How do the sorting and counting approaches compare in time complexity?",
        ],
        "resources": [
            "https://leetcode.com/problems/valid-anagram/",
        ],
    },
    {
        "id": "binary-search",
        "title": "Binary Search",
        "difficulty": "easy",
        "description": (
            "nums is a list of distinct integers sorted in ascending order. Return the "
            "index of target in nums, or -1 if it is not there. Aim for O(log n) time - "
            "do not just scan the whole list."
        ),
        "function": {"name": "binary_search", "params": ["nums", "target"]},
        "compare": "exact",
        "tests": [
            {"args": [[-1, 0, 3, 5, 9, 12], 9], "expected": 4},
            {"args": [[-1, 0, 3, 5, 9, 12], 2], "expected": -1},
            {"args": [[], 1], "expected": -1},
            {"args": [[5], 5], "expected": 0},
            {"args": [[5], -5], "expected": -1},
            {"args": [[1, 3], 3], "expected": 1},
            {"args": [[1, 2, 3, 4, 5, 6, 7], 1], "expected": 0},
            {"args": [[1, 2, 3, 4, 5, 6, 7], 7], "expected": 6},
        ],
        "hints": [
            "Because the list is sorted, looking at a single element tells you something about every element on one side of it.",
            "Keep track of the range that could still contain the target. Look at the middle of that range and throw away the half that can't contain it.",
            "Use two indices, left and right, for the ends of the remaining range. Decide carefully whether the range includes right, and make your loop condition and your updates agree with that decision.",
            "Structure: left = 0, right = last index; while left <= right: mid = middle index; if the middle value is the target return mid; if it is smaller, the target must be to the right, so move left to mid + 1; otherwise move right to mid - 1. Return -1 after the loop.",
        ],
        "questions": [
            "Why must the list be sorted for this to work?",
            "What goes wrong if you update with left = mid instead of left = mid + 1?",
            "How many steps does a list of one million elements need at most?",
        ],
        "resources": [
            "https://leetcode.com/explore/learn/card/binary-search/",
        ],
    },
    {
        "id": "valid-parentheses",
        "title": "Valid Parentheses",
        "difficulty": "easy",
        "description": (
            "s contains only the characters ( ) [ ] { }. Return True if every opening "
            "bracket is closed by the same type of bracket and in the correct order, "
            "otherwise False. An empty string is valid."
        ),
        "function": {"name": "is_valid", "params": ["s"]},
        "compare": "exact",
        "tests": [
            {"args": ["()[]{}"], "expected": True},
            {"args": ["(]"], "expected": False},
            {"args": ["()"], "expected": True},
            {"args": ["([)]"], "expected": False},
            {"args": ["{[]}"], "expected": True},
            {"args": [""], "expected": True},
            {"args": ["("], "expected": False},
            {"args": [")"], "expected": False},
            {"args": ["(("], "expected": False},
        ],
        "hints": [
            "When you meet a closing bracket, which opening bracket must it match: the first one you saw, or the most recent one that is still open?",
            "'Most recent first' is last-in, first-out behaviour, which is exactly what a stack gives you. A Python list with append and pop works as a stack.",
            "Push opening brackets. On a closing bracket, the stack must be non-empty and its top must be the matching opener. A dictionary from closing bracket to opening bracket keeps the matching logic short.",
            "Structure: empty stack; for each character: if it is an opener, push it; otherwise, if the stack is empty or the popped item isn't the matching opener, return False. After the loop the answer is whether the stack is empty.",
        ],
        "questions": [
            "Which test case fails if you forget to check that the stack is empty at the end?",
            "Why can't you solve this by just counting each bracket type?",
        ],
        "resources": [
            "https://leetcode.com/problems/valid-parentheses/",
        ],
    },
    {
        "id": "merge-sorted-lists",
        "title": "Merge Two Sorted Lists",
        "difficulty": "easy",
        "description": (
            "a and b are lists of integers, each already sorted in ascending order. "
            "Return a new sorted list containing every element of both. "
            "Try to do it in a single pass, without calling sort() or sorted()."
        ),
        "function": {"name": "merge_sorted", "params": ["a", "b"]},
        "compare": "exact",
        "tests": [
            {"args": [[1, 3, 5], [2, 4, 6]], "expected": [1, 2, 3, 4, 5, 6]},
            {"args": [[1, 1, 2], [1, 3]], "expected": [1, 1, 1, 2, 3]},
            {"args": [[], []], "expected": []},
            {"args": [[1], []], "expected": [1]},
            {"args": [[], [2, 3]], "expected": [2, 3]},
            {"args": [[-5, 0], [-7, -6, 10]], "expected": [-7, -6, -5, 0, 10]},
            {"args": [[1, 2, 3], [4, 5, 6]], "expected": [1, 2, 3, 4, 5, 6]},
        ],
        "hints": [
            "Both lists are already sorted, so the smallest element overall has to be at the front of one of them.",
            "Keep one position in each list. Repeatedly compare the two current elements, take the smaller one, and advance only the list you took from.",
            "The main loop can only run while both lists still have elements left. When one runs out, whatever remains in the other is already sorted and can be appended as it is.",
            "Structure: i = j = 0 and an empty result; while i and j are both in range: append the smaller of a[i] and b[j] and advance that index; after the loop, extend the result with the leftovers of a from i and of b from j; return the result.",
        ],
        "questions": [
            "What is the time complexity in terms of the two list lengths?",
            "Why is this better than concatenating the lists and sorting?",
            "Where is this merge step used inside a well-known sorting algorithm?",
        ],
        "resources": [
            "https://leetcode.com/problems/merge-sorted-array/",
        ],
    },
    {
        "id": "max-subarray",
        "title": "Maximum Subarray",
        "difficulty": "medium",
        "description": (
            "Given a non-empty list of integers nums, find the contiguous run of "
            "elements (at least one) with the largest sum, and return that sum."
        ),
        "function": {"name": "max_subarray", "params": ["nums"]},
        "compare": "exact",
        "tests": [
            {"args": [[-2, 1, -3, 4, -1, 2, 1, -5, 4]], "expected": 6},
            {"args": [[5, 4, -1, 7, 8]], "expected": 23},
            {"args": [[1]], "expected": 1},
            {"args": [[-3, -1, -2]], "expected": -1},
            {"args": [[0]], "expected": 0},
            {"args": [[2, -1, 2]], "expected": 3},
            {"args": [[-1, 5, -10, 4]], "expected": 5},
        ],
        "hints": [
            "Think about the best run that ends exactly at position i. How does it relate to the best run that ends at position i - 1?",
            "At each element you have two choices: extend the run that ended just before it, or start a fresh run at this element. When is starting fresh the better choice?",
            "Track two values as you scan: the best sum of a run ending at the current element, and the best sum seen anywhere so far. Be careful with your starting values - an all-negative list must not return 0.",
            "Structure: set both trackers to the first element; for each remaining element: the current-run value becomes the larger of (the element alone) and (current-run + the element); then update the overall best if the current-run value beats it. Return the overall best.",
        ],
        "questions": [
            "Why does starting your trackers at 0 give the wrong answer for [-3, -1, -2]?",
            "What is the complexity of trying every possible start and end instead?",
        ],
        "resources": [
            "https://leetcode.com/problems/maximum-subarray/",
            "https://en.wikipedia.org/wiki/Maximum_subarray_problem",
        ],
    },
    {
        "id": "climbing-stairs",
        "title": "Climbing Stairs",
        "difficulty": "medium",
        "description": (
            "You are climbing a staircase with n steps (n >= 1). Each move you can go "
            "up 1 step or 2 steps. Return the number of distinct ways to reach the top."
        ),
        "function": {"name": "climb_stairs", "params": ["n"]},
        "compare": "exact",
        "tests": [
            {"args": [2], "expected": 2},
            {"args": [3], "expected": 3},
            {"args": [1], "expected": 1},
            {"args": [4], "expected": 5},
            {"args": [5], "expected": 8},
            {"args": [10], "expected": 89},
            {"args": [30], "expected": 1346269},
        ],
        "hints": [
            "Work out the answers for n = 1, 2, 3, 4 and 5 by hand and write them in a row. Do you see a pattern?",
            "Think about the very last move onto step n. It was either a 1-step from step n - 1 or a 2-step from step n - 2, so the ways to reach n depend on the ways to reach those two steps.",
            "A plain recursive function recomputes the same sub-answers over and over. Build the answers from the bottom up instead; you only ever need the previous two values.",
            "Structure: handle n = 1 and n = 2 directly; keep two variables for the answers to the previous two steps; loop from 3 up to n, each time computing their sum and shifting the two variables along; return the last value computed.",
        ],
        "questions": [
            "Which famous number sequence does this produce, and why?",
            "How many calls does the naive recursive version make for n = 30?",
            "How would the recurrence change if you could also take 3 steps at once?",
        ],
        "resources": [
            "https://leetcode.com/problems/climbing-stairs/",
        ],
    },
]

CLASSIC = {problem["id"]: problem for problem in _PROBLEMS}
