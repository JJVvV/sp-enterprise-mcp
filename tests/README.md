# 测试目录说明

本目录包含了 SP Database MCP 项目的所有测试文件，按功能分类组织。

## 目录结构

### `/tests/` - 单元测试

- `test_database.py` - 数据库基础功能测试
- `test_database_client.py` - 数据库客户端测试

### `/tests/debug/` - 调试工具

- `debug_schema_query.py` - 低代码系统 schema 查询调试
- `debug_search.py` - 表名搜索功能调试

### `/tests/mcp/` - MCP 协议测试

- `test_mcp_client.py` - MCP 客户端基础测试
- `interactive_test.py` - MCP 交互式测试工具

### `/tests/manual/` - 手动测试

- `test_business_search.py` - 业务关键词搜索测试
- `manual_test.py` - 手动功能验证

### `/tests/integration/` - 集成测试

- `test_ai_field_analysis.py` - AI 字段分析功能测试
- `test_filtered_table_info.py` - 表信息过滤测试
- `test_metabase.py` - Metabase 集成测试
- `test_metabase_interactive.py` - Metabase 交互式测试
- `test_metabase_mcp.py` - Metabase MCP 集成测试
- `test_schema_query.py` - Schema 查询功能测试
- `test_table_info_query.py` - 表信息查询测试

## 运行测试

### 单元测试

```bash
# 运行所有单元测试
pytest tests/test_*.py

# 运行特定测试
pytest tests/test_database_client.py
```

### 调试工具

```bash
# 调试 schema 查询
python tests/debug/debug_schema_query.py

# 调试搜索功能
python tests/debug/debug_search.py
```

### MCP 测试

```bash
# 基础 MCP 客户端测试
python tests/mcp/test_mcp_client.py

# 交互式测试
python tests/mcp/interactive_test.py
```

### 手动测试

```bash
# 业务搜索测试
python tests/manual/test_business_search.py

# 手动功能测试
python tests/manual/manual_test.py
```

### 集成测试

```bash
# 运行所有集成测试
python tests/integration/test_*.py

# 运行特定集成测试
python tests/integration/test_schema_query.py
```

## 注意事项

1. 所有测试都遵循只读原则，不会修改数据库数据
2. 运行测试前请确保已正确配置环境变量（.env 文件）
3. 某些测试需要连接到实际的数据库，请确保网络连接正常
4. 调试工具主要用于开发阶段的问题排查
5. 集成测试验证各个组件之间的协作功能
