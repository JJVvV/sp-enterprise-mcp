#!/usr/bin/env python3
"""
测试 metabase 数据库的 MCP 功能
"""

import os
import sys

from dotenv import load_dotenv

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

try:
    from sp_database_mcp.database import DatabaseClient
except ImportError:
    print("❌ 无法导入 DatabaseClient，请检查项目结构")
    sys.exit(1)


def test_mcp_tools():
    """测试 MCP 工具"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ 未找到 DATABASE_URL")
        return

    print("🧪 测试 MCP 工具功能...")
    print("=" * 50)

    try:
        client = DatabaseClient(database_url)

        # 1. 测试 list_all_tables
        print("\n📊 1. 测试 list_all_tables:")
        # 获取所有表名
        all_tables = client.get_all_tables()
        tables_result = f"找到 {len(all_tables)} 个表: {', '.join(all_tables[:10])}{'...' if len(all_tables) > 10 else ''}"
        print(f"返回结果长度: {len(tables_result)} 字符")
        print("前500字符预览:")
        print(
            tables_result[:500] + "..." if len(tables_result) > 500 else tables_result
        )

        # 2. 测试 search_tables - 搜索资产相关的表
        print("\n🔍 2. 测试 search_tables (搜索 '资产'):")
        search_result = client.search_tables("资产")
        search_result = f"找到 {len(search_result)} 个包含'资产'的表: {[t.name for t in search_result]}"
        print(search_result)

        # 3. 测试 search_tables - 搜索用户相关的表
        print("\n🔍 3. 测试 search_tables (搜索 'user'):")
        user_search_result = client.search_tables("user")
        user_search_result = f"找到 {len(user_search_result)} 个包含'user'的表: {[t.name for t in user_search_result[:5]]}{'...' if len(user_search_result) > 5 else ''}"
        print(user_search_result)

        # 4. 测试 get_table_info - 获取具体表信息
        print("\n📋 4. 测试 get_table_info (sys_user 表):")
        table_info = client.get_table_info("sys_user")
        if table_info:
            table_info_result = f"表 {table_info.name}: {len(table_info.columns)} 个字段 - {[col.name for col in table_info.columns[:5]]}"
        else:
            table_info_result = "未找到 sys_user 表"
        print(table_info_result)

        # 5. 测试一些常见的业务表
        interesting_tables = [
            "da_logical_entity",  # 逻辑实体
            "da_entity_attribute",  # 实体属性
            "sys_role",  # 系统角色
            "project",  # 项目
            "activity",  # 活动
        ]

        print("\n📊 5. 测试常见业务表信息:")
        for table in interesting_tables:
            try:
                table_info = client.get_table_info(table)
                if table_info:
                    result = f"表 {table_info.name}: {len(table_info.columns)} 个字段"
                else:
                    result = f"未找到表 {table}"
                print(f"\n--- {table} ---")
                # 只显示前300字符
                preview = result[:300] + "..." if len(result) > 300 else result
                print(preview)
            except Exception as e:
                print(f"❌ 获取 {table} 信息失败: {e}")

        print("\n✅ MCP 工具测试完成!")

    except Exception as e:
        print(f"❌ MCP 工具测试失败: {e}")
        import traceback

        traceback.print_exc()


def main():
    """主函数"""
    print("🚀 Metabase MCP 工具测试")
    print("=" * 40)

    # 运行测试
    test_mcp_tools()


if __name__ == "__main__":
    main()
