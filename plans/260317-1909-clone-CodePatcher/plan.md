# Plan: Clone Project

Source Project: `/home/skul9x/Desktop/Test_code/CodePatcher-main`
Target Project: `/home/skul9x/Desktop/Test_code/CodePatcher-Go`

Backend Target: Go (qua Wails v2)
Frontend Target: [Chờ User Xác Nhận - Đề xuất React/Vite, hoặcc Svelte]

---

## Overview

Viết lại dự án (Direct Rewrite) phần mềm **TCO Patch Applier** từ Python (PySide6) sang Go (Wails v2). 
Giữ nguyên logic nghiệp vụ (Code patching an toàn, backup, rollback, git sync) và nâng cấp giao diện bằng Web Technology. Hỗ trợ cross-platform cho Windows và Ubuntu 24.

---

## Project Size

**Small** (< 5k LOC)

---

## Estimated Effort

Estimated LOC: ~1500 LOC
Estimated Phases: 8 phases
Estimated Sessions: 2-3 sessions

---

## Phases

| Phase | Name | Status |
|------|------|------|
| 01 | Setup (Wails project init) | ✅ Complete | 100% |
| 02 | Core Domain (Regex, File IO) | ✅ Complete | 100% |
| 03 | Backup/Rollback Engine | ✅ Complete | 100% |
| 04 | Git Service Integration | ✅ Complete | 100% |
| 05 | Frontend Layout & Patcher Tab | ✅ Complete | 100% |
| 06 | Frontend GitHub Tab | ✅ Complete | 100% |
| 07 | Integration & API Bindings | ✅ Complete | 100% |
| 08 | Build & Deployment (Win/Ubuntu) | ✅ Complete | 100% |

---

## Quick Commands

Start phase

`/code phase-01-setup.md`

Next phase

`/next`
