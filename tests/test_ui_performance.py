#!/usr/bin/env python3
"""
Performance and Load Testing for Strands SDK Agent UI
Tests response times, concurrent users, and system stability
"""

import sys
import time
import asyncio
import threading
import statistics
from pathlib import Path
from typing import Dict, List, Any, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class UIPerformanceTester:
    """Performance tester for UI agent interactions"""
    
    def __init__(self):
        self.project_root = project_root
        self.performance_results = {}
    
    def measure_response_time(self, agent_name: str, message: str, iterations: int = 5) -> Dict[str, Any]:
        """Measure response time for a specific agent and message"""
        print(f"⏱️ Measuring response time for {agent_name}")
        print(f"   Message: {message}")
        print(f"   Iterations: {iterations}")
        
        try:
            from ui.agent_runner import AgentRunner
            
            agent_runner = AgentRunner(str(self.project_root))
            model_config = {
                "provider": "bedrock",
                "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
                "temperature": 0.7,
                "max_tokens": 1000
            }
            
            response_times = []
            response_lengths = []
            successful_requests = 0
            
            for i in range(iterations):
                print(f"   Iteration {i+1}/{iterations}...", end=" ")
                
                start_time = time.time()
                try:
                    response = agent_runner.run_agent(agent_name, model_config, message)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    response_times.append(response_time)
                    response_lengths.append(len(response))
                    successful_requests += 1
                    
                    print(f"{response_time:.2f}s ✅")
                    
                except Exception as e:
                    end_time = time.time()
                    response_time = end_time - start_time
                    print(f"{response_time:.2f}s ❌ ({str(e)[:50]})")
                
                # Small delay between iterations
                time.sleep(0.5)
            
            if response_times:
                result = {
                    "agent_name": agent_name,
                    "message": message,
                    "iterations": iterations,
                    "successful_requests": successful_requests,
                    "success_rate": successful_requests / iterations,
                    "response_times": {
                        "min": min(response_times),
                        "max": max(response_times),
                        "mean": statistics.mean(response_times),
                        "median": statistics.median(response_times),
                        "std_dev": statistics.stdev(response_times) if len(response_times) > 1 else 0
                    },
                    "response_lengths": {
                        "min": min(response_lengths) if response_lengths else 0,
                        "max": max(response_lengths) if response_lengths else 0,
                        "mean": statistics.mean(response_lengths) if response_lengths else 0
                    }
                }
                
                print(f"   📊 Results:")
                print(f"      Success Rate: {result['success_rate']:.1%}")
                print(f"      Avg Response Time: {result['response_times']['mean']:.2f}s")
                print(f"      Response Time Range: {result['response_times']['min']:.2f}s - {result['response_times']['max']:.2f}s")
                
                return result
            else:
                return {
                    "agent_name": agent_name,
                    "message": message,
                    "error": "No successful responses",
                    "success_rate": 0
                }
                
        except Exception as e:
            return {
                "agent_name": agent_name,
                "message": message,
                "error": str(e),
                "success_rate": 0
            }
    
    def test_concurrent_users(self, agent_name: str, message: str, concurrent_users: int = 3) -> Dict[str, Any]:
        """Test concurrent user interactions"""
        print(f"👥 Testing concurrent users for {agent_name}")
        print(f"   Concurrent Users: {concurrent_users}")
        print(f"   Message: {message}")
        
        def single_user_request(user_id: int) -> Dict[str, Any]:
            """Single user request for concurrent testing"""
            try:
                from ui.agent_runner import AgentRunner
                
                agent_runner = AgentRunner(str(self.project_root))
                model_config = {
                    "provider": "bedrock",
                    "model": "anthropic.claude-3-5-sonnet-20241022-v2:0",
                    "temperature": 0.7,
                    "max_tokens": 1000
                }
                
                start_time = time.time()
                response = agent_runner.run_agent(agent_name, model_config, message)
                end_time = time.time()
                
                return {
                    "user_id": user_id,
                    "success": True,
                    "response_time": end_time - start_time,
                    "response_length": len(response),
                    "timestamp": start_time
                }
                
            except Exception as e:
                return {
                    "user_id": user_id,
                    "success": False,
                    "error": str(e),
                    "response_time": time.time() - start_time if 'start_time' in locals() else 0
                }
        
        # Execute concurrent requests
        start_time = time.time()
        results = []
        
        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            # Submit all requests
            future_to_user = {
                executor.submit(single_user_request, user_id): user_id 
                for user_id in range(1, concurrent_users + 1)
            }
            
            # Collect results
            for future in as_completed(future_to_user):
                user_id = future_to_user[future]
                try:
                    result = future.result()
                    results.append(result)
                    status = "✅" if result.get("success", False) else "❌"
                    print(f"   User {user_id}: {status} {result.get('response_time', 0):.2f}s")
                except Exception as e:
                    results.append({
                        "user_id": user_id,
                        "success": False,
                        "error": str(e)
                    })
                    print(f"   User {user_id}: ❌ {str(e)}")
        
        total_time = time.time() - start_time
        successful_requests = sum(1 for r in results if r.get("success", False))
        
        # Analyze results
        if successful_requests > 0:
            successful_results = [r for r in results if r.get("success", False)]
            response_times = [r["response_time"] for r in successful_results]
            
            concurrent_result = {
                "agent_name": agent_name,
                "message": message,
                "concurrent_users": concurrent_users,
                "total_requests": len(results),
                "successful_requests": successful_requests,
                "success_rate": successful_requests / len(results),
                "total_execution_time": total_time,
                "response_times": {
                    "min": min(response_times),
                    "max": max(response_times),
                    "mean": statistics.mean(response_times),
                    "median": statistics.median(response_times)
                },
                "throughput": successful_requests / total_time,
                "individual_results": results
            }
            
            print(f"   📊 Concurrent Test Results:")
            print(f"      Success Rate: {concurrent_result['success_rate']:.1%}")
            print(f"      Throughput: {concurrent_result['throughput']:.2f} requests/second")
            print(f"      Avg Response Time: {concurrent_result['response_times']['mean']:.2f}s")
            
            return concurrent_result
        else:
            return {
                "agent_name": agent_name,
                "message": message,
                "concurrent_users": concurrent_users,
                "error": "No successful concurrent requests",
                "success_rate": 0
            }
    
    def test_agent_performance_profile(self, agent_name: str) -> Dict[str, Any]:
        """Create a comprehensive performance profile for an agent"""
        print(f"\n🔬 Creating Performance Profile for {agent_name}")
        print("=" * 50)
        
        # Test messages of varying complexity
        test_cases = [
            {
                "type": "Simple",
                "message": "Hello, how are you?",
                "expected_time": 3.0  # seconds
            },
            {
                "type": "Medium",
                "message": "Can you help me understand how AI agents work and what they can do?",
                "expected_time": 5.0
            },
            {
                "type": "Complex",
                "message": "I need a detailed analysis of the benefits and challenges of implementing AI agents in business workflows, including specific use cases and potential ROI considerations.",
                "expected_time": 8.0
            }
        ]
        
        profile_results = {
            "agent_name": agent_name,
            "test_cases": {},
            "concurrent_test": {},
            "performance_grade": "Unknown"
        }
        
        # Test each complexity level
        for test_case in test_cases:
            print(f"\n📝 Testing {test_case['type']} Query")
            result = self.measure_response_time(
                agent_name, 
                test_case['message'], 
                iterations=3
            )
            profile_results["test_cases"][test_case['type']] = result
        
        # Test concurrent users
        print(f"\n👥 Testing Concurrent Users")
        concurrent_result = self.test_concurrent_users(
            agent_name,
            "What can you help me with?",
            concurrent_users=3
        )
        profile_results["concurrent_test"] = concurrent_result
        
        # Calculate performance grade
        grade = self._calculate_performance_grade(profile_results)
        profile_results["performance_grade"] = grade
        
        print(f"\n🏆 Performance Grade for {agent_name}: {grade}")
        
        return profile_results
    
    def _calculate_performance_grade(self, profile_results: Dict[str, Any]) -> str:
        """Calculate overall performance grade"""
        scores = []
        
        # Evaluate response time performance
        for test_type, result in profile_results.get("test_cases", {}).items():
            if result.get("success_rate", 0) > 0:
                avg_time = result.get("response_times", {}).get("mean", 10)
                success_rate = result.get("success_rate", 0)
                
                # Score based on response time and success rate
                time_score = max(0, 100 - (avg_time * 10))  # Penalty for slow responses
                success_score = success_rate * 100
                combined_score = (time_score + success_score) / 2
                scores.append(combined_score)
        
        # Evaluate concurrent performance
        concurrent_result = profile_results.get("concurrent_test", {})
        if concurrent_result.get("success_rate", 0) > 0:
            concurrent_success = concurrent_result.get("success_rate", 0) * 100
            scores.append(concurrent_success)
        
        if scores:
            avg_score = statistics.mean(scores)
            
            if avg_score >= 90:
                return "A+ (Excellent)"
            elif avg_score >= 80:
                return "A (Very Good)"
            elif avg_score >= 70:
                return "B (Good)"
            elif avg_score >= 60:
                return "C (Fair)"
            elif avg_score >= 50:
                return "D (Poor)"
            else:
                return "F (Failing)"
        else:
            return "F (No Data)"

