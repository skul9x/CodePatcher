import React, { useState } from 'react';
import './App.css';
import PatcherTab from './components/PatcherTab';
import GitHubTab from './components/GitHubTab';
import { Cpu, Github, FolderOpen } from 'lucide-react';
import { SelectProjectDir } from '../wailsjs/go/main/App';

function App() {
  const [activeTab, setActiveTab] = useState<'patcher' | 'github'>('patcher');
  const [projectDir, setProjectDir] = useState('');

  const handleSelectFolder = async () => {
    try {
      const dir = await SelectProjectDir();
      if (dir) setProjectDir(dir);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div id="App">
      <header className="app-header">
        <div className="brand">
          <Cpu size={16} color="#0e639c" />
          <span>CODE PATCHER PRO</span>
        </div>
        
        <div className="project-selector">
          <FolderOpen size={14} className="icon-muted" />
          <span className="current-path" title={projectDir}>
            {projectDir || 'Chưa chọn thư mục dự án'}
          </span>
          <button className="btn-browse" onClick={handleSelectFolder}>
            Chọn thư mục...
          </button>
        </div>

        <nav className="tab-nav">
          <button 
            className={`tab-btn ${activeTab === 'patcher' ? 'active' : ''}`}
            onClick={() => setActiveTab('patcher')}
          >
            <Cpu size={14} /> Trình Vá Mã
          </button>
          <button 
            className={`tab-btn ${activeTab === 'github' ? 'active' : ''}`}
            onClick={() => setActiveTab('github')}
          >
            <Github size={14} /> Đồng Bộ GitHub
          </button>
        </nav>
        <div style={{ width: 120 }}></div> {/* Spacer */}
      </header>

      <main className="main-content">
        {activeTab === 'patcher' && <PatcherTab projectDir={projectDir} />}
        {activeTab === 'github' && <GitHubTab projectDir={projectDir} />}
      </main>
    </div>
  );
}

export default App;
