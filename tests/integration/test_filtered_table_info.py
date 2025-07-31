#!/usr/bin/env python3
"""
模拟用户查询表信息时过滤系统字段的功能
场景：用户输入 "查询 activity_node 表信息，只展示非系统字段"
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


def is_system_field(column_name):
    """判断是否为系统字段"""
    # 定义常见的系统字段模式
    system_field_patterns = [
        # 时间相关
        "created_at",
        "updated_at",
        "deleted_at",
        "create_time",
        "update_time",
        "delete_time",
        "created_time",
        "updated_time",
        "deleted_time",
        # 操作人相关
        "created_by",
        "updated_by",
        "deleted_by",
        "create_user",
        "update_user",
        "delete_user",
        "creator",
        "updater",
        "deleter",
        # 删除标记
        "is_deleted",
        "del_flag",
        "delete_flag",
        "deleted",
        "is_delete",
        # 版本控制
        "system_version",
        "version",
        "revision",
        # 系统事件
        "system_event",
        "event_type",
        # 数据源
        "data_source",
        "source",
        # 生效相关
        "effective_start_time",
        "effective_end_time",
        "effective_status",
        "effective_condition",
        "effective_condition_status",
        # 组织相关（可能是系统级别）
        "owner_org_code",
        "corp_id",
        # 其他系统字段
        "latest",
        "app_belong",
        "access_modifier",
    ]

    column_lower = column_name.lower()

    # 检查是否匹配系统字段模式
    for pattern in system_field_patterns:
        if pattern.lower() in column_lower:
            return True

    return False


def get_business_fields_info(client, table_name, show_system_fields=False):
    """获取表的业务字段信息（过滤系统字段）"""
    print(
        f"🔍 正在获取表 '{table_name}' 的{'所有' if show_system_fields else '业务'}字段信息..."
    )
    print("=" * 70)

    try:
        table_info = client.get_table_info(table_name)

        if not table_info:
            print(f"❌ 未找到表 '{table_name}'")
            return None

        # 分类字段
        business_fields = []
        system_fields = []

        for col in table_info.columns:
            if is_system_field(col.name):
                system_fields.append(col)
            else:
                business_fields.append(col)

        # 显示表的基本信息
        print(f"📋 表名: {table_info.name}")
        if table_info.comment:
            print(f"📝 表描述: {table_info.comment}")

        print(f"📊 字段统计:")
        print(f"  - 总字段数: {len(table_info.columns)}")
        print(f"  - 业务字段: {len(business_fields)}")
        print(f"  - 系统字段: {len(system_fields)}")

        # 显示业务字段
        if business_fields:
            print(f"\n🎯 业务字段详细信息 ({len(business_fields)} 个):")
            print("-" * 60)
            print("字段名 | 数据类型 | 是否可空 | 是否主键 | 默认值")
            print("-" * 60)

            for col in business_fields:
                nullable = "是" if col.nullable else "否"
                is_pk = "是" if col.is_primary_key else "否"
                default_val = col.default if col.default else "无"

                print(
                    f"{col.name:<25} | {str(col.type):<15} | {nullable:<8} | {is_pk:<8} | {default_val}"
                )
        else:
            print(f"\n⚠️  未找到业务字段（所有字段都被识别为系统字段）")

        # 如果用户要求显示系统字段，则显示
        if show_system_fields and system_fields:
            print(f"\n🔧 系统字段详细信息 ({len(system_fields)} 个):")
            print("-" * 60)
            print("字段名 | 数据类型 | 是否可空 | 是否主键 | 默认值")
            print("-" * 60)

            for col in system_fields:
                nullable = "是" if col.nullable else "否"
                is_pk = "是" if col.is_primary_key else "否"
                default_val = col.default if col.default else "无"

                print(
                    f"{col.name:<25} | {str(col.type):<15} | {nullable:<8} | {is_pk:<8} | {default_val}"
                )

        # 显示主键信息（只显示业务主键）
        business_primary_keys = [
            col.name for col in business_fields if col.is_primary_key
        ]
        system_primary_keys = [col.name for col in system_fields if col.is_primary_key]

        if business_primary_keys:
            print(f"\n🔑 业务主键: {', '.join(business_primary_keys)}")
        if system_primary_keys:
            print(f"🔧 系统主键: {', '.join(system_primary_keys)}")

        # 显示外键关系（只显示业务相关的）
        if table_info.foreign_keys:
            business_fks = [
                fk
                for fk in table_info.foreign_keys
                if not is_system_field(fk["column"])
            ]
            if business_fks:
                print(f"\n🔗 业务外键关系:")
                for fk in business_fks:
                    print(
                        f"  - {fk['column']} → {fk['referenced_table']}.{fk['referenced_column']}"
                    )

        # 提供业务分析
        print(f"\n💡 业务字段分析:")
        if business_fields:
            # 分析业务字段类型
            business_type_counts = {}
            for col in business_fields:
                col_type = str(col.type).split("(")[0]
                business_type_counts[col_type] = (
                    business_type_counts.get(col_type, 0) + 1
                )

            print(f"  - 业务字段类型分布:")
            for col_type, count in sorted(business_type_counts.items()):
                print(f"    • {col_type}: {count} 个字段")

            # 分析可空性
            nullable_business = sum(1 for col in business_fields if col.nullable)
            print(f"  - 可空业务字段: {nullable_business} 个")
            print(f"  - 必填业务字段: {len(business_fields) - nullable_business} 个")

        return {
            "table_info": table_info,
            "business_fields": business_fields,
            "system_fields": system_fields,
        }

    except Exception as e:
        print(f"❌ 获取表信息时出错: {e}")
        import traceback

        traceback.print_exc()
        return None


def simulate_filtered_query():
    """模拟用户查询过滤后的表信息"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ 未找到 DATABASE_URL")
        return

    print("🚀 模拟用户查询过滤表信息")
    print("=" * 70)
    print("用户输入: '查询 activity_node 表信息，只展示非系统字段'")
    print("=" * 70)

    try:
        client = DatabaseClient(database_url)

        # 模拟解析用户输入
        table_name = "activity_node"
        show_only_business = True  # 用户要求只显示非系统字段

        print(f"🤖 AI 解析: 用户想要查询表 '{table_name}' 的业务字段信息")
        print()

        # 获取过滤后的表信息
        result = get_business_fields_info(client, table_name, show_system_fields=False)

        if result:
            print(f"\n✅ 已成功获取表 '{table_name}' 的业务字段信息!")

            business_fields = result["business_fields"]
            system_fields = result["system_fields"]

            print(f"\n📈 过滤结果:")
            print(f"  - 隐藏了 {len(system_fields)} 个系统字段")
            print(f"  - 展示了 {len(business_fields)} 个业务字段")

            if system_fields:
                print(f"\n🔧 被过滤的系统字段:")
                system_field_names = [col.name for col in system_fields]
                # 按行显示，每行5个
                for i in range(0, len(system_field_names), 5):
                    line_fields = system_field_names[i : i + 5]
                    print(f"    {', '.join(line_fields)}")

    except Exception as e:
        print(f"❌ 查询失败: {e}")
        import traceback

        traceback.print_exc()


def test_multiple_tables_filtered():
    """测试多个表的过滤查询"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ 未找到 DATABASE_URL")
        return

    print("\n" + "=" * 80)
    print("🧪 测试多个表的业务字段过滤功能")
    print("=" * 80)

    try:
        client = DatabaseClient(database_url)

        # 测试多个表
        test_tables = ["activity_task", "sys_role", "project", "da_logical_entity"]

        for table_name in test_tables:
            print(f"\n{'=' * 25} 测试表: {table_name} {'=' * 25}")
            result = get_business_fields_info(
                client, table_name, show_system_fields=False
            )

            if result:
                business_count = len(result["business_fields"])
                system_count = len(result["system_fields"])
                print(
                    f"📊 过滤效果: 业务字段 {business_count} 个，系统字段 {system_count} 个"
                )

    except Exception as e:
        print(f"❌ 测试失败: {e}")


def main():
    """主函数"""
    # 1. 模拟用户查询 activity_node 表的业务字段
    simulate_filtered_query()

    # 2. 测试多个表的过滤功能
    test_multiple_tables_filtered()


if __name__ == "__main__":
    main()
