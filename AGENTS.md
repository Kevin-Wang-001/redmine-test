# AGENTS.md

在本仓库改动代码或文档时，除 README 中的项目说明外，还必须遵守以下约束。

## 改动前

- 开发前先阅读 README，以及 `docs/design/` 中与本次 Issue 对应的设计文档；
  设计文档缺失时停下询问，不要自行发挥需求。

## 改动与测试

- 只使用 Python 标准库，不引入额外依赖。
- 修改功能时必须同步新增/更新 `test_*.py`（与实现同目录）。
- push 前必须执行并通过：

  ```bash
  python3 -m unittest test_app test_health_server
  ```

- 改动对外行为（接口、返回内容、示例命令）时，同步更新 README。
- 设计类文档写入 `docs/design/`，文件名 `issue-<编号>-<简述>.md`。

## PR 与分支

- 禁止直接 push `main`、禁止 force push、禁止自行 Merge PR。
- 一个 PR 只解决一个 Issue；分支名、PR 标题、PR 描述都要带对应 Issue 编号。

## 安全

- 不得提交 `.env`、Token、密钥等敏感内容。
- 不得修改仓库设置、分支保护规则或删除仓库。
