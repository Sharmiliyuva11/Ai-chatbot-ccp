# Frontend Integration Example for Code Execution

## React Component Example

Here's a complete React component showing how to integrate the code execution feature:

```jsx
// CodeEditor.jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CodeEditor = () => {
  const [code, setCode] = useState('print("Hello, World!")');
  const [language, setLanguage] = useState('python');
  const [input, setInput] = useState('');
  const [output, setOutput] = useState('');
  const [error, setError] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [supportedLanguages, setSupportedLanguages] = useState([]);
  const [executionTime, setExecutionTime] = useState(null);

  const API_BASE = 'http://localhost:5000/api/coding';
  const authToken = localStorage.getItem('auth_token'); // Your JWT token

  // Fetch supported languages on component mount
  useEffect(() => {
    fetchSupportedLanguages();
  }, []);

  const fetchSupportedLanguages = async () => {
    try {
      const response = await axios.get(`${API_BASE}/languages`);
      if (response.data.success) {
        setSupportedLanguages(response.data.languages);
      }
    } catch (err) {
      console.error('Failed to fetch languages:', err);
    }
  };

  const runCode = async () => {
    setIsRunning(true);
    setOutput('');
    setError('');
    setExecutionTime(null);

    try {
      // First validate the code
      const validationResponse = await axios.post(
        `${API_BASE}/validate`,
        { code, language },
        {
          headers: { 
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (!validationResponse.data.validation.valid) {
        setError(validationResponse.data.validation.error);
        setIsRunning(false);
        return;
      }

      // Execute the code
      const response = await axios.post(
        `${API_BASE}/execute`,
        { code, language, input },
        {
          headers: { 
            'Authorization': `Bearer ${authToken}`,
            'Content-Type': 'application/json'
          }
        }
      );

      if (response.data.success) {
        setOutput(response.data.output);
        setExecutionTime(response.data.execution_time);
        if (response.data.error) {
          setError(response.data.error);
        }
      } else {
        setError(response.data.error);
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Network error occurred');
    } finally {
      setIsRunning(false);
    }
  };

  const getLanguageExample = (lang) => {
    const examples = {
      python: 'print("Hello, Python!")\nname = input("Enter your name: ")\nprint(f"Hello, {name}!")',
      javascript: 'console.log("Hello, JavaScript!");\nconst name = "World";\nconsole.log(`Hello, ${name}!`);',
      java: 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, Java!");\n    }\n}',
      cpp: '#include <iostream>\nusing namespace std;\n\nint main() {\n    cout << "Hello, C++!" << endl;\n    return 0;\n}',
      c: '#include <stdio.h>\n\nint main() {\n    printf("Hello, C!\\n");\n    return 0;\n}',
    };
    return examples[lang] || 'console.log("Hello, World!");';
  };

  const handleLanguageChange = (newLanguage) => {
    setLanguage(newLanguage);
    setCode(getLanguageExample(newLanguage));
    setOutput('');
    setError('');
  };

  return (
    <div className="code-editor-container">
      {/* Header */}
      <div className="editor-header">
        <div className="language-selector">
          <label htmlFor="language-select">Language:</label>
          <select
            id="language-select"
            value={language}
            onChange={(e) => handleLanguageChange(e.target.value)}
            className="language-dropdown"
          >
            {supportedLanguages.map(lang => (
              <option key={lang} value={lang}>
                {lang.charAt(0).toUpperCase() + lang.slice(1)}
              </option>
            ))}
          </select>
        </div>

        <button 
          onClick={runCode} 
          disabled={isRunning}
          className="run-button"
        >
          {isRunning ? 'Running...' : '▶ Run Code'}
        </button>
      </div>

      {/* Code Editor */}
      <div className="editor-content">
        <div className="code-section">
          <label htmlFor="code-editor">Code:</label>
          <textarea
            id="code-editor"
            value={code}
            onChange={(e) => setCode(e.target.value)}
            className="code-textarea"
            rows={15}
            placeholder={`Enter your ${language} code here...`}
          />
        </div>

        <div className="input-section">
          <label htmlFor="input-area">Input (for interactive programs):</label>
          <textarea
            id="input-area"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="input-textarea"
            rows={3}
            placeholder="Enter program input here (each line represents one input)..."
          />
        </div>
      </div>

      {/* Output Section */}
      <div className="output-section">
        {executionTime && (
          <div className="execution-info">
            <span>Executed in {executionTime}s</span>
          </div>
        )}

        {output && (
          <div className="output-area">
            <h4>Output:</h4>
            <pre className="output-text">{output}</pre>
          </div>
        )}

        {error && (
          <div className="error-area">
            <h4>Error:</h4>
            <pre className="error-text">{error}</pre>
          </div>
        )}
      </div>
    </div>
  );
};

export default CodeEditor;
```

## CSS Styles

