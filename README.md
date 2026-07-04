# testmu-sdet1-roohee



\# TestMu AI SDET-1 Assessment — Roohee Gulnaz



AI-native regression testing scaffold covering Login, Dashboard, and REST API

modules, with a live LLM-powered Failure Explainer wired into the test run.



\## Stack

\- Python 3.11

\- Playwright for Login/Dashboard UI tests (against saucedemo.com)

\- requests + jsonschema for REST API tests (against reqres.in)

\- pytest + pytest-html for the test runner and reporting

\- Groq API (Llama 3.3 70B) for the Failure Explainer (Task 3)



\## Why these public demo targets

There's no access to TestMu's real Login/Dashboard/API, so tests run against

public equivalents that map cleanly onto the sprint ticket: saucedemo.com

(login states incl. lockout, a sortable product grid as the "dashboard") and

reqres.in (a real REST API with auth, CRUD, and error responses).



\## Setup

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

playwright install chromium



Copy `.env.example` to `.env` and add your own keys:

GROQ\_API\_KEY=your\_groq\_key

REQRES\_API\_KEY=your\_reqres\_key



pytest



This runs all three modules and generates:

\- `reports/report.html` — full HTML test report

\- `reports/failure\_explanations.json` — one entry per failed test with a real

&#x20; Groq-generated summary, likely cause, suggested fix, and confidence level



One test (`test\_deliberate\_failure\_for\_explainer\_demo` in

`tests/login/test\_login.py`) is intentionally left failing so every run

produces a real, non-mocked sample output for the Failure Explainer.



\## Repo structure

tests/

conftest.py

login/test\_login.py

dashboard/test\_dashboard.py

api/test\_api.py

src/

failure\_explainer.py

test\_cases/

prompts.md

ai-usage-log.md

reports/            (generated on run, gitignored)



\## What I'd build next with more time



\- Self-healing locators: when a Playwright selector fails, ask the LLM to

&#x20; inspect the DOM and suggest an updated selector automatically.

\- Flaky Test Classifier (Option B): run the suite N times in CI and classify

&#x20; failures using real pass/fail history, not just a single run's logs.

\- Cache Failure Explainer results by a hash of (test name + error) so

&#x20; repeated identical CI failures don't re-call the API every time.

\- Point the API suite at an environment with real rate limiting so that

&#x20; Gherkin scenario can be automated honestly.

