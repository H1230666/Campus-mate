# 用户模块代码评审记录（B → A）

| 项目 | 内容 |
| --- | --- |
| 评审人 | 宋沛蕾（组员 B） |
| 被评审人 | 何佳欣（组员 A） |
| 评审对象 | `main` 分支 `schemas/user_schema.py`、`tests/test_user.py`（commit `2f21aba`） |
| 评审时间 | 2026-11-05 |
| 说明 | A 的用户模块目前直接提交在 `main`，尚未开 PR。以下意见先记录在案；待 A 按规范提交 `feature/a-user` PR 后，B 将逐条贴到对应代码行，形成 GitHub 行内 Review 记录。 |

---

## 一、结论

**Request changes**。用户模型主体结构可用，但存在 2 个安全/结构阻断项（密码明文、模块未接入 backend 包）、2 个越权/隐私风险项，以及“缺少数据库实体”“测试反模式”两类工程问题。建议在 #2 登录接口合入前一并修复。

| 等级 | 数量 | 说明 |
| --- | --- | --- |
| Blocker | 3 | 密码安全、模块未接入 CI、缺少数据库实体 |
| Major | 3 | 手机号校验、`is_active` 越权、响应泄露手机号 |
| Minor | 3 | 用户名格式、测试写法、边界用例缺失 |

---

## 二、逐条意见

### B-01 [Blocker] 密码明文进入模型，且无强度约束

- **位置**：`schemas/user_schema.py:7`
- **问题**：`password: str = Field(min_length=6, max_length=100)` 只限制长度，未限制字符组成；`UserCreate` 会长期持有明文密码，后续若被日志/异常打印将直接泄露。
- **建议**：
  1. 入参侧增加复杂度校验（至少 8 位，包含字母与数字），例如 `field_validator("password")`；
  2. 服务层落库前必须哈希（bcrypt / argon2），模型字段命名为 `password_hash`；
  3. 禁止在 `UserResponse`、日志、异常中输出密码字段。
- **验收**：单测断言“注册后数据库中不存在明文密码”。

### B-02 [Blocker] 只有 Pydantic 模型，没有数据库实体/表结构

- **位置**：`schemas/user_schema.py` 全文
- **问题**：#1 的验收标准是“建立用户实体与数据库模型”，当前只有请求/响应 DTO，没有 ORM 模型、建表语句或迁移脚本，`UserResponse.id: int` 也没有生成策略。
- **建议**：补 `backend/app/models/user.py`（SQLAlchemy）或 `backend/sql/schema.sql`，至少包含主键、唯一索引（`username`、`phone`）、`created_at/updated_at` 默认值；并在架构文档 ER 图中对齐。
- **验收**：建表脚本可在空库执行成功；`username`、`phone` 有唯一约束。

### B-03 [Major] 手机号只校验长度，任意字符串都能通过

- **位置**：`schemas/user_schema.py:9`
- **问题**：`max_length=20` 允许 `"abc"`、`"123"` 等非法值，后续短信/找回密码逻辑会拿到脏数据。
- **建议**：大陆手机号用 `pattern=r"^1[3-9]\d{9}$"`；若要支持国际号码，显式定义 E.164 并统一存储格式。
- **验收**：`phone="123"` 触发 422，`phone="13800138000"` 通过。

### B-04 [Major] `UserUpdate.is_active` 允许普通用户改激活状态

- **位置**：`schemas/user_schema.py:16`
- **问题**：`is_active` 属于账号状态/管理权限字段，放在用户自助更新模型里，一旦接口直接透传，用户可自行解封或停用账号；若接口按 id 更新他人资料，还可停用他人。
- **建议**：从 `UserUpdate` 移除 `is_active`，另建 `AdminUserUpdate`；普通更新接口只允许 `nickname/avatar`（手机号变更走验证码流程）。
- **验收**：普通用户调用更新接口传 `is_active` 被忽略或 422。

### B-05 [Major] 响应模型直接返回完整手机号

