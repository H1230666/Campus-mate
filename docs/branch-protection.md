# main 分支保护配置

> 记录时间：2026-11-07　|　仓库：`H1230666/Campus-mate`　|　配置位置：Settings → Branches → main

## 一、已启用的规则

| 规则 | 状态 | 说明 |
|---|---|---|
| Require a pull request before merging | ✅ | 任何人（含组长）都不能直接 push 到 main |
| Required approvals | ✅ 1 人 | 至少 1 名非作者 Approve |
| Dismiss stale pull request approvals when new commits are pushed | ✅ | 新提交会作废旧 approve |
| Require conversation resolution before merging | ✅ | 评审意见必须逐条解决 |
| Require status checks to pass | ✅ | `Backend (lint / test / build)`、`Frontend (syntax check)` |
| Do not allow force pushes | ✅ | |
| Do not allow deletions | ✅ | |

## 二、配置页截图

`docs/branch-protection-setting.png`（2026-11-05 首次配置时截图）

> 2026-11-07 又补充了「Require conversation resolution」与「Require status checks」两项，
> 以本文表格和下方 API 快照为准；如需更新截图，可在 Settings → Branches 展开 main 规则后重截。

## 三、API 快照（可复核）

```json
{
  "required_status_checks": {
    "strict": false,
    "contexts": [
      "Backend (lint / test / build)",
      "Frontend (syntax check)"
    ]
  },
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": false
  },
  "required_conversation_resolution": true,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "enforce_admins": false
}
```

复核方式：

```bash
curl -H "Authorization: Bearer <TOKEN>" \
     -H "Accept: application/vnd.github+json" \
     https://api.github.com/repos/H1230666/Campus-mate/branches/main/protection
```
