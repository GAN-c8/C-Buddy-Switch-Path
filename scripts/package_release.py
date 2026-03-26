#!/usr/bin/env python3
"""
发布打包脚本 - 生成正式发布包
"""

import os
import sys
import json
import shutil
import datetime
from pathlib import Path
import zipfile

def get_version():
    """从SKILL.md读取版本号"""
    skill_path = Path(__file__).parent.parent / "SKILL.md"
    with open(skill_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    version = "1.0.0"
    for line in lines:
        if line.startswith("version:"):
            version = line.split(":", 1)[1].strip()
            break
    
    return version

def validate_skill_structure():
    """验证Skill结构完整性"""
    required_files = [
        "SKILL.md",
        "README.md", 
        "LICENSE",
        "scripts/diagnose_environment.py",
        "scripts/path_switcher.py",
        "references/solution_review_checklist.md",
        "references/case_studies.md"
    ]
    
    base_dir = Path(__file__).parent.parent
    missing_files = []
    
    for file_path in required_files:
        full_path = base_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"错误: 缺少必要文件: {', '.join(missing_files)}")
        return False
    
    # 验证SKILL.md元数据
    skill_md_path = base_dir / "SKILL.md"
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    required_metadata = ["name:", "description:", "version:", "author:", "license:"]
    missing_metadata = []
    
    for metadata in required_metadata:
        if metadata not in content:
            missing_metadata.append(metadata)
    
    if missing_metadata:
        print(f"错误: SKILL.md缺少必要元数据: {', '.join(missing_metadata)}")
        return False
    
    print("成功: Skill结构验证通过")
    return True

def create_release_info():
    """创建发布信息文件"""
    version = get_version()
    release_date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    release_info = {
        "name": "problem-solving-switch-path",
        "version": version,
        "release_date": release_date,
        "description": "通用问题解决框架——遇卡换路原则",
        "files": [
            "SKILL.md",
            "README.md",
            "LICENSE",
            "scripts/diagnose_environment.py",
            "scripts/path_switcher.py",
            "scripts/package_release.py",
            "references/solution_review_checklist.md",
            "references/case_studies.md",
            "assets/"
        ],
        "checksum": {
            "sha256": "待计算",
            "md5": "待计算"
        },
        "compatibility": {
            "workbuddy": ">=1.0.0",
            "python": ">=3.8",
            "node": ">=16.0.0"
        },
        "installation": {
            "manual": "解压到 ~/.workbuddy/skills/ 目录",
            "git": "git clone https://github.com/can-buddy/problem-solving-switch-path.git"
        }
    }
    
    return release_info

def create_zip_package(output_dir="releases"):
    """创建zip发布包"""
    version = get_version()
    base_dir = Path(__file__).parent.parent
    package_name = f"problem-solving-switch-path-v{version}"
    
    # 创建输出目录
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    zip_filename = output_path / f"{package_name}.zip"
    
    # 需要排除的文件和目录
    exclude_patterns = [
        "__pycache__",
        ".git",
        ".DS_Store",
        "*.pyc",
        "releases",
        "dist",
        "build"
    ]
    
    print(f"📦 正在创建发布包: {zip_filename}")
    
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 遍历所有文件
        for root, dirs, files in os.walk(base_dir):
            # 排除不需要的目录
            dirs[:] = [d for d in dirs if d not in exclude_patterns]
            
            for file in files:
                # 排除不需要的文件
                if any(file.endswith(pattern) for pattern in ['.pyc', '.DS_Store']):
                    continue
                
                file_path = Path(root) / file
                arcname = package_name / file_path.relative_to(base_dir)
                
                zipf.write(file_path, arcname)
                print(f"  + {arcname}")
    
    # 创建release_info.json
    release_info = create_release_info()
    release_info_path = output_path / f"{package_name}-info.json"
    
    with open(release_info_path, 'w', encoding='utf-8') as f:
        json.dump(release_info, f, ensure_ascii=False, indent=2)
    
    print(f"📄 发布信息文件: {release_info_path}")
    
    # 计算文件大小
    zip_size = zip_filename.stat().st_size
    print(f"📊 包大小: {zip_size / 1024:.1f} KB")
    
    return zip_filename, release_info_path

