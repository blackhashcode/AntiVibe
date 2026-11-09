"""The Binary Search Trees milestone, for the Python and C++ DSA tracks."""
from languages import CPP_HEADER

# =============================================================================
# Python
# =============================================================================

PY_TREE_NODE = '''class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
'''

PY_GIVEN_INSERT = '''    # insert is given - read it first
    def insert(self, value):
        if self.root is None:
            self.root = TreeNode(value)
            return
        node = self.root
        while True:
            if value == node.value:
                return
            if value < node.value:
                if node.left is None:
                    node.left = TreeNode(value)
                    return
                node = node.left
            else:
                if node.right is None:
                    node.right = TreeNode(value)
                    return
                node = node.right
'''

PY_GIVEN_IN_ORDER = '''
    def in_order(self):
        result = []

        def visit(node):
            if node is not None:
                visit(node.left)
                result.append(node.value)
                visit(node.right)

        visit(self.root)
        return result
'''


def py_bst_starter(methods, given=""):
    return f"{PY_TREE_NODE}\n\nclass BST:\n    def __init__(self):\n        self.root = None\n\n{given}{methods}"


def py_build(values):
    """Setup code that inserts values into a new BST called t."""
    return f"t = BST()\nfor v in {values!r}:\n    t.insert(v)"


