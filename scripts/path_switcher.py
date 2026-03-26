#!/usr/bin/env python3
"""
路径切换策略推荐工具
根据问题类型推荐完全不同的解决方案路径
"""

import json
from dataclasses import dataclass
from typing import List, Dict, Optional
import sys

@dataclass
class ProblemType:
    """问题类型定义"""
    name: str
    description: str
    typical_symptoms: List[str]
    
@dataclass
class SwitchPath:
    """换路策略定义"""
    name: str
    description: str
    implementation: str
    pros: List[str]
    cons: List[str]
    effort_level: int  # 1-5，5表示投入最大

# 定义常见问题类型
PROBLEM_TYPES = [
    ProblemType(
        name="环境配置问题",
        description="Python/Node版本、依赖包、系统配置等环境相关的问题",
        typical_symptoms=[
            "命令不存在",
            "模块未找到", 
            "版本不兼容",
            "权限被拒绝",
            "路径错误"
        ]
    ),
    ProblemType(
        name="技术方案错误",
        description="技术选型、架构设计、实现思路等方案层面的问题",
        typical_symptoms=[
            "逻辑死循环",
            "性能极差",
            "架构无法扩展",
            "代码复杂度爆炸",
            "频繁崩溃"
        ]
    ),
    ProblemType(
        name="外部依赖问题",
        description="API、数据库、第三方服务等外部依赖的问题",
        typical_symptoms=[
            "API返回404/403",
            "数据库连接失败",
            "网络超时",
            "服务不可用",
            "数据格式不匹配"
        ]
    ),
    ProblemType(
        name="资源限制问题",
        description="内存、存储、网络、时间等系统资源限制",
        typical_symptoms=[
            "内存不足",
            "磁盘空间满",
            "CPU占用100%",
            "网络超时",
            "执行时间过长"
        ]
    ),
    ProblemType(
        name="理解偏差问题",
        description="需求误解、目标错位、期望差异等理解层面的问题",
        typical_symptoms=[
            "用户说不是这个意思",
            "需求中途变更",
            "目标不明确",
            "期望不一致",
            "验收标准模糊"
        ]
    )
]

