"""
Test file for Code Execution Service
"""
import unittest
import json
from services.code_execution_service import CodeExecutionService

class TestCodeExecutionService(unittest.TestCase):
    
    def test_python_code_execution(self):
        """Test Python code execution"""
        code = """
print("Hello, World!")
x = 5 + 3
print(f"5 + 3 = {x}")
"""
        result = CodeExecutionService.execute_code(code, 'python')
        
        self.assertTrue(result['success'])
        self.assertIn("Hello, World!", result['output'])
        self.assertIn("5 + 3 = 8", result['output'])
        self.assertEqual(result['return_code'], 0)
    
    def test_javascript_code_execution(self):
        """Test JavaScript code execution"""
        code = """
console.log("Hello from JavaScript!");
const sum = 10 + 20;
console.log("10 + 20 =", sum);
"""
        result = CodeExecutionService.execute_code(code, 'javascript')
        
        self.assertTrue(result['success'])
        self.assertIn("Hello from JavaScript!", result['output'])
        self.assertIn("10 + 20 = 30", result['output'])
    
    def test_python_with_input(self):
        """Test Python code with input"""
        code = """
name = input("Enter your name: ")
print(f"Hello, {name}!")
"""
        input_data = "Alice\n"
        result = CodeExecutionService.execute_code(code, 'python', input_data)
        
        self.assertTrue(result['success'])
        self.assertIn("Hello, Alice!", result['output'])
    
    def test_code_validation_empty(self):
        """Test validation with empty code"""
        result = CodeExecutionService.validate_code("", 'python')
        
        self.assertFalse(result['valid'])
        self.assertIn("empty", result['error'].lower())
    
    def test_code_validation_unsupported_language(self):
        """Test validation with unsupported language"""
        result = CodeExecutionService.validate_code("print('test')", 'unsupported')
        
        self.assertFalse(result['valid'])
        self.assertIn("Unsupported language", result['error'])
        self.assertIn("supported_languages", result)
    
    def test_code_validation_dangerous_code(self):
        """Test validation with potentially dangerous code"""
        code = """
import os
os.system('rm -rf /')
"""
        result = CodeExecutionService.validate_code(code, 'python')
        
        self.assertFalse(result['valid'])
        self.assertIn("dangerous", result['error'].lower())
    
    def test_get_supported_languages(self):
        """Test getting supported languages"""
        languages = CodeExecutionService.get_supported_languages()
        
        self.assertIsInstance(languages, list)
        self.assertIn('python', languages)
        self.assertIn('javascript', languages)
        self.assertGreater(len(languages), 5)  # Should have multiple languages
    
    def test_execution_timeout_simulation(self):
        """Test execution timeout (simulated with sleep)"""
        code = """
import time
time.sleep(35)  # Should timeout after 30 seconds
print("This shouldn't print")
"""
        result = CodeExecutionService.execute_code(code, 'python')
        
        self.assertFalse(result['success'])
        self.assertIn("timeout", result['error'].lower())
    
    def test_syntax_error_handling(self):
        """Test handling of syntax errors"""
        code = """
print("Missing closing quote
"""
        result = CodeExecutionService.execute_code(code, 'python')
        
        self.assertFalse(result['success'])
        # Should have error information
        self.assertTrue('error' in result)
    
    def test_runtime_error_handling(self):
        """Test handling of runtime errors"""
        code = """
x = 10 / 0  # Division by zero
"""
        result = CodeExecutionService.execute_code(code, 'python')
        
        # Code executes but returns error
        self.assertTrue(result['success'])  # Execution completed
        self.assertNotEqual(result['return_code'], 0)  # But with error code
        self.assertIn("ZeroDivisionError", result['error'])

if __name__ == '__main__':
    # Run individual tests to check functionality
    service = CodeExecutionService()
    
    print("🧪 Testing Code Execution Service")
    print("=" * 50)
    
    # Test 1: Python execution
    print("\n1. Testing Python execution:")
    result = service.execute_code('print("Hello, World!")', 'python')
    print(f"   Success: {result['success']}")
    print(f"   Output: {result.get('output', 'N/A').strip()}")
    
    # Test 2: JavaScript execution (if Node.js is available)
    print("\n2. Testing JavaScript execution:")
    result = service.execute_code('console.log("Hello from JS!");', 'javascript')
    print(f"   Success: {result['success']}")
    print(f"   Output: {result.get('output', result.get('error', 'N/A')).strip()}")
    
    # Test 3: Get supported languages
    print("\n3. Supported languages:")
    languages = service.get_supported_languages()
    print(f"   Languages: {', '.join(languages)}")
    
    # Test 4: Validation
    print("\n4. Testing validation:")
    validation = service.validate_code('print("test")', 'python')
    print(f"   Valid: {validation['valid']}")
    
    # Test 5: Error handling
    print("\n5. Testing error handling:")
    result = service.execute_code('invalid syntax here', 'python')
    print(f"   Success: {result['success']}")
    if not result['success']:
        print(f"   Error: {result.get('error', 'Unknown error')}")
    
    print("\n✅ Basic tests completed!")