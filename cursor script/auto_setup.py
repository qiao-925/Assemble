#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
技术信息工作流自动设置脚本
一键完成依赖安装、目录创建、服务启动等所有配置
"""

import os
import sys
import subprocess
import time
from pathlib import Path

class AutoSetup:
    """自动设置器"""
    
    def __init__(self):
        self.work_dir = Path(os.path.dirname(os.path.abspath(__file__)))
        self.setup_log = []
    
    def log(self, message: str, status: str = "INFO"):
        """记录设置日志"""
        log_entry = f"[{status}] {message}"
        self.setup_log.append(log_entry)
        
        # 根据状态选择不同的emoji
        emoji_map = {
            "INFO": "ℹ️",
            "SUCCESS": "✅", 
            "ERROR": "❌",
            "WARNING": "⚠️",
            "PROGRESS": "🔄"
        }
        
        print(f"{emoji_map.get(status, 'ℹ️')} {message}")
    
    def check_python_version(self) -> bool:
        """检查Python版本"""
        self.log("检查Python版本", "PROGRESS")
        
        if sys.version_info < (3, 7):
            self.log(f"Python版本过低: {sys.version_info}，需要3.7+", "ERROR")
            return False
        
        self.log(f"Python版本检查通过: {sys.version_info}", "SUCCESS")
        return True
    
    def install_dependencies(self) -> bool:
        """安装依赖包"""
        self.log("安装Python依赖包", "PROGRESS")
        
        requirements_file = self.work_dir / "requirements.txt"
        if not requirements_file.exists():
            self.log("requirements.txt文件不存在", "ERROR")
            return False
        
        try:
            cmd = [sys.executable, "-m", "pip", "install", "-r", str(requirements_file)]
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=str(self.work_dir))
            
            if result.returncode == 0:
                self.log("依赖安装成功", "SUCCESS")
                return True
            else:
                self.log(f"依赖安装失败: {result.stderr}", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"依赖安装异常: {e}", "ERROR")
            return False
    
    def create_directories(self) -> bool:
        """创建必要目录"""
        self.log("创建目录结构", "PROGRESS")
        
        directories = [
            "data", "output", "cache", "config", 
            "logs", "triggers", "completed"
        ]
        
        try:
            for dir_name in directories:
                dir_path = self.work_dir / dir_name
                dir_path.mkdir(exist_ok=True)
                
            self.log("目录结构创建完成", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"创建目录失败: {e}", "ERROR")
            return False
    
    def setup_configuration(self) -> bool:
        """设置配置文件"""
        self.log("检查配置文件", "PROGRESS")
        
        config_file = self.work_dir / "config" / "workflow_config.yaml"
        
        if config_file.exists():
            self.log("配置文件已存在，跳过创建", "SUCCESS")
            return True
        
        # 配置文件已经通过edit_file创建了，这里只是检查
        if config_file.exists():
            self.log("配置文件设置完成", "SUCCESS")
            return True
        else:
            self.log("配置文件不存在，请检查", "WARNING")
            return True  # 不强制失败，系统会使用默认配置
    
    def test_basic_functionality(self) -> bool:
        """测试基本功能"""
        self.log("测试基本功能", "PROGRESS")
        
        try:
            # 测试导入主要模块
            sys.path.append(str(self.work_dir))
            
            from tech_info_collector import TechInfoCollector
            from tech_analyzer import TechAnalyzer
            from bg_agent_trigger import BackgroundAgentTrigger
            
            # 创建实例测试
            collector = TechInfoCollector()
            analyzer = TechAnalyzer()
            trigger = BackgroundAgentTrigger()
            
            self.log("基本功能测试通过", "SUCCESS")
            return True
            
        except Exception as e:
            self.log(f"功能测试失败: {e}", "ERROR")
            return False
    
    def start_daemon_service(self) -> bool:
        """启动守护进程服务"""
        self.log("启动守护进程服务", "PROGRESS")
        
        try:
            from service_manager import ServiceManager
            manager = ServiceManager()
            
            if manager.is_running():
                self.log("守护进程已在运行", "SUCCESS")
                return True
            
            success = manager.start_service()
            if success:
                self.log("守护进程启动成功", "SUCCESS")
                return True
            else:
                self.log("守护进程启动失败", "ERROR")
                return False
                
        except Exception as e:
            self.log(f"启动守护进程异常: {e}", "ERROR")
            return False
    
    def run_full_setup(self, start_service: bool = True) -> bool:
        """运行完整设置流程"""
        self.log("开始自动设置流程", "PROGRESS")
        print("=" * 60)
        
        steps = [
            ("检查Python环境", self.check_python_version),
            ("安装依赖包", self.install_dependencies),
            ("创建目录结构", self.create_directories),
            ("设置配置文件", self.setup_configuration),
            ("测试基本功能", self.test_basic_functionality),
        ]
        
        if start_service:
            steps.append(("启动守护进程", self.start_daemon_service))
        
        # 执行设置步骤
        all_success = True
        for step_name, step_func in steps:
            print(f"\n🔄 步骤: {step_name}")
            success = step_func()
            if not success:
                all_success = False
                break
        
        print("\n" + "=" * 60)
        
        if all_success:
            self.log("🎉 自动设置完成！系统已就绪", "SUCCESS")
            self._show_usage_guide()
            return True
        else:
            self.log("❌ 设置过程中出现错误", "ERROR")
            self._show_troubleshooting()
            return False
    
    def _show_usage_guide(self):
        """显示使用指南"""
        print("\n📚 使用指南:")
        print("=" * 40)
        print("🤖 Background Agent 使用:")
        print("  - 每日摘要: bg_daily_digest()")
        print("  - 项目分析: bg_analyze_project('microsoft/garnet')")  
        print("  - 趋势分析: bg_trend_analysis('ai')")
        print("  - 项目对比: bg_compare_projects(['redis/redis', 'microsoft/garnet'])")
        print("  - 系统状态: bg_get_status()")
        
        print("\n⌨️ 命令行使用:")
        print("  - 查看状态: python service_manager.py status")
        print("  - 查看日志: python service_manager.py logs")
        print("  - 手动触发: python bg_agent_trigger.py daily --wait")
        print("  - 停止服务: python service_manager.py stop")
        
        print("\n📋 系统特性:")
        print("  - ⏰ 自动运行: 每天8:00生成技术摘要")
        print("  - 🔔 随时触发: Background Agent可随时触发分析")
        print("  - 📊 状态监控: 实时查看运行状态和生成结果")
        print("  - 🎨 完全可配置: 编辑 config/workflow_config.yaml 自定义")
    
    def _show_troubleshooting(self):
        """显示故障排除指南"""
        print("\n🔧 故障排除:")
        print("=" * 40)
        print("1. 检查Python版本: python3 --version")
        print("2. 手动安装依赖: pip install -r requirements.txt")
        print("3. 检查网络连接: ping github.com")
        print("4. 查看详细日志: python service_manager.py logs")
        print("5. 重新运行设置: python auto_setup.py --full")

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='技术信息工作流自动设置')
    parser.add_argument('--full', action='store_true', help='运行完整设置流程')
    parser.add_argument('--no-service', action='store_true', help='不启动守护进程')
    parser.add_argument('--deps-only', action='store_true', help='仅安装依赖')
    parser.add_argument('--test-only', action='store_true', help='仅测试功能')
    
    args = parser.parse_args()
    
    setup = AutoSetup()
    
    if args.deps_only:
        setup.check_python_version()
        setup.install_dependencies()
        
    elif args.test_only:
        setup.test_basic_functionality()
        
    elif args.full or not any(vars(args).values()):
        # 默认运行完整设置
        start_service = not args.no_service
        setup.run_full_setup(start_service=start_service)
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()