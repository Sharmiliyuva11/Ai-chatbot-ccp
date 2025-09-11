"""
Example script showing how to use the Code Execution API endpoints

This demonstrates the API calls that the frontend should make to execute code.
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5000/api/coding"
JWT_TOKEN = "your-jwt-token-here"  # Replace with actual token

def make_request(method, endpoint, data=None, headers=None):
    """Helper function to make API requests"""
    url = f"{BASE_URL}{endpoint}"
    default_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {JWT_TOKEN}"
    }
    if headers:
        default_headers.update(headers)
    
    try:
        if method == "GET":
            response = requests.get(url, headers=default_headers)
        elif method == "POST":
            response = requests.post(url, headers=default_headers, json=data)
        
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def example_get_supported_languages():
    """Example: Get list of supported programming languages"""
    print("📋 Getting supported languages...")
    
    # This endpoint doesn't require authentication
    response = requests.get(f"{BASE_URL}/languages")
    result = response.json()
    
    if result.get('success'):
        print(f"✅ Supported languages: {', '.join(result['languages'])}")
        print(f"   Total: {result['total']} languages")
    else:
        print(f"❌ Error: {result.get('error')}")
    
    return result

def example_execute_python_code():
    """Example: Execute Python code"""
    print("\n🐍 Executing Python code...")
    
    data = {
        "code": """
# Simple Python program
name = "World"
print(f"Hello, {name}!")

# Math operations
result = 2 + 3 * 4
print(f"2 + 3 * 4 = {result}")

# List operations
numbers = [1, 2, 3, 4, 5]
total = sum(numbers)
print(f"Sum of {numbers} = {total}")
""",
        "language": "python",
        "input": ""
    }
    
    result, status_code = make_request("POST", "/execute", data)
    
    if result.get('success'):
        print("✅ Execution successful!")
        print(f"   Output:\n{result['output']}")
        print(f"   Execution time: {result['execution_time']}s")
        print(f"   Return code: {result['return_code']}")
    else:
        print(f"❌ Execution failed: {result.get('error')}")
    
    return result

def example_execute_javascript_code():
    """Example: Execute JavaScript code"""
    print("\n🟨 Executing JavaScript code...")
    
    data = {
        "code": """
// Simple JavaScript program
const greeting = "Hello from JavaScript!";
console.log(greeting);

// Array operations
const numbers = [1, 2, 3, 4, 5];
const sum = numbers.reduce((a, b) => a + b, 0);
console.log(`Sum of [${numbers}] = ${sum}`);

// Object example
const person = { name: "Alice", age: 30 };
console.log(`Person: ${person.name}, Age: ${person.age}`);
""",
        "language": "javascript",
        "input": ""
    }
    
    result, status_code = make_request("POST", "/execute", data)
    
    if result.get('success'):
        print("✅ Execution successful!")
        print(f"   Output:\n{result['output']}")
        print(f"   Execution time: {result['execution_time']}s")
    else:
        print(f"❌ Execution failed: {result.get('error')}")
    
    return result

def example_execute_with_input():
    """Example: Execute Python code with user input"""
    print("\n📝 Executing Python code with input...")
    
    data = {
        "code": """
# Program that requires input
name = input("What's your name? ")
age = input("What's your age? ")

print(f"Hello {name}!")
print(f"You are {age} years old.")

# Simple calculation
try:
    age_num = int(age)
    years_to_100 = 100 - age_num
    if years_to_100 > 0:
        print(f"You have {years_to_100} years until you're 100!")
    else:
        print("You're already over 100 or exactly 100!")
except ValueError:
    print("Invalid age entered!")
