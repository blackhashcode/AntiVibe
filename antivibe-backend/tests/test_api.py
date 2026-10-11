import pytest
from fastapi.testclient import TestClient

from main import app, classify_problem
from problems import MILESTONES, PROBLEMS

client = TestClient(app)


def test_health():
    assert client.get("/api/health").json()["status"] == "healthy"


def test_curriculum_lists_tracks_milestones_and_problems_in_order():
    tracks = client.get("/api/curriculum").json()["tracks"]

    assert [track["id"] for track in tracks] == ["python", "oop", "dsa"]
    milestones = [m for track in tracks for m in track["milestones"]]
    assert [m["id"] for m in milestones] == [m["id"] for m in MILESTONES]
    problems = [p for m in milestones for p in m["problems"]]
    assert [p["id"] for p in problems] == [p["id"] for p in PROBLEMS]


def test_curriculum_is_an_outline_only():
    first = client.get("/api/curriculum").json()["tracks"][0]["milestones"][0]

    assert "lesson" not in first
    assert set(first["problems"][0]) == {
        "id", "title", "difficulty", "track_id", "track", "milestone_id", "milestone",
    }


def test_milestone_detail_has_the_lesson():
    milestone = client.get("/api/milestones/py-loops").json()

    assert milestone["title"] == "Loops"
    assert milestone["track"] == "Python Fundamentals"
    assert [s["heading"] for s in milestone["lesson"]][0] == "for loops and range"
    assert any("return" in s["text"] for s in milestone["lesson"])
    assert client.get("/api/milestones/nope").status_code == 404


def test_problem_list_is_in_learning_order_without_hints_or_tests():
    problems = client.get("/api/problems").json()["problems"]

    assert [p["id"] for p in problems] == [p["id"] for p in PROBLEMS]
    assert "tests" not in problems[0] and "hints" not in problems[0]


def test_function_problem_detail_has_what_the_extension_needs_but_no_hints():
    problem = client.get("/api/problems/two-sum").json()

    assert problem["function"] == {"name": "two_sum", "params": ["nums", "target"]}
    assert problem["starter"] == "def two_sum(nums, target):\n    pass\n"
    assert problem["requires"] == ["two_sum"]
    assert problem["examples"][0] == "two_sum([2, 7, 11, 15], 9) -> [0, 1]"
    assert problem["tests"][0] == {"args": [[2, 7, 11, 15], 9], "expected": [0, 1]}
    assert problem["milestone_id"] == "dsa-hashing"
    assert problem["hint_count"] == 4
    assert "hints" not in problem


def test_class_problem_detail_has_starter_and_readable_examples():
    problem = client.get("/api/problems/bank-account").json()

    assert problem["function"] is None
    assert problem["starter"] == "class BankAccount:\n    pass\n"
    assert problem["requires"] == ["BankAccount"]
    assert problem["examples"] == [
        "a = BankAccount('Ann', 100)\na.deposit(50)\na.balance -> 150",
        "a = BankAccount('Ann', 100)\na.withdraw(500) -> raises ValueError",
    ]


def test_default_arguments_appear_in_the_starter():
    problem = client.get("/api/problems/to-int").json()

    assert problem["starter"] == "def to_int(text, default=0):\n    pass\n"


def test_examples_are_written_as_python():
    problem = client.get("/api/problems/valid-palindrome").json()

    assert problem["examples"][0] == "is_palindrome('A man, a plan, a canal: Panama') -> True"


def test_unknown_problem_is_404():
    assert client.get("/api/problems/nope").status_code == 404
    assert client.get("/api/problems/nope/hints").status_code == 404


def test_hints_are_revealed_in_order():
    first = client.get("/api/problems/two-sum/hints").json()
    assert [h["level"] for h in first["hints"]] == [1]
    assert first["total"] == 4

    third = client.get("/api/problems/two-sum/hints", params={"upto": 3}).json()
    assert [h["level"] for h in third["hints"]] == [1, 2, 3]
    assert third["hints"][0] == first["hints"][0]
    assert third["hints"][2]["label"] == "Implementation hint"


def test_hints_stop_at_the_last_level():
    data = client.get("/api/problems/two-sum/hints", params={"upto": 99}).json()

    assert len(data["hints"]) == 4
    assert client.get("/api/problems/two-sum/hints", params={"upto": 0}).status_code == 422


def test_hints_work_for_problems_without_resources():
    data = client.get("/api/problems/rectangle-area/hints").json()

    assert data["resources"] == []
    assert data["questions"]


@pytest.mark.parametrize("description, expected", [
    ("Find two numbers that add up to target", "two_sum"),
    ("Search for a value in a sorted array", "binary_search"),
    ("Find target in rotated sorted array", "binary_search"),
    ("Reverse a string", "string_reversal"),
    ("Reverse a linked list", "linked_list"),
    ("Add a node to a linked list", "linked_list"),
    ("Detect a cycle in a linked list", "linked_list"),
    ("Find the maximum subarray sum", "general"),
    ("Check if array contains duplicates", "general"),
    ("Merge two sorted arrays", "general"),
    ("Count islands in a grid", "general"),
    ("", "general"),
])
def test_classify_problem(description, expected):
    assert classify_problem(description) == expected


@pytest.mark.parametrize("level", [1, 2, 3, 4])
def test_freeform_hint(level):
    response = client.post("/api/hint", json={
        "code": "def reverse(head): pass",
        "problem_description": "Reverse a linked list",
        "hint_level": level,
    })

    assert response.status_code == 200
    data = response.json()
    assert data["hint"] and data["next_step"]
    assert len(data["questions"]) == 2
    assert all("linked-list" in url for url in data["resources"])


def test_freeform_hint_rejects_unknown_level():
    response = client.post("/api/hint", json={
        "code": "x", "problem_description": "two sum", "hint_level": 9,
    })

    assert response.status_code == 422
