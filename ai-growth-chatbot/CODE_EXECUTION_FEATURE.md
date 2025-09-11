# Code Execution Feature Documentation

## 🚀 Overview

The Code Execution feature has been successfully added to the AI Chatbot CCP coding space. This feature allows users to run code in multiple programming languages directly through the web interface using secure API endpoints.

## 📋 Features

### ✅ Implemented Features

1. **Multi-Language Support**: Execute code in 10+ programming languages
2. **Secure Execution**: Sandboxed execution with validation and security checks
3. **Input Handling**: Support for programs that require user input
4. **Error Handling**: Comprehensive error handling for compilation and runtime errors
5. **Timeout Protection**: Automatic timeout to prevent infinite loops
6. **Code Validation**: Pre-execution validation to catch security risks
7. **Snippet Execution**: Execute saved code snippets directly from the database

### 🔧 Supported Languages

- **Python** (.py)
- **JavaScript** (.js) - Node.js
- **Java** (.java)
- **C++** (.cpp)
- **C** (.c)
- **Go** (.go)
- **Rust** (.rs)
- **PHP** (.php)
- **Ruby** (.rb)
- **Bash** (.sh)

## 🌐 API Endpoints

### 1. Get Supported Languages
```
GET /api/coding/languages
```
**Description**: Returns list of supported programming languages
**Authentication**: None required
**Response**:
```json
{
  "success": true,
  "languages": ["python", "javascript", "java", ...],
  "total": 10
}
```

### 2. Execute Code
```
POST /api/coding/execute
```
**Description**: Execute code in specified language
**Authentication**: JWT required
**Request Body**:
```json
{
  "code": "print('Hello World')",
  "language": "python",
  "input": "optional input data"
}
```
**Response**:
```json
{
  "success": true,
  "output": "Hello World\n",
  "error": "",
  "execution_time": 0.123,
  "return_code": 0
}
```

### 3. Validate Code
```
POST /api/coding/validate
```
**Description**: Validate code before execution
**Authentication**: JWT required
**Request Body**:
```json
{
  "code": "print('Hello World')",
  "language": "python"
}
```
**Response**:
```json
{
  "success": true,
  "validation": {
    "valid": true
  }
}
```

### 4. Execute Saved Snippet
```
POST /api/coding/snippets/{snippet_id}/execute
```
**Description**: Execute a saved code snippet
**Authentication**: JWT required
**Request Body**:
```json
{
  "input": "optional input data"
}
```

## 🛡️ Security Features

### Code Validation
- **Empty Code Detection**: Prevents execution of empty code
- **Language Validation**: Ensures only supported languages are used
- **Dangerous Pattern Detection**: Blocks potentially harmful operations:
  - File system operations (`open()`, `file()`)
  - System calls (`import os`, `import subprocess`)
  - Dynamic execution (`exec()`, `eval()`)
  - Input functions in unsupervised mode

### Execution Safety
- **Sandboxed Execution**: Code runs in temporary isolated directories
- **Timeout Protection**: Automatic termination after 30-45 seconds
- **Memory Management**: Automatic cleanup of temporary files
- **Error Containment**: Runtime errors don't crash the server

## ⚡ Performance Features

### Execution Metrics
- **Execution Time Tracking**: Precise timing for performance analysis
- **Return Code Monitoring**: Exit status tracking
- **Memory Efficient**: Temporary file cleanup after execution

### Compilation Support
- **Smart Compilation**: Automatic compilation for C/C++/Java/Rust
- **Error Reporting**: Detailed compilation error messages
- **Binary Management**: Proper handling of compiled executables

## 🎯 Usage Examples

### Frontend JavaScript Integration
```javascript
class CodeExecutor {
    constructor(apiUrl, authToken) {
        this.apiUrl = apiUrl;
        this.authToken = authToken;
    }

    async executeCode(code, language, input = '') {
        const response = await fetch(`${this.apiUrl}/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.authToken}`
            },
            body: JSON.stringify({ code, language, input })
        });
        return await response.json();
    }
}
```

