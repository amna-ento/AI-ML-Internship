
# Initial Plan

## 1. Objective

### What am I going to do?

Build a simple Personal Finance Assistant that uses an LLM with tool calling to handle financial tasks. The assistant will provide at least three working tools: a calculator, an external currency-conversion API, and a local SQLite database query tool exposed through an MCP server. The project will also demonstrate Pydantic validation, streaming responses, retry with backoff, error handling, and token/cost logging.

### Why am I doing it?

The main purpose is to practically learn and demonstrate advanced LLM application concepts including model-driven tool selection, tool execution, MCP integration, structured validation, streaming, reliability, and observability. The project should also provide a realistic finance-related use case rather than isolated tool-calling examples.

### Expected Final Result

A working CLI-based Personal Finance Assistant that can:
- Perform calculations.
- Convert currencies using an external API.
- Query personal expense information from a local SQLite database.
- Use the LLM to decide which tool is required without hardcoded routing.
- Provide streamed final responses.
- Validate outputs with Pydantic before they are used.
- Retry transient failures with backoff.
- Handle rate limits, timeouts, malformed model output, and tool failures gracefully.
- Log token usage and estimated cost for each LLM request.
- Connect to one MCP server and use its database functionality.


---

# 2. Context

## Background

This project is intended as a practical exercise for learning LLM APIs and tool-calling architecture. The application will use an LLM that can select tools based on the user's natural-language request.

The project will intentionally remain small and focused. It will not include unnecessary frontend, authentication, deployment, or large framework layers.

The finance assistant will combine three useful capabilities into one application:

1. Mathematical calculations.
2. Currency conversion.
3. Expense-related database queries and management suggestions.

## Current Situation

The project has not yet been implemented. The requirements and learning objectives have been identified, but the project structure, dependencies, database, tools, MCP server, validation, error handling, and tests still need to be implemented.

## Relevant Information

- The application will be CLI-based.
- The LLM will decide which tool to call.
- A calculator will be implemented as an internal tool.
- Currency conversion will use an external currency API.
- SQLite will be used as the local database.
- The database functionality will be exposed through an MCP server.
- Pydantic will be used for validation.
- LLM responses will support streaming.
- Transient failures will use retry with backoff.
- Token usage and estimated cost will be logged.
- The project should use a minimal number of files and folders.
- The project must be testable by another person after implementation.

## Constraints

- Keep the architecture simple and easy to understand.
- Avoid unnecessary files, folders, and frameworks.
- Do not use hardcoded keyword-based tool routing.
- All required outputs must be validated before use.
- The project must demonstrate all listed learning topics.
- The project should be possible to run locally.
- Dependencies must be checked and installed before implementation.
- Code should remain concise and maintainable.
- The project should be suitable for systematic testing.


---

# 3. Understanding

Before starting implementation, explain my understanding of the work in my own words.

### My Understanding

I need to build a small but complete Personal Finance Assistant where the LLM acts as the decision-maker. Instead of manually checking the user's request and selecting a tool, the LLM will receive the available tools and decide whether it needs the calculator, currency API, or expense database.

The selected tool will execute, return its result, and the result will be validated before being passed back into the LLM. The final response will then be generated and streamed to the user.

The application must also demonstrate production-oriented reliability features such as retries, timeouts, graceful error handling, token tracking, and estimated cost logging.

### Inputs

- User's natural-language finance request.
- Calculator expressions.
- Currency amount and currency codes.
- Expense-related questions.
- Local SQLite database containing expense records.
- External currency API responses.
- LLM tool calls and responses.
- Environment variables such as the LLM API key.

### Outputs

- Calculated results.
- Currency conversion results.
- Expense summaries.
- Expense-management suggestions.
- Streamed natural-language responses.
- Structured and validated tool/final response data.
- Token usage information.
- Estimated request cost.
- Gracefully handled error messages when operations fail.

### Dependencies

- Python environment.
- LLM API.
- LLM SDK.
- Pydantic.
- SQLite.
- External currency API.
- MCP library.
- Python environment variables.
- Testing framework.
- Internet connection for the LLM and currency API.


---

# 4. Initial Investigation

Before deciding how to implement the work, investigate what already exists.

## Things to Check

- Existing Python environment.
- Existing virtual environment.
- Installed dependencies.
- LLM API availability.
- Available LLM model and tool-calling support.
- Currency API availability.
- MCP package availability.
- Existing SQLite setup.
- Existing project files.
- API configuration.
- Existing testing setup.

## Findings

### Finding 1

The project requires an LLM capable of tool calling and streaming. The selected model and SDK must therefore be verified before implementation.

### Finding 2

Currency conversion requires an external API. The selected API must be checked for availability, request format, response format, and error behavior.

### Finding 3

The local database functionality can be implemented with SQLite because it requires no separate database server and is sufficient for this learning project.

### Finding 4

MCP will be used to expose the database functionality so that the project demonstrates a meaningful MCP integration rather than an isolated MCP example.

### Finding 5

