#!/usr/bin/env python3
"""
交互式测试 metabase 数据库连接
"""

import os
import sys
import getpass
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.exc import SQLAlchemyError

def get_database_credentials():
    """获取数据库连接信息"""
    print("🔐 请输入数据库连接信息:")
    
    host = input("主机地址 (默认: 172.16.5.66): ").strip() or "172.16.5.66"
    port = input("端口 (默认: 5432): ").strip() or "5432"
    database = input("数据库名 (默认: metabase): ").strip() or "metabase"
    username = input("用户名 (默认: postgres): ").strip() or "postgres"
    password = getpass.getpass("密码: ")
    
    return f"postgresql://{username}:{password}@{host}:{port}/{database}"

def test_connection_with_url(database_url):
    """使用指定的连接字符串测试连接"""
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # 测试基本连接
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"✅ 数据库连接成功!")
            print(f"📊 PostgreSQL 版本: {version}")
            
            # 获取当前数据库名
            result = conn.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            print(f"🗄️  当前数据库: {db_name}")
            
            # 获取当前用户
            result = conn.execute(text("SELECT current_user"))
            user = result.fetchone()[0]
            print(f"👤 当前用户: {user}")
            
            return engine
            
    except SQLAlchemyError as e:
        print(f"❌ 数据库连接失败: {e}")
        return None

def explore_database(engine):
    """探索数据库结构"""
    inspector = inspect(engine)
    
    # 获取所有 schema
    schemas = inspector.get_schema_names()
    print(f"\n📁 数据库中的 Schema 列表 (共 {len(schemas)} 个):")
    for i, schema in enumerate(schemas, 1):
        print(f"  {i}. {schema}")
    
    # 重点关注 public schema
    print(f"\n🔍 探索 'public' schema:")
    tables = inspector.get_table_names(schema='public')
    
    if not tables:
        print("  ⚠️  public schema 中没有表")
    else:
        print(f"  📋 找到 {len(tables)} 个表:")
        for i, table in enumerate(tables, 1):
            print(f"    {i}. {table}")
            
        # 显示前几个表的结构
        print(f"\n📊 表结构详情 (显示前3个表):")
        for table in tables[:3]:
            show_table_structure(inspector, table, 'public')
    
    # 检查其他 schema 中的表
    for schema in schemas:
        if schema != 'public' and not schema.startswith('information_schema') and schema != 'pg_catalog':
            tables = inspector.get_table_names(schema=schema)
            if tables:
                print(f"\n📁 Schema '{schema}' 中的表 ({len(tables)} 个):")
                for table in tables[:5]:  # 只显示前5个
                    print(f"    - {table}")

def show_table_structure(inspector, table_name, schema_name='public'):
    """显示表结构"""
    try:
        columns = inspector.get_columns(table_name, schema=schema_name)
        print(f"\n  🔍 表: {schema_name}.{table_name}")
        print(f"     列数: {len(columns)}")
        
        # 显示前几个列
        for col in columns[:5]:
            nullable = "可空" if col['nullable'] else "非空"
            print(f"     - {col['name']}: {col['type']} ({nullable})")
        
        if len(columns) > 5:
            print(f"     ... 还有 {len(columns) - 5} 个列")
            
        # 获取主键
        pk = inspector.get_pk_constraint(table_name, schema=schema_name)
        if pk['constrained_columns']:
            print(f"     🔑 主键: {', '.join(pk['constrained_columns'])}")
            
    except Exception as e:
        print(f"     ❌ 获取表结构失败: {e}")

def save_connection_to_env(database_url):
    """保存连接信息到 .env 文件"""
    choice = input("\n💾 是否将此连接信息保存到 .env 文件? (y/n): ").strip().lower()
    if choice == 'y':
        try:
            # 读取现有的 .env 文件
            env_path = '/Users/alexliu/Project/sp-database-mcp/.env'
            lines = []
            
            if os.path.exists(env_path):
                with open(env_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
            
            # 更新 DATABASE_URL
            updated = False
            for i, line in enumerate(lines):
                if line.startswith('DATABASE_URL='):
                    lines[i] = f'DATABASE_URL={database_url}\n'
                    updated = True
                    break
            
            if not updated:
                lines.append(f'DATABASE_URL={database_url}\n')
            
            # 写回文件
            with open(env_path, 'w', encoding='utf-8') as f:
                f.writelines(lines)
                
            print(f"✅ 连接信息已保存到 {env_path}")
            
        except Exception as e:
            print(f"❌ 保存失败: {e}")

def main():
    """主函数"""
    print("🚀 Metabase 数据库连接测试工具")
    print("=" * 50)
    
    # 首先尝试从 .env 文件读取
    load_dotenv()
    env_url = os.getenv('DATABASE_URL')
    
    if env_url and env_url.startswith('postgresql://'):
        print(f"📄 从 .env 文件读取到连接信息")
        print(f"🔗 连接字符串: {env_url}")
        choice = input("是否使用此连接? (y/n): ").strip().lower()
        
        if choice == 'y':
            engine = test_connection_with_url(env_url)
            if engine:
                explore_database(engine)
                return
    
    # 交互式输入连接信息
    print("\n🔧 请手动输入连接信息:")
    database_url = get_database_credentials()
    
    engine = test_connection_with_url(database_url)
    if engine:
        explore_database(engine)
        save_connection_to_env(database_url)
    else:
        print("\n❌ 连接失败，请检查连接信息")

if __name__ == "__main__":
    main()
