#!/usr/bin/env python3
"""创建测试数据库和表"""

import sqlite3
import os

def create_test_database():
    """创建测试数据库和活动表"""
    db_path = "./test_database.db"
    
    # 如果数据库文件已存在，删除它
    if os.path.exists(db_path):
        os.remove(db_path)
    
    # 创建数据库连接
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # 创建活动表
    cursor.execute("""
        CREATE TABLE activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL,
            location VARCHAR(255),
            organizer VARCHAR(100) NOT NULL,
            max_participants INTEGER DEFAULT 0,
            current_participants INTEGER DEFAULT 0,
            status VARCHAR(20) DEFAULT 'active',
            category VARCHAR(50),
            price DECIMAL(10,2) DEFAULT 0.00,
            is_public BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 创建用户表
    cursor.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username VARCHAR(50) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            phone VARCHAR(20),
            avatar_url VARCHAR(255),
            is_active BOOLEAN DEFAULT 1,
            role VARCHAR(20) DEFAULT 'user',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # 创建活动参与表
    cursor.execute("""
        CREATE TABLE activity_participants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            activity_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            status VARCHAR(20) DEFAULT 'registered',
            registration_time DATETIME DEFAULT CURRENT_TIMESTAMP,
            notes TEXT,
            FOREIGN KEY (activity_id) REFERENCES activities(id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(activity_id, user_id)
        )
    """)
    
    # 插入一些测试数据
    cursor.execute("""
        INSERT INTO activities (title, description, start_time, end_time, location, organizer, max_participants, category, price)
        VALUES 
        ('Python 编程分享会', '分享 Python 编程技巧和最佳实践', '2024-02-01 14:00:00', '2024-02-01 17:00:00', '会议室A', '技术部', 50, '技术分享', 0.00),
        ('团队建设活动', '户外团队建设和拓展训练', '2024-02-05 09:00:00', '2024-02-05 18:00:00', '户外拓展基地', '人事部', 30, '团建', 200.00),
        ('产品发布会', '新产品功能介绍和演示', '2024-02-10 10:00:00', '2024-02-10 12:00:00', '大会议室', '产品部', 100, '产品', 0.00)
    """)
    
    cursor.execute("""
        INSERT INTO users (username, email, password_hash, full_name, phone, role)
        VALUES 
        ('admin', 'admin@example.com', 'hashed_password_123', '管理员', '13800138000', 'admin'),
        ('john_doe', 'john@example.com', 'hashed_password_456', '约翰·多伊', '13800138001', 'user'),
        ('jane_smith', 'jane@example.com', 'hashed_password_789', '简·史密斯', '13800138002', 'user')
    """)
    
    # 提交更改并关闭连接
    conn.commit()
    conn.close()
    
    print(f"测试数据库已创建: {db_path}")
    print("包含以下表:")
    print("- activities (活动表)")
    print("- users (用户表)")
    print("- activity_participants (活动参与表)")

if __name__ == "__main__":
    create_test_database()
