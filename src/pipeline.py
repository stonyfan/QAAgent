"""
QA Agent - Swagger 测试流水线

这是主控模块，负责串联整个测试流程：
swagger_parser → api_test → test_runner → report
"""

import sys
import os
from datetime import datetime

# 添加 src 目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from swagger_parser import parse_swagger
from api_test import generate_tests_for_apis
from test_runner import run_pytest
from report import generate_and_save_report, generate_and_save_detailed_report


def run_swagger_pipeline(swagger_path: str) -> dict:
    """
    运行完整的 Swagger 测试流水线

    步骤：
    1. 解析 Swagger 文档
    2. 生成测试代码
    3. 执行测试
    4. 生成报告

    Args:
        swagger_path: Swagger 文档路径

    Returns:
        流水线执行结果
        {
            "success": bool,
            "swagger_path": str,
            "apis_count": int,
            "test_files": list,
            "test_results": dict,
            "report_path": str
        }
    """
    print("=" * 60)
    print("QA Agent - Swagger 测试流水线")
    print("=" * 60)

    # 步骤 1: 解析 Swagger 文档
    print(f"\\n[步骤 1/4] 解析 Swagger 文档: {swagger_path}")
    try:
        base_url, apis = parse_swagger(swagger_path)
        print(f"✓ 成功解析 {len(apis)} 个 API")
        print(f"✓ BASE_URL: {base_url}")
        for api in apis:
            print(f"  - {api['method']} {api['path']}: {api['summary']}")
    except Exception as e:
        print(f"✗ 解析失败: {str(e)}")
        return {
            "success": False,
            "error": f"Swagger 解析失败: {str(e)}",
            "swagger_path": swagger_path
        }

    # 步骤 2: 生成测试代码
    print(f"\\n[步骤 2/4] 生成测试代码")
    try:
        test_files = generate_tests_for_apis(apis, base_url=base_url, output_dir='tests')
        print(f"✓ 成功生成 {len(test_files)} 个测试文件")
        for test_file in test_files:
            print(f"  - {test_file}")
    except Exception as e:
        print(f"✗ 生成失败: {str(e)}")
        return {
            "success": False,
            "error": f"测试代码生成失败: {str(e)}",
            "swagger_path": swagger_path,
            "apis_count": len(apis)
        }

    # 步骤 3: 执行测试
    print(f"\\n[步骤 3/4] 执行测试")
    try:
        test_results = run_pytest(test_dir='tests')
        print(f"✓ 测试执行完成")
        print(f"  - 总计: {test_results['total']} 个")
        print(f"  - 通过: {test_results['passed']} 个")
        print(f"  - 失败: {test_results['failed']} 个")
    except Exception as e:
        print(f"✗ 执行失败: {str(e)}")
        return {
            "success": False,
            "error": f"测试执行失败: {str(e)}",
            "swagger_path": swagger_path,
            "apis_count": len(apis),
            "test_files": test_files
        }

    # 创建报告目录（以时间戳命名）
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_dir = os.path.join('reports', timestamp)
    os.makedirs(report_dir, exist_ok=True)

    # 步骤 4: 生成测试报告
    print(f"\\n[步骤 4/5] 生成测试报告")
    try:
        report_path = generate_and_save_report(
            test_results,
            source=f"Swagger: {swagger_path}",
            output_dir=report_dir
        )
        print(f"✓ 报告已生成: {report_path}")
    except Exception as e:
        print(f"✗ 报告生成失败: {str(e)}")
        return {
            "success": False,
            "error": f"报告生成失败: {str(e)}",
            "swagger_path": swagger_path,
            "apis_count": len(apis),
            "test_files": test_files,
            "test_results": test_results
        }

    # 步骤 5: 生成详细报告
    print(f"\\n[步骤 5/5] 生成详细测试报告")
    try:
        detailed_report_path = generate_and_save_detailed_report(
            source=f"Swagger: {swagger_path}",
            output_dir=report_dir
        )
        if detailed_report_path:
            print(f"✓ 详细报告已生成: {detailed_report_path}")
        else:
            print("⚠ 没有找到详细日志，跳过详细报告生成")
    except Exception as e:
        print(f"⚠ 详细报告生成失败: {str(e)}")
        detailed_report_path = None

    # 完成
    print(f"\\n" + "=" * 60)
    print("✓ 流水线执行完成！")
    print("=" * 60)

    result = {
        "success": True,
        "swagger_path": swagger_path,
        "apis_count": len(apis),
        "test_files": test_files,
        "test_results": test_results,
        "report_path": report_path
    }

    if detailed_report_path:
        result["detailed_report_path"] = detailed_report_path

    return result


if __name__ == "__main__":
    # 命令行调用
    if len(sys.argv) < 2:
        print("用法: python pipeline.py <swagger_path>")
        print("示例: python pipeline.py swagger.json")
        sys.exit(1)

    swagger_path = sys.argv[1]
    result = run_swagger_pipeline(swagger_path)

    # 根据执行结果设置退出码
    sys.exit(0 if result["success"] else 1)
