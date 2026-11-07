# Campus-mate 贡献规范

## 一、分支策略

`main` 为受保护分支，**禁止直接 push**，所有变更必须经由 Pull Request 合并。

| 类型 | 命名格式 | 示例 |
|---|---|---|
| 新功能 | `feature/<issue号>-<英文简述>` | `feature/1-user-schema` |
| 缺陷修复 | `bugfix/<issue号>-<英文简述>` | `bugfix/12-login-401` |
| 紧急修复 | `hotfix/<issue号>-<英文简述>` | `hotfix/30-token-leak` |
| 文档/构建 | `chore/<英文简述>` | `chore/midterm-docs` |

## 二、提交规范（Conventional Commits）

```
<type>(<scope>): <subject>
```

- type 取值：`feat` `fix` `docs` `test` `refactor` `perf` `style` `chore`
- subject 用英文祈使句、小写开头、不加句号，一行不超过 72 字符
- **一个提交只做一件事**，不提交 `__pycache__`、`.idea`、`node_modules` 等自动生成物

示例：

```
feat(user): add field validation for user schema
fix(auth): read secret key from environment
docs(readme): add backend quick start
```

## 三、开发流程

```bash
git switch main && git pull origin main
git switch -c feature/1-user-schema
# 开发 + 提交（粒度见上）
git push -u origin feature/1-user-schema
# 在 GitHub 上开 PR，正文写 Closes #1
```

## 四、Pull Request 要求

- 必须关联 Issue：正文包含 `Closes #<issue号>`
- 变更说明、测试说明、自查清单齐全（使用 PR 模板）
- 单个 PR 控制在 400 行以内，超过需说明理由
- 至少 **1 名非作者** Approve 后才能合并，禁止自评自合
- CI 必须通过（`Backend` + `Miniprogram` 两个 job）

## 五、代码评审要求

- 至少 1 条**行内**评审意见，写清「问题 + 原因 + 建议」，不接受只发 LGTM
- 48 小时内响应，修改后重新 push，形成往返记录
- 评审关注：正确性、边界处理、可读性、安全（密钥/校验）、测试覆盖

## 六、目录与代码规范

- 后端代码统一放 `backend/app/`（`routers` / `schemas` / `services` / `repositories` / `core`），测试放 `backend/tests/`
- 小程序代码放 `frontend/`
- 提交前本地执行：

```bash
cd backend
python -m ruff check app tests
python -m pytest -q
```
