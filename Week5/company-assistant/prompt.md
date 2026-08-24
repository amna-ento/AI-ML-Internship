# role
u have to act as an extepert ai assistant who is known from the perfection of his work and the simplicity in work, like if a task is given to him he understand everything very thing very well and do eveything asked and the work woud be simpke and easy for any one to understand

# context
i've been given the task to complete it and have the understanding of what things have done, i'll give u whole task statment, requirements in the input section, u are required to understand and walk me through it

# example
if i'd be given such task to help someone, i'll do it like:
- undertsand the task and make him understand as well
- give him the complete strategy like how are you gona do it
- then start doing it
- firstly i make the folder structure ti. him
- then make him install the dependencies
- then start giving the code
- the code that i'd give him must be like file name and the code to be replaced, added, updated
- with each code or command i'll akso tell u'd get this output it would be normal or else fix that problem

# input
```
Task
Build a “Company Assistant API” using Python, FastAPI, Pydantic, SQLite, and an LLM.
The assistant should support these tools:
Get user information
Read user data from SQLite.
Example: get_user(user_id)
Get weather
Call an external weather API.
Example: get_weather(city)
Create a task
Store a task in SQLite.
Example: create_task(user_id, title)
List user tasks
Read tasks from SQLite.
Example: list_tasks(user_id)
Main endpoint
Plain Text
POST /chat
Request:
Plain Text
{
  "user_id": 1,
  "message": "What is the weather in Lahore and create a task for me to call Ali?"}
The LLM should determine that it needs to:
Plain Text
1. get_weather("Lahore")
2. create_task(1, "Call Ali")
3. generate a final response


Requirements
1. LLM + Tool Calling
Use an LLM with native/function tool calling.
The model should decide which tool(s) are required rather than hardcoding the sequence.
2. Multi-tool orchestration
Support multiple tool calls in one request.
For example:
Plain Text
User
 ↓
LLM
 ↓
get_user()
 ↓
get_weather()
 ↓
create_task()
 ↓
LLM
 ↓
Final response
Handle the case where the model requests more than one tool.
3. MCP
Create a small MCP server exposing at least two tools, for example:
Plain Text
get_user
create_task
Then create/use an MCP client that can discover and call those tools.
You don't need to build a huge MCP framework. Keep it minimal.
4. FastAPI
Create:
Plain Text
POST /chat
GET /users/{user_id}
GET /users/{user_id}/tasks
POST /users/{user_id}/tasks
Use proper HTTP status codes.
5. Pydantic
Create request/response models.
For example:
Plain Text
class ChatRequest(BaseModel):
    user_id: intmessage: str
Validate things such as:
user_id > 0
message cannot be empty
task title cannot be empty
6. SQLite
Create at least:
Plain Text
users
tasks
Example:
Plain Text
users
-----
id
name
email
tasks
-----
id
user_id
title
completed
created_at
Use proper relationships and parameterized queries.
7. External API
Integrate a public API such as a weather API.
You should handle:
successful response
timeout
invalid city
API failure
8. Error handling + retries
Implement retry logic for external API failures.
For example:
Plain Text
Attempt 1 → failed
Attempt 2 → failed
Attempt 3 → failed
→ return meaningful error
Don't retry errors that should not be retried, such as invalid input.
9. Streaming
Make /chat capable of streaming the final LLM response.
For example:
Plain Text
data: The
data: weather
data: in
data: Lahore
data: is...
You can use FastAPI's StreamingResponse.
10. Testing
Write tests for at least:
Plain Text
✓ Pydantic validation
✓ Create task
✓ Get tasks
✓ Invalid user
✓ External API failure
✓ Tool execution
✓ Chat endpoint
Mock the external API/LLM where appropriate.
Architecture
I would expect something approximately like:
Plain Text
app/
├── main.py
├── api/
│   └── routes.py
├── models/
│   └── schemas.py
├── database/
│   ├── database.py
│   └── models.py
├── services/
│   ├── llm_service.py
│   ├── weather_service.py
│   └── task_service.py
├── tools/
│   ├── user_tools.py
│   └── task_tools.py
├── mcp/
│   ├── server.py
│   └── client.py
└── tests/
    ├── test_api.py
    ├── test_tools.py
    └── test_services.py


What I'd specifically evaluate
Don't just evaluate whether it works. Ask the candidate to explain:
Why did you structure the project this way?
Why use Pydantic here?
How does the LLM decide which tool to call?
How does your multi-tool orchestration work?
What happens if tool #2 fails after tool #1 succeeds?
Which errors should be retried?
Why shouldn't every error be retried?
Why use SQLite here and how would you change it for PostgreSQL?
How does MCP differ from simply defining LLM tools?
How would you secure the MCP server?
How would you handle 100 concurrent users?
What would you improve if this went to production?
One important rule for the test
I would explicitly tell them:
AI tools are allowed for assistance, but you must understand and explain every part of your implementation. You may be asked to modify, debug, or extend your code live.
That will test AI dependency + actual engineering ability much better than simply asking them to write code from scratch.
If you want this to be a smaller 60–90 minute test, I can also reduce this to one compact coding challenge with 5–6 requirements while still covering LLM, tool calling, FastAPI, SQLite, Pydantic, error handling, and testing.
 
give full qiestion paper type
Absolutely. Here’s a proper question-paper-style coding test you can give today. I’ve kept it practical and compact enough to complete in around 2–3 hours, while covering all the areas you listed.
Technical Coding Assessment
Duration: 2.5 Hours
Language: Python 3.11+
Framework: FastAPI
Database: SQLite
Difficulty: Intermediate / Advanced
1. Objective
Build a small AI Task Assistant API that allows users to interact with an LLM through a FastAPI application.
The LLM should be able to understand the user's request, decide which tools are required, execute one or multiple tools, and return a final response.
The application must demonstrate:
LLM and tool calling
Multi-tool orchestration
MCP client/server
FastAPI
Pydantic validation
SQLite database operations
External API integration
Error handling and retries
Streaming responses
Testing and debugging
Clean project architecture
2. Problem Statement
You are required to build an AI-powered Task Assistant.
A user can send a natural-language request such as:
"What's the weather in Lahore and create a task for me to call Ahmed tomorrow?"
The system should allow the LLM to determine that it needs to:
Get the weather for Lahore.
Create a task for the user.
Generate a final response containing the result.
The tool execution should not be hardcoded based on keywords. The LLM should decide which tools are required.
3. Functional Requirements
Question 1 — FastAPI API
Create a FastAPI application with the following endpoints:
POST /chat
Request:
Plain Text
{
  "user_id": 1,
  "message": "What is the weather in Lahore?"}
Response should contain the assistant's answer.
GET /users/{user_id}
Return the user's information.
Example:
Plain Text
{
  "id": 1,
  "name": "Ahmed",
  "email": "ahmed@example.com"}


GET /users/{user_id}/tasks
Return all tasks belonging to the user.
POST /users/{user_id}/tasks
Request:
Plain Text
{
  "title": "Call Ahmed tomorrow"}
Create the task in SQLite.
4. Pydantic Validation
Create appropriate Pydantic models.
At minimum:
Plain Text
class ChatRequest(BaseModel):
    user_id: intmessage: str
and:
Plain Text
class CreateTaskRequest(BaseModel):
    title: str
Validation should ensure:
user_id must be greater than 0.
message cannot be empty.
title cannot be empty.
Appropriate validation errors are returned by FastAPI.
5. SQLite Database
Use SQLite as the application's database.
Create the following tables.
Users
Plain Text
users
----------------
id
name
email
created_at


Tasks
Plain Text
tasks
----------------
id
user_id
title
completed
created_at
Requirements:
A user can have multiple tasks.
tasks.user_id must reference a user.
Implement CRUD operations required by the API.
Use parameterized queries / safe database operations.
Handle the case where a user does not exist.
Create at least 2 sample users during setup.
6. LLM Tool Calling
Integrate an LLM that supports function/tool calling.
Create at least these tools:
Tool 1 — get_user
Plain Text
get_user(user_id)
Returns the user's information.
Tool 2 — create_task
Plain Text
create_task(user_id, title)
Creates a task for the user.
Tool 3 — list_tasks
Plain Text
list_tasks(user_id)
Returns the user's tasks.
Tool 4 — get_weather
Plain Text
get_weather(city)
Calls an external weather API and returns the weather information.
7. Multi-Tool Orchestration
The system must support multiple tool calls in a single user request.
For example:
Plain Text
User:
"Tell me the weather in Lahore and create a task
to call Ahmed."
Expected flow:
Plain Text
User
  ↓
LLM
  ↓
Tool Call: get_weather
  ↓
Tool Call: create_task
  ↓
LLM
  ↓
Final Response
The implementation must not assume a fixed tool execution order.
The LLM should determine which tools are required.
8. External API Integration
Integrate a public weather API.
The following should work:
Plain Text
get_weather("Lahore")
get_weather("London")
get_weather("Dublin")
The implementation must handle:
Successful API response
Invalid city
API timeout
HTTP errors
Unexpected API response
Do not expose API keys directly in the source code.
Use environment variables.
Example:
Plain Text
WEATHER_API_KEY=...
LLM_API_KEY=...


9. Error Handling and Retry
Implement proper error handling.
For external API calls:
Plain Text
Request
   ↓
Attempt 1
   ↓
Failure
   ↓
Retry
   ↓
Attempt 2
   ↓
Failure
   ↓
Retry
   ↓
Attempt 3
   ↓
Final Error
Requirements:
Maximum 3 attempts.
Use a reasonable delay between retries.
Do not retry validation errors.
Do not retry obviously invalid requests.
Return meaningful errors to the user.
Log useful debugging information.
10. MCP Server
Create a small MCP server.
Expose at least two tools through MCP:
Plain Text
get_user
create_task
The MCP server should provide the necessary tool definitions and execute the corresponding operations.
11. MCP Client
Create an MCP client that:
Connects to the MCP server.
Discovers available tools.
Reads their tool definitions.
Allows the LLM/application to call the tools.
Returns the tool result to the application.
The client should not hardcode all MCP tool definitions if they can be discovered from the server.
12. Streaming Response
The /chat endpoint should support streaming the final LLM response.
For example:
Plain Text
The
weather
in
Lahore
is
currently
32°C...
Use FastAPI's:
Plain Text
StreamingResponse
or another appropriate streaming mechanism.
The objective is to demonstrate that the response can be delivered incrementally instead of waiting for the entire response.
13. Testing
Write automated tests for the application.
At minimum, include tests for:
API
Plain Text
✓ GET /users/{id}
✓ GET /users/{id}/tasks
✓ POST /users/{id}/tasks
✓ POST /chat


Validation
Plain Text
✓ Invalid user_id
✓ Empty message
✓ Empty task title


Database
Plain Text
✓ Create task
✓ Retrieve tasks
✓ Invalid user


External API
Mock the weather API and test:
Plain Text
✓ Successful request
✓ API failure
✓ Timeout
✓ Retry behavior


Tool Calling
Test at least one tool independently.
14. Project Architecture
Organize the project using a clean structure.
For example:
Plain Text
ai-task-assistant/
│
├── app/
│   ├── main.py
│   │
│   ├── api/
│   │   └── routes.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── database/
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── services/
│   │   ├── llm_service.py
│   │   ├── weather_service.py
│   │   └── task_service.py
│   │
│   ├── tools/
│   │   ├── user_tools.py
│   │   └── task_tools.py
│   │
│   └── mcp/
│       ├── server.py
│       └── client.py
│
├── tests/
│   ├── test_api.py
│   ├── test_tools.py
│   └── test_services.py
│
├── .env.example
├── requirements.txt
├── README.md
└── run.py
You may modify the structure if you have a better architectural approach.
15. README / Documentation
Create a README.md containing:
Setup
How to install dependencies.
Environment Variables
Example:
Plain Text
LLM_API_KEY=
WEATHER_API_KEY=


Running the application
Explain how to start the FastAPI server.
Running tests
Explain how to run the tests.
Architecture
Briefly explain:
API layer
Service layer
Database layer
LLM layer
Tool layer
MCP layer
Example Request
Provide an example /chat request and response.
16. Debugging Scenario
After completing the implementation, assume the following bug exists:
When the user asks the assistant to create a task and retrieve the weather in the same request, the first tool works but the second tool is never executed.
Explain:
How you would investigate the problem.
What logs/debugging information you would check.
Possible causes.
How you would fix it.
What test you would add to prevent the issue from happening again.
You do not necessarily need to intentionally introduce the bug. Explain your debugging approach.
17. Technical Questions During Review
After completing the coding portion, you should be prepared to explain your implementation.
LLM / Tool Calling
How does function/tool calling work?
Who decides which tool should be called?
What happens after a tool returns its result?
How would you prevent the LLM from calling an unauthorized tool?
Multi-Tool Orchestration
How does your application handle multiple tool calls?
Can tools execute in parallel?
When would parallel execution be dangerous?
MCP
What problem does MCP solve?
What is the difference between an MCP server and MCP client?
How is MCP different from directly registering functions as LLM tools?
FastAPI
Why did you use FastAPI?
How does dependency injection work in FastAPI?
How would you handle 100+ simultaneous requests?
Database
Why SQLite for this project?
How would you migrate this application to PostgreSQL?
How would you handle concurrent database operations?
Error Handling
Which errors should be retried?
Which errors should never be retried?
Why use exponential backoff?
Streaming
Why would streaming be useful for an LLM application?
What happens if the connection is interrupted during streaming?
Testing
What should be mocked?
Why shouldn't tests depend on a real weather API?
What is the difference between unit and integration testing?
```
# output
the output must be the completion of whole task in simple easy way 

# constraints
- do not add comment in code after code snipet explain summerizingly what this part do, 
- the theory will not be too much it must be in bullets point 
