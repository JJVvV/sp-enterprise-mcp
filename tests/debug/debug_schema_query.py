#!/usr/bin/env python3
"""
专门用于调试低代码系统 schema 查询功能的脚本
"""

import os
import sys

from dotenv import load_dotenv

from sp_database_mcp.database import DatabaseClient

# 加载环境变量
load_dotenv()

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def debug_schema_query():
    """调试 schema 查询功能"""
    print("🔧 调试低代码系统 schema 查询功能")
    print("=" * 60)
    try:
        # 初始化数据库客户端
        print("1. 初始化数据库客户端...")
        db_client = DatabaseClient()
        print("✅ 数据库连接成功")

        # 测试 schema 查询方法
        print("\n2. 测试 _get_table_info_from_schema 方法...")
        table_name = "activity_node"

        # 设置断点：可以在这里设置断点来调试
        schema_info = db_client._get_table_info_from_schema(table_name)

        if schema_info:
            print(f"✅ Schema 查询成功")
            print(f"   表名: {schema_info.name}")
            print(f"   注释: {schema_info.comment}")
            print(f"   字段数量: {len(schema_info.columns)}")

            print("\n   前5个字段:")
            for i, col in enumerate(schema_info.columns[:5]):
                print(f"     {i + 1}. {col.name} ({col.type}) - {col.comment}")
                print(f"        可空: {col.nullable}, 主键: {col.is_primary_key}")

            if schema_info.foreign_keys:
                print(f"\n   外键关系:")
                for fk in schema_info.foreign_keys:
                    print(
                        f"     {fk['column']} -> {fk['referenced_table']}.{fk['referenced_column']}"
                    )
        else:
            print("❌ Schema 查询失败")

        # 测试完整的 get_table_info 方法
        print(f"\n3. 测试完整的 get_table_info 方法...")
        table_info = db_client.get_table_info(table_name)

        if table_info:
            print(f"✅ 完整查询成功")
            print(f"   使用的查询方式: {'Schema查询' if schema_info else '元数据查询'}")
        else:
            print("❌ 完整查询失败")

        # 测试其他表
        print(f"\n4. 测试其他表...")
        test_tables = ["activity_task", "scene_activity"]

        for test_table in test_tables:
            print(f"\n   测试表: {test_table}")
            result = db_client.get_table_info(test_table)
            if result:
                print(f"   ✅ 成功 - {len(result.columns)} 个字段")
            else:
                print(f"   ❌ 失败")

    except Exception as e:
        print(f"❌ 调试过程中出现错误: {e}")
        import traceback

        traceback.print_exc()


def debug_specific_function():
    """调试特定函数 - 可以在这里添加你想要调试的具体代码"""
    print("\n🎯 调试特定函数")
    print("=" * 60)

    # 在这里添加你想要调试的具体代码
    # 例如：
    db_client = DatabaseClient()

    # 设置断点：在这里设置断点来单步调试
    result = db_client._get_table_info_from_schema("activity_node")

    if result:
        print(f"调试结果: {result.name} - {len(result.columns)} 个字段")
    else:
        print("调试结果: 无结果")


if __name__ == "__main__":
    print("🚀 开始调试...")

    # 运行主要的调试功能
    debug_schema_query()

    # 运行特定函数调试
    debug_specific_function()

    print("\n🏁 调试完成!")
