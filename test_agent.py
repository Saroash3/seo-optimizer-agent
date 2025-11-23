"""
Test Script for SEO Optimizer Agent
Run this to test the agent's functionality
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_health_check():
    """Test the health check endpoint"""
    print_section("Testing Health Check")
    
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_registration():
    """Test agent registration"""
    print_section("Testing Registration")
    
    data = {
        "supervisor_id": "supervisor_test_001",
        "supervisor_url": "http://localhost:5001"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/register",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(data)
        )
        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_seo_analysis():
    """Test SEO content analysis"""
    print_section("Testing SEO Analysis")
    
    # Sample content for analysis
    test_content = {
        "task_id": "test_task_001",
        "task_type": "analyze_content",
        "content": {
            "title": "10 Best Practices for Modern Web Development",
            "body": """
# Introduction to Web Development

Web development has evolved significantly over the years. Modern web development 
requires knowledge of multiple technologies and best practices.

## Key Technologies

Understanding HTML, CSS, and JavaScript is fundamental. These technologies form 
the backbone of web development. Modern frameworks like React and Vue make 
development faster and more efficient.

## Best Practices

1. Write clean, maintainable code
2. Follow web development standards
3. Optimize for performance
4. Ensure responsive design
5. Implement proper SEO techniques

Web development is not just about writing code. It's about creating experiences 
that users love. Good web development practices lead to better websites and 
happier users.

## Conclusion

Modern web development continues to evolve. Staying updated with the latest 
trends and best practices is essential for success in this field.
            """,
            "target_keywords": ["web development", "best practices", "modern"],
            "url": "https://example.com/web-dev-practices"
        },
        "options": {
            "detailed_analysis": True
        }
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/analyze",
            headers={'Content-Type': 'application/json'},
            data=json.dumps(test_content)
        )
        print(f"Status Code: {response.status_code}")
        
        result = response.json()
        print("\n📊 Analysis Results:")
        print("-" * 60)
        
        if result['status'] == 'success':
            analysis = result['analysis']
            
            print(f"\n✅ Overall SEO Score: {analysis['overall_score']}/100")
            
            print("\n📝 Keyword Analysis:")
            for keyword, data in analysis['keyword_analysis']['keywords'].items():
                print(f"  • '{keyword}': {data['count']} occurrences, "
                      f"{data['density']}% density - {data['status']}")
            
            print(f"\n📖 Readability:")
            print(f"  • Score: {analysis['readability']['score']}")
            print(f"  • Level: {analysis['readability']['level']}")
            print(f"  • Grade: {analysis['readability']['grade']}")
            
            print(f"\n🏷️  Meta Analysis:")
            print(f"  • Title Length: {analysis['meta_analysis']['title_length']} chars")
            print(f"  • Title Quality: {analysis['meta_analysis']['title_quality']}")
            
            print(f"\n📑 Heading Structure:")
            print(f"  • H1 Count: {analysis['heading_structure']['h1_count']}")
            print(f"  • H2 Count: {analysis['heading_structure']['h2_count']}")
            print(f"  • Structure Quality: {analysis['heading_structure']['structure_quality']}")
            
            print(f"\n📄 Content Quality:")
            print(f"  • Word Count: {analysis['content_quality']['word_count']}")
            print(f"  • Length Quality: {analysis['content_quality']['length_quality']}")
            
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(analysis['recommendations'], 1):
                print(f"  {i}. {rec}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_status():
    """Test status endpoint"""
    print_section("Testing Status Endpoint")
    
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"Status Code: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_history():
    """Test history retrieval"""
    print_section("Testing History Retrieval")
    
    task_id = "test_task_001"
    
    try:
        response = requests.get(f"{BASE_URL}/history/{task_id}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Successfully retrieved task history")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"Task {task_id} not found (expected if this is first run)")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🚀 SEO Optimizer Agent Test Suite ".center(60, "="))
    print("Starting tests...\n")
    
    # Check if server is running
    print("⏳ Checking if server is running...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print("✅ Server is running!\n")
    except:
        print("❌ Server is not running!")
        print("\nPlease start the server first:")
        print("  python app.py")
        return
    
    # Run tests
    results = {
        "Health Check": test_health_check(),
        "Registration": test_registration(),
        "SEO Analysis": test_seo_analysis(),
        "Status Check": test_status(),
        "History Retrieval": test_history()
    }
    
    # Print summary
    print_section("Test Summary")
    passed = sum(results.values())
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:<20}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed successfully!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")

if __name__ == "__main__":
    main()
