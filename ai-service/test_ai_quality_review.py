import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
import time
from datetime import datetime
from services.groq_client import call_groq, load_prompt

print("=" * 60)
print("WEEK 2 AI QUALITY REVIEW — Day 10")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

# 10 Fresh Near Miss Incidents
FRESH_INCIDENTS = [
    "A worker was nearly hit by a reversing forklift in the loading bay",
    "An overhead crane load swung unexpectedly near workers below",
    "A gas leak was detected near the boiler room before ignition",
    "A worker nearly fell through an unguarded floor opening",
    "Electrical sparks were observed near flammable chemical storage",
    "A scaffolding plank cracked under a worker's weight on level 4",
    "A vehicle entered a pedestrian-only zone at high speed",
    "A worker inhaled chemical fumes due to inadequate ventilation",
    "A loose bolt was found on a critical machine component during inspection",
    "A fire extinguisher was found expired during a routine safety check",
]

results = {
    "describe": {"scores": [], "passed": 0, "failed": 0},
    "recommend": {"scores": [], "passed": 0, "failed": 0},
    "generate_report": {"scores": [], "passed": 0, "failed": 0},
}


# ─────────────────────────────────────────
# SCORING FUNCTIONS
# ─────────────────────────────────────────
def score_describe(response: str) -> int:
    """Score /describe response 1-5."""
    if not response or len(response) < 30:
        return 1

    score = 5

    # Too short
    if len(response) < 60:
        score -= 2

    # Too long (should be 2-3 sentences)
    if len(response) > 600:
        score -= 1

    # Must contain safety keywords
    keywords = ["incident", "worker", "near", "safety",
                "risk", "hazard", "occurred", "potential"]
    found = sum(1 for k in keywords if k.lower() in response.lower())
    if found < 2:
        score -= 2

    return max(1, score)


def score_recommend(response: str) -> int:
    """Score /recommend response 1-5."""
    if not response or len(response) < 20:
        return 1

    score = 5

    # Must contain JSON structure
    if "action_type" not in response:
        score -= 2
    if "priority" not in response:
        score -= 1
    if "description" not in response:
        score -= 1

    # Must contain priority values
    has_priority = any(p in response for p in ["High", "Medium", "Low"])
    if not has_priority:
        score -= 1

    return max(1, score)


def score_generate_report(response: str) -> int:
    """Score /generate-report response 1-5."""
    if not response or len(response) < 50:
        return 1

    score = 5

    # Must contain report fields
    required_fields = ["title", "summary", "severity"]
    for field in required_fields:
        if field not in response.lower():
            score -= 1

    # Must be substantial
    if len(response) < 200:
        score -= 2

    return max(1, score)


# ─────────────────────────────────────────
# TEST /describe ENDPOINT
# ─────────────────────────────────────────
def test_describe_quality():
    print("\n" + "="*60)
    print("ENDPOINT: /describe — 10 Fresh Inputs")
    print("="*60)

    for i, incident in enumerate(FRESH_INCIDENTS, 1):
        try:
            prompt = load_prompt(
                "describe_prompt.txt",
                incident_text=incident
            )
            messages = [{"role": "user", "content": prompt}]
            result = call_groq(messages, temperature=0.3)

            score = score_describe(result["content"])
            results["describe"]["scores"].append(score)

            status = "✅" if score >= 4 else "❌"
            if score >= 4:
                results["describe"]["passed"] += 1
            else:
                results["describe"]["failed"] += 1

            print(f"\n  [{i:02d}] {status} Score: {score}/5")
            print(f"  Incident: {incident[:55]}...")
            print(f"  Response: {result['content'][:100]}...")

            # Small delay to avoid rate limiting
            time.sleep(1)

        except Exception as e:
            print(f"  [{i:02d}] ❌ Error: {e}")
            results["describe"]["scores"].append(1)
            results["describe"]["failed"] += 1

    avg = sum(results["describe"]["scores"]) / len(results["describe"]["scores"])
    print(f"\n  📊 Average Score: {avg:.1f}/5")
    print(f"  {'✅ PASSED' if avg >= 4 else '❌ NEEDS IMPROVEMENT'}")
    return avg


