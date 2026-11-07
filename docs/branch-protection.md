# main 分支保护配置

> 记录时间：2026-11-07（配置截图见 `docs/branch-protection-setting.png`）

在 GitHub 仓库 `Settings → Branches → main` 启用以下规则：

| 规则 | 状态 |
|---|---|
| Require a pull request before merging | ✅ 已启用 |
| Required approvals | ✅ 1 人 |
| Dismiss stale pull request approvals when new commits are pushed | ✅ 已启用 |
| Require conversation resolution before merging | ✅ 已启用 |
| Do not allow force pushes | ✅ 已启用 |
| Do not allow deletions | ✅ 已启用 |
| Require status checks to pass（CI） | ✅ 已启用（`Backend (lint / test / build)`、`Frontend (syntax check)`） |

效果：任何人（含组长）都不能直接 push 到 main，必须走 PR 且通过评审与 CI。
