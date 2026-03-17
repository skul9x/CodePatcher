import React, { useState, useEffect } from 'react';
import { Github, Settings, CloudUpload, CloudDownload, RefreshCw, Key, GitBranch as BranchIcon } from 'lucide-react';
import { GitGetStatus, GitPull, GitPush } from '../../wailsjs/go/main/App';

interface GitHubTabProps {
    projectDir: string;
}

const GitHubTab: React.FC<GitHubTabProps> = ({ projectDir }) => {
    const [token, setToken] = useState('');
    const [branch, setBranch] = useState('main');
    const [status, setStatus] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [logs, setLogs] = useState<{time: string, msg: string}[]>([]);

    const addLog = (msg: string) => {
        const time = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
        setLogs(prev => [{ time, msg }, ...prev].slice(0, 50));
    };

    const fetchStatus = async () => {
        if (!projectDir) return;
        try {
            const data = await GitGetStatus(projectDir);
            setStatus(data);
            if (data.currentBranch) setBranch(data.currentBranch);
            addLog(`Đã cập nhật trạng thái: ${data.currentBranch}`);
        } catch (err) {
            console.error(err);
        }
    };

    useEffect(() => {
        fetchStatus();
    }, [projectDir]);

    const handlePull = async () => {
        if (!projectDir) return;
        setIsLoading(true);
        addLog("Đang thực hiện Git Pull...");
        try {
            const out = await GitPull(projectDir);
            addLog("Pull Thành Công: " + out);
        } catch (err: any) {
            addLog("Pull Lỗi: " + err.toString());
        } finally {
            setIsLoading(false);
        }
    };

    const handlePush = async () => {
        if (!projectDir) return;
        const msg = prompt("Nhập thông điệp commit:", "Áp dụng bản vá via CodePatcher");
        if (!msg) return;

        setIsLoading(true);
        addLog("Đang thực hiện Git Push (Commit & Push)...");
        try {
            const out = await GitPush(projectDir, msg, token);
            addLog("Push Thành Công: " + out);
        } catch (err: any) {
            addLog("Push Lỗi: " + err.toString());
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="github-container">
            {!projectDir ? (
                <div style={{ padding: 40, textAlign: 'center', color: '#858585' }}>
                    <Settings size={48} strokeWidth={1} style={{ marginBottom: 16 }} />
                    <h2>Cần chọn thư mục dự án</h2>
                    <p>Chọn một thư mục dự án ở thanh tiêu đề để sử dụng các tính năng Git.</p>
                </div>
            ) : (
                <div className="github-grid">
                    {/* Cấu hình Section */}
                    <div className="settings-card">
                        <div className="card-header">
                            <Settings size={14} />
                            <span>CẤU HÌNH GIT</span>
                        </div>
                        <div className="card-body">
                            <div className="form-group">
                                <label><Key size={12} /> GitHub Personal Access Token (Tùy chọn)</label>
                                <input 
                                    type="password" 
                                    value={token} 
                                    onChange={(e) => setToken(e.target.value)}
                                    placeholder="ghp_xxxxxxxxxxxx"
                                />
                                <span className="hint">Dùng cho xác thực repo riêng tư nếu chưa được lưu trong hệ thống.</span>
                            </div>

                            <div className="form-group">
                                <label><BranchIcon size={12} /> Nhánh (Branch) Hiện Tại</label>
                                <div className="input-with-button">
                                    <input 
                                        type="text" 
                                        value={branch} 
                                        readOnly
                                    />
                                    <button className="btn-icon" title="Cập nhật trạng thái" onClick={fetchStatus}>
                                        <RefreshCw size={12} />
                                    </button>
                                </div>
                            </div>
                            
                            <button className="btn-primary w-full mt-lg" onClick={fetchStatus}>
                                Cập Nhật Trạng Thái Git
                            </button>
                        </div>
                    </div>

                    {/* Trạng thái & Hành động Section */}
                    <div className="actions-card">
                        <div className="card-header">
                            <Github size={14} />
                            <span>HÀNH ĐỘNG NHANH</span>
                        </div>
                        <div className="card-body">
                            <div className={`status-indicator ${status ? 'online' : ''}`}>
                                <div className="status-dot"></div>
                                <span>{status ? `Đang ở nhánh: ${status.currentBranch}` : 'Không phải là Repository Git?'}</span>
                            </div>
                            
                            <div className="git-buttons-grid">
                                <button className="btn-git pull" onClick={handlePull} disabled={isLoading}>
                                    <CloudDownload size={20} />
                                    <div className="btn-label">
                                        <strong>{isLoading ? 'Chờ...' : 'PULL'}</strong>
                                        <span>Đồng bộ thay đổi</span>
                                    </div>
                                </button>
                                
                                <button className="btn-git push" onClick={handlePush} disabled={isLoading}>
                                    <CloudUpload size={20} />
                                    <div className="btn-label">
                                        <strong>{isLoading ? 'Chờ...' : 'PUSH'}</strong>
                                        <span>Commit & Đẩy mã</span>
                                    </div>
                                </button>
                            </div>

                            <div className="sync-log">
                                <div className="log-header">Hoạt Động Đồng Bộ</div>
                                <div className="log-content">
                                    {logs.length === 0 ? (
                                        <div style={{ color: '#444' }}>Chưa có hoạt động nào.</div>
                                    ) : (
                                        logs.map((log, i) => (
                                            <div className="log-entry" key={i}>
                                                <span className="time">[{log.time}]</span>
                                                <span className="msg">{log.msg}</span>
                                            </div>
                                        ))
                                    )}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default GitHubTab;
