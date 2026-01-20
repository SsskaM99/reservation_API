# PROMPTIT

## Prompt 1

You are a senior backend engineer acting as my pair programmer. 
We are building a simple Meeting Room Reservation API.

The goal is NOT to write perfect code immediately, but to produce a working, AI-generated baseline
that I will later critically review and refactor myself.

TECHNOLOGY & CONSTRAINTS
- Language: Python
- Framework: FastAPI
- Storage: in-memory only (no external database)
- The project must be runnable locally with minimal setup

BUSINESS RULES (MUST BE ENFORCED):
1. Reservations must NOT overlap within the same room.
2. Reservations must NOT be created in the past.
3. Start time must be strictly before end time.

FUNCTIONAL REQUIREMENTS:
Provide API endpoints for:
- Creating a reservation
- Canceling (deleting) a reservation
- Listing all reservations for a specific room

TECHNICAL REQUIREMENTS:
- Use FastAPI and Pydantic (v1 or v2 is fine, but be consistent)
- Use timezone-aware datetime objects (UTC only)
- Validate ISO 8601 timestamps
- Separate concerns clearly (e.g. main.py, models/schemas.py, storage.py, services.py)
- In-memory storage using Python data structures (dict/list)
- Proper HTTP status codes and JSON error responses:
  - 400 for validation errors
  - 404 for missing resources
  - 409 for overlapping reservations
- Add a /health endpoint
- Add OpenAPI-compatible request/response examples

TESTING & QUALITY:
- Add unit tests (pytest) at least for:
  - Overlapping reservation logic
  - Time validation rules
- Optionally add integration tests using FastAPI TestClient
- Use type hints throughout the code
- Add a README.md with:
  - Setup instructions
  - How to run the API
  - Example curl requests
  - List of endpoints and business rules

MANDATORY DOCUMENTATION (IMPORTANT):
1) Create a file PROMPTIT.md in the repository root.
   - Add this prompt under the heading "Prompt 1".
   - From now on, every message exchanged between me (User) and you (AI)
     related to this project MUST be appended to PROMPTIT.md.
   - Use a clear log format:
     - Timestamp
     - "User:"
     - "AI:"

2) Create a file DEVELOPMENT_PLAN.md in the repository root.
   Include:
   - Project goal and scope
   - Assumptions (since no real customer is available)
   - API contract (endpoints, payloads, status codes)
   - Data model description (e.g. Reservation)
   - Validation rules and overlap-checking logic (explained clearly)
   - Project structure and responsibilities
   - Testing strategy
   - Potential future improvements

WORKFLOW:
1) First, propose a concrete project structure as a file tree.
2) Then generate all required files with full contents:
   - Application code
   - Tests
   - README.md
   - PROMPTIT.md
   - DEVELOPMENT_PLAN.md
3) Ensure the project runs with:
   - `pip install -r requirements.txt`
   - `uvicorn main:app --reload`
4) Finally, provide a short checklist:
   - How to run tests
   - Which endpoints to manually test

Start now with step 1: propose the project structure.


**AI:**

Generated initial project structure, FastAPI application, in-memory storage,
business logic, API routes, tests, and documentation files.

## Prompt 2
Uvicorn fails to start with:
AssertionError: Status code 204 must not have a response body

The error happens in app/api/routes/reservations.py at cancel_reservation.
Fix the DELETE cancel endpoint so it complies with HTTP rules:
- If status code is 204 No Content, it must not return any response body and must not define a response_model or response content examples.
Use FastAPI Response to return 204 cleanly.

Make the minimal change needed to start the app and keep behavior correct. Do not refactor other parts yet.

**AI:**
Fixing the DELETE endpoint to return 204 No Content without a response body. Checking the current implementation:
Updating the DELETE endpoint to return 204 No Content without a response body:

## Prompt 3
You are now acting as a senior engineer performing a critical code review
of the AI-generated baseline implementation.

