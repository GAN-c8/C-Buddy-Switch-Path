#!/usr/bin/env python3
"""
环境诊断工具 - 快速检查系统环境状态
用于"遇卡换路"流程中的"析"步骤，判断是否是环境问题
"""

import sys
import subprocess
import platform
import os
from pathlib import Path

def check_python_environment():
    """检查Python环境"""
    print("=" * 60)
    print("Python环境诊断")
    print("=" * 60)
    
    checks = []
    
    # Python版本
    python_version = platform.python_version()
    checks.append(f"✓ Python版本: {python_version}")
    
    # Python路径
    python_path = sys.executable
    checks.append(f"✓ Python路径: {python_path}")
    
    # 检查常见问题Python路径
    if "Microsoft\\WindowsApps" in python_path:
        checks.append("⚠️  警告: Python路径指向Microsoft Store版本（可能有问题）")
    
    # 检查pip可用性
    try:
        pip_version = subprocess.check_output([python_path, "-m", "pip", "--version"], 
                                            stderr=subprocess.STDOUT, text=True)
        checks.append(f"✓ pip可用: {pip_version.split()[1]}")
    except Exception as e:
        checks.append(f"✗ pip不可用: {str(e)}")
    
    # 检查关键库
    key_packages = ["matplotlib", "pandas", "numpy", "requests", "openpyxl", "python-docx"]
    try:
        installed = subprocess.check_output([python_path, "-m", "pip", "list"], 
                                          stderr=subprocess.STDOUT, text=True)
        for pkg in key_packages:
            if pkg in installed:
                checks.append(f"✓ {pkg}: 已安装")
            else:
                checks.append(f"✗ {pkg}: 未安装")
    except Exception as e:
        checks.append(f"✗ 无法获取包列表: {str(e)}")
    
    return checks

def check_node_environment():
    """检查Node.js环境"""
    print("\n" + "=" * 60)
    print("Node.js环境诊断")
    print("=" * 60)
    
    checks = []
    
    # Node版本
    try:
        node_version = subprocess.check_output(["node", "--version"], 
                                             stderr=subprocess.STDOUT, text=True).strip()
        checks.append(f"✓ Node版本: {node_version}")
    except FileNotFoundError:
        checks.append("✗ Node.js: 未安装或不在PATH中")
        return checks
    except Exception as e:
        checks.append(f"✗ Node检查失败: {str(e)}")
        return checks
    
    # npm版本
    try:
        npm_version = subprocess.check_output(["npm", "--version"], 
                                            stderr=subprocess.STDOUT, text=True).strip()
        checks.append(f"✓ npm版本: {npm_version}")
    except Exception as e:
        checks.append(f"✗ npm检查失败: {str(e)}")
    
    # 检查关键包
    key_npm_packages = ["exceljs", "nodemailer", "docx"]
    try:
        npm_list = subprocess.check_output(["npm", "list", "--depth=0", "--json"], 
                                         stderr=subprocess.STDOUT, text=True)
        # 简化检查：只检查是否存在node_modules目录
        cwd = os.getcwd()
        node_modules_path = Path(cwd) / "node_modules"
        if node_modules_path.exists():
            checks.append(f"✓ node_modules目录: 存在")
            for pkg in key_npm_packages:
                pkg_path = node_modules_path / pkg
                if pkg_path.exists():
                    checks.append(f"✓ {pkg}: 已安装")
                else:
                    checks.append(f"✗ {pkg}: 未安装")
        else:
            checks.append("✗ node_modules目录: 不存在")
    except Exception as e:
        checks.append(f"✗ npm包检查失败: {str(e)}")
    
    return checks

def check_system_resources():
    """检查系统资源"""
    print("\n" + "=" * 60)
    print("系统资源诊断")
    print("=" * 60)
    
    checks = []
    
    # 操作系统
    checks.append(f"✓ 操作系统: {platform.system()} {platform.release()}")
    
    # 架构
    checks.append(f"✓ 系统架构: {platform.machine()}")
    
    # 内存信息（Windows）
    if platform.system() == "Windows":
        try:
            import psutil
            mem = psutil.virtual_memory()
            checks.append(f"✓ 内存: 总量{mem.total//(1024**3)}GB, 可用{mem.available//(1024**3)}GB ({mem.percent}%使用)")
            
            disk = psutil.disk_usage("C:\\")
            checks.append(f"✓ C盘: 总量{disk.total//(1024**3)}GB, 可用{disk.free//(1024**3)}GB ({disk.percent}%使用)")
        except ImportError:
            checks.append("⚠️  无法获取详细内存/磁盘信息（需要psutil包）")
    else:
        checks.append("⚠️  非Windows系统，资源检查可能需要适配")
    
    # 当前工作目录
    checks.append(f"✓ 工作目录: {os.getcwd()}")
    
    # 用户主目录
    checks.append(f"✓ 用户目录: {Path.home()}")
    
    return checks

