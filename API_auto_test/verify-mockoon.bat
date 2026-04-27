@echo off
REM ============================================
REM Mockoon配置验证脚本
REM ============================================

echo.
echo ========================================
echo  Mockoon配置验证
echo ========================================
echo.

REM 检查服务器是否运行
echo [1/10] 检查服务器状态...
curl -s http://localhost:3000/api/posts >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [错误] Mockoon服务器未运行
    echo.
    echo 请先运行: start-mockoon.bat
    echo.
    pause
    exit /b 1
)
echo         ✓ 服务器运行中
echo.

REM 测试计数器
set /a passed=0
set /a total=0

REM 测试函数
:set_test
set /a total+=1
exit /b

:pass_test
echo [✓] 测试通过: %~1
set /a passed+=1
exit /b

:fail_test
echo [✗] 测试失败: %~1
exit /b

REM ==================== 测试开始 ====================

call :set_test
echo [%total%] 测试GET /api/posts (200 OK)
curl -s -w "%%{http_code}" http://localhost:3000/api/posts -o nul >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    call :pass_test "GET /api/posts 返回200"
) else (
    call :fail_test "GET /api/posts 返回200"
)

call :set_test
echo [%total%] 测试GET /api/posts/999999 (404 Not Found)
curl -s -w "%%{http_code}" http://localhost:3000/api/posts/999999 -o nul | findstr "404" >nul
if %ERRORLEVEL% EQU 0 (
    call :pass_test "GET /api/posts/999999 返回404"
) else (
    call :fail_test "GET /api/posts/999999 返回404"
)

call :set_test
echo [%total%] 测试POST /api/posts (201 Created)
curl -s -X POST http://localhost:3000/api/posts -H "Content-Type: application/json" -d "{\"title\":\"Test\"}" -w "%%{http_code}" -o nul | findstr "201" >nul
if %ERRORLEVEL% EQU 0 (
    call :pass_test "POST /api/posts 返回201"
) else (
    call :fail_test "POST /api/posts 返回201"
)

call :set_test
echo [%total%] 测试POST /api/posts (缺少title - 422)
curl -s -X POST http://localhost:3000/api/posts -H "Content-Type: application/json" -d "{\"body\":\"Test\"}" -w "%%{http_code}" -o nul | findstr "422" >nul
if %ERRORLEVEL% EQU 0 (
    call :pass_test "POST /api/posts (缺少title) 返回422"
) else (
    call :fail_test "POST /api/posts (缺少title) 返回422"
)

call :set_test
echo [%total%] 测试GET /api/protected (无认证 - 401)
curl -s -w "%%{http_code}" http://localhost:3000/api/protected -o nul | findstr "401" >nul
if %ERRORLEVEL% EQU 0 (
    call :pass_test "GET /api/protected (无认证) 返回401"
) else (
    call :fail_test "GET /api/protected (无认证) 返回401"
)

call :set_test
echo [%total%] 测试GET /api/protected (有效token - 200)
curl -s -H "Authorization: Bearer valid-token" -w "%%{http_code}" http://localhost:3000/api/protected -o nul | findstr "200" >nul
if %ERRORLEVEL% EQU 0 (
    call :pass_test "GET /api/protected (有效token) 返回200"
) else (
    call :fail_test "GET /api/protected (有效token) 返回200"
)

call :set_test
echo [%total%] 测试GET /api/admin/users (普通用户token - 403)
curl -s -H "Authorization: Bearer valid-token" -w "%%{http_code}" http://localhost:3000/api/admin/users -o nul | findstr "403" >nul
if %ERRORLEVEL% EQU 0 (
    call :pass_test "GET /api/admin/users (普通用户) 返回403"
) else (
    call :fail_test "GET /api/admin/users (普通用户) 返回403"
)

call :set_test
echo [%total%] 测试GET /api/admin/users (管理员token - 200)
curl -s -H "Authorization: Bearer admin-token" -w "%%{http_code}" http://localhost:3000/api/admin/users -o nul | findstr "200" >nul
if %ERRORLEVEL% EQU 0 (
    call :pass_test "GET /api/admin/users (管理员) 返回200"
) else (
    call :fail_test "GET /api/admin/users (管理员) 返回200"
)

call :set_test
echo [%total%] 测试GET /api/old-url (301重定向)
curl -s -i http://localhost:3000/api/old-url | findstr "301" >nul
if %ERRORLEVEL% EQU 0 (
    call :pass_test "GET /api/old-url 返回301"
) else (
    call :fail_test "GET /api/old-url 返回301"
)

call :set_test
echo [%total%] 测试GET /api/error (500服务器错误)
curl -s -w "%%{http_code}" http://localhost:3000/api/error -o nul | findstr "500" >nul
if %ERRORLEVEL% EQU 0 (
    call :pass_test "GET /api/error 返回500"
) else (
    call :fail_test "GET /api/error 返回500"
)

call :set_test
echo [%total%] 测试GET /api/maintenance (503服务不可用)
curl -s -w "%%{http_code}" http://localhost:3000/api/maintenance -o nul | findstr "503" >nul
if %ERRORLEVEL% EQU 0 (
    call :pass_test "GET /api/maintenance 返回503"
) else (
    call :fail_test "GET /api/maintenance 返回503"
)

echo.
echo ========================================
echo  验证结果
echo ========================================
echo.
echo 通过: %passed%/%total%
echo.

if %passed% EQU %total% (
    echo [✓] 所有测试通过！Mockoon配置正常
    echo.
    echo 下一步:
    echo   1. 运行测试: test-with-mockoon.bat
    echo   2. 查看文档: Mockoon配置使用指南.md
) else (
    echo [✗] 有 %total% - %passed% 个测试失败
    echo.
    echo 请检查:
    echo   1. Mockoon服务器是否正在运行
    echo   2. 端口3000是否被占用
    echo   3. 配置文件是否正确
)

echo.
pause
