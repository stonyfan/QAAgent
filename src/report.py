import os
import json
from datetime import datetime
from typing import Dict, Any, List


def get_risk_level(test_results: Dict[str, Any]) -> tuple:
    """
    根据测试结果计算风险等级

    Args:
        test_results: 测试结果字典

    Returns:
        (风险等级, 风险描述, 建议)
        风险等级: LOW / MEDIUM / HIGH / CRITICAL
    """
    if test_results['total'] == 0:
        return 'UNKNOWN', '无法评估', '没有可用的测试结果'

    pass_rate = (test_results['passed'] / test_results['total']) * 100

    if pass_rate == 100:
        return 'LOW', '低风险', '所有测试通过，系统质量良好'
    elif pass_rate >= 80:
        return 'MEDIUM', '中等风险', f'有 {test_results["failed"]} 个测试失败，建议检查失败的API'
    elif pass_rate >= 50:
        return 'HIGH', '高风险', f'超过 {(100-pass_rate):.0f}% 的测试失败，系统可能存在严重问题'
    else:
        return 'CRITICAL', '极高风险', f'大部分测试失败（{test_results["failed"]}/{test_results["total"]}），系统不可用'


def extract_failure_details(output: str) -> list:
    """
    从pytest输出中提取失败详情

    Args:
        output: pytest的完整输出

    Returns:
        失败详情列表
        [
            {
                "test_name": str,
                "error_type": str,
                "error_message": str,
                "file_line": str
            }
        ]
    """
    failures = []
    lines = output.split('\n')

    current_failure = None
    capture_next = False

    for line in lines:
        # 检测失败测试的开始
        if 'FAILED' in line and 'test_' in line:
            parts = line.split()
            test_name = parts[0] if parts else 'unknown'
            current_failure = {
                "test_name": test_name,
                "error_type": "",
                "error_message": "",
                "file_line": ""
            }
            capture_next = True
            continue

        # 捕获错误类型（如 AssertionError）
        if current_failure and capture_next:
            if 'Error' in line or 'Exception' in line:
                current_failure["error_type"] = line.strip()
            elif '.py:' in line:
                current_failure["file_line"] = line.strip()
            elif 'AssertionError' in line or 'assert' in line:
                current_failure["error_message"] = line.strip()

            # 如果信息收集完成，添加到列表
            if current_failure["error_type"] or current_failure["file_line"]:
                failures.append(current_failure)
                current_failure = None
                capture_next = False

    return failures


