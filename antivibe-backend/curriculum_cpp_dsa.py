"""C++ track 3: Data Structures & Algorithms in C++."""
from languages import CPP_HEADER
from porting import fn, port

NODE = """struct Node {
    int value;
    Node* next;
    Node(int v) : value(v), next(nullptr) {}
};
"""

GIVEN_APPEND_AND_TO_LIST = """    // append and to_list are given - read them first
    void append(int value) {
        Node* node = new Node(value);
        if (head == nullptr) {
            head = node;
            return;
        }
        Node* current = head;
        while (current->next != nullptr) {
            current = current->next;
        }
        current->next = node;
    }

    vector<int> to_list() const {
        vector<int> values;
        for (Node* current = head; current != nullptr; current = current->next) {
            values.push_back(current->value);
        }
        return values;
    }
"""


def linked_list_starter(methods):
    return (CPP_HEADER + "\n" + NODE + "\nclass LinkedList {\npublic:\n    Node* head = nullptr;\n\n"
            + methods.strip("\n") + "\n};\n")


TRACK = {
    "id": "cpp-dsa",
    "title": "Data Structures & Algorithms in C++",
    "description": "The classic structures and techniques, with the C++ standard library and pointers.",
    "milestones": [
        # ------------------------------------------------------------------
        {
            "id": "cpp-dsa-hashing",
            "title": "Complexity, Arrays & Hashing",
            "summary": "Measure how fast a solution is, and use unordered_set and unordered_map to avoid repeated scanning.",
            "lesson": [
                {
                    "heading": "Correct is not enough",
                    "text": "From here on, most problems have an obvious solution that is too slow and a cleverer one that is fast. Big-O describes how the work grows with the input size n: O(1) stays the same, O(n) grows in step with n (one loop), O(n^2) is a loop inside a loop, O(log n) halves the problem each step.",
                },
                {
                    "heading": "Count the loops - including hidden ones",
                    "text": "One loop over the input is O(n); a nested loop is O(n^2). Standard library calls hide loops too: `std::find` and `std::count` scan the whole range, so calling them inside a loop is O(n^2).",
                    "code": "for (int a : nums) {                 // n times\n    if (count(nums.begin(), nums.end(), a) > 1) {   // n more each time\n        return true;\n    }\n}",
                },
                {
                    "heading": "Trading memory for speed",
                    "text": "`unordered_set` and `unordered_map` answer 'have I seen this?' and 'what did I store for this key?' in O(1) on average. Remembering what you have seen usually replaces an inner loop and turns O(n^2) into O(n), at the price of O(n) extra memory.",
                    "code": "unordered_set<int> seen;\nfor (int n : nums) {\n    if (seen.count(n)) {\n        // seen before - found in O(1)\n    }\n    seen.insert(n);\n}",
                },
                {
                    "heading": "How to approach each problem",
                    "text": "1. Solve a small example by hand. 2. Describe the brute force solution and its complexity. 3. Ask what work is repeated, and what you could remember to avoid it.",
                },
            ],
            "quiz": [
                {
                    "question": "What is `count` at the end, and what would it be if both loops ran to 200?",
                    "code": "int count = 0;\nfor (int a = 0; a < 100; a++) {\n    for (int b = 0; b < 100; b++) {\n        count++;\n    }\n}",
                    "answer": "`10000`, and `40000` for 200: doubling the input quadrupled the work - O(n^2).",
                },
                {
                    "question": "What is the time complexity?",
                    "code": "bool has_repeat(const vector<int>& nums) {\n    for (int n : nums) {\n        if (count(nums.begin(), nums.end(), n) > 1) return true;\n    }\n    return false;\n}",
                    "answer": "O(n^2): std::count scans the whole vector for every n - a hidden inner loop.",
                },
            ],
            "problems": [
                port(
                    "has-pair-sum",
                    signature=fn("has_pair_sum", "bool", nums="array[int]", target="int"),
                    description="Return true if two numbers at different positions in nums add up to target, and false otherwise. First think of the brute-force solution and its complexity - then aim for O(n).",
                    hints=[
                        "Brute force tries every pair with a loop inside a loop: O(n^2). What is the repeated work?",
                        "For each number n, the question is 'have I already seen target - n?'. An unordered_set answers that in O(1).",
                        "Check for the partner before inserting the current number, so a single 5 cannot pair with itself for target 10.",
                        "Structure: unordered_set<int> seen; for (int n : nums) { if (seen.count(target - n)) return true; seen.insert(n); } return false;",
                    ],
                ),
                port(
                    "two-sum",
                    signature=fn("two_sum", "array[int]", nums="array[int]", target="int"),
                    description="Given a vector of integers nums and an integer target, return the indices of the two numbers that add up to target, as a vector of two ints. Each input has exactly one solution, and you may not use the same element twice. The order of the two indices does not matter.",
                    hints=[
                        "For each number, you know exactly which partner it needs: target - nums[i].",
                        "Pair With Sum only needed to know whether the partner was seen. Now you need where it was seen.",
                        "An unordered_map<int, int> from value to index remembers both. Look the partner up before storing the current number.",
                        "Structure: unordered_map<int, int> index_of; for (int i = 0; i < (int)nums.size(); i++) { int need = target - nums[i]; if (index_of.count(need)) return {index_of[need], i}; index_of[nums[i]] = i; } return {};",
                    ],
                ),
                port(
                    "missing-number",
                    signature=fn("missing_number", "int", nums="array[int]"),
                    description="nums contains n different numbers taken from the range 0 to n, so exactly one number of that range is missing. Return it.",
                    hints=[
                        "If nums has n numbers, the full range 0..n has n + 1 candidates, and one is absent.",
                        "Brute force asks 'is it there?' by scanning for each candidate. What makes that question O(1)?",
                        "Put the numbers in an unordered_set and test the candidates 0..n. (Or use arithmetic: the sum of 0..n minus the sum of nums.)",
                        "Structure: unordered_set<int> present(nums.begin(), nums.end()); for (int c = 0; c <= (int)nums.size(); c++) if (!present.count(c)) return c; return -1;",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-dsa-two-pointers",
            "title": "Two Pointers",
            "summary": "Walk through data with two indexes instead of a nested loop.",
            "lesson": [
                {
                    "heading": "The idea",
                    "text": "A 'pointer' here is just an index variable. Many problems that seem to need a loop inside a loop can be solved with two indexes that only move forward (or towards each other), which is O(n).",
                },
                {
                    "heading": "One index per sequence",
                    "text": "With two sequences, keep a position in each. Compare the two current items, act, and advance one index (or both). When the loop ends because one sequence ran out, deal with what is left of the other.",
                    "code": "size_t i = 0, j = 0;\nwhile (i < a.size() && j < b.size()) {\n    // compare a[i] and b[j], then move i or j\n}",
                },
                {
                    "heading": "From both ends",
                    "text": "On one sequence, start one index at each end and move them towards each other until they meet. Use `int` for the right index (or check for empty input first): with `size_t`, `size() - 1` on an empty vector is a huge number.",
                    "code": "int left = 0;\nint right = (int)nums.size() - 1;\nwhile (left < right) {\n    // ...\n    left++;\n    right--;\n}",
                },
            ],
            "quiz": [
                {
                    "question": "What is `steps` at the end?",
                    "code": "vector<int> nums = {1, 3, 4, 6};\nint left = 0, right = 3;\nvector<int> steps;\nwhile (left < right) {\n    int total = nums[left] + nums[right];\n    steps.push_back(total);\n    if (total == 9) break;\n    if (total < 9) left++; else right--;\n}",
                    "answer": "`{7, 9}`. 1 + 6 is too small, so left moves to 3; 3 + 6 is 9.",
                },
                {
                    "question": "Merging {1, 5} and {2, 3, 4}: which items are still unplaced when the main loop ends?",
                    "answer": "Just `5`. The second vector ran out after 4, so the rest of the first must be added after the loop.",
                },
            ],
            "problems": [
                port(
                    "pair-sum-sorted",
                    signature=fn("pair_sum_sorted", "bool", nums="array[int]", target="int"),
                    description="nums is sorted in ascending order. Return true if two numbers at different positions add up to target. Use two pointers - no set or map - for O(n) time and O(1) extra memory.",
                    hints=[
                        "Start with the smallest and the largest number. If their sum is too small, which one can never be part of an answer?",
                        "Put one index at each end and let the sorted order tell you which to move after each comparison.",
                        "Sum too small: move left forward. Too big: move right back. When they meet, there is no pair.",
                        "Structure: int left = 0, right = (int)nums.size() - 1; while (left < right) { int s = nums[left] + nums[right]; if (s == target) return true; if (s < target) left++; else right--; } return false;",
                    ],
                ),
                port(
                    "merge-sorted-lists",
                    signature=fn("merge_sorted", "list[int]", a="array[int]", b="array[int]"),
                    description="a and b are each sorted in ascending order. Return one vector containing all their numbers in ascending order. Do not just concatenate and sort - merge them in one pass.",
                    hints=[
                        "The smallest number overall is either a[0] or b[0]. After you take it, the same question repeats.",
                        "Keep an index into each vector, and always take the smaller of the two current numbers.",
                        "When one vector runs out, everything left in the other is already sorted and bigger - copy it over.",
                        "Structure: vector<int> result; size_t i = 0, j = 0; while (i < a.size() && j < b.size()) push the smaller of a[i] and b[j] and advance that index; then push the rest of a, then the rest of b; return result;",
                    ],
                ),
                port(
                    "is-subsequence",
                    signature=fn("is_subsequence", "bool", s="str", t="str"),
                    description="Return true if s is a subsequence of t: you can get s by deleting zero or more characters of t without changing the order of the rest.",
                    hints=[
                        "Read t from left to right while keeping a finger on the next character of s you still need.",
                        "One index into s, one into t. The t index always moves; when does the s index move?",
                        "Advance the s index only when the two current characters match. If it reaches the end of s, all of s was found in order.",
                        "Structure: size_t i = 0, j = 0; while (i < s.size() && j < t.size()) { if (s[i] == t[j]) i++; j++; } return i == s.size();",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-dsa-stack",
            "title": "Stacks in Action",
            "summary": "Use std::stack (or a vector) to match, cancel and evaluate.",
            "lesson": [
                {
                    "heading": "std::stack",
                    "text": "`stack<char> st;` has `push`, `top` (look), `pop` (remove - returns nothing) and `empty`. A vector works just as well with push_back/back/pop_back. Remember: `top()` or `pop()` on an empty stack is undefined behaviour, so check `empty()` first.",
                    "code": "stack<char> st;\nst.push('(');\nchar open = st.top();   // '('\nst.pop();\nbool done = st.empty();   // true",
                },
                {
                    "heading": "The usual shape",
                    "text": "Loop over the input once. For each item, either push it for later or pop earlier items and combine them with it. Each item is pushed and popped at most once: O(n).",
                },
                {
                    "heading": "Strings to numbers",
                    "text": "`stoi(token)` turns text like \"-3\" into an int. To tell an operator from a number, compare the whole token: `token == \"+\"`.",
                },
            ],
            "quiz": [
                {
                    "question": "What is the stack at the end, as a string from bottom to top?",
                    "code": "string st;\nfor (char ch : string(\"abba\")) {\n    if (!st.empty() && st.back() == ch) st.pop_back();\n    else st.push_back(ch);\n}",
                    "answer": "Empty. a is pushed, b is pushed, the second b cancels the first, and the last a cancels the first a. (A string works as a stack of chars.)",
                },
                {
                    "question": "Checking \"([)]\": what is on the stack when the first closing bracket arrives, and what is the answer?",
                    "answer": "`(` and `[` with `[` on top. The closer is `)`, which does not match `[`, so the answer is false.",
                },
            ],
            "problems": [
                port(
                    "valid-parentheses",
                    signature=fn("is_valid", "bool", s="str"),
                    description="s contains only the characters ( ) [ ] { }. Return true if every bracket is closed by the same kind of bracket, in the right order.",
                    hints=[
                        "The most recently opened bracket must be the first one closed.",
                        "Push every opening bracket. Each closing bracket must match the one on top, which you then pop.",
                        "A closer with an empty stack is invalid, and so is anything left open at the end. A small helper that maps ')' to '(' etc. keeps the comparison tidy.",
                        "Structure: stack<char> st; for (char c : s) { if c is an opener, push it; else { if (st.empty() || st.top() != opener_for(c)) return false; st.pop(); } } return st.empty();",
                    ],
                ),
                port(
                    "remove-adjacent-duplicates",
                    signature=fn("remove_adjacent_duplicates", "str", s="str"),
                    hints=[
                        "Removing one pair can make two new letters neighbours. One pass works if you keep the right thing around.",
                        "Keep the surviving letters on a stack. A new letter only needs comparing with the most recent survivor.",
                        "A string itself works as a stack: push_back, back, pop_back. If the top equals the new letter, pop; otherwise push.",
                        "Structure: string st; for (char c : s) { if (!st.empty() && st.back() == c) st.pop_back(); else st.push_back(c); } return st;",
                    ],
                ),
                port(
                    "evaluate-rpn",
                    signature=fn("evaluate_rpn", "int", tokens="array[str]"),
                    description="tokens is a vector of strings forming an expression in Reverse Polish Notation, where each operator comes after its two operands: {\"2\", \"1\", \"+\"} means 2 + 1. Each token is a whole number or one of \"+\", \"-\", \"*\". Return the value. For \"-\", the operand that appeared first is subtracted from.",
                    hints=[
                        "Work through {\"2\", \"1\", \"+\", \"3\", \"*\"} by hand. Which numbers does each operator apply to?",
                        "An operator applies to the two most recent unused values, and its result becomes a value itself: a stack.",
                        "Push stoi(token) for numbers. For an operator pop twice - the first pop is the right operand, the second the left - and push the result.",
                        "Structure: stack<int> st; for each token: if it is \"+\", \"-\" or \"*\": int right = st.top(); st.pop(); int left = st.top(); st.pop(); push the result; else push stoi(token). Return st.top();",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-dsa-binary-search",
            "title": "Binary Search",
            "summary": "Find things in sorted data by halving - and avoid integer overflow while you do.",
            "lesson": [
                {
                    "heading": "Halving",
                    "text": "On sorted data, look at the middle element and discard the half that cannot contain the answer. A million items need about 20 steps: O(log n).",
                    "code": "int left = 0, right = (int)nums.size() - 1;\nwhile (left <= right) {\n    int mid = left + (right - left) / 2;\n    if (nums[mid] == target) return mid;\n    if (nums[mid] < target) left = mid + 1;\n    else right = mid - 1;\n}",
                },
                {
                    "heading": "Overflow",
                    "text": "`(left + right) / 2` can overflow when left and right are both large, because their sum no longer fits in an int. `left + (right - left) / 2` gives the same middle without the large sum. The same danger appears whenever you square a number: `mid * mid` needs `long long` long before mid itself is big.",
                },
                {
                    "heading": "Boundaries, not just matches",
                    "text": "The same halving answers 'where is the first element that is at least x?' or 'what is the largest r with r * r <= n?'. Keep a best-so-far answer and keep narrowing until the range is empty.",
                },
                {
                    "heading": "The standard library",
                    "text": "`std::lower_bound` and `std::binary_search` exist - write your own here so you understand them.",
                },
            ],
            "quiz": [
                {
                    "question": "Searching for 9 in {1, 3, 5, 7, 9, 11}: which indexes does binary search look at?",
                    "answer": "2, then 4. left = 0, right = 5, mid = 2 (5 is too small, left = 3); mid = 3 + (5 - 3) / 2 = 4, which holds 9.",
                },
                {
                    "question": "What is wrong with this line when mid is 50000?",
                    "code": "int mid = 50000;\nint square = mid * mid;",
                    "answer": "50000 * 50000 = 2.5 billion, which does not fit in an int (the maximum is about 2.1 billion). The result overflows. Use `long long square = (long long)mid * mid;`.",
                },
            ],
            "problems": [
                port(
                    "binary-search",
                    signature=fn("binary_search", "int", nums="array[int]", target="int"),
                    description="nums is sorted in ascending order with no duplicates. Return the index of target, or -1 if it is not there. Your solution must be O(log n).",
                    hints=[
                        "Look at the middle element. If it is not the target, which half can you throw away?",
                        "Keep left and right indexes for the part that might still hold the target, and narrow them.",
                        "mid = left + (right - left) / 2. Move left to mid + 1 or right to mid - 1 - never to mid itself, or the range can stop shrinking.",
                        "Structure: int left = 0, right = (int)nums.size() - 1; while (left <= right) { compute mid; if equal return mid; if smaller left = mid + 1; else right = mid - 1; } return -1;",
                    ],
                ),
                port(
                    "sqrt-floor",
                    signature=fn("sqrt_floor", "long", n="long"),
                    description="Return the largest whole number r with r * r <= n, for a whole number n of 0 or more. Use binary search over the possible answers - not sqrt() or a loop that tries every number. Watch out: r * r can overflow an int.",
                    hints=[
                        "The possible answers 0..n are sorted, and for each you can ask 'is r * r too big?'. That is enough for binary search.",
                        "Search 0..n. If mid * mid <= n, mid could be the answer: remember it and search right. Otherwise search left.",
                        "Everything here is long long, so mid * mid does not overflow for the test values. (In general, compare mid <= n / mid to avoid even that.)",
                        "Structure: long long left = 0, right = n, answer = 0; while (left <= right) { long long mid = left + (right - left) / 2; if (mid * mid <= n) { answer = mid; left = mid + 1; } else right = mid - 1; } return answer;",
                    ],
                ),
                port(
                    "first-at-least",
                    signature=fn("first_at_least", "int", nums="array[int]", target="int"),
                    description="nums is sorted in ascending order and may contain repeated values. Return the index of the first element that is greater than or equal to target, or nums.size() if every element is smaller. Aim for O(log n).",
                    hints=[
                        "All the 'too small' elements come before all the 'big enough' ones. You are looking for the boundary.",
                        "Do not stop when you see the target - an equal element further left might exist. Keep narrowing.",
                        "If nums[mid] >= target, mid might be the answer: remember it and search left. Otherwise search right.",
                        "Structure: int left = 0, right = (int)nums.size() - 1, answer = nums.size(); while (left <= right) { mid; if (nums[mid] >= target) { answer = mid; right = mid - 1; } else left = mid + 1; } return answer;",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-dsa-linked-lists",
            "title": "Linked Lists & Pointers",
            "summary": "Build a list from nodes connected by pointers, and rewire it.",
            "lesson": [
                {
                    "heading": "Pointers",
                    "text": "A pointer holds the address of an object. `Node* p` is 'a pointer to a Node'. `new Node(5)` creates a Node that lives until it is deleted, and gives you a pointer to it. `nullptr` is the pointer to nothing. `p->value` reads a member through a pointer (it means `(*p).value`).",
                    "code": "Node* first = new Node(1);\nfirst->next = new Node(2);\nint second = first->next->value;     // 2\nbool end = first->next->next == nullptr;   // true",
                },
                {
                    "heading": "Nodes and links",
                    "text": "Each node holds a value and a pointer to the next node. The list itself only remembers the first node, `head`. The last node's `next` is `nullptr`.",
                    "code": "struct Node {\n    int value;\n    Node* next;\n    Node(int v) : value(v), next(nullptr) {}\n};\n// head -> [1] -> [2] -> [3] -> nullptr",
                },
                {
                    "heading": "Walking the list",
                    "text": "Start at head and follow next until you reach nullptr.",
                    "code": "for (Node* current = head; current != nullptr; current = current->next) {\n    // current->value\n}",
                },
                {
                    "heading": "Crashes instead of errors",
                    "text": "Reading `->` through `nullptr` crashes the program - Antivibe reports it as a memory access violation. Most linked list bugs are exactly this: handle the empty list (head == nullptr) before anything else, and save `current->next` before you change it, or the rest of the list is lost.",
                },
                {
                    "heading": "Memory",
                    "text": "Every `new` should eventually be matched by a `delete`, or the memory leaks until the program ends. In these short exercises leaks do no harm; real code would free the nodes in the list's destructor.",
                },
            ],
            "quiz": [
                {
                    "question": "What is `a->next->next->value`?",
                    "code": "Node* a = new Node(1);\na->next = new Node(2);\na->next->next = new Node(3);",
                    "answer": "`3`.",
                },
                {
                    "question": "What is wrong with this walk?",
                    "code": "Node* current = head;\nwhile (current->next != nullptr) {\n    values.push_back(current->value);\n    current = current->next;\n}",
                    "answer": "It skips the last node's value, and on an empty list `head->next` crashes because head is nullptr. Loop `while (current != nullptr)`.",
                },
            ],
            "problems": [
                port(
                    "linked-list-search",
                    description="append and to_list are written for you. Add two member functions that walk the nodes: contains(value) returns true if any node holds value, and last() returns the value of the last node - throwing out_of_range if the list is empty. Walk the nodes - do not call to_list.",
                    starter=linked_list_starter(GIVEN_APPEND_AND_TO_LIST + """
    bool contains(int value) const {
        return false;
    }

    int last() const {
        return 0;
    }
"""),
                    tests=[
                        {"setup": "LinkedList ll;\nfor (int v : {4, 8, 15}) ll.append(v);", "check": "vector<bool>{ll.contains(8), ll.contains(5)}", "expected": [True, False]},
                        {"setup": "LinkedList ll;\nfor (int v : {4, 8, 15}) ll.append(v);", "check": "ll.last()", "expected": 15},
                        {"edge": "empty list", "check": "LinkedList().contains(1)", "expected": False},
                        {"edge": "empty list", "setup": "LinkedList ll;", "check": "ll.last()", "raises": "out_of_range"},
                        {"edge": "single node", "setup": "LinkedList ll;\nll.append(7);", "check": "vector<int>{ll.contains(7), ll.last()}", "expected": [1, 7]},
                        {"setup": "LinkedList ll;\nfor (int v : {1, 2, 3}) ll.append(v);", "check": "ll.contains(3)", "expected": True},
                    ],
                    hints=[
                        "Both functions are the walk from the lesson. to_list in the starter shows it working.",
                        "contains is a search: return true the moment a node holds the value, false when the walk ends. last must stop on the final node instead of walking past it.",
                        "The final node is the one whose next is nullptr (append finds it the same way). Check head == nullptr first, because nullptr has no ->next.",
                        "Structure: contains: for (Node* c = head; c != nullptr; c = c->next) if (c->value == value) return true; return false. last: if (head == nullptr) throw out_of_range(\"empty list\"); Node* c = head; while (c->next != nullptr) c = c->next; return c->value;",
                    ],
                    questions=[
                        "Why do the two walks use different loop conditions?",
                        "What does the program do if last() forgets the empty-list check?",
                    ],
                ),
                port(
                    "linked-list-basics",
                    description="Complete the LinkedList class (Node is given). append(value) adds a node at the end, prepend(value) adds one at the front, to_list() returns the values from head to tail, and size() counts the nodes. Store the values in Node objects linked by next - not in a vector.",
                    starter=linked_list_starter("""
    void append(int value) {
    }

    void prepend(int value) {
    }

    vector<int> to_list() const {
        return {};
    }

    int size() const {
        return 0;
    }
"""),
                    tests=[
                        {"setup": "LinkedList ll;\nll.append(1);\nll.append(2);\nll.append(3);", "check": "ll.to_list()", "expected": [1, 2, 3]},
                        {"setup": "LinkedList ll;\nll.prepend(1);\nll.prepend(2);", "check": "ll.to_list()", "expected": [2, 1]},
                        {"edge": "empty list", "check": "LinkedList().to_list()", "expected": []},
                        {"edge": "empty list", "check": "LinkedList().size()", "expected": 0},
                        {"setup": "LinkedList ll;\nll.append(2);\nll.prepend(1);\nll.append(3);", "check": "ll.to_list()", "expected": [1, 2, 3]},
                        {"setup": "LinkedList ll;\nll.append(5);\nll.append(6);\nll.prepend(7);", "check": "ll.size()", "expected": 3},
                        {"edge": "links between nodes", "setup": "LinkedList ll;\nll.append(5);\nll.prepend(4);", "check": "vector<int>{ll.head->value, ll.head->next->value, ll.head->next->next == nullptr}", "expected": [4, 5, 1]},
                    ],
                    hints=[
                        "to_list and size are the same walk doing different work. prepend needs no walk. append walks to the last node.",
                        "prepend: the new node's next is the current head, then the new node becomes head. append: walk to the node whose next is nullptr and hang the new node there.",
                        "An empty list has no last node: in append, if head is nullptr, the new node simply becomes head.",
                        "Structure: append: Node* node = new Node(value); if (!head) { head = node; return; } walk while current->next; current->next = node. prepend: Node* node = new Node(value); node->next = head; head = node. to_list/size: walk from head.",
                    ],
                ),
                port(
                    "reverse-linked-list",
                    description="Add a reverse() member function that reverses the list in place by changing where the nodes' next pointers point. Afterwards head must be the node that used to be last. Do not create new nodes and do not copy the values into a vector.",
                    starter=linked_list_starter(GIVEN_APPEND_AND_TO_LIST + """
    void reverse() {
    }
"""),
                    tests=[
                        {"setup": "LinkedList ll;\nfor (int v : {1, 2, 3}) ll.append(v);\nll.reverse();", "check": "ll.to_list()", "expected": [3, 2, 1]},
                        {"setup": "LinkedList ll;\nll.append(1);\nll.append(2);\nll.reverse();", "check": "ll.to_list()", "expected": [2, 1]},
                        {"edge": "empty list", "setup": "LinkedList ll;\nll.reverse();", "check": "ll.to_list()", "expected": []},
                        {"edge": "single node", "setup": "LinkedList ll;\nll.append(7);\nll.reverse();", "check": "ll.to_list()", "expected": [7]},
                        {"setup": "LinkedList ll;\nfor (int v : {1, 2, 3}) ll.append(v);\nll.reverse();", "check": "ll.head->value", "expected": 3},
                        {"edge": "list still usable after reversing", "setup": "LinkedList ll;\nfor (int v : {1, 2, 3}) ll.append(v);\nll.reverse();\nll.append(0);", "check": "ll.to_list()", "expected": [3, 2, 1, 0]},
                        {"setup": "LinkedList ll;\nfor (int v : {1, 2, 3, 4}) ll.append(v);\nll.reverse();\nll.reverse();", "check": "ll.to_list()", "expected": [1, 2, 3, 4]},
                    ],
                    hints=[
                        "Draw 1 -> 2 -> 3 -> nullptr and 3 -> 2 -> 1 -> nullptr. The nodes stay put; every arrow turns around.",
                        "Walk the list once and point each node's next at the node behind it. You must remember the node behind you.",
                        "Changing current->next loses the way forward, so save it first. Three pointers: previous, current, and the saved next.",
                        "Structure: Node* previous = nullptr; Node* current = head; while (current != nullptr) { Node* following = current->next; current->next = previous; previous = current; current = following; } head = previous;",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-dsa-dynamic-programming",
            "title": "From Recursion to Dynamic Programming",
            "summary": "Solve each subproblem once, build answers bottom-up, and keep the numbers in range.",
            "lesson": [
                {
                    "heading": "Overlapping subproblems",
                    "text": "A naive recursive Fibonacci recomputes the same values over and over; fib(40) makes hundreds of millions of calls. Dynamic programming solves each subproblem once and reuses the answer.",
                    "code": "long long fib(int n) {\n    if (n < 2) return n;\n    return fib(n - 1) + fib(n - 2);    // exponential\n}",
                },
                {
                    "heading": "Bottom-up",
                    "text": "Start from the smallest cases and build upwards, so every answer you need is already known. If each answer needs only the previous one or two, two variables are enough.",
                    "code": "long long fib(int n) {\n    if (n < 2) return n;\n    long long previous = 0, current = 1;\n    for (int i = 2; i <= n; i++) {\n        long long next = previous + current;\n        previous = current;\n        current = next;\n    }\n    return current;\n}",
                },
                {
                    "heading": "Mind the size of the numbers",
                    "text": "These answers grow fast. fib(47) no longer fits in an int, and fib(93) not even in a long long. Use `long long` for the answer, and know where its limit is.",
                },
            ],
            "quiz": [
                {
                    "question": "What are `a` and `b` after the loop?",
                    "code": "long long a = 1, b = 2;\nfor (int i = 0; i < 3; i++) {\n    long long next = a + b;\n    a = b;\n    b = next;\n}",
                    "answer": "`a` is `5` and `b` is `8`: (1, 2) -> (2, 3) -> (3, 5) -> (5, 8).",
                },
                {
                    "question": "With the naive recursive fib, how many times is fib(2) computed while computing fib(5)?",
                    "answer": "`3` times - once inside fib(4) directly and once inside each of the two fib(3) calls.",
                },
            ],
            "problems": [
                port(
                    "fibonacci",
                    signature=fn("fib", "long", n="int"),
                    description="Return the n-th Fibonacci number: fib(0) is 0, fib(1) is 1, and each later one is the sum of the two before it. The tests go up to n = 70, so the naive recursion is far too slow - build the answer bottom-up, in a long long.",
                    hints=[
                        "Try the naive recursion and watch the n = 70 test time out. Why is it so slow?",
                        "Build upwards from fib(0) and fib(1) so each value is computed once.",
                        "Only the previous two values are needed, so two long long variables are enough. fib(70) does not fit in an int.",
                        "Structure: if (n < 2) return n; long long previous = 0, current = 1; repeat n - 1 times: next = previous + current; previous = current; current = next; return current;",
                    ],
                ),
                port(
                    "climbing-stairs",
                    signature=fn("climb_stairs", "long", n="int"),
                    hints=[
                        "To reach step n, your last move came from step n - 1 or from step n - 2.",
                        "So the number of ways to reach n is ways(n - 1) + ways(n - 2) - but computing that recursively repeats work.",
                        "Build it bottom-up like Fibonacci: ways(1) = 1, ways(2) = 2, and each later value is the sum of the two before.",
                        "Structure: if (n <= 2) return n; long long prev = 1, cur = 2; for (int i = 3; i <= n; i++) { long long next = prev + cur; prev = cur; cur = next; } return cur;",
                    ],
                ),
                port(
                    "max-subarray",
                    signature=fn("max_subarray", "int", nums="array[int]"),
                    description="Return the largest sum of a non-empty run of consecutive numbers in nums.",
                    hints=[
                        "Trying every start and end is O(n^2) or worse. Think about the best run that ends exactly at position i.",
                        "The best run ending at i either extends the best run ending at i - 1, or starts fresh at nums[i] - whichever is bigger.",
                        "Track that 'best ending here' and, separately, the best seen anywhere. Start both at nums[0], since the answer is at least one element.",
                        "Structure: int here = nums[0], best = nums[0]; for (size_t i = 1; i < nums.size(); i++) { here = max(nums[i], here + nums[i]); best = max(best, here); } return best;",
                    ],
                ),
            ],
        },
    ],
}

# Binary search trees come between linked lists and dynamic programming
from curriculum_bst import CPP_MILESTONE  # noqa: E402

TRACK["milestones"].insert(
    next(i for i, m in enumerate(TRACK["milestones"]) if m["id"] == "cpp-dsa-dynamic-programming"),
    CPP_MILESTONE,
)
