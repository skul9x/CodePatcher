package utils

import (
	"os"
	"path/filepath"
	"strings"
)

// IsSafePath checks if the given relative path, when joined with baseDir,
// stays within the boundaries of baseDir to prevent directory traversal attacks.
func IsSafePath(baseDir, relPath string) (bool, error) {
	if baseDir == "" {
		return false, nil
	}

	// Clean and get absolute path of base directory
	absBase, err := filepath.Abs(filepath.Clean(baseDir))
	if err != nil {
		return false, err
	}

	// Handle absolute relPath like Python's os.path.join:
	// If relPath is absolute, it becomes the full path.
	var fullPath string
	if filepath.IsAbs(relPath) {
		fullPath = relPath
	} else {
		fullPath = filepath.Join(absBase, relPath)
	}

	absFull, err := filepath.Abs(fullPath)
	if err != nil {
		return false, err
	}

	// Double check: the cleaned absolute path must have the base directory as a prefix
	// We use a trailing separator to avoid cases like "/base" matching "/basement"
	baseWithSep := absBase
	if !strings.HasSuffix(baseWithSep, string(os.PathSeparator)) {
		baseWithSep += string(os.PathSeparator)
	}

	// Special case: if base is exactly same as full path (no rel path part)
	if absBase == absFull {
		return true, nil
	}

	return strings.HasPrefix(absFull, baseWithSep), nil
}
