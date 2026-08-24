
# Personal Finance Assistant

An AI-powered personal finance assistant built with **Python, Groq LLM, tool calling, SQLite, MCP, and FastAPI**. The system can understand finance-related user requests, select the appropriate tool, execute the operation, and return a natural-language response.

---

## 1. Project Purpose

The purpose of this project is to build a practical **LLM-powered personal finance assistant** that demonstrates how modern AI applications can connect an LLM with external tools, APIs, and local data.

Instead of relying only on the LLM's internal knowledge, the assistant can use specialized tools when real operations or external information are required.

For example:

```text
User: "Calculate 15000 - 4500 + 2000"

        ↓

LLM
        ↓
calculator tool
        ↓
12,500
        ↓
Natural-language response
````

For database-related questions:

```text
User: "How much did I spend on food?"

        ↓
LLM
        ↓
get_expenses tool
        ↓
SQLite database
        ↓
5,000 PKR
        ↓
Natural-language response
```

The project therefore demonstrates the complete pipeline of:

**LLM → Tool Selection → Tool Execution → External/Local Data → Final Response**

---

# 2. Project Functionalities

The assistant currently supports the following functionality.

## 2.1 Arithmetic Calculations

The assistant can perform basic arithmetic operations such as:

* Addition
* Subtraction
* Multiplication
* Division
* Modulo
* Powers
* Negative numbers

Example:

```text
Calculate 15000 - 4500 + 2000
```

Response:

```text
The result of the calculation is 12,500.
```

The calculator uses Python's `ast` module rather than directly using `eval()`, providing safer expression evaluation.

---

## 2.2 Currency Conversion

The assistant can convert currencies using the **Frankfurter API**.

Example:

```text
Convert 100 USD to PKR
```

The tool obtains the exchange rate from the external API and calculates the converted amount.

Example result:

```text
100 USD ≈ 27,817 PKR
```

The exchange rate is obtained dynamically rather than being hardcoded.

---

## 2.3 Expense Retrieval

The assistant can retrieve expenses stored in the local SQLite database.

Example:

```text
Show me all my expenses
```

It can also filter expenses by category:

```text
How much did I spend on food?
```

The database currently contains sample expense records such as:

| Category      | Amount | Currency |
| ------------- | -----: | -------- |
| Food          |  5,000 | PKR      |
| Transport     |  3,000 | PKR      |
| Shopping      |  8,000 | PKR      |
| Bills         |  4,000 | PKR      |
| Entertainment |  2,500 | PKR      |

---

## 2.4 Multiple Tool Usage

The LLM can use multiple tools to answer a single request.

For example:

```text
Show me my food expenses and convert the total to USD.
```

The system used:

```text
get_expenses
      ↓
Food = 5,000 PKR
      ↓
currency_converter
      ↓
