package utils

import (
	"os"
	"testing"
)

func TestIsSafePath(t *testing.T) {
	tempDir, err := os.MkdirTemp("", "codepatcher_test")
	if err != nil {
		t.Fatal(err)
	}
	defer os.RemoveAll(tempDir)

	tests := []struct {
		name    string
		base    string
		rel     string
		want    bool
		wantErr bool
	}{
		{"Safe path", tempDir, "app/main.go", true, false},
		{"Safe path deep", tempDir, "a/b/c/d.txt", true, false},
		{"Exactly base", tempDir, ".", true, false},
		{"Traversal attempt", tempDir, "../secret.txt", false, false},
		{"Traversal attempt deep", tempDir, "app/../../secret.txt", false, false},
		{"Sibling directory", tempDir, "../other_dir/file.txt", false, false},
		{"Absolute path outside", "/tmp", "/etc/passwd", false, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			got, err := IsSafePath(tt.base, tt.rel)
			if (err != nil) != tt.wantErr {
				t.Errorf("IsSafePath() error = %v, wantErr %v", err, tt.wantErr)
				return
			}
			if got != tt.want {
				// On some systems tempDir might have symlinks, but filepath.Abs should handle it
				t.Errorf("IsSafePath(%q, %q) = %v, want %v", tt.base, tt.rel, got, tt.want)
			}
		})
	}
}
