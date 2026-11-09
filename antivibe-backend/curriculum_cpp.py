"""The C++ curriculum: fundamentals, then OOP, then DSA."""
import curriculum_cpp_dsa
import curriculum_cpp_fundamentals
import curriculum_cpp_oop

TRACKS = [curriculum_cpp_fundamentals.TRACK, curriculum_cpp_oop.TRACK, curriculum_cpp_dsa.TRACK]

# Questions and descriptions copied from the Python exercises that talk about Python
REWORDED = {
    "largest-number": {"questions": [
        "Why does starting with best = 0 fail for {-3, -1, -2}?",
        "How many comparisons does your loop make for a vector of n numbers?",
    ]},
    "fizz-buzz": {"questions": [
        "Why does `i < n` give the wrong answer here?",
        "Which order of checks breaks the 15 test, and why?",
    ]},
    "running-total": {"questions": [
        "Why would re-adding everything from the start for each position be slower?",
        "What does const in `const vector<int>& nums` stop you from doing?",
    ]},
    "initials": {"questions": [
        "Why is reading words with >> safer than looking for spaces yourself?",
        "Why does the empty name not crash your solution?",
    ]},
    "is-palindrome-word": {"questions": [
        "Why does \"Level\" fail without tolower?",
        "Why must right be an int rather than a size_t when the word is empty?",
    ]},
    "unique-count": {
        "description": "Return how many different values the vector nums contains.",
        "questions": [
            "How would you do this without a set, and how much slower would it be?",
            "What does a set lose that a vector keeps?",
        ],
    },
    "first-unique-char": {"questions": [
        "Why must the second loop go over the string rather than over the map?",
        "How many times is each character looked at in total?",
    ]},
    "valid-anagram": {"questions": [
        "Strings of different lengths can never be anagrams. Where could you check that first?",
        "How would sorting both strings compare with counting, in time complexity?",
    ]},
    "parse-scores": {"questions": [
        "Why does the empty string give an empty vector, not an error?",
        "Why does \"5x\" need the used-characters check?",
    ]},
    "primes": {"description": (
        "Write two functions. is_prime(n) returns true if n is a prime number - a whole number greater than 1 "
        "whose only divisors are 1 and itself - and false otherwise. primes_up_to(n) returns a vector of all the "
        "primes from 2 to n inclusive, in order, and must use is_prime to decide."
    )},
    "sum-list": {"questions": [
        "Trace sum_list({1, 2, 3}) on paper the way the lesson does.",
        "What happens to the recursive version for a vector of a million numbers, and why?",
    ]},
    "two-sum": {"questions": [
        "What are the time and space complexities of the brute-force and the unordered_map approach?",
        "How does your solution behave when the vector contains duplicate numbers?",
    ]},
    "pair-sum-sorted": {"questions": [
        "Why is it safe to discard the smallest number when the sum is too small?",
        "Why does this need a sorted vector, when Pair With Sum did not?",
    ]},
    "merge-sorted-lists": {"questions": [
        "What is the time complexity in terms of the two lengths?",
        "Why is this better than putting both into one vector and sorting it?",
    ]},
    "binary-search": {"questions": [
        "Why must the vector be sorted for this to work?",
        "How many steps does a vector of one million elements need at most?",
    ]},
    "reverse-linked-list": {"questions": [
        "Why does the old head end up pointing at nullptr without any special case?",
        "How much extra memory does your reverse use?",
    ]},
}

for _track in TRACKS:
    for _milestone in _track["milestones"]:
        for _problem in _milestone["problems"]:
            _problem.update(REWORDED.get(_problem["id"], {}))
