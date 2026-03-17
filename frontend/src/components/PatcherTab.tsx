import React, { useState, useEffect } from 'react';
import { Panel, Group as PanelGroup, Separator as PanelResizeHandle } from 'react-resizable-panels';
import { Clipboard, Trash2, Play, History, FileText, CheckCircle2, RotateCcw, AlertCircle } from 'lucide-react';
import { ParsePatchExtract, ApplyPatch, GetHistory, Rollback } from '../../wailsjs/go/main/App';
import { services, models } from '../../wailsjs/go/models';

interface PatcherTabProps {
    projectDir: string;
}

const PatcherTab: React.FC<PatcherTabProps> = ({ projectDir }) => {
    const [patchText, setPatchText] = useState('');
    const [history, setHistory] = useState<models.HistoryItem[]>([]);
    const [previewEntries, setPreviewEntries] = useState<services.PatchEntry[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const fetchHistory = async () => {
        try {
            const data = await GetHistory();
            setHistory(data);
        } catch (err) {
            console.error('Failed to fetch history', err);
        }
    };

    useEffect(() => {
        fetchHistory();
    }, []);

    // Cập nhật xem trước khi văn bản thay đổi
    useEffect(() => {
        const updatePreview = async () => {
            if (!patchText.trim()) {
                setPreviewEntries([]);
                return;
            }
            try {
                const entries = await ParsePatchExtract(patchText);
                setPreviewEntries(entries);
            } catch (err) {
                console.error('Parse error', err);
            }
        };

        const timer = setTimeout(updatePreview, 500); // Debounce
        return () => clearTimeout(timer);
    }, [patchText]);

    const handlePaste = async () => {
        try {
            const text = await navigator.clipboard.readText();
            setPatchText(text);
        } catch (err) {
            console.error('Không thể đọc clipboard', err);
        }
    };

    const handleClear = () => {
        setPatchText('');
        setError(null);
    };

    const handleApply = async () => {
        if (!projectDir) {
            setError('Vui lòng chọn thư mục dự án trước.');
            return;
        }
        if (!patchText.trim() || previewEntries.length === 0) {
            setError('Không tìm thấy khối mã hợp lệ để áp dụng.');
            return;
        }

        setIsLoading(true);
        setError(null);
        try {
            await ApplyPatch(projectDir, patchText);
            setPatchText('');
            await fetchHistory();
        } catch (err: any) {
            setError(err.toString());
        } finally {
            setIsLoading(false);
        }
    };

    const handleRollback = async (batchID: string) => {
        if (!window.confirm("Bạn có chắc chắn muốn hoàn tác (Rollback) đợt thay đổi này?")) return;
        try {
            await Rollback(batchID);
            await fetchHistory();
        } catch (err: any) {
            setError("Hoàn tác thất bại: " + err.toString());
        }
    };

    return (
        <div className="patcher-container">
            <PanelGroup orientation="horizontal">
                {/* Bên trái: Biên tập & Hành động */}
                <Panel defaultSize={70} minSize={30}>
                    <div className="editor-panel">
                        <div className="panel-header">
                            <span className="panel-title">Nội Dung Bản Vá AI</span>
                            <div className="header-actions">
                                <button onClick={handlePaste} title="Dán từ Clipboard">
                                    <Clipboard size={14} /> Dán
                                </button>
                                <button onClick={handleClear} title="Xóa tất cả">
                                    <Trash2 size={14} /> Xóa
                                </button>
                            </div>
                        </div>
                        <textarea
                            className="patch-textarea"
                            placeholder="Dán các đoạn mã AI tại đây...&#10;Ví dụ:&#10;```go&#10;# path/to/file.go&#10;package main&#10;...&#10;```"
                            value={patchText}
                            onChange={(e) => setPatchText(e.target.value)}
                            spellCheck={false}
                        />
                        
                        {error && (
                            <div className="error-banner">
                                <AlertCircle size={14} />
                                <span>{error}</span>
                            </div>
                        )}

                        <div className="action-bar">
                            <button 
                                className="btn-primary" 
                                onClick={handleApply}
                                disabled={isLoading || !projectDir || previewEntries.length === 0}
                            >
                                <Play size={16} /> {isLoading ? 'Đang thực hiện...' : 'Áp Dụng Bản Vá'}
                            </button>
                        </div>
                    </div>
                </Panel>

                <PanelResizeHandle className="resizer" />

                {/* Bên phải: Xem trước & Lịch sử */}
                <Panel defaultSize={30} minSize={20}>
                    <PanelGroup orientation="vertical">
                        <Panel defaultSize={50} minSize={20}>
                            <div className="preview-panel">
                                <div className="panel-header">
                                    <span className="panel-title">Tệp Thay Đổi ({previewEntries.length})</span>
                                </div>
                                <div className="tree-view">
                                    {previewEntries.length === 0 ? (
                                        <div className="tree-empty">Chưa phát hiện thay đổi nào</div>
                                    ) : (
                                        previewEntries.map((entry, i) => (
                                            <div className="tree-item changed" key={i} title={entry.path}>
                                                <FileText size={14} className="icon-file" />
                                                <span className="file-path">{entry.path}</span>
                                                <CheckCircle2 size={12} className="icon-status" />
                                            </div>
                                        ))
                                    )}
                                </div>
                            </div>
                        </Panel>
                        
                        <PanelResizeHandle className="resizer-v" />
                        
                        <Panel defaultSize={50} minSize={20}>
                            <div className="history-panel">
                                <div className="panel-header">
                                    <span className="panel-title">Lịch Sử Gần Đây</span>
                                    <History size={14} className="icon-header" />
                                </div>
                                <div className="history-list">
                                    {history.length === 0 ? (
                                        <div className="tree-empty">Chưa có lịch sử</div>
                                    ) : (
                                        history.map((item) => (
                                            <div className={`history-item ${item.rolled_back ? 'rolled-back' : ''}`} key={item.batch_id}>
                                                <div className="history-info">
                                                    <span className="history-date">{item.batch_id}</span>
                                                    <span className="history-desc">
                                                        {item.patched_files.length} tệp trong {item.project_name}
                                                    </span>
                                                </div>
                                                <button 
                                                    className="btn-rollback" 
                                                    title={item.rolled_back ? "Đã được hoàn tác" : "Hoàn tác đợt này"}
                                                    disabled={item.rolled_back}
                                                    onClick={() => handleRollback(item.batch_id)}
                                                >
                                                    <RotateCcw size={12} />
                                                </button>
                                            </div>
                                        ))
                                    )}
                                </div>
                            </div>
                        </Panel>
                    </PanelGroup>
                </Panel>
            </PanelGroup>
        </div>
    );
};

export default PatcherTab;
