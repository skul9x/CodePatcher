package models

// Manifest represents the structure of the manifest.json file stored in each backup batch.
type Manifest struct {
	ProjectDir   string   `json:"project_dir"`
	PatchedFiles []string `json:"patched_files"`
	RolledBack   bool     `json:"rolled_back"`
}

// HistoryItem represents a single backup batch for display in the frontend.
type HistoryItem struct {
	BatchID      string   `json:"batch_id"`
	ProjectName  string   `json:"project_name"`
	ProjectDir   string   `json:"project_dir"`
	PatchedFiles []string `json:"patched_files"`
	RolledBack   bool     `json:"rolled_back"`
}
