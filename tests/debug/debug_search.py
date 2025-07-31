#!/usr/bin/env python3
"""
调试搜索功能的简化脚本
专门用于调试表名搜索逻辑
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


def debug_search_single_keyword(client, keyword):
    """调试单个关键词的搜索过程"""
    print(f"\n🔍 调试搜索关键词: '{keyword}'")
    print("=" * 50)

    # 1. 获取所有表名
    all_tables = client.get_all_tables()
    print(f"📊 数据库总表数: {len(all_tables)}")

    # 2. 手动筛选包含关键词的表名
    matching_tables = [
        table for table in all_tables if keyword.lower() in table.lower()
    ]
    print(f"🎯 包含 '{keyword}' 的表名: {len(matching_tables)} 个")

    # 3. 显示匹配的表名
    if matching_tables:
        print("匹配的表名:")
        for i, table_name in enumerate(matching_tables, 1):
            print(f"  {i}. {table_name}")
    else:
        print("❌ 没有找到匹配的表名")

        # 尝试模糊匹配
        print(f"\n🔍 尝试模糊匹配 '{keyword}':")
        fuzzy_matches = []
        for table in all_tables:
            if any(char in table.lower() for char in keyword.lower()):
                fuzzy_matches.append(table)

        if fuzzy_matches:
            print(f"可能相关的表 (前10个): {fuzzy_matches[:10]}")
        else:
            print("没有找到相关的表")

    # 4. 使用 DatabaseClient 的搜索方法
    print(f"\n🧪 使用 DatabaseClient.search_tables() 方法:")
    try:
        search_results = client.search_tables(keyword)
        print(f"搜索结果数量: {len(search_results)}")

        for i, table_info in enumerate(search_results, 1):
            print(f"  {i}. {table_info.name} (字段数: {len(table_info.columns)})")

    except Exception as e:
        print(f"❌ 搜索出错: {e}")
        import traceback

        traceback.print_exc()


def main():
    """主调试函数"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ 未找到 DATABASE_URL")
        return

    print("🚀 搜索功能调试工具")
    print("=" * 60)

    try:
        client = DatabaseClient(database_url)

        # 调试几个关键词
        test_keywords = [
            "activity",  # 活动 (英文)
            "活动",  # 活动 (中文)
            "user",  # 用户
            "sys",  # 系统
            "role",  # 角色
            "task",  # 任务
            "project",  # 项目
            "data",  # 数据
        ]

        for keyword in test_keywords:
            debug_search_single_keyword(client, keyword)

            # 在每个关键词之间添加分隔
            print("\n" + "=" * 60)

        print("✅ 调试完成!")

    except Exception as e:
        print(f"❌ 调试失败: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
