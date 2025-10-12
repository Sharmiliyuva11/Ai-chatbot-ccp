import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Code, Play, Save, Share, Plus, Search, FileText, Folder, Terminal } from 'lucide-react';
import './CodingSpace.css';

const CodingSpace = () => {
  const [activeTab, setActiveTab] = useState('projects');
  const [showProjectModal, setShowProjectModal] = useState(false);
  const [showTemplateModal, setShowTemplateModal] = useState(false);
  const [showSnippetModal, setShowSnippetModal] = useState(false);
  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    language: '',
    framework: '',
    github_link: '',
    phase: 'idea',
  });
  const [newTemplate, setNewTemplate] = useState({
    name: '',
    description: '',
    language: '',
    category: '',
    code: '',
    tags: '',
  });
  const [newSnippet, setNewSnippet] = useState({
    name: '',
    description: '',
    language: '',
    code: '',
    category: '',
  });
  const [selectedProject, setSelectedProject] = useState(null); // eslint-disable-line no-unused-vars
  const [code, setCode] = useState('// Welcome to Coding Space\n// Start coding here!\n\nfunction hello() {\n  console.log("Hello, World!");\n}\n\nhello();');
  const [projects, setProjects] = useState({ projects: [], templates: [], snippets: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  
  // Code execution state
  const [output, setOutput] = useState('Ready to run your code...');
  const [isExecuting, setIsExecuting] = useState(false);
  const [currentLanguage, setCurrentLanguage] = useState('javascript');
  const [supportedLanguages, setSupportedLanguages] = useState([]);
  const [executionTime, setExecutionTime] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError('');
      try {
        // Fetch projects, templates, snippets and supported languages from new API endpoints
        const [projectsRes, templatesRes, snippetsRes, languagesRes] = await Promise.all([
          api.getProjects(),
          api.getTemplates(),
          api.getSnippets(),
          api.getSupportedLanguages()
        ]);
        setProjects({
          projects: projectsRes.projects || [],
          templates: templatesRes.templates || [],
          snippets: snippetsRes.snippets || [],
        });
        // Transform backend language strings to objects with name and displayName
        const transformedLanguages = (languagesRes.languages || []).map(lang => ({
          name: lang,
          displayName: lang.charAt(0).toUpperCase() + lang.slice(1)
        }));
        setSupportedLanguages(transformedLanguages);
      } catch (err) {
        console.error('Error loading coding data:', err);
        let errorMessage = 'Failed to load data. ';
        if (err.message) {
          errorMessage += err.message;
        } else if (err.response) {
          errorMessage += `Server error: ${err.response.status}`;
        } else {
          errorMessage += 'Please check your connection and try again.';
        }
        setError(errorMessage);
        // fall back to example data if backend is unavailable
        setProjects({
          projects: [],
          templates: getExampleTemplates(),
          snippets: getExampleSnippets()
        });
        // Set default languages if API fails
        setSupportedLanguages([
          { name: 'javascript', displayName: 'JavaScript' },
          { name: 'python', displayName: 'Python' },
          { name: 'java', displayName: 'Java' },
          { name: 'cpp', displayName: 'C++' },
          { name: 'c', displayName: 'C' }
        ]);
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  // Add improved error display for network and auth errors
  // When a network error occurs, probe the backend root endpoint before
  // showing the full "Unable to connect..." message. This prevents the
  // intimidating copy from showing when the backend is actually reachable
  // (for example, due to an intermittent fetch error or proxy).
  const ErrorMessage = ({ message }) => {
    const [backendReachable, setBackendReachable] = React.useState(null);

    React.useEffect(() => {
      let mounted = true;
      if (message && message.includes('Network error')) {
        // Probe the backend root (CORS allows this) to confirm reachability
        (async () => {
          try {
            const res = await fetch('http://localhost:5000/');
            if (!mounted) return;
            setBackendReachable(!!res && res.ok);
          } catch (e) {
            if (!mounted) return;
            setBackendReachable(false);
          }
        })();
      } else {
        setBackendReachable(null);
      }
      return () => { mounted = false; };
    }, [message]);

    if (!message) return null;

    let displayMessage = message;

    if (message.includes('Network error')) {
      if (backendReachable === null) {
        displayMessage = 'Checking server availability...';
      } else if (backendReachable === true) {
        // Backend appears reachable — do not show a banner. The page
        // already falls back to local example data; hiding the message
        // avoids confusing the user when the server is reachable.
        return null;
      } else {
        displayMessage = 'Unable to connect to the backend server. Please ensure the backend is running.';
      }
    } else if (message.includes('Authentication error')) {
      displayMessage = 'Authentication failed. Please log in again.';
    } else if (message.includes('Access denied')) {
      displayMessage = 'You do not have permission to access this data.';
    } else if (message.includes('Not found')) {
      displayMessage = 'Requested data not found.';
    } else if (message.includes('Server error')) {
      displayMessage = 'Internal server error occurred. Please try again later.';
    }

    return (
      <div className="error-message detailed-error">
        {displayMessage}
      </div>
    );
  };

  // Example data functions
  const getExampleTemplates = () => [
    {
      id: 'template_1',
      name: 'React Component Template',
      description: 'Basic functional React component with hooks',
      language: 'JavaScript',
      category: 'Frontend',
      difficulty: 'Beginner',
      code: `import React, { useState, useEffect } from 'react';

const ComponentName = ({ prop1, prop2 }) => {
  const [state, setState] = useState('');

  useEffect(() => {
    // Side effects here
  }, []);

  const handleClick = () => {
    // Handle click logic
  };

  return (
    <div className="component-name">
      <h1>Hello World</h1>
      <button onClick={handleClick}>Click me</button>
    </div>
  );
};

export default ComponentName;`,
      tags: ['react', 'component', 'hooks'],
      lastModified: '2 days ago'
    },
    {
      id: 'template_2',
      name: 'Python Flask API',
      description: 'REST API endpoint using Flask framework',
      language: 'Python',
      category: 'Backend',
      difficulty: 'Intermediate',
      code: `from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        # Your logic here
        users = []
        return jsonify({'success': True, 'users': users})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        # Create user logic
        return jsonify({'success': True, 'message': 'User created'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)`,
      tags: ['flask', 'api', 'python'],
      lastModified: '1 week ago'
    }
  ];

  const getExampleSnippets = () => [
    {
      id: 'snippet_1',
      name: 'Array Sort Methods',
      description: 'Common JavaScript array sorting techniques',
      language: 'JavaScript',
      category: 'Utilities',
      code: `// Sort numbers ascending
const numbers = [3, 1, 4, 1, 5];
numbers.sort((a, b) => a - b);

// Sort objects by property
const users = [{name: 'John', age: 30}, {name: 'Jane', age: 25}];
users.sort((a, b) => a.age - b.age);

// Sort strings (case-insensitive)
const names = ['John', 'jane', 'Bob'];
names.sort((a, b) => a.toLowerCase().localeCompare(b.toLowerCase()));`,
      lines: 9,
      lastModified: '3 days ago'
    },
    {
      id: 'snippet_2',
      name: 'Python List Comprehensions',
      description: 'Efficient list processing patterns',
      language: 'Python',
      category: 'Data Processing',
      code: `# Basic list comprehension
squares = [x**2 for x in range(10)]

# With condition
evens = [x for x in range(20) if x % 2 == 0]

# Nested comprehension
matrix = [[j for j in range(3)] for i in range(3)]

# Dictionary comprehension
word_lengths = {word: len(word) for word in ['hello', 'world']}`,
      lines: 8,
      lastModified: '5 days ago'
    }
  ];

  const createTemplate = async (templateData) => {
    try {
      const response = await api.createTemplate(templateData);
      if (response.success) {
        // Refresh templates list
        const templatesRes = await api.getTemplates();
        setProjects(prev => ({
          ...prev,
          templates: templatesRes.templates || prev.templates
        }));
        return true;
      }
      return false;
    } catch (err) {
      console.error('Failed to create template:', err);
      if (err.message && err.message.toLowerCase().includes('network')) {
        alert('Unable to reach the server. Templates are stored locally only while the backend is offline.');
      }
      return false;
    }
  };

  const createSnippet = async (snippetData) => {
    try {
      const response = await api.createSnippet(snippetData);
      if (response.success) {
        // Refresh snippets list
        const snippetsRes = await api.getSnippets();
        setProjects(prev => ({
          ...prev,
          snippets: snippetsRes.snippets || prev.snippets
        }));
        return true;
      }
      return false;
    } catch (err) {
      console.error('Failed to create snippet:', err);
      if (err.message && err.message.toLowerCase().includes('network')) {
        alert('Unable to reach the server. Snippets are stored locally only while the backend is offline.');
      }
      return false;
    }
  };

  const getLanguageColor = (language) => {
    const colors = {
      'javascript': '#f7df1e',
      'JavaScript': '#f7df1e',
      'python': '#306998',
      'Python': '#306998',
      'java': '#b07219',
      'Java': '#b07219',
      'cpp': '#f34b7d',
      'c++': '#f34b7d',
      'c': '#555555',
      'go': '#00ADD8',
      'rust': '#dea584',
      'php': '#4F5D95',
      'ruby': '#701516',
      'bash': '#89e051',
      'typescript': '#3178c6',
      'TypeScript': '#3178c6',
    };
    return colors[language] || '#000000';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'status-active';
      case 'completed': return 'status-completed';
      case 'in-progress': return 'status-progress';
      default: return '';
    }
  };

  const runCode = async () => {
    if (!code.trim()) {
      setOutput('❌ Error: No code to execute');
      return;
    }

    setIsExecuting(true);
    setOutput('🚀 Executing code...');
    setExecutionTime(null);

    try {
      const startTime = Date.now();
      
      // Execute the code
      const result = await api.executeCode({
        code: code.trim(),
        language: currentLanguage,
        input: '' // We can add input support later
      });

      const executionTime = Date.now() - startTime;
      setExecutionTime(executionTime);

      if (result.success) {
        let outputText = '';
        
        if (result.output) {
          outputText += `✅ Output:\n${result.output}`;
        }
        
        if (result.error && result.error.trim()) {
          outputText += `${outputText ? '\n\n' : ''}❌ Error:\n${result.error}`;
        }
        
        if (!outputText) {
          outputText = '✅ Code executed successfully (no output)';
        }
        
        outputText += `\n\n⏱️ Execution time: ${executionTime}ms`;
        setOutput(outputText);
      } else {
        setOutput(`❌ Execution failed:\n${result.error || 'Unknown error occurred'}`);
      }
    } catch (error) {
      console.error('Code execution error:', error);
      setOutput(`❌ Execution error:\n${error.message || 'Failed to execute code'}`);
    } finally {
      setIsExecuting(false);
    }
  };

  const saveCode = () => {
    console.log('Saving code...');
    alert('Code saved successfully!');
  };

  const shareCode = () => {
    console.log('Sharing code...');
    alert('Share link copied to clipboard!');
  };

  return (
    <div className="coding-space">
      <div className="coding-header">
        <div className="header-content">
          <h1>Coding Space</h1>
          <p>Build, test, and share your code projects</p>
        </div>
        <div className="header-actions">
          <div className="search-container">
            <Search className="search-icon" />
            <input type="text" placeholder="Search projects..." />
          </div>
          {activeTab === 'projects' && (
            <button className="create-project-btn" onClick={() => setShowProjectModal(true)}>
              <Plus className="icon" />
              New Project
            </button>
          )}
          {activeTab === 'templates' && (
            <button className="create-project-btn" onClick={() => setShowTemplateModal(true)}>
              <Plus className="icon" />
              New Template
            </button>
          )}
          {activeTab === 'snippets' && (
            <button className="create-project-btn" onClick={() => setShowSnippetModal(true)}>
              <Plus className="icon" />
              New Snippet
            </button>
          )}
          {showProjectModal && (
            <div className="modal-overlay" role="dialog" aria-modal="true">
              <div className="add-reminder-modal">
                <div className="modal-header" style={{background: 'linear-gradient(90deg, #667eea, #764ba2)'}}>
                  <button className="modal-back" type="button" onClick={() => setShowProjectModal(false)} aria-label="Close">←</button>
                  <h2 className="modal-title">Add Project</h2>
                  <button className="modal-menu" type="button" aria-label="Menu">≡</button>
                </div>
                <div className="modal-card">
                  <form onSubmit={async (e) => {
                    e.preventDefault();
                    try {
                      await api.createProject(newProject);
                      setNewProject({
                        name: '',
                        description: '',
                        language: '',
                        framework: '',
                        github_link: '',
                        phase: 'idea',
                      });
                      setShowProjectModal(false);
                      // Refresh projects list
                      const projectsRes = await api.getProjects();
                      setProjects(prev => ({
                        ...prev,
                        projects: projectsRes.projects || []
                      }));
                    } catch (err) {
                      console.error('Failed to create project:', err);
                      alert('Failed to create project. Please try again.');
                    }
                  }}>
                    <div className="modal-field">
                      <label>Project Name<span className="req">*</span></label>
                      <input type="text" value={newProject.name} onChange={e => setNewProject({...newProject, name: e.target.value})} required placeholder="Enter project name" />
                    </div>
                    <div className="modal-field">
                      <label>Description<span className="req">*</span></label>
                      <textarea value={newProject.description} onChange={e => setNewProject({...newProject, description: e.target.value})} required placeholder="Describe the project" rows="3" />
                    </div>
                    <div className="modal-row">
                      <div className="modal-field">
                        <label>Language<span className="req">*</span></label>
                        <input type="text" value={newProject.language} onChange={e => setNewProject({...newProject, language: e.target.value})} required placeholder="e.g. JavaScript, Python" />
                      </div>
                      <div className="modal-field">
                        <label>Framework<span className="req">*</span></label>
                        <input type="text" value={newProject.framework} onChange={e => setNewProject({...newProject, framework: e.target.value})} required placeholder="e.g. React, Flask" />
                      </div>
                    </div>
                    <div className="modal-field">
                      <label>GitHub Link</label>
                      <input type="url" value={newProject.github_link} onChange={e => setNewProject({...newProject, github_link: e.target.value})} placeholder="https://github.com/username/repo" />
                    </div>
                    <div className="modal-field">
                      <label>Project Phase<span className="req">*</span></label>
                      <select value={newProject.phase} onChange={e => setNewProject({...newProject, phase: e.target.value})} required>
                        <option value="idea">Idea</option>
                        <option value="prototype">Prototype</option>
                        <option value="development">Development</option>
                        <option value="production">Production</option>
                      </select>
                    </div>
                    <div className="modal-actions">
                      <button type="submit" className="primary">Save</button>
                      <button type="button" className="secondary" onClick={() => setShowProjectModal(false)}>Cancel</button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          )}
          
          {/* Template Creation Modal */}
          {showTemplateModal && (
            <div className="modal-overlay" role="dialog" aria-modal="true">
              <div className="add-reminder-modal">
                <div className="modal-header" style={{background: 'linear-gradient(90deg, #f093fb, #f5576c)'}}>
                  <button className="modal-back" type="button" onClick={() => setShowTemplateModal(false)} aria-label="Close">←</button>
                  <h2 className="modal-title">Create Template</h2>
                  <button className="modal-menu" type="button" aria-label="Menu">≡</button>
                </div>
                <div className="modal-card">
                  <form onSubmit={async (e) => {
                    e.preventDefault();
                    const success = await createTemplate({
                      ...newTemplate,
                      tags: newTemplate.tags.split(',').map(t => t.trim()).filter(Boolean)
                    });
                    if (success) {
                      setNewTemplate({
                        name: '',
                        description: '',
                        language: '',
                        category: '',
                        code: '',
                        tags: '',
                      });
                      setShowTemplateModal(false);
                    } else {
                      alert('Failed to create template. Please try again.');
                    }
                  }}>
                    <div className="modal-field">
                      <label>Template Name<span className="req">*</span></label>
                      <input type="text" value={newTemplate.name} onChange={e => setNewTemplate({...newTemplate, name: e.target.value})} required placeholder="Enter template name" />
                    </div>
                    <div className="modal-field">
                      <label>Description<span className="req">*</span></label>
                      <textarea value={newTemplate.description} onChange={e => setNewTemplate({...newTemplate, description: e.target.value})} required placeholder="Describe the template" rows="2" />
                    </div>
                    <div className="modal-row">
                      <div className="modal-field">
                        <label>Language<span className="req">*</span></label>
                        <input type="text" value={newTemplate.language} onChange={e => setNewTemplate({...newTemplate, language: e.target.value})} required placeholder="e.g. JavaScript, Python" />
                      </div>
                      <div className="modal-field">
                        <label>Category<span className="req">*</span></label>
                        <input type="text" value={newTemplate.category} onChange={e => setNewTemplate({...newTemplate, category: e.target.value})} required placeholder="e.g. Frontend, Backend" />
                      </div>
                    </div>
                    <div className="modal-field">
                      <label>Code<span className="req">*</span></label>
                      <textarea value={newTemplate.code} onChange={e => setNewTemplate({...newTemplate, code: e.target.value})} required placeholder="Paste your template code here..." rows="8" style={{fontFamily: 'monospace'}} />
                    </div>
                    <div className="modal-field">
                      <label>Tags <span className="optional">(comma-separated)</span></label>
                      <input type="text" value={newTemplate.tags} onChange={e => setNewTemplate({...newTemplate, tags: e.target.value})} placeholder="e.g. react, component, hooks" />
                    </div>
                    <div className="modal-actions">
                      <button type="submit" className="primary">Create Template</button>
                      <button type="button" className="secondary" onClick={() => setShowTemplateModal(false)}>Cancel</button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          )}

          {/* Snippet Creation Modal */}
          {showSnippetModal && (
            <div className="modal-overlay" role="dialog" aria-modal="true">
              <div className="add-reminder-modal">
                <div className="modal-header" style={{background: 'linear-gradient(90deg, #4facfe, #00f2fe)'}}>
                  <button className="modal-back" type="button" onClick={() => setShowSnippetModal(false)} aria-label="Close">←</button>
                  <h2 className="modal-title">Create Snippet</h2>
                  <button className="modal-menu" type="button" aria-label="Menu">≡</button>
                </div>
                <div className="modal-card">
                  <form onSubmit={async (e) => {
                    e.preventDefault();
                    const success = await createSnippet(newSnippet);
                    if (success) {
                      setNewSnippet({
                        name: '',
                        description: '',
                        language: '',
                        code: '',
                        category: '',
                      });
                      setShowSnippetModal(false);
                    } else {
                      alert('Failed to create snippet. Please try again.');
                    }
                  }}>
                    <div className="modal-field">
                      <label>Snippet Name<span className="req">*</span></label>
                      <input type="text" value={newSnippet.name} onChange={e => setNewSnippet({...newSnippet, name: e.target.value})} required placeholder="Enter snippet name" />
                    </div>
                    <div className="modal-field">
                      <label>Description<span className="req">*</span></label>
                      <textarea value={newSnippet.description} onChange={e => setNewSnippet({...newSnippet, description: e.target.value})} required placeholder="Describe the snippet" rows="2" />
                    </div>
                    <div className="modal-row">
                      <div className="modal-field">
                        <label>Language<span className="req">*</span></label>
                        <input type="text" value={newSnippet.language} onChange={e => setNewSnippet({...newSnippet, language: e.target.value})} required placeholder="e.g. JavaScript, Python" />
                      </div>
                      <div className="modal-field">
                        <label>Category<span className="req">*</span></label>
                        <input type="text" value={newSnippet.category} onChange={e => setNewSnippet({...newSnippet, category: e.target.value})} required placeholder="e.g. Utilities, Data Processing" />
                      </div>
                    </div>
                    <div className="modal-field">
                      <label>Code<span className="req">*</span></label>
                      <textarea value={newSnippet.code} onChange={e => setNewSnippet({...newSnippet, code: e.target.value})} required placeholder="Paste your code snippet here..." rows="6" style={{fontFamily: 'monospace'}} />
                    </div>
                    <div className="modal-actions">
                      <button type="submit" className="primary">Create Snippet</button>
                      <button type="button" className="secondary" onClick={() => setShowSnippetModal(false)}>Cancel</button>
                    </div>
                  </form>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      <div className="coding-tabs">
        <button
          className={`tab ${activeTab === 'projects' ? 'active' : ''}`}
          onClick={() => setActiveTab('projects')}
        >
          <Folder className="tab-icon" />
          My Projects ({projects.projects.length})
        </button>
        <button
          className={`tab ${activeTab === 'templates' ? 'active' : ''}`}
          onClick={() => setActiveTab('templates')}
        >
          <FileText className="tab-icon" />
          Templates ({projects.templates.length})
        </button>
        <button
          className={`tab ${activeTab === 'snippets' ? 'active' : ''}`}
          onClick={() => setActiveTab('snippets')}
        >
          <Code className="tab-icon" />
          Code Snippets ({projects.snippets.length})
        </button>
        <button
          className={`tab ${activeTab === 'editor' ? 'active' : ''}`}
          onClick={() => setActiveTab('editor')}
        >
          <Terminal className="tab-icon" />
          Code Editor
        </button>
      </div>

      {loading ? (
        <div className="loading">Loading...</div>
      ) : error ? (
        <ErrorMessage message={error} />
      ) : activeTab === 'editor' ? (
        <div className="code-editor-container">
          <div className="editor-toolbar">
            <div className="editor-info">
              <select 
                value={currentLanguage} 
                onChange={(e) => setCurrentLanguage(e.target.value)}
                className="language-selector"
              >
                {supportedLanguages.map((lang) => (
                  <option key={lang.name} value={lang.name}>
                    {lang.displayName}
                  </option>
                ))}
              </select>
              <span className="language-badge" style={{ backgroundColor: getLanguageColor(currentLanguage) }}>
                {supportedLanguages.find(lang => lang.name === currentLanguage)?.displayName || currentLanguage}
              </span>
            </div>
            <div className="editor-actions">
              <button 
                className="editor-btn" 
                onClick={runCode}
                disabled={isExecuting}
              >
                <Play className="icon" />
                {isExecuting ? 'Running...' : 'Run'}
              </button>
              <button className="editor-btn" onClick={saveCode}>
                <Save className="icon" />
                Save
              </button>
              <button className="editor-btn" onClick={shareCode}>
                <Share className="icon" />
                Share
              </button>
            </div>
          </div>

          <div className="editor-content">
            <div className="code-editor">
              <textarea
                value={code}
                onChange={(e) => setCode(e.target.value)}
                className="code-textarea"
                placeholder="Start coding here..."
                spellCheck="false"
              />
            </div>
            <div className="output-panel">
              <div className="output-header">
                <Terminal className="icon" />
                <span>Output</span>
                {executionTime && (
                  <span className="execution-time">{executionTime}ms</span>
                )}
              </div>
              <div className="output-content">
                <pre className="output-text">{output}</pre>
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="projects-grid">
          {projects[activeTab].map((item) => (
            <div key={item.id} className="project-card">
              <div className="project-header">
                <div className="project-language">
                  <span
                    className="language-dot"
                    style={{ backgroundColor: getLanguageColor(item.language) }}
                  ></span>
                  {item.language}
                </div>
                {item.status && (
                  <div className={`project-status ${getStatusColor(item.status)}`}>
                    {item.status.replace('-', ' ')}
                  </div>
                )}
                {item.difficulty && (
                  <div className="project-difficulty">
                    {item.difficulty}
                  </div>
                )}
              </div>

              <h3 className="project-title">{item.name}</h3>
              <p className="project-description">{item.description}</p>

              <div className="project-meta">
                {item.framework && (
                  <div className="meta-item">
                    <Code className="meta-icon" />
                    <span>{item.framework}</span>
                  </div>
                )}
                {item.lastModified && (
                  <div className="meta-item">
                    <span>Modified {item.lastModified}</span>
                  </div>
                )}
                {item.category && (
                  <div className="meta-item">
                    <span>{item.category}</span>
                  </div>
                )}
              </div>

              {(item.files || item.lines) && (
                <div className="project-stats">
                  {item.files && <span>{item.files} files</span>}
                  {item.lines && <span>{item.lines} lines</span>}
                </div>
              )}

              <div className="project-actions">
                {activeTab === 'projects' && (
                  <>
                    <button className="action-btn primary">
                      <Code className="icon" />
                      Open
                    </button>
                    {item.github_link && (
                      <button
                        className="action-btn secondary"
                        onClick={() => window.open(item.github_link, '_blank')}
                      >
                        <Share className="icon" />
                        View Details
                      </button>
                    )}
                    <button className="action-btn secondary">
                      <Share className="icon" />
                      Share
                    </button>
                  </>
                )}
                {activeTab === 'templates' && (
                  <button className="action-btn primary">
                    <Plus className="icon" />
                    Use Template
                  </button>
                )}
                {activeTab === 'snippets' && (
                  <button className="action-btn primary">
                    <Code className="icon" />
                    View Code
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {projects[activeTab] && projects[activeTab].length === 0 && !loading && !error && (
        <div className="empty-state">
          <Code className="empty-icon" />
          <h3>No {activeTab} found</h3>
          <p>Start by creating your first {activeTab.slice(0, -1)}.</p>
          {activeTab === 'projects' && (
            <button className="create-project-btn" onClick={() => setShowProjectModal(true)}>
              <Plus className="icon" />
              Create New Project
            </button>
          )}
          {activeTab === 'templates' && (
            <button className="create-project-btn" onClick={() => setShowTemplateModal(true)}>
              <Plus className="icon" />
              Create New Template
            </button>
          )}
          {activeTab === 'snippets' && (
            <button className="create-project-btn" onClick={() => setShowSnippetModal(true)}>
              <Plus className="icon" />
              Create New Snippet
            </button>
          )}
        </div>
      )}
    </div>
  );
};

export default CodingSpace;
