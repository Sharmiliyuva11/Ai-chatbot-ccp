import subprocess
import tempfile
import os
import json
import time
import signal
from typing import Dict, Any, Tuple
import threading

class CodeExecutionService:
    """
    Service for executing code in various programming languages safely
    """
    
    # Supported languages and their configurations
    LANGUAGE_CONFIGS = {
        'python': {
            'extension': '.py',
            'command': ['python'],
            'timeout': 30
        },
        'javascript': {
            'extension': '.js',
            'command': ['node'],
            'timeout': 30
        },
        'java': {
            'extension': '.java',
            'compile_command': ['javac'],
            'run_command': ['java'],
            'timeout': 45
        },
        'cpp': {
            'extension': '.cpp',
            'compile_command': ['g++', '-o'],
            'timeout': 45
        },
        'c': {
            'extension': '.c',
            'compile_command': ['gcc', '-o'],
            'timeout': 45
        },
        'go': {
            'extension': '.go',
            'command': ['go', 'run'],
            'timeout': 30
        },
        'rust': {
            'extension': '.rs',
            'compile_command': ['rustc'],
            'timeout': 45
        },
        'php': {
            'extension': '.php',
            'command': ['php'],
            'timeout': 30
        },
        'ruby': {
            'extension': '.rb',
            'command': ['ruby'],
            'timeout': 30
        },
        'bash': {
            'extension': '.sh',
            'command': ['bash'],
            'timeout': 30
        }
    }
    
    @classmethod
    def execute_code(cls, code: str, language: str, input_data: str = "") -> Dict[str, Any]:
        """
        Execute code in the specified language
        
        Args:
            code: The source code to execute
            language: Programming language (python, javascript, java, etc.)
            input_data: Input data to pass to the program
            
        Returns:
            Dict containing execution results
        """
        language = language.lower()
        
        if language not in cls.LANGUAGE_CONFIGS:
            return {
                'success': False,
                'error': f'Unsupported language: {language}',
                'supported_languages': list(cls.LANGUAGE_CONFIGS.keys())
            }
        
        config = cls.LANGUAGE_CONFIGS[language]
        
        try:
            # Create temporary directory for execution
            with tempfile.TemporaryDirectory() as temp_dir:
                # Write code to temporary file
                file_path = os.path.join(temp_dir, f"main{config['extension']}")
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(code)
                
                # Handle compilation if needed
                if 'compile_command' in config:
                    compile_result = cls._compile_code(file_path, config, temp_dir)
                    if not compile_result['success']:
                        return compile_result
                    
                    # Update file_path for execution
                    if language in ['java']:
                        # For Java, extract class name
                        class_name = cls._extract_java_class_name(code)
                        if class_name:
                            file_path = class_name
                        else:
                            return {
                                'success': False,
                                'error': 'Could not find public class in Java code'
                            }
                    else:
                        # For C/C++/Rust, use compiled executable
                        file_path = os.path.join(temp_dir, "main")
                
                # Execute the code
                return cls._execute_file(file_path, config, input_data, temp_dir, language)
                
        except Exception as e:
            return {
                'success': False,
                'error': f'Execution failed: {str(e)}'
            }
    
    @classmethod
    def _compile_code(cls, file_path: str, config: Dict, temp_dir: str) -> Dict[str, Any]:
        """Compile code if compilation is required"""
        try:
            compile_cmd = config['compile_command'].copy()
            
            if config['compile_command'][0] in ['gcc', 'g++']:
                # For C/C++
                compile_cmd.extend([file_path, '-o', os.path.join(temp_dir, 'main')])
            elif config['compile_command'][0] == 'javac':
                # For Java
                compile_cmd.append(file_path)
            elif config['compile_command'][0] == 'rustc':
                # For Rust
                compile_cmd.extend([file_path, '-o', os.path.join(temp_dir, 'main')])
            
            result = subprocess.run(
                compile_cmd,
                cwd=temp_dir,
                capture_output=True,
                text=True,
                timeout=config['timeout']
            )
            
            if result.returncode != 0:
                return {
                    'success': False,
                    'error': f'Compilation failed: {result.stderr}'
                }
            
            return {'success': True}
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': 'Compilation timeout'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Compilation error: {str(e)}'
            }
    
    @classmethod
    def _execute_file(cls, file_path: str, config: Dict, input_data: str, temp_dir: str, language: str) -> Dict[str, Any]:
        """Execute the code file"""
        try:
            # Prepare command
            if 'command' in config:
                if language == 'java':
                    cmd = config.get('run_command', ['java']) + [file_path]
                elif language in ['cpp', 'c', 'rust']:
                    cmd = [file_path]  # Direct execution of compiled binary
                else:
                    cmd = config['command'] + [file_path]
            else:
                cmd = [file_path]  # For compiled languages without explicit command
            
            # Execute with timeout
            start_time = time.time()
            
            result = subprocess.run(
                cmd,
                cwd=temp_dir,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=config['timeout']
            )
            
            execution_time = time.time() - start_time
            
            return {
                'success': True,
                'output': result.stdout,
                'error': result.stderr,
                'execution_time': round(execution_time, 3),
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'error': f'Execution timeout ({config["timeout"]}s)'
            }
        except FileNotFoundError:
            return {
                'success': False,
                'error': f'Runtime not found. Please ensure {language} is installed.'
            }
        except Exception as e:
            return {
                'success': False,
                'error': f'Execution error: {str(e)}'
            }
    
    @classmethod
    def _extract_java_class_name(cls, code: str) -> str:
        """Extract public class name from Java code"""
        import re
        match = re.search(r'public\s+class\s+(\w+)', code)
        return match.group(1) if match else None
    
    @classmethod
    def get_supported_languages(cls) -> list:
        """Get list of supported programming languages"""
        return list(cls.LANGUAGE_CONFIGS.keys())
    
    @classmethod
    def validate_code(cls, code: str, language: str) -> Dict[str, Any]:
        """
        Basic code validation before execution
        
        Args:
            code: Source code to validate
            language: Programming language
            
        Returns:
            Dict with validation results
        """
        if not code or not code.strip():
            return {
                'valid': False,
                'error': 'Code cannot be empty'
            }
        
        if language.lower() not in cls.LANGUAGE_CONFIGS:
            return {
                'valid': False,
                'error': f'Unsupported language: {language}',
                'supported_languages': cls.get_supported_languages()
            }
        
        # Basic security checks
        dangerous_patterns = [
            'import os',
            'import subprocess',
            'import sys',
            '__import__',
            'exec(',
            'eval(',
            'open(',
            'file(',
            'input(',
            'raw_input(',
        ]
        
        code_lower = code.lower()
        found_dangerous = [pattern for pattern in dangerous_patterns if pattern in code_lower]
        
        if found_dangerous:
            return {
                'valid': False,
                'error': f'Code contains potentially dangerous operations: {", ".join(found_dangerous)}',
                'warning': 'For security reasons, file operations and system calls are restricted'
            }
        
        return {'valid': True}