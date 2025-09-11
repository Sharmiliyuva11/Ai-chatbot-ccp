import sys
sys.path.append('.')

from services.code_execution_service import CodeExecutionService

print("🧪 Testing Code Execution Service")
print("=" * 50)

# Test 1: Python execution
print("\n1. Testing Python execution:")
result = CodeExecutionService.execute_code('print("Hello, World!")', 'python')
print(f"   Success: {result['success']}")
print(f"   Output: {result.get('output', 'N/A').strip()}")

# Test 2: Get supported languages
print("\n2. Supported languages:")
languages = CodeExecutionService.get_supported_languages()
print(f"   Languages: {', '.join(languages)}")

# Test 3: Validation
print("\n3. Testing validation:")
validation = CodeExecutionService.validate_code('print("test")', 'python')
print(f"   Valid: {validation['valid']}")

print("\n✅ Basic tests completed!")