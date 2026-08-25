
# Company Assistant — Technical Project Report

## 1. Project Overview

**Company Assistant** is a FastAPI-based AI assistant that combines an LLM with application services, SQLite persistence, external APIs, tool calling, and MCP.

The system allows a user to interact with a single `/chat` endpoint while the assistant determines what action is required. Depending on the request, it can:

- Retrieve user information.
- Create tasks.
- Retrieve existing tasks.
- Retrieve weather information.
- Reject requests outside the assistant's intended scope.
- Persist application data in SQLite.
- Use MCP to expose application capabilities as tools.
- Use the LLM to decide when a tool should be invoked.

The project demonstrates an end-to-end architecture:

```text
Client
  ↓
FastAPI
  ↓
LLM Service
  ↓
LLM decides what to do
  ↓
Tool / MCP layer
  ↓
Service layer
  ↓
Database / External API
  ↓
Tool result
  ↓
LLM
  ↓
Final response
````

---

# 2. Project Objectives

The primary objectives of the project are:

1. Build a production-style FastAPI application around an LLM.
2. Separate API, business logic, database, LLM, and tool responsibilities.
3. Implement structured request validation using Pydantic.
4. Persist users and tasks using SQLite.
5. Integrate an external weather API/tool.
6. Implement MCP-based tool exposure and execution.
7. Allow the LLM to select appropriate tools based on user intent.
8. Handle invalid or unsupported requests gracefully.
9. Provide a foundation that can be extended with additional tools and services.

---

# 3. Core Technologies

| Technology            | Purpose                                     |
| --------------------- | ------------------------------------------- |
| Python                | Primary programming language                |
| FastAPI               | HTTP API framework                          |
| Uvicorn               | ASGI application server                     |
| Pydantic              | Request/response validation                 |
| SQLite                | Persistent application database             |
| Groq / LLM API        | Language-model reasoning and tool selection |
| MCP                   | Standardized tool communication             |
| `httpx` / HTTP client | External API communication                                          |
| `.env`                | Environment configuration                   |

---

# 4. Setup

## 4.1 Clone/Open the Project

Open the project directory:

```bash
cd ai-task-assistant
```

---

## 4.2 Create a Virtual Environment

```bash
python3 -m venv .venv
```

Activate it:

### macOS/Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

After activation, the terminal should show something similar to:

```text
(.venv)
```

---

## 4.3 Install Dependencies

Install the project's dependencies:

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available, the project dependencies can be installed individually according to the project's imports, for example:

```bash
pip install fastapi uvicorn pydantic python-dotenv httpx mcp pytest
```

---

# 5. Environment Variables

Sensitive configuration should not be hard-coded inside Python files.

Create a `.env` file in the project root.

Example:

```text
GROQ_API_KEY=your_groq_api_key
WEATHER_API_KEY=your_weather_api_key
```

If the application uses different names, the names must exactly match the variables expected by the configuration code.

### Important

The `.env` file should **not** be committed to Git.

Add:

```text
.env
```

to `.gitignore`.

Environment variables provide a clean separation between:

```text
Application code
        +
Environment-specific configuration
        +
Secret credentials
```

This prevents credentials from becoming part of the source code.

---

# 6. Database Setup

The project uses SQLite for persistent storage.

The database file is:

```text
company_assistant.db
```

The database contains tables such as:

```text
users
tasks
```

Conceptually:

```text
users
--------------------------------
id
name
email
created_at


tasks
--------------------------------
id
user_id
title
completed
created_at
```

The relationship is:

```text
users
  │
  └──────< tasks
