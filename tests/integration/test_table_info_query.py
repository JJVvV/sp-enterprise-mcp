#!/usr/bin/env python3
"""
模拟用户查询特定表信息的功能
场景：用户输入 "帮我获取一下表名为 activity_node 表的信息"
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


def get_table_detailed_info(client, table_name):
    """获取表的详细信息 - 模拟 MCP 工具的 get_table_info 功能"""
    print(f"🔍 正在获取表 '{table_name}' 的详细信息...")
    print("=" * 60)

    try:
        table_info = client.get_table_info(table_name)

        if not table_info:
            print(f"❌ 未找到表 '{table_name}'")

            # 提供建议：搜索相似的表名
            print(f"\n💡 建议：搜索包含 '{table_name}' 关键词的表...")
            similar_tables = client.search_tables(table_name)
            if similar_tables:
                print(f"找到 {len(similar_tables)} 个相似的表:")
                for i, similar_table in enumerate(similar_tables[:5], 1):
                    print(f"  {i}. {similar_table.name}")
            else:
                print("没有找到相似的表名")
            return

        # 显示表的基本信息
        print(f"📋 表名: {table_info.name}")
        if table_info.comment:
            print(f"📝 表描述: {table_info.comment}")
        print(f"📊 字段总数: {len(table_info.columns)}")

        # 显示所有字段的详细信息
        print(f"\n🔍 字段详细信息:")
        print("-" * 50)
        print("字段名 | 数据类型 | 是否可空 | 是否主键 | 默认值 | 最大长度")
        print("-" * 50)

        for col in table_info.columns:
            nullable = "是" if col.nullable else "否"
            is_pk = "是" if col.is_primary_key else "否"
            default_val = col.default if col.default else "无"
            max_len = col.max_length if col.max_length else "无限制"

            print(
                f"{col.name:<20} | {str(col.type):<15} | {nullable:<8} | {is_pk:<8} | {default_val:<10} | {max_len}"
            )

        # 显示主键信息
        primary_keys = [col.name for col in table_info.columns if col.is_primary_key]
        if primary_keys:
            print(f"\n🔑 主键字段: {', '.join(primary_keys)}")

        # 显示外键关系
        if table_info.foreign_keys:
            print(f"\n🔗 外键关系:")
            for fk in table_info.foreign_keys:
                print(
                    f"  - {fk['column']} → {fk['referenced_table']}.{fk['referenced_column']}"
                )

        # 显示索引信息
        if table_info.indexes:
            print(f"\n📇 索引信息:")
            for idx in table_info.indexes:
                unique_mark = " (唯一索引)" if idx["unique"] else ""
                print(f"  - {idx['name']}: {', '.join(idx['columns'])}{unique_mark}")

        # 提供使用建议
        print(f"\n💡 使用建议:")
        print(f"  - 该表共有 {len(table_info.columns)} 个字段")
        if primary_keys:
            print(f"  - 主键字段: {', '.join(primary_keys)}")
        if table_info.foreign_keys:
            print(f"  - 该表与其他 {len(table_info.foreign_keys)} 个表有关联关系")

        return table_info

    except Exception as e:
        print(f"❌ 获取表信息时出错: {e}")
        import traceback

        traceback.print_exc()
        return None


def simulate_user_query():
    """模拟用户查询场景"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ 未找到 DATABASE_URL")
        return

    print("🚀 模拟用户查询表信息")
    print("=" * 60)
    print("用户输入: '帮我获取一下表名为 activity_node 表的信息'")
    print("=" * 60)

    try:
        client = DatabaseClient(database_url)

        # 模拟解析用户输入，提取表名
        user_input = "帮我获取一下表名为 activity_node 表的信息"
        table_name = "activity_node"  # 从用户输入中提取的表名

        print(f"🤖 AI 解析: 用户想要查询表 '{table_name}' 的信息")
        print()

        # 获取表信息
        table_info = get_table_detailed_info(client, table_name)

        if table_info:
            print(f"\n✅ 已成功获取表 '{table_name}' 的完整信息!")

            # 额外提供一些分析
            print(f"\n📈 数据分析:")

            # 统计字段类型
            type_counts = {}
            for col in table_info.columns:
                col_type = str(col.type).split("(")[0]  # 去掉长度信息
                type_counts[col_type] = type_counts.get(col_type, 0) + 1

            print(f"  - 字段类型分布:")
            for col_type, count in sorted(type_counts.items()):
                print(f"    • {col_type}: {count} 个字段")

            # 统计可空字段
            nullable_count = sum(1 for col in table_info.columns if col.nullable)
            non_nullable_count = len(table_info.columns) - nullable_count
            print(f"  - 可空字段: {nullable_count} 个")
            print(f"  - 非空字段: {non_nullable_count} 个")

    except Exception as e:
        print(f"❌ 查询失败: {e}")
        import traceback

        traceback.print_exc()


def test_multiple_tables():
    """测试多个表的查询"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ 未找到 DATABASE_URL")
        return

    print("\n" + "=" * 80)
    print("🧪 测试多个表的查询功能")
    print("=" * 80)

    try:
        client = DatabaseClient(database_url)

        # 测试多个表
        test_tables = [
            "activity_node",
            "activity_task",
            "sys_role",
            "project",
            "da_logical_entity",
        ]

        for table_name in test_tables:
            print(f"\n{'=' * 20} 测试表: {table_name} {'=' * 20}")
            get_table_detailed_info(client, table_name)

    except Exception as e:
        print(f"❌ 测试失败: {e}")


def main():
    """主函数"""
    # 1. 模拟用户查询 activity_node 表
    simulate_user_query()

    # 2. 测试多个表的查询
    test_multiple_tables()


if __name__ == "__main__":
    main()
