package services

import (
	"regexp"
	"strings"
)

// PatchEntry represents a single file change extracted from the patch text.
type PatchEntry struct {
	Path    string `json:"path"`
	Content string `json:"content"`
}

// patchRegex matches markdown code blocks: ```[lang]\n[content]\n```
// (?s) flag allows . to match newlines (equivalent to re.DOTALL in Python)
var patchRegex = regexp.MustCompile("(?s)```[^\n]*\n(.*?)\n```")

// ParsePatch extracts file paths and their updated content from the provided text.
func ParsePatch(text string) []PatchEntry {
	var entries []PatchEntry
	matches := patchRegex.FindAllStringSubmatch(text, -1)

	for _, match := range matches {
		if len(match) < 2 {
			continue
		}
		
		// The captured group (1) is the content inside the backticks
		fullBlock := match[1]
		trimmedBlock := strings.TrimSpace(fullBlock)
		
		// Split by first newline to find the header line (e.g., "# path/to/file")
		lines := strings.SplitN(trimmedBlock, "\n", 2)
		if len(lines) == 0 {
			continue
		}

		firstLine := strings.TrimSpace(lines[0])
		if strings.HasPrefix(firstLine, "#") {
			filePath := strings.TrimSpace(strings.TrimPrefix(firstLine, "#"))
			// Normalize to forward slashes for cross-platform consistency
			filePath = strings.ReplaceAll(filePath, "\\", "/")
			
			content := ""
			if len(lines) > 1 {
				// We want to keep the content as is, just stripping the header line and any leading newlines
				content = lines[1]
			}
			
			entries = append(entries, PatchEntry{
				Path:    filePath,
				Content: content,
			})
		}
	}
	return entries
}
