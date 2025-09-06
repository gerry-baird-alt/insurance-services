# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python FastAPI application for insurance services. The project uses modern Python tooling with uv for dependency management and FastAPI for the web framework.

## Development Commands

### Running the Application
```bash
# Install dependencies
uv sync

# Run the development server
uvicorn main:app --reload

# Run on specific host/port
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Testing
- HTTP test file: `test_main.http` contains sample requests for manual testing
- Test endpoints at http://127.0.0.1:8000 when server is running

### Dependencies
- Uses `uv` for Python package management (not pip/poetry)
- Dependencies are defined in `pyproject.toml`
- Lock file is `uv.lock`

## Architecture

### Project Structure
- `main.py`: Main FastAPI application with route definitions
- `pyproject.toml`: Project configuration and dependencies
- `test_main.http`: HTTP test requests for manual API testing

### Application Structure
- Simple FastAPI application with basic REST endpoints
- Uses async/await pattern for route handlers
- Currently implements:
  - Root endpoint (`/`) returning a hello world message
  - Parameterized greeting endpoint (`/hello/{name}`)

### Python Version
- Requires Python >= 3.13
- Uses modern async/await patterns

## Key Libraries
- **FastAPI**: Web framework for building APIs
- **Uvicorn**: ASGI server for running FastAPI applications