# 数据资产管理平台架构设计

## 1. 目标与范围
围绕 7 大模块建设统一的数据资产平台：
1. 数据源管理
2. 数据库表管理
3. 数据资产查询
4. 血缘链路分析
5. 开发规范化管控
6. 数据标准映射
7. 数据探索模块

## 2. 总体架构

```text
[Web Console]
    |
[API Gateway + Auth]
    |
+------------------------------+
| Asset Platform Backend       |
| - IAM & RBAC                |
| - Data Source Service        |
| - Metadata/Table Service     |
| - Search Service             |
| - Lineage Service            |
| - Rule Engine Service        |
| - Standard Mapping Service   |
| - Query Exploration Service  |
| - Workflow/Approval Service  |
| - Audit & Watermark Service  |
+------------------------------+
    |
+------------------------------+
| Infrastructure               |
| - PostgreSQL (OLTP)          |
| - Elasticsearch (Search)     |
| - Neo4j (Lineage Graph)      |
| - Redis (Cache/Lock)         |
| - MQ(Kafka/RabbitMQ)         |
| - Object Storage (Export)    |
+------------------------------+
```

## 3. 模块详细设计

### 3.1 数据源管理
- 支持 GBASE8a, GAUSSDB, PostgreSQL, TDSQL, Hive, Oracle, FTP, 本地文件。
- 数据源连接器 SPI：统一 `ConnectorDriver` 接口，按数据源类型加载实现。
- 配置加密：密码字段使用 KMS + AES 加密存储。
- 锁定保护：当数据源关联表/任务>0 时，禁止删除；修改需走变更审批。
- 权限：
  - `ROLE_ADMIN`：增删改查/测试连接
  - `ROLE_USER`：仅查看与使用授权数据源

### 3.2 数据库表管理
- 建表模式：
  - 可视化建表（列编辑器、分区配置）
  - SQL 建表（ANTLR 语法解析）
- 合规校验：字段/表必须存在中文注释；SQL 语法与目标方言匹配。
- 元数据：资产分类、安全等级、责任人、状态（在途/下线）。
- 变更日志：记录 DDL 变更前后快照 + 操作人 + 审批单号。

### 3.3 数据资产查询
- 检索维度：表名、字段名、标签、责任人、所属系统、库名。
- 检索方案：
  - 元数据写入 PostgreSQL
  - 索引异步写入 Elasticsearch
- 全景页：基本信息、分区、变更历史、任务依赖（来自调度系统同步）。

### 3.4 血缘链路分析
- SQL 解析：抽取 `source_table -> target_table`、`source_col -> target_col`。
- ETL 任务适配器：支持离线任务 DAG 导入。
- 存储：Neo4j 图模型（节点：表/字段/任务；边：读取/写入/派生）。
- 前端：拓扑图支持缩放、拖拽、点击节点看详情。

### 3.5 开发规范化管控
- 命名规范：可配置正则（如 `^(ods|dwd|dws|ads)_[a-z0-9_]+$`）。
- SQL 检查：多方言 parser + lint 规则（禁止 `select *` 等）。
- 分层依赖：O/G/R 层级白名单矩阵校验。

### 3.6 数据标准映射
- 维护分行 ODS 接口：CRUD + Excel 导入导出。
- 总行标准管理：接口标准、字段安全等级、检索。
- 自动对齐：按字段名/语义相似度建议映射；人工确认。
- 映射图谱：按系统/主题域展示覆盖率、缺口字段。

### 3.7 数据探索模块
- 在线查询：SQL 编辑、执行计划预检、结果分页。
- 查询安全：
  - 行数阈值限制
  - 超时/资源配额
  - 脱敏函数注入
- 结果导出：发起审批 -> 责任人批准 -> 加密打包（含水印元数据）。
- 安全加固：
  - 数字水印（EHR/姓名/IP/时间）
  - IP 白名单绑定
  - 用户私有表 TTL 自动清理任务

## 4. 关键非功能设计
- 可用性：服务无状态部署 + 水平扩展。
- 安全性：RBAC、字段级权限、审计全留痕、敏感数据脱敏。
- 可观测：日志、指标、链路追踪（OpenTelemetry）。
- 性能目标：
  - 检索 P95 < 1.5s
  - 血缘图查询 P95 < 2s
  - 连接测试 < 5s

## 5. 事件驱动流程（示例）
1. 用户提交建表 SQL。
2. Rule Engine 校验命名/注释/分层依赖。
3. 合规通过后写入元数据并发布 `TABLE_CHANGED` 事件。
4. Lineage Service 订阅事件，解析 SQL 并更新图谱。
5. Search Service 订阅事件，更新索引。
6. Audit Service 记录全链路操作日志。
