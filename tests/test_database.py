"""数据库客户端测试"""

import pytest
from unittest.mock import Mock, patch
from sp_database_mcp.database import DatabaseClient
from sp_database_mcp.models import TableInfo, ColumnInfo


class TestDatabaseClient:
    """数据库客户端测试类"""
    
    @patch('sp_database_mcp.database.create_engine')
    def test_init_success(self, mock_create_engine):
        """测试成功初始化"""
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        client = DatabaseClient("sqlite:///test.db")
        assert client.database_url == "sqlite:///test.db"
        assert client.engine == mock_engine
    
    def test_init_no_url(self):
        """测试没有提供数据库 URL"""
        with pytest.raises(ValueError, match="DATABASE_URL is required"):
            DatabaseClient()
    
    @patch('sp_database_mcp.database.create_engine')
    @patch('sp_database_mcp.database.MetaData')
    @patch('sp_database_mcp.database.Table')
    def test_get_table_info(self, mock_table, mock_metadata, mock_create_engine):
        """测试获取表信息"""
        # Mock 设置
        mock_engine = Mock()
        mock_create_engine.return_value = mock_engine
        
        mock_column = Mock()
        mock_column.name = "id"
        mock_column.type = "INTEGER"
        mock_column.nullable = False
        mock_column.default = None
        mock_column.comment = "主键"
        mock_column.primary_key = True
        
        mock_table_instance = Mock()
        mock_table_instance.columns = [mock_column]
        mock_table_instance.foreign_keys = []
        mock_table_instance.indexes = []
        mock_table_instance.comment = "测试表"
        mock_table.return_value = mock_table_instance
        
        client = DatabaseClient("sqlite:///test.db")
        result = client.get_table_info("test_table")
        
        assert isinstance(result, TableInfo)
        assert result.name == "test_table"
        assert result.comment == "测试表"
        assert len(result.columns) == 1
        assert result.columns[0].name == "id"
        assert result.columns[0].is_primary_key == True