# 定义换路策略库
SWITCH_STRATEGIES: Dict[str, List[SwitchPath]] = {
    "环境配置问题": [
        SwitchPath(
            name="更换执行环境",
            description="使用独立的虚拟环境或容器，隔离系统环境",
            implementation="使用venv/conda创建独立Python环境，或使用Docker容器",
            pros=["环境干净", "可重复", "不影响系统"],
            cons=["需要额外配置", "可能增加复杂度"],
            effort_level=2
        ),
        SwitchPath(
            name="更换技术栈",
            description="完全换用不同的技术栈避开环境问题",
            implementation="如Python有问题换Node.js，matplotlib有问题换自定义SVG",
            pros=["彻底避开问题", "可能更简单"],
            cons=["需要学习新工具", "可能不是最优方案"],
            effort_level=3
        ),
        SwitchPath(
            name="使用预配置环境",
            description="使用云服务或预配置好的环境",
            implementation="如Google Colab、Replit、CodeSandbox等在线环境",
            pros=["零配置", "跨平台", "资源充足"],
            cons=["需要网络", "可能有使用限制"],
            effort_level=1
        )
    ],
    "技术方案错误": [
        SwitchPath(
            name="更换实现算法",
            description="换用完全不同的算法或设计模式",
            implementation="如递归换迭代，同步换异步，集中式换分布式",
            pros=["可能解决根本问题", "性能可能更好"],
            cons=["需要重新设计", "风险较高"],
            effort_level=4
        ),
        SwitchPath(
            name="简化问题范围",
            description="缩小问题范围，先解决核心子问题",
            implementation="如先实现基础功能，再扩展；先处理小数据集，再扩展",
            pros=["降低复杂度", "快速验证"],
            cons["功能可能不完整"],
            effort_level=2
        ),
        SwitchPath(
            name="寻找成熟轮子",
            description="使用成熟的第三方库或框架，避免重复造轮子",
            implementation="搜索GitHub、PyPI、npm寻找成熟解决方案",
            pros=["节省时间", "经过验证"],
            cons=["依赖第三方", "可能不完全符合需求"],
            effort_level=2
        )
    ],
    "外部依赖问题": [
        SwitchPath(
            name="更换数据来源",
            description="换用不同的API、数据库或数据文件",
            implementation="如API不可用换模拟数据，数据库不可用换CSV文件",
            pros=["快速解决阻塞", "可控制"],
            cons=["数据可能不一致", "需要适配"],
            effort_level=2
        ),
        SwitchPath(
            name="实现缓存或降级",
            description="缓存数据或提供降级方案",
            implementation="如缓存API响应，API失败时使用上次缓存",
            pros=["提高可用性", "用户体验好"],
            cons=["数据可能过时", "增加复杂度"],
            effort_level=3
        ),
        SwitchPath(
            name="手动干预方案",
            description="提供人工处理的后备方案",
            implementation="如API失败时生成数据模板让用户手动填写",
            pros=["保证任务完成", "简单可靠"],
            cons=["需要人工", "效率低"],
            effort_level=1
        )
    ],
    "资源限制问题": [
        SwitchPath(
            name="优化资源使用",
            description="优化算法或数据结构减少资源占用",
            implementation="如使用生成器代替列表，使用索引优化查询",
            pros=["解决根本问题", "性能提升"],
            cons=["需要技术能力", "可能复杂"],
            effort_level=4
        ),
        SwitchPath(
            name="分批处理",
            description="将大任务分解为小批次处理",
            implementation="如分批读取大文件，分批处理数据",
            pros=["避免资源溢出", "可恢复性"],
            cons=["需要额外逻辑", "可能慢"],
            effort_level=2
        ),
        SwitchPath(
            name="使用外部资源",
            description="利用云服务或外部资源",
            implementation="如使用云函数、云数据库、CDN等",
            pros=["资源充足", "弹性扩展"],
            cons=["可能有成本", "需要网络"],
            effort_level=3
        )
    ],
    "理解偏差问题": [
        SwitchPath(
            name="重新确认需求",
            description="与用户重新沟通，明确需求和期望",
            implementation="使用具体示例、原型、图表等方式澄清",
            pros=["解决根本问题", "避免返工"],
            cons=["需要沟通时间", "可能影响进度"],
            effort_level=1
        ),
        SwitchPath(
            name="快速原型验证",
            description="快速制作原型让用户确认",
            implementation="创建最小可行产品(MVP)验证核心功能",
            pros=["直观明了", "减少误解"],
            cons["需要额外时间"],
            effort_level=2
        ),
        SwitchPath(
            name="分阶段交付",
            description="分阶段交付，每阶段确认",
            implementation="将大任务分解，每完成一部分就确认",
            pros=["及时纠偏", "风险可控"],
            cons=["增加沟通成本", "可能影响效率"],
            effort_level=2
        )
    ]
}

def diagnose_problem_type(description: str, symptoms: List[str]) -> Optional[ProblemType]:
    """根据描述和症状诊断问题类型"""
    description_lower = description.lower()
    symptoms_lower = [s.lower() for s in symptoms]
    
    scores = []
    for problem_type in PROBLEM_TYPES:
        score = 0
        
        # 检查描述中的关键词
        for symptom in problem_type.typical_symptoms:
            if symptom.lower() in description_lower:
                score += 2
        
        # 检查提供的症状
        for symptom in symptoms_lower:
            for typical_symptom in problem_type.typical_symptoms:
                if typical_symptom.lower() in symptom:
                    score += 3
        
        # 问题类型名称匹配
        if problem_type.name.lower() in description_lower:
            score += 5
            
        scores.append((problem_type, score))
    
    # 按分数排序
    scores.sort(key=lambda x: x[1], reverse=True)
    
    if scores and scores[0][1] > 0:
        return scores[0][0]
    return None

def recommend_switch_paths(problem_type: ProblemType, max_recommendations: int = 3) -> List[SwitchPath]:
    """推荐换路策略"""
    if problem_type.name not in SWITCH_STRATEGIES:
        return []
    
    strategies = SWITCH_STRATEGIES[problem_type.name]
    
    # 按投入水平排序（推荐从低投入开始）
    strategies.sort(key=lambda x: x.effort_level)
    
    return strategies[:max_recommendations]

