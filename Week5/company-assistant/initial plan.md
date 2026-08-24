# Initial Plan — Company Assistant API

Based on the provided task specification, the goal is to build an AI-powered **Company Assistant API** that combines LLM tool calling, multi-tool orchestration, MCP, FastAPI, Pydantic, SQLite, external APIs, retries, streaming, and testing.

### 1. Objective

- **What:** Build a Company Assistant API where users can interact with an LLM through `/chat`.
- **Why:** To demonstrate practical integration of LLMs with tools, APIs, databases, and backend services.
- **Final result:** The LLM should understand a request, select the required tools, execute one or multiple tools, and return a useful final response.

### 2. Context

- The system will manage **users and tasks** using SQLite.
- It will retrieve weather information through an external weather API.
- The LLM will use **native/function tool calling** instead of hardcoded keyword logic.
- Main technologies: **Python, FastAPI, Pydantic, SQLite, LLM, MCP, external weather API**.
- The task also requires streaming, retries, automated testing, and clean architecture.

### 3. Understanding

- Build a backend assistant that can understand a natural-language request and decide whether it needs user data, weather data, or task operations.
- **Inputs:** `user_id`, natural-language message, task titles, cities, and API requests.
- **Processing:** LLM → tool selection → tool execution → collect results → LLM → final response.
- **Outputs:** User information, tasks, weather information, or a combined natural-language response.
- **Dependencies:** LLM API, weather API, SQLite database, FastAPI, Pydantic, and MCP.

### 4. Initial Investigation

- Check which LLM supports **native/function tool calling**.
- Check the chosen weather API's request format, authentication, errors, and timeout behavior.
- Understand the MCP SDK and the minimal client/server communication required.
- Decide how the LLM tool-calling loop will handle **multiple tool calls**.
- Verify how FastAPI `StreamingResponse` will be used.
- Identify which external components should be mocked during testing.

### 5. Requirements

- **Must Have:**
  - `POST /chat`
  - User and task endpoints
  - SQLite `users` and `tasks`
  - Pydantic validation
  - LLM tool calling
  - `get_user`, `create_task`, `list_tasks`, `get_weather`
  - Multi-tool orchestration
  - MCP server + client
  - Weather API integration
  - Retry/error handling
  - Streaming response
  - Automated tests

- **Should Have:**
  - Clean service/tool separation.
  - Parameterized database queries.
  - Environment variables for secrets.
  - Useful logging.
  - Proper HTTP status codes.

- **Nice to Have:**
  - Better logging/observability.
  - Parallel execution where safe.
  - More sophisticated retry policies.
  - Production-oriented improvements.

- **Out of Scope:**
  - Building a large/general-purpose MCP framework.
  - Building unnecessary frontend functionality.
  - Adding features unrelated to the required assistant functionality.

### 6. Approach

- **Input → Processing → Output:**

  `User Request → FastAPI → LLM → Tool Selection → Tool Execution → Tool Results → LLM → Streaming Final Response`

- **Components:**
  - FastAPI → API layer
  - Pydantic → request/response validation
  - SQLite → users/tasks
  - LLM → reasoning and tool selection
  - Tools → application capabilities
  - Weather API → external data
  - MCP → tool discovery/execution
  - Tests → validation

- **Why this approach:** It separates responsibilities so the API, LLM, tools, database, and external services can be developed and tested independently.

- **Alternative considered:** Hardcoding keyword-based tool selection, but this is explicitly not acceptable because the LLM must decide which tools are required.

### 7. Execution Steps

#### Phase 1 — Setup & Architecture

- **Goal:** Create the project foundation.
- **Actions:**
  - Create project structure.
  - Create virtual environment.
  - Install dependencies.
  - Create `.env`.
  - Configure FastAPI application.
- **Expected result:** Application starts successfully with a clean architecture.

#### Phase 2 — Database

- **Goal:** Build the SQLite data layer.
- **Actions:**
  - Create `users` and `tasks`.
  - Add relationships.
  - Add sample users.
  - Implement database operations.
- **Expected result:** Users and tasks can be safely created and retrieved.

#### Phase 3 — Pydantic Schemas

- **Goal:** Validate API inputs and outputs.
- **Actions:**
  - Create `ChatRequest`.
  - Create task request/response models.
  - Validate positive `user_id`.
  - Reject empty messages/titles.
- **Expected result:** Invalid requests are rejected before reaching business logic.

#### Phase 4 — Core Services & Tools

- **Goal:** Build the actual assistant capabilities.
- **Actions:**
  - Implement `get_user`.
  - Implement `create_task`.
  - Implement `list_tasks`.
  - Implement `get_weather`.
- **Expected result:** Each tool works independently before connecting it to the LLM.

#### Phase 5 — External Weather API

- **Goal:** Connect the weather service.
- **Actions:**
  - Implement API request.
  - Handle successful responses.
  - Handle invalid cities.
  - Handle timeout/HTTP failures.
  - Add retry logic.
- **Expected result:** Weather requests work reliably and failures produce meaningful errors.

#### Phase 6 — LLM Tool Calling

