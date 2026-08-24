# Initial Plan — Personal Finance Assistant

## 1. Objective

**What am I going to do?**

Build a CLI-based Personal Finance Assistant powered by an LLM (Groq) that can hold a natural-language conversation about my finances. It will have at least three real tools — a calculator, a live currency conversion API, and a local SQLite expense database — plus one connected MCP server as a demo. The model itself decides which tool to call for a given request; nothing is hardcoded.

**Why am I doing it?**

This is the capstone project for the internship's "LLM APIs, Structured Output, and Tools" week. The goal is to move past toy examples and build something with real tool-calling, schema validation, streaming, error handling, and cost tracking — the core skills that week is meant to teach.

**Expected Final Result**

A working CLI app where I can type things like "I spent 4500 on groceries yesterday, add it", "how much is that in USD?", or "what's my total food spend this month?" and the assistant correctly picks and runs the right tool, validates the result, streams its reply, and logs token usage/cost — while handling errors (rate limits, timeouts, bad model output, tool failures) gracefully.

---

## 2. Context

**Background**

This project sits at the end of the internship's LLM APIs/Structured Output/Tools week, which itself covers: auth/key management, the chat completions message array, streaming, structured output/JSON mode, Pydantic validation, function calling, multiple tools, error handling, retry with backoff, token counting/cost estimation, guardrails, and MCP basics. Groq was chosen as the LLM provider for this week.

**Current Situation**

No code exists yet for this project. I already have Python fundamentals through OOP, and I've separately completed a working MCP server (a GitHub Repo Assistant with `get_repo_info`, `list_issues`, and `search_code` tools) from an earlier MCP practice project — this can potentially serve as the MCP demo connection, or I can connect to a different lightweight MCP server instead.

**Relevant Information**

- Existing behavior: none — greenfield build
- Existing implementation: GitHub Repo Assistant MCP server (separate project, already working) — reusable as the MCP demo client target
- Related documentation: Groq API docs (chat completions, function calling, streaming), Pydantic docs, a free currency API (e.g. frankfurter.dev or exchangerate-api.com)
- Related requirements: the project spec (calculator, external API tool, local DB tool, model-driven routing, Pydantic-validated output, streaming, retry w/ backoff, token/cost logging, graceful error handling, one MCP server connected)

**Constraints**

- Time constraint: internship week timeline — should be buildable in a few focused sessions
- Technology constraint: Python, Groq as LLM provider, free-tier currency API (no paid keys)
- Business constraint: none (personal/learning project)
- Other limitation: DSA is a current weak spot, but this project doesn't require heavy algorithmic work — mostly API integration and architecture

---

## 3. Understanding

**My Understanding**
I need to build a tool-calling loop where an LLM decides, per user message, whether to do plain math, hit a currency API, query a local expense database, or call an MCP-based tool. Every tool's input and output must be validated with Pydantic before use. The assistant should stream its text responses, retry on transient failures, log token usage and estimated cost per request, and fail gracefully rather than crashing on bad input, rate limits, or tool errors.

**Inputs**
- User's natural-language messages (CLI stdin)
- Groq API responses (including tool-call requests and streamed text)
- Currency API responses (live exchange rates)
- Local SQLite `expenses` table data
- MCP server responses (from the connected demo server)

**Outputs**
- Streamed conversational replies in the CLI
- Updated/queried rows in the local expense database
- A log of token usage and estimated cost per request (file or DB table)
- Graceful error messages on failure cases instead of stack traces

**Dependencies**
- Groq API key and access
- A free currency conversion API (no-key option preferred, e.g. frankfurter.dev)
- Python packages: `groq` SDK, `pydantic`, SQLite (`sqlite3`, standard library), a retry helper (e.g. `tenacity`) or manual backoff logic
- A running MCP server to connect to as the demo (reuse GitHub Repo Assistant or stand up a simple one)

---

## 4. Initial Investigation

**Things to Check**
- [x] Existing implementation — GitHub Repo Assistant MCP server already built and working
- [ ] Existing documentation — Groq function-calling/streaming docs not yet reviewed in detail
- [ ] Existing APIs — currency API not yet chosen/tested
- [ ] Existing database/schema — no expense schema designed yet
- [ ] Existing components/modules — none
- [ ] Existing similar implementation — none
- [ ] Existing tests — none
- [ ] Existing configuration — Groq API key setup from earlier weeks may already exist
- [ ] External dependencies — need to confirm `groq` SDK supports streamed tool calls cleanly

**Findings**

*Finding 1*
Groq was already selected and used earlier in this internship week, so auth/key setup and basic chat completions are likely already familiar — this project builds on that rather than starting from zero.

*Finding 2*
An MCP server (GitHub Repo Assistant) already exists and works, with three tools. It can plausibly satisfy the "one MCP server connected" requirement without new server-side work — only an MCP *client* connection needs to be built.

*Finding 3*
The three custom tools (calculator, currency, DB) have no overlapping dependencies and can each be built and tested standalone before any LLM is involved — reducing the risk of debugging two unknowns (tool logic vs. model routing) at once.

