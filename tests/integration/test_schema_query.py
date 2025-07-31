#!/usr/bin/env python3
"""测试低代码系统 schema 查询功能"""

import asyncio
import os

from sp_database_mcp.api_client import APIClient
from sp_database_mcp.database import DatabaseClient


async def test_database_schema_query():
    """测试数据库直连的 schema 查询"""
    print("=== 测试数据库直连的 schema 查询 ===")

    try:
        # 初始化数据库客户端
        db_client = DatabaseClient()

        # 测试查询 activity_node 表
        print("\n1. 查询 activity_node 表信息:")
        table_info = db_client.get_table_info("activity_node")

        if table_info:
            print(f"表名: {table_info.name}")
            print(f"注释: {table_info.comment}")
            print(f"字段数量: {len(table_info.columns)}")

            print("\n字段信息:")
            for i, col in enumerate(table_info.columns[:5]):  # 只显示前5个字段
                print(f"  {i + 1}. {col.name} ({col.type}) - {col.comment}")
                print(f"     可空: {col.nullable}, 主键: {col.is_primary_key}")
                if col.default:
                    print(f"     默认值: {col.default}")

            if len(table_info.columns) > 5:
                print(f"  ... 还有 {len(table_info.columns) - 5} 个字段")

            if table_info.foreign_keys:
                print(f"\n外键关系:")
                for fk in table_info.foreign_keys:
                    print(
                        f"  {fk['column']} -> {fk['referenced_table']}.{fk['referenced_column']}"
                    )
        else:
            print("未找到表信息")

        # 测试查询一个不存在的表
        print("\n2. 查询不存在的表 (test_nonexistent):")
        table_info = db_client.get_table_info("test_nonexistent")
        if table_info:
            print("找到了表信息")
        else:
            print("未找到表信息（预期结果）")

    except Exception as e:
        print(f"数据库查询测试失败: {e}")


async def test_api_schema_query():
    """测试 API 的 schema 查询"""
    print("\n=== 测试 API 的 schema 查询 ===")

    # 检查是否配置了 API
    api_base_url = os.getenv("API_BASE_URL")
    if not api_base_url:
        print("未配置 API_BASE_URL，跳过 API 测试")
        return

    try:
        # 初始化 API 客户端
        api_client = APIClient()

        # 测试查询 activity_node 表
        print("\n1. 通过 API 查询 activity_node 表信息:")
        table_info = await api_client.get_table_info("activity_node")

        if table_info:
            print(f"表名: {table_info.name}")
            print(f"注释: {table_info.comment}")
            print(f"字段数量: {len(table_info.columns)}")

            print("\n字段信息:")
            for i, col in enumerate(table_info.columns[:3]):  # 只显示前3个字段
                print(f"  {i + 1}. {col.name} ({col.type}) - {col.comment}")
        else:
            print("未找到表信息（可能是 API 未实现或网络问题）")

    except Exception as e:
        print(f"API 查询测试失败: {e}")


def test_schema_table_existence():
    """测试 schema 表是否存在"""
    print("\n=== 检查 schema 表是否存在 ===")

    try:
        db_client = DatabaseClient()
        all_tables = db_client.get_all_tables()

        schema_tables = ["da_logic_entity", "da_entity_attribute"]
        for table in schema_tables:
            if table in all_tables:
                print(f"✓ {table} 表存在")
            else:
                print(f"✗ {table} 表不存在")

        # 检查是否有 activity_node 相关的实体
        print(f"\n检查数据库中是否有 activity_node 相关数据...")
        if "da_logic_entity" in all_tables:
            try:
                from sqlalchemy import text

                with db_client.engine.connect() as conn:
                    result = conn.execute(
                        text(
                            "SELECT code, name FROM da_logic_entity WHERE code LIKE '%activity%' LIMIT 5"
                        )
                    ).fetchall()

                    if result:
                        print("找到相关实体:")
                        for row in result:
                            print(f"  - {row[0]}: {row[1]}")
                    else:
                        print("未找到包含 'activity' 的实体")
            except Exception as e:
                print(f"查询实体数据失败: {e}")

    except Exception as e:
        print(f"检查 schema 表失败: {e}")


async def main():
    """主测试函数"""
    print("SP Database MCP - Schema 查询功能测试")
    print("=" * 50)

    # 检查环境变量
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("错误: 未设置 DATABASE_URL 环境变量")
        return

    print(f"数据库连接: {database_url[:50]}...")

    # 运行测试
    test_schema_table_existence()
    await test_database_schema_query()
    await test_api_schema_query()

    print("\n测试完成!")


if __name__ == "__main__":
    asyncio.run(main())
