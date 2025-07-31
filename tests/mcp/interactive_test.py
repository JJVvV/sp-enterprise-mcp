#!/usr/bin/env python3
"""交互式测试 MCP 服务器"""

import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def interactive_test():
    """交互式测试 MCP 功能"""
    print("🎮 SP Database MCP 交互式测试")
    print("=" * 50)

    # 配置服务器参数
    server_params = StdioServerParameters(
        command="python", args=["-m", "sp_database_mcp.server"], env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化会话
            await session.initialize()
            print("✅ MCP 会话已初始化\n")

            while True:
                print("\n🔧 可用的测试选项:")
                print("1. 列出所有工具")
                print("2. 列出所有资源")
                print("3. 获取活动表信息")
                print("4. 获取用户表信息")
                print("5. 搜索包含 'activity' 的表")
                print("6. 列出所有表")
                print("7. 自定义查询")
                print("0. 退出")

                choice = input("\n请选择测试选项 (0-7): ").strip()

                if choice == "0":
                    print("👋 测试结束")
                    break
                elif choice == "1":
                    print("\n📋 列出所有工具:")
                    tools = await session.list_tools()
                    for i, tool in enumerate(tools.tools, 1):
                        print(f"  {i}. {tool.name}: {tool.description}")

                elif choice == "2":
                    print("\n📚 列出所有资源:")
                    resources = await session.list_resources()
                    for i, resource in enumerate(resources.resources, 1):
                        print(f"  {i}. {resource.name} ({resource.uri})")

                elif choice == "3":
                    print("\n🔍 获取活动表信息:")
                    try:
                        result = await session.call_tool(
                            "get_table_info",
                            {"table_name": "activities", "source": "database"},
                        )
                        for content in result.content:
                            if hasattr(content, "text"):
                                print(content.text)
                    except Exception as e:
                        print(f"❌ 错误: {e}")

                elif choice == "4":
                    print("\n👥 获取用户表信息:")
                    try:
                        result = await session.call_tool(
                            "get_table_info",
                            {"table_name": "users", "source": "database"},
                        )
                        for content in result.content:
                            if hasattr(content, "text"):
                                print(content.text)
                    except Exception as e:
                        print(f"❌ 错误: {e}")

                elif choice == "5":
                    print("\n🔎 搜索包含 'activity' 的表:")
                    try:
                        result = await session.call_tool(
                            "search_tables",
                            {"keyword": "activity", "source": "database"},
                        )
                        for content in result.content:
                            if hasattr(content, "text"):
                                print(content.text)
                    except Exception as e:
                        print(f"❌ 错误: {e}")

                elif choice == "6":
                    print("\n📊 列出所有表:")
                    try:
                        result = await session.call_tool(
                            "list_all_tables", {"source": "database"}
                        )
                        for content in result.content:
                            if hasattr(content, "text"):
                                print(content.text)
                    except Exception as e:
                        print(f"❌ 错误: {e}")

                elif choice == "7":
                    print("\n🛠️ 自定义查询:")
                    table_name = input("请输入表名: ").strip()
                    if table_name:
                        try:
                            result = await session.call_tool(
                                "get_table_info",
                                {"table_name": table_name, "source": "database"},
                            )
                            for content in result.content:
                                if hasattr(content, "text"):
                                    print(content.text)
                        except Exception as e:
                            print(f"❌ 错误: {e}")

                else:
                    print("❌ 无效选择，请重试")


if __name__ == "__main__":
    try:
        asyncio.run(interactive_test())
    except KeyboardInterrupt:
        print("\n👋 测试被用户中断")