```

One user can therefore have multiple tasks.

---

# 7. Running the Application

Start the FastAPI application from the project root:

```bash
uvicorn app.main:app --reload
```

The application will normally be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is available at:

```text
http://127.0.0.1:8000/docs
```

The Swagger interface can be used to test the API without manually writing `curl` commands.

---

# 8. API Endpoints

## 8.1 Root Endpoint

```http
GET /
```

Purpose:

* Verify that the API is running.
* Provide a basic health-style response.

Example:

```json
{
    "message": "Company Assistant API is running"
}
```

---

## 8.2 Create User Endpoint

```http
POST /users
```

Purpose:

* Create a new user.
* Store the user in SQLite.
* Return the newly created user.

Example request:

```json
{
    "name": "Ahmed",
    "email": "ahmed@example.com"
}
```

---

## 8.3 Chat Endpoint

```http
POST /chat
```

This is the primary AI interaction endpoint.

Example:

```json
{
    "user_id": 1,
    "message": "What is the weather in Lahore?"
}
```

The request enters the LLM service, where the assistant determines what operation is appropriate.

---

# 9. Running Tests

If the project uses `pytest`, execute:

```bash
pytest
```

For more detailed output:

```bash
pytest -v
```

To run a particular test file:

```bash
pytest tests/test_assistant.py -v
```

Testing should cover both individual components and the complete assistant workflow.

---

# 10. Architecture

The project follows a layered architecture.

```text
                 ┌─────────────────┐
                 │     Client      │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │   API Layer     │
                 │    FastAPI      │
                 └────────┬────────┘
                          │
                          ▼
                 ┌─────────────────┐
                 │  Service Layer  │
                 │ Business Logic  │
                 └────────┬────────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       ┌─────────────┐        ┌─────────────┐
       │ LLM Layer   │        │ MCP Layer   │
       └──────┬──────┘        └──────┬──────┘
              │                      │
              └──────────┬───────────┘
                         ▼
                  ┌─────────────┐
                  │ Tool Layer  │
                  └──────┬──────┘
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
       ┌─────────────┐       ┌─────────────┐
       │  Database   │       │ External API│
       │   SQLite    │       │   Weather   │
       └─────────────┘       └─────────────┘
```

---

# 11. API Layer

The API layer is responsible for handling HTTP requests.

Main file:

```text
app/main.py
```

It defines endpoints such as:

```python
@app.get("/")
```

```python
@app.post("/users")
```

```python
@app.post("/chat")
```

The API layer should **not** contain the actual business logic.

Instead, it receives validated data and delegates the work to services.

For example:

```python
@app.post("/chat")
async def chat(request: ChatRequest):
    response = await run_assistant(
        request.message,
        request.user_id
    )

    return {"response": response}
```

The important architectural idea is:

> **FastAPI handles HTTP; services handle application logic.**

---

# 12. Schema / Validation Layer

Main file:

```text
app/models/schemas.py
```

Pydantic models define what the API accepts and returns.

For example:

```python
class ChatRequest(BaseModel):
    user_id: int
    message: str
```

Validation prevents malformed requests from entering the application.

For example, an invalid request such as:

```json
{
    "user_id": -1,
    "message": ""
}
```

can be rejected before the business logic executes.

This is why the API may return:

```text
422 Unprocessable Content
```

A `422` response generally indicates that the request did not satisfy the declared Pydantic schema.

---

# 13. Service Layer

The service layer contains application/business operations.

Typical files include:

```text
app/services/user_service.py
app/services/task_service.py
app/services/llm_service.py
```

## `user_service.py`

Responsible for operations involving users.

Examples:

```python
get_user(user_id)
```

Retrieves a user from SQLite.

```python
create_user(name, email)
```

Creates and stores a new user.

---

## `task_service.py`

Responsible for task-related operations.

Typical responsibilities include:

```text
create task
retrieve tasks
update task
delete task
```

The service layer isolates database operations from the API.

---

# 14. Database Layer

Typical file:

```text
app/database/database.py
```

Its responsibility is to manage database connectivity.

The service layer can request a connection:

```python
connection = get_connection()
```

and then execute SQL.

For example:

```sql
SELECT * FROM users WHERE id = ?
```

The database layer therefore provides the foundation for persistence without forcing every part of the application to manage SQLite connections independently.

---

# 15. LLM Layer

Main file:

```text
app/services/llm_service.py
```

This is one of the most important components.

The LLM service:

1. Receives the user's message.
2. Provides the model with the available capabilities/tools.
3. Sends the request to the LLM.
4. Determines whether the model requested a tool.
5. Executes the requested tool through MCP.
6. Sends the tool result back to the LLM when required.
7. Produces the final natural-language response.

Conceptually:

```text
User message
     ↓
LLM
     ↓
Does this require a tool?
     ↓
 ┌───┴────┐
No       Yes
 │         │
 ▼         ▼
Answer   MCP tool
           ↓
       Tool result
           ↓
          LLM
           ↓
        Answer
```

This is the central orchestration component.

---

# 16. Tool Layer

Tools represent capabilities that the LLM can use.

Examples in this project include:

```text
get_user
create_user
create_task
list_tasks
get_weather
```

The LLM does not directly manipulate SQLite or external services.

Instead:

```text
LLM
 ↓
Tool
 ↓
Service
 ↓