- **位置**：`schemas/user_schema.py:21`
- **问题**：`UserResponse.phone` 原样返回，列表页/他人主页会泄露手机号；广场详情也只应展示昵称和头像。
- **建议**：拆成 `UserPublic`（id、nickname、avatar）与 `UserSelf`（含脱敏手机号 `138****8000`），按接口场景返回。
- **验收**：他人主页接口响应中不含完整手机号。

### B-06 [Minor] 用户名缺少字符集约束

- **位置**：`schemas/user_schema.py:6`
- **问题**：只限制 3–50 位，允许空格、emoji、`<script>` 等；既影响展示，也可能在未转义场景引发 XSS。
- **建议**：`pattern=r"^[a-zA-Z0-9_]{3,50}$"`，并在注册时做唯一性检查（409）。
- **验收**：`"ab cd"`、`"<b>"` 被拒绝；重复用户名返回 409。

### B-07 [Major] 测试用 `try/except + assert False`，无法定位失败原因

- **位置**：`tests/test_user.py:19-26`、`28-33`
- **问题**：捕获所有异常并断言 `True`，会把拼写错误、导入错误也当成“校验通过”；且没有断言错误字段。
- **建议**：
  ```python
  with pytest.raises(ValidationError) as exc:
      UserCreate(username="ab", password="123456")
  assert exc.value.errors()[0]["loc"] == ("username",)
  ```
- **验收**：故意改错字段名时测试能失败。

### B-08 [Minor] 边界用例缺失

- **位置**：`tests/test_user.py` 全文
- **问题**：只测了 2 位用户名、3 位密码两个下界，缺少 3/50 位边界、密码 6 位边界、手机号合法/非法、重复用户名、`is_active` 越权等场景。
- **建议**：用 `@pytest.mark.parametrize` 覆盖边界值；每个 Issue 至少 2 条有效用例（考核硬性下限）。

### B-09 [Blocker] 用户模块放在仓库根目录，未接入 backend 包，CI 不会执行其测试

- **位置**：仓库根目录 `schemas/user_schema.py`、`tests/test_user.py`
- **问题**：C 建立的 FastAPI 包位于 `backend/app/`，`backend/pyproject.toml` 配置 `testpaths = ["tests"]`（即 `backend/tests`）。根目录的 `schemas/`、`tests/` 既不会被 `pytest` 收集，也无法在 `backend` 工作目录下通过 `import app...` 引用。实测在 `backend` 下执行 `pytest --collect-only` 只收集 30 条，A 的 4 条 `test_user` 用例不在其中；CI 日志会“全绿”，但用户模块实际零验证。
- **建议**：迁移为 `backend/app/schemas/user.py` + `backend/tests/test_user.py`，import 改为 `from app.schemas.user import ...`；迁移后本地确认 `pytest --collect-only` 为 34 条。
- **验收**：CI 日志出现 `test_user.py::test_user_create_valid` 等 4 条用例；覆盖率报告中包含 `app/schemas/user.py`。

---

## 三、可复用的评审话术（贴到 GitHub 行内）

> **B-01**：这里的 `password` 会以明文形式在内存/日志中流转，建议入参只做复杂度校验，落库前统一 `bcrypt.hashpw`，模型改名为 `password_hash`，并在 `UserResponse` 中彻底移除该字段。

> **B-04**：`is_active` 是管理态字段，放在用户自助更新模型里会带来越权风险；建议移到 `AdminUserUpdate`，普通接口只允许昵称/头像。

> **B-07**：`try/except` 会把实现错误也判为“校验成功”，建议改为 `pytest.raises(ValidationError)` 并断言 `loc`，这样字段改名时测试才会红。

---

## 四、后续动作

| 动作 | 负责人 | 截止 |
| --- | --- | --- |
| 按 B-01/B-02/B-09 修复后再提交 #2 PR | A | 11-06 |
| 在 PR 中逐条回复/标记 resolved | A | 11-06 |
| B 复核并 Approve（或再次 Request changes） | B | 11-06 |