---

## 5. Requirements

**Must Have**
- [ ] At least 3 working tools: calculator, real external API (currency), local DB/file query
- [ ] Model-driven tool selection — no hardcoded routing (e.g. no `if "convert" in text`)
- [ ] All tool inputs and outputs validated against Pydantic schemas before use
- [ ] Streaming responses in the CLI
- [ ] Retry with backoff on transient errors (rate limits, timeouts)
- [ ] Token usage and estimated cost logged per request
- [ ] Graceful handling of: rate limits, timeouts, malformed model output, tool failure
- [ ] One MCP server connected as a demo

**Should Have**
- [ ] Persistent expense history across CLI sessions (SQLite file, not in-memory)
- [ ] Basic categorization support in the expense DB (category column, filterable)
- [ ] A simple cost-log view command (e.g. "show me token usage today")

**Nice to Have**
- [ ] Multi-currency default settings (e.g. remembering preferred display currency)
- [ ] A minimal export of expenses (CSV) for review outside the CLI
- [ ] Colorized/streamed CLI output for readability

**Out of Scope**
- Any GUI or web frontend — CLI only for this project
- Multi-user support or authentication
- Real bank/account integrations — expenses are manually entered by the user

---

## 6. Approach

**Proposed Approach**

Step 1: Build SQLite schema + seed data, tested with raw Python (no LLM)
  ↓
Step 2: Build the three tool functions (`add_expense`, `convert_currency`, `calculate`) and call them directly to confirm they work in isolation
  ↓
Step 3: Define Pydantic input/output schemas for each tool
  ↓
Step 4: Wire up Groq function-calling with all three tools registered, letting the model choose which to call
  ↓
Step 5: Add streaming for text responses, handling tool-call chunks separately from plain text chunks
  ↓
Step 6: Add retry-with-backoff around the Groq API call
  ↓
Step 7: Add token usage + estimated cost logging per request
  ↓
Step 8: Deliberately break things (malformed JSON, bad currency codes, no network) and add graceful error handling
  ↓
Step 9: Connect an MCP server as a fourth tool option, plugging into the same tool-calling loop
  ↓
Expected Result: a CLI assistant satisfying every requirement above, buildable and testable incrementally at each step

**Why This Approach?**
Building strictly bottom-up (data layer → isolated tool functions → schemas → LLM wiring → resilience → MCP) means at every step there is only one new unknown to debug. Jumping straight into LLM tool-calling without first confirming the tools work standalone makes it impossible to tell whether a bug is in the tool logic or in how the model is invoking it.

**Alternatives Considered**

*Alternative 1: Build the LLM tool-calling loop first, then implement each tool inline as needed*
Pros:
- Faster to see "something working" early
Cons:
- Any bug could be in either the model's tool call or the tool's own logic — much harder to isolate
- Encourages hardcoded routing shortcuts to get a demo working fast, defeating the "no hardcoded routing" requirement

*Alternative 2: Build all three custom tools plus MCP connection in parallel before touching the LLM at all*
Pros:
- Clear separation of "tool work" vs "LLM work"
Cons:
- MCP client work has its own setup/debugging surface; better to confirm the core tool-calling loop works with simpler tools first, then add MCP once the pattern is proven

**Final Decision**
Go with the sequential bottom-up approach (Steps 1–9 above). It isolates unknowns at each stage and defers the MCP connection until the core tool-calling loop is already proven to work, which lowers overall risk.

---

## 7. Execution Steps

**Step 1: Data layer**
Goal: Have a working, queryable local expense database with no LLM involved.
Actions:
- [ ] Design `expenses` table schema (`id, amount, category, date, currency`)
- [ ] Write seed/insert script with a few sample expenses
- [ ] Write and manually test a few raw query functions (by category, by date range, totals)
Expected Result: A `.db` file with sample data that can be reliably queried via plain Python.

**Step 2: Isolated tool functions**
Goal: Confirm each of the three core tools works correctly on its own.
Actions:
- [ ] Write `add_expense()`, `convert_currency()`, `calculate()` as plain functions
- [ ] Manually call and test each with a range of inputs, including edge cases
Expected Result: Three tested, working Python functions with no LLM dependency yet.

**Step 3: Pydantic schemas**
Goal: Define validation for every tool's input and output.
Actions:
- [ ] Write input schema per tool (e.g. `ConvertCurrencyInput`)
- [ ] Write output schema per tool
- [ ] Validate a few sample calls against the schemas
Expected Result: Every tool has enforced input/output contracts.

**Step 4: LLM tool-calling wiring**
Goal: Let Groq choose and call tools based on natural-language input, with zero hardcoded routing.
Actions:
- [ ] Register tool definitions (JSON schema) with Groq's function-calling API
- [ ] Build the request/response loop: send message → get tool call → run tool → validate output → send result back → get final reply
Expected Result: The assistant correctly picks the right tool for a variety of test prompts.

