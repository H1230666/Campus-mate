```
# Campus-mate 贡献规范
## 开发流程
1. 从 main 分支拉取最新代码
2. 新建功能分支：`git checkout -b feature/xxx`
3. 开发完成后提交，commit 规范：
   - feat: 新增功能
   - fix: 修复bug
   - docs: 文档修改
   - chore: 工程配置、清理缓存
4. 推送分支，创建 Pull Request
5. 至少一名组员 Review 通过，才能合并进 main
6. 合并后可删除功能分支

## 禁止事项
- 禁止直接在 main 分支 push 代码
- 禁止提交 IDE 配置、缓存文件、本地私有配置
- 修改前先 git pull，避免大量冲突

## 环境启动
后端：
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```