The required Python dependencies must be checked before coding. Missing packages will be installed rather than assuming that the environment is ready.


---

# 5. Requirements

## Must Have

- At least three working tools.
- Internal calculator tool.
- External currency conversion API tool.
- Local SQLite database query tool.
- MCP server connected to the application.
- LLM decides which tool to call.
- No hardcoded keyword-based routing.
- Pydantic validation for required outputs.
- Streaming final responses.
- Retry with backoff for transient failures.
- Token usage logging.
- Estimated cost logging.
- Rate-limit handling.
- Timeout handling.
- Malformed model-output handling.
- Tool-failure handling.
- Automated tests for core functionality.
- Clear and minimal project structure.

## Should Have

- Pre-populated expense data for testing.
- Clear CLI interaction.
- Centralized configuration.
- Meaningful error messages.
- Reusable validation models.
- A README explaining setup, architecture, usage, and testing.


## Out of Scope

- Web frontend.
- Mobile application.
- User authentication.
- Production deployment.
- Docker.
- Complex financial planning.
- Investment advice.
- Payment processing.
- Large-scale database infrastructure.
- Unnecessary framework abstractions.


---

# 6. Approach

Explain how I plan to solve the work.

## Proposed Approach

```text
Set up Python environment
        ↓
Verify and install dependencies
        ↓
Create minimal project structure
        ↓
Create SQLite database and sample expenses
        ↓
Define Pydantic schemas
        ↓
Implement calculator tool
        ↓
Implement currency API tool
        ↓
Implement database query functionality
        ↓
Expose database functionality through MCP
        ↓
Connect LLM with available tools
        ↓
Allow LLM to decide tool usage
        ↓
Execute selected tool
        ↓
Validate tool result
        ↓
Return result to LLM
        ↓
Generate final response
        ↓
Stream final response
        ↓
Add retry and error handling
        ↓
Add token/cost logging
        ↓
Write automated tests
        ↓
Run complete validation
        ↓
Expected Result
````

## Why This Approach?

This approach follows the natural lifecycle of an LLM tool-calling application. The basic tools and data layer are built first, followed by MCP integration, LLM tool selection, validation, reliability features, observability, and testing.

This keeps dependencies understandable and makes it easier to identify problems at each stage.

## Alternatives Considered

### Alternative 1

Use LangChain to implement the complete tool-calling workflow.

**Pros:**

* Less low-level implementation.
* Built-in abstractions for tools and agents.
* Faster to create a prototype.

**Cons:**

* Hides important tool-calling concepts.
* Adds unnecessary abstraction for a learning project.
* Makes it harder to understand the actual LLM API workflow.

### Alternative 2

Build a web application with FastAPI and a frontend.

**Pros:**

* More realistic application interface.
* Easier to expose as a service later.

**Cons:**

* Adds unnecessary complexity.
* Introduces API and frontend concerns unrelated to the current learning objectives.
* Makes testing the LLM/tool-calling concepts less focused.

## Final Decision

Use a simple Python CLI application with direct LLM API integration, custom tools, SQLite, and one MCP server. Avoid unnecessary frameworks so the implementation clearly demonstrates how LLM tool calling, validation, MCP, streaming, reliability, and observability work.

---

# 7. Execution Steps

Break the work into logical steps.

## Step 1: Environment and Dependency Setup

**Goal:**

Prepare a clean Python environment and verify all required dependencies.

**Actions:**

* Check the Python version.
* Check whether a virtual environment exists.
* Create or activate the virtual environment.
* Check installed packages.
* Install missing dependencies.
* Configure environment variables.
* Verify LLM API connectivity.

**Expected Result:**

The project environment is ready and the LLM API can be accessed successfully.

---

## Step 2: Project Structure and Configuration

**Goal:**

Create a minimal and organized project structure.

**Actions:**

* Create the project directory.
* Create the required source directory.
* Create the test directory.
* Create configuration files.
* Create `.env` and `.gitignore`.
* Create `requirements.txt`.

**Expected Result:**

A clean project structure exists without unnecessary files or folders.

---



## Step 3: Implement the Three Tools

**Goal:**

Implement the required calculator, currency, and database capabilities.

**Actions:**

* Implement calculator functionality.
* Implement currency conversion using the external API.
* Implement database expense querying.
* Define tool input schemas.
* Define tool output schemas.
* Validate tool results with Pydantic.

**Expected Result:**

All three tools work independently and return validated results.

---

## Step 4: MCP Server Integration

**Goal:**

Expose the database functionality through an MCP server.

**Actions:**

* Create the MCP server.
* Expose the expense query functionality as an MCP tool.
* Connect the application to the MCP server.
* Verify the MCP tool can query SQLite.
* Validate the returned data.

**Expected Result:**

The application successfully communicates with the MCP server and retrieves expense data.

---

## Step 5: LLM Tool Calling

**Goal:**

Allow the LLM to decide which tool is required.

**Actions:**

* Define available tools for the model.
* Provide tool schemas to the LLM.
* Send user requests to the LLM.
* Detect model-generated tool calls.
* Execute the selected tool.
* Return tool results to the LLM.
* Allow the LLM to generate the final response.

**Expected Result:**

The model selects the appropriate tool based on the user's request without hardcoded routing.

---

## Step 6: Validation and Structured Output

**Goal:**

Ensure data used by the application follows the expected schemas.

**Actions:**

* Define Pydantic models.
* Validate tool arguments.
* Validate tool results.
* Validate required final response data.
* Handle validation failures gracefully.

**Expected Result:**

Invalid data is rejected before it is used by the application.

---

## Step 7: Streaming and Reliability

**Goal:**

Make the application resilient and provide streamed responses.

**Actions:**

* Enable LLM streaming.
* Display streamed final responses in the CLI.
* Add timeout handling.
* Add retry with exponential backoff.
* Handle rate-limit errors.
* Handle external API failures.
* Handle database failures.
* Handle malformed model output.
* Handle unexpected tool failures.

**Expected Result:**

The application can recover from transient failures and gracefully report unrecoverable failures while streaming successful responses.

---

## Step 8: Token Usage and Cost Logging

**Goal:**

Track LLM usage for every request.

**Actions:**

* Extract input token usage.
* Extract output token usage.
* Calculate total token usage.
* Configure model pricing.
* Calculate estimated request cost.
* Log usage and estimated cost.

**Expected Result:**

Each completed LLM request produces token and estimated cost information.

---

## Step 10: Testing

**Goal:**

Verify that the project meets all functional and technical requirements.

**Actions:**

* Test calculator.
* Test currency conversion.
* Test database queries.
* Test MCP communication.
* Test model-driven tool selection.
* Test Pydantic validation.
* Test streaming.
* Test retries.
* Test rate-limit handling.
* Test timeout handling.
* Test malformed model output.
* Test tool failures.
* Test token logging.
* Test cost estimation.
* Test combined finance requests.

**Expected Result:**

The project passes the defined test cases and all required features can be demonstrated.

---

## Step 11: Documentation and Final Verification

**Goal:**

Prepare the project for another person to understand and test.

**Actions:**

* Document project purpose.
* Document architecture.
* Document setup instructions.
* Document dependencies.
* Document available tools.
* Document MCP integration.
* Document usage examples.
* Document testing instructions.
* Run the complete project from a clean environment.
* Verify that no critical issues remain.

**Expected Result:**

The project is complete, documented, reproducible, and ready to be handed to a tester.

---



# 8. Validation Plan

How will I know that the work is correct?

## Functional Validation

* Calculator correctly evaluates valid calculations.
* Currency tool returns a valid converted amount.
* Database tool returns correct expense information.
* MCP server successfully exposes the database tool.
* LLM selects the appropriate tool based on user intent.
* Multiple tools can be used when a request requires them.
* Final responses are streamed to the CLI.
* Expense-management questions produce useful responses based on available data.

## Edge Cases

* Empty user input.
* Invalid calculator expression.
* Invalid currency code.
* External currency API timeout.
* External currency API failure.
* LLM rate limit.
* LLM timeout.
* Malformed tool arguments.
* Malformed model output.
* Invalid Pydantic data.
* Database query failure.
* MCP connection failure.
* Unknown tool request.
* Tool execution failure.
* Streaming interruption.

## Regression

* Calculator continues working after adding other tools.
* Currency conversion continues working after MCP integration.
* Database queries continue working after LLM integration.
* Streaming continues working after retry/error handling is added.
* Token and cost logging continues working for normal and tool-calling requests.

## Final Validation

Run the complete application from the configured environment and execute representative requests for calculation, currency conversion, database querying, and expense management. Then execute the complete automated test suite and confirm that all required features, error cases, logging, validation, streaming, and MCP integration work as expected.

---

# 9. Expected Deliverable

At the end of the work, I expect to have:

* A working CLI-based Personal Finance Assistant.
* A calculator tool.
* An external currency conversion tool.
* A SQLite expense database tool.
* One connected MCP server.
* LLM-driven tool selection without hardcoded routing.
* Pydantic validation.
* Streaming responses.
* Retry and backoff handling.
* Graceful error handling.
* Token usage and estimated cost logging.
* Automated tests.
* Setup and usage documentation.

---

# 10. Completion Criteria

The work is complete when:

* Objective has been achieved.
* All three required tools work.
* LLM decides which tool to call.
* No hardcoded routing is used.
* MCP server is successfully connected.
* Tool and required response data are validated with Pydantic.
* Final responses can be streamed.
* Transient errors use retry with backoff.
* Rate limits are handled gracefully.
* Timeouts are handled gracefully.
* Malformed model output is handled gracefully.
* Tool failures are handled gracefully.
* Token usage is logged.
* Estimated cost is logged.
* Automated tests pass.
* Edge cases have been checked.
* Documentation is complete.
* No known critical issues remain.
* The project can be handed to a tester and reproduced locally.

---

