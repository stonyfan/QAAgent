@echo off
REM ============================================
REM 使用Mockoon API运行测试
REM ============================================

echo.
echo ========================================
echo  使用Mockoon API运行测试
echo ========================================
echo.

REM 设置环境变量
set API_BASE_URL=http://localhost:3000

REM 检查Mockoon是否运行
echo [1/3] 检查Mockoon服务器...
curl -s http://localhost:3000/api/posts >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] Mockoon服务器未运行
    echo.
    echo 请先运行 start-mockoon.bat 启动服务器
    echo.
    pause
    exit /b 1
)
echo         服务器运行中... OK

REM 检查配置文件
echo [2/3] 检查测试配置...
if not exist "swagger_jsonplaceholder.json" (
    echo [错误] 找不到 swagger_jsonplaceholder.json
    echo.
    pause
    exit /b 1
)
echo         配置文件存在... OK

REM 运行测试
echo [3/3] 运行测试...
echo.
python src\pipeline.py swagger_jsonplaceholder.json

echo.
echo ========================================
echo  测试完成！
echo ========================================
echo.
echo 查看报告:
echo   - reports\[timestamp]\API测试报告.txt
echo   - reports\[timestamp]\API测试详细报告.txt
echo.

pause
