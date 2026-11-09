"""Track 2: Object-Oriented Programming. The format is described in problems.py."""

TRACK = {
    "id": "oop",
    "title": "Object-Oriented Programming",
    "description": "Bundle data and behaviour into your own types with classes.",
    "milestones": [
        # ------------------------------------------------------------------
        {
            "id": "oop-classes",
            "title": "Classes & Objects",
            "summary": "Define a class, create objects from it, and give them attributes and methods.",
            "lesson": [
                {
                    "heading": "Why classes?",
                    "text": "So far your data (numbers, lists, dictionaries) and the functions that work on it have lived separately. A class lets you bundle them: it describes a new kind of value, with its own data (attributes) and its own functions (methods). `list` and `str` are classes; now you will write your own.",
                },
                {
                    "heading": "Defining a class",
                    "text": "A class is a blueprint. An object (or instance) is one thing built from that blueprint. `__init__` is a special method that runs automatically when an object is created; it sets up the object's starting attributes.",
                    "code": "class Dog:\n    def __init__(self, name):\n        self.name = name\n        self.tricks = 0\n\nrex = Dog(\"Rex\")     # runs __init__\nrex.name            # 'Rex'",
                },
                {
                    "heading": "self",
                    "text": "Every method's first parameter is `self`: the particular object the method was called on. You never pass it yourself - `rex.learn()` passes `rex` as `self` automatically. Inside a method, attributes are always reached through `self`.",
                    "code": "class Dog:\n    def __init__(self, name):\n        self.name = name\n        self.tricks = 0\n\n    def learn(self):\n        self.tricks = self.tricks + 1\n\n    def describe(self):\n        return f\"{self.name} knows {self.tricks} tricks\"",
                },
                {
                    "heading": "Objects are independent",
                    "text": "Each object has its own copy of the attributes. Changing one object does not affect another made from the same class.",
                    "code": "rex = Dog(\"Rex\")\nfido = Dog(\"Fido\")\nrex.learn()\nrex.tricks      # 1\nfido.tricks     # 0",
                },
                {
                    "heading": "Common mistakes",
                    "text": "Forgetting `self.` creates an ordinary local variable that vanishes when the method ends: `tricks = 0` inside `__init__` sets nothing on the object.\n\nForgetting `self` in a method's parameter list gives 'takes 0 positional arguments but 1 was given'.\n\nIf an answer depends on attributes that can change, compute it in a method each time instead of storing it once in `__init__`.",
                },
                {
                    "heading": "Attributes can hold lists",
                    "text": "An attribute can hold any value - a number, a string, or a whole list or dictionary. Create the empty list in `__init__`, so every object gets its own, and then use `self.books` in the methods exactly like any other list. This pattern - a class that keeps a list and offers methods to work with it - is how most data structures are built.",
                    "code": "class Shelf:\n    def __init__(self):\n        self.books = []           # every Shelf starts with its own empty list\n\n    def add(self, title):\n        self.books.append(title)\n\n    def count(self):\n        return len(self.books)\n\nshelf = Shelf()\nshelf.add(\"Dune\")\nshelf.count()       # 1",
                },
            ],
            "quiz": [
                {
                    "question": "What are `a.items` and `b.items` at the end?",
                    "code": "class Box:\n    def __init__(self):\n        self.items = []\n\n    def put(self, x):\n        self.items.append(x)\n\na = Box()\nb = Box()\na.put(1)\na.put(2)\nb.put(3)",
                    "answer": "`a.items` is `[1, 2]` and `b.items` is `[3]`. Each Box got its own list when `__init__` ran.",
                },
                {
                    "question": "What happens on the last line?",
                    "code": "class Light:\n    def __init__(self):\n        on = False\n\n    def is_on(self):\n        return self.on\n\nLight().is_on()",
                    "answer": "An `AttributeError`: the object has no attribute `on`. `on = False` without `self.` made an ordinary local variable that vanished when `__init__` finished.",
                },
                {
                    "question": "What is `d.name` at the end?",
                    "code": "class Dog:\n    def __init__(self, name):\n        self.name = name\n\n    def rename(self, new_name):\n        self.name = new_name\n\nd = Dog(\"Rex\")\ne = d\ne.rename(\"Max\")",
                    "answer": "`'Max'`. `e = d` does not copy the dog - d and e are two names for the same object, just like two names for one list.",
                },
            ],
            "problems": [
                {
                    "id": "counter-class",
                    "title": "Counter",
                    "difficulty": "easy",
                    "description": "Write a class Counter. A new counter has an attribute count equal to 0. increment() raises count by one, and reset() sets it back to 0.",
                    "starter": (
                        "class Counter:\n"
                        "    def __init__(self):\n"
                        "        pass\n"
                        "\n"
                        "    def increment(self):\n"
                        "        pass\n"
                        "\n"
                        "    def reset(self):\n"
                        "        pass\n"
                    ),
                    "requires": ["Counter"],
                    "compare": "exact",
                    "tests": [
                        {"setup": "c = Counter()\nc.increment()\nc.increment()", "check": "c.count", "expected": 2},
                        {"edge": "brand-new object", "setup": "c = Counter()", "check": "c.count", "expected": 0},
                        {"setup": "c = Counter()\nc.increment()\nc.reset()", "check": "c.count", "expected": 0},
                        {"edge": "two separate objects", "setup": "a = Counter()\nb = Counter()\na.increment()", "check": "[a.count, b.count]", "expected": [1, 0]},
                        {"setup": "c = Counter()\nfor _ in range(5):\n    c.increment()", "check": "c.count", "expected": 5},
                    ],
                    "hints": [
                        "A counter has to remember one number between method calls. Where can an object keep a value so that all its methods can reach it?",
                        "Attributes live on self. Create the attribute when the object is built, and change it in the other methods.",
                        "__init__ runs once for each new object: set `self.count` there. Every other method reads and writes that same `self.count`.",
                        "Structure: in __init__ set self.count to 0; in increment set self.count to itself plus 1; in reset set self.count to 0.",
                    ],
                    "questions": [
                        "Why do two Counter objects not share their count?",
                        "What happens if you write count = 0 instead of self.count = 0?",
                    ],
                },
                {
                    "id": "light-switch",
                    "title": "Debug: Light Switch",
                    "difficulty": "easy",
                    "description": "A LightSwitch starts off. toggle() flips it between off and on, and is_on() returns True when it is on. The class has two bugs - both are about self. Fix them.",
                    "starter": "class LightSwitch:\n    def __init__(self):\n        on = False\n\n    def toggle(self):\n        self.on = not self.on\n\n    def is_on():\n        return self.on\n",
                    "requires": ["LightSwitch"],
                    "compare": "exact",
                    "tests": [
                        {"edge": "brand-new object", "check": "LightSwitch().is_on()", "expected": False},
                        {"setup": "s = LightSwitch()\ns.toggle()", "check": "s.is_on()", "expected": True},
                        {"setup": "s = LightSwitch()\ns.toggle()\ns.toggle()", "check": "s.is_on()", "expected": False},
                        {"edge": "two separate objects", "setup": "a = LightSwitch()\nb = LightSwitch()\na.toggle()", "check": "[a.is_on(), b.is_on()]", "expected": [True, False]},
                        {"setup": "s = LightSwitch()", "check": "s.on", "expected": False},
                    ],
                    "hints": [
                        "Read the error in each failing test carefully - they point at two different lines.",
                        "One error says a method takes 0 arguments but 1 was given. Python passes the object itself into every method call. The other says the object has no attribute on.",
                        "Every method needs self as its first parameter. And a value only becomes part of the object when you assign it through self.",
                        "Structure: in __init__, write self.on = False; give is_on the parameter self.",
                    ],
                    "questions": [
                        "Why does `s.is_on()` count as passing one argument?",
                        "What does `not` do to True and to False?",
                    ],
                },
                {
                    "id": "rectangle-class",
                    "title": "Rectangle",
                    "difficulty": "easy",
                    "description": "Write a class Rectangle that is created with a width and a height and stores them as attributes of the same names. area() returns width times height, perimeter() returns the distance around the edge, and is_square() returns True when width and height are equal.",
                    "starter": (
                        "class Rectangle:\n"
                        "    def __init__(self, width, height):\n"
                        "        pass\n"
                        "\n"
                        "    def area(self):\n"
                        "        pass\n"
                        "\n"
                        "    def perimeter(self):\n"
                        "        pass\n"
                        "\n"
                        "    def is_square(self):\n"
                        "        pass\n"
                    ),
                    "requires": ["Rectangle"],
                    "compare": "exact",
                    "tests": [
                        {"check": "Rectangle(3, 4).area()", "expected": 12},
                        {"check": "Rectangle(3, 4).perimeter()", "expected": 14},
                        {"check": "Rectangle(3, 4).is_square()", "expected": False},
                        {"edge": "square", "check": "Rectangle(5, 5).is_square()", "expected": True},
                        {"setup": "r = Rectangle(3, 4)", "check": "[r.width, r.height]", "expected": [3, 4]},
                        {"edge": "attribute changed after creation", "setup": "r = Rectangle(3, 4)\nr.width = 10", "check": "r.area()", "expected": 40},
                    ],
                    "hints": [
                        "The object has to remember the two numbers it was created with, so its methods can use them later.",
                        "__init__ receives width and height as parameters. Parameters disappear when __init__ finishes unless you copy them onto self.",
                        "Each method works from self.width and self.height. Calculate the answer when the method is called rather than storing it in __init__ - the last test changes the width afterwards.",
                        "Structure: __init__ stores both parameters on self; area returns their product; perimeter returns two times their sum; is_square returns the comparison of the two with ==.",
                    ],
                    "questions": [
                        "Why would storing self.area in __init__ fail the last test?",
                        "What is the difference between the parameter width and the attribute self.width?",
                    ],
                },
                {
                    "id": "playlist",
                    "title": "Playlist",
                    "difficulty": "easy",
                    "description": "Write a class Playlist. A new playlist is empty. Its attribute songs is the list of song titles in the order they were added. add(song) adds a title to the end, count() returns how many songs it holds, has(song) returns True if that title is in it, and remove(song) removes the first copy of that title - raising ValueError if it is not there.",
                    "starter": "class Playlist:\n    def __init__(self):\n        pass\n\n    def add(self, song):\n        pass\n\n    def count(self):\n        pass\n\n    def has(self, song):\n        pass\n\n    def remove(self, song):\n        pass\n",
                    "requires": ["Playlist"],
                    "compare": "exact",
                    "tests": [
                        {"setup": "p = Playlist()\np.add('Intro')\np.add('Hello')", "check": "p.songs", "expected": ["Intro", "Hello"]},
                        {"setup": "p = Playlist()\np.add('Intro')\np.add('Hello')", "check": "p.count()", "expected": 2},
                        {"edge": "brand-new object", "check": "Playlist().count()", "expected": 0},
                        {"setup": "p = Playlist()\np.add('A')", "check": "[p.has('A'), p.has('B')]", "expected": [True, False]},
                        {"edge": "duplicate titles", "setup": "p = Playlist()\np.add('A')\np.add('B')\np.add('A')\np.remove('A')", "check": "p.songs", "expected": ["B", "A"]},
                        {"setup": "p = Playlist()", "check": "p.remove('X')", "raises": "ValueError"},
                        {"edge": "two separate objects", "setup": "a = Playlist()\nb = Playlist()\na.add('A')", "check": "b.songs", "expected": []},
                    ],
                    "hints": [
                        "The playlist has to remember a sequence of titles between method calls. Which built-in type keeps things in order, and where does the object keep it?",
                        "Create an empty list in __init__ and store it as self.songs. Every other method is one line that uses that list - see 'Attributes can hold lists' in the lesson.",
                        "append adds to the end, len counts, `in` checks membership, and a list's remove(x) deletes the first x - it already raises ValueError when x is missing.",
                        "Structure: __init__ sets self.songs = []; add appends song to self.songs; count returns len(self.songs); has returns song in self.songs; remove calls self.songs.remove(song).",
                    ],
                    "questions": [
                        "Why must the empty list be created inside __init__ and not shared?",
                        "Which method would you add to move a song to the top?",
                    ],
                },
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "oop-encapsulation",
            "title": "Protecting State & Special Methods",
            "summary": "Make objects enforce their own rules, and teach them to print and compare themselves.",
            "lesson": [
                {
                    "heading": "Objects guard their own data",
                    "text": "A good class does not let itself be put into a nonsense state. Instead of letting outside code change attributes freely, it offers methods that check the rules first. This is called encapsulation: the rules about the data live next to the data.",
                    "code": "class Thermostat:\n    def __init__(self):\n        self.target = 20\n\n    def set_target(self, degrees):\n        if degrees < 5 or degrees > 30:\n            raise ValueError(\"target must be between 5 and 30\")\n        self.target = degrees",
                },
                {
                    "heading": "Check first, then change",
                    "text": "Validate before you modify anything. If a method raises an error halfway through, the object should be left exactly as it was.",
                },
                {
                    "heading": "__str__: how an object prints",
                    "text": "Methods with double underscores are special: Python calls them for you. `__str__` is used by `str(obj)` and `print(obj)`. It must return a string.",
                    "code": "class Money:\n    def __init__(self, amount):\n        self.amount = amount\n\n    def __str__(self):\n        return f\"${self.amount}\"\n\nstr(Money(5))      # '$5'",
                },
                {
                    "heading": "__eq__: what 'equal' means",
                    "text": "By default two different objects are never `==`, even if their attributes match. Define `__eq__` to say when two objects of your class count as equal. It receives the other object and returns True or False.",
                    "code": "    def __eq__(self, other):\n        return self.amount == other.amount\n\nMoney(5) == Money(5)     # True, thanks to __eq__",
                },
                {
                    "heading": "Returning new objects",
                    "text": "A method can build and return a brand-new object of its own class instead of changing itself. That keeps the original untouched, which is often safer.",
                    "code": "    def doubled(self):\n        return Money(self.amount * 2)",
                },
            ],
            "quiz": [
                {
                    "question": "What is the value of the last line?",
                    "code": "class Money:\n    def __init__(self, amount):\n        self.amount = amount\n\n    def __str__(self):\n        return f\"${self.amount}\"\n\nm = Money(5)\n[str(m), m.amount]",
                    "answer": "`['$5', 5]`. `str(m)` calls `__str__`; `m.amount` is still the plain number.",
                },
                {
                    "question": "What is the value of the last line?",
                    "code": "class P:\n    def __init__(self, x):\n        self.x = x\n\n[P(1) == P(1), P(1).x == P(1).x]",
                    "answer": "`[False, True]`. Without `__eq__`, two different objects are never equal, even with identical attributes. Their x values, being plain numbers, are.",
                },
                {
                    "question": "What is `a.balance` at the end?",
                    "code": "class Account:\n    def __init__(self):\n        self.balance = 10\n\n    def withdraw(self, amount):\n        self.balance = self.balance - amount\n        if self.balance < 0:\n            raise ValueError(\"not enough money\")\n\na = Account()\ntry:\n    a.withdraw(50)\nexcept ValueError:\n    pass",
                    "answer": "`-40`. The balance was changed before the check, so the error came too late to protect it. Check first, then change.",
                },
            ],
            "problems": [
                {
                    "id": "bank-account",
                    "title": "Bank Account",
                    "difficulty": "easy",
                    "description": "Write a class BankAccount created with an owner and an optional starting balance (default 0), stored as attributes owner and balance. deposit(amount) adds to the balance and withdraw(amount) subtracts from it. Both raise ValueError if amount is not positive, and withdraw also raises ValueError if amount is more than the balance. A failed call must leave the balance unchanged.",
                    "starter": "class BankAccount:\n    pass\n",
                    "requires": ["BankAccount"],
                    "compare": "exact",
                    "tests": [
                        {"setup": "a = BankAccount('Ann', 100)\na.deposit(50)", "check": "a.balance", "expected": 150},
                        {"setup": "a = BankAccount('Ann', 100)", "check": "a.withdraw(500)", "raises": "ValueError"},
                        {"edge": "default argument", "check": "BankAccount('Ann').balance", "expected": 0},
                        {"check": "BankAccount('Ann', 100).owner", "expected": "Ann"},
                        {"setup": "a = BankAccount('Ann', 100)\na.withdraw(30)", "check": "a.balance", "expected": 70},
                        {"edge": "withdraw everything", "setup": "a = BankAccount('Ann', 100)\na.withdraw(100)", "check": "a.balance", "expected": 0},
                        {"setup": "a = BankAccount('Ann', 100)", "check": "a.deposit(-5)", "raises": "ValueError"},
                        {"setup": "a = BankAccount('Ann', 100)", "check": "a.withdraw(0)", "raises": "ValueError"},
                        {"edge": "failed call leaves state unchanged", 
                            "setup": "a = BankAccount('Ann', 100)\ntry:\n    a.withdraw(500)\nexcept ValueError:\n    pass",
                            "check": "a.balance",
                            "expected": 100,
                        },
                    ],
                    "hints": [
                        "The account remembers two things and has two actions. Each action has rules about which amounts it accepts.",
                        "Write __init__ first, with a default value for the balance parameter. Then write each method as: check the rules, then change the balance.",
                        "Do the checks before touching self.balance, so a rejected call changes nothing. `raise ValueError(\"message\")` rejects the call.",
                        "Structure: __init__(self, owner, balance=0) stores both on self. deposit: if amount <= 0 raise ValueError, otherwise add it. withdraw: if amount <= 0 or amount is greater than self.balance raise ValueError, otherwise subtract it.",
                    ],
                    "questions": [
                        "Why should the checks come before the balance changes?",
                        "Outside code can still write a.balance = -50 directly. How might a class discourage that?",
                    ],
                },
                {
                    "id": "point-class",
                    "title": "Point",
                    "difficulty": "easy",
                    "description": "Write a class Point with attributes x and y. str(point) gives text like \"(1, 2)\". Two points are equal with == when their x and y values match. translate(dx, dy) returns a new Point moved by that amount and leaves the original point unchanged.",
                    "starter": "class Point:\n    pass\n",
                    "requires": ["Point"],
                    "compare": "exact",
                    "tests": [
                        {"check": "str(Point(1, 2))", "expected": "(1, 2)"},
                        {"check": "Point(1, 2) == Point(1, 2)", "expected": True},
                        {"check": "Point(1, 2) == Point(2, 1)", "expected": False},
                        {"edge": "negative numbers", "check": "str(Point(-1, 0))", "expected": "(-1, 0)"},
                        {"check": "str(Point(1, 2).translate(3, -1))", "expected": "(4, 1)"},
                        {"edge": "original must not change", 
                            "setup": "p = Point(1, 2)\nq = p.translate(1, 1)",
                            "check": "[p.x, p.y, q.x, q.y]",
                            "expected": [1, 2, 2, 3],
                        },
                    ],
                    "hints": [
                        "There are three behaviours to add: how a point turns into text, when two points are equal, and how to make a moved copy.",
                        "Python looks for specially named methods: __str__ for text and __eq__ for ==. translate is an ordinary method that builds a new object.",
                        "__str__ must return a string - an f-string with self.x and self.y does it. __eq__ takes self and other and compares both coordinates. translate calls Point(...) with new coordinates and returns the result.",
                        "Structure: __init__ stores x and y. __str__ returns the f-string \"({self.x}, {self.y})\". __eq__ returns whether both x values match and both y values match. translate returns Point(self.x + dx, self.y + dy).",
                    ],
                    "questions": [
                        "Without __eq__, why is Point(1, 2) == Point(1, 2) False?",
                        "Why does translate not need to change self.x?",
                    ],
                },
                {
                    "id": "inventory",
                    "title": "Inventory",
                    "difficulty": "medium",
                    "description": "Write a class Inventory that tracks how many of each item is in stock, using a dictionary stored in an attribute. add(item, qty) adds qty units of item. remove(item, qty) takes qty units away. quantity(item) returns how many are in stock, 0 for an item never added. total() returns the number of units across all items. add and remove raise ValueError if qty is not positive, and remove also raises ValueError if there are fewer than qty in stock - leaving the stock unchanged.",
                    "starter": "class Inventory:\n    pass\n",
                    "requires": ["Inventory"],
                    "compare": "exact",
                    "tests": [
                        {"setup": "inv = Inventory()\ninv.add('apple', 5)\ninv.add('apple', 3)", "check": "inv.quantity('apple')", "expected": 8},
                        {"setup": "inv = Inventory()\ninv.add('apple', 2)", "check": "inv.remove('apple', 5)", "raises": "ValueError"},
                        {"edge": "unknown item", "check": "Inventory().quantity('pear')", "expected": 0},
                        {"setup": "inv = Inventory()\ninv.add('a', 2)\ninv.add('b', 3)", "check": "inv.total()", "expected": 5},
                        {"setup": "inv = Inventory()\ninv.add('a', 4)\ninv.remove('a', 1)", "check": "inv.quantity('a')", "expected": 3},
                        {"setup": "inv = Inventory()", "check": "inv.add('a', 0)", "raises": "ValueError"},
                        {"edge": "failed call leaves state unchanged", "setup": "inv = Inventory()\ninv.add('a', 2)\ntry:\n    inv.remove('a', 3)\nexcept ValueError:\n    pass", "check": "inv.quantity('a')", "expected": 2},
                        {"setup": "inv = Inventory()", "check": "inv.remove('ghost', 1)", "raises": "ValueError"},
                        {"edge": "brand-new object", "check": "Inventory().total()", "expected": 0},
                    ],
                    "hints": [
                        "This is Bank Account with many balances instead of one - one per item. What maps a name to a number?",
                        "Keep a dictionary from item name to quantity in self.stock, created empty in __init__. The counting pattern from the Dictionaries milestone handles adding.",
                        "`self.stock.get(item, 0)` is the current quantity even for an unknown item - use it in quantity and in remove's check. Check every rule before changing anything. total adds up the values in the dictionary.",
                        "Structure: __init__: self.stock = {}. add: if qty <= 0 raise; set stock[item] to get(item, 0) + qty. remove: if qty <= 0 or quantity(item) < qty raise; subtract qty. quantity: return get(item, 0). total: loop over the values, adding them up.",
                    ],
                    "questions": [
                        "Why can remove call self.quantity instead of reading the dictionary directly?",
                        "Should an item with quantity 0 stay in the dictionary? What changes if it doesn't?",
                    ],
                },
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "oop-inheritance",
            "title": "Inheritance & Polymorphism",
            "summary": "Build specialised classes on top of general ones, and let different objects answer the same call in their own way.",
            "lesson": [
                {
                    "heading": "Inheritance",
                    "text": "A class can be based on another class. The new class (the subclass or child) automatically gets all the attributes and methods of the original (the parent), and can add or replace some.",
                    "code": "class Employee:\n    def __init__(self, name):\n        self.name = name\n\n    def role(self):\n        return \"employee\"\n\n    def badge(self):\n        return f\"{self.name} ({self.role()})\"\n\nclass Manager(Employee):\n    def role(self):\n        return \"manager\"",
                },
                {
                    "heading": "Overriding",
                    "text": "When a subclass defines a method with the same name as one in its parent, the subclass version wins for objects of the subclass. Everything it does not override still comes from the parent - `Manager` has no `__init__` or `badge` of its own, yet both work.",
                    "code": "Manager(\"Grace\").badge()      # 'Grace (manager)'\nEmployee(\"Alan\").badge()      # 'Alan (employee)'",
                },
                {
                    "heading": "Polymorphism",
                    "text": "Notice that `badge` calls `self.role()` without knowing which class self is. Each object answers in its own way. Code that works on 'any Employee' keeps working for every subclass you add later, with no if statements checking types.",
                    "code": "staff = [Employee(\"Alan\"), Manager(\"Grace\")]\nfor person in staff:\n    print(person.badge())",
                },
                {
                    "heading": "super()",
                    "text": "If a subclass needs its own `__init__`, it should usually let the parent set itself up first. `super().__init__(...)` calls the parent's version.",
                    "code": "class Manager(Employee):\n    def __init__(self, name, team_size):\n        super().__init__(name)\n        self.team_size = team_size",
                },
                {
                    "heading": "isinstance",
                    "text": "`isinstance(obj, SomeClass)` is True if the object was made from that class or any subclass of it. A Manager is an Employee.",
                    "code": "isinstance(Manager(\"Grace\", 4), Employee)     # True",
                },
            ],
            "quiz": [
                {
                    "question": "What does the last line return?",
                    "code": "class A:\n    def hello(self):\n        return \"A\"\n\n    def greet(self):\n        return \"I am \" + self.hello()\n\nclass B(A):\n    def hello(self):\n        return \"B\"\n\nB().greet()",
                    "answer": "`'I am B'`. greet comes from A, but self is a B object, so `self.hello()` runs B's version.",
                },
                {
                    "question": "What happens on the last line?",
                    "code": "class Base:\n    def __init__(self, name):\n        self.name = name\n\nclass Child(Base):\n    def __init__(self, name, age):\n        self.age = age\n\nChild(\"Kim\", 9).name",
                    "answer": "An `AttributeError`. Child has its own `__init__`, so Base's never runs and name is never set. It needs `super().__init__(name)`.",
                },
                {
                    "question": "What does `Cat().describe()` return?",
                    "code": "class Cat:\n    def sound(self):\n        return \"Meow\"\n\n    def describe(self):\n        return f\"says {self.sound}\"",
                    "answer": "Something like `'says <bound method Cat.sound of <...Cat object at 0x...>>'`. `self.sound` without brackets is the method itself; `self.sound()` calls it and gives `'Meow'`.",
                },
            ],
            "problems": [
                {
                    "id": "animal-sounds",
                    "title": "Animal Sounds",
                    "difficulty": "easy",
                    "description": "Write a class Animal created with a name (stored as the attribute name). speak() returns \"Some sound\", and describe() returns text like \"Rex says Woof\", built from the name and whatever speak() returns. Then write Dog and Cat as subclasses of Animal: a Dog's speak() returns \"Woof\" and a Cat's returns \"Meow\". Dog and Cat should not need a describe() of their own.",
                    "starter": "class Animal:\n    pass\n\n\nclass Dog(Animal):\n    pass\n\n\nclass Cat(Animal):\n    pass\n",
                    "requires": ["Animal", "Dog", "Cat"],
                    "compare": "exact",
                    "tests": [
                        {"check": "Dog('Rex').speak()", "expected": "Woof"},
                        {"check": "Cat('Tom').describe()", "expected": "Tom says Meow"},
                        {"check": "Dog('Rex').describe()", "expected": "Rex says Woof"},
                        {"edge": "the base class itself", "check": "Animal('Generic').describe()", "expected": "Generic says Some sound"},
                        {"check": "isinstance(Dog('Rex'), Animal)", "expected": True},
                        {"check": "Dog('Rex').name", "expected": "Rex"},
                        {"check": "[a.speak() for a in [Dog('a'), Cat('b'), Dog('c')]]", "expected": ["Woof", "Meow", "Woof"]},
                    ],
                    "hints": [
                        "Everything the three classes have in common belongs in Animal. Dog and Cat only need to say what is different about them.",
                        "Only one thing differs between the animals: the sound. So each subclass overrides exactly one method.",
                        "Inside describe, call self.speak() rather than writing the sound out. For a Dog object, self.speak() runs the Dog version automatically.",
                        "Structure: Animal has __init__ storing the name, speak returning \"Some sound\", and describe returning an f-string made from self.name and self.speak(). Dog and Cat each contain only a speak method returning their own sound.",
                    ],
                    "questions": [
                        "How does describe() know which speak() to call?",
                        "What would you have to change to add a Cow class?",
                    ],
                },
                {
                    "id": "vehicles",
                    "title": "Debug: Vehicles",
                    "difficulty": "easy",
                    "description": "summary() should give text like \"Car has 4 wheels\". A Bike has 2 wheels; a Truck has 6 and also remembers its load. There are two bugs: one in Vehicle and one in Truck. Use the errors in the results panel to find them.",
                    "starter": "class Vehicle:\n    def __init__(self, name):\n        self.name = name\n\n    def wheels(self):\n        return 4\n\n    def summary(self):\n        return f\"{self.name} has {self.wheels} wheels\"\n\n\nclass Bike(Vehicle):\n    def wheels(self):\n        return 2\n\n\nclass Truck(Vehicle):\n    def __init__(self, name, load):\n        self.load = load\n\n    def wheels(self):\n        return 6\n",
                    "requires": ["Vehicle", "Bike", "Truck"],
                    "compare": "exact",
                    "tests": [
                        {"check": "Vehicle('Car').summary()", "expected": "Car has 4 wheels"},
                        {"edge": "subclass with its own __init__", "check": "Truck('Big', 10).name", "expected": "Big"},
                        {"check": "Bike('BMX').summary()", "expected": "BMX has 2 wheels"},
                        {"check": "Truck('Big', 10).summary()", "expected": "Big has 6 wheels"},
                        {"check": "Truck('Big', 10).load", "expected": 10},
                        {"check": "Bike('BMX').wheels()", "expected": 2},
                    ],
                    "hints": [
                        "Look at what summary returned in the first test - the text in the middle is not a number. And the second test says a Truck has no name.",
                        "One bug is about using a method without calling it. The other is about a subclass that has its own __init__.",
                        "`self.wheels` is the method; `self.wheels()` is its result. When a subclass defines __init__, the parent's __init__ only runs if you call it with super().",
                        "Structure: in summary, call self.wheels() with brackets. In Truck.__init__, start with super().__init__(name), then store the load.",
                    ],
                    "questions": [
                        "Why does Bike need no __init__ of its own, but Truck does?",
                        "Which quiz question in the lesson showed the same two bugs?",
                    ],
                },
                {
                    "id": "shapes",
                    "title": "Shapes",
                    "difficulty": "medium",
                    "description": "Write a class Shape created with a name (attribute name); its area() returns 0 and its describe() returns text like \"square with area 9\". Square is a Shape created with a side length: its name is \"square\" and its area is side times side. Triangle is a Shape created with a base and a height: its name is \"triangle\" and its area is base times height divided by 2. Finally, write a function total_area(shapes) that returns the sum of the areas of a list of shapes.",
                    "starter": "class Shape:\n    pass\n\n\nclass Square(Shape):\n    pass\n\n\nclass Triangle(Shape):\n    pass\n\n\ndef total_area(shapes):\n    pass\n",
                    "requires": ["Shape", "Square", "Triangle", "total_area"],
                    "compare": "exact",
                    "tests": [
                        {"check": "Square(3).area()", "expected": 9},
                        {"check": "total_area([Square(2), Triangle(4, 5), Square(1)])", "expected": 15.0},
                        {"check": "Triangle(4, 5).area()", "expected": 10.0},
                        {"check": "[Square(2).name, Triangle(1, 1).name]", "expected": ["square", "triangle"]},
                        {"edge": "the base class itself", "check": "Shape('blob').area()", "expected": 0},
                        {"check": "Square(3).describe()", "expected": "square with area 9"},
                        {"check": "isinstance(Triangle(1, 1), Shape)", "expected": True},
                        {"edge": "empty input", "check": "total_area([])", "expected": 0},
                    ],
                    "hints": [
                        "Shape holds what every shape shares: a name, and a describe that works for any shape. Each subclass knows its own measurements and its own area formula.",
                        "The subclasses need their own __init__, because they are created with measurements rather than a name. They still have to give Shape its name.",
                        "`super().__init__(\"square\")` runs Shape's __init__ with a fixed name; then store the measurements on self. total_area just calls .area() on every shape - it never needs to know which kind each one is.",
                        "Structure: Shape.__init__ stores name; Shape.area returns 0; Shape.describe returns an f-string using self.name and self.area(). Square.__init__(self, side) calls super().__init__ with \"square\" and stores side; its area returns side * side. Triangle is the same idea with base and height. total_area adds up shape.area() in a loop.",
                    ],
                    "questions": [
                        "Why does total_area need no if statements about shape types?",
                        "What goes wrong if Square.__init__ forgets to call super().__init__?",
                    ],
                },
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "oop-data-structures",
            "title": "Building Data Structures",
            "summary": "Use classes to build a stack and a queue - your bridge into data structures and algorithms.",
            "lesson": [
                {
                    "heading": "A data structure is a class with rules",
                    "text": "A data structure stores items and controls how they go in and come out. You already use Python's built-in ones (list, dict, set). Writing your own is the best way to understand them - and a class is the natural tool: the storage is an attribute, and the allowed operations are the methods.",
                },
                {
                    "heading": "Stack: last in, first out",
                    "text": "A stack works like a pile of plates: you add to the top and take from the top. The last item pushed is the first one popped. Undo history and the browser's back button are stacks.",
                    "code": "push 1, push 2, push 3\npop  -> 3\npop  -> 2",
                },
                {
                    "heading": "Queue: first in, first out",
                    "text": "A queue works like a line at a shop: you join at the back and leave from the front. The first item added is the first one removed.",
                    "code": "enqueue 1, enqueue 2, enqueue 3\ndequeue -> 1\ndequeue -> 2",
                },
                {
                    "heading": "Interface and implementation",
                    "text": "Users of your class only see its methods (the interface). How you store the items inside (the implementation) is your private business - here, a plain list kept in an attribute. A list's `append` adds to the end, `pop()` removes from the end, and `pop(0)` removes from the front.",
                    "code": "items = [1, 2, 3]\nitems.pop()       # 3, items is [1, 2]\nitems.pop(0)      # 1, items is [2]",
                },
                {
                    "heading": "__len__ and empty structures",
                    "text": "Define `__len__` and Python's `len(obj)` works on your objects. Decide what happens when someone removes from an empty structure: the convention is to raise IndexError, just as a list does.",
                    "code": "    def __len__(self):\n        return len(self.items)",
                },
                {
                    "heading": "The pattern, in full",
                    "text": "Here is the whole pattern in a small class that is not a stack or a queue. Read it until each line makes sense: the storage is created once in `__init__`, every method works through `self.pages`, and the method that cannot work on an empty list raises an error with a message.",
                    "code": "class History:\n    def __init__(self):\n        self.pages = []                  # the storage\n\n    def visit(self, page):\n        self.pages.append(page)\n\n    def current(self):\n        if len(self.pages) == 0:\n            raise IndexError(\"no pages visited yet\")\n        return self.pages[-1]\n\n    def __len__(self):\n        return len(self.pages)",
                },
            ],
            "quiz": [
                {
                    "question": "What is the value of the last line?",
                    "code": "q = []\nq.append(\"a\")\nq.append(\"b\")\nq.append(\"c\")\nfirst = q.pop(0)\nlast = q.pop()\n[first, last, q]",
                    "answer": "`['a', 'c', ['b']]`. pop(0) takes from the front (queue order), pop() takes from the end (stack order).",
                },
                {
                    "question": "What is `s` at the end?",
                    "code": "s = []\ns.append(1)\ns.append(2)\ns.pop()\ns.append(3)\ns.append(4)\ns.pop()",
                    "answer": "`[1, 3]`. Push 1, push 2, pop 2, push 3, push 4, pop 4.",
                },
                {
                    "question": "What happens here?",
                    "code": "items = []\nitems.pop()",
                    "answer": "`IndexError: pop from empty list`. That is why a Stack's pop on an empty stack raises IndexError for free if it uses a list.",
                },
            ],
            "problems": [
                {
                    "id": "stack-class",
                    "title": "Stack",
                    "difficulty": "easy",
                    "description": "Write a class Stack. push(item) puts an item on top. pop() removes and returns the top item. peek() returns the top item without removing it. is_empty() returns True when the stack holds nothing, and len(stack) gives the number of items. pop() and peek() raise IndexError on an empty stack.",
                    "starter": (
                        "class Stack:\n"
                        "    def __init__(self):\n"
                        "        pass\n"
                        "\n"
                        "    def push(self, item):\n"
                        "        pass\n"
                        "\n"
                        "    def pop(self):\n"
                        "        pass\n"
                        "\n"
                        "    def peek(self):\n"
                        "        pass\n"
                        "\n"
                        "    def is_empty(self):\n"
                        "        pass\n"
                        "\n"
                        "    def __len__(self):\n"
                        "        pass\n"
                    ),
                    "requires": ["Stack"],
                    "compare": "exact",
                    "tests": [
                        {"setup": "s = Stack()\ns.push(1)\ns.push(2)\ns.push(3)", "check": "[s.pop(), s.pop()]", "expected": [3, 2]},
                        {"setup": "s = Stack()", "check": "s.pop()", "raises": "IndexError"},
                        {"edge": "brand-new object", "check": "Stack().is_empty()", "expected": True},
                        {"setup": "s = Stack()\ns.push('a')", "check": "s.is_empty()", "expected": False},
                        {"setup": "s = Stack()\ns.push(1)\ns.push(2)", "check": "[s.peek(), len(s)]", "expected": [2, 2]},
                        {"setup": "s = Stack()\ns.push(1)\ns.push(2)\ns.pop()", "check": "len(s)", "expected": 1},
                        {"edge": "empty structure", "check": "len(Stack())", "expected": 0},
                        {"setup": "s = Stack()", "check": "s.peek()", "raises": "IndexError"},
                        {"edge": "emptied again", "setup": "s = Stack()\ns.push(1)\ns.pop()", "check": "s.is_empty()", "expected": True},
                    ],
                    "hints": [
                        "The stack needs somewhere to keep its items in order. Which built-in type keeps things in order and lets you add and remove at one end?",
                        "Keep a list in an attribute. Decide which end of the list is the 'top' - one end is much more convenient than the other.",
                        "Treat the end of the list as the top: append adds there, pop() removes from there, and index -1 reads it. Popping or indexing an empty list already raises IndexError.",
                        "Structure: __init__ creates self.items as an empty list; push appends; pop returns self.items.pop(); peek returns the item at index -1; is_empty compares the length with 0; __len__ returns the length of the list.",
                    ],
                    "questions": [
                        "Why is the end of the list a better 'top' than the start?",
                        "peek and pop both read the top. What is the one difference?",
                    ],
                },
                {
                    "id": "queue-class",
                    "title": "Queue",
                    "difficulty": "easy",
                    "description": "Write a class Queue. enqueue(item) adds an item at the back. dequeue() removes and returns the item at the front, and raises IndexError if the queue is empty. is_empty() returns True when the queue holds nothing, and len(queue) gives the number of items.",
                    "starter": "class Queue:\n    pass\n",
                    "requires": ["Queue"],
                    "compare": "exact",
                    "tests": [
                        {"setup": "q = Queue()\nq.enqueue(1)\nq.enqueue(2)\nq.enqueue(3)", "check": "[q.dequeue(), q.dequeue()]", "expected": [1, 2]},
                        {"setup": "q = Queue()", "check": "q.dequeue()", "raises": "IndexError"},
                        {"edge": "brand-new object", "check": "Queue().is_empty()", "expected": True},
                        {"setup": "q = Queue()\nq.enqueue('a')", "check": "[q.is_empty(), len(q)]", "expected": [False, 1]},
                        {"edge": "reused after emptying", "setup": "q = Queue()\nq.enqueue(1)\nq.dequeue()\nq.enqueue(2)", "check": "q.dequeue()", "expected": 2},
                        {"edge": "emptied again", "setup": "q = Queue()\nq.enqueue(1)\nq.dequeue()", "check": "q.is_empty()", "expected": True},
                        {"edge": "empty structure", "check": "len(Queue())", "expected": 0},
                    ],
                    "hints": [
                        "A queue is almost a stack. The only difference is which end the items leave from.",
                        "Keep a list in an attribute again. Items join at one end and leave from the opposite end.",
                        "append adds at the back. `pop(0)` removes and returns the item at the front, and raises IndexError on an empty list.",
                        "Structure: __init__ creates self.items as an empty list; enqueue appends; dequeue returns self.items.pop(0); is_empty compares the length with 0; __len__ returns the length.",
                    ],
                    "questions": [
                        "After pop(0), every remaining item shifts one place. What does that cost for a long queue?",
                        "Where have you met queues in everyday software?",
                    ],
                },
                {
                    "id": "text-editor",
                    "title": "Text Editor with Undo",
                    "difficulty": "medium",
                    "description": "Write a class TextEditor. Its attribute text is the current text and starts as an empty string. write(s) adds s to the end of the text. undo() reverts the most recent write() that has not been undone yet; with nothing left to undo it does nothing.",
                    "starter": "class TextEditor:\n    pass\n",
                    "requires": ["TextEditor"],
                    "compare": "exact",
                    "tests": [
                        {"setup": "e = TextEditor()\ne.write('Hello')\ne.write(' world')\ne.undo()", "check": "e.text", "expected": "Hello"},
                        {"setup": "e = TextEditor()\ne.write('a')\ne.write('b')\ne.write('c')\ne.undo()\ne.undo()", "check": "e.text", "expected": "a"},
                        {"edge": "brand-new object", "check": "TextEditor().text", "expected": ""},
                        {"edge": "nothing to undo", "setup": "e = TextEditor()\ne.undo()", "check": "e.text", "expected": ""},
                        {"edge": "undo past the start", "setup": "e = TextEditor()\ne.write('x')\ne.undo()\ne.undo()", "check": "e.text", "expected": ""},
                        {"edge": "write after undo", "setup": "e = TextEditor()\ne.write('ab')\ne.undo()\ne.write('cd')", "check": "e.text", "expected": "cd"},
                        {"setup": "e = TextEditor()\ne.write('1')\ne.write('2')\ne.undo()\ne.write('3')", "check": "e.text", "expected": "13"},
                    ],
                    "hints": [
                        "To undo, the editor must remember what the text looked like before each write. Several undos in a row go back further and further - the most recent change is undone first.",
                        "'Most recent first' is last in, first out: a stack. Keep a list of earlier versions of the text alongside the text itself.",
                        "In write, push the current text onto the history list before changing it. In undo, if the history is not empty, pop the last saved version and make it the text.",
                        "Structure: __init__: self.text = \"\" and self.history = []. write: append self.text to history, then add s to self.text. undo: if history is not empty, set self.text to history.pop().",
                    ],
                    "questions": [
                        "Why is a stack the right structure here and not a queue?",
                        "How would you add redo()?",
                    ],
                },
            ],
        },
    ],
}
