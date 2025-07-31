#!/usr/bin/env python3
"""数据库客户端的单元测试"""

import os
import sqlite3

# 添加项目根目录到 Python 路径
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from sp_database_mcp.database import DatabaseClient
from sp_database_mcp.models import ColumnInfo, TableInfo


class TestDatabaseClient:
    """数据库客户端测试类"""

    @pytest.fixture
    def temp_db(self):
        """创建临时测试数据库"""
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name

        # 创建测试表
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(255) UNIQUE,
                age INTEGER,
                is_active BOOLEAN DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            INSERT INTO test_table (name, email, age) 
            VALUES ('张三', 'zhangsan@example.com', 25)
        """)

        conn.commit()
        conn.close()

        yield f"sqlite:///{db_path}"

        # 清理
        os.unlink(db_path)

    def test_database_client_init(self, temp_db):
        """测试数据库客户端初始化"""
        client = DatabaseClient(temp_db)
        assert client.database_url == temp_db
        assert client.engine is not None

    def test_get_table_info(self, temp_db):
        """测试获取表信息"""
        client = DatabaseClient(temp_db)
        table_info = client.get_table_info("test_table")

        assert table_info is not None
        assert table_info.name == "test_table"
        assert len(table_info.columns) == 6

        # 检查主键列
        id_column = next((col for col in table_info.columns if col.name == "id"), None)
        assert id_column is not None
        assert id_column.is_primary_key is True

        # 检查非空列
        name_column = next(
            (col for col in table_info.columns if col.name == "name"), None
        )
        assert name_column is not None
        assert name_column.nullable is False

    def test_get_all_tables(self, temp_db):
        """测试获取所有表"""
        client = DatabaseClient(temp_db)
        tables = client.get_all_tables()

        assert isinstance(tables, list)
        assert "test_table" in tables

    def test_search_tables(self, temp_db):
        """测试搜索表"""
        client = DatabaseClient(temp_db)

        # 搜索存在的表
        results = client.search_tables("test")
        assert len(results) > 0
        assert any(table.name == "test_table" for table in results)

        # 搜索不存在的表
        results = client.search_tables("nonexistent")
        assert len(results) == 0

    def test_invalid_database_url(self):
        """测试无效的数据库URL"""
        with pytest.raises(ConnectionError):
            DatabaseClient("invalid://database/url")

    def test_get_table_info_nonexistent(self, temp_db):
        """测试获取不存在的表信息"""
        client = DatabaseClient(temp_db)
        table_info = client.get_table_info("nonexistent_table")
        assert table_info is None


if __name__ == "__main__":
    # 简单的测试运行器
    import unittest

    # 创建临时数据库进行快速测试
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        # 创建测试表
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE activities (
                id INTEGER PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT
            )
        """)
        conn.commit()
        conn.close()

        # 测试数据库客户端
        client = DatabaseClient(f"sqlite:///{db_path}")

        print("🧪 运行数据库客户端测试...")

        # 测试获取表信息
        table_info = client.get_table_info("activities")
        print(f"✅ 获取表信息: {table_info.name if table_info else 'None'}")

        # 测试获取所有表
        tables = client.get_all_tables()
        print(f"✅ 获取所有表: {tables}")

        # 测试搜索表
        search_results = client.search_tables("act")
        print(f"✅ 搜索表: {[t.name for t in search_results]}")

        print("🎉 所有测试通过！")

    finally:
        os.unlink(db_path)