PYTHON_MILESTONE = {
    "id": "dsa-trees",
    "title": "Binary Search Trees",
    "summary": "Trees of nodes with two children, kept in order so that searching halves the work at every step.",
    "lesson": [
        {
            "heading": "Trees",
            "text": "A linked list node points to one next node. A tree node can point to several children. The node at the top is the root, a node with no children is a leaf, and every node together with everything below it is a subtree. In a binary tree each node has at most two children: `left` and `right`. A missing child is `None`.",
            "code": "class TreeNode:\n    def __init__(self, value, left=None, right=None):\n        self.value = value\n        self.left = left\n        self.right = right\n\n#        5\n#       / \\\n#      3   8\n#     / \\\n#    1   4\nroot = TreeNode(5, TreeNode(3, TreeNode(1), TreeNode(4)), TreeNode(8))",
        },
        {
            "heading": "The search tree rule",
            "text": "A binary search tree (BST) keeps one rule at every node: everything in the left subtree is smaller than the node, and everything in the right subtree is bigger. Not just the two children - the whole subtrees. That rule is what makes searching fast: at each node you know which side the value must be on, so you throw the other side away, exactly like binary search.",
            "code": "def contains(node, value):\n    while node is not None:\n        if value == node.value:\n            return True\n        node = node.left if value < node.value else node.right\n    return False",
        },
        {
            "heading": "Inserting",
            "text": "To insert, search for the value. Where the search falls off the tree - at a missing child - is exactly where the new value belongs. In these exercises a value that is already in the tree is not inserted again.",
        },
        {
            "heading": "Recursion fits trees",
            "text": "A tree is made of smaller trees, so most tree functions are short recursions: answer for the empty tree (`None`), and otherwise combine the answers for the left and right subtrees with the current node. Visiting left subtree, then the node, then the right subtree is called an in-order traversal - and in a BST it produces the values in sorted order.",
            "code": "def count(node):\n    if node is None:\n        return 0\n    return count(node.left) + 1 + count(node.right)",
        },
        {
            "heading": "Height and speed",
            "text": "The height is the number of nodes on the longest path from the root down to a leaf. Search and insert take O(height) steps. A well-shaped tree with n nodes has a height of about log n, so a million values need about 20 steps. But inserting values that are already sorted builds a tree that is just a line - height n - and every operation becomes O(n). Self-balancing trees (AVL, red-black) fix that by reshaping themselves; Python's dict and C++'s std::map are built on such ideas.",
        },
        {
            "heading": "Removing a node",
            "text": "There are three cases. A leaf is simply cut off. A node with one child is replaced by that child. A node with two children keeps its place but takes the value of its in-order successor - the smallest value in its right subtree - and that successor is then removed from the right subtree instead (it has at most one child, so that is one of the easy cases).",
        },
        {
            "heading": "Common mistakes",
            "text": "Checking only a node against its own children when validating a BST. A value deep in the left subtree can be bigger than an ancestor further up while still being smaller than its parent. Every node must fit between a lower and an upper bound passed down from all its ancestors.\n\nForgetting the empty tree: `None` has no `.left`, so handle it first.",
        },
    ],
    "quiz": [
        {
            "question": "Insert 5, 3, 8, 1, 4 into an empty BST, in that order. What are the left and right children of 3?",
            "answer": "`1` (left) and `4` (right). 1 and 4 are both smaller than 5, so they go left of the root; then 1 < 3 goes left of 3 and 4 > 3 goes right.",
        },
        {
            "question": "For the tree from question 1, what does `in_order(root)` return?",
            "code": "def in_order(node):\n    if node is None:\n        return []\n    return in_order(node.left) + [node.value] + in_order(node.right)",
            "answer": "`[1, 3, 4, 5, 8]` - the values in sorted order. That is always true for a BST.",
        },
        {
            "question": "Insert 1, 2, 3, 4, 5 into an empty BST. What is its height, and how many steps does searching for 5 take?",
            "answer": "Height `5`, and 5 steps: every value went to the right, so the tree is a straight line and search is O(n). Inserting the same values in the order 3, 1, 4, 2, 5 gives height 3.",
        },
        {
            "question": "Is this a valid BST?",
            "code": "TreeNode(5, TreeNode(1), TreeNode(6, TreeNode(3), TreeNode(7)))",
            "answer": "No. 3 is in the right subtree of 5, so it would have to be bigger than 5. Each node is fine compared with its own children, which is why checking only children is not enough.",
        },
    ],
    "problems": [
        {
            "id": "bst-insert",
            "title": "Insert and Search",
            "difficulty": "easy",
            "description": "TreeNode is given. Complete the BST class: insert(value) adds a value in the right place (ignoring a value that is already in the tree), and contains(value) returns True if the value is in the tree. Use the BST rule to walk down one path - do not visit every node.",
            "starter": py_bst_starter("    def insert(self, value):\n        pass\n\n    def contains(self, value):\n        pass\n"),
            "requires": ["TreeNode", "BST"],
            "compare": "exact",
            "tests": [
                {"setup": py_build([5, 3, 8]), "check": "[t.root.value, t.root.left.value, t.root.right.value]", "expected": [5, 3, 8]},
                {"setup": py_build([5, 3, 8, 1, 4]), "check": "[t.contains(4), t.contains(7)]", "expected": [True, False]},
                {"edge": "empty tree", "check": "BST().contains(1)", "expected": False},
                {"setup": py_build([5, 3, 1]), "check": "t.root.left.left.value", "expected": 1},
                {"edge": "duplicate values", "setup": py_build([5, 5]), "check": "[t.root.left, t.root.right]", "expected": [None, None]},
                {"edge": "single node", "setup": py_build([7]), "check": "[t.contains(7), t.root.left]", "expected": [True, None]},
                {"edge": "sorted input makes a line", "setup": py_build([1, 2, 3, 4]), "check": "t.root.right.right.right.value", "expected": 4},
            ],
            "hints": [
                "Searching and inserting walk the same path: at each node the BST rule tells you whether to go left or right.",
                "contains: start at the root and keep moving to the left or right child until you find the value or run out of tree. insert: walk the same way until the child you want to move to is missing - that is where the new node goes.",
                "An empty tree is a special case for insert: the new node becomes the root. Stop when value == node.value, so duplicates are ignored.",
                "Structure: contains: node = self.root; while node is not None: if equal return True; node = node.left if value < node.value else node.right; return False. insert: if root is None, root = TreeNode(value); otherwise loop: go left or right, and when that child is None, create the node there and return.",
            ],
            "questions": [
                "Why does contains only need to look at one node per level?",
                "What shape does the tree take when the values arrive already sorted?",
            ],
        },
        {
            "id": "bst-inorder",
            "title": "In-Order Traversal",
            "difficulty": "easy",
            "description": "insert is given. Add in_order(), which returns all the values in the tree as a list in ascending order, and size(), which returns how many nodes there are. Visit the nodes recursively - do not sort.",
            "starter": py_bst_starter("\n    def in_order(self):\n        pass\n\n    def size(self):\n        pass\n", PY_GIVEN_INSERT),
            "requires": ["TreeNode", "BST"],
            "compare": "exact",
            "tests": [
                {"setup": py_build([5, 3, 8, 1, 4]), "check": "t.in_order()", "expected": [1, 3, 4, 5, 8]},
                {"setup": py_build([5, 3, 8, 1, 4]), "check": "t.size()", "expected": 5},
                {"edge": "empty tree", "check": "[BST().in_order(), BST().size()]", "expected": [[], 0]},
                {"edge": "duplicate values", "setup": py_build([2, 2, 1]), "check": "t.in_order()", "expected": [1, 2]},
                {"edge": "negative numbers", "setup": py_build([0, -5, 5, -10]), "check": "t.in_order()", "expected": [-10, -5, 0, 5]},
                {"edge": "single node", "setup": py_build([9]), "check": "[t.in_order(), t.size()]", "expected": [[9], 1]},
            ],
            "hints": [
                "Everything in the left subtree is smaller than the root and everything in the right subtree is bigger. In what order should you visit the three parts to get sorted output?",
                "Left subtree first, then the node itself, then the right subtree - and the subtrees are trees, so the same rule applies to them. That is a recursion on nodes.",
                "Write a helper that takes a node. Its base case is None (contribute nothing / count 0). in_order and size just call the helper on self.root.",
                "Structure: def walk(node): if node is None: return []; return walk(node.left) + [node.value] + walk(node.right). count(node) is 0 for None, otherwise count(left) + 1 + count(right).",
            ],
            "questions": [
                "Why does in-order traversal of a BST come out sorted?",
                "What order do you get if you visit the node before its subtrees (pre-order)?",
            ],
        },
        {
            "id": "bst-height",
            "title": "Height, Minimum and Maximum",
            "difficulty": "easy",
            "description": "insert is given. Add height() - the number of nodes on the longest path from the root down to a leaf, 0 for an empty tree - and min_value() and max_value(), which return the smallest and largest values and raise ValueError on an empty tree.",
            "starter": py_bst_starter("\n    def height(self):\n        pass\n\n    def min_value(self):\n        pass\n\n    def max_value(self):\n        pass\n", PY_GIVEN_INSERT),
            "requires": ["TreeNode", "BST"],
            "compare": "exact",
            "tests": [
                {"setup": py_build([5, 3, 8, 1]), "check": "t.height()", "expected": 3},
                {"setup": py_build([5, 3, 8, 1]), "check": "[t.min_value(), t.max_value()]", "expected": [1, 8]},
                {"edge": "empty tree", "check": "BST().height()", "expected": 0},
                {"edge": "empty tree", "check": "BST().min_value()", "raises": "ValueError"},
                {"edge": "single node", "setup": py_build([4]), "check": "[t.height(), t.min_value(), t.max_value()]", "expected": [1, 4, 4]},
                {"edge": "sorted input makes a line", "setup": py_build([1, 2, 3, 4, 5]), "check": "t.height()", "expected": 5},
                {"setup": py_build([3, 1, 4, 2, 5]), "check": "t.height()", "expected": 3},
            ],
            "hints": [
                "Where in a BST is the smallest value? Follow the rule: smaller values are always to the left.",
                "min and max need no recursion: keep going left (or right) until there is no further child. Height does need recursion: a tree is one node taller than its taller subtree.",
                "height(None) is 0. For a node it is 1 + the larger of the two subtree heights - max() picks the larger. Check for an empty tree before walking for the minimum.",
                "Structure: def h(node): return 0 if node is None else 1 + max(h(node.left), h(node.right)). min_value: if root is None raise ValueError; node = root; while node.left is not None: node = node.left; return node.value. max_value mirrors it to the right.",
            ],
            "questions": [
                "Why is a height of about log n the best a tree with n nodes can do?",
                "How do the two orders of inserting 1 to 5 in the tests give such different heights?",
            ],
        },
        {
            "id": "valid-bst",
            "title": "Debug: Is It a BST?",
            "difficulty": "medium",
            "description": "is_valid_bst(node) should return True if the tree rooted at node is a valid binary search tree: every value in a node's left subtree is smaller than it, and every value in its right subtree is bigger (no duplicates). The given version only compares each node with its own children - which looks right, but is not. Find the trees it gets wrong and fix it.",
            "starter": PY_TREE_NODE + '''

def is_valid_bst(node):
    if node is None:
        return True
    if node.left is not None and node.left.value >= node.value:
        return False
    if node.right is not None and node.right.value <= node.value:
        return False
    return is_valid_bst(node.left) and is_valid_bst(node.right)
''',
            "requires": ["TreeNode", "is_valid_bst"],
            "compare": "exact",
            "tests": [
                {"check": "is_valid_bst(TreeNode(5, TreeNode(1), TreeNode(6, TreeNode(3), TreeNode(7))))", "expected": False},
                {"check": "is_valid_bst(TreeNode(10, TreeNode(5, None, TreeNode(15)), TreeNode(20)))", "expected": False},
                {"check": "is_valid_bst(TreeNode(2, TreeNode(1), TreeNode(3)))", "expected": True},
                {"edge": "empty tree", "check": "is_valid_bst(None)", "expected": True},
                {"edge": "single node", "check": "is_valid_bst(TreeNode(1))", "expected": True},
                {"edge": "duplicate values", "check": "is_valid_bst(TreeNode(2, TreeNode(2)))", "expected": False},
                {"check": "is_valid_bst(TreeNode(5, TreeNode(3, TreeNode(1), TreeNode(4)), TreeNode(8)))", "expected": True},
            ],
            "hints": [
                "Draw the first test's tree. Every node is fine compared with its own children - so why is it not a BST?",
                "The rule is about whole subtrees: 3 sits in the right subtree of 5, so it must be bigger than 5, not just smaller than its parent 6. Each node has to respect every ancestor above it.",
                "Pass the allowed range down the recursion: a lower and an upper bound (None meaning 'no limit'). Going left, the node's value becomes the new upper bound; going right, it becomes the new lower bound.",
                "Structure: def is_valid_bst(node, low=None, high=None): if node is None return True; if low is not None and node.value <= low return False; if high is not None and node.value >= high return False; return is_valid_bst(node.left, low, node.value) and is_valid_bst(node.right, node.value, high).",
            ],
            "questions": [
                "Why did the tests where the tree is a valid BST pass even with the bug?",
                "How could an in-order traversal check the same thing?",
            ],
        },
        {
            "id": "bst-remove",
            "title": "Remove a Value",
            "difficulty": "medium",
            "description": "insert and in_order are given. Add remove(value), which takes a value out of the tree and keeps it a valid BST. Removing a value that is not there does nothing. When the node has two children, replace its value with the smallest value in its right subtree and remove that value from the right subtree instead.",
            "starter": py_bst_starter("\n    def remove(self, value):\n        pass\n", PY_GIVEN_INSERT + PY_GIVEN_IN_ORDER),
            "requires": ["TreeNode", "BST"],
            "compare": "exact",
            "tests": [
                {"setup": py_build([5, 3, 8, 1, 4, 7, 9]) + "\nt.remove(1)", "check": "t.in_order()", "expected": [3, 4, 5, 7, 8, 9]},
                {"setup": py_build([5, 3, 8, 1, 4, 7, 9]) + "\nt.remove(5)", "check": "[t.in_order(), t.root.value]", "expected": [[1, 3, 4, 7, 8, 9], 7]},
                {"setup": py_build([5, 3, 8, 1, 4, 7, 9]) + "\nt.remove(3)", "check": "t.in_order()", "expected": [1, 4, 5, 7, 8, 9]},
                {"edge": "node with one child", "setup": py_build([5, 3, 1]) + "\nt.remove(3)", "check": "[t.in_order(), t.root.left.value]", "expected": [[1, 5], 1]},
                {"edge": "value not in the tree", "setup": py_build([5, 3, 8]) + "\nt.remove(42)", "check": "t.in_order()", "expected": [3, 5, 8]},
                {"edge": "empty tree", "setup": "t = BST()\nt.remove(1)", "check": "t.in_order()", "expected": []},
                {"edge": "single node", "setup": py_build([7]) + "\nt.remove(7)", "check": "t.root", "expected": None},
            ],
            "hints": [
                "First find the node, as in contains. Then the work depends on how many children it has: none, one, or two.",
                "No children: the node simply disappears. One child: the child takes the node's place. Two children: keep the node, give it the smallest value of its right subtree, then remove that value from the right subtree.",
                "A recursive helper that returns the new root of a subtree makes the re-linking easy: node.left = remove_from(node.left, value). Returning None removes a leaf; returning the only child replaces a one-child node.",
                "Structure: def remove_from(node, value): if node is None return None; if value < node.value: node.left = remove_from(node.left, value); elif value > node.value: node.right = remove_from(node.right, value); else: if node.left is None return node.right; if node.right is None return node.left; find the minimum of node.right, copy it into node.value, node.right = remove_from(node.right, that value). return node. remove sets self.root = remove_from(self.root, value).",
            ],
            "questions": [
                "Why does the in-order successor have at most one child?",
                "Why is the result still a valid BST after copying the successor's value up?",
            ],
        },
    ],
}

