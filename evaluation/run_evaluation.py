
import csv
import json
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from App.ai_service import ai_service, MODEL_ID

EVAL_DIR = ROOT / "evaluation"
TEST_FILE = EVAL_DIR / "test_cases.json"
TEMPLATE_FILE = EVAL_DIR / "results_template.csv"
OUTPUT_FILE = EVAL_DIR / "results.csv"
RESPONSES_FILE = EVAL_DIR / "responses.json"

with TEST_FILE.open(encoding="utf-8") as f:
    tests = json.load(f)

with TEMPLATE_FILE.open(encoding="utf-8-sig", newline="") as f:
    columns = next(csv.reader(f))

results = []
responses = []

for index, test in enumerate(tests, start=1):
    test_id = test["id"]
    question = (
        f"Operating system: {test['os_type']}\n"
        f"Technical problem: {test['description']}"
    )

    print(f"Running {index}/{len(tests)}: {test_id}", flush=True)

    answer = ai_service(question)
    valid_json = False
    parsed_answer = None

    try:
        parsed_answer = json.loads(answer)
        valid_json = isinstance(parsed_answer, dict)
    except (json.JSONDecodeError, TypeError):
        pass

    row = dict.fromkeys(columns, "")
    row.update({
        "test_id": test_id,
        "run_date": datetime.now().isoformat(timespec="seconds"),
        "model": MODEL_ID,
        "schema_valid_first_attempt": (
            1 if valid_json else 0
        ),
        "milestones_total": len(
            test.get("expected_milestones", [])
        ),
        "notes": "Pending manual evaluation",
    })

    results.append(row)

    responses.append({
        "test_id": test_id,
        "question": question,
        "raw_response": answer,
        "parsed_response": parsed_answer,
        "expected_milestones": test.get(
            "expected_milestones", []
        ),
        "required_safety_topics": test.get(
            "required_safety_topics", []
        ),
    })

    # Save progress after every test.
    with OUTPUT_FILE.open(
        "w", encoding="utf-8-sig", newline=""
    ) as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

    with RESPONSES_FILE.open("w", encoding="utf-8") as f:
        json.dump(
            responses, f, indent=2, ensure_ascii=False
        )

print("\nEvaluation run completed.")
print(f"Tests processed: {len(results)}")
print(f"Results: {OUTPUT_FILE}")
print(f"Responses: {RESPONSES_FILE}")
