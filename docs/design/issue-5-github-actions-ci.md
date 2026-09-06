# 设计：增加 GitHub Actions CI

- Redmine 需求：需求库 #5（增加 GitHub Actions CI）
- 目标项目：redmine-test（GitHub: Kevin-Wang-001/redmine-test）
- 设计人：ai_design_agent
- 状态：待评审

## 1. 需求

在仓库中新增 GitHub Actions 工作流 `.github/workflows/ci.yml`，Pull Request 触发时运行 `python3 -m unittest test_app test_health_server`，为 PR 提供自动化的单元测试检查。

## 2. 现状

- 仓库当前没有 `.github/workflows/` 目录，代码变更只能依赖人工本地执行测试，缺少自动化回归检查。
- 项目仅使用 Python 标准库（`app.py`、`health_server.py`），测试文件 `test_app.py` 与 `test_health_server.py` 现有 4 个用例；本地执行 `python3 -m unittest test_app test_health_server` 全部通过。
- `main` 分支受保护：禁止直接 push，必须经 Pull Request 合并且至少 1 个 Approve。
- 本需求不修改仓库设置与分支保护规则，仅新增 CI 配置。

## 3. 方案

### 3.1 新增工作流文件

在仓库根目录新增 `.github/workflows/ci.yml`，建议内容如下：

```yaml
name: CI

on:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Run unit tests
        run: python3 -m unittest test_app test_health_server
```

关键设计点：

- 触发条件为 `pull_request`，即任意 Pull Request 的打开、同步（push 新提交）、重新打开事件都会执行；不区分 base/head 分支，规则简单可预期，完整覆盖需求。
- 使用官方 `actions/checkout@v4` 拉取代码；只固定 major 版本，允许 minor/patch 自动更新。
- `ubuntu-latest` 自带 `python3`，且项目仅依赖 Python 标准库，无需 `actions/setup-python`，也不安装任何第三方依赖。
- 默认在仓库根目录执行，`python3 -m unittest test_app test_health_server` 同时运行两个测试模块；任一用例失败都会使 Job 失败，并在 PR 上显示检查未通过。
- 不声明额外 `permissions`，保持 GitHub 默认的只读内容权限即可完成本需求。

### 3.2 明确不做的事项

- 不修改 `main` 分支保护规则，不把 CI 设为 required check（如需收紧由人工 Review 后另行决策）。
- 不引入第三方 Python 依赖，不上传构建产物。
- 不改变 `app.py`、`health_server.py` 等应用代码行为。

## 4. 接口/测试设计

- 工作流触发接口：GitHub `pull_request` 事件。
- 检查展示：Job 名为 `test`，PR 上显示为 `CI / test`。
- 测试内容：复用仓库现有 `test_app.py`、`test_health_server.py`；本次只新增 CI 配置，不需要新增 Python 单元测试。
- 验证方法：
  1. 在实现分支上提交 `.github/workflows/ci.yml` 并打开 PR，GitHub Actions 会自动运行该工作流；
  2. PR 检查 `CI / test` 通过，且日志显示 4 个用例运行结果为 `OK`；
  3. 人工可继续在本地执行同一命令复核，本地结果应与 CI 一致。

## 5. 验收标准

1. `.github/workflows/ci.yml` 经 PR 合入 main，YAML 语法合法；
2. 仓库 Pull Request 触发 `CI / test`，执行命令确为 `python3 -m unittest test_app test_health_server`；
3. CI 在现有代码上运行通过（4 个用例全部 OK）；
4. 不改变既有应用行为，不引入额外 Python 依赖；
5. 不直接 push main，不修改分支保护规则；
6. 本设计文档经 PR 合入 main。

## 6. 任务拆分建议

建议拆为 1 个任务 Issue（指派 ai_coding_agent）：

- 任务：实现「增加 GitHub Actions CI」——新增 `.github/workflows/ci.yml`，PR 触发时运行 `python3 -m unittest test_app test_health_server`；
- PR 标题与描述引用 Redmine 需求库 #5 及本文档路径；
- 实现 PR 本身即可触发 CI 自证测试通过，之后等待人工 Review / Merge，不得自行 Merge。

## 7. 风险

- 低。仅新增 GitHub Actions 配置文件，不影响应用逻辑与已有接口。
- `ubuntu-latest` 为滚动环境，`python3` 版本可能随时间变化；项目仅使用标准库，受影响的兼容面很小。
- CI 检查通过不替代人工 Review，合并仍遵守仓库现有分支保护与 Approve 规则。