Database/API
```

This separation is important because it prevents the LLM from directly controlling application infrastructure.

---

# 17. MCP Layer

The MCP implementation is located under:

```text
app/mcp/
```

Important files include:

```text
app/mcp/server.py
app/mcp/client.py
```

The MCP server exposes application capabilities as standardized tools.

For example:

```text
get_user
create_task
list_tasks
get_weather
```

The MCP client connects to the MCP server and invokes the requested tool.

The flow is:

```text
LLM Service
     ↓
MCP Client
     ↓
MCP Server
     ↓
Requested Tool
     ↓
Service Function
     ↓
Database / API
```

This creates a clean boundary between the assistant/orchestration side and the tools that provide actual capabilities.

---

# 18. Example: Getting User Information

User asks:

```text
Tell me my user information
```

The flow is:

```text
POST /chat
     ↓
ChatRequest validation
     ↓
run_assistant()
     ↓
LLM identifies get_user
     ↓
MCP client
     ↓
MCP server
     ↓
get_user(user_id=1)
     ↓
SQLite
     ↓
User record
     ↓
LLM
     ↓
Final response
```

Example response:

```json
{
    "response": "{\"id\": 1, \"name\": \"Ahmed\", \"email\": \"ahmed@example.com\", \"created_at\": \"2026-08-24 11:49:56\"}"
}
```

---

# 19. Example: Weather

Request:

```json
{
    "user_id": 1,
    "message": "What is the weather in Lahore?"
}
```

The LLM identifies that weather information is required.

It selects:

```text
get_weather
```

The tool receives:

```json
{
    "city": "Lahore"
}
```

The tool retrieves the weather information and returns it to the assistant.

Example:

```json
{
    "response": "The current weather in Lahore is 30 °C and sunny."
}
```

---

# 20. Example: Creating a Task

Request:

```json
{
    "user_id": 1,
    "message": "Create a task to finish my project"
}
```

The assistant identifies the task-creation intent.

It invokes:

```text
create_task
```

with approximately:

```json
{
    "user_id": 1,
    "title": "finish my project"
}
```

The task service stores the task in SQLite.

The assistant then returns:

```text
Task created successfully. The new task is titled "finish my project".
```

---

# 21. Example Request

### Request

```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"user_id":1,"message":"What is the weather in Lahore?"}'
```

### Response

```json
{
    "response": "The current weather in Lahore is 30 °C and sunny."
}
```

---

# 22. Create User Example

### Request

```bash
curl -X POST http://127.0.0.1:8000/users \
-H "Content-Type: application/json" \
-d '{"name":"Ali","email":"ali@example.com"}'
```

### Response

Conceptually:

```json
{
    "id": 2,
    "name": "Ali",
    "email": "ali@example.com",
    "created_at": "2026-08-25T10:00:00"
}
```

The exact response depends on the implementation of the endpoint and response schema.

---

# 23. Important Distinction: `/users` vs `/chat`

The project intentionally separates direct API operations from AI interaction.

### `/users`

```text
POST /users
```

is a conventional API endpoint.

It directly represents:

```text
Create user
```

### `/chat`

```text
POST /chat
```

is the AI interface.

The user can communicate naturally:

```text
"Tell me my user information"
```

or:

```text
"Create a task to finish my project"
```

The LLM determines which capability is needed.

Therefore:

```text
/users
    ↓
Direct application operation


/chat
    ↓
Natural language
    ↓
LLM
    ↓
Tool selection
    ↓
Application operation
```

---

# 24. Debugging Scenario

## Problem

Assume the following bug occurs:

> When the user asks the assistant to create a task and retrieve the weather in the same request, the first tool works but the second tool is never executed.

For example:

```text
Create a task called "Prepare presentation" and tell me the weather in Lahore.
```

Expected:

```text
LLM
 ↓
create_task
 ↓
task created
 ↓
get_weather
 ↓
weather retrieved
 ↓
LLM
 ↓
final answer
```

Actual:

```text
LLM
 ↓
create_task
 ↓
task created
 ↓
STOP
```

The second tool never executes.

---

# 25. Investigation Strategy

The first step is **not** to immediately modify the code.

First determine where the execution pipeline stops.

Trace the request through every layer:

```text
HTTP request
    ↓
FastAPI
    ↓
run_assistant()
    ↓
LLM response
    ↓
tool calls
    ↓
MCP client
    ↓
MCP server
    ↓
tool execution
    ↓
tool result
    ↓