def generate_text_report(test_results: Dict[str, Any], source: str = "API测试") -> str:
    """
    生成增强版的文本格式测试报告

    Args:
        test_results: 测试结果字典
        source: 测试来源描述

    Returns:
        文本报告内容
    """
    report_lines = []

    # ===== 报告头部 =====
    report_lines.append("=" * 80)
    report_lines.append(f"API 测试报告".center(80))
    report_lines.append("=" * 80)
    report_lines.append(f"测试来源: {source}")
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # ===== 风险评估 =====
    risk_level, risk_desc, risk_advice = get_risk_level(test_results)
    risk_icon = {
        'LOW': '🟢',
        'MEDIUM': '🟡',
        'HIGH': '🟠',
        'CRITICAL': '🔴',
        'UNKNOWN': '⚪'
    }.get(risk_level, '⚪')

    report_lines.append("-" * 80)
    report_lines.append("⚠️  风险评估")
    report_lines.append("-" * 80)
    report_lines.append(f"风险等级: {risk_icon} {risk_level} - {risk_desc}")
    report_lines.append(f"建议: {risk_advice}")
    report_lines.append("")

    # ===== 测试统计 =====
    report_lines.append("-" * 80)
    report_lines.append("📊 测试统计")
    report_lines.append("-" * 80)

    total = test_results['total']
    passed = test_results['passed']
    failed = test_results['failed']

    report_lines.append(f"总测试数: {total} 个")
    report_lines.append(f"✅ 通过: {passed} 个")
    report_lines.append(f"❌ 失败: {failed} 个")

    if total > 0:
        pass_rate = (passed / total) * 100
        fail_rate = (failed / total) * 100

        # 通过率可视化条
        bar_length = 40
        filled = int(bar_length * pass_rate / 100)
        bar = '█' * filled + '░' * (bar_length - filled)
        report_lines.append(f"通过率: {pass_rate:.1f}% [{bar}]")
        report_lines.append(f"失败率: {fail_rate:.1f}%")

    report_lines.append("")

    # ===== 失败详情 =====
    if failed > 0:
        report_lines.append("-" * 80)
        report_lines.append("❌ 失败详情")
        report_lines.append("-" * 80)

        # 提取失败详情
        failure_details = extract_failure_details(test_results.get('output', ''))

        # 如果解析到了详细信息，使用详细信息
        if failure_details:
            for i, failure in enumerate(failure_details, 1):
                report_lines.append(f"{i}. 测试: {failure['test_name']}")
                if failure.get('error_type'):
                    report_lines.append(f"   错误类型: {failure['error_type']}")
                if failure.get('error_message'):
                    report_lines.append(f"   错误信息: {failure['error_message']}")
                if failure.get('file_line'):
                    report_lines.append(f"   位置: {failure['file_line']}")
                report_lines.append("")
        else:
            # 回退到简单的失败列表
            failed_tests = [t for t in test_results.get('tests', []) if t['status'] == 'failed']
            for i, test in enumerate(failed_tests, 1):
                report_lines.append(f"{i}. {test['name']}")
                if test.get('error'):
                    report_lines.append(f"   错误: {test['error']}")
                report_lines.append("")

        # 失败分析建议
        report_lines.append("🔍 失败分析建议:")
        if failed == 1:
            report_lines.append("   - 仅1个测试失败，可能是API接口变更或临时问题")
        elif failed <= 3:
            report_lines.append(f"   - 有{failed}个测试失败，建议检查相关API的可用性")
        else:
            report_lines.append(f"   - 大量测试失败（{failed}个），可能存在系统性问题")
            report_lines.append("   - 建议：检查API服务是否正常运行")
            report_lines.append("   - 建议：验证API文档是否更新")

        report_lines.append("")

    # ===== 通过的测试（简要列表） =====
    if passed > 0:
        report_lines.append("-" * 80)
        report_lines.append(f"✅ 通过的测试 ({passed}个)")
        report_lines.append("-" * 80)

        passed_tests = [t for t in test_results.get('tests', []) if t['status'] == 'passed']
        for test in passed_tests[:10]:  # 最多显示10个
            report_lines.append(f"  ✓ {test['name']}")

        if len(passed_tests) > 10:
            report_lines.append(f"  ... 还有 {len(passed_tests) - 10} 个测试通过")

        report_lines.append("")

    # ===== 完整输出（可选） =====
    if failed > 0:
        report_lines.append("-" * 80)
        report_lines.append("📄 完整测试输出")
        report_lines.append("-" * 80)
        output = test_results.get('output', '')
        # 限制输出长度，避免过长
        if len(output) > 2000:
            output = output[:2000] + "\n... (输出已截断)"
        report_lines.append(output)
        report_lines.append("")

    # ===== 报告尾部 =====
    report_lines.append("=" * 80)
    report_lines.append(f"报告生成完毕 | QA Agent v0.1.0".center(80))
    report_lines.append("=" * 80)

    return "\n".join(report_lines)