- **Goal:** Allow the LLM to select tools.
- **Actions:**
  - Register tool definitions with the LLM.
  - Send the user request.
  - Detect tool calls.
  - Execute requested tools.
  - Send tool results back to the LLM.
- **Expected result:** The model dynamically chooses the appropriate tool instead of using hardcoded sequences.

#### Phase 7 — Multi-Tool Orchestration

- **Goal:** Support multiple tools in one request.
- **Actions:**
  - Handle multiple tool calls from one LLM response.
  - Execute each requested tool.
  - Collect all results.
  - Send results back to the LLM.
  - Generate the final response.
- **Expected result:** A request such as *“What's the weather in Lahore and create a task to call Ahmed?”* can execute both operations.

#### Phase 8 — MCP

- **Goal:** Add MCP-based tool discovery and execution.
- **Actions:**
  - Create MCP server.
  - Expose `get_user` and `create_task`.
  - Create MCP client.
  - Connect client to server.
  - Discover tools.
  - Call discovered tools.
- **Expected result:** The application can interact with tools through MCP without building a large MCP framework.

#### Phase 9 — FastAPI Endpoints

- **Goal:** Expose functionality through HTTP.
- **Actions:**
  - Implement `POST /chat`.
  - Implement `GET /users/{user_id}`.
  - Implement `GET /users/{user_id}/tasks`.
  - Implement `POST /users/{user_id}/tasks`.
  - Add appropriate status codes.
- **Expected result:** All required API operations are accessible through HTTP.

#### Phase 10 — Streaming

- **Goal:** Stream the final LLM response.
- **Actions:**
  - Use FastAPI `StreamingResponse`.
  - Stream the final response incrementally.
  - Handle streaming failures.
- **Expected result:** `/chat` can return the final answer progressively instead of waiting for the complete response.

#### Phase 11 — Testing

- **Goal:** Verify each component and the complete workflow.
- **Actions:**
  - Test schemas.
  - Test database operations.
  - Test tools.
  - Test API endpoints.
  - Mock LLM/weather API.
  - Test failures and retries.
  - Test multi-tool chat.
- **Expected result:** Automated tests pass and major failure scenarios are covered.

#### Phase 12 — Documentation & Review

- **Goal:** Make the project understandable and explainable.
- **Actions:**
  - Write README.
  - Document setup and environment variables.
  - Explain architecture.
  - Add sample requests/responses.
  - Prepare explanations for technical review questions.
- **Expected result:** Another developer can install, run, test, and understand the project.


### 8. Assumptions

- The selected LLM supports both **tool calling and streaming**.
- SQLite is sufficient for this assessment.
- The weather API provides the required city/weather information.
- API credentials will be available through environment variables.
- Sample users can be inserted during database setup.
- MCP only needs to demonstrate the required minimal functionality.
- These assumptions should be verified during implementation rather than blindly relied upon.

### 9. Risks

| Risk | Severity | Likelihood | Handling |
|---|---|---|---|
| LLM produces invalid tool arguments | High | Medium | Pydantic/tool validation |
| Multiple tools aren't processed correctly | High | Medium | Dedicated orchestration tests |
| Weather API fails | Medium | Medium | Timeout + retry + meaningful error |
| Database operation fails | High | Low | Validation + safe queries + tests |
| MCP connection fails | High | Medium | Test client/server independently |
| Streaming breaks | Medium | Medium | Streaming-specific tests |
| Secrets exposed | High | Low | `.env` + `.gitignore` |
| External APIs make tests unreliable | Medium | High | Mock external services |

### 10. Validation Plan

- **Normal behavior:**
  - Get user.
  - Create task.
  - List tasks.
  - Get weather.
  - Send a normal `/chat` request.
  - Send a multi-tool request.

- **Invalid inputs:**
  - `user_id <= 0`.
  - Empty message.
  - Empty task title.
  - Non-existent user.
  - Invalid city.

- **Failures:**
  - Weather API timeout.
  - Weather API HTTP error.
  - LLM failure.
  - Tool execution failure.
  - MCP connection failure.
  - Database failure.

- **Integration:**
  - Verify `LLM → tools → results → LLM → final response`.
  - Verify that multiple tools can execute in one request.
  - Verify final streamed output.
  - Verify tests are independent of real external APIs.

### 11. Expected Deliverable

- Python/FastAPI project.
- Clean `app/` architecture.
- SQLite database setup.
- LLM tool-calling implementation.
- Weather service.
- MCP server and client.
- Pydantic schemas.
- Retry/error-handling logic.
- Streaming `/chat`.
- Automated tests.
- `.env.example`.
- `requirements.txt`.
- `README.md`.
- Sample requests/responses.

### 12. Completion Criteria

The project is finished when:

- All required FastAPI endpoints work.
- SQLite users/tasks operations work correctly.
- Pydantic validation works.
- LLM dynamically selects tools.
- Multiple tools can execute in one request.
- Weather API integration works with failure handling.
- Retry behavior is implemented correctly.
- MCP server/client work.
- `/chat` supports streaming.
- Automated tests pass.
- External APIs are mocked in tests.
- README explains setup, architecture, and usage.
- I can explain **why each component exists and how it works**.

