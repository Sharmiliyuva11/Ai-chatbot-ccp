import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import { Code, Play, Save, Share, Plus, Search, FileText, Folder, Terminal } from 'lucide-react';
import './CodingSpace.css';

const CodingSpace = () => {
  const [activeTab, setActiveTab] = useState('projects');
  const [showProjectModal, setShowProjectModal] = useState(false);
  const [newProject, setNewProject] = useState({
    name: '',
    description: '',
    language: '',
    framework: '',
    github_link: '',
    phase: 'idea',
  });
  const [selectedProject, setSelectedProject] = useState(null);
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
        setProjects({ projects: [], templates: [], snippets: [] });
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
  const ErrorMessage = ({ message }) => {
    if (!message) return null;

    let displayMessage = message;

    if (message.includes('Network error')) {
      displayMessage = 'Unable to connect to the backend server. Please ensure the backend is running.';
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

  // Removed duplicate getLanguageColor function to fix redeclaration error

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
          <button className="create-project-btn" onClick={() => setShowProjectModal(true)}>
            <Plus className="icon" />
            New Project
          </button>
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
          <button className="create-project-btn">
            <Plus className="icon" />
            Create New {activeTab.slice(0, -1)}
          </button>
        </div>
      )}
    </div>
  );
};

export default CodingSpace;
