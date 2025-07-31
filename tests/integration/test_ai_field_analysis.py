#!/usr/bin/env python3
"""
使用 AI 分析字段的业务含义
利用大模型的分析能力来判断字段是否为系统字段
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


def analyze_field_with_ai(
    field_name, field_type, field_comment=None, table_name=None, table_comment=None
):
    """
    使用 AI 分析字段是否为系统字段
    这里模拟 AI 分析过程，实际应用中可以调用大模型 API
    """

    # 构建分析上下文
    context = {
        "field_name": field_name,
        "field_type": str(field_type),
        "field_comment": field_comment,
        "table_name": table_name,
        "table_comment": table_comment,
    }

    # 模拟 AI 分析提示词
    analysis_prompt = f"""
    请分析以下数据库字段是否为系统字段：
    
    表名: {table_name}
    表描述: {table_comment}
    字段名: {field_name}
    字段类型: {field_type}
    字段注释: {field_comment}
    
    系统字段通常包括：
    1. 审计字段：创建时间、更新时间、删除时间、操作人等
    2. 版本控制：版本号、系统事件等
    3. 软删除：删除标记、删除状态等
    4. 权限控制：组织代码、访问权限等
    5. 技术实现：数据源、应用归属等
    6. 生效控制：生效时间、生效状态等
    
    业务字段通常包括：
    1. 核心业务标识：业务ID、编码、名称等
    2. 业务属性：状态、类型、描述等
    3. 业务关系：关联ID、父子关系等
    4. 业务数据：金额、数量、配置等
    
    请判断该字段是 "系统字段" 还是 "业务字段"，并给出理由。
    """

    # 这里模拟 AI 分析结果
    # 实际应用中，这里应该调用大模型 API 进行分析
    ai_analysis = simulate_ai_analysis(context)

    return ai_analysis


def simulate_ai_analysis(context):
    """
    模拟 AI 分析结果
    实际应用中应该替换为真实的大模型调用
    """
    field_name = context["field_name"].lower()
    field_type = context["field_type"].lower()

    # 模拟 AI 的智能分析逻辑
    analysis_result = {
        "is_system_field": False,
        "confidence": 0.0,
        "reasoning": "",
        "category": "business",
    }

    # 高置信度的系统字段
    high_confidence_system_patterns = [
        ("created_at", "timestamp", "创建时间戳，用于审计"),
        ("updated_at", "timestamp", "更新时间戳，用于审计"),
        ("deleted_at", "timestamp", "删除时间戳，用于软删除"),
        ("created_by", "varchar", "创建人，用于审计"),
        ("updated_by", "varchar", "更新人，用于审计"),
        ("deleted_by", "varchar", "删除人，用于审计"),
        ("is_deleted", "boolean", "删除标记，用于软删除"),
        ("del_flag", "integer", "删除标志，用于软删除"),
        ("system_version", "bigint", "系统版本号，用于版本控制"),
        ("system_event", "varchar", "系统事件，用于审计"),
        ("data_source", "varchar", "数据源标识，用于技术实现"),
        ("corp_id", "varchar", "公司ID，用于多租户"),
        ("owner_org_code", "varchar", "所属组织代码，用于权限控制"),
        ("app_belong", "varchar", "应用归属，用于技术实现"),
        ("access_modifier", "varchar", "访问修饰符，用于权限控制"),
        ("latest", "boolean", "最新标记，用于版本控制"),
        ("effective_start_time", "timestamp", "生效开始时间，用于生效控制"),
        ("effective_end_time", "timestamp", "生效结束时间，用于生效控制"),
        ("effective_status", "boolean", "生效状态，用于生效控制"),
        ("effective_condition", "text", "生效条件，用于生效控制"),
    ]

    # 检查是否匹配高置信度系统字段
    for pattern_name, pattern_type, reasoning in high_confidence_system_patterns:
        if pattern_name in field_name and pattern_type in field_type:
            analysis_result.update(
                {
                    "is_system_field": True,
                    "confidence": 0.95,
                    "reasoning": reasoning,
                    "category": "system_audit"
                    if "audit" in reasoning
                    else "system_technical",
                }
            )
            return analysis_result

    # 中等置信度的系统字段模式
    medium_confidence_patterns = [
        ("version", "版本相关字段，通常用于系统版本控制"),
        ("flag", "标记字段，可能用于系统状态控制"),
        ("source", "来源字段，通常用于数据源标识"),
        ("modifier", "修饰符字段，通常用于权限或访问控制"),
        ("event", "事件字段，通常用于系统审计"),
    ]

    for pattern, reasoning in medium_confidence_patterns:
        if pattern in field_name:
            analysis_result.update(
                {
                    "is_system_field": True,
                    "confidence": 0.75,
                    "reasoning": reasoning,
                    "category": "system_control",
                }
            )
            return analysis_result

    # 高置信度的业务字段
    high_confidence_business_patterns = [
        ("name", "名称字段，核心业务属性"),
        ("code", "编码字段，业务标识"),
        ("type", "类型字段，业务分类"),
        ("status", "状态字段，业务状态"),
        ("description", "描述字段，业务说明"),
        ("sequence", "序号字段，业务排序"),
        ("amount", "金额字段，业务数据"),
        ("quantity", "数量字段，业务数据"),
        ("price", "价格字段，业务数据"),
        ("id", "标识字段，业务主键"),
    ]

    for pattern, reasoning in high_confidence_business_patterns:
        if pattern in field_name and not any(
            sys_pattern in field_name
            for sys_pattern, _, _ in high_confidence_system_patterns
        ):
            analysis_result.update(
                {
                    "is_system_field": False,
                    "confidence": 0.90,
                    "reasoning": reasoning,
                    "category": "business_core",
                }
            )
            return analysis_result

    # 默认分析：如果包含业务相关的表名或者是主键
    if context["table_name"] and context["table_name"].lower() in field_name:
        analysis_result.update(
            {
                "is_system_field": False,
                "confidence": 0.80,
                "reasoning": f"字段名包含表名 {context['table_name']}，可能是业务关联字段",
                "category": "business_relation",
            }
        )
        return analysis_result

    # 默认为业务字段（低置信度）
    analysis_result.update(
        {
            "is_system_field": False,
            "confidence": 0.60,
            "reasoning": "无明确系统字段特征，推测为业务字段",
            "category": "business_unknown",
        }
    )

    return analysis_result


def get_ai_analyzed_table_info(
    client, table_name, show_system_fields=False, confidence_threshold=0.7
):
    """使用 AI 分析获取表的字段分类信息"""
    print(f"🤖 使用 AI 分析表 '{table_name}' 的字段分类...")
    print("=" * 70)

    try:
        table_info = client.get_table_info(table_name)

        if not table_info:
            print(f"❌ 未找到表 '{table_name}'")
            return None

        # 使用 AI 分析每个字段
        business_fields = []
        system_fields = []
        uncertain_fields = []

        print(f"🔍 AI 正在分析 {len(table_info.columns)} 个字段...")

        for col in table_info.columns:
            # 使用 AI 分析字段
            ai_result = analyze_field_with_ai(
                field_name=col.name,
                field_type=col.type,
                field_comment=col.comment,
                table_name=table_info.name,
                table_comment=table_info.comment,
            )

            # 根据 AI 分析结果和置信度分类
            if ai_result["confidence"] >= confidence_threshold:
                if ai_result["is_system_field"]:
                    system_fields.append((col, ai_result))
                else:
                    business_fields.append((col, ai_result))
            else:
                uncertain_fields.append((col, ai_result))

        # 显示分析结果
        print(f"\n📋 表名: {table_info.name}")
        if table_info.comment:
            print(f"📝 表描述: {table_info.comment}")

        print(f"\n🤖 AI 分析结果:")
        print(f"  - 总字段数: {len(table_info.columns)}")
        print(
            f"  - 业务字段: {len(business_fields)} 个 (置信度 ≥ {confidence_threshold})"
        )
        print(
            f"  - 系统字段: {len(system_fields)} 个 (置信度 ≥ {confidence_threshold})"
        )
        print(
            f"  - 不确定字段: {len(uncertain_fields)} 个 (置信度 < {confidence_threshold})"
        )

        # 显示业务字段
        if business_fields:
            print(f"\n🎯 AI 识别的业务字段:")
            print("-" * 80)
            print("字段名 | 数据类型 | 置信度 | AI 分析理由")
            print("-" * 80)

            for col, ai_result in business_fields:
                confidence_str = f"{ai_result['confidence']:.2f}"
                reasoning = (
                    ai_result["reasoning"][:40] + "..."
                    if len(ai_result["reasoning"]) > 40
                    else ai_result["reasoning"]
                )
                print(
                    f"{col.name:<20} | {str(col.type):<12} | {confidence_str:<6} | {reasoning}"
                )

        # 显示系统字段（如果需要）
        if show_system_fields and system_fields:
            print(f"\n🔧 AI 识别的系统字段:")
            print("-" * 80)
            print("字段名 | 数据类型 | 置信度 | AI 分析理由")
            print("-" * 80)

            for col, ai_result in system_fields:
                confidence_str = f"{ai_result['confidence']:.2f}"
                reasoning = (
                    ai_result["reasoning"][:40] + "..."
                    if len(ai_result["reasoning"]) > 40
                    else ai_result["reasoning"]
                )
                print(
                    f"{col.name:<20} | {str(col.type):<12} | {confidence_str:<6} | {reasoning}"
                )

        # 显示不确定字段
        if uncertain_fields:
            print(f"\n❓ AI 不确定的字段 (需要人工确认):")
            print("-" * 80)
            print("字段名 | 数据类型 | 置信度 | AI 分析理由")
            print("-" * 80)

            for col, ai_result in uncertain_fields:
                confidence_str = f"{ai_result['confidence']:.2f}"
                reasoning = (
                    ai_result["reasoning"][:40] + "..."
                    if len(ai_result["reasoning"]) > 40
                    else ai_result["reasoning"]
                )
                field_type = "系统" if ai_result["is_system_field"] else "业务"
                print(
                    f"{col.name:<20} | {str(col.type):<12} | {confidence_str:<6} | {field_type}: {reasoning}"
                )

        return {
            "table_info": table_info,
            "business_fields": [col for col, _ in business_fields],
            "system_fields": [col for col, _ in system_fields],
            "uncertain_fields": [col for col, _ in uncertain_fields],
            "ai_analysis": {
                "business_analysis": [ai_result for _, ai_result in business_fields],
                "system_analysis": [ai_result for _, ai_result in system_fields],
                "uncertain_analysis": [ai_result for _, ai_result in uncertain_fields],
            },
        }

    except Exception as e:
        print(f"❌ AI 分析失败: {e}")
        import traceback

        traceback.print_exc()
        return None


def simulate_user_ai_query():
    """模拟用户使用 AI 分析查询"""
    load_dotenv()
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("❌ 未找到 DATABASE_URL")
        return

    print("🚀 AI 驱动的字段分析")
    print("=" * 70)
    print("用户输入: '查询 activity_node 表信息，使用 AI 分析哪些是业务字段'")
    print("=" * 70)

    try:
        client = DatabaseClient(database_url)

        # 使用 AI 分析表字段
        result = get_ai_analyzed_table_info(
            client,
            "activity_node",
            show_system_fields=True,  # 显示系统字段用于对比
            confidence_threshold=0.7,
        )

        if result:
            print(f"\n✅ AI 分析完成!")

            business_count = len(result["business_fields"])
            system_count = len(result["system_fields"])
            uncertain_count = len(result["uncertain_fields"])

            print(f"\n📊 AI 分析总结:")
            print(f"  - 高置信度业务字段: {business_count} 个")
            print(f"  - 高置信度系统字段: {system_count} 个")
            print(f"  - 需要人工确认: {uncertain_count} 个")

            # 显示 AI 的分析类别统计
            all_analysis = (
                result["ai_analysis"]["business_analysis"]
                + result["ai_analysis"]["system_analysis"]
                + result["ai_analysis"]["uncertain_analysis"]
            )

            category_counts = {}
            for analysis in all_analysis:
                category = analysis["category"]
                category_counts[category] = category_counts.get(category, 0) + 1

            print(f"\n🏷️  AI 识别的字段类别:")
            for category, count in sorted(category_counts.items()):
                print(f"  - {category}: {count} 个字段")

    except Exception as e:
        print(f"❌ AI 分析失败: {e}")


def main():
    """主函数"""
    simulate_user_ai_query()


if __name__ == "__main__":
    main()
