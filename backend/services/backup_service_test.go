package services

import (
	"os"
	"path/filepath"
	"testing"
)

func TestBackupService(t *testing.T) {
	// Setup temporary project directory
	projectDir, _ := os.MkdirTemp("", "project_src")
	defer os.RemoveAll(projectDir)

	// Create dummy file
	fileName := "test.txt"
	filePath := filepath.Join(projectDir, fileName)
	os.WriteFile(filePath, []byte("original content"), 0644)

	service := NewBackupService()
	
	// Override backup root for testing to avoid polluting system
	testBackupRoot, _ := os.MkdirTemp("", "backups_test")
	defer os.RemoveAll(testBackupRoot)
	service.customRootDir = testBackupRoot

	// 1. Create Backup
	batchID, err := service.CreateBackupBatch(projectDir, []string{fileName})
	if err != nil {
		t.Fatalf("Failed to create backup: %v", err)
	}

	manifestPath := filepath.Join(testBackupRoot, batchID, "manifest.json")
	if _, err := os.Stat(manifestPath); os.IsNotExist(err) {
		t.Errorf("Manifest file not created at %s", manifestPath)
	}

	// 2. Modify file to simulate "patching"
	os.WriteFile(filePath, []byte("patched content"), 0644)

	// 3. Rollback
	err = service.RollbackBatch(batchID)
	if err != nil {
		t.Fatalf("Rollback failed: %v", err)
	}

	content, _ := os.ReadFile(filePath)
	if string(content) != "original content" {
		t.Errorf("Rollback failed to restore content. Got: %s", string(content))
	}

	// 4. History
	history, err := service.GetHistory()
	if err != nil {
		t.Fatalf("GetHistory failed: %v", err)
	}
	if len(history) == 0 {
		t.Error("History should not be empty")
	}
	if !history[0].RolledBack {
		t.Error("Manifest should be updated to RolledBack: true")
	}
}
