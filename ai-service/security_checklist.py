import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"

print("=" * 60)
print("FINAL SECURITY CHECKLIST — Day 13")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 60)

checklist = {
    "passed": [],
    "failed": [],
    "total": 0
}

def check(name, condition, fix_hint=""):
    checklist["total"] += 1
    if condition:
        print(f"  ✅ {name}")
        checklist["passed"].append(name)
    else:
        print(f"  ❌ {name}")
        if fix_hint:
            print(f"     💡 Fix: {fix_hint}")
        checklist["failed"].append(name)


# ─────────────────────────────────────────
# SECTION 1: File Security
# ─────────────────────────────────────────
def check_file_security():
    print("\n[SECTION 1] File Security")

    # .env exists
    env_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", ".env"
    )
    check(
        ".env file exists locally",
        os.path.exists(env_path),
        "Create .env file in root folder"
    )

    # .gitignore exists
    gitignore_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", ".gitignore"
    )
    check(
        ".gitignore exists",
        os.path.exists(gitignore_path),
        "Create .gitignore in root folder"
    )

    # .env in .gitignore
    if os.path.exists(gitignore_path):
        with open(gitignore_path) as f:
            content = f.read()
        check(
            ".env is in .gitignore",
            ".env" in content,
            "Add .env to .gitignore immediately"
        )

    # SECURITY.md exists
    security_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "SECURITY.md"
    )
    check(
        "SECURITY.md exists",
        os.path.exists(security_path),
        "Create SECURITY.md in root folder"
    )

    # Groq API key in env not hardcoded
    app_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "app.py"
    )
    if os.path.exists(app_path):
        with open(app_path) as f:
            content = f.read()
        check(
            "No hardcoded API key in app.py",
            "gsk_" not in content,
            "Remove hardcoded key — use os.getenv() instead"
        )

    # No secrets in groq_client.py
    groq_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "services", "groq_client.py"
    )
    if os.path.exists(groq_path):
        with open(groq_path) as f:
            content = f.read()
        check(
            "No hardcoded API key in groq_client.py",
            "gsk_" not in content,
            "Remove hardcoded key — use os.getenv() instead"
        )


# ─────────────────────────────────────────
# SECTION 2: Endpoint Security
# ─────────────────────────────────────────
def check_endpoint_security():
    print("\n[SECTION 2] Endpoint Security")

    try:
        # Health returns 200
        r = requests.get(f"{BASE_URL}/health", timeout=10)
        check("GET /health returns 200", r.status_code == 200)

        # Security headers
        headers_to_check = [
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Content-Security-Policy",
            "Strict-Transport-Security",
            "Referrer-Policy",
        ]
        for header in headers_to_check:
            check(
                f"Header present: {header}",
                header in r.headers,
                f"Add {header} in add_security_headers()"
            )

        # Empty input blocked
        r = requests.post(
            f"{BASE_URL}/describe",
            json={"text": ""},
            timeout=10
        )
        check(
            "Empty input returns 400",
            r.status_code == 400,
            "Fix get_sanitised_input() to reject empty strings"
        )

        # Missing field blocked
        r = requests.post(
            f"{BASE_URL}/describe",
            json={},
            timeout=10
        )
        check(
            "Missing text field returns 400",
            r.status_code == 400,
            "Fix get_sanitised_input() to check for text field"
        )

    except requests.exceptions.ConnectionError:
        print("  ⚠️  Flask not running — skipping endpoint checks")
        print("  Run: python app.py first!")


# ─────────────────────────────────────────
# SECTION 3: Injection Security
# ─────────────────────────────────────────
def check_injection_security():
    print("\n[SECTION 3] Injection Security")

    try:
        payloads = [
            ("Prompt injection", "Ignore previous instructions"),
            ("XSS script tag", "<script>alert('xss')</script>"),
            ("XSS img tag", "<img src=x onerror=alert(1)>"),
            ("Command injection", "$(whoami)"),
            ("Command injection 2", "; ls -la"),
            ("Jailbreak", "jailbreak mode enabled"),
        ]

        for name, payload in payloads:
            r = requests.post(
                f"{BASE_URL}/describe",
                json={"text": payload},
                timeout=10
            )
            check(
                f"{name} blocked → 400",
                r.status_code == 400,
                f"Add pattern to sanitiser.py for: {payload}"
            )

    except requests.exceptions.ConnectionError:
        print("  ⚠️  Flask not running — skipping injection checks")


