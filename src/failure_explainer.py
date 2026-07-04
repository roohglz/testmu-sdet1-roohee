"""
Task 3 - Option A: Failure Explainer (powered by Groq)

Why this option over the Flaky Test Classifier:
The Flaky Test Classifier needs a history of MULTIPLE runs before it can
reliably tell "flaky" apart from "real bug", which is hard to demonstrate
convincingly in a single assessment build. The Failure Explainer gives
immediate, demonstrable value on every single failure - the moment a test
breaks, whoever picks it up gets a plain-English diagnosis and a suggested
fix instead of a raw stack trace they have to reverse-engineer themselves.
"""

import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "llama-3.3-70b-versatile"

EXPLAINER_SYSTEM_PROMPT = """You are a senior SDET reviewing an automated test failure.
Given the test name, error/traceback, and page or API context, respond with ONLY a
JSON object (no markdown fences, no preamble) in this exact shape:

{
  "summary": "one sentence plain-English explanation of what broke",
  "likely_cause": "2-3 sentences on the most probable root cause",
  "suggested_fix": "concrete, actionable fix - code-level if possible",
  "confidence": "high | medium | low"
}
"""


def explain_failure(test_name: str, error_message: str, context: dict) -> dict:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY not set. Copy .env.example to .env and add your key."
        )

    user_prompt = f"""Test name: {test_name}

Error / traceback:
{error_message}

Additional context:
{json.dumps(context, indent=2)}

Diagnose this failure."""

    response = requests.post(
        GROQ_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "system", "content": EXPLAINER_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
            "max_tokens": 500,
        },
        timeout=30,
    )
    response.raise_for_status()

    raw_text = response.json()["choices"][0]["message"]["content"].strip()

    try:
        parsed = json.loads(raw_text)
    except json.JSONDecodeError:
        parsed = {
            "summary": raw_text[:200],
            "likely_cause": "Could not parse structured response from LLM.",
            "suggested_fix": raw_text,
            "confidence": "low",
        }

    return parsed


def save_explanation(test_name: str, explanation: dict, out_path: str = "reports/failure_explanations.json"):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    entries = []
    if os.path.exists(out_path):
        with open(out_path, "r") as f:
            try:
                entries = json.load(f)
            except json.JSONDecodeError:
                entries = []

    entries.append({"test": test_name, "explanation": explanation})

    with open(out_path, "w") as f:
        json.dump(entries, f, indent=2)