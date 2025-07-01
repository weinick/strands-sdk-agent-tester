#!/usr/bin/env python3
"""
Master Test Runner for Strands SDK Agent UI Tests
Orchestrates all UI testing suites and generates comprehensive reports
"""

import sys
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class MasterUITestRunner:
    """Master test runner for all UI tests"""
    
    def __init__(self):
        self.project_root = project_root
        self.test_results = {}
        self.start_time = None
        self.end_time = None
        
    def run_all_tests(self, include_scenarios: bool = True) -> Dict[str, Any]:
        """Run all UI test suites"""
        print("🚀 STRANDS SDK AGENTS - MASTER UI TEST SUITE")
        print("=" * 80)
        print("Comprehensive testing of all 6 agents through Streamlit UI")
        print("Simulating real user interactions and validating responses")
        print("=" * 80)
        
        self.start_time = datetime.now()
        
        # Test suites to run
        test_suites = [
            {
                "name": "Basic Agents UI Tests",
                "module": "test_ui_basic_agents",
                "function": "run_basic_agents_tests",
                "description": "Tests Simple Agent, Agent with Tools, and Custom Tool Agent"
            },
            {
                "name": "Advanced Agents UI Tests", 
                "module": "test_ui_advanced_agents",
                "function": "run_advanced_agents_tests",
                "description": "Tests Web Research Agent, File Manager Agent, and Multi Agent System"
            }
        ]
        
        if include_scenarios:
            test_suites.append({
                "name": "User Scenario Tests",
                "module": "test_user_scenarios", 
                "function": "run_user_scenario_tests",
                "description": "Simulates realistic user interactions and conversation flows"
            })
        
        # Run each test suite
        for i, suite in enumerate(test_suites, 1):
            print(f"\n📋 Running Test Suite {i}/{len(test_suites)}: {suite['name']}")
            print(f"   {suite['description']}")
            print("-" * 60)
            
            try:
                # Import and run the test function
                module = __import__(f"tests.{suite['module']}", fromlist=[suite['function']])
                test_function = getattr(module, suite['function'])
                
                suite_start = time.time()
                result = test_function()
                suite_duration = time.time() - suite_start
                
                self.test_results[suite['name']] = {
                    "result": result,
                    "duration": suite_duration,
                    "success": True,
                    "timestamp": datetime.now().isoformat()
                }
                
                print(f"✅ {suite['name']} completed in {suite_duration:.1f}s")
                
            except Exception as e:
                print(f"❌ {suite['name']} failed: {e}")
                self.test_results[suite['name']] = {
                    "error": str(e),
                    "success": False,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Brief pause between test suites
            if i < len(test_suites):
                print("\n⏳ Preparing next test suite...")
                time.sleep(2)
        
        self.end_time = datetime.now()
        
        # Generate master report
        self._generate_master_report()
        
        return self.test_results
    
    def _generate_master_report(self):
        """Generate comprehensive master test report"""
        print("\n" + "=" * 100)
        print("📊 MASTER UI TEST REPORT")
        print("=" * 100)
        
        total_duration = (self.end_time - self.start_time).total_seconds()
        
        print(f"🕐 Test Execution Time: {total_duration:.1f} seconds")
        print(f"📅 Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📅 Completed: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Analyze results from each test suite
        suite_summary = {}
        total_agents_tested = 0
        total_tests_run = 0
        total_tests_passed = 0
        
        for suite_name, suite_data in self.test_results.items():
            if not suite_data.get("success", False):
                suite_summary[suite_name] = {
                    "status": "❌ FAILED",
                    "error": suite_data.get("error", "Unknown error")
                }
                continue
            
            result = suite_data.get("result", {})
            
            # Analyze different result formats
            if isinstance(result, dict):
                if "Simple Agent" in result:  # Basic/Advanced agents format
                    agents_in_suite = len(result)
                    tests_in_suite = 0
                    passed_in_suite = 0
                    
                    for agent_name, agent_result in result.items():
                        if isinstance(agent_result, dict):
                            if "total_tests" in agent_result:
                                tests_in_suite += agent_result.get("total_tests", 0)
                                passed_in_suite += agent_result.get("passed_tests", 0)
                            elif isinstance(agent_result, list):  # Scenario format
                                tests_in_suite += len(agent_result)
                                passed_in_suite += sum(1 for s in agent_result if s.get("success", False))
                    
                    total_agents_tested += agents_in_suite
                    total_tests_run += tests_in_suite
                    total_tests_passed += passed_in_suite
                    
                    success_rate = passed_in_suite / tests_in_suite if tests_in_suite > 0 else 0
                    
                    suite_summary[suite_name] = {
                        "status": "✅ PASSED" if success_rate >= 0.6 else "⚠️ PARTIAL" if success_rate >= 0.3 else "❌ FAILED",
                        "agents": agents_in_suite,
                        "tests": tests_in_suite,
                        "passed": passed_in_suite,
                        "success_rate": success_rate,
                        "duration": suite_data.get("duration", 0)
                    }
        
        # Display suite summaries
        print(f"\n📋 TEST SUITE SUMMARIES:")
        print("-" * 50)
        
        for suite_name, summary in suite_summary.items():
            print(f"\n{summary['status']} {suite_name}")
            if "error" in summary:
                print(f"   Error: {summary['error']}")
            else:
                print(f"   Agents: {summary.get('agents', 0)}")
                print(f"   Tests: {summary.get('passed', 0)}/{summary.get('tests', 0)} passed ({summary.get('success_rate', 0):.1%})")
                print(f"   Duration: {summary.get('duration', 0):.1f}s")
        
        # Overall statistics
        overall_success_rate = total_tests_passed / total_tests_run if total_tests_run > 0 else 0
        
        print(f"\n🎯 OVERALL STATISTICS:")
        print("-" * 30)
        print(f"   Total Agents Tested: {total_agents_tested}")
        print(f"   Total Tests Run: {total_tests_run}")
        print(f"   Total Tests Passed: {total_tests_passed}")
        print(f"   Overall Success Rate: {overall_success_rate:.1%}")
        print(f"   Total Duration: {total_duration:.1f}s")
        
        # Final assessment
        print(f"\n🏆 FINAL ASSESSMENT:")
        print("-" * 25)
        
        if overall_success_rate >= 0.8:
            assessment = "🎉 OUTSTANDING"
            message = "All agents are performing excellently! Ready for production use."
        elif overall_success_rate >= 0.6:
            assessment = "✅ GOOD"
            message = "Most agents are working well. Minor improvements may be beneficial."
        elif overall_success_rate >= 0.4:
            assessment = "⚠️ FAIR"
            message = "Agents are functional but need improvements for optimal user experience."
        else:
            assessment = "❌ NEEDS WORK"
            message = "Significant improvements needed before production deployment."
        
        print(f"   Status: {assessment}")
        print(f"   Recommendation: {message}")
        
        # Save master report
        self._save_master_report(overall_success_rate, total_duration)
    
    def _save_master_report(self, success_rate: float, duration: float):
        """Save master test report to file"""
        report_data = {
            "test_execution": {
                "start_time": self.start_time.isoformat(),
                "end_time": self.end_time.isoformat(),
                "duration_seconds": duration,
                "timestamp": datetime.now().isoformat()
            },
            "summary": {
                "overall_success_rate": success_rate,
                "total_test_suites": len(self.test_results),
                "successful_suites": sum(1 for r in self.test_results.values() if r.get("success", False))
            },
            "detailed_results": self.test_results
        }
        
        # Save JSON report
        report_file = self.project_root / "tests" / "master_ui_test_report.json"
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2, default=str)
        
        # Save human-readable report
        readable_report = self.project_root / "tests" / "UI_TEST_REPORT.md"
        with open(readable_report, 'w') as f:
            f.write(f"# Strands SDK Agents - UI Test Report\n\n")
            f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"## Summary\n\n")
            f.write(f"- **Overall Success Rate:** {success_rate:.1%}\n")
            f.write(f"- **Test Duration:** {duration:.1f} seconds\n")
            f.write(f"- **Test Suites:** {len(self.test_results)}\n\n")
            f.write(f"## Test Results\n\n")
            
            for suite_name, suite_data in self.test_results.items():
                status = "✅ PASSED" if suite_data.get("success", False) else "❌ FAILED"
                f.write(f"### {status} {suite_name}\n\n")
                if suite_data.get("success", False):
                    f.write(f"- Duration: {suite_data.get('duration', 0):.1f}s\n")
                else:
                    f.write(f"- Error: {suite_data.get('error', 'Unknown error')}\n")
                f.write(f"\n")
        
        print(f"\n💾 Reports saved:")
        print(f"   📄 JSON Report: {report_file}")
        print(f"   📄 Readable Report: {readable_report}")

