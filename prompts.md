Prompt 1

Write test cases for a login page



Result: Returned an exhaustive, unfocused list covering functional, security,

UI/UX, accessibility, session, SSO, cross-browser, and performance test cases —

over 40 items total. Useful as a checklist but not usable as-is: no concrete

Gherkin format, no example data, and far beyond the 5 scenarios the ticket

actually asked for (valid login, invalid credentials, forgot password, session

expiry, brute-force lockout).



Prompt 2 

Act as a senior SDET. Generate Gherkin (Given/When/Then) test cases for a web login page covering exactly these 5 scenarios: valid login, invalid credentials, forgot password flow, session expiry, and brute-force lockout after repeated failed attempts. For each scenario include a Scenario title, concrete example data, and the expected observable outcome. Output as a Gherkin feature file.

\*\*Result:\*\* Clean, usable Gherkin feature file with concrete example data

("jane.doe@example.com", specific error messages, specific timings like "31

minutes" and "15 minutes") and observable outcomes tied directly to assertions.

Used as the basis for `test\_cases/login.feature`.



\### What didn't work first time / what changed

The first prompt returned a comprehensive but unfocused checklist — great for

inspiration, useless for direct automation since it wasn't in Gherkin format,

had no concrete data, and covered far more scope (SSO, accessibility, cross-

browser) than the sprint ticket asked for. Fixing this required explicitly

naming the exact 5 in-scope scenarios, requesting Gherkin format specifically,

and asking for concrete example data + observable outcomes so each line maps

directly to a testable assertion.

### Prompt 1 (first attempt — too broad)
generate dashboard test cases
**Result:** Returned a massive generic checklist (data loading, navigation,
filtering, charts, real-time updates, accessibility, performance — 40+ items)
assuming a generic analytics-style dashboard. Not anchored to any concrete UI,
so not directly usable as automation without picking and translating specific
items. Also far broader than the 5 areas the sprint ticket actually asked for.

### Prompt 2 (final — specific + constrained)
Act as a senior SDET. Generate Gherkin test cases for a product-listing dashboard page covering: widget/product loading, data accuracy of displayed name and price, sort behavior (name and price, ascending/descending), responsive layout on a mobile viewport, and permission-based visibility differences between two user roles. For each scenario give a Scenario title, concrete steps, and a specific assertion. Output as a Gherkin feature file.
**Result:** Clean, focused Gherkin covering exactly the 5 required areas, with
concrete data (product SKUs, prices, viewport dimensions, role names) and
specific assertions (e.g. HTTP 403 for restricted API access, 44x44px tap
targets on mobile). Used as the basis for `test_cases/dashboard.feature`.

### What didn't work first time / what changed
The first prompt returned a broad, unfocused checklist for a generic
dashboard with features (charts, real-time notifications, search) that don't
necessarily exist on the target page. Naming the 5 required areas explicitly,
specifying "product-listing dashboard" instead of "dashboard," and asking for
concrete steps + specific assertions produced directly automatable Gherkin
instead of a wishlist.