package services

import (
	"CodePatcher/backend/models"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"time"
)

const BackupDirName = ".patch_backups"

// BackupService handles the backup and rollback of patched files.
type BackupService struct {
	customRootDir string
}

func NewBackupService() *BackupService {
	return &BackupService{}
}

// getBackupRootDir returns the absolute path to the global backup directory.
func (s *BackupService) getBackupRootDir() (string, error) {
	if s.customRootDir != "" {
		return s.customRootDir, nil
	}
	exePath, err := os.Executable()
	if err != nil {
		// Fallback to current working directory if executable path cannot be found
		return filepath.Join(".", BackupDirName), nil
	}
	return filepath.Join(filepath.Dir(exePath), BackupDirName), nil
}

// CreateBackupBatch creates a timestamped backup of the specified files from the project directory.
func (s *BackupService) CreateBackupBatch(projectDir string, relFilePaths []string) (string, error) {
	batchID := time.Now().Format("2006-01-02_150405")
	rootDir, err := s.getBackupRootDir()
	if err != nil {
		return "", err
	}

	batchDir := filepath.Join(rootDir, batchID)
	if err := os.MkdirAll(batchDir, 0755); err != nil {
		return "", fmt.Errorf("failed to create backup batch directory: %w", err)
	}

	backedUpFiles := []string{}
	for _, relPath := range relFilePaths {
		src := filepath.Join(projectDir, relPath)
		dst := filepath.Join(batchDir, relPath)

		// Only backup if file exists. If it doesn't exist, it's a new file (no backup needed).
		if _, err := os.Stat(src); err == nil {
			if err := os.MkdirAll(filepath.Dir(dst), 0755); err != nil {
				return "", fmt.Errorf("failed to create directory for backup file %s: %w", relPath, err)
			}
			if err := copyFile(src, dst); err != nil {
				return "", fmt.Errorf("failed to copy file %s for backup: %w", relPath, err)
			}
		}
		backedUpFiles = append(backedUpFiles, relPath)
	}

	// Create manifest
	manifest := models.Manifest{
		ProjectDir:   projectDir,
		PatchedFiles: backedUpFiles,
		RolledBack:   false,
	}

	manifestPath := filepath.Join(batchDir, "manifest.json")
	mFile, err := os.Create(manifestPath)
	if err != nil {
		return "", fmt.Errorf("failed to create manifest file: %w", err)
	}
	defer mFile.Close()

	encoder := json.NewEncoder(mFile)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(manifest); err != nil {
		return "", fmt.Errorf("failed to encode manifest: %w", err)
	}

	return batchID, nil
}

// RollbackBatch reverts changes from a specific backup batch.
func (s *BackupService) RollbackBatch(batchID string) error {
	rootDir, err := s.getBackupRootDir()
	if err != nil {
		return err
	}

	batchDir := filepath.Join(rootDir, batchID)
	manifestPath := filepath.Join(batchDir, "manifest.json")
	
	mFile, err := os.Open(manifestPath)
	if err != nil {
		return fmt.Errorf("failed to open manifest: %w", err)
	}
	defer mFile.Close()

	var manifest models.Manifest
	if err := json.NewDecoder(mFile).Decode(&manifest); err != nil {
		return fmt.Errorf("failed to decode manifest: %w", err)
	}

	if manifest.RolledBack {
		return fmt.Errorf("this batch has already been rolled back")
	}

	for _, relPath := range manifest.PatchedFiles {
		src := filepath.Join(batchDir, relPath)
		dst := filepath.Join(manifest.ProjectDir, relPath)

		if _, err := os.Stat(src); err == nil {
			// Restore from backup
			if err := os.MkdirAll(filepath.Dir(dst), 0755); err != nil {
				return fmt.Errorf("failed to create directory for restore: %w", err)
			}
			if err := copyFile(src, dst); err != nil {
				return fmt.Errorf("failed to restore file %s: %w", relPath, err)
			}
		} else {
			// If not in backup, maybe it was a new file? Try removing it from project.
			if _, err := os.Stat(dst); err == nil {
				if err := os.Remove(dst); err != nil {
					// We log but continue
					fmt.Printf("Warning: failed to remove newly created file during rollback: %s\n", dst)
				}
			}
		}
	}

	// Update manifest
	manifest.RolledBack = true
	mFileUpdate, err := os.Create(manifestPath)
	if err != nil {
		return fmt.Errorf("failed to update manifest: %w", err)
	}
	defer mFileUpdate.Close()
	encoder := json.NewEncoder(mFileUpdate)
	encoder.SetIndent("", "  ")
	return encoder.Encode(manifest)
}

// GetHistory returns the list of all backup batches found in the root backup directory.
func (s *BackupService) GetHistory() ([]models.HistoryItem, error) {
	rootDir, err := s.getBackupRootDir()
	if err != nil {
		return nil, err
	}

	if _, err := os.Stat(rootDir); os.IsNotExist(err) {
		return []models.HistoryItem{}, nil
	}

	entries, err := os.ReadDir(rootDir)
	if err != nil {
		return nil, fmt.Errorf("failed to read backup root: %w", err)
	}

	history := []models.HistoryItem{}
	for _, entry := range entries {
		if !entry.IsDir() {
			continue
		}

		manifestPath := filepath.Join(rootDir, entry.Name(), "manifest.json")
		mFile, err := os.Open(manifestPath)
		if err != nil {
			continue
		}

		var m models.Manifest
		err = json.NewDecoder(mFile).Decode(&m)
		mFile.Close()
		if err != nil {
			continue
		}

		history = append(history, models.HistoryItem{
			BatchID:      entry.Name(),
			ProjectName:  filepath.Base(m.ProjectDir),
			ProjectDir:   m.ProjectDir,
			PatchedFiles: m.PatchedFiles,
			RolledBack:   m.RolledBack,
		})
	}

	// Sort newest first
	sort.Slice(history, func(i, j int) bool {
		return history[i].BatchID > history[j].BatchID
	})

	return history, nil
}

// ClearHistory deletes all backup batches.
func (s *BackupService) ClearHistory() error {
	rootDir, err := s.getBackupRootDir()
	if err != nil {
		return err
	}
	return os.RemoveAll(rootDir)
}

// helper to copy file contents
func copyFile(src, dst string) error {
	source, err := os.Open(src)
	if err != nil {
		return err
	}
	defer source.Close()

	destination, err := os.Create(dst)
	if err != nil {
		return err
	}
	defer destination.Close()

	_, err = io.Copy(destination, source)
	return err
}