```css
/* CodeEditor.css */
.code-editor-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
}

.editor-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.language-selector label {
  margin-right: 10px;
  font-weight: bold;
}

.language-dropdown {
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.run-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
  font-weight: bold;
  transition: background-color 0.3s;
}

.run-button:hover:not(:disabled) {
  background-color: #218838;
}

.run-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.editor-content {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.code-section, .input-section {
  display: flex;
  flex-direction: column;
}

.code-section label, .input-section label {
  font-weight: bold;
  margin-bottom: 5px;
}

.code-textarea, .input-textarea {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 14px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  resize: vertical;
  background-color: #f8f9fa;
}

.code-textarea {
  min-height: 400px;
}

.input-textarea {
  min-height: 80px;
}

.output-section {
  border-top: 1px solid #ddd;
  padding-top: 20px;
}

.execution-info {
  background-color: #e3f2fd;
  padding: 8px 12px;
  border-radius: 4px;
  margin-bottom: 15px;
  font-size: 14px;
  color: #1565c0;
}

.output-area, .error-area {
  margin-bottom: 15px;
}

.output-area h4 {
  color: #28a745;
  margin-bottom: 10px;
}

.error-area h4 {
  color: #dc3545;
  margin-bottom: 10px;
}

.output-text, .error-text {
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 15px;
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
  font-size: 13px;
  white-space: pre-wrap;
  max-height: 300px;
  overflow-y: auto;
  margin: 0;
}

.error-text {
  background-color: #f8d7da;
  border-color: #f5c6cb;
  color: #721c24;
}

@media (max-width: 768px) {
  .editor-content {
    grid-template-columns: 1fr;
  }
  
  .editor-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
}
```

## Integration with Monaco Editor (Advanced)

For a more professional code editor experience, integrate with Monaco Editor:

```jsx
// CodeEditorWithMonaco.jsx
import React, { useState, useRef } from 'react';
import Editor from '@monaco-editor/react';
import axios from 'axios';

const CodeEditorWithMonaco = () => {
  const editorRef = useRef(null);
  const [language, setLanguage] = useState('python');
  const [output, setOutput] = useState('');
  const [isRunning, setIsRunning] = useState(false);

  const handleEditorDidMount = (editor, monaco) => {
    editorRef.current = editor;
  };

  const runCode = async () => {
    const code = editorRef.current.getValue();
    setIsRunning(true);
    
    try {
      const response = await axios.post('/api/coding/execute', {
        code,
        language,
        input: ''
      }, {
        headers: { 'Authorization': `Bearer ${localStorage.getItem('auth_token')}` }
      });
      
      setOutput(response.data.output || response.data.error);
    } catch (error) {
      setOutput(error.message);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      <div style={{ padding: '10px', backgroundColor: '#f0f0f0' }}>
        <select 
          value={language} 
          onChange={(e) => setLanguage(e.target.value)}
          style={{ marginRight: '10px' }}
        >
          <option value="python">Python</option>
          <option value="javascript">JavaScript</option>
          <option value="java">Java</option>
          <option value="cpp">C++</option>
          <option value="c">C</option>
        </select>
        
        <button onClick={runCode} disabled={isRunning}>
          {isRunning ? 'Running...' : 'Run Code'}
        </button>
      </div>
      
      <div style={{ flex: 1, display: 'flex' }}>
        <div style={{ flex: 1 }}>
          <Editor
            height="100%"
            defaultLanguage={language}
            language={language}
            defaultValue="print('Hello, World!')"
            theme="vs-dark"
            onMount={handleEditorDidMount}
            options={{
              minimap: { enabled: false },
              scrollBeyondLastLine: false,
              fontSize: 14,
            }}
          />
        </div>
        
        <div style={{ 
          width: '300px', 
          backgroundColor: '#1e1e1e', 
          color: 'white', 
          padding: '10px',
          fontFamily: 'monospace',
          whiteSpace: 'pre-wrap',
          overflow: 'auto'
        }}>
          <h4>Output:</h4>
          {output}
        </div>
      </div>
    </div>
  );
};

export default CodeEditorWithMonaco;
```

## Usage in Parent Component

```jsx
// App.jsx or CodingSpace.jsx
import React from 'react';
import CodeEditor from './components/CodeEditor';
import './styles/CodeEditor.css';

const CodingSpace = () => {
  return (
    <div className="coding-space">
      <h1>Code Execution Environment</h1>
      <CodeEditor />
    </div>
  );
};

export default CodingSpace;
```

## Installation Requirements

```bash
# Install required packages
npm install axios @monaco-editor/react

# Or with yarn
yarn add axios @monaco-editor/react
```

## Key Integration Points

1. **Authentication**: Use your existing JWT token system
2. **API Base URL**: Update to match your backend URL
3. **Error Handling**: Integrate with your existing error handling system
4. **Styling**: Adapt styles to match your application theme
5. **State Management**: Consider integrating with Redux/Context if needed

This example provides a fully functional code execution interface that integrates seamlessly with the backend API endpoints you've implemented.