**Step 5: Streaming, retries, logging, error handling**
Goal: Make the assistant resilient and observable.
Actions:
- [ ] Add streaming for text responses
- [ ] Add retry-with-backoff around Groq calls
- [ ] Add token usage/cost logging per request
- [ ] Handle malformed output, tool failures, timeouts, and rate limits gracefully
Expected Result: The assistant survives deliberately induced failures without crashing.

**Step 6: MCP connection**
Goal: Demonstrate a connected MCP server as a fourth tool source.
Actions:
- [ ] Connect to the existing GitHub Repo Assistant MCP server (or a simpler alternative)
- [ ] Register its tool(s) into the same tool-calling loop as the other three
Expected Result: The model can call an MCP-backed tool through the same architecture as the custom tools.

---

## 8. Unknowns

| Question | Why It Matters | How I Will Find the Answer |
|---|---|---|
| Does the Groq SDK stream tool-call chunks the same way as plain text chunks? | Determines how Step 5's streaming logic needs to branch | Test directly against the Groq API with a tool-registered request |
| Which free currency API has the most reliable uptime with no key required? | Affects reliability of the "real external API" tool | Test frankfurter.dev and exchangerate-api.com directly before committing |
| Can the existing GitHub MCP server be reused as-is for the MCP demo, or does it need finance-relevant tools? | Affects whether Step 6 is "plug in existing work" or "build new" | Review the spec wording — likely just needs a working MCP *connection*, not a finance-specific one |

---

## 9. Assumptions

- The MCP demo requirement is satisfied by connecting to *any* working MCP server (including the pre-existing, unrelated GitHub one), not necessarily a finance-specific one
- A free-tier currency API without an API key is acceptable for the "real external API" requirement
- SQLite is an acceptable "local database" — no need for Postgres or another engine
- The CLI is the only required interface — no web/GUI layer needed

If an assumption turns out to be incorrect, this plan will be updated.

---

## 10. Risks

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| Model doesn't reliably pick the correct tool for ambiguous prompts | Medium | Medium | Write clear, distinct tool descriptions; test with varied phrasing early in Step 4 |
| Free currency API has rate limits or downtime | Medium | Low | Have a backup free API in mind; cache last-known rates |
| Streaming + tool calls interact in an unexpected way in the Groq SDK | Medium | Medium | Investigate this as Unknown #1 before starting Step 5, not during it |
| Scope creep (adding "Should Have"/"Nice to Have" items before Must Haves are solid) | Low | Medium | Follow Execution Steps in order; treat Must Haves as the completion gate |

---

## 11. Validation Plan

**Functional Validation**
- [ ] Each of the 3 custom tools produces correct results when called directly
- [ ] The model correctly routes at least 5 varied natural-language prompts to the right tool
- [ ] Pydantic validation actually rejects a deliberately malformed tool input/output
- [ ] Streaming visibly renders token-by-token (or chunk-by-chunk) in the CLI
- [ ] Token usage and cost are logged after every request
- [ ] The MCP-connected tool is successfully called at least once via the same loop

**Edge Cases**
- [ ] Ambiguous prompt that could match more than one tool (e.g. "what's 100 usd in pkr" — calculator vs currency)
- [ ] Invalid currency code passed to the currency tool
- [ ] Empty or malformed model tool-call output
- [ ] Currency API unreachable (simulate by blocking network access)

**Regression**
- [ ] N/A — greenfield project, no existing behavior to preserve

**Final Validation**
Run a full end-to-end session covering all three custom tools plus the MCP tool in one conversation, confirming correct routing, validated output, streamed replies, and a clean cost/token log — with at least one deliberately triggered failure (e.g. bad currency code) handled gracefully instead of crashing.

---

## 12. Expected Deliverable

- A working CLI Python application implementing the Personal Finance Assistant
- SQLite database file with expense schema and sample data
- Pydantic schema definitions for all tool inputs/outputs
- A log file (or DB table) of token usage and estimated cost per request
- A working MCP client connection to at least one MCP server

---

## 13. Completion Criteria

The work is complete when:
- [ ] Objective has been achieved
- [ ] All required steps are completed
- [ ] Expected result is produced
- [ ] Validation has been completed
- [ ] Edge cases have been checked
- [ ] No known critical issues remain
- [ ] Documentation is updated if required

---

## 14. Post Work Review

*(To be filled in after the work is complete)*

**What I Actually Did**


**What Changed From the Initial Plan?**


**What Did I Learn?**


**Problems Encountered**


**How Were They Solved?**


**Remaining Work**


**Final Result**


---

## 15. LLM Context

When giving this plan to an LLM, use the complete document as context.

The LLM should:
- Understand the Objective before suggesting or writing anything
- Understand the Context and Current Situation
- Use the Investigation section to understand what already exists
- Follow the Requirements and Scope
- Follow the selected Approach unless there is a strong technical reason to change it
- Never invent missing information
- Clearly identify Unknowns instead of making assumptions
- Respect the listed Constraints
- Follow the Execution Steps in order when dependencies exist
- Consider the documented Risks and Edge Cases
- Validate the final result against the Validation Plan
- If the implementation differs from the plan, explain why
- Keep the work aligned with the original Objective
- At the end, compare the actual result with the Initial Plan