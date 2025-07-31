#!/usr/bin/env python3
"""测试 MCP 客户端 - 演示如何与 SP Database MCP 服务器交互"""

import asyncio
import json

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_mcp_client():
    """测试 MCP 客户端功能"""
    print("🚀 启动 MCP 客户端测试...")

    # 配置服务器参数
    server_params = StdioServerParameters(
        command="python", args=["-m", "sp_database_mcp.server"], env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化会话
            await session.initialize()

            print("\n📋 列出可用的工具:")
            tools = await session.list_tools()
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            print("\n📚 列出可用的资源:")
            resources = await session.list_resources()
            for resource in resources.resources:
                print(f"  - {resource.name} ({resource.uri})")

            print("\n🔍 测试获取活动表信息:")
            try:
                result = await session.call_tool(
                    "get_table_info", {"table_name": "activities", "source": "database"}
                )
                print("✅ 成功获取活动表信息:")
                for content in result.content:
                    if hasattr(content, "text"):
                        print(content.text)
            except Exception as e:
                print(f"❌ 获取表信息失败: {e}")

            print("\n📊 测试列出所有表:")
            try:
                result = await session.call_tool(
                    "list_all_tables", {"source": "database"}
                )
                print("✅ 成功列出所有表:")
                for content in result.content:
                    if hasattr(content, "text"):
                        print(content.text)
            except Exception as e:
                print(f"❌ 列出表失败: {e}")

            print("\n🔎 测试搜索表:")
            try:
                result = await session.call_tool(
                    "search_tables", {"keyword": "activity", "source": "database"}
                )
                print("✅ 成功搜索表:")
                for content in result.content:
                    if hasattr(content, "text"):
                        print(content.text)
            except Exception as e:
                print(f"❌ 搜索表失败: {e}")


if __name__ == "__main__":
    asyncio.run(test_mcp_client())
