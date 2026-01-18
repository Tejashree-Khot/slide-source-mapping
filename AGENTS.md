# Repo description

RAG source mapping. The api uses semantic search to retrieve relevant context from uploaded documents and generate informed responses.

## Repo structure

```text
slide-source-mapping/
├── assets/             # Sample pdf files
├── app/                # FastAPI backend application
├── ui/                 # React/TypeScript frontend
├── scripts/            # Test and utility scripts
```

## Development Rules

1. Always use `uv run` to execute Python scripts.
2. Do **not** add test cases unless explicitly requested.
3. Do **not** add comments in the code.
4. Always add single line Docstrings.
5. Do **not** over-engineer the solution.
6. Use **classes and functions** wherever appropriate.
7. Follow the **existing project structure and coding style** when adding new code.
8. **Always confirm with me before changing or introducing a design pattern.**
9. Implement **only the requested functionality** — do not add extras.

## Coding practices

- **Type hints**: Use type annotations for function signatures and class attributes
- **Pydantic**: Use `BaseModel` for data validation and `BaseSettings` for configuration
- **Async/await**: Use async patterns for I/O operations (database, LLM calls)
- **Dependency injection**: Use `@lru_cache` decorated functions for singleton instances
- **Factory pattern**: Use factory classes/functions for creating instances
- **ABC pattern**: Use abstract base classes for extensible components
- **Retry with tenacity**: Use `@retry` decorator for external API calls
- **Path handling**: Use `pathlib.Path` for file path operations
- **Logging**: Use centralized logging configuration with module-level loggers
- **DRY principle**: Reuse existing functions and abstractions; avoid code duplication
- **Code style**: Write concise, optimized code with a single-line docstring