def check_file_permissions():
    """检查文件权限"""
    print("\n" + "=" * 60)
    print("文件权限诊断")
    print("=" * 60)
    
    checks = []
    
    cwd = os.getcwd()
    
    # 检查当前目录是否可写
    test_file = Path(cwd) / ".permission_test.tmp"
    try:
        test_file.write_text("test")
        test_file.unlink()
        checks.append(f"✓ 当前目录: 可读写")
    except Exception as e:
        checks.append(f"✗ 当前目录: 不可写 ({str(e)})")
    
    # 检查常见问题目录
    problem_dirs = [
        "C:\\Windows\\System32",
        "C:\\Program Files",
        str(Path.home() / "Desktop"),
        str(Path.home() / "Documents")
    ]
    
    for dir_path in problem_dirs:
        dir_obj = Path(dir_path)
        if dir_obj.exists():
            checks.append(f"✓ 目录存在: {dir_path}")
            # 尝试列出目录（不修改）
            try:
                list(dir_obj.iterdir())[:3]  # 只尝试列出前3个
                checks.append(f"  → 可读取")
            except Exception as e:
                checks.append(f"  → 不可读取 ({str(e)})")
    
    return checks

def generate_diagnosis_report():
    """生成完整的诊断报告"""
    all_checks = []
    
    all_checks.extend(check_python_environment())
    all_checks.extend(check_node_environment())
    all_checks.extend(check_system_resources())
    all_checks.extend(check_file_permissions())
    
    print("\n" + "=" * 60)
    print("诊断报告总结")
    print("=" * 60)
    
    # 分类统计
    total = len(all_checks)
    ok_count = sum(1 for c in all_checks if c.startswith("✓"))
    warn_count = sum(1 for c in all_checks if "⚠️" in c)
    error_count = sum(1 for c in all_checks if c.startswith("✗"))
    
    print(f"总检查项: {total}")
    print(f"✓ 正常: {ok_count}")
    print(f"⚠️  警告: {warn_count}")
    print(f"✗ 错误: {error_count}")
    
    # 输出问题摘要
    if error_count > 0:
        print("\n" + "=" * 60)
        print("发现的问题（需要关注）:")
        print("=" * 60)
        for check in all_checks:
            if check.startswith("✗"):
                print(f"  {check}")
    
    if warn_count > 0:
        print("\n" + "=" * 60)
        print("警告信息（建议检查）:")
        print("=" * 60)
        for check in all_checks:
            if "⚠️" in check:
                print(f"  {check}")
    
    return {
        "total": total,
        "ok": ok_count,
        "warn": warn_count,
        "error": error_count,
        "checks": all_checks
    }

def main():
    """主函数"""
    print("遇卡换路 - 环境诊断工具")
    print("版本: 1.0.0")
    print("用途: 快速诊断系统环境，辅助判断是否是环境问题导致的卡顿")
    print()
    
    try:
        result = generate_diagnosis_report()
        
        # 给出建议
        print("\n" + "=" * 60)
        print("建议的换路方向:")
        print("=" * 60)
        
        if result["error"] > 3:
            print("⚠️  发现多个严重错误，建议：")
            print("  1. 修复环境问题（安装缺失的包/工具）")
            print("  2. 切换到更简单的技术方案（避开复杂依赖）")
            print("  3. 使用独立的虚拟环境（如venv、conda）")
        elif result["warn"] > 2:
            print("⚠️  发现多个警告，建议：")
            print("  1. 验证关键依赖是否正常工作")
            print("  2. 检查文件权限和路径配置")
            print("  3. 准备备用方案（如数据源不可用时的模拟数据）")
        else:
            print("✓ 环境基本正常，问题可能在其他方面（方案、理解、资源等）")
            print("  建议检查：")
            print("  1. 技术方案是否合理")
            print("  2. 需求理解是否正确")
            print("  3. 外部依赖是否可用")
        
        return result
        
    except Exception as e:
        print(f"诊断过程中发生错误: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    main()