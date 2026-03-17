package services

import (
	"fmt"
	"os/exec"
	"strings"
)

// GitService handles interactions with the Git CLI.
type GitService struct{}

func NewGitService() *GitService {
	return &GitService{}
}

// GetCurrentBranch returns the name of the currently checked out branch.
func (s *GitService) GetCurrentBranch(projectDir string) (string, error) {
	cmd := exec.Command("git", "rev-parse", "--abbrev-ref", "HEAD")
	cmd.Dir = projectDir
	output, err := cmd.CombinedOutput()
	if err != nil {
		return "", fmt.Errorf("failed to get current branch: %s", string(output))
	}
	return strings.TrimSpace(string(output)), nil
}

// GetBranches returns a list of all local and remote branches.
func (s *GitService) GetBranches(projectDir string) ([]string, error) {
	cmd := exec.Command("git", "branch", "-a")
	cmd.Dir = projectDir
	output, err := cmd.CombinedOutput()
	if err != nil {
		return nil, fmt.Errorf("failed to list branches: %s", string(output))
	}

	lines := strings.Split(string(output), "\n")
	var branches []string
	for _, line := range lines {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		// Remove the active branch marker '*'
		line = strings.TrimPrefix(line, "*")
		line = strings.TrimSpace(line)
		
		// Skip duplicates (especially from -a which shows remotes)
		isDup := false
		for _, b := range branches {
			if b == line {
				isDup = true
				break
			}
		}
		if !isDup {
			branches = append(branches, line)
		}
	}
	return branches, nil
}

// CheckoutBranch switches to the specified branch.
func (s *GitService) CheckoutBranch(projectDir, branch string) error {
	cmd := exec.Command("git", "checkout", branch)
	cmd.Dir = projectDir
	output, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("failed to checkout branch %s: %s", branch, string(output))
	}
	return nil
}

// PullCurrent pulls updates from the remote for the current branch.
func (s *GitService) PullCurrent(projectDir string) (string, error) {
	// We use --rebase to keep history clean, matching common developer practices
	cmd := exec.Command("git", "pull", "--rebase")
	cmd.Dir = projectDir
	output, err := cmd.CombinedOutput()
	if err != nil {
		return string(output), fmt.Errorf("failed to pull updates: %w", err)
	}
	return string(output), nil
}

// CommitAndPush stages changes, commits them with a message, and pushes to remote.
func (s *GitService) CommitAndPush(projectDir, message, token string) (string, error) {
	// 1. Add all changes
	addCmd := exec.Command("git", "add", ".")
	addCmd.Dir = projectDir
	if out, err := addCmd.CombinedOutput(); err != nil {
		return string(out), fmt.Errorf("failed to add files: %w", err)
	}

	// 2. Commit
	commitCmd := exec.Command("git", "commit", "-m", message)
	commitCmd.Dir = projectDir
	if out, err := commitCmd.CombinedOutput(); err != nil {
		// If there's nothing to commit, it's not strictly an error for the user
		if strings.Contains(string(out), "nothing to commit") {
			return string(out), nil
		}
		return string(out), fmt.Errorf("failed to commit: %w", err)
	}

	// 3. Push
	// Note: Authentication typically handled via Git Credential Manager or SSH.
	// We don't explicitly pass the token to the CLI for security reasons,
	// but if the user provided it, we could potentially use it in the remote URL (not recommended).
	// For now, we assume the environment is authenticated.
	pushCmd := exec.Command("git", "push")
	pushCmd.Dir = projectDir
	out, err := pushCmd.CombinedOutput()
	if err != nil {
		return string(out), fmt.Errorf("failed to push: %w", err)
	}

	return string(out), nil
}
