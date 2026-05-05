# 开发计划（MVP -> V1）

## 里程碑 M1：基础治理（4 周）
- IAM + RBAC
- 数据源管理 + 连接测试 + 锁定保护
- 表管理（可视化/SQL）+ 变更日志
- 资产搜索（基础字段）

## 里程碑 M2：规范与血缘（4 周）
- SQL 规则引擎（命名/注释/层级）
- SQL/ETL 自动血缘解析
- 血缘图谱页面

## 里程碑 M3：标准映射与探索（4~6 周）
- 总行/分行标准维护 + 导入导出
- 自动/手动映射与覆盖率统计
- 在线查询 + 导出审批 + 加密 + 水印
- IP 绑定与自动清理

## 建议技术栈
- 后端：Java 21 + Spring Boot + MyBatis/JPA
- 前端：Vue3 + TypeScript + Ant Design Vue + G6(血缘图)
- 数据库：PostgreSQL + Elasticsearch + Neo4j + Redis
- 消息：Kafka
- 运维：K8s + Helm + GitLab CI

## 测试策略
- 单元测试：规则引擎、SQL 解析器
- 集成测试：连接器、审批流、导出加密
- E2E：建表->血缘->检索->查询导出全链路