def run_quick_test():
    """Run a quick test of basic functionality"""
    print("⚡ QUICK UI TEST")
    print("=" * 40)
    print("Running basic functionality tests only")
    
    runner = MasterUITestRunner()
    return runner.run_all_tests(include_scenarios=False)

def run_comprehensive_test():
    """Run comprehensive test including user scenarios"""
    print("🔬 COMPREHENSIVE UI TEST")
    print("=" * 40)
    print("Running all tests including user scenarios")
    
    runner = MasterUITestRunner()
    return runner.run_all_tests(include_scenarios=True)

def check_test_environment():
    """Check if the test environment is ready"""
    print("🔍 Checking Test Environment")
    print("-" * 30)
    
    checks = []
    
    # Check if required modules exist
    required_files = [
        "ui/streamlit_ui.py",
        "ui/agent_runner.py", 
        "tests/test_ui_basic_agents.py",
        "tests/test_ui_advanced_agents.py",
        "tests/test_user_scenarios.py"
    ]
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            checks.append(f"✅ {file_path}")
        else:
            checks.append(f"❌ {file_path} - MISSING")
    
    # Check Python dependencies
    try:
        import streamlit
        checks.append("✅ Streamlit available")
    except ImportError:
        checks.append("❌ Streamlit not installed")
    
    try:
        import requests
        checks.append("✅ Requests available")
    except ImportError:
        checks.append("❌ Requests not installed")
    
    for check in checks:
        print(f"   {check}")
    
    missing_count = sum(1 for check in checks if check.startswith("❌"))
    
    if missing_count == 0:
        print("\n✅ Environment is ready for testing!")
        return True
    else:
        print(f"\n❌ Environment has {missing_count} issues. Please resolve before testing.")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Strands SDK Agent UI Tests")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    parser.add_argument("--check", action="store_true", help="Check test environment")
    parser.add_argument("--comprehensive", action="store_true", help="Run comprehensive tests")
    
    args = parser.parse_args()
    
    if args.check:
        check_test_environment()
    elif args.quick:
        run_quick_test()
    elif args.comprehensive:
        run_comprehensive_test()
    else:
        # Default: run comprehensive tests
        if check_test_environment():
            run_comprehensive_test()
        else:
            print("❌ Cannot run tests due to environment issues.")
