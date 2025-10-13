# Security Notes for Prepify

## Code Execution Sandbox

### Current Implementation
The platform uses a **restricted Python execution environment** with the following security measures:

1. **Limited Builtins**: Only safe built-in functions are available (no `open`, `eval`, `exec`, file I/O, etc.)
2. **Timeout Protection**: Code execution is limited to 5 seconds per test case
3. **Whitelisted Imports**: Only safe modules allowed (`math`, `random`, `itertools`, `collections`, `functools`)
4. **No File System Access**: File operations are not available in the sandbox
5. **Custom Import Handler**: Blocks all imports except whitelisted safe modules

### Known Limitations

⚠️ **CRITICAL WARNING**: This is a **basic educational sandbox ONLY** - NOT suitable for untrusted code:

- **Fundamental Limitation**: Uses Python's `exec()` with restricted builtins, not true isolation
- **Known Attack Vector**: Python object introspection (`__subclasses__()`, etc.) can potentially bypass restrictions
- **No Memory Limits**: Only time-based execution limits (5 seconds)
- **Target Audience**: Designed for educational use with trusted students in a controlled environment
- **NOT Production Safe**: Should NOT be used with completely untrusted or malicious code

### Trust Model
This platform assumes:
- Users are students practicing for interviews, not malicious actors
- Code submissions are educational in nature
- The environment is monitored and access-controlled
- This is a learning tool, not a public code execution service

### Production Recommendations
For production deployment with untrusted user code, consider:

1. **Docker Containers**: Run code in isolated Docker containers
2. **Firejail**: Use Firejail for process sandboxing
3. **Cloud Code Execution**: Use services like AWS Lambda or Judge0 API
4. **WebAssembly**: Consider PyScript or Pyodide for browser-based execution

### Password Security
- Passwords are hashed using SHA-256 before storage
- Password hashes are **never** returned in API responses
- Only safe user data (id, username, email, full_name, points) is exposed

### Session Management
- Flask sessions with secure secret key
- Session-based authentication
- Automatic session cleanup on logout

## Reporting Security Issues
If you discover a security vulnerability, please report it responsibly by contacting the development team directly rather than posting publicly.