def create_install_script():
    """创建安装脚本"""
    install_content = """#!/bin/bash
# 遇卡换路Skill安装脚本
# 版本: {version}
# 日期: {date}

set -e

SKILL_NAME="problem-solving-switch-path"
SKILL_VERSION="{version}"
INSTALL_DIR="$HOME/.workbuddy/skills"

echo "🚀 开始安装遇卡换路Skill v$SKILL_VERSION"
echo "========================================"

# 检查安装目录
if [ ! -d "$INSTALL_DIR" ]; then
    echo "📁 创建Skills目录: $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
else
    echo "✓ Skills目录已存在: $INSTALL_DIR"
fi

# 检查是否已安装
if [ -d "$INSTALL_DIR/$SKILL_NAME" ]; then
    echo "⚠️  检测到已安装的旧版本"
    read -p "是否备份并覆盖？(y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        BACKUP_DIR="$INSTALL_DIR/${SKILL_NAME}-backup-$(date +%Y%m%d-%H%M%S)"
        echo "📦 备份到: $BACKUP_DIR"
        mv "$INSTALL_DIR/$SKILL_NAME" "$BACKUP_DIR"
    else
        echo "❌ 安装取消"
        exit 1
    fi
fi

# 解压安装
echo "📂 解压文件到: $INSTALL_DIR/$SKILL_NAME"
unzip -q -o "$0" -d "$INSTALL_DIR"

# 设置权限
chmod +x "$INSTALL_DIR/$SKILL_NAME/scripts/"*.py 2>/dev/null || true

echo "✅ 安装完成！"
echo ""
echo "📖 使用说明:"
echo "   1. 重启WorkBuddy或重新加载Skills"
echo "   2. 当任务卡住超过2次时，Skill会自动触发"
echo "   3. 手动使用:"
echo "      python $INSTALL_DIR/$SKILL_NAME/scripts/diagnose_environment.py"
echo "      python $INSTALL_DIR/$SKILL_NAME/scripts/path_switcher.py"
echo ""
echo "🔗 文档: $INSTALL_DIR/$SKILL_NAME/README.md"
echo "========================================"

exit 0

# 以下是zip文件内容
"""

    version = get_version()
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    
    install_script = install_content.format(version=version, date=date)
    
    # 创建自解压安装脚本
    base_dir = Path(__file__).parent.parent
    output_path = base_dir / "releases" / f"install-problem-solving-switch-path-v{version}.sh"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(install_script)
    
    # 设置执行权限（Linux/macOS）
    if sys.platform != "win32":
        os.chmod(output_path, 0o755)
    
    print(f"📜 创建安装脚本: {output_path}")
    
    return output_path

def main():
    """主函数"""
    print("=" * 60)
    print("遇卡换路Skill - 发布打包工具")
    print("=" * 60)
    
    # 步骤1：验证结构
    print("\n[1] 验证Skill结构...")
    if not validate_skill_structure():
        print("错误: 验证失败，请修复问题后再打包")
        return 1
    
    # 步骤2：创建发布包
    print("\n[2] 创建发布包...")
    try:
        zip_file, info_file = create_zip_package()
        print(f"成功: 发布包创建成功: {zip_file}")
    except Exception as e:
        print(f"错误: 创建发布包失败: {str(e)}")
        return 1
    
    # 步骤3：创建安装脚本（可选）
    print("\n[3] 创建安装脚本...")
    if sys.platform != "win32":
        install_script = create_install_script()
        print(f"✅ 安装脚本创建成功: {install_script}")
    else:
        print("ℹ️  Windows系统跳过创建shell安装脚本")
    
    # 步骤4：生成发布说明
    print("\n[4] 生成发布说明...")
    version = get_version()
    release_note = f"""
# 遇卡换路Skill v{version} 发布说明

## 版本信息
- **版本号**: {version}
- **发布日期**: {datetime.datetime.now().strftime('%Y-%m-%d')}
- **包大小**: {Path(zip_file).stat().st_size / 1024:.1f} KB

## 更新内容
### 🎉 新功能
- 完整的"遇卡换路"问题解决框架
- 环境诊断工具 (`diagnose_environment.py`)
- 路径切换策略推荐器 (`path_switcher.py`)
- 方案审查清单和详细案例库

### 🐛 修复与改进
- 完善了Skill元数据和文档
- 添加了MIT许可证
- 创建了完整的发布包

### 📦 安装方式
1. **手动安装**: 解压 `{Path(zip_file).name}` 到 `~/.workbuddy/skills/`
2. **脚本安装**: 运行 `install-problem-solving-switch-path-v{version}.sh`

## 文件清单
- `SKILL.md` - Skill主文档
- `README.md` - 项目说明
- `LICENSE` - MIT许可证
- `scripts/` - 工具脚本
- `references/` - 参考资料
- `releases/` - 发布文件

## 兼容性
- WorkBuddy >= 1.0.0
- Python >= 3.8
- Node.js >= 16.0.0
- Windows/macOS/Linux

## 使用反馈
如有问题或建议，请通过GitHub Issues反馈。
"""
    
    release_note_path = Path(__file__).parent.parent / "releases" / f"RELEASE-v{version}.md"
    with open(release_note_path, 'w', encoding='utf-8') as f:
        f.write(release_note)
    
    print(f"📝 发布说明: {release_note_path}")
    
    print("\n" + "=" * 60)
    print("✅ 发布准备完成！")
    print("=" * 60)
    
    print(f"\n📁 发布文件位于: releases/")
    print(f"  1. {Path(zip_file).name}")
    print(f"  2. {Path(info_file).name}")
    if sys.platform != "win32":
        print(f"  3. install-problem-solving-switch-path-v{version}.sh")
    print(f"  4. RELEASE-v{version}.md")
    
    print("\n🎯 下一步: 将发布文件上传到GitHub Releases或Skill市场")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())