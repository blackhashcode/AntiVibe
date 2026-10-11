"""Track 3: Data Structures & Algorithms. The format is described in problems.py."""
from classic_problems import CLASSIC

LINKED_LIST_STARTER = '''class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        pass

    def prepend(self, value):
        pass

    def to_list(self):
        pass

    def __len__(self):
        pass
'''

REVERSE_LINKED_LIST_STARTER = '''class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # append and to_list are given - you only write reverse
    def append(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = node

    def to_list(self):
        values = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def reverse(self):
        pass
'''

TRACK = {
    "id": "dsa",
    "title": "Data Structures & Algorithms",
    "description": "Solve problems efficiently with the classic structures and techniques.",
    "milestones": [
        # ------------------------------------------------------------------
        {
            "id": "dsa-hashing",
            "title": "Complexity, Arrays & Hashing",
            "summary": "Measure how fast a solution is, and use dictionaries and sets to avoid repeated scanning.",
            "lesson": [
                {
                    "heading": "Correct is not enough",
                    "text": "From here on, most problems have an obvious solution that is too slow and a cleverer one that is fast. DSA is the skill of finding the second kind. First you need a way to say how fast a solution is.",
                },
                {
                    "heading": "Big-O in one minute",
                    "text": "Big-O describes how the amount of work grows as the input grows, ignoring constant factors. For a list of n items:\n\n`O(1)` - the same work whatever n is (reading one index, a dictionary lookup).\n\n`O(n)` - work proportional to n (one loop over the list).\n\n`O(n^2)` - a loop inside a loop: for 1,000 items that is 1,000,000 steps.\n\n`O(log n)` - halving the problem each step: 1,000,000 items take about 20 steps.",
                },
                {
                    "heading": "Count the loops",
                    "text": "To estimate a solution's complexity, look at its loops. One loop over the input is O(n). A loop nested inside another is O(n^2). Hidden loops count too: `x in some_list` scans the list, so using it inside a loop is quietly O(n^2).",
                    "code": "for a in nums:              # n times\n    for b in nums:          # n times each\n        ...                 # n * n steps in total",
                },
                {
                    "heading": "Trading memory for speed",
                    "text": "A dictionary or set answers 'have I seen this?' in O(1). Remembering what you have seen, in a set or dict, often replaces an inner loop and turns O(n^2) into O(n). The price is O(n) extra memory. This is the single most common trick in interview-style problems.",
                    "code": "seen = set()\nfor n in nums:\n    if n in seen:        # O(1), not a scan\n        ...\n    seen.add(n)",
                },
                {
                    "heading": "How to approach each problem",
                    "text": "1. Solve a small example by hand.\n\n2. Write the brute-force solution in your head and work out its complexity.\n\n3. Ask what work is being repeated, and what you could remember to avoid it.",
                },
            ],
            "problems": [
                CLASSIC["two-sum"],
                {
                    "id": "missing-number",
                    "title": "Missing Number",
                    "difficulty": "easy",
                    "description": "nums contains n different numbers taken from the range 0 to n, so exactly one number of that range is missing. Return the missing number.",
                    "function": {"name": "missing_number", "params": ["nums"]},
                    "compare": "exact",
                    "tests": [
                        {"args": [[3, 0, 1]], "expected": 2},
                        {"args": [[0, 1]], "expected": 2},
                        {"args": [[1]], "expected": 0},
                        {"args": [[0]], "expected": 1},
                        {"args": [[9, 6, 4, 2, 3, 5, 7, 0, 1]], "expected": 8},
                        {"args": [[1, 2, 3]], "expected": 0},
                    ],
                    "hints": [
                        "If the list has n numbers, the full range is 0 to n: that is n + 1 candidates, and one of them is absent.",
                        "Brute force: for each candidate, scan the list to see whether it is there. That is a loop inside a loop. What could make the 'is it there?' question instant?",
                        "Put the numbers in a set, then walk through the candidates 0..n and return the first one the set does not contain. (There is also a neat arithmetic way using the sum of 0..n.)",
                        "Structure: build a set from nums; loop a candidate over range(len(nums) + 1); return the candidate that is not in the set.",
                    ],
                    "questions": [
                        "What is the complexity of the brute-force version, and of yours?",
                        "The sum approach needs no extra memory. How does it work?",
                    ],
                },
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "dsa-two-pointers",
            "title": "Two Pointers",
            "summary": "Walk through data with two positions at once instead of nested loops.",
            "lesson": [
                {
                    "heading": "The idea",
                    "text": "A 'pointer' here is just a variable holding an index. Many problems that look like they need a loop inside a loop can be solved with two indexes that each move forward only, giving O(n) instead of O(n^2).",
                },
                {
                    "heading": "Pattern 1: one pointer per sequence",
                    "text": "When you have two sequences, keep a position in each. At every step, look at the two current items, decide what to do, and advance one pointer (or both).",
                    "code": "i = 0\nj = 0\nwhile i < len(a) and j < len(b):\n    # compare a[i] and b[j], then move i or j\n    ...",
                },
                {
                    "heading": "Pattern 2: from both ends",
                    "text": "On a single sequence, start one pointer at each end and move them towards each other until they meet. You used this for palindromes and for reversing.",
                    "code": "left = 0\nright = len(s) - 1\nwhile left < right:\n    ...\n    left += 1\n    right -= 1",
                },
                {
                    "heading": "Getting the loop right",
                    "text": "Two things go wrong most often. First, the loop condition: it must stop before either index goes out of range. Second, the leftovers: when the loop ends because one sequence ran out, the other may still have items you need to deal with.",
                },
            ],
            "problems": [
                CLASSIC["merge-sorted-lists"],
                {
                    "id": "is-subsequence",
                    "title": "Is Subsequence",
                    "difficulty": "easy",
                    "description": "Return True if s is a subsequence of t: you can get s by deleting zero or more characters from t without changing the order of the rest. For example \"ace\" is a subsequence of \"abcde\", but \"aec\" is not.",
                    "function": {"name": "is_subsequence", "params": ["s", "t"]},
                    "compare": "exact",
                    "tests": [
                        {"args": ["abc", "ahbgdc"], "expected": True},
                        {"args": ["axc", "ahbgdc"], "expected": False},
                        {"args": ["", "abc"], "expected": True},
                        {"args": ["", ""], "expected": True},
                        {"args": ["abc", ""], "expected": False},
                        {"args": ["aaa", "aa"], "expected": False},
                        {"args": ["ace", "abcde"], "expected": True},
                        {"args": ["aec", "abcde"], "expected": False},
                    ],
                    "hints": [
                        "Read t from left to right while keeping a finger on the next character of s you still need to find.",
                        "Use one index into s and one into t. The t index always moves forward. When does the s index move?",
                        "Advance the s pointer only when the two current characters match. If the s pointer reaches the end of s, every character of s was found in order.",
                        "Structure: i = 0 and j = 0; while both are in range: if s[i] equals t[j], advance i; always advance j. After the loop, return whether i equals len(s).",
                    ],
                    "questions": [
                        "Why is it safe to match each character of s at the earliest possible place in t?",
                        "What is the complexity in terms of the two lengths?",
                    ],
                },
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "dsa-stack",
            "title": "Stacks in Action",
            "summary": "Use last-in, first-out order to match, nest and evaluate.",
            "lesson": [
                {
                    "heading": "When to reach for a stack",
                    "text": "You built a Stack class in the OOP track. A stack is the right tool whenever the most recent unfinished thing has to be dealt with first: nested brackets, undo, function calls, or evaluating expressions.",
                },
                {
                    "heading": "A list is a stack",
                    "text": "In day-to-day Python you do not need your own class: a plain list works as a stack. `append` pushes, `pop()` pops, `stack[-1]` peeks, and an empty list is falsy, so `not stack` means 'the stack is empty'.",
                    "code": "stack = []\nstack.append(1)\nstack.append(2)\nstack[-1]        # 2\nstack.pop()      # 2\nnot stack        # False - it still holds 1",
                },
                {
                    "heading": "The usual shape",
                    "text": "Loop over the input once. For each item, either push it for later, or pop one or more earlier items and combine them with the current one. Each item is pushed and popped at most once, so these solutions are O(n).",
                },
                {
                    "heading": "Common mistakes",
                    "text": "Popping from an empty stack raises IndexError - check before you pop if the input might be unbalanced.\n\nForgetting the final check: when the input ends, leftover items on the stack usually mean something was never closed or used.",
                },
            ],
            "problems": [
                CLASSIC["valid-parentheses"],
                {
                    "id": "evaluate-rpn",
                    "title": "Reverse Polish Notation",
                    "difficulty": "medium",
                    "description": "tokens is a list of strings forming an expression in Reverse Polish Notation, where each operator comes after its two operands: [\"2\", \"1\", \"+\"] means 2 + 1. Each token is a whole number or one of the operators \"+\", \"-\" and \"*\". Return the value of the expression as an integer. For \"-\", the operand that appeared first is the one being subtracted from.",
                    "function": {"name": "evaluate_rpn", "params": ["tokens"]},
                    "compare": "exact",
                    "tests": [
                        {"args": [["2", "1", "+", "3", "*"]], "expected": 9},
                        {"args": [["4", "2", "-"]], "expected": 2},
                        {"args": [["5"]], "expected": 5},
                        {"args": [["2", "4", "-"]], "expected": -2},
                        {"args": [["1", "2", "+", "3", "4", "+", "*"]], "expected": 21},
                        {"args": [["10", "2", "3", "*", "-"]], "expected": 4},
                        {"args": [["-3", "2", "*"]], "expected": -6},
                    ],
                    "hints": [
                        "Work through [\"2\", \"1\", \"+\", \"3\", \"*\"] by hand. When you reach an operator, which numbers does it apply to?",
                        "An operator always applies to the two most recent values that have not been used yet - and its result becomes a value itself. 'Most recent first' means a stack.",
                        "Push numbers (converted with int). On an operator, pop twice: the first value popped is the right-hand operand, the second is the left-hand one. Push the result back.",
                        "Structure: empty stack; for each token: if it is \"+\", \"-\" or \"*\", pop right, then pop left, compute, and push the result; otherwise push int(token). At the end the stack holds exactly one value - return it.",
                    ],
                    "questions": [
                        "Which test fails if you mix up the left and right operands?",
                        "Why can you not detect numbers with token.isdigit() here?",
                    ],
                },
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "dsa-binary-search",
            "title": "Binary Search",
            "summary": "Find things in sorted data by halving the search space.",
            "lesson": [
                {
                    "heading": "Halving",
                    "text": "Looking for a word in a paper dictionary, you do not read every page: you open it in the middle and discard the half that cannot contain the word. Binary search does the same on a sorted list. Each step halves what is left, so a million items need only about 20 steps: O(log n).",
                },
                {
                    "heading": "The search range",
                    "text": "Keep two indexes marking the part of the list that could still contain the answer. Look at the middle element, then move one of the two indexes past it. The loop ends when the range is empty.",
                    "code": "left = 0\nright = len(nums) - 1\nwhile left <= right:\n    mid = (left + right) // 2\n    # compare nums[mid] with the target,\n    # then set left = mid + 1 or right = mid - 1",
                },
                {
                    "heading": "It only works on sorted data",
                    "text": "Discarding half is only valid because the list is sorted: if the middle element is too small, everything to its left is too small as well. On unsorted data that reasoning is false.",
                },
                {
                    "heading": "Common mistakes",
                    "text": "Infinite loops: if you set `left = mid` instead of `left = mid + 1`, the range can stop shrinking.\n\nOff-by-one errors: decide whether `right` is the last valid index or one past it, and keep the loop condition and the updates consistent with that choice. Always test lists of length 0, 1 and 2.",
                },
                {
                    "heading": "Beyond exact matches",
                    "text": "The same halving idea answers questions like 'where is the first element that is at least x?'. Instead of stopping when you find the target, you keep narrowing until the range closes on the boundary.",
                },
            ],
            "problems": [
                CLASSIC["binary-search"],
                {
                    "id": "first-at-least",
                    "title": "First Element At Least X",
                    "difficulty": "medium",
                    "description": "nums is sorted in ascending order and may contain repeated values. Return the index of the first element that is greater than or equal to target. If every element is smaller than target, return len(nums). Aim for O(log n).",
                    "function": {"name": "first_at_least", "params": ["nums", "target"]},
                    "compare": "exact",
                    "tests": [
                        {"args": [[1, 3, 5, 7], 5], "expected": 2},
                        {"args": [[1, 3, 5, 7], 4], "expected": 2},
                        {"args": [[1, 3, 5, 7], 0], "expected": 0},
                        {"args": [[1, 3, 5, 7], 8], "expected": 4},
                        {"args": [[], 1], "expected": 0},
                        {"args": [[2, 2, 2], 2], "expected": 0},
                        {"args": [[1, 2, 2, 3], 3], "expected": 3},
                        {"args": [[1, 2, 2, 3], 2], "expected": 1},
                    ],
                    "hints": [
                        "Every element is either 'too small' or 'big enough', and because the list is sorted, all the too-small ones come first. You are looking for the boundary between the two groups.",
                        "Use binary search, but do not stop when you see the target - an equal element further left might exist. Keep narrowing until the range is empty.",
                        "If nums[mid] is too small, the boundary is to the right of mid. If nums[mid] is big enough, mid itself might be the answer, so remember it or keep it in range, and continue to the left.",
                        "Structure: left = 0, right = len(nums) - 1, answer = len(nums); while left <= right: compute mid; if nums[mid] >= target, record mid as the answer and move right to mid - 1; otherwise move left to mid + 1. Return the answer.",
                    ],
                    "questions": [
                        "Why is len(nums) the right starting value for the answer?",
                        "How would you change it to find the last element that is at most target?",
                    ],
                },
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "dsa-linked-lists",
            "title": "Linked Lists",
            "summary": "Build a list out of nodes that point to each other, and rewire it.",
            "lesson": [
                {
                    "heading": "Nodes and links",
                    "text": "A Python list keeps its items side by side in memory. A linked list instead keeps each value in its own small object, a node, which also holds a reference to the next node. The list object itself only remembers the first node, called the head. The last node's `next` is `None`.",
                    "code": "class Node:\n    def __init__(self, value):\n        self.value = value\n        self.next = None\n\n# head -> [1] -> [2] -> [3] -> None",
                },
                {
                    "heading": "Walking a linked list",
                    "text": "There are no indexes. To reach anything you start at the head and follow `next` until you run out of nodes. This loop is the heart of almost every linked list method.",
                    "code": "current = self.head\nwhile current is not None:\n    # use current.value\n    current = current.next",
                },
                {
                    "heading": "Why bother?",
                    "text": "Adding at the front of a linked list is O(1): make a node, point it at the old head, and call it the new head. Nothing has to shift, unlike inserting at the front of a Python list. The cost is that reaching the k-th item takes O(k) steps.",
                },
                {
                    "heading": "Common mistakes",
                    "text": "The empty list: when `head` is `None` there is no node to call `.next` on, so most methods need to handle that case first.\n\nLosing the rest of the list: the moment you overwrite a node's `next`, the node it used to point to is unreachable unless you saved it in a variable beforehand. Draw the boxes and arrows on paper and change one arrow at a time.",
                },
            ],
            "problems": [
                {
                    "id": "linked-list-basics",
                    "title": "Linked List",
                    "difficulty": "medium",
                    "description": "Complete the LinkedList class (Node is given). append(value) adds a node at the end, prepend(value) adds a node at the front, to_list() returns the values as an ordinary Python list from head to tail, and len(linked_list) gives the number of nodes. Store the values in Node objects linked through next - do not keep them in a Python list.",
                    "starter": LINKED_LIST_STARTER,
                    "requires": ["Node", "LinkedList"],
                    "compare": "exact",
                    "tests": [
                        {"setup": "ll = LinkedList()\nll.append(1)\nll.append(2)\nll.append(3)", "check": "ll.to_list()", "expected": [1, 2, 3]},
                        {"setup": "ll = LinkedList()\nll.prepend(1)\nll.prepend(2)", "check": "ll.to_list()", "expected": [2, 1]},
                        {"check": "LinkedList().to_list()", "expected": []},
                        {"check": "len(LinkedList())", "expected": 0},
                        {"setup": "ll = LinkedList()\nll.append(2)\nll.prepend(1)\nll.append(3)", "check": "ll.to_list()", "expected": [1, 2, 3]},
                        {"setup": "ll = LinkedList()\nll.append('a')\nll.append('b')\nll.prepend('c')", "check": "len(ll)", "expected": 3},
                        {"setup": "ll = LinkedList()\nll.append(5)\nll.prepend(4)", "check": "[ll.head.value, ll.head.next.value, ll.head.next.next]", "expected": [4, 5, None]},
                    ],
                    "hints": [
                        "Three of the four methods are the same walk from the head, doing something different along the way. prepend is the odd one out: it needs no walk at all.",
                        "prepend: the new node's next should be the current head, and then the new node becomes the head. to_list and __len__: walk from the head, collecting or counting. append: walk to the last node and hang the new node off it.",
                        "For append, the last node is the one whose next is None, so walk while current.next is not None. An empty list has no last node - in that case the new node simply becomes the head.",
                        "Structure for append: make the node; if self.head is None, set head to it and return; otherwise start current at head, advance while current.next is not None, then set current.next to the node. to_list: empty list, walk while current is not None appending current.value. __len__: the same walk with a counter.",
                    ],
                    "questions": [
                        "What is the complexity of prepend, and of append?",
                        "How could LinkedList make append O(1) as well?",
                    ],
                },
                {
                    "id": "reverse-linked-list",
                    "title": "Reverse a Linked List",
                    "difficulty": "medium",
                    "description": "Add a reverse() method to LinkedList that reverses the list in place by changing where the nodes' next references point. Afterwards head must be the node that used to be last. Do not create new nodes and do not copy the values into a Python list.",
                    "starter": REVERSE_LINKED_LIST_STARTER,
                    "requires": ["Node", "LinkedList"],
                    "compare": "exact",
                    "tests": [
                        {"setup": "ll = LinkedList()\nfor v in [1, 2, 3]:\n    ll.append(v)\nll.reverse()", "check": "ll.to_list()", "expected": [3, 2, 1]},
                        {"setup": "ll = LinkedList()\nfor v in [1, 2]:\n    ll.append(v)\nll.reverse()", "check": "ll.to_list()", "expected": [2, 1]},
                        {"setup": "ll = LinkedList()\nll.reverse()", "check": "ll.to_list()", "expected": []},
                        {"setup": "ll = LinkedList()\nll.append(7)\nll.reverse()", "check": "ll.to_list()", "expected": [7]},
                        {"setup": "ll = LinkedList()\nfor v in [1, 2, 3]:\n    ll.append(v)\nll.reverse()", "check": "ll.head.value", "expected": 3},
                        {"setup": "ll = LinkedList()\nfor v in [1, 2, 3]:\n    ll.append(v)\nll.reverse()\nll.append(0)", "check": "ll.to_list()", "expected": [3, 2, 1, 0]},
                        {"setup": "ll = LinkedList()\nfor v in [1, 2, 3, 4]:\n    ll.append(v)\nll.reverse()\nll.reverse()", "check": "ll.to_list()", "expected": [1, 2, 3, 4]},
                    ],
                    "hints": [
                        "Draw 1 -> 2 -> 3 -> None and then the result, 3 -> 2 -> 1 -> None. The nodes stay where they are; every arrow simply turns around.",
                        "Walk the list once, and at each node point its next at the node behind it instead of the node ahead. To do that you must remember the node behind you.",
                        "As soon as you repoint current.next you lose the way forward - so save the old next in a variable first. You need three names: previous, current, and the saved next.",
                        "Structure: previous = None and current = self.head; while current is not None: save current.next; set current.next to previous; move previous to current; move current to the saved node. When the loop ends, previous is the new head - store it in self.head.",
                    ],
                    "questions": [
                        "Why does the old head end up pointing at None without any special case?",
                        "How much extra memory does your reverse use?",
                    ],
                },
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "dsa-dynamic-programming",
            "title": "From Recursion to Dynamic Programming",
            "summary": "Solve a big problem by combining answers to smaller versions of itself - without recomputing them.",
            "lesson": [
                {
                    "heading": "Overlapping subproblems",
                    "text": "Some recursive solutions ask the same question again and again. The classic example is Fibonacci: computing fib(30) naively makes over a million calls, because fib(28) is computed twice, fib(27) three times, and so on.",
                    "code": "def fib(n):\n    if n < 2:\n        return n\n    return fib(n - 1) + fib(n - 2)     # recomputes the same values",
                },
                {
                    "heading": "Remember the answers",
                    "text": "Dynamic programming (DP) is one idea: solve each subproblem once and reuse the result. The simplest way is bottom-up - start from the smallest cases and build upwards, so every answer you need is already known.",
                    "code": "def fib(n):\n    if n < 2:\n        return n\n    previous, current = 0, 1\n    for _ in range(2, n + 1):\n        previous, current = current, previous + current\n    return current",
                },
                {
                    "heading": "Finding the recurrence",
                    "text": "The hard part of DP is not the code but the question: 'if I already knew the answers for smaller inputs, how would I get the answer for this one?' That relationship is called the recurrence. Work out the first few answers by hand and look for it.",
                },
                {
                    "heading": "You often need only the last few answers",
                    "text": "If each answer depends only on the previous one or two, you do not need a whole table - a couple of variables is enough, as in the Fibonacci example above.",
                },
            ],
            "problems": [
                CLASSIC["climbing-stairs"],
                CLASSIC["max-subarray"],
            ],
        },
    ],
}