def run_performance_tests():
    """Run comprehensive performance tests for all agents"""
    print("⚡ STRANDS SDK AGENTS - PERFORMANCE TESTING SUITE")
    print("=" * 80)
    print("Testing response times, concurrent users, and system stability")
    print("=" * 80)
    
    tester = UIPerformanceTester()
    
    # Agents to test
    agents_to_test = [
        "Simple Agent",
        "Agent with Tools", 
        "Custom Tool Agent",
        "Web Research Agent",
        "File Manager Agent",
        "Multi Agent System"
    ]
    
    all_results = {}
    
    for i, agent_name in enumerate(agents_to_test, 1):
        print(f"\n🤖 Testing Agent {i}/{len(agents_to_test)}: {agent_name}")
        print("=" * 60)
        
        try:
            profile = tester.test_agent_performance_profile(agent_name)
            all_results[agent_name] = profile
        except Exception as e:
            print(f"❌ Failed to test {agent_name}: {e}")
            all_results[agent_name] = {
                "agent_name": agent_name,
                "error": str(e),
                "performance_grade": "F (Error)"
            }
        
        # Brief pause between agents
        if i < len(agents_to_test):
            print("\n⏳ Preparing next agent test...")
            time.sleep(2)
    
    # Generate performance report
    print("\n" + "=" * 100)
    print("⚡ PERFORMANCE TEST RESULTS")
    print("=" * 100)
    
    for agent_name, result in all_results.items():
        grade = result.get("performance_grade", "Unknown")
        print(f"\n🏆 {agent_name}: {grade}")
        
        if "error" not in result:
            # Show key metrics
            test_cases = result.get("test_cases", {})
            for test_type, test_result in test_cases.items():
                if test_result.get("success_rate", 0) > 0:
                    avg_time = test_result.get("response_times", {}).get("mean", 0)
                    success_rate = test_result.get("success_rate", 0)
                    print(f"   {test_type}: {avg_time:.2f}s avg, {success_rate:.1%} success")
            
            concurrent = result.get("concurrent_test", {})
            if concurrent.get("success_rate", 0) > 0:
                throughput = concurrent.get("throughput", 0)
                print(f"   Concurrent: {throughput:.2f} req/s throughput")
    
    # Save performance results
    results_file = project_root / "tests" / "performance_test_results.json"
    with open(results_file, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    
    print(f"\n💾 Performance results saved to: {results_file}")
    
    return all_results

if __name__ == "__main__":
    run_performance_tests()
