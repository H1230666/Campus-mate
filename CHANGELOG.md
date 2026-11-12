# Changelog

## [v0.1.0-alpha] - 2026-11-07

中期 Alpha：首个可运行版本，覆盖用户模块、邀约发布/草稿、邀约广场、报名加入与状态流转、统一前后端异常处理，配套工程规范、CI 门禁与中期文档。

### Added
- **用户模块**：#1 用户实体与字段校验、#2 JWT 登录态鉴权中间件与密钥外置、#3 小程序登录授权兜底与 token 存储
- **邀约发布**：#5 发布接口与表单校验、#6 草稿暂存与恢复、#7 发布表单页与草稿恢复
- **邀约广场**：#16 分页与类型筛选、#18 详情接口、#19 广场列表与详情页、#50 状态筛选（全部 / 招募中 / 已满）与详情时间格式化
- **报名与状态流转**：#38 报名加入邀约接口、招募状态流转（招募中 / 已满）、招募人数上限控制
- **全局异常**：#36 后端统一错误码与异常拦截器（ErrorCode / BusinessException）、#37 前端全局异常处理、网络错误弹窗与兜底错误页
- **工程规范**：`CONTRIBUTING.md`、Issue / PR 模板、`.env.example`
- **CI**：`.github/workflows/ci.yml`（ruff / pytest 覆盖率 ≥40% 门禁 / compileall + 小程序 JS 语法检查）；#48 补充广场边界与非法参数测试并上传覆盖率报告
- **分支保护**：main 需 PR + 至少 1 人 Approve + CI 通过，禁强推、禁删除
- **文档**：`docs/SRS.md`、架构文档（Mermaid 架构图 / ER 图 / 7 条 ADR）、会议记录 ×2、`docs/branch-protection.md`、#49 个人工程贡献说明书

### Changed
- 目录结构收敛：删除根目录早期试点目录与旧扁平副本（`api/` `core/` `models/` `schemas/` `tests/`、根 `main.py`、早期小程序试点 `miniprogram/`），共 45 个文件、约 653 行；后端统一为 `backend/app/` 分层（router / service / repository / schemas / core），测试位于 `backend/tests/`，前端统一为 `frontend/`（#53）

### Fixed
- 修复 JWT 密钥硬编码兜底：非 dev 环境未配置 `AUTH_SECRET` 时启动即失败
- 修复密码明文存储：模型改用 `password_hash`
- 修复 wx-login 把前端 code 当 openid 的问题，mock 仅在 dev 环境开启
- 邀约筛选重构为单次遍历，补充组合条件 / 招募中 / 无匹配等边界用例

### Known Limitations
- 数据仍为进程内内存实现，重启丢数据，未接入 MySQL
- 微信登录未接入 jscode2session，非 dev 环境不可用
- 邀约状态机仅实现「招募中 / 已满」两态
