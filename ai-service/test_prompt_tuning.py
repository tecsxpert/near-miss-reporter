import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.groq_client import call_groq, load_prompt
from datetime import datetime

# 10 Real near miss incidents for testing
TEST_INCIDENTS = [
    "A worker slipped on a wet floor near the warehouse entrance",
    "A forklift nearly collided with a pedestrian in the loading bay",
    "An electrical panel was left open near water pipes",
    "A scaffold platform was missing guardrails on the third floor",
    "A chemical spill occurred near the storage room with no PPE available",
    "A worker was nearly struck by a falling tool from an elevated platform",
    "A fire exit was blocked by boxes during the night shift",
    "A machine guard was removed for maintenance and not replaced",
    "A worker was exposed to excessive noise without ear protection",
    "A ladder was improperly secured and slipped during use",
]

def score_response(response: str, endpoint: str) -> int:
    """
    Score AI response quality from 1-10.
    Returns score based on quality checks.
    """
    score = 10

    if not response or len(response) < 20:
        return 1

    if endpoint == "describe":
        if len(response) < 50:
            score -= 3
        if len(response) > 500:
            score -= 2
        keywords = ["incident", "worker", "near", "safety", "risk", "hazard"]
        found = sum(1 for k in keywords if k.lower() in response.lower())
        if found < 2:
            score -= 2

    elif endpoint == "recommend":
        if "action_type" not in response:
            score -= 4
        if "priority" not in response:
            score -= 3
        if "description" not in response:
            score -= 3

    return max(1, score)


def test_describe_prompts():
    print("\n" + "="*60)
    print("PROMPT TUNING — /describe endpoint")
    print("="*60)

    scores = []
    for i, incident in enumerate(TEST_INCIDENTS, 1):
        prompt = load_prompt("describe_prompt.txt", incident_text=incident)
        messages = [{"role": "user", "content": prompt}]
        result = call_groq(messages, temperature=0.3)

        content = str(result["content"])
        score = score_response(content, "describe")
        scores.append(score)

        status = "✅" if score >= 7 else "❌"
        print(f"\n  Test {i:02d}: {status} Score: {score}/10")
        print(f"  Incident: {incident[:60]}...")
        print(f"  Response: {content[:100]}...")

    avg = sum(scores) / len(scores)
    print(f"\n  📊 Average Score: {avg:.1f}/10")
    print(f"  {'✅ PASSED' if avg >= 7 else '❌ NEEDS IMPROVEMENT'}")
    return avg


def test_recommend_prompts():
    print("\n" + "="*60)
    print("PROMPT TUNING — /recommend endpoint")
    print("="*60)

    scores = []
    for i, incident in enumerate(TEST_INCIDENTS, 1):
        prompt = load_prompt("recommend_prompt.txt", incident_text=incident)
        messages = [{"role": "user", "content": prompt}]
        result = call_groq(messages, temperature=0.3)

        content = str(result["content"])
        score = score_response(content, "recommend")
        scores.append(score)

        status = "✅" if score >= 7 else "❌"
        print(f"\n  Test {i:02d}: {status} Score: {score}/10")
        print(f"  Incident: {incident[:60]}...")
        print(f"  Response: {content[:150]}...")

    avg = sum(scores) / len(scores)
    print(f"\n  📊 Average Score: {avg:.1f}/10")
    print(f"  {'✅ PASSED' if avg >= 7 else '❌ NEEDS IMPROVEMENT'}")
    return avg


if __name__ == "__main__":
    print(f"Starting Prompt Tuning Tests — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    desc_avg = test_describe_prompts()
    rec_avg = test_recommend_prompts()

    print("\n" + "="*60)
    print("PROMPT TUNING SUMMARY")
    print("="*60)
    print(f"  /describe  average score: {desc_avg:.1f}/10")
    print(f"  /recommend average score: {rec_avg:.1f}/10")
    overall = (desc_avg + rec_avg) / 2
    print(f"  Overall average:          {overall:.1f}/10")
    print(f"\n  {'✅ ALL PROMPTS PASSED' if overall >= 7 else '❌ PROMPTS NEED IMPROVEMENT'}")