≈ $17.95 USD
```

This demonstrates **multi-tool orchestration**.

---

## 2.5 Streaming Responses

The project includes a streaming endpoint:

```text
POST /chat/stream
```

The assistant can stream generated response text instead of waiting for the complete response before returning it.

---

## 2.6 Error Handling

The project includes error handling for:

* Invalid arithmetic expressions
* Unknown tools
* Missing tool arguments
* Currency API timeout
* Currency API request failures
* LLM API failures
* Invalid API input
* Pydantic validation errors
* Maximum tool execution rounds

---

## 2.7 Retry Mechanism

Transient LLM failures are handled using retry logic with exponential backoff.

The current configuration allows up to:

```text
MAX_RETRIES = 3
```

The retry delays follow:

```text
Attempt 1 → 1 second
Attempt 2 → 2 seconds
Attempt 3 → 4 seconds
```

This helps handle temporary API failures without immediately terminating the application.

---

## 2.8 Usage Logging and Cost Estimation

The system tracks:

* Input tokens
* Output tokens
* Total tokens
* Estimated API cost

Example:

```json
{
    "input_tokens": 862,
    "output_tokens": 75,
    "total_tokens": 937,
    "estimated_cost": 0.0001743
}
```

This provides visibility into LLM usage and estimated operational cost.

---

# 3. Technology Stack

| Technology      | Purpose                               |
| --------------- | ------------------------------------- |
| Python          | Main programming language             |
| Groq            | LLM API provider                      |
| GPT-OSS-120B    | LLM used by the application           |
| Pydantic        | Data validation and structured models |
| SQLite          | Local expense database                |
| FastAPI         | HTTP API layer                        |
| Uvicorn         | ASGI server                           |
| MCP             | Tool/system interoperability          |
| Requests        | External HTTP requests                |
| Frankfurter API | Currency exchange rates               |
| python-dotenv   | Environment variable management       |
| asyncio         | Asynchronous MCP client               |
| logging         | Application/usage logging             |

---

# 4. Tools Used by the Assistant

The project uses three primary finance tools.

| Tool                 | Type                 | Purpose                 | Data Source     |
| -------------------- | -------------------- | ----------------------- | --------------- |
| `calculator`         | Internal Python tool | Arithmetic calculations | Python          |
| `currency_converter` | External API tool    | Currency conversion     | Frankfurter API |
| `get_expenses`       | Local database tool  | Retrieve expenses       | SQLite          |

## Tool 1 — Calculator

```text
Tool name:
calculator
```

Implementation:

```python
calculator(expression: str)
```

Example:

```text
4500 + 2300 - 800
```

Result:

```text
6000
```

---

## Tool 2 — Currency Converter

```text
Tool name:
currency_converter
```

Implementation:

```python
currency_converter(
    amount,
    from_currency,
    to_currency
)
```

Example:

```text
100 USD → PKR
```

The tool calls the external Frankfurter API to retrieve the exchange rate.

---

## Tool 3 — Expense Database

```text
Tool name:
get_expenses
```

Implementation:

```python
get_expenses(category: str | None = None)
```

It queries:

```text
data/expenses.db
```

and returns the stored expense records.

---

# 5. Tool Calling Architecture

The LLM is provided with the schemas of the available tools.

The LLM decides whether a tool is required.

For example:

```text
"Calculate 5000 + 3000"
```

LLM decision:

```text
calculator
```

While:

```text
"Convert 100 USD to PKR"
```

results in:

```text
currency_converter
```

And:

```text
"Show me my expenses"
```

results in:

```text
get_expenses
```

The general flow is:

```text
User Request
     ↓
System Prompt
     ↓
Groq LLM
     ↓
Tool Selection
     ↓
Tool Execution
     ↓
Tool Result
     ↓
LLM
     ↓
Final Response
```

---

# 6. Database

The project uses **SQLite** for local expense storage.

Database location:

```text
data/expenses.db
```

The database contains an `expenses` table with:

| Column         | Type    | Description         |
| -------------- | ------- | ------------------- |
| `id`           | INTEGER | Unique expense ID   |
| `category`     | TEXT    | Expense category    |
| `amount`       | REAL    | Expense amount      |
| `currency`     | TEXT    | Currency code       |
| `description`  | TEXT    | Expense description |
| `expense_date` | TEXT    | Date of expense     |

The database is initialized automatically by:

```text
app/database.py
```

If the database is empty, the application currently inserts sample expense records for development/testing.

---

# 7. MCP Integration

The project also demonstrates **Model Context Protocol (MCP)**.

The project contains:

```text
mcp_server/
├── server.py
└── client.py
```

The MCP server exposes the local expense functionality as an MCP tool.

Current MCP tool:

```text
get_user_expenses
```

The MCP client successfully connects to the server and retrieves expense data.

The MCP architecture is:

```text
MCP Client
     ↓
MCP Server
     ↓
get_user_expenses
     ↓
database.py
     ↓
