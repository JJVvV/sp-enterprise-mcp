# SP Database MCP 发布指南

本文档介绍如何将 SP Database MCP 服务器发布给其他用户使用。

## 发布方式

### 1. PyPI 发布（推荐）

#### 准备工作

1. 确保你有 PyPI 账号：https://pypi.org/account/register/
2. 安装发布工具：
   ```bash
   uv add --dev build twine
   ```

#### 发布步骤

1. **构建包**：
   ```bash
   # 清理之前的构建
   rm -rf dist/ build/
   
   # 构建包
   uv run python -m build
   ```

2. **检查包**：
   ```bash
   # 检查包的完整性
   uv run twine check dist/*
   ```

3. **上传到 TestPyPI（测试）**：
   ```bash
   # 先上传到测试环境
   uv run twine upload --repository testpypi dist/*
   ```

4. **测试安装**：
   ```bash
   # 从 TestPyPI 安装测试
   pip install --index-url https://test.pypi.org/simple/ sp-database-mcp
   ```

5. **上传到正式 PyPI**：
   ```bash
   # 确认无误后上传到正式环境
   uv run twine upload dist/*
   ```

#### 用户安装方式

发布后，用户可以通过以下方式安装：

```bash
# 基础安装
pip install sp-database-mcp

# 或使用 uv
uv add sp-database-mcp

# 安装特定数据库支持
pip install sp-database-mcp[mysql]
pip install sp-database-mcp[postgresql]
```

### 2. GitHub Releases

#### 创建 Release

1. 在 GitHub 仓库中点击 "Releases"
2. 点击 "Create a new release"
3. 创建新的 tag（如 v0.1.0）
4. 填写 Release 说明
5. 上传构建好的 wheel 文件

#### 用户安装方式

```bash
# 直接从 GitHub 安装
pip install git+https://github.com/yourusername/sp-enterprise-mcp.git

# 安装特定版本
pip install git+https://github.com/yourusername/sp-enterprise-mcp.git@v0.1.0
```

### 3. Docker 镜像

#### 创建 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml .
COPY src/ src/

RUN pip install .

EXPOSE 8000

CMD ["sp-database-mcp"]
```

#### 构建和发布

```bash
# 构建镜像
docker build -t sp-database-mcp:latest .

# 推送到 Docker Hub
docker tag sp-database-mcp:latest yourusername/sp-database-mcp:latest
docker push yourusername/sp-database-mcp:latest
```

#### 用户使用方式

```bash
# 运行 Docker 容器
docker run -e DATABASE_URL="your_db_url" yourusername/sp-database-mcp:latest
```

## MCP 客户端配置

### Claude Desktop 配置

用户需要在 Claude Desktop 的配置文件中添加：

```json
{
  "mcpServers": {
    "sp-database-mcp": {
      "command": "sp-database-mcp",
      "env": {
        "DATABASE_URL": "your_database_url_here"
      }
    }
  }
}
```

### Windsurf 配置

在 Windsurf 的 MCP 配置文件中添加：

```json
{
  "mcpServers": {
    "sp-database-mcp": {
      "command": "python",
      "args": ["-m", "sp_database_mcp.server"],
      "env": {
        "DATABASE_URL": "your_database_url_here"
      }
    }
  }
}
```

## 版本管理

### 语义化版本

遵循 [Semantic Versioning](https://semver.org/)：
- `MAJOR.MINOR.PATCH`
- 主版本号：不兼容的 API 修改
- 次版本号：向下兼容的功能性新增
- 修订号：向下兼容的问题修正

### 更新版本

1. 更新 `pyproject.toml` 中的版本号
2. 更新 `CHANGELOG.md`
3. 创建 git tag
4. 重新构建和发布

## 文档和支持

### 必要文档

- [x] README.md - 项目介绍和快速开始
- [x] LICENSE - 开源许可证
- [x] USAGE.md - 详细使用说明
- [ ] CHANGELOG.md - 版本更新日志
- [ ] CONTRIBUTING.md - 贡献指南

### 社区支持

1. **GitHub Issues** - 问题追踪和功能请求
2. **GitHub Discussions** - 社区讨论
3. **文档网站** - 详细的 API 文档
4. **示例项目** - 使用示例和最佳实践

## 推广策略

1. **MCP 社区** - 在 MCP 相关社区分享
2. **技术博客** - 写技术文章介绍项目
3. **开源社区** - 参与相关开源项目讨论
4. **社交媒体** - 在技术社交平台分享

## 维护建议

1. **定期更新依赖** - 保持依赖包的最新版本
2. **安全更新** - 及时修复安全漏洞
3. **性能优化** - 持续改进性能
4. **用户反馈** - 积极响应用户问题和建议
5. **测试覆盖** - 保持高质量的测试覆盖率
