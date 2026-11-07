# 第 2 次小组会议记录

- 时间：2026-11-07 19:00–19:40
- 地点/方式：线上（微信群语音）
- 出席：@H1230666、@kindly-cs、@heijinggang、@Gyuuu333
- 记录人：何佳欣（@H1230666）

## 一、上次行动项回顾

| 行动项 | 责任人 | 状态 |
|---|---|---|
| 用户模块（#1 #2 #3） | @H1230666 | 代码完成，按 PR 流程合并中 |
| 仓库工程规范（#4） | @H1230666 | 已完成，见 PR #35 |
| 广场与 CI（#15 #16） | @Gyuuu333 | 已提 PR，等评审 |
| 发布/草稿/架构文档（#5–#8） | @kindly-cs | 已提 PR，等评审 |
| 全局异常与状态流转（#11 #12 #13） | @heijinggang | 进行中，尚未提 PR |

## 二、本次议题与结论

| # | 议题 | 结论 | 责任人 |
|---|---|---|---|
| 1 | 后端目录结构 | 统一 `backend/app/`（main/routers/schemas/services/repositories/models）+ `backend/tests`，不保留根目录副本 | 全组 |
| 2 | 小程序目录 | 统一为 `frontend/`，页面放 `frontend/pages/<模块>/` | @kindly-cs |
| 3 | 中期检查材料 | 架构文档（#28）、分支保护截图、CI 配置、Alpha Release v0.1.0、会议记录 ≥2 | @H1230666 |
| 4 | 开发流程 | 禁止直推 main；`feature/<issue号>-<简述>` → PR → 1 人 Approve → 合并 | 全组 |
| 5 | 评审要求 | 每个 PR 至少 1 条行内评审（问题+原因+建议），48 小时内响应；固定 A 评审 D 的 PR | 全组 |
| 6 | PR 数量控制 | 一个 Issue 对应一个 PR，合并后删除分支 | 全组 |

## 三、行动项

- [ ] @H1230666：合并 #1 #2 #3 的 PR（#32/#33/#34），打通 Issue 闭环
- [x] @H1230666：开启 main 分支保护并提交规则说明 `docs/branch-protection.md`
- [x] @H1230666：发布 v0.1.0-alpha（Release Notes 见 Releases）
- [ ] @kindly-cs：把 `miniprogram/` 内容并入 `frontend/`，并把 #5~#8 的 stacked PR 合并为一个
- [ ] @Gyuuu333：确认 CI 门禁在 main 上生效
- [ ] @heijinggang：把 `d-*` 分支开成 PR；删除 `feature/d-backend-global-exception（废除` 分支
- [ ] 全组：下次会前每人至少给他人 PR 留 1 条行内评审

## 四、下次会议

- 时间：2026-11-14 19:00（待定，以群通知为准）
- 议题：v0.2.0 进度对齐、Beta 版本发布准备、评审记录检查