expenses.db
```

This demonstrates how an application can expose local functionality through MCP rather than tightly coupling every system directly to the database.

---

# 8. FastAPI API

The application exposes the assistant through **FastAPI**.

> This project uses **FastAPI**, not a manually built REST framework. FastAPI provides HTTP endpoints, request validation, and streaming support.

## Health Check

```http
GET /health
```

Example:

```json
{
    "status": "healthy",
    "service": "personal-finance-assistant"
}
```

---

## Chat Endpoint

```http
POST /chat
```

Request:

```json
{
    "message": "Calculate 4500 + 2300 - 800"
}
```

Response contains:

* Assistant answer
* Tools used
* Status
* Tool results
* Token usage
* Estimated cost

---

## Streaming Endpoint

```http
POST /chat/stream
```

Request:

```json
{
    "message": "Calculate 5000 + 3000"
}
```

The response is streamed to the client.

---

# 9. Pydantic Validation

Pydantic is used to validate API input and application responses.

The FastAPI request model is:

```python
class ChatRequest(BaseModel):
    message: str
```

Therefore:

## Valid

```json
{
    "message": "Calculate 100 + 200"
}
```

## Invalid

```json
{
    "message": 12345
}
```

FastAPI correctly returns a validation error because `message` must be a string.

Similarly, missing input:

```json
{}
```

is rejected.

---

# 10. Error Handling

The project implements error handling at multiple layers.

## Calculator

Invalid:

```text
hello + 5
```

Result:

```text
Only basic arithmetic expressions are supported
```

## Unknown Tool

```text
fake_tool
```

Result:

```text
Unknown tool: fake_tool
```

## Missing Tool Argument

Calling the calculator without an expression is handled and returned as a structured error.

## Currency API

The application handles:

* Timeout
* HTTP/request failures
* Other exceptions

## LLM

The application handles transient failures using retry logic.

---

# 11. Testing

The project was tested at both the **individual tool level** and the **end-to-end API level**.

## 11.1 Tool-Level Tests

| Test                   | Input               | Expected Result            | Status |
| ---------------------- | ------------------- | -------------------------- | ------ |
| Calculator valid       | `5000 + 3000`       | `8000`                     | Passed |
| Calculator invalid     | `hello + 5`         | Error                      | Passed |
| Unknown tool           | `fake_tool`         | Unknown-tool error         | Passed |
| Missing argument       | `calculator {}`     | Validation/execution error | Passed |
| Expense tool           | `get_expenses()`    | Expense records            | Passed |
| Pydantic invalid types | Wrong field types   | Validation errors          | Passed |
| MCP server loading     | Import server       | Server loads               | Passed |
| MCP client             | `get_user_expenses` | Expense data               | Passed |

---

# 12. End-to-End API Test Cases

The following tests were executed through the running FastAPI application.

| # | Test Case              | Input                      | Tool Used                            | Result                                                                           |
| - | ---------------------- | -------------------------- | ------------------------------------ | -------------------------------------------------------------------------------- |
| 1 | Arithmetic calculation | `15000 - 4500 + 2000`      | `calculator`                         | 12,500                                                                           |
| 2 | Retrieve all expenses  | `Show me all my expenses`  | `get_expenses`                       | 5 expenses retrieved                                                             |
| 3 | Currency conversion    | `Convert 100 USD to PKR`   | `currency_converter`                 | Conversion completed                                                             |
| 4 | Multi-tool request     | Food expenses → USD        | `get_expenses`, `currency_converter` | Both tools executed                                                              |
| 5 | Streaming              | `Calculate 25000 - 7500`   | `calculator`                         | Streaming endpoint responded, but output behavior still needs final verification |
| 6 | Empty message          | `""`                       | None                                 | Handled                                                                          |
| 7 | Missing message        | `{}`                       | None                                 | Pydantic rejected request                                                        |
| 8 | Wrong input type       | `message=12345`            | None                                 | Pydantic rejected request                                                        |
| 9 | Finance advice         | Monthly expense management | None                                 | Natural-language response                                                        |

## Important Multi-Tool Test

The following request successfully demonstrated multi-tool orchestration:

```text
Show me my food expenses and convert the total to USD
```

The system selected:

```text
get_expenses
      ↓
5000 PKR
      ↓
currency_converter
      ↓