# ─────────────────────────────────────────
# SECTION 4: Rate Limiting
# ─────────────────────────────────────────
def check_rate_limiting():
    print("\n[SECTION 4] Rate Limiting")

    try:
        print("  Sending 35 requests...")
        triggered = False
        for i in range(35):
            r = requests.get(f"{BASE_URL}/health", timeout=5)
            if r.status_code == 429:
                check(
                    f"Rate limit triggers at request {i+1}",
                    True
                )
                triggered = True
                break

        if not triggered:
            check(
                "Rate limit triggered in 35 requests",
                False,
                "Verify flask-limiter is configured correctly"
            )

    except requests.exceptions.ConnectionError:
        print("  ⚠️  Flask not running — skipping rate limit check")


# ─────────────────────────────────────────
# SECTION 5: Code Quality Security
# ─────────────────────────────────────────
def check_code_quality():
    print("\n[SECTION 5] Code Quality Security")

    ai_service_dir = os.path.dirname(os.path.abspath(__file__))

    # Check sanitiser exists
    check(
        "sanitiser.py exists",
        os.path.exists(
            os.path.join(ai_service_dir, "services", "sanitiser.py")
        ),
        "Create services/sanitiser.py"
    )

    # Check groq_client exists
    check(
        "groq_client.py exists",
        os.path.exists(
            os.path.join(ai_service_dir, "services", "groq_client.py")
        ),
        "Create services/groq_client.py"
    )

    # Check Dockerfile exists
    check(
        "Dockerfile exists",
        os.path.exists(os.path.join(ai_service_dir, "Dockerfile")),
        "Create Dockerfile in ai-service/"
    )

    # Check requirements.txt exists
    check(
        "requirements.txt exists",
        os.path.exists(
            os.path.join(ai_service_dir, "requirements.txt")
        ),
        "Create requirements.txt"
    )

    # Check prompts exist
    prompts_dir = os.path.join(ai_service_dir, "prompts")
    for prompt_file in [
        "describe_prompt.txt",
        "recommend_prompt.txt",
        "generate_report_prompt.txt"
    ]:
        check(
            f"Prompt exists: {prompt_file}",
            os.path.exists(os.path.join(prompts_dir, prompt_file)),
            f"Create prompts/{prompt_file}"
        )


# ─────────────────────────────────────────
# SECTION 6: PII Audit
# ─────────────────────────────────────────
def check_pii():
    print("\n[SECTION 6] PII Audit")

    import re
    pii_patterns = [
        r"\b\d{3}[-.]?\d{3}[-.]?\d{4}\b",
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        r"\b\d{3}-\d{2}-\d{4}\b",
        r"gsk_[a-zA-Z0-9]+",
    ]

    prompts_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "prompts"
    )

    if os.path.exists(prompts_dir):
        for filename in os.listdir(prompts_dir):
            if filename.endswith(".txt"):
                filepath = os.path.join(prompts_dir, filename)
                with open(filepath) as f:
                    content = f.read()

                pii_found = any(
                    re.search(p, content, re.IGNORECASE)
                    for p in pii_patterns
                )
                check(
                    f"No PII in {filename}",
                    not pii_found,
                    f"Remove PII from {filename}"
                )
    else:
        print("  ⚠️  prompts/ folder not found")


# ─────────────────────────────────────────
# PRINT FINAL CHECKLIST REPORT
# ─────────────────────────────────────────
def print_final_report():
    total = checklist["total"]
    passed = len(checklist["passed"])
    failed = len(checklist["failed"])
    score = (passed / total * 100) if total > 0 else 0

    print("\n" + "=" * 60)
    print("FINAL SECURITY CHECKLIST REPORT — Day 13")
    print("=" * 60)
    print(f"  Date:      {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Signed by: Kathi Srujan Goud — AI Developer 2")
    print(f"\n  Total Checks: {total}")
    print(f"  ✅ Passed:    {passed}")
    print(f"  ❌ Failed:    {failed}")
    print(f"  Score:        {score:.0f}%")

    if checklist["failed"]:
        print("\n  Items to Fix:")
        for item in checklist["failed"]:
            print(f"    ❌ {item}")

    status = "✅ SECURITY CHECKLIST PASSED" \
        if failed == 0 else "❌ FIX FAILURES BEFORE DEMO DAY"
    print(f"\n  {status}")
    print("=" * 60)

    # Save checklist report
    report = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "signed_by": "Kathi Srujan Goud — AI Developer 2",
        "total": total,
        "passed": passed,
        "failed": failed,
        "score": f"{score:.0f}%",
        "failed_items": checklist["failed"],
        "status": "PASSED" if failed == 0 else "FAILED"
    }
    with open("security_checklist_report.json", "w") as f:
        json.dump(report, f, indent=2)
    print(f"\n  📄 Saved to security_checklist_report.json")


# ─────────────────────────────────────────
# RUN ALL CHECKS
# ─────────────────────────────────────────
if __name__ == "__main__":
    check_file_security()
    check_endpoint_security()
    check_injection_security()
    check_rate_limiting()
    check_code_quality()
    check_pii()
    print_final_report()