# ─────────────────────────────────────────
# TEST /recommend ENDPOINT
# ─────────────────────────────────────────
def test_recommend_quality():
    print("\n" + "="*60)
    print("ENDPOINT: /recommend — 10 Fresh Inputs")
    print("="*60)

    for i, incident in enumerate(FRESH_INCIDENTS, 1):
        try:
            prompt = load_prompt(
                "recommend_prompt.txt",
                incident_text=incident
            )
            messages = [{"role": "user", "content": prompt}]
            result = call_groq(messages, temperature=0.3)

            score = score_recommend(result["content"])
            results["recommend"]["scores"].append(score)

            status = "✅" if score >= 4 else "❌"
            if score >= 4:
                results["recommend"]["passed"] += 1
            else:
                results["recommend"]["failed"] += 1

            print(f"\n  [{i:02d}] {status} Score: {score}/5")
            print(f"  Incident: {incident[:55]}...")
            print(f"  Response: {result['content'][:120]}...")

            time.sleep(1)

        except Exception as e:
            print(f"  [{i:02d}] ❌ Error: {e}")
            results["recommend"]["scores"].append(1)
            results["recommend"]["failed"] += 1

    avg = sum(results["recommend"]["scores"]) / len(results["recommend"]["scores"])
    print(f"\n  📊 Average Score: {avg:.1f}/5")
    print(f"  {'✅ PASSED' if avg >= 4 else '❌ NEEDS IMPROVEMENT'}")
    return avg


# ─────────────────────────────────────────
# TEST /generate-report ENDPOINT
# ─────────────────────────────────────────
def test_generate_report_quality():
    print("\n" + "="*60)
    print("ENDPOINT: /generate-report — 10 Fresh Inputs")
    print("="*60)

    for i, incident in enumerate(FRESH_INCIDENTS, 1):
        try:
            prompt = load_prompt(
                "generate_report_prompt.txt",
                incident_text=incident
            )
            messages = [{"role": "user", "content": prompt}]
            result = call_groq(messages, temperature=0.3, max_tokens=1500)

            score = score_generate_report(result["content"])
            results["generate_report"]["scores"].append(score)

            status = "✅" if score >= 4 else "❌"
            if score >= 4:
                results["generate_report"]["passed"] += 1
            else:
                results["generate_report"]["failed"] += 1

            print(f"\n  [{i:02d}] {status} Score: {score}/5")
            print(f"  Incident: {incident[:55]}...")
            print(f"  Response: {result['content'][:120]}...")

            time.sleep(1)

        except Exception as e:
            print(f"  [{i:02d}] ❌ Error: {e}")
            results["generate_report"]["scores"].append(1)
            results["generate_report"]["failed"] += 1

    avg = sum(results["generate_report"]["scores"]) / len(results["generate_report"]["scores"])
    print(f"\n  📊 Average Score: {avg:.1f}/5")
    print(f"  {'✅ PASSED' if avg >= 4 else '❌ NEEDS IMPROVEMENT'}")
    return avg


# ─────────────────────────────────────────
# PRINT FINAL QUALITY REPORT
# ─────────────────────────────────────────
def print_quality_report(desc_avg, rec_avg, report_avg):
    overall = (desc_avg + rec_avg + report_avg) / 3

    print("\n" + "=" * 60)
    print("WEEK 2 AI QUALITY REVIEW REPORT")
    print("=" * 60)
    print(f"  Reviewed by: Kathi Srujan Goud — AI Developer 2")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n  /describe       avg: {desc_avg:.1f}/5  "
          f"{'✅' if desc_avg >= 4 else '❌'}")
    print(f"  /recommend      avg: {rec_avg:.1f}/5  "
          f"{'✅' if rec_avg >= 4 else '❌'}")
    print(f"  /generate-report avg: {report_avg:.1f}/5  "
          f"{'✅' if report_avg >= 4 else '❌'}")
    print(f"\n  Overall Average: {overall:.1f}/5")
    print(f"\n  {'✅ ALL ENDPOINTS PASSED' if overall >= 4 else '❌ SOME ENDPOINTS NEED IMPROVEMENT'}")
    print("=" * 60)

    # Save report to file
    report = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "reviewer": "Kathi Srujan Goud",
        "describe_avg": round(desc_avg, 1),
        "recommend_avg": round(rec_avg, 1),
        "generate_report_avg": round(report_avg, 1),
        "overall_avg": round(overall, 1),
        "status": "PASSED" if overall >= 4 else "NEEDS IMPROVEMENT"
    }

    with open("ai_quality_report.json", "w") as f:
        json.dump(report, f, indent=2)

    print(f"\n  📄 Report saved to ai_quality_report.json")


# ─────────────────────────────────────────
# RUN ALL TESTS
# ─────────────────────────────────────────
if __name__ == "__main__":
    desc_avg = test_describe_quality()
    rec_avg = test_recommend_quality()
    report_avg = test_generate_report_quality()
    print_quality_report(desc_avg, rec_avg, report_avg)