# =============================================================================
# C++
# =============================================================================

CPP_TREE_NODE = """struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v, TreeNode* l = nullptr, TreeNode* r = nullptr) : value(v), left(l), right(r) {}
};
"""

CPP_GIVEN_INSERT = """    // insert is given - read it first
    void insert(int value) {
        if (root == nullptr) {
            root = new TreeNode(value);
            return;
        }
        TreeNode* node = root;
        while (true) {
            if (value == node->value) return;
            if (value < node->value) {
                if (node->left == nullptr) { node->left = new TreeNode(value); return; }
                node = node->left;
            } else {
                if (node->right == nullptr) { node->right = new TreeNode(value); return; }
                node = node->right;
            }
        }
    }
"""

CPP_GIVEN_IN_ORDER = """
    vector<int> in_order() const {
        vector<int> result;
        visit(root, result);
        return result;
    }

    static void visit(const TreeNode* node, vector<int>& result) {
        if (node == nullptr) return;
        visit(node->left, result);
        result.push_back(node->value);
        visit(node->right, result);
    }
"""


def cpp_bst_starter(methods, given=""):
    return (CPP_HEADER + "\n" + CPP_TREE_NODE + "\nclass BST {\npublic:\n    TreeNode* root = nullptr;\n\n"
            + given + methods.rstrip("\n") + "\n};\n")


