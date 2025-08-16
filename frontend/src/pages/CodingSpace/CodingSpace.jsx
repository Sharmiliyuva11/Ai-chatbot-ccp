import React, { useState } from 'react';
import { Code, Play, Save, Share, Plus, Search, FileText, Folder, Terminal } from 'lucide-react';
import './CodingSpace.css';

const CodingSpace = () => {
  const [activeTab, setActiveTab] = useState('projects');
  const [selectedProject, setSelectedProject] = useState(null);
  const [code, setCode] = useState('// Welcome to Coding Space\n// Start coding here!\n\nfunction hello() {\n  console.log("Hello, World!");\n}\n\nhello();');

  const projects = {
    projects: [
      {
        id: 1,
        name: 'React Todo App',
        description: 'A simple todo application built with React and local storage.',
        language: 'JavaScript',
        framework: 'React',
        lastModified: '2 hours ago',
        status: 'active',
        files: 3,
        lines: 245
      },
      {
        id: 2,
        name: 'Python Data Analysis',
        description: 'Data analysis project using pandas and matplotlib.',
        language: 'Python',
        framework: 'Pandas',
        lastModified: '1 day ago',
        status: 'completed',
        files: 5,
        lines: 432
      },
      {
        id: 3,
        name: 'Node.js API',
        description: 'RESTful API with Express.js and MongoDB.',
        language: 'JavaScript',
        framework: 'Node.js',
        lastModified: '3 days ago',
        status: 'in-progress',
        files: 8,
        lines: 567
      }
    ],
    templates: [
      {
        id: 4,
        name: 'React Starter',
        description: 'Basic React application template with routing.',
        language: 'JavaScript',
        framework: 'React',
        category: 'Frontend',
        difficulty: 'Beginner'
      },
      {
        id: 5,
        name: 'Express API Template',
        description: 'Node.js Express API with authentication.',
        language: 'JavaScript',
        framework: 'Express',
        category: 'Backend',
        difficulty: 'Intermediate'
      },
      {
        id: 6,
        name: 'Python Flask App',
        description: 'Flask web application with database integration.',
        language: 'Python',
        framework: 'Flask',
        category: 'Full Stack',
        difficulty: 'Intermediate'
      }
    ],
    snippets: [
      {
        id: 7,
        name: 'Array Methods',
        description: 'Common JavaScript array manipulation methods.',
        language: 'JavaScript',
        category: 'Utilities',
        code: 'const arr = [1, 2, 3, 4, 5];\n// Map, filter, reduce examples'
      },
      {
        id: 8,
        name: 'API Fetch',
        description: 'Async/await API call with error handling.',
        language: 'JavaScript',
        category: 'Network',
        code: 'async function fetchData(url) {\n  try {\n    const response = await fetch(url);\n    return await response.json();\n  } catch (error) {\n    console.error(error);\n  }\n}'
      }
    ]
  };

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
          <button className="create-project-btn">
            <Plus className="icon" />
            New Project
          </button>
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

      {activeTab === 'editor' ? (
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

      {projects[activeTab] && projects[activeTab].length === 0 && (
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