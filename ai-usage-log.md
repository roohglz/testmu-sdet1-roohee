\# AI Usage Log



| Tool | Task | What it produced |

|---|---|---|

| Claude (Anthropic) | Task 1 - Repo scaffolding | Folder structure, pytest.ini, .gitignore, requirements.txt, first commit message |

| Claude (Anthropic) | Task 2 - Prompt engineering | Generated Gherkin test cases in test\_cases/ (login, dashboard, api) from prompts logged in prompts.md. Two prompt iterations per module - vague first attempt discarded, specific constrained prompt used |

| Claude (Anthropic) | Task 3 - Code implementation | Helped write the Playwright/pytest test files (tests/login, tests/dashboard, tests/api) and the pytest hook wiring in conftest.py |

| Groq (Llama 3.3 70B) | Task 3 - Failure Explainer | Real, live API integration (src/failure\_explainer.py) called from conftest.py's pytest\_runtest\_makereport hook. On every real test failure, makes a live call to Groq's API and returns a structured JSON diagnosis (summary, likely cause, suggested fix, confidence), saved to reports/failure\_explanations.json |

| Claude (Anthropic) | Debugging | Diagnosed reqres.in requiring a real x-api-key (their auth policy changed), and identified two stray leftover test files causing unrelated crashes |

| Claude (Anthropic) | Documentation | Drafted this log and README.md |



\## Known gaps / honest limitations



\- \*\*Rate limiting (API module):\*\* reqres.in doesn't enforce real rate limits in a way that's testable here, so the rate-limiting Gherkin scenario in test\_cases/api.feature has no corresponding automated test.

\- \*\*Forgot password (Login module):\*\* saucedemo.com has no forgot-password flow. The Gherkin scenario is kept for completeness but isn't automated against this demo target.

\- \*\*Flaky Test Classifier (Task 3, Option B):\*\* not built - Option A (Failure Explainer) was chosen instead. Rationale is documented as a comment at the top of src/failure\_explainer.py.