LLM continuation
```


---

# 26. Logs to Check

## 26.1 FastAPI Logs

Check whether the request reaches:

```text
POST /chat
```

Example:

```text
POST /chat 200 OK
```

---

## 26.2 LLM Tool-Call Logs

Inspect the raw LLM response.

Determine whether the LLM returned:

```text
create_task
```

only, or:

```text
create_task
get_weather
```

This distinction is critical.

### Case A

LLM returns:

```text
create_task
```

only.

Then the problem may be in:

* prompt design
* tool definitions
* model behavior
* tool selection
* multi-tool orchestration

### Case B

LLM returns both:

```text
create_task
get_weather
```

but only the first executes.

Then the problem is probably in the orchestration/execution loop.

---

# 27. MCP Logs

Check the MCP server logs.

You should see something similar to:

```text
tools/call -> create_task
tools/call -> get_weather
```

If only:

```text
tools/call -> create_task
```

appears, the second call never reached the MCP server.

If both appear but weather fails, the problem is inside the weather tool.


# 28. Error Handling

The application should distinguish between different classes of errors.

### Validation Error

Example:

```text
422 Unprocessable Content
```

Occurs when the request does not satisfy the Pydantic schema.

---

### Application Error

Example:

```text
User not found
```

Occurs when valid input refers to unavailable application data.

---

### Tool Error

Example:

```text
Unknown tool: get_weather
```

Occurs when the requested tool is not registered by the MCP server.

---

### External API Error

Occurs when the weather service fails or returns an invalid response.

---

### LLM Error

Can occur because of:

* API failure
* invalid request
* rate limit
* malformed tool call
* unavailable model

A robust application should log these failures and return controlled responses instead of exposing raw stack traces to users.

---

# 29. Project File Responsibilities

A high-level mapping of the project is:

```text
app/
│
├── main.py
│   └── FastAPI application and HTTP endpoints
│
├── models/
│   └── schemas.py
│       └── Pydantic request/response models
│
├── database/
│   └── database.py
│       └── SQLite connection/database handling
│
├── services/
│   ├── user_service.py
│   │   └── User operations
│   │
│   ├── task_service.py
│   │   └── Task operations
│   │
│   └── llm_service.py
│       └── LLM interaction and orchestration
│
└── mcp/
    ├── server.py
    │   └── MCP tool definitions and execution
    │
    └── client.py
        └── MCP server communication
```

---

# 30. Complete System Flow

The complete application can be understood through this pipeline:

```text
                         USER
                           │
                           ▼
                    POST /chat
                           │
                           ▼
                    Pydantic Schema
                           │
                           ▼
                    FastAPI Endpoint
                           │
                           ▼
                    LLM Service
                           │
                           ▼
                     LLM Decision
                           │
              ┌────────────┼────────────┐
              │            │            │
              ▼            ▼            ▼
          get_user    create_task   get_weather
              │            │            │
              └────────────┼────────────┘
                           ▼
                       MCP Client
                           │
                           ▼
                       MCP Server
                           │
                           ▼
                     Tool Execution
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
           SQLite                  External API
              │                         │
              └────────────┬────────────┘
                           ▼
                       Tool Result
                           │
                           ▼
                          LLM
                           │
                           ▼
                    Final Response
                           │
                           ▼
                       FastAPI
                           │
                           ▼
                         USER
```

---

# 31. Key Engineering Principles Demonstrated

### Separation of Concerns

Each layer has a specific responsibility.

```text
API → HTTP
Service → Business logic
Database → Persistence
LLM → Reasoning
Tool → Capability
MCP → Tool communication
```

---

### Validation

Pydantic prevents invalid data from entering the application.

---

### Persistence

SQLite ensures user and task information survives application restarts.

---

### Tool Calling

The LLM can translate natural-language requests into structured operations.

---

### Multi-Tool Orchestration

A single user request can require multiple independent tools.

---

### MCP

MCP provides a standardized interface between the assistant and its tools.

---

### Modularity

A new capability can be introduced as another tool rather than rewriting the entire assistant.

For example:

```text
send_email
search_documents
create_calendar_event
get_company_policy
```

can later become additional tools.

---

# 32. Final Project Outcome

The completed project demonstrates a complete **AI application pipeline**, rather than merely an LLM API call.

The system combines:

```text
FastAPI
+
Pydantic
+
SQLite
+
Service Architecture
+
LLM
+
Tool Calling
+
External API
+
MCP
+
Testing
+
Error Handling
```

The most important architectural outcome is that the LLM is **not directly responsible for performing application operations**.

Instead, it decides **what capability is required**, while deterministic application code performs the actual operation:

```text
LLM = Decision maker
Tool = Capability
Service = Business logic
Database/API = Data source
MCP = Communication layer
FastAPI = Application interface
```

That separation is what turns the project from a simple chatbot into a structured, extensible **AI task assistant system**.

