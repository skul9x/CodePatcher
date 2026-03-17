package main

import (
	"CodePatcher/backend/models"
	"CodePatcher/backend/services"
	"context"
	"fmt"
	"os"
	"path/filepath"

	"github.com/wailsapp/wails/v2/pkg/runtime"
)

// App struct
type App struct {
	ctx           context.Context
	backupService *services.BackupService
	gitService    *services.GitService
}

// NewApp tạo một instance của ứng dụng App
func NewApp() *App {
	return &App{
		backupService: services.NewBackupService(),
		gitService:    services.NewGitService(),
	}
}

// startup được gọi khi ứng dụng khởi chạy.
func (a *App) startup(ctx context.Context) {
	a.ctx = ctx
}

// SelectProjectDir mở hộp thoại chọn thư mục
func (a *App) SelectProjectDir() (string, error) {
	result, err := runtime.OpenDirectoryDialog(a.ctx, runtime.OpenDialogOptions{
		Title: "Chọn Thư Mục Dự Án",
	})
	if err != nil {
		return "", err
	}
	return result, nil
}

// ParsePatchExtract trích xuất các thay đổi từ văn bản patch
func (a *App) ParsePatchExtract(text string) []services.PatchEntry {
	return services.ParsePatch(text)
}

// ApplyPatch thực hiện quy trình áp dụng bản vá: backup sau đó ghi đè
func (a *App) ApplyPatch(projectDir string, patchText string) (string, error) {
	if projectDir == "" {
		return "", fmt.Errorf("chưa chọn thư mục dự án")
	}

	entries := services.ParsePatch(patchText)
	if len(entries) == 0 {
		return "", fmt.Errorf("không tìm thấy khối mã (code block) hợp lệ trong văn bản")
	}

	// 1. Chuẩn bị danh sách file để backup
	var filesToBackup []string
	for _, entry := range entries {
		filesToBackup = append(filesToBackup, entry.Path)
	}

	// 2. Tạo bản sao lưu (Backup)
	batchID, err := a.backupService.CreateBackupBatch(projectDir, filesToBackup)
	if err != nil {
		return "", fmt.Errorf("sao lưu thất bại: %w", err)
	}

	// 3. Áp dụng thay đổi (ghi đè file)
	for _, entry := range entries {
		fullPath := filepath.Join(projectDir, entry.Path)
		
		// Đảm bảo thư mục cha tồn tại (cho các file mới)
		if err := os.MkdirAll(filepath.Dir(fullPath), 0755); err != nil {
			return batchID, fmt.Errorf("không thể tạo thư mục cho %s: %w", entry.Path, err)
		}

		if err := os.WriteFile(fullPath, []byte(entry.Content), 0644); err != nil {
			return batchID, fmt.Errorf("không thể ghi file %s: %w", entry.Path, err)
		}
	}

	return batchID, nil
}

// GetHistory lấy lịch sử sao lưu
func (a *App) GetHistory() ([]models.HistoryItem, error) {
	return a.backupService.GetHistory()
}

// Rollback hoàn tác một đợt thay đổi cụ thể
func (a *App) Rollback(batchID string) error {
	return a.backupService.RollbackBatch(batchID)
}

// GitGetStatus lấy thông tin branch và trạng thái hiện tại
func (a *App) GitGetStatus(projectDir string) (map[string]interface{}, error) {
	branch, err := a.gitService.GetCurrentBranch(projectDir)
	if err != nil {
		return nil, err
	}
	
	branches, _ := a.gitService.GetBranches(projectDir)
	
	return map[string]interface{}{
		"currentBranch": branch,
		"branches":      branches,
	}, nil
}

// GitPull thực hiện git pull
func (a *App) GitPull(projectDir string) (string, error) {
	return a.gitService.PullCurrent(projectDir)
}

// GitPush thực hiện git commit và push
func (a *App) GitPush(projectDir, message, token string) (string, error) {
	return a.gitService.CommitAndPush(projectDir, message, token)
}