### Python Code Example
```python
# This code can be executed through the API
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

for i in range(10):
    print(f"fib({i}) = {fibonacci(i)}")
```

### JavaScript Code Example
```javascript
// Node.js code execution
const numbers = [1, 2, 3, 4, 5];
const sum = numbers.reduce((a, b) => a + b, 0);
console.log(`Sum: ${sum}`);

const factorial = (n) => n <= 1 ? 1 : n * factorial(n - 1);
console.log(`5! = ${factorial(5)}`);
```

## 📁 File Structure

```
backend/
├── services/
│   └── code_execution_service.py     # Core execution service
├── routes/
│   └── coding_routes.py              # API endpoints (updated)
├── tests/
│   └── test_code_execution.py        # Test suite
├── simple_test.py                    # Basic functionality test
└── example_code_execution_usage.py   # Usage examples
```

## 🚦 Error Handling

### Common Error Scenarios

1. **Compilation Errors**
   ```json
   {
     "success": false,
     "error": "Compilation failed: syntax error at line 5"
   }
   ```

2. **Runtime Errors**
   ```json
   {
     "success": true,
     "output": "",
     "error": "ZeroDivisionError: division by zero",
     "return_code": 1
   }
   ```

3. **Timeout Errors**
   ```json
   {
     "success": false,
     "error": "Execution timeout (30s)"
   }
   ```

4. **Security Violations**
   ```json
   {
     "success": false,
     "error": "Code contains potentially dangerous operations: import os",
     "warning": "For security reasons, file operations are restricted"
   }
   ```

## 📊 Testing

### Automated Tests
- Unit tests for the CodeExecutionService
- Integration tests for API endpoints
- Security validation tests
- Error handling tests

### Manual Testing
```bash
# Run basic functionality test
python simple_test.py

# Test API endpoints (requires running server)
python example_code_execution_usage.py
```

## 🔧 Installation & Setup

### Prerequisites
Ensure the following runtime environments are installed:
- **Python 3.x** (for Python execution)
- **Node.js** (for JavaScript execution)
- **Java JDK** (for Java execution)
- **GCC/G++** (for C/C++ execution)
- **Go** (for Go execution)
- **Rust** (for Rust execution)
- **PHP** (for PHP execution)
- **Ruby** (for Ruby execution)

### Backend Setup
The feature is already integrated into the existing Flask application. No additional setup required.

### Frontend Integration
Update your frontend to include:
1. Language selector dropdown
2. Code editor (Monaco Editor recommended)
3. Input area for program input
4. Output display area
5. Run button with API integration

## 🔮 Future Enhancements

### Planned Features
1. **Package Management**: Support for installing packages (pip, npm, etc.)
2. **Multi-file Projects**: Support for projects with multiple files
3. **Interactive Console**: REPL-like interface
4. **Code Sharing**: Share executable code snippets
5. **Performance Analytics**: Detailed execution metrics
6. **Custom Timeouts**: User-configurable execution limits

### Advanced Security
1. **Resource Limits**: CPU and memory usage controls
2. **Network Isolation**: Prevent network access
3. **Advanced Sandboxing**: Docker-based execution

## 🎉 Success Metrics

✅ **Code Execution Service**: Fully implemented and tested
✅ **API Endpoints**: All endpoints working correctly
✅ **Security Validation**: Comprehensive security checks in place
✅ **Multi-language Support**: 10+ languages supported
✅ **Error Handling**: Robust error management
✅ **Documentation**: Complete API and usage documentation

## 🚀 Next Steps

1. **Frontend Integration**: Update the coding space UI to include:
   - Run button in the code editor
   - Language selector
   - Output console
   - Input field for interactive programs

2. **User Experience**: Add:
   - Syntax highlighting for all supported languages
   - Auto-completion
   - Real-time error highlighting

3. **Advanced Features**: Consider implementing:
   - Code sharing functionality
   - Execution history
   - Performance benchmarking

---

**Status**: ✅ **FEATURE READY FOR FRONTEND INTEGRATION**

The backend code execution feature is fully implemented and ready for use. The frontend team can now integrate these API endpoints into the coding space interface.