def cpp_build(values):
    """Setup code that inserts values into a new BST called t."""
    return "BST t;\nfor (int v : {" + ", ".join(str(v) for v in values) + "}) t.insert(v);"


CPP_MILESTONE = {
    "id": "cpp-dsa-trees",
    "title": "Binary Search Trees",
    "summary": "Trees of nodes with two child pointers, kept in order so that searching halves the work at every step.",
    "lesson": [
        {
            "heading": "Trees",
            "text": "A tree node has pointers to its children. The node at the top is the root, a node with no children is a leaf, and a node with everything below it is a subtree. In a binary tree each node has at most two children, `left` and `right`; a missing child is `nullptr`. The given `TreeNode` constructor takes optional children, so a small tree can be written in one expression.",
            "code": "struct TreeNode {\n    int value;\n    TreeNode* left;\n    TreeNode* right;\n    TreeNode(int v, TreeNode* l = nullptr, TreeNode* r = nullptr) : value(v), left(l), right(r) {}\n};\n\n//        5\n//       / \\\n//      3   8\nTreeNode* root = new TreeNode(5, new TreeNode(3), new TreeNode(8));",
        },
        {
            "heading": "The search tree rule",
            "text": "In a binary search tree (BST), everything in a node's left subtree is smaller than the node and everything in its right subtree is bigger - the whole subtrees, not just the children. So at each node you know which side a value must be on, and searching throws half the tree away at every step, like binary search.",
            "code": "bool contains(const TreeNode* node, int value) {\n    while (node != nullptr) {\n        if (value == node->value) return true;\n        node = value < node->value ? node->left : node->right;\n    }\n    return false;\n}",
        },
        {
            "heading": "Inserting",
            "text": "Search for the value; where the search reaches a missing child is where the new node goes, created with `new`. A value already in the tree is not inserted again.",
        },
        {
            "heading": "Recursion fits trees",
            "text": "A tree is made of smaller trees, so most tree functions are short recursions on a `TreeNode*`: answer for `nullptr`, otherwise combine the answers for the two subtrees. Visiting left, then the node, then right (in-order) gives a BST's values in sorted order. Write the recursion as a `static` helper that takes a node, and call it on `root` from the member function.",
            "code": "static int count(const TreeNode* node) {\n    if (node == nullptr) return 0;\n    return count(node->left) + 1 + count(node->right);\n}",
        },
        {
            "heading": "Height and speed",
            "text": "The height is the number of nodes on the longest root-to-leaf path. Search and insert are O(height): about log n for a well-shaped tree, but n for a tree built from already sorted values, which is just a line. `std::map` and `std::set` are balanced search trees (red-black trees) that reshape themselves to keep the height small.",
        },
        {
            "heading": "Removing a node",
            "text": "A leaf is cut off. A node with one child is replaced by that child. A node with two children takes the value of its in-order successor (the smallest value in its right subtree), and the successor is removed from the right subtree instead. A helper that returns the new root of a subtree makes the re-linking simple: `node->left = remove_from(node->left, value);`. `delete` the node you unlink.",
        },
        {
            "heading": "Common mistakes",
            "text": "Using `->` on `nullptr` - it crashes. Handle the empty tree first.\n\nValidating a BST by comparing each node only with its children. Every node must fit between bounds passed down from all its ancestors.",
        },
    ],
    "quiz": [
        {
            "question": "Insert 5, 3, 8, 1, 4 into an empty BST in that order. What are 3's children?",
            "answer": "`1` on the left and `4` on the right.",
        },
        {
            "question": "What does this produce for the tree from question 1?",
            "code": "void visit(const TreeNode* node, vector<int>& out) {\n    if (node == nullptr) return;\n    visit(node->left, out);\n    out.push_back(node->value);\n    visit(node->right, out);\n}",
            "answer": "`{1, 3, 4, 5, 8}` - in-order traversal of a BST is always sorted.",
        },
        {
            "question": "Is this a valid BST?",
            "code": "TreeNode* root = new TreeNode(5, new TreeNode(1), new TreeNode(6, new TreeNode(3), new TreeNode(7)));",
            "answer": "No: 3 is in 5's right subtree, so it would have to be bigger than 5. Each node is fine against its own children, which is why checking only children is not enough.",
        },
    ],
    "problems": [
        {
            "id": "bst-insert",
            "title": "Insert and Search",
            "difficulty": "easy",
            "description": "TreeNode is given. Complete the BST class: insert(value) adds a value in the right place (ignoring a value that is already there), and contains(value) returns true if the value is in the tree. Walk down one path using the BST rule - do not visit every node.",
            "starter": cpp_bst_starter("    void insert(int value) {\n    }\n\n    bool contains(int value) const {\n        return false;\n    }\n"),
            "compare": "exact",
            "tests": [
                {"setup": cpp_build([5, 3, 8]), "check": "vector<int>{t.root->value, t.root->left->value, t.root->right->value}", "expected": [5, 3, 8]},
                {"setup": cpp_build([5, 3, 8, 1, 4]), "check": "vector<bool>{t.contains(4), t.contains(7)}", "expected": [True, False]},
                {"edge": "empty tree", "check": "BST().contains(1)", "expected": False},
                {"setup": cpp_build([5, 3, 1]), "check": "t.root->left->left->value", "expected": 1},
                {"edge": "duplicate values", "setup": cpp_build([5, 5]), "check": "t.root->left == nullptr && t.root->right == nullptr", "expected": True},
                {"edge": "single node", "setup": cpp_build([7]), "check": "vector<bool>{t.contains(7), t.root->left == nullptr}", "expected": [True, True]},
                {"edge": "sorted input makes a line", "setup": cpp_build([1, 2, 3, 4]), "check": "t.root->right->right->right->value", "expected": 4},
            ],
            "hints": [
                "Searching and inserting walk the same path: at each node the BST rule says go left or go right.",
                "contains: start at root and move to the left or right child until you find the value or reach nullptr. insert: walk the same way until the child you need is nullptr - put the new node there.",
                "An empty tree is special for insert: the new node becomes root. Stop when value == node->value, so duplicates are ignored. Create nodes with new TreeNode(value).",
                "Structure: contains: const TreeNode* node = root; while (node) { if equal return true; node = value < node->value ? node->left : node->right; } return false. insert: if (!root) { root = new TreeNode(value); return; } loop: pick the side; if that child is nullptr, create it and return; else move to it.",
            ],
            "questions": [
                "Why does contains only need one node per level?",
                "What shape does the tree take when the values arrive sorted?",
            ],
        },
        {
            "id": "bst-inorder",
            "title": "In-Order Traversal",
            "difficulty": "easy",
            "description": "insert is given. Add in_order(), which returns all the values as a vector in ascending order, and size(), which counts the nodes. Visit the nodes recursively - do not sort.",
            "starter": cpp_bst_starter("\n    vector<int> in_order() const {\n        return {};\n    }\n\n    int size() const {\n        return 0;\n    }\n", CPP_GIVEN_INSERT),
            "compare": "exact",
            "tests": [
                {"setup": cpp_build([5, 3, 8, 1, 4]), "check": "t.in_order()", "expected": [1, 3, 4, 5, 8]},
                {"setup": cpp_build([5, 3, 8, 1, 4]), "check": "t.size()", "expected": 5},
                {"edge": "empty tree", "check": "BST().in_order()", "expected": []},
                {"edge": "empty tree", "check": "BST().size()", "expected": 0},
                {"edge": "duplicate values", "setup": cpp_build([2, 2, 1]), "check": "t.in_order()", "expected": [1, 2]},
                {"edge": "negative numbers", "setup": cpp_build([0, -5, 5, -10]), "check": "t.in_order()", "expected": [-10, -5, 0, 5]},
                {"edge": "single node", "setup": cpp_build([9]), "check": "vector<int>{t.size(), t.in_order()[0]}", "expected": [1, 9]},
            ],
            "hints": [
                "Left subtree values are smaller and right subtree values are bigger. In which order should you visit the three parts to get sorted output?",
                "Left subtree, then the node, then the right subtree - and the same rule inside each subtree. That is a recursion on TreeNode pointers.",
                "Write static helpers that take a const TreeNode* (and, for in_order, a vector<int>& to push into). nullptr is the base case.",
                "Structure: static void visit(const TreeNode* n, vector<int>& out) { if (!n) return; visit(n->left, out); out.push_back(n->value); visit(n->right, out); } in_order: vector<int> out; visit(root, out); return out. static int count(const TreeNode* n) { return n ? count(n->left) + 1 + count(n->right) : 0; }",
            ],
            "questions": [
                "Why does in-order traversal of a BST come out sorted?",
                "Why pass the vector by reference into the helper?",
            ],
        },
        {
            "id": "bst-height",
            "title": "Height, Minimum and Maximum",
            "difficulty": "easy",
            "description": "insert is given. Add height() - the number of nodes on the longest path from the root down to a leaf, 0 for an empty tree - and min_value() and max_value(), which return the smallest and largest values and throw out_of_range on an empty tree.",
            "starter": cpp_bst_starter("\n    int height() const {\n        return 0;\n    }\n\n    int min_value() const {\n        return 0;\n    }\n\n    int max_value() const {\n        return 0;\n    }\n", CPP_GIVEN_INSERT),
            "compare": "exact",
            "tests": [
                {"setup": cpp_build([5, 3, 8, 1]), "check": "t.height()", "expected": 3},
                {"setup": cpp_build([5, 3, 8, 1]), "check": "vector<int>{t.min_value(), t.max_value()}", "expected": [1, 8]},
                {"edge": "empty tree", "check": "BST().height()", "expected": 0},
                {"edge": "empty tree", "setup": "BST t;", "check": "t.min_value()", "raises": "out_of_range"},
                {"edge": "single node", "setup": cpp_build([4]), "check": "vector<int>{t.height(), t.min_value(), t.max_value()}", "expected": [1, 4, 4]},
                {"edge": "sorted input makes a line", "setup": cpp_build([1, 2, 3, 4, 5]), "check": "t.height()", "expected": 5},
                {"setup": cpp_build([3, 1, 4, 2, 5]), "check": "t.height()", "expected": 3},
            ],
            "hints": [
                "Where is the smallest value in a BST? Smaller values are always to the left.",
                "min and max need no recursion: keep going left (or right) until there is no further child. Height does: a tree is one node taller than its taller subtree.",
                "height(nullptr) is 0; otherwise 1 + max(height of left, height of right). Throw out_of_range before walking an empty tree.",
                "Structure: static int h(const TreeNode* n) { return n ? 1 + max(h(n->left), h(n->right)) : 0; } min_value: if (!root) throw out_of_range(\"empty tree\"); const TreeNode* n = root; while (n->left) n = n->left; return n->value; max_value mirrors it.",
            ],
            "questions": [
                "Why is a height of about log n the best possible for n nodes?",
                "Which C++ containers keep their trees balanced for you?",
            ],
        },
        {
            "id": "valid-bst",
            "title": "Debug: Is It a BST?",
            "difficulty": "medium",
            "description": "is_valid_bst(node) should return true if the tree rooted at node is a valid binary search tree: every value in a node's left subtree is smaller than it and every value in its right subtree is bigger (no duplicates). The given version only compares each node with its own children - which looks right, but is not. Find the trees it gets wrong and fix it. You may add a helper function.",
            "starter": CPP_HEADER + "\n" + CPP_TREE_NODE + """
bool is_valid_bst(const TreeNode* node) {
    if (node == nullptr) return true;
    if (node->left != nullptr && node->left->value >= node->value) return false;
    if (node->right != nullptr && node->right->value <= node->value) return false;
    return is_valid_bst(node->left) && is_valid_bst(node->right);
}
""",
            "compare": "exact",
            "tests": [
                {"check": "is_valid_bst(new TreeNode(5, new TreeNode(1), new TreeNode(6, new TreeNode(3), new TreeNode(7))))", "expected": False},
                {"check": "is_valid_bst(new TreeNode(10, new TreeNode(5, nullptr, new TreeNode(15)), new TreeNode(20)))", "expected": False},
                {"check": "is_valid_bst(new TreeNode(2, new TreeNode(1), new TreeNode(3)))", "expected": True},
                {"edge": "empty tree", "check": "is_valid_bst(nullptr)", "expected": True},
                {"edge": "single node", "check": "is_valid_bst(new TreeNode(1))", "expected": True},
                {"edge": "duplicate values", "check": "is_valid_bst(new TreeNode(2, new TreeNode(2)))", "expected": False},
                {"check": "is_valid_bst(new TreeNode(5, new TreeNode(3, new TreeNode(1), new TreeNode(4)), new TreeNode(8)))", "expected": True},
            ],
            "hints": [
                "Draw the first test's tree. Every node is fine against its own children - so why is it not a BST?",
                "3 sits in the right subtree of 5, so it must be bigger than 5, not just smaller than its parent 6. A node has to respect every ancestor.",
                "Pass an allowed range down the recursion in a helper: going left, the node's value becomes the upper bound; going right, the lower bound. Pointers to the bounding nodes work well, with nullptr meaning 'no limit'.",
                "Structure: bool within(const TreeNode* n, const TreeNode* low, const TreeNode* high) { if (!n) return true; if (low && n->value <= low->value) return false; if (high && n->value >= high->value) return false; return within(n->left, low, n) && within(n->right, n, high); } and is_valid_bst returns within(node, nullptr, nullptr).",
            ],
            "questions": [
                "Why did the valid trees pass even with the bug?",
                "Why are pointers to the bounding nodes neater than int bounds here?",
            ],
        },
        {
            "id": "bst-remove",
            "title": "Remove a Value",
            "difficulty": "medium",
            "description": "insert and in_order are given. Add remove(value), which takes a value out of the tree and keeps it a valid BST. Removing a value that is not there does nothing. When the node has two children, replace its value with the smallest value in its right subtree and remove that value from the right subtree instead.",
            "starter": cpp_bst_starter("\n    void remove(int value) {\n    }\n", CPP_GIVEN_INSERT + CPP_GIVEN_IN_ORDER),
            "compare": "exact",
            "tests": [
                {"setup": cpp_build([5, 3, 8, 1, 4, 7, 9]) + "\nt.remove(1);", "check": "t.in_order()", "expected": [3, 4, 5, 7, 8, 9]},
                {"setup": cpp_build([5, 3, 8, 1, 4, 7, 9]) + "\nt.remove(5);", "check": "t.root->value", "expected": 7},
                {"setup": cpp_build([5, 3, 8, 1, 4, 7, 9]) + "\nt.remove(3);", "check": "t.in_order()", "expected": [1, 4, 5, 7, 8, 9]},
                {"setup": cpp_build([5, 3, 8, 1, 4, 7, 9]) + "\nt.remove(5);", "check": "t.in_order()", "expected": [1, 3, 4, 7, 8, 9]},
                {"edge": "node with one child", "setup": cpp_build([5, 3, 1]) + "\nt.remove(3);", "check": "vector<int>{t.root->left->value, (int)t.in_order().size()}", "expected": [1, 2]},
                {"edge": "value not in the tree", "setup": cpp_build([5, 3, 8]) + "\nt.remove(42);", "check": "t.in_order()", "expected": [3, 5, 8]},
                {"edge": "empty tree", "setup": "BST t;\nt.remove(1);", "check": "t.in_order()", "expected": []},
                {"edge": "single node", "setup": cpp_build([7]) + "\nt.remove(7);", "check": "t.root == nullptr", "expected": True},
            ],
            "hints": [
                "First find the node, as in contains. Then it depends on how many children it has: none, one, or two.",
                "No children: it disappears. One child: the child takes its place. Two children: keep the node, copy in the smallest value of its right subtree, and remove that value from the right subtree.",
                "A static helper that returns the new root of a subtree makes re-linking easy: node->left = remove_from(node->left, value). Returning nullptr removes a leaf; returning the only child replaces a one-child node (delete the node you unlink).",
                "Structure: static TreeNode* remove_from(TreeNode* n, int value) { if (!n) return nullptr; if (value < n->value) n->left = remove_from(n->left, value); else if (value > n->value) n->right = remove_from(n->right, value); else { if (!n->left) { TreeNode* r = n->right; delete n; return r; } if (!n->right) { TreeNode* l = n->left; delete n; return l; } find the minimum m of n->right; n->value = m; n->right = remove_from(n->right, m); } return n; } and remove sets root = remove_from(root, value).",
            ],
            "questions": [
                "Why does the in-order successor have at most one child?",
                "What would leak if you unlinked a node without delete?",
            ],
        },
    ],
}
