# 数据资产管理平台（MVP 实现）

本仓库基于设计文档实现了一个可运行的 MVP 后端（FastAPI），覆盖以下核心能力：

- 数据源管理：新增、列表、连接测试
- 表资产管理：新增、列表、基础规则校验
- 资产检索：按关键字模糊查询表资产

## 目录

- `architecture.md`：系统架构设计
- `dev-plan.md`：里程碑开发计划
- `domain-model.sql`：领域模型 SQL
- `openapi.yaml`：API 草案
- `src/`：MVP 后端实现

## 快速启动

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn src.main:app --reload
```

访问：

- 健康检查：`GET /health`
- Swagger：`/docs`

## 已实现 API（MVP）

- `GET /api/v1/datasources`
- `POST /api/v1/datasources`
- `POST /api/v1/datasources/{id}/test-connection`
- `GET /api/v1/tables`
- `POST /api/v1/tables`
- `POST /api/v1/tables/{id}/validate`
- `GET /api/v1/assets/search`

## 后续建议

按 `dev-plan.md` 继续补齐：

- RBAC / 审批流 / 审计
- 血缘解析与图数据库
- 标准映射与在线探索
