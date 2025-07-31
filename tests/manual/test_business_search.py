#!/usr/bin/env python3
"""
模拟用户搜索各种业务关键词的测试
测试用户可能会搜索的各种业务术语
"""

import os
import sys

from dotenv import load_dotenv

from sp_database_mcp.database import DatabaseClient

# 添加项目根目录到 Python 路径
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)


def search_and_display(client, keyword, description=""):
    """搜索关键词并显示结果"""
    print(f"\n🔍 搜索关键词: '{keyword}' {description}")
    print("-" * 60)

    try:
        results = client.search_tables(keyword)

        if not results:
            print(f"❌ 未找到包含 '{keyword}' 的表")
            return

        print(f"✅ 找到 {len(results)} 个相关表:")

        for i, table_info in enumerate(results, 1):
            if i != 0:
                return
            print(f"  {i}. {table_info.name}")

            # 显示表的基本信息
            if table_info.comment:
                print(f"     📝 描述: {table_info.comment}")

            # 显示前几个字段
            if table_info.columns:
                key_columns = [col.name for col in table_info.columns[:5]]
                print(f"     📊 主要字段: {', '.join(key_columns)}")
                if len(table_info.columns) > 5:
                    print(f"     📊 总字段数: {len(table_info.columns)}")

            # 显示主键
            primary_keys = [
                col.name for col in table_info.columns if col.is_primary_key
            ]
            if primary_keys:
                print(f"     🔑 主键: {', '.join(primary_keys)}")

            print()  # 空行分隔

    except Exception as e:
        print(f"❌ 搜索 '{keyword}' 时出错: {e}")


def test_business_keywords():
    """测试各种业务关键词"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ 未找到 DATABASE_URL")
        return

    print("🚀 业务关键词搜索测试")
    print("=" * 80)
    print("模拟用户可能搜索的各种业务术语...")

    try:
        client = DatabaseClient(database_url)

        # 定义要测试的关键词
        search_keywords = [
            ("activity_node", "- 活动"),
        ]

        # 执行搜索测试
        for keyword, description in search_keywords:
            search_and_display(client, keyword, description)

        # 额外测试：获取一些热门表的详细信息
        print("\n" + "=" * 80)
        print("🔍 热门表详细信息预览")
        print("=" * 80)

        # 基于搜索结果，选择一些可能比较重要的表
        important_tables = ["activity_task"]

        for table_name in important_tables:
            print(f"\n📋 表: {table_name}")
            print("-" * 40)

            table_info = client.get_table_info(table_name)
            if table_info:
                print(f"📊 字段总数: {len(table_info.columns)}")

                # 显示所有字段的详细信息
                print("字段详情:")
                for col in table_info.columns:
                    nullable = "可空" if col.nullable else "非空"
                    pk_mark = " 🔑" if col.is_primary_key else ""
                    default_info = f" (默认: {col.default})" if col.default else ""
                    print(
                        f"  - {col.code}: {col.name} {col.type} ({nullable}){pk_mark}{default_info}"
                    )

                # 显示外键关系
                if table_info.foreign_keys:
                    print("外键关系:")
                    for fk in table_info.foreign_keys:
                        print(
                            f"  - {fk['column']} -> {fk['referenced_table']}.{fk['referenced_column']}"
                        )

                # 显示索引
                if table_info.indexes:
                    print("索引:")
                    for idx in table_info.indexes:
                        unique_mark = " (唯一)" if idx["unique"] else ""
                        print(
                            f"  - {idx['name']}: {', '.join(idx['columns'])}{unique_mark}"
                        )
            else:
                print(f"❌ 表 {table_name} 不存在")

        print("\n✅ 业务关键词搜索测试完成!")

    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback

        traceback.print_exc()


def main():
    """主函数"""
    test_business_keywords()


if __name__ == "__main__":
    main()