def generate_switch_plan(problem_description: str, attempted_solutions: List[str]) -> Dict:
    """生成完整的换路计划"""
    print("=" * 70)
    print("遇卡换路 - 路径切换策略生成器")
    print("=" * 70)
    
    # 步骤1：诊断问题类型
    print("\n🔍 步骤1：分析问题类型")
    print("-" * 40)
    
    # 从尝试的解决方案中提取症状
    symptoms = []
    for attempt in attempted_solutions:
        if "失败" in attempt or "错误" in attempt or "卡住" in attempt:
            symptoms.append(attempt)
    
    problem_type = diagnose_problem_type(problem_description, symptoms)
    
    if problem_type:
        print(f"✓ 诊断结果: {problem_type.name}")
        print(f"  描述: {problem_type.description}")
        
        if symptoms:
            print(f"  匹配的症状: {', '.join(symptoms[:3])}")
    else:
        print("⚠️  无法准确诊断问题类型")
        print("  可能原因: 问题描述不清晰或症状不典型")
        problem_type = ProblemType("未知问题类型", "需要进一步分析", [])
    
    # 步骤2：推荐换路策略
    print("\n🔄 步骤2：推荐换路策略")
    print("-" * 40)
    
    recommended_paths = recommend_switch_paths(problem_type)
    
    if not recommended_paths:
        print("⚠️  没有找到针对性的换路策略")
        print("  建议: 重新分析问题或寻求人工帮助")
        return {}
    
    print(f"推荐 {len(recommended_paths)} 条换路策略（按投入从小到大）:")
    
    for i, path in enumerate(recommended_paths, 1):
        print(f"\n{i}. {path.name}")
        print(f"  描述: {path.description}")
        print(f"  实现方式: {path.implementation}")
        print(f"  优点: {', '.join(path.pros)}")
        print(f"  缺点: {', '.join(path.cons)}")
        print(f"  投入水平: {'⭐' * path.effort_level} ({path.effort_level}/5)")
    
    # 步骤3：生成行动建议
    print("\n🎯 步骤3：行动建议")
    print("-" * 40)
    
    if recommended_paths:
        best_path = recommended_paths[0]  # 投入最小的
        
        print(f"推荐优先尝试: {best_path.name}")
        print(f"理由: 投入最小 ({best_path.effort_level}/5)，快速验证可行性")
        print()
        print("具体行动步骤:")
        print(f"1. 停止当前方向: 不再尝试已失败的方法")
        print(f"2. 准备新环境: {best_path.implementation.split('，')[0]}")
        print(f"3. 验证可行性: 用最小代码验证新方案")
        print(f"4. 评估结果: 检查是否解决了核心问题")
        print(f"5. 再卡再换: 如果新方案也卡住，尝试下一条路径")
    
    # 返回结构化结果
    result = {
        "problem_type": problem_type.name if problem_type else "未知",
        "diagnosis": problem_type.description if problem_type else "",
        "recommended_paths": [
            {
                "name": p.name,
                "description": p.description,
                "implementation": p.implementation,
                "effort_level": p.effort_level,
                "pros": p.pros,
                "cons": p.cons
            }
            for p in recommended_paths
        ],
        "best_path": recommended_paths[0].name if recommended_paths else None,
        "action_steps": [
            "停止当前方向，不再尝试已失败的方法",
            f"准备新环境: {recommended_paths[0].implementation.split('，')[0]}" if recommended_paths else "",
            "用最小代码验证新方案可行性",
            "评估是否解决了核心问题",
            "再卡再换: 新方案也卡住就尝试下一条路径"
        ]
    }
    
    return result

def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print("用法: python path_switcher.py '问题描述' [尝试过的解决方案1] [解决方案2] ...")
        print("示例: python path_switcher.py 'Python matplotlib中文字体显示乱码' '尝试rcParams配置字体' '安装额外字体包失败'")
        return
    
    problem_description = sys.argv[1]
    attempted_solutions = sys.argv[2:] if len(sys.argv) > 2 else []
    
    print(f"问题描述: {problem_description}")
    if attempted_solutions:
        print(f"已尝试: {', '.join(attempted_solutions)}")
    
    result = generate_switch_plan(problem_description, attempted_solutions)
    
    # 保存结果到文件（可选）
    if result:
        with open("switch_path_recommendation.json", "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"\n✓ 换路计划已保存到: switch_path_recommendation.json")

if __name__ == "__main__":
    main()