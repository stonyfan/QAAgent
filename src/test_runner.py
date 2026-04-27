import subprocess
import json
from typing import Dict, Any, Tuple


def run_tests(test_dir: str = 'tests', pytest_args: list = None) -> Tuple[int, str, str]:
    """
    运行 pytest 测试并返回完整的原始输出

    Args:
        test_dir: 测试文件目录或测试文件路径
        pytest_args: 额外的 pytest 参数（如 ['-v', '-s']）

    Returns:
        元组 (exit_code, stdout, stderr)
        - exit_code: 退出码（0表示成功，1表示有失败）
        - stdout: 标准输出（完整输出）
        - stderr: 标准错误（错误信息）

    示例：
        exit_code, stdout, stderr = run_tests('tests')
        if exit_code == 0:
            print("所有测试通过")
        else:
            print(f"有测试失败:\\n{stdout}")
    """
    # 构建命令
    cmd = ['pytest', test_dir]

    # 添加额外的参数
    if pytest_args:
        cmd.extend(pytest_args)

    # 默认参数
    if '-v' not in cmd:
        cmd.append('-v')
    if '--tb=short' not in cmd:
        cmd.append('--tb=short')

    try:
        # 执行 pytest
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300
        )

        return result.returncode, result.stdout, result.stderr

    except subprocess.TimeoutExpired:
        return 1, '', '测试执行超时（超过300秒）'
    except FileNotFoundError:
        return 1, '', 'pytest 未安装，请先安装: pip install pytest'
    except Exception as e:
        return 1, '', f'测试执行错误: {str(e)}'


def run_pytest(test_dir: str = 'tests') -> Dict[str, Any]:
    """
    运行 pytest 测试并返回结果

    Args:
        test_dir: 测试文件目录

    Returns:
        测试结果字典
        {
            "success": bool,
            "total": int,
            "passed": int,
            "failed": int,
            "duration": float,
            "output": str,
            "tests": [
                {
                    "name": str,
                    "status": "passed" | "failed",
                    "duration": float,
                    "error": str | None
                }
            ]
        }
    """
    try:
        # 运行 pytest，使用 JSON 报告格式
        result = subprocess.run(
            ['pytest', test_dir, '-v', '--tb=short', '--strict-markers'],
            capture_output=True,
            text=True,
            timeout=300
        )

        output = result.stdout + result.stderr

        # 解析 pytest 输出
        test_results = parse_pytest_output(output)

        return test_results

    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "total": 0,
            "passed": 0,
            "failed": 0,
            "duration": 0,
            "output": "测试执行超时",
            "tests": []
        }
    except Exception as e:
        return {
            "success": False,
            "total": 0,
            "passed": 0,
            "failed": 0,
            "duration": 0,
            "output": f"测试执行错误: {str(e)}",
            "tests": []
        }


def parse_pytest_output(output: str) -> Dict[str, Any]:
    """
    解析 pytest 文本输出，提取测试结果

    Args:
        output: pytest 的文本输出

    Returns:
        结构化的测试结果
    """
    lines = output.split('\n')  # 修复：使用真正的换行符

    tests = []
    total = 0
    passed = 0
    failed = 0

    for line in lines:
        line = line.strip()

        # 解析测试行，例如: "test_login_success PASSED"
        if 'test_' in line and ('PASSED' in line or 'FAILED' in line):
            parts = line.split()
            test_name = parts[0]
            status = 'passed' if 'PASSED' in line else 'failed'

            total += 1
            if status == 'passed':
                passed += 1
            else:
                failed += 1

            tests.append({
                "name": test_name,
                "status": status,
                "duration": 0,
                "error": None if status == 'passed' else "Test failed"
            })

    # 尝试从输出中提取总结信息
    for line in lines:
        if 'passed' in line and 'failed' in line:
            # 例如: "2 passed, 1 failed in 1.23s"
            if 'passed' in line:
                try:
                    passed_str = line.split('passed')[0].strip().split()[-1]
                    passed = int(passed_str)
                except:
                    pass
            if 'failed' in line:
                try:
                    failed_str = line.split('failed')[0].strip().split()[-1]
                    failed = int(failed_str)
                except:
                    pass

    total = passed + failed

    return {
        "success": failed == 0,
        "total": total,
        "passed": passed,
        "failed": failed,
        "duration": 0,
        "output": output,
        "tests": tests
    }
