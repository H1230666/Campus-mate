# Changelog

格式参考 Keep a Changelog，版本号遵循语义化版本。

## [v0.1.0-alpha] - 2026-11-07

中期 Alpha 版本：完成用户模块与工程骨架，后端统一为 `backend/` 结构。

### Added
- 后端结构统一：`backend/app/`（main / routers / schemas / services / repositories）+ `backend/tests`
- 用户模块：#1 用户模型与字段校验、#2 JWT 登录态鉴权、#3 小程序登录页
- 工程规范：#4 CONTRIBUTING、Issue/PR 模板、`.env.example`、分支保护
- 质量保障：`backend/pyproject.toml`（ruff + pytest 配置）、GitHub Actions CI
- 文档：`docs/SRS.md`、`docs/meetings/`、`CHANGELOG.md`

### Changed
- 移除根目录遗留的 `api/` `core/` `models/` `schemas/` `tests/` `main.py`，统一收敛到 `backend/`
- 小程序目录统一为 `frontend/`

### Known Limitations
- 数据库仍为内存模拟，未接入 MySQL
- 密码尚未哈希存储
- 全局异常处理（#12）与邀约模块（#11）仍在开发
