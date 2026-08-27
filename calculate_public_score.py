import json
import os
import sys


assignment = os.environ.get("ASSIGNMENT")

if not assignment:
    print("ERROR: ASSIGNMENT 환경변수가 없습니다.")
    sys.exit(1)


config_file = f"{assignment}/grading_config.json"

if not os.path.exists(config_file):
    print(f"ERROR: 채점 설정 파일을 찾을 수 없습니다: {config_file}")
    sys.exit(1)


with open(config_file, "r", encoding="utf-8") as f:
    config = json.load(f)


try:
    with open("public_report.json", "r", encoding="utf-8") as f:
        report = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    print("ERROR: Public Test 결과를 읽을 수 없습니다.")
    sys.exit(1)


score = 0
summary_rows = []
max_score = sum(
    item["points"]
    for item in config.values()
)


print()
print("==========================================")
print("          Public Grading Result")
print("==========================================")
print(f"Assignment: {assignment}")
print()


for test in report.get("tests", []):
    test_name = test["nodeid"].split("::")[-1]
    outcome = test.get("outcome", "failed")

    if test_name not in config:
        continue

    item = config[test_name]

    display_name = item["name"]
    points = item["points"]

    if outcome == "passed":
        score += points
        print(
            f"[PASS] {display_name}: "
            f"+{points}점"
        )

        summary_rows.append(
            f"| ✅ | {display_name} | {points}/{points} |"
        )
    else:
        print(
            f"[FAIL] {display_name}: "
            f"+0점 / {points}점"
        )

        summary_rows.append(
            f"| ❌ | {display_name} | 0/{points} |"
        )


print()
print("------------------------------------------")
print(f"Total Score: {score}/{max_score}")
print("==========================================")

github_summary = os.environ.get("GITHUB_STEP_SUMMARY")

if github_summary:
    with open(github_summary, "a", encoding="utf-8") as f:
        f.write(f"## 🧪 {assignment} 채점 결과\n\n")
        f.write("| 결과 | 테스트 | 점수 |\n")
        f.write("| --- | --- | ---: |\n")

        for row in summary_rows:
            f.write(row + "\n")

        f.write("\n")
        f.write(f"### 총점: **{score}/{max_score}**\n")

result = {
    "assignment": assignment,
    "score": score,
    "max_score": max_score
}

with open("public_score.json", "w", encoding="utf-8") as f:
    json.dump(
        result,
        f,
        ensure_ascii=False,
        indent=2
    )


if score < max_score:
    sys.exit(1)