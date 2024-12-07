def execute_code(code_snippet):
    """Executes code dynamically and returns the result or error."""
    try:
        local_scope = {}
        exec(code_snippet, {}, local_scope)
        return {"result": local_scope}
    except Exception as e:
        return {"error": str(e)}