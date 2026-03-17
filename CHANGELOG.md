# Changelog

## [2026-03-17]
### Added
- Project initialization with Wails v2 (React-TS template).
- Backend structure with services, models, and utils.
- Path utility service with `IsSafePath` for security.
- Parser service using regex to extract code blocks from AI text.
- Backup engine with manifest-based backup/rollback/history.
- Git service integration for pull, push, and branch management.
- Crypto utility for GitHub token encryption (Parity with original Python version).
- Dark Mode base UI layout in React.

### Fixed
- Go version incompatibility in `go.mod` (downgraded to 1.22.2).
- Security logic for absolute path join in `IsSafePath`.

### Progress
- Phase 01: Setup (100%)
- Phase 02: Core Domain (100%)
- Phase 03: Backup/Rollback (100%)
- Phase 04: Git Service (100%)
- Overall: 4/8 phases completed (50%).
