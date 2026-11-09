"""Reference solutions, used only to prove that every problem's tests can be passed.

SPOILERS: if you are here to practice, close this file.
"""

SOLUTIONS = {
    "fizz-buzz": '''
def fizz_buzz(n):
    result = []
    for i in range(1, n + 1):
        if i % 15 == 0:
            result.append("FizzBuzz")
        elif i % 3 == 0:
            result.append("Fizz")
        elif i % 5 == 0:
            result.append("Buzz")
        else:
            result.append(str(i))
    return result
''',
    "reverse-string": '''
def reverse_string(s):
    chars = list(s)
    left, right = 0, len(chars) - 1
    while left < right:
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1
    return "".join(chars)
''',
    "valid-palindrome": '''
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left].lower() != s[right].lower():
            return False
        left += 1
        right -= 1
    return True
''',
    "contains-duplicate": '''
def contains_duplicate(nums):
    seen = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False
''',
    "two-sum": '''
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
''',
    "valid-anagram": '''
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in t:
        if counts.get(ch, 0) == 0:
            return False
        counts[ch] -= 1
    return True
''',
    "binary-search": '''
def binary_search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
''',
    "valid-parentheses": '''
def is_valid(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
        else:
            stack.append(ch)
    return not stack
''',
    "merge-sorted-lists": '''
def merge_sorted(a, b):
    i = j = 0
    result = []
    while i < len(a) and j < len(b):
        if a[i] <= b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])
    result.extend(b[j:])
    return result
''',
    "max-subarray": '''
def max_subarray(nums):
    current = best = nums[0]
    for num in nums[1:]:
        current = max(num, current + num)
        best = max(best, current)
    return best
''',
    "climbing-stairs": '''
def climb_stairs(n):
    if n <= 2:
        return n
    prev, current = 1, 2
    for _ in range(3, n + 1):
        prev, current = current, prev + current
    return current
''',
    "rectangle-area": '''
def rectangle_area(width, height):
    return width * height
''',
    "full-name": '''
def full_name(first, last):
    return f"{first} {last}"
''',
    "hours-and-minutes": '''
def hours_and_minutes(total_minutes):
    return [total_minutes // 60, total_minutes % 60]
''',
    "is-even": '''
def is_even(n):
    return n % 2 == 0
''',
    "sign-of": '''
def sign_of(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"
''',
    "letter-grade": '''
def letter_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"
''',
    "leap-year": '''
def is_leap_year(year):
    if year % 400 == 0:
        return True
    elif year % 100 == 0:
        return False
    else:
        return year % 4 == 0
''',
    "sum-to": '''
def sum_to(n):
    total = 0
    for i in range(1, n + 1):
        total += i
    return total
''',
    "count-vowels": '''
def count_vowels(s):
    count = 0
    for ch in s:
        if ch.lower() in "aeiou":
            count += 1
    return count
''',
    "largest-number": '''
def largest(nums):
    best = nums[0]
    for num in nums:
        if num > best:
            best = num
    return best
''',
    "only-evens": '''
def only_evens(nums):
    result = []
    for num in nums:
        if num % 2 == 0:
            result.append(num)
    return result
''',
    "average": '''
def average(nums):
    if len(nums) == 0:
        return 0
    total = 0
    for num in nums:
        total += num
    return total / len(nums)
''',
    "running-total": '''
def running_total(nums):
    total = 0
    result = []
    for num in nums:
        total += num
        result.append(total)
    return result
''',
    "count-words": '''
def count_words(s):
    return len(s.split())
''',
    "initials": '''
def initials(name):
    result = ""
    for word in name.split():
        result += word[0].upper()
    return result
''',
    "char-count": '''
def char_count(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    return counts
''',
    "first-unique-char": '''
def first_unique_char(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    for ch in s:
        if counts[ch] == 1:
            return ch
    return ""
''',
    "factorial": '''
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n - 1)
''',
    "safe-divide": '''
def safe_divide(a, b):
    if b == 0:
        raise ValueError("cannot divide by zero")
    return a / b
''',
    "to-int": '''
def to_int(text, default=0):
    try:
        return int(text)
    except ValueError:
        return default
''',
    "counter-class": '''
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def reset(self):
        self.count = 0
''',
    "rectangle-class": '''
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def is_square(self):
        return self.width == self.height
''',
    "bank-account": '''
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0 or amount > self.balance:
            raise ValueError("invalid amount")
        self.balance -= amount
''',
    "point-class": '''
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def translate(self, dx, dy):
        return Point(self.x + dx, self.y + dy)
''',
    "animal-sounds": '''
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "Some sound"

    def describe(self):
        return f"{self.name} says {self.speak()}"


class Dog(Animal):
    def speak(self):
        return "Woof"


class Cat(Animal):
    def speak(self):
        return "Meow"
''',
    "shapes": '''
class Shape:
    def __init__(self, name):
        self.name = name

    def area(self):
        return 0

    def describe(self):
        return f"{self.name} with area {self.area()}"


class Square(Shape):
    def __init__(self, side):
        super().__init__("square")
        self.side = side

    def area(self):
        return self.side * self.side


class Triangle(Shape):
    def __init__(self, base, height):
        super().__init__("triangle")
        self.base = base
        self.height = height

    def area(self):
        return self.base * self.height / 2


def total_area(shapes):
    total = 0
    for shape in shapes:
        total += shape.area()
    return total
''',
    "stack-class": '''
class Stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)
''',
    "queue-class": '''
class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        return self.items.pop(0)

    def is_empty(self):
        return len(self.items) == 0

    def __len__(self):
        return len(self.items)
''',
    "missing-number": '''
def missing_number(nums):
    present = set(nums)
    for candidate in range(len(nums) + 1):
        if candidate not in present:
            return candidate
''',
    "is-subsequence": '''
def is_subsequence(s, t):
    i = j = 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)
''',
    "evaluate-rpn": '''
def evaluate_rpn(tokens):
    stack = []
    for token in tokens:
        if token in ("+", "-", "*"):
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            else:
                stack.append(left * right)
        else:
            stack.append(int(token))
    return stack[0]
''',
    "first-at-least": '''
def first_at_least(nums, target):
    left, right = 0, len(nums) - 1
    answer = len(nums)
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] >= target:
            answer = mid
            right = mid - 1
        else:
            left = mid + 1
    return answer
''',
    "linked-list-basics": '''
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, value):
        node = Node(value)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = node

    def prepend(self, value):
        node = Node(value)
        node.next = self.head
        self.head = node

    def to_list(self):
        values = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def __len__(self):
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count
''',
    "reverse-linked-list": '''
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

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
        previous = None
        current = self.head
        while current is not None:
            following = current.next
            current.next = previous
            previous = current
            current = following
        self.head = previous
''',
    "average-of-two": '''
def average_of_two(a, b):
    total = a + b
    return total / 2
''',
    "sum-of-evens": '''
def sum_of_evens(n):
    total = 0
    for i in range(1, n + 1):
        if i % 2 == 0:
            total += i
    return total
''',
    "count-char": '''
def count_char(s, ch):
    count = 0
    for letter in s:
        if letter == ch:
            count += 1
    return count
''',
    "has-digit": '''
def has_digit(s):
    for ch in s:
        if ch.isdigit():
            return True
    return False
''',
    "sum-of-digits": '''
def sum_of_digits(n):
    total = 0
    rest = n
    while rest > 0:
        total += rest % 10
        rest = rest // 10
    return total
''',
    "index-of": '''
def index_of(nums, target):
    for i in range(len(nums)):
        if nums[i] == target:
            return i
    return -1
''',
    "without-negatives": '''
def without_negatives(nums):
    result = []
    for n in nums:
        if n >= 0:
            result.append(n)
    return result
''',
    "capitalize-words": '''
def capitalize_words(s):
    words = []
    for word in s.split():
        words.append(word[0].upper() + word[1:])
    return " ".join(words)
''',
    "is-palindrome-word": '''
def is_palindrome_word(word):
    lowered = word.lower()
    return lowered == lowered[::-1]
''',
    "longest-word": '''
def longest_word(s):
    best = ""
    for word in s.split():
        if len(word) > len(best):
            best = word
    return best
''',
    "remove-spaces": '''
def remove_spaces(s):
    return s.replace(" ", "")
''',
    "unique-count": '''
def unique_count(nums):
    return len(set(nums))
''',
    "most-common-char": '''
def most_common_char(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    best = ""
    for ch in s:
        if best == "" or counts[ch] > counts[best]:
            best = ch
    return best
''',
    "group-by-first-letter": '''
def group_by_first_letter(words):
    groups = {}
    for word in words:
        letter = word[0]
        if letter not in groups:
            groups[letter] = []
        groups[letter].append(word)
    return groups
''',
    "parse-scores": '''
def parse_scores(text):
    scores = []
    for piece in text.split(","):
        try:
            scores.append(int(piece))
        except ValueError:
            pass
    return scores
''',
    "primes": '''
def is_prime(n):
    if n < 2:
        return False
    for d in range(2, n):
        if n % d == 0:
            return False
    return True


def primes_up_to(n):
    result = []
    for k in range(2, n + 1):
        if is_prime(k):
            result.append(k)
    return result
''',
    "power": '''
def power(base, exp):
    if exp == 0:
        return 1
    return base * power(base, exp - 1)
''',
    "count-down": '''
def count_down(n):
    if n == 0:
        return [0]
    return [n] + count_down(n - 1)
''',
    "sum-list": '''
def sum_list(nums):
    if len(nums) == 0:
        return 0
    return nums[0] + sum_list(nums[1:])
''',
    "reverse-recursive": '''
def reverse_recursive(s):
    if s == "":
        return ""
    return reverse_recursive(s[1:]) + s[0]
''',
    "light-switch": '''
class LightSwitch:
    def __init__(self):
        self.on = False

    def toggle(self):
        self.on = not self.on

    def is_on(self):
        return self.on
''',
    "playlist": '''
class Playlist:
    def __init__(self):
        self.songs = []

    def add(self, song):
        self.songs.append(song)

    def count(self):
        return len(self.songs)

    def has(self, song):
        return song in self.songs

    def remove(self, song):
        self.songs.remove(song)
''',
    "inventory": '''
class Inventory:
    def __init__(self):
        self.stock = {}

    def add(self, item, qty):
        if qty <= 0:
            raise ValueError("quantity must be positive")
        self.stock[item] = self.stock.get(item, 0) + qty

    def remove(self, item, qty):
        if qty <= 0 or self.quantity(item) < qty:
            raise ValueError("cannot remove that many")
        self.stock[item] -= qty

    def quantity(self, item):
        return self.stock.get(item, 0)

    def total(self):
        units = 0
        for qty in self.stock.values():
            units += qty
        return units
''',
    "vehicles": '''
class Vehicle:
    def __init__(self, name):
        self.name = name

    def wheels(self):
        return 4

    def summary(self):
        return f"{self.name} has {self.wheels()} wheels"


class Bike(Vehicle):
    def wheels(self):
        return 2


class Truck(Vehicle):
    def __init__(self, name, load):
        super().__init__(name)
        self.load = load

    def wheels(self):
        return 6
''',
    "text-editor": '''
class TextEditor:
    def __init__(self):
        self.text = ""
        self.history = []

    def write(self, s):
        self.history.append(self.text)
        self.text = self.text + s

    def undo(self):
        if self.history:
            self.text = self.history.pop()
''',
    "has-pair-sum": '''
def has_pair_sum(nums, target):
    seen = set()
    for n in nums:
        if target - n in seen:
            return True
        seen.add(n)
    return False
''',
    "pair-sum-sorted": '''
def pair_sum_sorted(nums, target):
    left, right = 0, len(nums) - 1
    while left < right:
        total = nums[left] + nums[right]
        if total == target:
            return True
        if total < target:
            left += 1
        else:
            right -= 1
    return False
''',
    "remove-adjacent-duplicates": '''
def remove_adjacent_duplicates(s):
    stack = []
    for ch in s:
        if stack and stack[-1] == ch:
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)
''',
    "sqrt-floor": '''
def sqrt_floor(n):
    left, right = 0, n
    answer = 0
    while left <= right:
        mid = (left + right) // 2
        if mid * mid <= n:
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    return answer
''',
    "linked-list-search": '''
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

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

    def contains(self, value):
        current = self.head
        while current is not None:
            if current.value == value:
                return True
            current = current.next
        return False

    def last(self):
        if self.head is None:
            return None
        current = self.head
        while current.next is not None:
            current = current.next
        return current.value
''',
    "fibonacci": '''
def fib(n):
    if n < 2:
        return n
    previous, current = 0, 1
    for _ in range(n - 1):
        previous, current = current, previous + current
    return current
''',
    'bst-insert': '''
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class BST:
    def __init__(self):
        self.root = None

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

    def contains(self, value):
        node = self.root
        while node is not None:
            if value == node.value:
                return True
            node = node.left if value < node.value else node.right
        return False
''',
    'bst-inorder': '''
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def _walk(node):
    if node is None:
        return []
    return _walk(node.left) + [node.value] + _walk(node.right)


def _count(node):
    if node is None:
        return 0
    return _count(node.left) + 1 + _count(node.right)


class BST:
    def __init__(self):
        self.root = None

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

    def in_order(self):
        return _walk(self.root)

    def size(self):
        return _count(self.root)
''',
    'bst-height': '''
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def _height(node):
    if node is None:
        return 0
    return 1 + max(_height(node.left), _height(node.right))


class BST:
    def __init__(self):
        self.root = None

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

    def height(self):
        return _height(self.root)

    def min_value(self):
        if self.root is None:
            raise ValueError("empty tree")
        node = self.root
        while node.left is not None:
            node = node.left
        return node.value

    def max_value(self):
        if self.root is None:
            raise ValueError("empty tree")
        node = self.root
        while node.right is not None:
            node = node.right
        return node.value
''',
    'valid-bst': '''
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def is_valid_bst(node, low=None, high=None):
    if node is None:
        return True
    if low is not None and node.value <= low:
        return False
    if high is not None and node.value >= high:
        return False
    return is_valid_bst(node.left, low, node.value) and is_valid_bst(node.right, node.value, high)
''',
    'bst-remove': '''
class TreeNode:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


def _remove_from(node, value):
    if node is None:
        return None
    if value < node.value:
        node.left = _remove_from(node.left, value)
    elif value > node.value:
        node.right = _remove_from(node.right, value)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        successor = node.right
        while successor.left is not None:
            successor = successor.left
        node.value = successor.value
        node.right = _remove_from(node.right, successor.value)
    return node


class BST:
    def __init__(self):
        self.root = None

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

    def in_order(self):
        result = []

        def visit(node):
            if node is not None:
                visit(node.left)
                result.append(node.value)
                visit(node.right)

        visit(self.root)
        return result

    def remove(self, value):
        self.root = _remove_from(self.root, value)
''',
}
