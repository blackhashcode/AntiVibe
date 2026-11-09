"""C++ track 2: Object-Oriented Programming in C++."""
from languages import CPP_HEADER
from porting import port


def starter(body):
    return CPP_HEADER + "\n" + body.strip("\n") + "\n"


TRACK = {
    "id": "cpp-oop",
    "title": "Object-Oriented C++",
    "description": "Classes, encapsulation, operators, inheritance with virtual functions, and your own data structures.",
    "milestones": [
        # ------------------------------------------------------------------
        {
            "id": "cpp-classes",
            "title": "Classes & Objects",
            "summary": "Define a class with private data and public member functions, and create objects from it.",
            "lesson": [
                {
                    "heading": "A class in C++",
                    "text": "A class bundles data (member variables) with the functions that work on it (member functions). Members under `public:` can be used by anyone; members under `private:` only by the class's own functions. The usual design keeps the data private and offers public functions - so the class decides what is allowed to happen to its data. Note the `;` after the closing brace of a class.",
                    "code": "class Counter {\npublic:\n    void increment() {\n        count_++;\n    }\n    int count() const {\n        return count_;\n    }\nprivate:\n    int count_ = 0;     // every Counter starts at 0\n};",
                },
                {
                    "heading": "Creating and using objects",
                    "text": "`Counter c;` creates an object; `c.increment()` calls a member function on it. Each object has its own copy of the member variables. There is no `self`: inside a member function, the members are simply in scope (and `this` points at the current object if you need it).",
                    "code": "Counter a;\nCounter b;\na.increment();\na.count();     // 1\nb.count();     // 0",
                },
                {
                    "heading": "Constructors",
                    "text": "A constructor has the class's name and no return type, and runs when an object is created. The member initializer list after the `:` sets the members before the body runs - the preferred way to initialise them.",
                    "code": "class Rectangle {\npublic:\n    Rectangle(double width, double height) : width_(width), height_(height) {}\n    double area() const {\n        return width_ * height_;\n    }\nprivate:\n    double width_;\n    double height_;\n};\n\nRectangle r(3, 4);\nr.area();      // 12",
                },
                {
                    "heading": "const member functions",
                    "text": "`const` after a member function's brackets promises it does not change the object. Functions that only read (getters, area, count) should be const. The compiler enforces the promise - and only const functions can be called on a const object.",
                },
                {
                    "heading": "Naming members",
                    "text": "Many C++ programmers end member variable names with `_` (`count_`, `width_`). It is not required, but it prevents a classic bug: a parameter with the same name as a member hides the member, so `width = width;` assigns the parameter to itself and the member never changes.",
                },
                {
                    "heading": "Members can be containers",
                    "text": "A member variable can be a vector or a map. Every object gets its own, and the member functions use it like any other variable - this is how most data structures are built.",
                    "code": "class Shelf {\npublic:\n    void add(const string& title) {\n        books_.push_back(title);\n    }\n    int count() const {\n        return books_.size();\n    }\nprivate:\n    vector<string> books_;\n};",
                },
            ],
            "quiz": [
                {
                    "question": "What are `a.count()` and `b.count()`?",
                    "code": "Counter a;\nCounter b = a;\na.increment();",
                    "answer": "`1` and `0`. `Counter b = a;` makes b a separate copy of a - objects, like vectors, are copied in C++.",
                },
                {
                    "question": "What does `t.get()` return?",
                    "code": "class Box {\npublic:\n    void set(int value) {\n        int value_ = value;\n    }\n    int get() const {\n        return value_;\n    }\nprivate:\n    int value_ = 0;\n};\n\nBox t;\nt.set(5);",
                    "answer": "`0`. `int value_ = value;` declares a new local variable that hides the member; the member is never changed. It should be `value_ = value;`.",
                },
                {
                    "question": "Why does this not compile?",
                    "code": "class Coin {\npublic:\n    int value() const {\n        value_++;\n        return value_;\n    }\nprivate:\n    int value_ = 1;\n};",
                    "answer": "`value()` is marked const, which promises not to change the object, but `value_++` changes it.",
                },
            ],
            "problems": [
                port(
                    "counter-class",
                    description="Write a class Counter. A new counter's count() is 0. increment() raises the count by one and reset() sets it back to 0.",
                    starter=starter("""
class Counter {
public:
    void increment() {
    }

    void reset() {
    }

    int count() const {
        return 0;
    }

private:
    // add a member variable for the count
};
"""),
                    tests=[
                        {"setup": "Counter c;\nc.increment();\nc.increment();", "check": "c.count()", "expected": 2},
                        {"setup": "Counter c;\nfor (int i = 0; i < 5; i++) c.increment();", "check": "c.count()", "expected": 5},
                        {"edge": "brand-new object", "check": "Counter().count()", "expected": 0},
                        {"setup": "Counter c;\nc.increment();\nc.reset();", "check": "c.count()", "expected": 0},
                        {"edge": "two separate objects", "setup": "Counter a;\nCounter b;\na.increment();", "check": "vector<int>{a.count(), b.count()}", "expected": [1, 0]},
                    ],
                    hints=[
                        "A counter remembers one number between calls. Where can an object keep a value that all its member functions can reach?",
                        "Add a private member variable, give it a starting value, and change it in the member functions.",
                        "int count_ = 0; under private: starts every Counter at 0. increment does count_++, reset sets it to 0, count() returns it.",
                        "Structure: private: int count_ = 0; increment: count_++; reset: count_ = 0; count: return count_;",
                    ],
                    questions=[
                        "Why do two Counter objects not share their count?",
                        "Why is count() marked const but increment() is not?",
                    ],
                ),
                {
                    "id": "thermostat",
                    "title": "Debug: Thermostat",
                    "difficulty": "easy",
                    "description": "A Thermostat starts at a target of 20 degrees, set_target(t) changes the target, and target() returns it. Neither part works. Both bugs are a name hiding the member variable.",
                    "starter": starter("""
class Thermostat {
public:
    Thermostat() {
        int target_ = 20;
    }

    void set_target(int target_) {
        target_ = target_;
    }

    int target() const {
        return target_;
    }

private:
    int target_ = 0;
};
"""),
                    "compare": "exact",
                    "tests": [
                        {"edge": "brand-new object", "check": "Thermostat().target()", "expected": 20},
                        {"setup": "Thermostat t;\nt.set_target(25);", "check": "t.target()", "expected": 25},
                        {"setup": "Thermostat t;\nt.set_target(25);\nt.set_target(18);", "check": "t.target()", "expected": 18},
                        {"edge": "two separate objects", "setup": "Thermostat a;\nThermostat b;\na.set_target(30);", "check": "vector<int>{a.target(), b.target()}", "expected": [30, 20]},
                    ] + [
                        {"setup": "Thermostat t;\nt.set_target(5);", "check": "t.target()", "expected": 5},
                    ],
                    "hints": [
                        "A new thermostat reports 0, not 20, and set_target changes nothing. Look for a name that is declared twice.",
                        "In the constructor, `int target_ = 20;` declares a brand-new local variable. In set_target, the parameter is called target_, the same as the member.",
                        "Inside set_target, `target_` means the parameter, so `target_ = target_;` copies the parameter onto itself. Rename the parameter (or write this->target_). In the constructor, drop the int so it assigns the member.",
                        "Structure: constructor body: target_ = 20; (or use an initializer list : target_(20)). set_target(int target) { target_ = target; }",
                    ],
                    "questions": [
                        "Why does the compiler accept `int target_ = 20;` inside the constructor?",
                        "How does the trailing-underscore naming habit prevent this bug?",
                    ],
                },
                port(
                    "rectangle-class",
                    description="Write a class Rectangle created with a width and a height. width() and height() return them, area() returns width times height, perimeter() returns the distance around the edge, is_square() returns true when width and height are equal, and set_width(w) changes the width.",
                    starter=starter("""
class Rectangle {
public:
    Rectangle(double width, double height) {
    }

    double width() const { return 0; }
    double height() const { return 0; }
    double area() const { return 0; }
    double perimeter() const { return 0; }
    bool is_square() const { return false; }

    void set_width(double width) {
    }

private:
    // the width and height
};
"""),
                    tests=[
                        {"check": "Rectangle(3, 4).area()", "expected": 12},
                        {"check": "Rectangle(3, 4).perimeter()", "expected": 14},
                        {"check": "Rectangle(3, 4).is_square()", "expected": False},
                        {"edge": "square", "check": "Rectangle(5, 5).is_square()", "expected": True},
                        {"setup": "Rectangle r(3, 4);", "check": "vector<double>{r.width(), r.height()}", "expected": [3, 4]},
                        {"edge": "changed after creation", "setup": "Rectangle r(3, 4);\nr.set_width(10);", "check": "r.area()", "expected": 40},
                        {"edge": "zero size", "check": "Rectangle(0, 5).area()", "expected": 0},
                    ],
                    hints=[
                        "The object has to remember the two numbers it was created with.",
                        "Add two private member variables and set them in the constructor - the initializer list is the neat way.",
                        "Compute area and perimeter from the members when they are called, so set_width is reflected automatically. Name members width_ and height_ so the parameters do not hide them.",
                        "Structure: Rectangle(double width, double height) : width_(width), height_(height) {} ; area returns width_ * height_; perimeter 2 * (width_ + height_); is_square width_ == height_; set_width assigns width_.",
                    ],
                    questions=[
                        "Why would storing the area in the constructor fail the set_width test?",
                        "What does the initializer list do that assigning in the body does not?",
                    ],
                ),
                port(
                    "playlist",
                    description="Write a class Playlist. A new playlist is empty. add(song) adds a title to the end, songs() returns the titles in order, count() returns how many there are, has(song) returns true if the title is in it, and remove(song) removes the first copy of that title - throwing invalid_argument if it is not there.",
                    starter=starter("""
class Playlist {
public:
    void add(const string& song) {
    }

    vector<string> songs() const {
        return {};
    }

    int count() const {
        return 0;
    }

    bool has(const string& song) const {
        return false;
    }

    void remove(const string& song) {
        // throw invalid_argument if the song is not in the playlist
    }

private:
    // store the songs here
};
"""),
                    tests=[
                        {"setup": "Playlist p;\np.add(\"Intro\");\np.add(\"Hello\");", "check": "p.songs()", "expected": ["Intro", "Hello"]},
                        {"setup": "Playlist p;\np.add(\"Intro\");\np.add(\"Hello\");", "check": "p.count()", "expected": 2},
                        {"edge": "brand-new object", "check": "Playlist().count()", "expected": 0},
                        {"setup": "Playlist p;\np.add(\"A\");", "check": "vector<bool>{p.has(\"A\"), p.has(\"B\")}", "expected": [True, False]},
                        {"edge": "duplicate titles", "setup": "Playlist p;\np.add(\"A\");\np.add(\"B\");\np.add(\"A\");\np.remove(\"A\");", "check": "p.songs()", "expected": ["B", "A"]},
                        {"setup": "Playlist p;", "check": "p.remove(\"X\")", "raises": "invalid_argument"},
                        {"edge": "two separate objects", "setup": "Playlist a;\nPlaylist b;\na.add(\"A\");", "check": "b.songs()", "expected": []},
                    ],
                    hints=[
                        "The playlist remembers a sequence of titles. Which container keeps things in order?",
                        "Keep a private vector<string> member. Every member function is a short use of that vector.",
                        "push_back adds; size() counts; std::find(songs_.begin(), songs_.end(), song) finds a title and returns songs_.end() if it is missing; erase(iterator) removes it.",
                        "Structure: private: vector<string> songs_; add: push_back; songs: return songs_; count: return songs_.size(); has: find(...) != end; remove: auto it = find(...); if (it == end) throw invalid_argument(...); songs_.erase(it);",
                    ],
                    questions=[
                        "Why does songs() return a copy of the vector, and why is that safe?",
                        "What would go wrong if remove erased without checking?",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-encapsulation",
            "title": "Encapsulation & Operators",
            "summary": "Keep objects valid, give them operators like ==, and return new objects.",
            "lesson": [
                {
                    "heading": "Objects guard their own data",
                    "text": "Because the data is private, the only way to change it is through the member functions - so they can check every change. Validate first, change second: if a function throws halfway through, the object should be exactly as it was.",
                    "code": "class Thermostat {\npublic:\n    void set_target(int degrees) {\n        if (degrees < 5 || degrees > 30) {\n            throw invalid_argument(\"target must be between 5 and 30\");\n        }\n        target_ = degrees;\n    }\nprivate:\n    int target_ = 20;\n};",
                },
                {
                    "heading": "Operators",
                    "text": "C++ lets a class define what operators mean for its objects. `bool operator==(const Point& other) const` makes `a == b` work. Without it, `==` between two of your objects does not even compile.",
                    "code": "class Money {\npublic:\n    explicit Money(int cents) : cents_(cents) {}\n    bool operator==(const Money& other) const {\n        return cents_ == other.cents_;\n    }\nprivate:\n    int cents_;\n};",
                },
                {
                    "heading": "Turning an object into text",
                    "text": "There is no `__str__`. A common approach is a member function that builds a string - here called `str()`. (If you call a member function `to_string`, remember to write `std::to_string` inside the class, or the member function hides the standard one.)",
                },
                {
                    "heading": "Returning new objects",
                    "text": "A const member function can build and return a new object of its own class, leaving the original untouched.",
                    "code": "Money doubled() const {\n    return Money(cents_ * 2);\n}",
                },
                {
                    "heading": "Maps as members",
                    "text": "A const member function cannot use `m[key]` on a map member, because `[]` may insert a key - which would change the object. Use `m.count(key)`, `m.find(key)` or `m.at(key)` in const functions.",
                },
            ],
            "quiz": [
                {
                    "question": "What is `a.balance()` at the end?",
                    "code": "class Account {\npublic:\n    void withdraw(int amount) {\n        balance_ -= amount;\n        if (balance_ < 0) throw invalid_argument(\"not enough money\");\n    }\n    int balance() const { return balance_; }\nprivate:\n    int balance_ = 10;\n};\n\nAccount a;\ntry { a.withdraw(50); } catch (const invalid_argument&) {}",
                    "answer": "`-40`. The balance was changed before the check. Check first, then change.",
                },
                {
                    "question": "Why does this not compile?",
                    "code": "class Stock {\npublic:\n    int quantity(const string& item) const {\n        return stock_[item];\n    }\nprivate:\n    map<string, int> stock_;\n};",
                    "answer": "quantity is const, but `stock_[item]` may insert a missing key, which would change the object. Use count/find/at instead.",
                },
            ],
            "problems": [
                port(
                    "bank-account",
                    description="Write a class BankAccount created with an owner and an optional starting balance (default 0). owner() and balance() return them. deposit(amount) adds to the balance and withdraw(amount) subtracts from it. Both throw invalid_argument if amount is not positive, and withdraw also throws invalid_argument if amount is more than the balance. A failed call must leave the balance unchanged.",
                    starter=starter("""
class BankAccount {
public:
    BankAccount(const string& owner, double balance = 0) {
    }

    string owner() const { return ""; }
    double balance() const { return 0; }

    void deposit(double amount) {
    }

    void withdraw(double amount) {
    }

private:
};
"""),
                    tests=[
                        {"setup": "BankAccount a(\"Ann\", 100);\na.deposit(50);", "check": "a.balance()", "expected": 150},
                        {"setup": "BankAccount a(\"Ann\", 100);", "check": "a.withdraw(500)", "raises": "invalid_argument"},
                        {"edge": "default argument", "check": "BankAccount(\"Ann\").balance()", "expected": 0},
                        {"check": "BankAccount(\"Ann\", 100).owner()", "expected": "Ann"},
                        {"setup": "BankAccount a(\"Ann\", 100);\na.withdraw(30);", "check": "a.balance()", "expected": 70},
                        {"edge": "withdraw everything", "setup": "BankAccount a(\"Ann\", 100);\na.withdraw(100);", "check": "a.balance()", "expected": 0},
                        {"setup": "BankAccount a(\"Ann\", 100);", "check": "a.deposit(-5)", "raises": "invalid_argument"},
                        {"setup": "BankAccount a(\"Ann\", 100);", "check": "a.withdraw(0)", "raises": "invalid_argument"},
                        {"edge": "failed call leaves state unchanged", "setup": "BankAccount a(\"Ann\", 100);\ntry {\n    a.withdraw(500);\n} catch (const invalid_argument&) {\n}", "check": "a.balance()", "expected": 100},
                    ],
                    hints=[
                        "The account remembers two things and has two actions, each with rules about which amounts are allowed.",
                        "Store owner_ and balance_ as private members, set by the constructor. Each action: check the rules, then change the balance.",
                        "Throw before touching balance_, so a rejected call changes nothing: throw invalid_argument(\"...\");",
                        "Structure: constructor initializer list sets both members; deposit: if (amount <= 0) throw; balance_ += amount; withdraw: if (amount <= 0 || amount > balance_) throw; balance_ -= amount;",
                    ],
                    questions=[
                        "How does making balance_ private stop other code from setting it to -50?",
                        "Why must the checks come before the change?",
                    ],
                ),
                port(
                    "point-class",
                    description="Write a class Point with x() and y(). str() returns text like \"(1, 2)\". Two points are == when their x and y match. translate(dx, dy) returns a new Point moved by that amount and leaves the original unchanged.",
                    starter=starter("""
class Point {
public:
    Point(int x, int y) {
    }

    int x() const { return 0; }
    int y() const { return 0; }

    string str() const {
        return "";
    }

    bool operator==(const Point& other) const {
        return false;
    }

    Point translate(int dx, int dy) const {
        return Point(0, 0);
    }

private:
};
"""),
                    tests=[
                        {"check": "Point(1, 2).str()", "expected": "(1, 2)"},
                        {"check": "Point(1, 2) == Point(1, 2)", "expected": True},
                        {"check": "Point(1, 2) == Point(2, 1)", "expected": False},
                        {"edge": "negative numbers", "check": "Point(-1, 0).str()", "expected": "(-1, 0)"},
                        {"check": "Point(1, 2).translate(3, -1).str()", "expected": "(4, 1)"},
                        {"edge": "original must not change", "setup": "Point p(1, 2);\nPoint q = p.translate(1, 1);", "check": "vector<int>{p.x(), p.y(), q.x(), q.y()}", "expected": [1, 2, 2, 3]},
                    ],
                    hints=[
                        "Three behaviours: turning a point into text, comparing two points, and making a moved copy.",
                        "Store x_ and y_. str builds a string with to_string; operator== compares both coordinates with other's; translate constructs a new Point.",
                        "Inside operator==, you can read other.x_ directly - private means private to the class, not to the object.",
                        "Structure: str: return \"(\" + to_string(x_) + \", \" + to_string(y_) + \")\"; operator==: return x_ == other.x_ && y_ == other.y_; translate: return Point(x_ + dx, y_ + dy);",
                    ],
                    questions=[
                        "Why is translate const?",
                        "Why can operator== read other.x_ even though it is private?",
                    ],
                ),
                port(
                    "inventory",
                    description="Write a class Inventory that tracks how many of each item is in stock, using a map member. add(item, qty) adds qty units, remove(item, qty) takes qty away, quantity(item) returns the stock (0 for an item never added) and total() returns all units together. add and remove throw invalid_argument if qty is not positive, and remove also throws invalid_argument if fewer than qty are in stock - leaving the stock unchanged.",
                    starter=starter("""
class Inventory {
public:
    void add(const string& item, int qty) {
    }

    void remove(const string& item, int qty) {
    }

    int quantity(const string& item) const {
        return 0;
    }

    int total() const {
        return 0;
    }

private:
};
"""),
                    tests=[
                        {"setup": "Inventory inv;\ninv.add(\"apple\", 5);\ninv.add(\"apple\", 3);", "check": "inv.quantity(\"apple\")", "expected": 8},
                        {"setup": "Inventory inv;\ninv.add(\"apple\", 2);", "check": "inv.remove(\"apple\", 5)", "raises": "invalid_argument"},
                        {"edge": "unknown item", "check": "Inventory().quantity(\"pear\")", "expected": 0},
                        {"setup": "Inventory inv;\ninv.add(\"a\", 2);\ninv.add(\"b\", 3);", "check": "inv.total()", "expected": 5},
                        {"setup": "Inventory inv;\ninv.add(\"a\", 4);\ninv.remove(\"a\", 1);", "check": "inv.quantity(\"a\")", "expected": 3},
                        {"setup": "Inventory inv;", "check": "inv.add(\"a\", 0)", "raises": "invalid_argument"},
                        {"edge": "failed call leaves state unchanged", "setup": "Inventory inv;\ninv.add(\"a\", 2);\ntry {\n    inv.remove(\"a\", 3);\n} catch (const invalid_argument&) {\n}", "check": "inv.quantity(\"a\")", "expected": 2},
                        {"setup": "Inventory inv;", "check": "inv.remove(\"ghost\", 1)", "raises": "invalid_argument"},
                        {"edge": "brand-new object", "check": "Inventory().total()", "expected": 0},
                    ],
                    hints=[
                        "Bank Account with one balance per item. What maps a name to a number?",
                        "Keep a private map<string, int> stock_. Adding is the counting pattern: stock_[item] += qty.",
                        "quantity and total are const, so they cannot use stock_[item]. Use stock_.count(item) and stock_.at(item), or find. remove can call quantity(item) for its check.",
                        "Structure: add: if (qty <= 0) throw; stock_[item] += qty; remove: if (qty <= 0 || quantity(item) < qty) throw; stock_[item] -= qty; quantity: return stock_.count(item) ? stock_.at(item) : 0; total: loop over the map adding the values.",
                    ],
                    questions=[
                        "Why does stock_[item] not compile inside quantity()?",
                        "Should an item with quantity 0 stay in the map?",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-inheritance",
            "title": "Inheritance & Virtual Functions",
            "summary": "Build specialised classes on general ones, and make the right version of a function run.",
            "lesson": [
                {
                    "heading": "Inheritance",
                    "text": "`class Dog : public Animal` makes Dog a kind of Animal: it gets Animal's members and can add its own. A subclass's constructor must hand the base class what it needs, in the initializer list.",
                    "code": "class Animal {\npublic:\n    Animal(const string& name) : name_(name) {}\n    string name() const { return name_; }\nprivate:\n    string name_;\n};\n\nclass Dog : public Animal {\npublic:\n    Dog(const string& name) : Animal(name) {}\n};",
                },
                {
                    "heading": "virtual: letting the subclass decide",
                    "text": "This is the biggest difference from Python. In Python, `self.speak()` always runs the object's own version. In C++ that only happens if the base class marks the function `virtual`. Without `virtual`, a call made inside Animal - or through an `Animal*` or `Animal&` - runs Animal's version even when the object is a Dog. Mark the subclass's version `override`, and the compiler checks that it really overrides something.",
                    "code": "class Animal {\npublic:\n    virtual string speak() const { return \"Some sound\"; }\n    string describe() const { return \"It says \" + speak(); }\n    virtual ~Animal() = default;\n};\n\nclass Dog : public Animal {\npublic:\n    string speak() const override { return \"Woof\"; }\n};\n\nDog d;\nd.describe();     // \"It says Woof\" - only because speak is virtual",
                },
                {
                    "heading": "Polymorphism through pointers",
                    "text": "To keep different kinds of objects in one collection and have each answer in its own way, store pointers (`vector<Animal*>`) or references to the base class. Storing the objects themselves in a `vector<Animal>` would copy only their Animal part - this is called slicing, and the Dog-ness is lost.",
                    "code": "Dog d;\nCat c;\nvector<Animal*> pets = {&d, &c};\nfor (Animal* pet : pets) {\n    pet->speak();       // -> calls a member through a pointer\n}",
                },
                {
                    "heading": "virtual destructor",
                    "text": "A class meant to be used through base-class pointers should have `virtual ~Base() = default;` so that deleting through a base pointer cleans up the whole object. Make it a habit whenever a class has virtual functions.",
                },
            ],
            "quiz": [
                {
                    "question": "What does `B().greet()` return?",
                    "code": "class A {\npublic:\n    string hello() const { return \"A\"; }\n    string greet() const { return \"I am \" + hello(); }\n};\n\nclass B : public A {\npublic:\n    string hello() const { return \"B\"; }\n};",
                    "answer": "`\"I am A\"`. hello is not virtual, so the call inside A's greet is fixed to A's version. With `virtual` in A it would be \"I am B\".",
                },
                {
                    "question": "What is `p->sound()`?",
                    "code": "class Animal {\npublic:\n    virtual string sound() const { return \"...\"; }\n};\nclass Cow : public Animal {\npublic:\n    string sound() const override { return \"Moo\"; }\n};\n\nCow cow;\nAnimal* p = &cow;",
                    "answer": "`\"Moo\"`. sound is virtual, so the call through the Animal pointer runs the Cow version.",
                },
                {
                    "question": "What is `zoo[0].sound()`?",
                    "code": "vector<Animal> zoo;\nzoo.push_back(Cow());",
                    "answer": "`\"...\"`. Pushing a Cow into a vector<Animal> copies only its Animal part (slicing). Use a vector<Animal*> to keep polymorphism.",
                },
            ],
            "problems": [
                port(
                    "animal-sounds",
                    description="Animal is created with a name. name() returns it, speak() returns \"Some sound\", and describe() returns text like \"Rex says Woof\" built from the name and whatever speak() returns. Dog and Cat are Animals whose speak() returns \"Woof\" and \"Meow\". Dog and Cat must not need their own describe() - and calls through an Animal pointer must still speak correctly.",
                    starter=starter("""
class Animal {
public:
    Animal(const string& name) {
    }

    string name() const { return ""; }
    string speak() const { return ""; }
    string describe() const { return ""; }
};

class Dog : public Animal {
public:
    Dog(const string& name) : Animal(name) {}
};

class Cat : public Animal {
public:
    Cat(const string& name) : Animal(name) {}
};
"""),
                    tests=[
                        {"check": "Dog(\"Rex\").speak()", "expected": "Woof"},
                        {"check": "Cat(\"Tom\").describe()", "expected": "Tom says Meow"},
                        {"check": "Dog(\"Rex\").describe()", "expected": "Rex says Woof"},
                        {"edge": "the base class itself", "check": "Animal(\"Generic\").describe()", "expected": "Generic says Some sound"},
                        {"check": "Dog(\"Rex\").name()", "expected": "Rex"},
                        {"edge": "called through a base pointer", "setup": "Dog d(\"a\");\nCat c(\"b\");\nvector<Animal*> all = {&d, &c};", "check": "vector<string>{all[0]->speak(), all[1]->speak()}", "expected": ["Woof", "Meow"]},
                    ],
                    hints=[
                        "Everything the three classes share belongs in Animal. Dog and Cat only say what is different: the sound.",
                        "Store the name in Animal. Dog and Cat each override speak(). describe() in Animal calls speak().",
                        "describe() runs inside Animal, so it only reaches Dog's speak if speak is virtual in Animal. Mark the overrides with override.",
                        "Structure: Animal: private string name_ set in the constructor; virtual string speak() const { return \"Some sound\"; } describe returns name_ + \" says \" + speak(); virtual destructor. Dog/Cat: string speak() const override { return \"Woof\"; } (\"Meow\").",
                    ],
                    questions=[
                        "Which tests fail if you forget virtual, and why?",
                        "What would go wrong with a vector<Animal> instead of vector<Animal*>?",
                    ],
                ),
                {
                    "id": "vehicles",
                    "title": "Debug: Vehicles",
                    "difficulty": "easy",
                    "description": "summary() should give text like \"Car has 4 wheels\". A Bike has 2 wheels and a Truck has 6. Every vehicle claims to have 4 wheels in its summary. Find the one missing word.",
                    "starter": starter("""
class Vehicle {
public:
    Vehicle(const string& name) : name_(name) {}
    virtual ~Vehicle() = default;

    int wheels() const { return 4; }

    string summary() const {
        return name_ + " has " + to_string(wheels()) + " wheels";
    }

protected:
    string name_;
};

class Bike : public Vehicle {
public:
    Bike(const string& name) : Vehicle(name) {}
    int wheels() const { return 2; }
};

class Truck : public Vehicle {
public:
    Truck(const string& name, int load) : Vehicle(name), load_(load) {}
    int wheels() const { return 6; }
    int load() const { return load_; }

private:
    int load_;
};
"""),
                    "compare": "exact",
                    "tests": [
                        {"check": "Bike(\"BMX\").summary()", "expected": "BMX has 2 wheels"},
                        {"check": "Truck(\"Big\", 10).summary()", "expected": "Big has 6 wheels"},
                        {"check": "Vehicle(\"Car\").summary()", "expected": "Car has 4 wheels"},
                        {"check": "Bike(\"BMX\").wheels()", "expected": 2},
                        {"check": "Truck(\"Big\", 10).load()", "expected": 10},
                        {"edge": "called through a base pointer", "setup": "Truck t(\"Big\", 10);\nVehicle* v = &t;", "check": "v->wheels()", "expected": 6},
                    ],
                    "hints": [
                        "Bike(\"BMX\").wheels() gives 2 - so why does Bike's summary say 4?",
                        "summary() is written in Vehicle. Which version of wheels() does a call inside Vehicle reach?",
                        "Without virtual, a call made inside the base class is fixed to the base class's version at compile time.",
                        "Structure: mark wheels() virtual in Vehicle, and add override to the versions in Bike and Truck.",
                    ],
                    "questions": [
                        "Why did Bike(\"BMX\").wheels() pass even with the bug?",
                        "What does adding override to Bike::wheels() check for you?",
                    ],
                },
                port(
                    "shapes",
                    description="Shape is created with a name; name() returns it and area() returns 0. Square is a Shape created with a side length: its name is \"square\" and its area side * side. Triangle is created with a base and a height: its name is \"triangle\" and its area base * height / 2. total_area(shapes) returns the sum of the areas of a vector of Shape pointers.",
                    starter=starter("""
class Shape {
public:
    Shape(const string& name) {
    }

    string name() const { return ""; }
    double area() const { return 0; }
};

class Square : public Shape {
public:
    Square(double side) : Shape("square") {
    }
};

class Triangle : public Shape {
public:
    Triangle(double base, double height) : Shape("triangle") {
    }
};

double total_area(const vector<Shape*>& shapes) {
    return 0;
}
"""),
                    tests=[
                        {"check": "Square(3).area()", "expected": 9},
                        {"setup": "Square a(2);\nTriangle b(4, 5);\nSquare c(1);\nvector<Shape*> all = {&a, &b, &c};", "check": "total_area(all)", "expected": 15.0},
                        {"check": "Triangle(4, 5).area()", "expected": 10.0},
                        {"check": "vector<string>{Square(2).name(), Triangle(1, 1).name()}", "expected": ["square", "triangle"]},
                        {"edge": "the base class itself", "check": "Shape(\"blob\").area()", "expected": 0},
                        {"edge": "empty input", "check": "total_area(vector<Shape*>{})", "expected": 0},
                    ],
                    hints=[
                        "Shape holds what every shape shares: a name. Each subclass knows its own measurements and its own area formula.",
                        "The subclass constructors already pass the name to Shape; store the measurements as members of the subclass.",
                        "total_area only sees Shape pointers, so area must be virtual in Shape for each shape's own formula to run. Give Shape a virtual destructor too.",
                        "Structure: Shape: string name_; virtual double area() const { return 0; } virtual ~Shape() = default. Square: double side_; area() const override { return side_ * side_; } Triangle likewise. total_area: double total = 0; for (Shape* s : shapes) total += s->area(); return total;",
                    ],
                    questions=[
                        "Why does total_area take pointers instead of Shape objects?",
                        "Why does total_area need no if statements about shape types?",
                    ],
                ),
            ],
        },
        # ------------------------------------------------------------------
        {
            "id": "cpp-data-structures",
            "title": "Building Data Structures",
            "summary": "Write your own stack and queue classes - the bridge into data structures and algorithms.",
            "lesson": [
                {
                    "heading": "A data structure is a class with rules",
                    "text": "The storage is a private member - here a vector - and the public member functions are the only allowed ways in and out. Users of the class see the interface; how it is stored is the class's own business.",
                },
                {
                    "heading": "Stack and queue",
                    "text": "A stack is last in, first out: push onto the top, pop from the top. A queue is first in, first out: join at the back, leave from the front. With a vector, the end is the natural top of a stack (`push_back`, `back`, `pop_back`). Removing from the front of a vector with `erase(begin())` works for a queue but shifts every other item; a `deque` can remove from both ends cheaply.",
                },
                {
                    "heading": "Empty structures must throw",
                    "text": "`pop_back()` or `back()` on an empty vector is undefined behaviour in C++ - it does not raise an error for you the way Python's pop does. Your class has to check and throw `out_of_range` itself.",
                    "code": "class History {\npublic:\n    void visit(const string& page) {\n        pages_.push_back(page);\n    }\n    string current() const {\n        if (pages_.empty()) {\n            throw out_of_range(\"no pages visited yet\");\n        }\n        return pages_.back();\n    }\n    int size() const {\n        return pages_.size();\n    }\nprivate:\n    vector<string> pages_;\n};",
                },
                {
                    "heading": "The standard library has them too",
                    "text": "`std::stack`, `std::queue` and `std::deque` exist and you will use them in the DSA track. Writing your own once is how you learn what they do.",
                },
            ],
            "quiz": [
                {
                    "question": "What is `v` at the end?",
                    "code": "vector<int> v;\nv.push_back(1);\nv.push_back(2);\nv.pop_back();\nv.push_back(3);\nv.push_back(4);\nv.pop_back();",
                    "answer": "`{1, 3}`: push 1, push 2, pop 2, push 3, push 4, pop 4.",
                },
                {
                    "question": "What is the problem here?",
                    "code": "vector<int> v;\nint top = v.back();",
                    "answer": "back() on an empty vector is undefined behaviour - the program might crash or carry on with a garbage value. A stack class must check empty() first and throw.",
                },
            ],
            "problems": [
                port(
                    "stack-class",
                    description="Write a class Stack of ints. push(item) puts an item on top. pop() removes and returns the top item. peek() returns the top item without removing it. is_empty() and size() tell you what is in it. pop() and peek() throw out_of_range on an empty stack.",
                    starter=starter("""
class Stack {
public:
    void push(int item) {
    }

    int pop() {
        return 0;
    }

    int peek() const {
        return 0;
    }

    bool is_empty() const {
        return true;
    }

    int size() const {
        return 0;
    }

private:
};
"""),
                    tests=[
                        {"setup": "Stack s;\ns.push(1);\ns.push(2);\ns.push(3);", "check": "vector<int>{s.pop(), s.pop()}", "expected": [3, 2]},
                        {"setup": "Stack s;", "check": "s.pop()", "raises": "out_of_range"},
                        {"edge": "brand-new object", "check": "Stack().is_empty()", "expected": True},
                        {"setup": "Stack s;\ns.push(5);", "check": "s.is_empty()", "expected": False},
                        {"setup": "Stack s;\ns.push(1);\ns.push(2);", "check": "vector<int>{s.peek(), s.size()}", "expected": [2, 2]},
                        {"setup": "Stack s;\ns.push(1);\ns.push(2);\ns.pop();", "check": "s.size()", "expected": 1},
                        {"edge": "empty structure", "check": "Stack().size()", "expected": 0},
                        {"setup": "Stack s;", "check": "s.peek()", "raises": "out_of_range"},
                        {"edge": "emptied again", "setup": "Stack s;\ns.push(1);\ns.pop();", "check": "s.is_empty()", "expected": True},
                    ],
                    hints=[
                        "The stack keeps its items in order and adds and removes at one end. Which end of a vector is cheap to change?",
                        "Keep a private vector<int> items_ and treat its end as the top.",
                        "push_back adds to the top, back() reads it, pop_back() removes it - but pop_back returns nothing, so read back() first. Check empty() and throw out_of_range before touching an empty vector.",
                        "Structure: pop: if (items_.empty()) throw out_of_range(\"empty stack\"); int top = items_.back(); items_.pop_back(); return top; peek: same check, return back(); is_empty: items_.empty(); size: items_.size().",
                    ],
                    questions=[
                        "Why must pop read back() before calling pop_back()?",
                        "What could happen if pop did not check for an empty stack?",
                    ],
                ),
                port(
                    "queue-class",
                    description="Write a class Queue of ints. enqueue(item) adds an item at the back. dequeue() removes and returns the item at the front, and throws out_of_range if the queue is empty. is_empty() and size() tell you what is in it.",
                    starter=starter("""
class Queue {
public:
    void enqueue(int item) {
    }

    int dequeue() {
        return 0;
    }

    bool is_empty() const {
        return true;
    }

    int size() const {
        return 0;
    }

private:
};
"""),
                    tests=[
                        {"setup": "Queue q;\nq.enqueue(1);\nq.enqueue(2);\nq.enqueue(3);", "check": "vector<int>{q.dequeue(), q.dequeue()}", "expected": [1, 2]},
                        {"setup": "Queue q;", "check": "q.dequeue()", "raises": "out_of_range"},
                        {"edge": "brand-new object", "check": "Queue().is_empty()", "expected": True},
                        {"setup": "Queue q;\nq.enqueue(7);", "check": "vector<int>{q.is_empty(), q.size()}", "expected": [0, 1]},
                        {"edge": "reused after emptying", "setup": "Queue q;\nq.enqueue(1);\nq.dequeue();\nq.enqueue(2);", "check": "q.dequeue()", "expected": 2},
                        {"edge": "emptied again", "setup": "Queue q;\nq.enqueue(1);\nq.dequeue();", "check": "q.is_empty()", "expected": True},
                        {"edge": "empty structure", "check": "Queue().size()", "expected": 0},
                    ],
                    hints=[
                        "A queue is almost a stack - only the end the items leave from is different.",
                        "Keep a private container. Items join at the back and leave from the front.",
                        "With a vector: push_back to join, front() to read the first item, erase(items_.begin()) to remove it. A deque<int> has push_back, front and pop_front, which is cheaper.",
                        "Structure: dequeue: if (items_.empty()) throw out_of_range(\"empty queue\"); int first = items_.front(); remove the front; return first;",
                    ],
                    questions=[
                        "Why is erase(begin()) on a long vector slow?",
                        "What does deque do differently?",
                    ],
                ),
                port(
                    "text-editor",
                    description="Write a class TextEditor. text() returns the current text, which starts empty. write(s) adds s to the end. undo() reverts the most recent write() that has not been undone yet; with nothing left to undo it does nothing.",
                    starter=starter("""
class TextEditor {
public:
    string text() const {
        return "";
    }

    void write(const string& s) {
    }

    void undo() {
    }

private:
};
"""),
                    tests=[
                        {"setup": "TextEditor e;\ne.write(\"Hello\");\ne.write(\" world\");\ne.undo();", "check": "e.text()", "expected": "Hello"},
                        {"setup": "TextEditor e;\ne.write(\"a\");\ne.write(\"b\");\ne.write(\"c\");\ne.undo();\ne.undo();", "check": "e.text()", "expected": "a"},
                        {"edge": "brand-new object", "check": "TextEditor().text()", "expected": ""},
                        {"edge": "nothing to undo", "setup": "TextEditor e;\ne.undo();", "check": "e.text()", "expected": ""},
                        {"edge": "undo past the start", "setup": "TextEditor e;\ne.write(\"x\");\ne.undo();\ne.undo();", "check": "e.text()", "expected": ""},
                        {"edge": "write after undo", "setup": "TextEditor e;\ne.write(\"ab\");\ne.undo();\ne.write(\"cd\");", "check": "e.text()", "expected": "cd"},
                        {"setup": "TextEditor e;\ne.write(\"1\");\ne.write(\"2\");\ne.undo();\ne.write(\"3\");", "check": "e.text()", "expected": "13"},
                    ],
                    hints=[
                        "To undo, the editor must remember what the text looked like before each write. The most recent change is undone first.",
                        "'Most recent first' is a stack. Keep a history of earlier versions next to the text.",
                        "In write, push the current text onto the history before changing it. In undo, if the history is not empty, make its last entry the text and pop it.",
                        "Structure: members string text_; vector<string> history_; write: history_.push_back(text_); text_ += s; undo: if (!history_.empty()) { text_ = history_.back(); history_.pop_back(); }",
                    ],
                ),
            ],
        },
    ],
}
