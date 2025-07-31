# SP Database MCP Server 使用指南

## 项目概述

这个项目实现了一个 MCP (Model Context Protocol) 服务器，用于实时获取数据库表结构信息，解决知识库中静态信息过时的问题。

## 功能特性

- 🔄 实时获取数据库表结构信息
- 📊 支持表字段查询和搜索
- 🚀 通过 MCP 协议与 Claude Desktop 集成
- 📝 自动生成格式化的表结构文档

## 快速开始

### 1. 安装依赖

```bash
cd ~/Project/sp-database-mcp
uv sync
```

### 2. 测试服务器

```bash
# 测试简化版服务器（推荐用于演示）
uv run sp-database-mcp-simple

# 测试完整版服务器（需要配置数据库连接）
uv run sp-database-mcp
```

### 3. 配置 Claude Desktop

将以下配置添加到 Claude Desktop 的配置文件中：

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "sp-database": {
      "command": "uv",
      "args": ["run", "sp-database-mcp-simple"],
      "cwd": "/Users/alexliu/Project/sp-database-mcp"
    }
  }
}
```

### 4. 重启 Claude Desktop

配置完成后，重启 Claude Desktop 应用。

## 使用示例

在 Claude Desktop 中，您可以使用以下方式查询数据库表信息：

### 基本查询

```
介绍一下活动表有哪些字段
```

```
获取 activity_node 表的结构信息
```

### 搜索表

```
搜索包含 "activity" 的表
```

### 列出所有表

```
列出所有数据库表
```

### 获取字段简要说明

```
获取 activity_node 表的字段简要说明
```

## 可用的表

目前演示版本包含以下表：

1. **activity_node** - 活动节点表，用于记录流程活动中的关键节点
2. **scene_activity** - 场景活动表，记录各种业务场景下的活动信息
3. **da_asset_object** - 数据资产对象表，存储数据资产的基本信息

## 扩展功能

### 连接真实数据库

如果您想连接真实的数据库，请：

1. 创建 `.env` 文件：

```bash
cp .env.example .env
```

2. 配置数据库连接：

```env
DATABASE_URL=mysql://username:password@localhost:3306/database_name
```

3. 使用完整版服务器：

```json
{
  "mcpServers": {
    "sp-database": {
      "command": "uv",
      "args": ["run", "sp-database-mcp"],
      "cwd": "/Users/alexliu/Project/sp-database-mcp"
    }
  }
}
```

### 通过 API 获取数据

配置 API 接口：

```env
API_BASE_URL=https://your-api-server.com
API_TOKEN=your-api-token
```

## 故障排除

### 常见问题

1. **服务器启动失败**
   - 检查 Python 版本（需要 >= 3.10）
   - 确保所有依赖已安装：`uv sync`

2. **Claude Desktop 无法连接**
   - 检查配置文件路径是否正确
   - 确保 JSON 格式正确
   - 重启 Claude Desktop

3. **权限问题**
   - 确保 Claude Desktop 有权限访问项目目录
   - 检查文件权限设置

### 调试模式

启用调试输出：

```bash
export LOG_LEVEL=DEBUG
uv run sp-database-mcp-simple
```

## 开发

### 运行测试

```bash
uv run pytest
```

### 代码格式化

```bash
uv run black .
uv run isort .
```

### 类型检查

```bash
uv run mypy .
```

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License
