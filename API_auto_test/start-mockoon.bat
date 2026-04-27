@echo off
REM ============================================
REM Mockoon测试API服务器 - 快速启动脚本
REM ============================================

echo.
echo ========================================
echo  Mockoon测试API服务器启动
echo ========================================
echo.

REM 检查Mockoon CLI是否已安装
where mockoon-cli >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [错误] Mockoon CLI未安装
    echo.
    echo 请先安装Mockoon CLI:
    echo   npm install -g @mockoon/cli
    echo.
    echo 或使用桌面应用:
    echo   1. 下载安装: https://mockoon.com/download/windows
    echo   2. 启动Mockoon应用
    echo   3. File ^> Import ^> 选择 mockoon-test-api.json
    echo   4. 点击 "Start Server"
    echo.
    pause
    exit /b 1
)

REM 检查配置文件是否存在
if not exist "mockoon-test-api.json" (
    echo [错误] 找不到配置文件 mockoon-test-api.json
    echo.
    echo 请确保在正确的目录中运行此脚本
    echo 当前目录: %CD%
    echo.
    pause
    exit /b 1
)

echo [1/2] 检查环境... 完成
echo [2/2] 启动Mockoon服务器...
echo.
echo 服务器信息:
echo   - 端口: 3000
echo   - 地址: http://localhost:3000
echo   - 配置: mockoon-test-api.json
echo.
echo ========================================
echo  服务器正在运行...
echo  按 Ctrl+C 停止服务器
echo ========================================
echo.

REM 启动Mockoon服务器
mockoon-cli start --data mockoon-test-api.json --port 3000

pause
