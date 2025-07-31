#!/usr/bin/env python3
"""
测试 metabase 数据库连接和表结构查询
"""

import os
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import SQLAlchemyError


def test_database_connection():
    """测试数据库连接"""
    # 加载环境变量
    load_dotenv()

    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ 错误：未找到 DATABASE_URL 环境变量")
        return False

    print(f"🔗 连接字符串: {database_url}")

    try:
        # 创建数据库引擎
        engine = create_engine(database_url)

        # 测试连接
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ 数据库连接成功!")
            print(f"📊 PostgreSQL 版本: {version}")

            # 获取当前数据库名
            result = conn.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            print(f"🗄️  当前数据库: {db_name}")

            return True

    except SQLAlchemyError as e:
        print(f"❌ 数据库连接失败: {e}")
        return False


def list_schemas():
    """列出所有 schema"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    try:
        engine = create_engine(database_url)
        inspector = inspect(engine)

        schemas = inspector.get_schema_names()
        print(f"\n📁 数据库中的 Schema 列表:")
        for i, schema in enumerate(schemas, 1):
            print(f"  {i}. {schema}")

        return schemas

    except SQLAlchemyError as e:
        print(f"❌ 获取 schema 失败: {e}")
        return []


def list_tables_in_schema(schema_name="public"):
    """列出指定 schema 中的表"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    try:
        engine = create_engine(database_url)
        inspector = inspect(engine)

        tables = inspector.get_table_names(schema=schema_name)
        print(f"\n📋 Schema '{schema_name}' 中的表:")
        if not tables:
            print(f"  ⚠️  Schema '{schema_name}' 中没有表")
        else:
            for i, table in enumerate(tables, 1):
                print(f"  {i}. {table}")

        return tables

    except SQLAlchemyError as e:
        print(f"❌ 获取表列表失败: {e}")
        return []


def get_table_info(table_name, schema_name="public"):
    """获取表的详细信息"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    try:
        engine = create_engine(database_url)
        inspector = inspect(engine)

        # 获取列信息
        columns = inspector.get_columns(table_name, schema=schema_name)
        print(f"\n🔍 表 '{schema_name}.{table_name}' 的结构:")
        print("列名 | 类型 | 可空 | 默认值")
        print("-" * 50)

        for col in columns:
            nullable = "是" if col["nullable"] else "否"
            default = col.get("default", "None")
            print(f"{col['name']} | {col['type']} | {nullable} | {default}")

        # 获取主键信息
        pk = inspector.get_pk_constraint(table_name, schema=schema_name)
        if pk["constrained_columns"]:
            print(f"\n🔑 主键: {', '.join(pk['constrained_columns'])}")

        # 获取外键信息
        fks = inspector.get_foreign_keys(table_name, schema=schema_name)
        if fks:
            print(f"\n🔗 外键:")
            for fk in fks:
                print(
                    f"  {fk['constrained_columns']} -> {fk['referred_schema']}.{fk['referred_table']}.{fk['referred_columns']}"
                )

        return True

    except SQLAlchemyError as e:
        print(f"❌ 获取表信息失败: {e}")
        return False


def test_mcp_tools():
    """测试 MCP 工具功能"""
    print("\n🧪 测试 MCP 工具功能...")

    # 这里可以导入并测试你的 MCP 工具
    try:
        from sp_database_mcp.database_client import DatabaseClient

        load_dotenv()
        database_url = os.getenv("DATABASE_URL")

        client = DatabaseClient(database_url)

        # 测试获取所有表
        print("\n📊 使用 MCP 工具获取表列表:")
        tables_info = client.list_all_tables()
        print(tables_info)

        return True

    except Exception as e:
        print(f"❌ MCP 工具测试失败: {e}")
        return False


def main():
    """主测试函数"""
    print("🚀 开始测试 metabase 数据库连接...")
    print("=" * 60)

    # 1. 测试基本连接
    if not test_database_connection():
        print("\n❌ 数据库连接失败，请检查配置")
        sys.exit(1)

    # 2. 列出所有 schema
    schemas = list_schemas()

    # 3. 列出 public schema 中的表
    tables = list_tables_in_schema("public")

    # 4. 如果有表，获取第一个表的详细信息
    if tables:
        print(f"\n🔍 获取表 '{tables[0]}' 的详细信息:")
        get_table_info(tables[0])

    # 5. 测试 MCP 工具
    test_mcp_tools()

    print("\n✅ 测试完成!")


if __name__ == "__main__":
    main()
