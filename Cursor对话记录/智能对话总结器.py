#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Closer智能对话总结器
自动分析对话内容，提取关键信息，生成持久化记录
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

class CloserDialogueSummarizer:
    def __init__(self):
        self.dialogue_folder = Path("closer对话")
        self.template_file = self.dialogue_folder / "对话持久化模板.md"
        self.dialogue_folder.mkdir(exist_ok=True)
        
        # 对话关键词模式
        self.patterns = {
            "file_operations": {
                "created": r"创建.*?文件|新建.*?文件|建立.*?文件夹",
                "modified": r"修改.*?文件|更新.*?文件|编辑.*?文件",
                "deleted": r"删除.*?文件|移除.*?文件|清理.*?文件",
                "moved": r"移动.*?文件|重命名.*?文件|转移.*?文件"
            },
            "tools_used": {
                "python": r"Python|python|pip install|import.*?requests|BeautifulSoup",
                "terminal": r"终端|命令行|shell|PowerShell|cd|mkdir",
                "git": r"git|版本控制|commit|push|pull",
                "editor": r"编辑|修改|更新|Cursor|IDE"
            },
            "problems": {
                "error": r"错误|失败|问题|异常|bug|404|500",
                "solution": r"解决|修复|处理|方案|方法|办法",
                "decision": r"决定|选择|决策|方案|策略"
            },
            "achievements": {
                "success": r"成功|完成|达成|实现|搞定|解决",
                "result": r"结果|成果|效果|输出|生成|创建"
            }
        }
    
    def analyze_dialogue_content(self, dialogue_text):
        """分析对话内容，提取关键信息"""
        analysis = {
            "file_operations": {},
            "tools_used": [],
            "problems": [],
            "achievements": [],
            "key_topics": [],
            "estimated_duration": "未知",
            "complexity_level": "中等"
        }
        
        # 分析文件操作
        for op_type, pattern in self.patterns["file_operations"].items():
            matches = re.findall(pattern, dialogue_text)
            if matches:
                analysis["file_operations"][op_type] = list(set(matches))
        
        # 分析工具使用
        for tool, pattern in self.patterns["tools_used"].items():
            if re.search(pattern, dialogue_text):
                analysis["tools_used"].append(tool)
        
        # 分析问题和解决方案
        for prob_type, pattern in self.patterns["problems"].items():
            matches = re.findall(pattern, dialogue_text)
            if matches:
                analysis["problems"].extend(matches)
        
        # 分析成果
        for ach_type, pattern in self.patterns["achievements"].items():
            matches = re.findall(pattern, dialogue_text)
            if matches:
                analysis["achievements"].extend(matches)
        
        # 估算对话时长（基于内容长度和复杂度）
        content_length = len(dialogue_text)
        if content_length < 1000:
            analysis["estimated_duration"] = "约30分钟"
            analysis["complexity_level"] = "简单"
        elif content_length < 5000:
            analysis["estimated_duration"] = "约1小时"
            analysis["complexity_level"] = "中等"
        else:
            analysis["estimated_duration"] = "约2小时+"
            analysis["complexity_level"] = "复杂"
        
        return analysis
    
    def generate_dialogue_summary(self, dialogue_text, topic="未知主题"):
        """生成对话总结"""
        analysis = self.analyze_dialogue_content(dialogue_text)
        
        # 读取模板
        with open(self.template_file, 'r', encoding='utf-8') as f:
            template = f.read()
        
        # 生成时间戳
        timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        
        # 填充模板
        summary = template.replace("对话日期: ", f"对话日期: {timestamp}")
        summary = summary.replace("对话主题: ", f"对话主题: {topic}")
        summary = summary.replace("对话时长: ", f"对话时长: {analysis['estimated_duration']}")
        summary = summary.replace("主要参与者: ", "主要参与者: 用户 + Closer AI助手")
        
        # 填充文件操作信息
        file_ops = []
        for op_type, files in analysis["file_operations"].items():
            if op_type == "created":
                file_ops.append(f"创建的文件: {', '.join(files[:3])}")
            elif op_type == "modified":
                file_ops.append(f"修改的文件: {', '.join(files[:3])}")
        
        if file_ops:
            summary = summary.replace("创建的文件: ", f"创建的文件: \n  - " + "\n  - ".join(file_ops))
        
        # 填充工具信息
        if analysis["tools_used"]:
            tools_str = ", ".join(analysis["tools_used"])
            summary = summary.replace("使用的工具: ", f"使用的工具: {tools_str}")
        
        # 填充问题信息
        if analysis["problems"]:
            problems_str = "\n  - ".join(analysis["problems"][:3])
            summary = summary.replace("问题1: ", f"问题1: \n  - 描述: {problems_str}")
        
        # 填充成果信息
        if analysis["achievements"]:
            achievements_str = "\n  - ".join(analysis["achievements"][:3])
            summary = summary.replace("成果1: ", f"成果1: \n  - {achievements_str}")
        
        # 填充复杂度信息
        summary = summary.replace("难度级别: ", f"难度级别: {analysis['complexity_level']}")
        
        return summary
    
    def auto_save_dialogue(self, dialogue_text, topic="未知主题"):
        """自动保存对话总结"""
        try:
            # 生成总结
            summary = self.generate_dialogue_summary(dialogue_text, topic)
            
            # 创建文件名
            safe_topic = re.sub(r'[<>:"/\\|?*]', '_', topic)
            filename = f"{safe_topic}_对话.md"
            filepath = self.dialogue_folder / filename
            
            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(summary)
            
            print(f"✅ 对话总结已自动保存到: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"❌ 自动保存失败: {e}")
            return None
    
    def create_quick_summary(self, topic, key_points):
        """创建快速总结（用于简单对话）"""
        timestamp = datetime.now().strftime("%Y年%m月%d日 %H:%M")
        
        summary = f"""# {topic} - 快速对话总结

## 📅 **对话基本信息**
- **对话日期**: {timestamp}
- **对话主题**: {topic}
- **对话时长**: 约30分钟
- **主要参与者**: 用户 + Closer AI助手

## 🎯 **关键要点**
{chr(10).join([f"- {point}" for point in key_points])}

## 📝 **快速记录**
- 这是一个快速对话，主要讨论了{topic}
- 关键信息已记录如上
- 如需详细记录，请使用完整模板

---
*此文档由Closer智能对话总结器自动生成*
"""
        
        # 保存文件
        safe_topic = re.sub(r'[<>:"/\\|?*]', '_', topic)
        filename = f"{safe_topic}_快速总结.md"
        filepath = self.dialogue_folder / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"✅ 快速总结已保存到: {filepath}")
        return filepath

def main():
    """主函数 - 演示用法"""
    summarizer = CloserDialogueSummarizer()
    
    print("🤖 Closer智能对话总结器")
    print("=" * 50)
    
    # 示例用法
    print("\n📋 使用方法:")
    print("1. 自动保存: summarizer.auto_save_dialogue(dialogue_text, topic)")
    print("2. 快速总结: summarizer.create_quick_summary(topic, key_points)")
    print("3. 手动分析: summarizer.analyze_dialogue_content(dialogue_text)")
    
    print("\n💡 建议:")
    print("- 在对话结束时调用 auto_save_dialogue()")
    print("- 对于简单对话使用 create_quick_summary()")
    print("- 系统会自动分析内容并填充模板")

if __name__ == "__main__":
    main()
