@echo off
chcp 65001 >nul
title Boss直聘批量投递简历脚本

echo.
echo ========================================
echo    🚀 Boss直聘批量投递简历脚本
echo ========================================
echo.
echo 请选择要运行的脚本：
echo.
echo 1. 🎯 真实运行版 (推荐)
echo 2. 🧪 演示版本
echo 3. 📚 完整功能版
echo 4. 🔧 编辑配置文件
echo 5. ❌ 退出
echo.
set /p choice=请输入选择 (1-5): 

if "%choice%"=="1" (
    echo.
    echo 🎯 启动真实运行版脚本...
    echo 注意：这将打开浏览器并访问真实网站
    echo.
    pause
    python boss_zhilian_real.py
) else if "%choice%"=="2" (
    echo.
    echo 🧪 启动演示版本脚本...
    echo 注意：这是模拟版本，不会访问真实网站
    echo.
    pause
    python boss_zhilian_simple.py
) else if "%choice%"=="3" (
    echo.
    echo 📚 启动完整功能版脚本...
    echo 注意：需要安装qrcode等依赖包
    echo.
    pause
    python boss_zhilian_batch_apply.py
) else if "%choice%"=="4" (
    echo.
    echo 🔧 打开配置文件进行编辑...
    notepad boss_config.json
    goto :menu
) else if "%choice%"=="5" (
    echo.
    echo 👋 再见！
    pause
    exit
) else (
    echo.
    echo ❌ 无效选择，请重新运行脚本
    pause
    exit
)

echo.
echo 脚本执行完成！
pause