""",
        "language": "python",
        "input": "Alice\n25\n"  # Simulated user input
    }
    
    result, status_code = make_request("POST", "/execute", data)
    
    if result.get('success'):
        print("✅ Execution successful!")
        print(f"   Output:\n{result['output']}")
    else:
        print(f"❌ Execution failed: {result.get('error')}")
    
    return result

def example_validate_code():
    """Example: Validate code before execution"""
    print("\n🔍 Validating code...")
    
    # Test with valid code
    data = {
        "code": "print('This is valid Python code')",
        "language": "python"
    }
    
    result, status_code = make_request("POST", "/validate", data)
    
    if result.get('success'):
        validation = result['validation']
        print(f"✅ Code validation: {'Valid' if validation['valid'] else 'Invalid'}")
        if not validation['valid']:
            print(f"   Error: {validation.get('error')}")
    else:
        print(f"❌ Validation failed: {result.get('error')}")
    
    # Test with potentially dangerous code
    print("\n🚨 Testing dangerous code validation...")
    data = {
        "code": "import os\nos.system('ls')",
        "language": "python"
    }
    
    result, status_code = make_request("POST", "/validate", data)
    
    if result.get('success'):
        validation = result['validation']
        print(f"   Code validation: {'Valid' if validation['valid'] else 'Invalid'}")
        if not validation['valid']:
            print(f"   Error: {validation.get('error')}")
            print(f"   Warning: {validation.get('warning', 'N/A')}")
    
    return result

def example_error_handling():
    """Example: Error handling"""
    print("\n🐛 Testing error handling...")
    
    # Test syntax error
    data = {
        "code": "print('Missing closing quote",  # Syntax error
        "language": "python",
        "input": ""
    }
    
    result, status_code = make_request("POST", "/execute", data)
    
    print(f"   Syntax error handling:")
    print(f"   Success: {result.get('success')}")
    print(f"   Error: {result.get('error', 'No error message')}")
    
    # Test runtime error
    data = {
        "code": "print(10 / 0)",  # Runtime error
        "language": "python",
        "input": ""
    }
    
    result, status_code = make_request("POST", "/execute", data)
    
    print(f"\n   Runtime error handling:")
    print(f"   Success: {result.get('success')}")
    if result.get('success') and result.get('error'):
        print(f"   Error output: {result['error'][:100]}...")
    
    return result

def frontend_integration_example():
    """Example showing how frontend should integrate with the API"""
    print("\n🌐 Frontend Integration Example")
    print("=" * 50)
    
    frontend_code = '''
// Frontend JavaScript code example

class CodeExecutor {
    constructor(apiUrl, authToken) {
        this.apiUrl = apiUrl;
        this.authToken = authToken;
    }

    async getSupportedLanguages() {
        const response = await fetch(`${this.apiUrl}/languages`);
        return await response.json();
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

    async validateCode(code, language) {
        const response = await fetch(`${this.apiUrl}/validate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.authToken}`
            },
            body: JSON.stringify({ code, language })
        });
        return await response.json();
    }

    async executeSnippet(snippetId, input = '') {
        const response = await fetch(`${this.apiUrl}/snippets/${snippetId}/execute`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.authToken}`
            },
            body: JSON.stringify({ input })
        });
        return await response.json();
    }
}

// Usage example
const executor = new CodeExecutor('/api/coding', getUserToken());

// Execute code
async function runCode() {
    const code = document.getElementById('codeEditor').value;
    const language = document.getElementById('languageSelect').value;
    const input = document.getElementById('inputArea').value;

    try {
        // Validate first
        const validation = await executor.validateCode(code, language);
        if (!validation.validation.valid) {
            showError(validation.validation.error);
            return;
        }

        // Execute
        showLoading(true);
        const result = await executor.executeCode(code, language, input);
        
        if (result.success) {
            displayOutput(result.output);
            displayExecutionInfo({
                time: result.execution_time,
                returnCode: result.return_code
            });
        } else {
            showError(result.error);
        }
    } catch (error) {
        showError('Network error: ' + error.message);
    } finally {
        showLoading(false);
    }
}
'''
    
    print("Frontend integration code saved to example above ☝️")
    return frontend_code

if __name__ == "__main__":
    print("🚀 Code Execution API Examples")
    print("=" * 50)
    
    # Note: These examples will fail without a valid JWT token
    # They're meant to show the structure of API calls
    
    try:
        # Example 1: Get supported languages (no auth required)
        example_get_supported_languages()
        
        # The following examples require authentication
        print("\n⚠️  Note: The following examples require a valid JWT token")
        print("   Update JWT_TOKEN variable with your actual token to test")
        
        # Uncomment these when you have a valid token:
        # example_execute_python_code()
        # example_execute_javascript_code()
        # example_execute_with_input()
        # example_validate_code()
        # example_error_handling()
        
        # Show frontend integration example
        frontend_integration_example()
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server")
        print("   Make sure the Flask server is running on localhost:5000")
    except Exception as e:
        print(f"❌ Error: {e}")
    
    print("\n✅ Examples completed!")
    print("\nAPI Endpoints Summary:")
    print("- GET  /api/coding/languages         - Get supported languages")
    print("- POST /api/coding/execute           - Execute code")
    print("- POST /api/coding/validate          - Validate code")
    print("- POST /api/coding/snippets/{id}/execute - Execute saved snippet")