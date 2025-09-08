
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
  });
  const [selectedProject, setSelectedProject] = useState(null);
  const [code, setCode] = useState('// Welcome to Coding Space\n// Start coding here!\n\nfunction hello() {\n  console.log("Hello, World!");\n}\n\nhello();');
  const [projects, setProjects] = useState({ projects: [], templates: [], snippets: [] });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError('');
      try {
        // Replace with actual API endpoints for projects, templates, snippets
        // Example: await api.getProjects(), api.getTemplates(), api.getSnippets()
        // For now, fallback to static if API not implemented
        const userProjects = await api.getProfile(); // Replace with api.getProjects() if available
        // You may need to adjust the response structure below
        setProjects({
          projects: userProjects.projects || [],
          templates: userProjects.templates || [],
          snippets: userProjects.snippets || [],
        });
      } catch (err) {
        setError('Failed to load data.');
        setProjects({ projects: [], templates: [], snippets: [] });
      }
      setLoading(false);
    };
    fetchData();
  }, []);

  const getLanguageColor = (language) => {
    const colors = {
      'JavaScript': '#f7df1e',
      'Python': '#3776ab',
      'Java': '#ed8b00',
      'C++': '#00599c',
      'HTML': '#e34f26',
      'CSS': '#1572b6'
    };
    return colors[language] || '#6b7280';
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'active': return 'status-active';
      case 'completed': return 'status-completed';
      case 'in-progress': return 'status-progress';
      default: return '';
    }
  };

  const runCode = () => {
    console.log('Running code...');
    // Here you would implement code execution logic
    alert('Code execution feature coming soon!');
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
                  <form onSubmit={e => {e.preventDefault(); setShowProjectModal(false);}}>
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
        <div className="error-message">{error}</div>
      ) : activeTab === 'editor' ? (
        <div className="code-editor-container">
          <div className="editor-toolbar">
            <div className="editor-info">
              <span className="file-name">main.js</span>
              <span className="language-badge" style={{ backgroundColor: getLanguageColor('JavaScript') }}>
                JavaScript
              </span>
            </div>
            <div className="editor-actions">
              <button className="editor-btn" onClick={runCode}>
                <Play className="icon" />
                Run
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
              </div>
              <div className="output-content">
                <div className="output-line">Ready to run your code...</div>
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