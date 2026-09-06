# 设计：HTTP 服务增加版本查询接口

- Redmine 需求：需求库 #3（HTTP 服务增加版本查询接口）
- 目标项目：redmine-test（GitHub: Kevin-Wang-001/redmine-test）
- 设计人：ai_design_agent
- 状态：待评审

## 1. 需求

新增 `GET /version` 接口，返回服务名称和版本号，并提供配套单元测试。

## 2. 现状

`health_server.py` 基于 Python 标准库 `http.server` 实现，当前只有 `GET /health` 路由，返回 `{"status": "ok"}`；未知路径返回 404。单元测试位于 `test_health_server.py`，用真实 HTTP 连接验证响应。

## 3. 方案

### 3.1 接口定义

`GET /version`

- 成功响应：HTTP 200
- Content-Type：`application/json; charset=utf-8`
- Body：

```json
{
  "service": "redmine-test",
  "version": "0.1.0"
}
```

- 查询参数忽略，按路径精确匹配。

### 3.2 实现方式

在 `health_server.py` 顶部增加模块级常量作为唯一来源：

```python
SERVICE_NAME = "redmine-test"
SERVICE_VERSION = "0.1.0"
```

在请求分发处增加 `/version` 分支，复用现有 `_send_json` 方法；未知路径继续返回 404，不影响 `/health` 现有行为。

### 3.3 测试

在 `test_health_server.py` 中新增用例：

- `GET /version` 返回 200；
- Content-Type 为 JSON；
- Body 等于 `{"service": "redmine-test", "version": "0.1.0"}`；
- 原有 `/health` 与 404 用例保持通过。

### 3.4 文档

在 `README.md` 的 Health check 之后补充 `/version` 的调用示例与返回示例。

## 4. 验收标准

1. `python3 -m unittest test_app test_health_server` 全部通过；
2. `curl http://127.0.0.1:8000/version` 返回 200 及上述 JSON；
3. 已有 `/health` 行为不回归；
4. 通过 PR 合并到 main（禁止直推）。

## 5. 任务拆分建议

本需求改动集中且可独立交付，建议拆为 1 个任务 Issue：

- 任务：实现 `GET /version` 接口并补充单元测试与 README

## 6. 风险

- 低。仅新增只读接口，使用标准库，不引入依赖，不改变既有路由。
