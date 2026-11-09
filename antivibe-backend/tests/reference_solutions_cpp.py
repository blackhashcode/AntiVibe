"""Reference solutions for the C++ exercises - used only to prove every exercise is solvable.

Each solution is the code below CPP_HEADER (the test adds the header).
"""

SOLUTIONS = {
    # ------------------------------------------------------------ fundamentals
    "rectangle-area": '''
double rectangle_area(double width, double height) {
    return width * height;
}
''',
    "full-name": '''
string full_name(const string& first, const string& last) {
    return first + " " + last;
}
''',
    "average-of-two": '''
double average_of_two(int a, int b) {
    return (a + b) / 2.0;
}
''',
    "hours-and-minutes": '''
vector<int> hours_and_minutes(int total_minutes) {
    return {total_minutes / 60, total_minutes % 60};
}
''',
    "is-even": '''
bool is_even(int n) {
    return n % 2 == 0;
}
''',
    "sign-of": '''
string sign_of(double n) {
    if (n > 0) {
        return "positive";
    } else if (n < 0) {
        return "negative";
    }
    return "zero";
}
''',
    "classify-number": '''
string classify(int n) {
    if (n == 0) {
        return "zero";
    } else if (n > 0) {
        return "positive";
    } else {
        return "negative";
    }
}
''',
    "letter-grade": '''
string letter_grade(int score) {
    if (score >= 90) return "A";
    if (score >= 80) return "B";
    if (score >= 70) return "C";
    if (score >= 60) return "D";
    return "F";
}
''',
    "leap-year": '''
bool is_leap_year(int year) {
    if (year % 400 == 0) return true;
    if (year % 100 == 0) return false;
    return year % 4 == 0;
}
''',
    "sum-to": '''
int sum_to(int n) {
    int total = 0;
    for (int i = 1; i <= n; i++) {
        total += i;
    }
    return total;
}
''',
    "sum-of-evens": '''
int sum_of_evens(int n) {
    int total = 0;
    for (int i = 2; i <= n; i += 2) {
        total += i;
    }
    return total;
}
''',
    "count-char": '''
int count_char(const string& s, char ch) {
    int count = 0;
    for (char c : s) {
        if (c == ch) count++;
    }
    return count;
}
''',
    "count-vowels": '''
int count_vowels(const string& s) {
    int count = 0;
    for (char c : s) {
        char low = tolower(c);
        if (string("aeiou").find(low) != string::npos) count++;
    }
    return count;
}
''',
    "has-digit": '''
bool has_digit(const string& s) {
    for (char ch : s) {
        if (isdigit(ch)) {
            return true;
        }
    }
    return false;
}
''',
    "sum-of-digits": '''
int sum_of_digits(int n) {
    int total = 0;
    int rest = n;
    while (rest > 0) {
        total += rest % 10;
        rest /= 10;
    }
    return total;
}
''',
    "reverse-string": '''
string reverse_string(const string& s) {
    string result;
    for (int i = (int)s.size() - 1; i >= 0; i--) {
        result += s[i];
    }
    return result;
}
''',
    "largest-number": '''
int largest(const vector<int>& nums) {
    int best = nums[0];
    for (int x : nums) {
        if (x > best) best = x;
    }
    return best;
}
''',
    "index-of": '''
int index_of(const vector<int>& nums, int target) {
    for (int i = 0; i < (int)nums.size(); i++) {
        if (nums[i] == target) return i;
    }
    return -1;
}
''',
    "only-evens": '''
vector<int> only_evens(const vector<int>& nums) {
    vector<int> result;
    for (int n : nums) {
        if (n % 2 == 0) result.push_back(n);
    }
    return result;
}
''',
    "average": '''
double average(const vector<int>& nums) {
    if (nums.empty()) return 0;
    int total = 0;
    for (int n : nums) total += n;
    return static_cast<double>(total) / nums.size();
}
''',
    "fizz-buzz": '''
vector<string> fizz_buzz(int n) {
    vector<string> result;
    for (int i = 1; i <= n; i++) {
        if (i % 15 == 0) result.push_back("FizzBuzz");
        else if (i % 3 == 0) result.push_back("Fizz");
        else if (i % 5 == 0) result.push_back("Buzz");
        else result.push_back(to_string(i));
    }
    return result;
}
''',
    "running-total": '''
vector<int> running_total(const vector<int>& nums) {
    vector<int> result;
    int total = 0;
    for (int n : nums) {
        total += n;
        result.push_back(total);
    }
    return result;
}
''',
    "without-negatives": '''
vector<int> without_negatives(vector<int> nums) {
    vector<int> result;
    for (int n : nums) {
        if (n >= 0) result.push_back(n);
    }
    return result;
}
''',
    "count-words": '''
int count_words(const string& s) {
    istringstream in(s);
    string word;
    int count = 0;
    while (in >> word) count++;
    return count;
}
''',
    "capitalize-words": '''
string capitalize_words(const string& s) {
    string result = s;
    for (size_t i = 0; i < result.size(); i++) {
        if (i == 0 || result[i - 1] == ' ') result[i] = toupper(result[i]);
    }
    return result;
}
''',
    "initials": '''
string initials(const string& name) {
    istringstream in(name);
    string word, result;
    while (in >> word) result += (char)toupper(word[0]);
    return result;
}
''',
    "is-palindrome-word": '''
bool is_palindrome_word(const string& word) {
    int left = 0, right = (int)word.size() - 1;
    while (left < right) {
        if (tolower(word[left]) != tolower(word[right])) return false;
        left++;
        right--;
    }
    return true;
}
''',
    "longest-word": '''
string longest_word(const string& s) {
    istringstream in(s);
    string word, best;
    while (in >> word) {
        if (word.size() > best.size()) best = word;
    }
    return best;
}
''',
    "shout": '''
string shout(string s) {
    for (char& c : s) {
        c = toupper(c);
    }
    return s;
}
''',
    "valid-palindrome": '''
bool is_palindrome(const string& s) {
    string cleaned;
    for (char c : s) {
        if (isalnum(c)) cleaned += (char)tolower(c);
    }
    int left = 0, right = (int)cleaned.size() - 1;
    while (left < right) {
        if (cleaned[left] != cleaned[right]) return false;
        left++;
        right--;
    }
    return true;
}
''',
    "char-count": '''
map<char, int> char_count(const string& s) {
    map<char, int> counts;
    for (char c : s) counts[c]++;
    return counts;
}
''',
    "unique-count": '''
int unique_count(const vector<int>& nums) {
    set<int> values(nums.begin(), nums.end());
    return values.size();
}
''',
    "contains-duplicate": '''
bool contains_duplicate(const vector<int>& nums) {
    unordered_set<int> seen;
    for (int x : nums) {
        if (seen.count(x)) return true;
        seen.insert(x);
    }
    return false;
}
''',
    "first-unique-char": '''
string first_unique_char(const string& s) {
    map<char, int> counts;
    for (char c : s) counts[c]++;
    for (char c : s) {
        if (counts[c] == 1) return string(1, c);
    }
    return "";
}
''',
    "most-common-char": '''
string most_common_char(const string& s) {
    map<char, int> counts;
    for (char c : s) counts[c]++;
    string best;
    for (char c : s) {
        if (best.empty() || counts[c] > counts[best[0]]) best = string(1, c);
    }
    return best;
}
''',
    "valid-anagram": '''
bool is_anagram(const string& s, const string& t) {
    map<char, int> a, b;
    for (char c : s) a[c]++;
    for (char c : t) b[c]++;
    return a == b;
}
''',
    "group-by-first-letter": '''
map<char, vector<string>> group_by_first_letter(const vector<string>& words) {
    map<char, vector<string>> groups;
    for (const string& w : words) groups[w[0]].push_back(w);
    return groups;
}
''',
    "safe-divide": '''
double safe_divide(double a, double b) {
    if (b == 0) throw invalid_argument("b must not be zero");
    return a / b;
}
''',
    "to-int": '''
int to_int(const string& text, int fallback = 0) {
    try {
        size_t used = 0;
        int value = stoi(text, &used);
        if (used != text.size()) return fallback;
        return value;
    } catch (const invalid_argument&) {
        return fallback;
    }
}
''',
    "parse-scores": '''
bool parse_whole(const string& piece, int& value) {
    try {
        size_t used = 0;
        value = stoi(piece, &used);
        return used == piece.size();
    } catch (const invalid_argument&) {
        return false;
    }
}

vector<int> parse_scores(const string& text) {
    vector<int> scores;
    istringstream in(text);
    string piece;
    while (getline(in, piece, ',')) {
        int value;
        if (parse_whole(piece, value)) scores.push_back(value);
    }
    return scores;
}
''',
    "primes": '''
bool is_prime(int n) {
    if (n < 2) return false;
    for (int d = 2; d < n; d++) {
        if (n % d == 0) return false;
    }
    return true;
}

vector<int> primes_up_to(int n) {
    vector<int> result;
    for (int k = 2; k <= n; k++) {
        if (is_prime(k)) result.push_back(k);
    }
    return result;
}
''',
    "factorial": '''
long long factorial(int n) {
    if (n == 0) return 1;
    return n * factorial(n - 1);
}
''',
    "power": '''
long long power(int base, int exp) {
    if (exp == 0) return 1;
    return base * power(base, exp - 1);
}
''',
    "count-down": '''
vector<int> count_down(int n) {
    if (n == 0) {
        return {0};
    }
    vector<int> result = {n};
    vector<int> rest = count_down(n - 1);
    result.insert(result.end(), rest.begin(), rest.end());
    return result;
}
''',
    "sum-list": '''
int sum_from(const vector<int>& nums, int start) {
    if (start == (int)nums.size()) return 0;
    return nums[start] + sum_from(nums, start + 1);
}

int sum_list(const vector<int>& nums) {
    return sum_from(nums, 0);
}
''',
    "reverse-recursive": '''
string reverse_recursive(const string& s) {
    if (s.empty()) return "";
    return reverse_recursive(s.substr(1)) + s[0];
}
''',
    # ------------------------------------------------------------ OOP
    "counter-class": '''
class Counter {
public:
    void increment() { count_++; }
    void reset() { count_ = 0; }
    int count() const { return count_; }
private:
    int count_ = 0;
};
''',
    "thermostat": '''
class Thermostat {
public:
    Thermostat() : target_(20) {}
    void set_target(int target) { target_ = target; }
    int target() const { return target_; }
private:
    int target_ = 0;
};
''',
    "rectangle-class": '''
class Rectangle {
public:
    Rectangle(double width, double height) : width_(width), height_(height) {}
    double width() const { return width_; }
    double height() const { return height_; }
    double area() const { return width_ * height_; }
    double perimeter() const { return 2 * (width_ + height_); }
    bool is_square() const { return width_ == height_; }
    void set_width(double width) { width_ = width; }
private:
    double width_;
    double height_;
};
''',
    "playlist": '''
class Playlist {
public:
    void add(const string& song) { songs_.push_back(song); }
    vector<string> songs() const { return songs_; }
    int count() const { return songs_.size(); }
    bool has(const string& song) const { return find(songs_.begin(), songs_.end(), song) != songs_.end(); }
    void remove(const string& song) {
        auto it = find(songs_.begin(), songs_.end(), song);
        if (it == songs_.end()) throw invalid_argument("no such song");
        songs_.erase(it);
    }
private:
    vector<string> songs_;
};
''',
    "bank-account": '''
class BankAccount {
public:
    BankAccount(const string& owner, double balance = 0) : owner_(owner), balance_(balance) {}
    string owner() const { return owner_; }
    double balance() const { return balance_; }
    void deposit(double amount) {
        if (amount <= 0) throw invalid_argument("amount must be positive");
        balance_ += amount;
    }
    void withdraw(double amount) {
        if (amount <= 0 || amount > balance_) throw invalid_argument("invalid amount");
        balance_ -= amount;
    }
private:
    string owner_;
    double balance_;
};
''',
    "point-class": '''
class Point {
public:
    Point(int x, int y) : x_(x), y_(y) {}
    int x() const { return x_; }
    int y() const { return y_; }
    string str() const { return "(" + to_string(x_) + ", " + to_string(y_) + ")"; }
    bool operator==(const Point& other) const { return x_ == other.x_ && y_ == other.y_; }
    Point translate(int dx, int dy) const { return Point(x_ + dx, y_ + dy); }
private:
    int x_;
    int y_;
};
''',
    "inventory": '''
class Inventory {
public:
    void add(const string& item, int qty) {
        if (qty <= 0) throw invalid_argument("quantity must be positive");
        stock_[item] += qty;
    }
    void remove(const string& item, int qty) {
        if (qty <= 0 || quantity(item) < qty) throw invalid_argument("cannot remove that many");
        stock_[item] -= qty;
    }
    int quantity(const string& item) const {
        auto it = stock_.find(item);
        return it == stock_.end() ? 0 : it->second;
    }
    int total() const {
        int units = 0;
        for (const auto& [item, qty] : stock_) units += qty;
        return units;
    }
private:
    map<string, int> stock_;
};
''',
    "animal-sounds": '''
class Animal {
public:
    Animal(const string& name) : name_(name) {}
    virtual ~Animal() = default;
    string name() const { return name_; }
    virtual string speak() const { return "Some sound"; }
    string describe() const { return name_ + " says " + speak(); }
private:
    string name_;
};

class Dog : public Animal {
public:
    Dog(const string& name) : Animal(name) {}
    string speak() const override { return "Woof"; }
};

class Cat : public Animal {
public:
    Cat(const string& name) : Animal(name) {}
    string speak() const override { return "Meow"; }
};
''',
    "vehicles": '''
class Vehicle {
public:
    Vehicle(const string& name) : name_(name) {}
    virtual ~Vehicle() = default;
    virtual int wheels() const { return 4; }
    string summary() const { return name_ + " has " + to_string(wheels()) + " wheels"; }
protected:
    string name_;
};

class Bike : public Vehicle {
public:
    Bike(const string& name) : Vehicle(name) {}
    int wheels() const override { return 2; }
};

class Truck : public Vehicle {
public:
    Truck(const string& name, int load) : Vehicle(name), load_(load) {}
    int wheels() const override { return 6; }
    int load() const { return load_; }
private:
    int load_;
};
''',
    "shapes": '''
class Shape {
public:
    Shape(const string& name) : name_(name) {}
    virtual ~Shape() = default;
    string name() const { return name_; }
    virtual double area() const { return 0; }
private:
    string name_;
};

class Square : public Shape {
public:
    Square(double side) : Shape("square"), side_(side) {}
    double area() const override { return side_ * side_; }
private:
    double side_;
};

class Triangle : public Shape {
public:
    Triangle(double base, double height) : Shape("triangle"), base_(base), height_(height) {}
    double area() const override { return base_ * height_ / 2; }
private:
    double base_;
    double height_;
};

double total_area(const vector<Shape*>& shapes) {
    double total = 0;
    for (Shape* s : shapes) total += s->area();
    return total;
}
''',
    "stack-class": '''
class Stack {
public:
    void push(int item) { items_.push_back(item); }
    int pop() {
        if (items_.empty()) throw out_of_range("empty stack");
        int top = items_.back();
        items_.pop_back();
        return top;
    }
    int peek() const {
        if (items_.empty()) throw out_of_range("empty stack");
        return items_.back();
    }
    bool is_empty() const { return items_.empty(); }
    int size() const { return items_.size(); }
private:
    vector<int> items_;
};
''',
    "queue-class": '''
class Queue {
public:
    void enqueue(int item) { items_.push_back(item); }
    int dequeue() {
        if (items_.empty()) throw out_of_range("empty queue");
        int first = items_.front();
        items_.erase(items_.begin());
        return first;
    }
    bool is_empty() const { return items_.empty(); }
    int size() const { return items_.size(); }
private:
    vector<int> items_;
};
''',
    "text-editor": '''
class TextEditor {
public:
    string text() const { return text_; }
    void write(const string& s) {
        history_.push_back(text_);
        text_ += s;
    }
    void undo() {
        if (!history_.empty()) {
            text_ = history_.back();
            history_.pop_back();
        }
    }
private:
    string text_;
    vector<string> history_;
};
''',
    # ------------------------------------------------------------ DSA
    "has-pair-sum": '''
bool has_pair_sum(const vector<int>& nums, int target) {
    unordered_set<int> seen;
    for (int n : nums) {
        if (seen.count(target - n)) return true;
        seen.insert(n);
    }
    return false;
}
''',
    "two-sum": '''
vector<int> two_sum(const vector<int>& nums, int target) {
    unordered_map<int, int> index_of;
    for (int i = 0; i < (int)nums.size(); i++) {
        int need = target - nums[i];
        if (index_of.count(need)) return {index_of[need], i};
        index_of[nums[i]] = i;
    }
    return {};
}
''',
    "missing-number": '''
int missing_number(const vector<int>& nums) {
    unordered_set<int> present(nums.begin(), nums.end());
    for (int c = 0; c <= (int)nums.size(); c++) {
        if (!present.count(c)) return c;
    }
    return -1;
}
''',
    "pair-sum-sorted": '''
bool pair_sum_sorted(const vector<int>& nums, int target) {
    int left = 0, right = (int)nums.size() - 1;
    while (left < right) {
        int s = nums[left] + nums[right];
        if (s == target) return true;
        if (s < target) left++;
        else right--;
    }
    return false;
}
''',
    "merge-sorted-lists": '''
vector<int> merge_sorted(const vector<int>& a, const vector<int>& b) {
    vector<int> result;
    size_t i = 0, j = 0;
    while (i < a.size() && j < b.size()) {
        if (a[i] <= b[j]) result.push_back(a[i++]);
        else result.push_back(b[j++]);
    }
    while (i < a.size()) result.push_back(a[i++]);
    while (j < b.size()) result.push_back(b[j++]);
    return result;
}
''',
    "is-subsequence": '''
bool is_subsequence(const string& s, const string& t) {
    size_t i = 0, j = 0;
    while (i < s.size() && j < t.size()) {
        if (s[i] == t[j]) i++;
        j++;
    }
    return i == s.size();
}
''',
    "valid-parentheses": '''
char opener_for(char c) {
    if (c == ')') return '(';
    if (c == ']') return '[';
    return '{';
}

bool is_valid(const string& s) {
    stack<char> st;
    for (char c : s) {
        if (c == '(' || c == '[' || c == '{') {
            st.push(c);
        } else {
            if (st.empty() || st.top() != opener_for(c)) return false;
            st.pop();
        }
    }
    return st.empty();
}
''',
    "remove-adjacent-duplicates": '''
string remove_adjacent_duplicates(const string& s) {
    string st;
    for (char c : s) {
        if (!st.empty() && st.back() == c) st.pop_back();
        else st.push_back(c);
    }
    return st;
}
''',
    "evaluate-rpn": '''
int evaluate_rpn(const vector<string>& tokens) {
    stack<int> st;
    for (const string& token : tokens) {
        if (token == "+" || token == "-" || token == "*") {
            int right = st.top(); st.pop();
            int left = st.top(); st.pop();
            if (token == "+") st.push(left + right);
            else if (token == "-") st.push(left - right);
            else st.push(left * right);
        } else {
            st.push(stoi(token));
        }
    }
    return st.top();
}
''',
    "binary-search": '''
int binary_search(const vector<int>& nums, int target) {
    int left = 0, right = (int)nums.size() - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] == target) return mid;
        if (nums[mid] < target) left = mid + 1;
        else right = mid - 1;
    }
    return -1;
}
''',
    "sqrt-floor": '''
long long sqrt_floor(long long n) {
    long long left = 0, right = n, answer = 0;
    while (left <= right) {
        long long mid = left + (right - left) / 2;
        if (mid * mid <= n) {
            answer = mid;
            left = mid + 1;
        } else {
            right = mid - 1;
        }
    }
    return answer;
}
''',
    "first-at-least": '''
int first_at_least(const vector<int>& nums, int target) {
    int left = 0, right = (int)nums.size() - 1, answer = nums.size();
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (nums[mid] >= target) {
            answer = mid;
            right = mid - 1;
        } else {
            left = mid + 1;
        }
    }
    return answer;
}
''',
    "linked-list-search": '''
struct Node {
    int value;
    Node* next;
    Node(int v) : value(v), next(nullptr) {}
};

class LinkedList {
public:
    Node* head = nullptr;

    void append(int value) {
        Node* node = new Node(value);
        if (head == nullptr) { head = node; return; }
        Node* current = head;
        while (current->next != nullptr) current = current->next;
        current->next = node;
    }

    vector<int> to_list() const {
        vector<int> values;
        for (Node* c = head; c != nullptr; c = c->next) values.push_back(c->value);
        return values;
    }

    bool contains(int value) const {
        for (Node* c = head; c != nullptr; c = c->next) {
            if (c->value == value) return true;
        }
        return false;
    }

    int last() const {
        if (head == nullptr) throw out_of_range("empty list");
        Node* c = head;
        while (c->next != nullptr) c = c->next;
        return c->value;
    }
};
''',
    "linked-list-basics": '''
struct Node {
    int value;
    Node* next;
    Node(int v) : value(v), next(nullptr) {}
};

class LinkedList {
public:
    Node* head = nullptr;

    void append(int value) {
        Node* node = new Node(value);
        if (head == nullptr) { head = node; return; }
        Node* current = head;
        while (current->next != nullptr) current = current->next;
        current->next = node;
    }

    void prepend(int value) {
        Node* node = new Node(value);
        node->next = head;
        head = node;
    }

    vector<int> to_list() const {
        vector<int> values;
        for (Node* c = head; c != nullptr; c = c->next) values.push_back(c->value);
        return values;
    }

    int size() const {
        int count = 0;
        for (Node* c = head; c != nullptr; c = c->next) count++;
        return count;
    }
};
''',
    "reverse-linked-list": '''
struct Node {
    int value;
    Node* next;
    Node(int v) : value(v), next(nullptr) {}
};

class LinkedList {
public:
    Node* head = nullptr;

    void append(int value) {
        Node* node = new Node(value);
        if (head == nullptr) { head = node; return; }
        Node* current = head;
        while (current->next != nullptr) current = current->next;
        current->next = node;
    }

    vector<int> to_list() const {
        vector<int> values;
        for (Node* c = head; c != nullptr; c = c->next) values.push_back(c->value);
        return values;
    }

    void reverse() {
        Node* previous = nullptr;
        Node* current = head;
        while (current != nullptr) {
            Node* following = current->next;
            current->next = previous;
            previous = current;
            current = following;
        }
        head = previous;
    }
};
''',
    "fibonacci": '''
long long fib(int n) {
    if (n < 2) return n;
    long long previous = 0, current = 1;
    for (int i = 2; i <= n; i++) {
        long long next = previous + current;
        previous = current;
        current = next;
    }
    return current;
}
''',
    "climbing-stairs": '''
long long climb_stairs(int n) {
    if (n <= 2) return n;
    long long prev = 1, cur = 2;
    for (int i = 3; i <= n; i++) {
        long long next = prev + cur;
        prev = cur;
        cur = next;
    }
    return cur;
}
''',
    "max-subarray": '''
int max_subarray(const vector<int>& nums) {
    int here = nums[0], best = nums[0];
    for (size_t i = 1; i < nums.size(); i++) {
        here = max(nums[i], here + nums[i]);
        best = max(best, here);
    }
    return best;
}
''',
    'bst-insert': '''
struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v, TreeNode* l = nullptr, TreeNode* r = nullptr) : value(v), left(l), right(r) {}
};

class BST {
public:
    TreeNode* root = nullptr;

    void insert(int value) {
        if (root == nullptr) { root = new TreeNode(value); return; }
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

    bool contains(int value) const {
        const TreeNode* node = root;
        while (node != nullptr) {
            if (value == node->value) return true;
            node = value < node->value ? node->left : node->right;
        }
        return false;
    }
};
''',
    'bst-inorder': '''
struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v, TreeNode* l = nullptr, TreeNode* r = nullptr) : value(v), left(l), right(r) {}
};

class BST {
public:
    TreeNode* root = nullptr;

    void insert(int value) {
        if (root == nullptr) { root = new TreeNode(value); return; }
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

    vector<int> in_order() const {
        vector<int> out;
        visit(root, out);
        return out;
    }

    int size() const { return count(root); }

private:
    static void visit(const TreeNode* n, vector<int>& out) {
        if (!n) return;
        visit(n->left, out);
        out.push_back(n->value);
        visit(n->right, out);
    }
    static int count(const TreeNode* n) { return n ? count(n->left) + 1 + count(n->right) : 0; }
};
''',
    'bst-height': '''
struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v, TreeNode* l = nullptr, TreeNode* r = nullptr) : value(v), left(l), right(r) {}
};

class BST {
public:
    TreeNode* root = nullptr;

    void insert(int value) {
        if (root == nullptr) { root = new TreeNode(value); return; }
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

    int height() const { return h(root); }

    int min_value() const {
        if (!root) throw out_of_range("empty tree");
        const TreeNode* n = root;
        while (n->left) n = n->left;
        return n->value;
    }

    int max_value() const {
        if (!root) throw out_of_range("empty tree");
        const TreeNode* n = root;
        while (n->right) n = n->right;
        return n->value;
    }

private:
    static int h(const TreeNode* n) { return n ? 1 + max(h(n->left), h(n->right)) : 0; }
};
''',
    'valid-bst': '''
struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v, TreeNode* l = nullptr, TreeNode* r = nullptr) : value(v), left(l), right(r) {}
};

bool within(const TreeNode* n, const TreeNode* low, const TreeNode* high) {
    if (!n) return true;
    if (low && n->value <= low->value) return false;
    if (high && n->value >= high->value) return false;
    return within(n->left, low, n) && within(n->right, n, high);
}

bool is_valid_bst(const TreeNode* node) {
    return within(node, nullptr, nullptr);
}
''',
    'bst-remove': '''
struct TreeNode {
    int value;
    TreeNode* left;
    TreeNode* right;
    TreeNode(int v, TreeNode* l = nullptr, TreeNode* r = nullptr) : value(v), left(l), right(r) {}
};

class BST {
public:
    TreeNode* root = nullptr;

    void insert(int value) {
        if (root == nullptr) { root = new TreeNode(value); return; }
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

    void remove(int value) { root = remove_from(root, value); }

private:
    static TreeNode* remove_from(TreeNode* n, int value) {
        if (!n) return nullptr;
        if (value < n->value) {
            n->left = remove_from(n->left, value);
        } else if (value > n->value) {
            n->right = remove_from(n->right, value);
        } else {
            if (!n->left) { TreeNode* r = n->right; delete n; return r; }
            if (!n->right) { TreeNode* l = n->left; delete n; return l; }
            const TreeNode* m = n->right;
            while (m->left) m = m->left;
            n->value = m->value;
            n->right = remove_from(n->right, n->value);
        }
        return n;
    }
};
''',
}