Context:
- Commit #1 ("Alkuperäinen AI-generoitu commit") represents the raw AI-generated code.
- From this point forward, I (the human developer) take responsibility for quality and correctness.
- Your task is to help identify problems and improvement opportunities, not to blindly refactor everything.

TASK:
Carefully review the entire codebase and produce a structured analysis covering:

1) What the AI-generated code does well
   - Architecture choices
   - Separation of concerns
   - Correct handling of business rules (if any)

2) Problems, bugs, or weaknesses
   - Logical errors or edge cases
   - Error handling issues
   - Validation gaps
   - Concurrency or data consistency risks
   - API design issues
   - Testing shortcomings
   - Pydantic v2 warnings or misuse
   - Any violations of FastAPI best practices

3) Concrete refactoring and improvement suggestions
   - Each suggestion should be actionable
   - Explain *why* the change is needed
   - Keep scope realistic (no gold-plating)

OUTPUT FORMAT (IMPORTANT):
- Do NOT change code yet.
- Do NOT generate refactored code.
- Produce a clear, numbered list of findings and suggestions.
- Group findings by category (e.g. API, Validation, Storage, Tests, Structure).

NEXT STEP PREPARATION:
At the end, propose:
- A refactoring plan broken into small, logical steps
- Each step should be suitable for a separate git commit
- Commit messages must be written in Finnish

This output will be used directly to guide the human-led refactoring phase.

**AI:**

Performed comprehensive code review of the entire codebase. Created `CODE_REVIEW.md` with structured analysis covering:

1. **What the code does well:**
   - Clear separation of concerns and modular architecture
   - Correct business logic implementation (overlap detection, time validation)
   - Good use of type hints and RESTful API design

2. **Problems identified:**
   - **Critical:** Pydantic v2 compatibility issues (deprecated `@validator` and `orm_mode`)
   - **High Priority:** Redundant `room_id` in request body, overly complex timezone validation
   - **Medium Priority:** Missing type hints, test coverage gaps, missing docstrings
   - **Low Priority:** Unused imports, magic numbers in tests

3. **Refactoring plan:**
   - Phase 1: Critical fixes (Pydantic v2 migration, API design)
   - Phase 2: Validation improvements and test coverage
   - Phase 3: Code quality improvements
   - All commits planned with Finnish commit messages

The review identified 12 distinct issues grouped by category (Pydantic, API Design, Validation, Storage, Testing, Code Quality). Overall assessment: functionally correct baseline with deprecation warnings and API design improvements needed.

## Prompt 4

**Timestamp:** 2026-01-19

**User:**

Refactor the reservation creation API to remove redundancy.

Scope:
- Files:
  - app/models/schemas.py
  - app/api/routes/reservations.py

Changes to make:
1) Remove room_id from the reservation creation request body schema.
2) Use only the path parameter room_id in POST /rooms/{room_id}/reservations.
3) Remove any code that mutates Pydantic models (e.g. payload.room_id = room_id).
4) Update OpenAPI examples to match the new request body.
5) Keep API behavior and responses otherwise unchanged.

Rules:
- Do NOT change business logic.
- Do NOT refactor unrelated code.
- Do NOT change endpoint paths.

After implementing:
- Run pytest and ensure all tests pass.
- Append this prompt and your response to PROMPTIT.md with a timestamp.

**AI:**

Implemented the redundancy removal for reservation creation while keeping business logic unchanged:

- **Schema change** (`app/models/schemas.py`): added `ReservationCreateRequest` (request body model) without `room_id`; `room_id` remains part of internal models used by services/storage.
- **Route change** (`app/api/routes/reservations.py`): POST now accepts `ReservationCreateRequest`, constructs an internal `ReservationCreate(room_id=room_id, ...)`, and no longer mutates the request model.
- **OpenAPI examples**: updated POST examples to remove `room_id` from the request body.

**Verification:** `pytest` passes (7 tests).

## Other Prompts
Alussa syötin tehtävänannon Chat GPT 5.2 Versiolle ja loin tämän pohjalta suunnitelman. Koodauksen suoritin Cursorissa GPT:n tekemillä prompteilla.
