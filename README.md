# Campus-mate 校园搭子小程序
> 软件工程小组作业 | 校园搭子匹配平台

## ✨项目简介
本小程序面向在校大学生，提供搭子发布、兴趣匹配、活动约伴功能，支持学习搭子、运动搭子、美食搭子等多种场景。

## 👥小组组员
- 组员A：何佳欣
- 组员B：宋沛蕾
- 组员C：何佳宇
- 组员D：蓝海欣

## 📌第八周任务目标
完成需求梳理、原型设计，搭建基础项目结构，划分模块，提交中期进展报告。

## 📂目录规划（后续填充）
├── docs/            # 项目文档：SRS 需求规格说明书、周报、分工记录、中期报告
├── frontend/        # 微信小程序前端代码
├── backend/         # 后端服务代码
└── README.md        # 项目说明文档

## 📜开发规范
1. 分支规则：main为主分支（开启保护，禁止直接push），每位成员新建独立开发分支（dev-a / dev-b / dev-c / dev-d），通过PR合并代码。
2. 提交规范：`feat: 新增xx功能` / `docs: 更新文档` / `fix: 修复xx问题` / `style: 调整页面样式`

## 🧱 技术栈

| 层 | 技术 |
|---|---|
| 前端 | 微信小程序原生（WXML / WXSS / JS），目录 `frontend/` |
| 后端 | Python 3.12 + FastAPI + Pydantic v2，目录 `backend/` |
| 认证 | JWT（python-jose，HS256） |
| 数据 | SQLAlchemy ORM（当前为内存模拟，后续切 MySQL） |
| 质量 | pytest + ruff + GitHub Actions |

## 📂 目录结构

```
backend/
├── app/
│   ├── main.py            # FastAPI 入口
│   ├── routers/           # 路由层
│   ├── schemas/           # Pydantic 模型
│   ├── services/          # 业务逻辑
│   ├── repositories/      # 数据访问
│   └── core/              # 鉴权、配置等基础设施
├── tests/                 # 单元测试
├── requirements.txt
└── pyproject.toml         # ruff / pytest 配置
frontend/                  # 微信小程序
docs/                      # 需求、会议记录
```

## 🚀 快速开始

### 环境要求
- Python >= 3.10（CI 使用 3.12）
- Node.js >= 20（小程序 JS 语法检查，可选）

### 后端启动

```bash
git clone https://github.com/H1230666/Campus-mate.git
cd Campus-mate/backend

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
# source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

访问 `http://127.0.0.1:8000/docs` 查看接口文档。

### 运行测试

```bash
cd backend
python -m pytest -q
```

### 小程序端

用微信开发者工具导入 `frontend/` 目录即可。

## 📚 文档索引

| 文档 | 说明 |
|---|---|
| `docs/SRS.md` | 需求规格说明书 |
| `docs/meetings/` | 小组会议记录 |
| `CHANGELOG.md` | 版本变更记录 |
| `CONTRIBUTING.md` | 开发与协作规范 |

## 🔁 分支与提交规范

- 分支：`feature/<issue号>-<英文简称>`、`bugfix/<issue号>-<英文简称>`、`chore/<简称>`
- 禁止直推 `main`，一律走 PR，至少 1 名非作者 Approve 后合并
- 提交类型：`feat` / `fix` / `docs` / `test` / `refactor` / `chore`，一个提交只做一件事
- 每个 PR 必须写 `Closes #<issue号>`，保证 Issue 闭环可追溯
