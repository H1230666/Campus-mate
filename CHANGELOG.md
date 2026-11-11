# Changelog

## [v0.1.0-alpha] - 2026-11-07

中期 Alpha：完成用户模块与工程骨架，后端统一为 `backend/` 结构。

### Added
- 工程规范：`CONTRIBUTING.md`、`.github/ISSUE_TEMPLATE/`、`.github/pull_request_template.md`、`.env.example`
- 分支保护：main 需 PR + 1 人 Approve + CI 通过 + 禁强推
- CI：`.github/workflows/ci.yml`（ruff / pytest / compileall + 小程序 JS 语法检查）
- 文档：`docs/SRS.md`、`docs/meetings/`、`docs/branch-protection.md`、`CHANGELOG.md`
- 用户模块：#1 模型与校验、#2 JWT 鉴权、#3 小程序登录页

### Changed
- 移除根目录遗留的 `api/` `core/` `models/` `schemas/` `tests/` `main.py`，收敛到 `backend/`
- 小程序目录统一为 `frontend/`

### Known Limitations
- 数据库仍为内存模拟，未接入 MySQL
- 密码尚未哈希存储
- 全局异常处理（#12）与邀约模块（#11）仍在开发
