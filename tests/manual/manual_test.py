#!/usr/bin/env python3
"""手动测试 MCP 服务器的脚本"""

import asyncio
import json
import subprocess
import sys
from pathlib import Path


async def test_mcp_server_manually():
    """手动测试 MCP 服务器"""
    print("🔧 手动测试 MCP 服务器...")

    # 启动服务器进程
    server_process = subprocess.Popen(
        [sys.executable, "-m", "sp_database_mcp.server"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd=Path(__file__).parent,
    )

    try:
        # 发送初始化请求
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"roots": {"listChanged": True}, "sampling": {}},
                "clientInfo": {"name": "test-client", "version": "1.0.0"},
            },
        }

        print("📤 发送初始化请求...")
        server_process.stdin.write(json.dumps(init_request) + "\n")
        server_process.stdin.flush()

        # 读取响应
        response_line = server_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(
                f"📥 初始化响应: {json.dumps(response, indent=2, ensure_ascii=False)}"
            )

        # 发送 tools/list 请求
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {},
        }

        print("\n📤 发送工具列表请求...")
        server_process.stdin.write(json.dumps(tools_request) + "\n")
        server_process.stdin.flush()

        # 读取响应
        response_line = server_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(
                f"📥 工具列表响应: {json.dumps(response, indent=2, ensure_ascii=False)}"
            )

        # 发送 tools/call 请求
        call_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "get_table_info",
                "arguments": {"table_name": "activities", "source": "database"},
            },
        }

        print("\n📤 发送工具调用请求...")
        server_process.stdin.write(json.dumps(call_request) + "\n")
        server_process.stdin.flush()

        # 读取响应
        response_line = server_process.stdout.readline()
        if response_line:
            response = json.loads(response_line.strip())
            print(
                f"📥 工具调用响应: {json.dumps(response, indent=2, ensure_ascii=False)}"
            )

    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
    finally:
        # 终止服务器进程
        server_process.terminate()
        server_process.wait()
        print("\n✅ 测试完成")


if __name__ == "__main__":
    asyncio.run(test_mcp_server_manually())
