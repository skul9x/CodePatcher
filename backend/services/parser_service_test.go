package services

import (
	"strings"
	"testing"
)

func TestParsePatch(t *testing.T) {
	input := `
Đây là bản vá cho file main.go:
` + "```go" + `
# app/main.go
package main
func main() {}
` + "```" + `

Và một file khác:
` + "```python" + `
# src/utils.py
def hello():
    print("world")
` + "```" + `
`

	expected := []PatchEntry{
		{
			Path:    "app/main.go",
			Content: "package main\nfunc main() {}",
		},
		{
			Path:    "src/utils.py",
			Content: "def hello():\n    print(\"world\")",
		},
	}

	got := ParsePatch(input)

	if len(got) != len(expected) {
		t.Fatalf("Expected %d entries, got %d", len(expected), len(got))
	}

	for i := range expected {
		if got[i].Path != expected[i].Path {
			t.Errorf("[%d] Expected path %q, got %q", i, expected[i].Path, got[i].Path)
		}
		if strings.TrimSpace(got[i].Content) != strings.TrimSpace(expected[i].Content) {
			t.Errorf("[%d] Content mismatch.\nExpected:\n%q\nGot:\n%q", i, expected[i].Content, got[i].Content)
		}
	}
}

func TestParsePatchSpecialChars(t *testing.T) {
	input := "```\n# docs/README.md\n# Title\nContent with # inside\n```"
	got := ParsePatch(input)
	
	if len(got) != 1 {
		t.Fatalf("Expected 1 entry, got %d", len(got))
	}
	
	if got[0].Path != "docs/README.md" {
		t.Errorf("Path mismatch: %q", got[0].Path)
	}
	
	expectedContent := "# Title\nContent with # inside"
	if strings.TrimSpace(got[0].Content) != strings.TrimSpace(expectedContent) {
		t.Errorf("Content mismatch: %q", got[0].Content)
	}
}