17.95 USD
```

Result:

```text
Your food expenses total 5,000 PKR,
which converts to approximately $17.95 USD.
```

---

# 13. Project Structure

The project follows a modular structure:

```text
personal-finance-assistant/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── llm.py
│   ├── main.py
│   ├── models.py
│   └── tools.py
│
├── data/
│   └── expenses.db
│
├── mcp_server/
│   ├── client.py
│   └── server.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 14. Important Files

| File                   | Responsibility                                                         |
| ---------------------- | ---------------------------------------------------------------------- |
| `app/main.py`          | FastAPI application and API endpoints                                  |
| `app/llm.py`           | LLM communication, tool calling, retries, streaming and usage tracking |
| `app/tools.py`         | Finance tool implementations                                           |
| `app/database.py`      | SQLite database operations                                             |
| `app/models.py`        | Pydantic response/tool models                                          |
| `mcp_server/server.py` | MCP server                                                             |
| `mcp_server/client.py` | MCP client                                                             |
| `data/expenses.db`     | SQLite expense database                                                |
| `.env`                 | API configuration/secrets                                              |

---

# 15. Running the Project

## 1. Activate virtual environment

```bash
source .venv/bin/activate
```

## 2. Configure environment variables

Create `.env`:

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=openai/gpt-oss-120b
```

## 3. Start FastAPI

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

## 4. Test health

```bash
curl http://127.0.0.1:8000/health
```

## 5. Test the assistant

```bash
curl -X POST http://127.0.0.1:8000/chat \
-H "Content-Type: application/json" \
-d '{"message":"Calculate 5000 + 3000"}'
```

---

# 16. MCP Testing

Test that the MCP server can be imported:

```bash
python -c "from mcp_server.server import mcp; print('MCP server loaded:', mcp.name)"
```

Test the MCP client:

```bash
python mcp_server/client.py
```

Expected:

```text
Available MCP tools:
- get_user_expenses
```

The client should then retrieve the expense records from the database.

---

# 17. Security Considerations

The project includes several basic security practices:

* API key stored through environment variables
* `.env` should not be committed to Git
* Calculator avoids unrestricted `eval()`
* Pydantic validates API input
* External API requests use timeouts
* Tool execution errors are caught
* LLM retries are limited
* Tool execution rounds are limited

For production deployment, additional authentication, authorization, rate limiting, encrypted secrets management, and stronger database controls would be recommended.

---

# 18. Limitations

This is currently a **learning/demo project**, so it has some limitations:

* Expense records are currently sample data.
* There is no user authentication or separate user accounts.
* Expense creation/update/delete functionality is not currently implemented.
* SQLite is suitable for this demonstration but may not be ideal for a large production system.
* Currency conversion depends on an external API.
* LLM responses can still vary because they are generated by a language model.
* The streaming implementation requires a final verification/fix before being considered completely production-ready.
* A final CLI interface is still a remaining project task.

---

# 19. Future Improvements

Possible future improvements include:

* Add expense creation
* Add expense deletion/update
* Add monthly expense summaries
* Add category-wise analytics
* Add budgeting functionality
* Add authentication and multiple users
* Add persistent conversation history
* Add a proper CLI interface
* Add automated unit tests with `pytest`
* Add Docker support
* Add production database such as PostgreSQL
* Improve streaming implementation
* Add comprehensive logging
* Add monitoring and observability

---


---

# 20. What This Project Demonstrates

This project demonstrates practical implementation of several important AI engineering concepts:

* LLM API integration
* Prompt engineering
* Function/tool calling
* Tool schema definition
* Pydantic validation
* Safe tool execution
* External API integration
* Local database integration
* Multi-tool orchestration
* MCP server/client architecture
* Streaming responses
* Retry mechanisms
* Error handling
* Token usage tracking
* Cost estimation
* FastAPI API development
* End-to-end testing

The key concept demonstrated by the project is that an LLM does **not need to perform every operation itself**. Instead, it can determine which specialized tool is required, call that tool, receive the result, and use that result to produce the final response.

---