def save_report(report_content: str, output_path: str) -> None:
    """
    保存报告到文件

    Args:
        report_content: 报告内容
        output_path: 输出文件路径
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_content)


def generate_and_save_report(test_results: Dict[str, Any], source: str, output_dir: str = 'reports') -> str:
    """
    生成并保存测试报告

    Args:
        test_results: 测试结果字典
        source: 测试来源描述
        output_dir: 报告输出目录

    Returns:
        报告文件路径
    """
    # 生成报告
    report_content = generate_text_report(test_results, source)

    # 生成文件名（固定名称，时间戳在目录中）
    report_filename = 'API测试报告.txt'
    report_path = os.path.join(output_dir, report_filename)

    # 保存报告
    save_report(report_content, report_path)

    return report_path


def read_detailed_log(log_file_path: str) -> List[Dict[str, Any]]:
    """
    读取详细日志文件（JSON Lines格式）

    Args:
        log_file_path: 日志文件路径

    Returns:
        日志条目列表
    """
    if not os.path.exists(log_file_path):
        return []

    log_entries = []
    with open(log_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                log_entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

    return log_entries


def generate_detailed_report(log_entries: List[Dict[str, Any]], source: str) -> str:
    """
    生成详细的API测试报告

    Args:
        log_entries: 日志条目列表
        source: 测试来源描述

    Returns:
        详细报告内容
    """
    if not log_entries:
        return "没有可用的详细日志数据"

    report_lines = []

    # 报告头部
    report_lines.append("=" * 100)
    report_lines.append(f"{'API测试详细报告'.center(100)}")
    report_lines.append("=" * 100)
    report_lines.append(f"测试来源: {source}")
    report_lines.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"总请求数: {len(log_entries)}")
    report_lines.append("")

    # 按测试分组
    grouped = {}
    for entry in log_entries:
        test_name = entry.get('test_name', 'unknown')
        if test_name not in grouped:
            grouped[test_name] = []
        grouped[test_name].append(entry)

    # 为每个测试生成详情
    for idx, (test_name, entries) in enumerate(grouped.items(), 1):
        report_lines.append("=" * 100)
        report_lines.append(f"[{idx}/{len(grouped)}] 测试: {test_name}")
        report_lines.append("=" * 100)
        report_lines.append("")

        for entry_idx, entry in enumerate(entries, 1):
            report_lines.append("-" * 100)
            report_lines.append(f"执行 #{entry_idx} - {entry.get('timestamp', 'N/A')}")
            report_lines.append("-" * 100)

            # 请求信息
            request = entry.get('request', {})
            report_lines.append("📤 请求信息:")
            report_lines.append(f"  方法: {request.get('method', 'N/A')}")
            report_lines.append(f"  URL: {request.get('url', 'N/A')}")

            request_body = request.get('body')
            if request_body:
                report_lines.append(f"  请求体: {json.dumps(request_body, ensure_ascii=False, indent=2)}")

            report_lines.append("")

            # 响应信息
            response = entry.get('response', {})
            report_lines.append("📥 响应信息:")
            report_lines.append(f"  状态码: {response.get('status_code', 'N/A')}")

            response_time = response.get('response_time_ms', 0)
            report_lines.append(f"  响应时间: {response_time:.2f} ms")

            # 响应头
            headers = response.get('headers', {})
            if headers:
                report_lines.append("  响应头:")
                for key, value in headers.items():
                    report_lines.append(f"    {key}: {value}")

            report_lines.append("")

            # 响应体
            body = response.get('body', '')
            if body:
                report_lines.append("  响应体:")
                try:
                    body_json = json.loads(body)
                    report_lines.append(f"    {json.dumps(body_json, ensure_ascii=False, indent=2)}")
                except:
                    # 如果不是JSON，直接显示
                    for line in body.split('\n')[:10]:  # 只显示前10行
                        report_lines.append(f"    {line}")
                    if len(body.split('\n')) > 10:
                        report_lines.append("    ... (内容已截断)")

            report_lines.append("")

        report_lines.append("")

    # 报告尾部
    report_lines.append("=" * 100)
    report_lines.append(f"{'详细报告生成完毕'.center(100)}")
    report_lines.append("=" * 100)

    return "\n".join(report_lines)


def generate_and_save_detailed_report(source: str, output_dir: str = 'reports') -> str:
    """
    生成并保存详细测试报告

    Args:
        source: 测试来源描述
        output_dir: 报告输出目录

    Returns:
        详细报告文件路径
    """
    # 尝试多个位置查找日志文件
    log_file = os.path.join(output_dir, 'api_detailed_log.jsonl')

    # 如果在子目录中找不到，尝试在reports根目录查找
    if not os.path.exists(log_file):
        # 从output_dir提取reports根目录
        # 兼容Windows和Unix路径分隔符
        if output_dir.startswith('reports/') or output_dir.startswith('reports\\'):
            reports_root = 'reports'
            log_file = os.path.join(reports_root, 'api_detailed_log.jsonl')

    if not os.path.exists(log_file):
        return None

    log_entries = read_detailed_log(log_file)

    # 生成详细报告
    report_content = generate_detailed_report(log_entries, source)

    # 生成文件名（固定名称，时间戳在目录中）
    report_filename = 'API测试详细报告.txt'
    report_path = os.path.join(output_dir, report_filename)

    # 保存报告
    save_report(report_content, report_path)

    # 清理日志文件（可选）
    try:
        os.remove(log_file)
    except:
        pass

    return report_path
