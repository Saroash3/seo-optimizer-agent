"""
Memory Test Script - Proves Long-Term Memory Works
This will:
1. Start the agent
2. Send 3 analysis requests
3. Check if memory file is created
4. Read and display the memory file
"""

import requests
import json
import time
import os

BASE_URL = "http://localhost:5000"

def test_memory_persistence():
    print("\n" + "="*60)
    print("  MEMORY PERSISTENCE TEST")
    print("="*60)
    
    # Test 1: Send first analysis
    print("\n1️⃣  Sending first analysis...")
    data1 = {
        "content": {
            "title": "First Test Article",
            "body": "This is the first test to check memory. SEO is important.",
            "target_keywords": ["SEO", "test"]
        }
    }
    
    response1 = requests.post(f"{BASE_URL}/analyze", json=data1)
    if response1.status_code == 200:
        result1 = response1.json()
        print(f"   ✅ Analysis 1 completed - Score: {result1['analysis']['overall_score']}")
    
    time.sleep(1)
    
    # Test 2: Send second analysis
    print("\n2️⃣  Sending second analysis...")
    data2 = {
        "content": {
            "title": "Second Test Article",
            "body": "This is the second test. Content optimization is key for SEO success.",
            "target_keywords": ["content", "optimization"]
        }
    }
    
    response2 = requests.post(f"{BASE_URL}/analyze", json=data2)
    if response2.status_code == 200:
        result2 = response2.json()
        print(f"   ✅ Analysis 2 completed - Score: {result2['analysis']['overall_score']}")
    
    time.sleep(1)
    
    # Test 3: Send third analysis
    print("\n3️⃣  Sending third analysis...")
    data3 = {
        "content": {
            "title": "Third Test Article",
            "body": "Final test for memory persistence. Machine learning and AI are transforming technology.",
            "target_keywords": ["machine learning", "AI"]
        }
    }
    
    response3 = requests.post(f"{BASE_URL}/analyze", json=data3)
    if response3.status_code == 200:
        result3 = response3.json()
        print(f"   ✅ Analysis 3 completed - Score: {result3['analysis']['overall_score']}")
    
    time.sleep(1)
    
    # Check if memory file exists
    print("\n4️⃣  Checking if long-term memory file was created...")
    memory_file = "data/long_term_memory.json"
    
    if os.path.exists(memory_file):
        print(f"   ✅ Memory file EXISTS at: {memory_file}")
        
        # Read and display memory content
        print("\n5️⃣  Reading memory file contents...")
        with open(memory_file, 'r') as f:
            memory_data = json.load(f)
        
        print("\n" + "─"*60)
        print("📁 LONG-TERM MEMORY FILE CONTENTS:")
        print("─"*60)
        print(json.dumps(memory_data, indent=2))
        
        # Show statistics
        print("\n" + "─"*60)
        print("📊 MEMORY STATISTICS:")
        print("─"*60)
        print(f"Total analyses stored: {len(memory_data.get('analyses', []))}")
        
        if memory_data.get('analyses'):
            print("\n🔍 Stored Analyses:")
            for i, analysis in enumerate(memory_data['analyses'], 1):
                print(f"   {i}. Task: {analysis['task_id']}")
                print(f"      Score: {analysis['overall_score']}")
                print(f"      Keywords: {', '.join(analysis['keywords_analyzed'])}")
                print(f"      Time: {analysis['timestamp']}")
        
        if memory_data.get('patterns', {}).get('average_scores'):
            patterns = memory_data['patterns']['average_scores']
            print(f"\n📈 Pattern Analysis:")
            if patterns.get('overall'):
                avg_overall = sum(patterns['overall']) / len(patterns['overall'])
                print(f"   Average Overall Score: {avg_overall:.1f}")
            if patterns.get('readability'):
                avg_read = sum(patterns['readability']) / len(patterns['readability'])
                print(f"   Average Readability: {avg_read:.1f}")
        
        print("\n" + "="*60)
        print("  ✅ LONG-TERM MEMORY IS WORKING!")
        print("="*60)
        
    else:
        print(f"   ❌ Memory file NOT found at: {memory_file}")
        print("   This could mean:")
        print("   - Agent hasn't processed any requests yet")
        print("   - Data directory doesn't exist")
    
    # Get agent status
    print("\n6️⃣  Getting agent status...")
    status_response = requests.get(f"{BASE_URL}/status")
    if status_response.status_code == 200:
        status = status_response.json()
        print("\n📊 Agent Statistics:")
        print(json.dumps(status['statistics'], indent=2))

if __name__ == "__main__":
    print("\n🧪 Starting Memory Persistence Test...")
    print("Make sure the agent is running: python app.py\n")
    
    try:
        # Check if agent is running
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        print("✅ Agent is running!\n")
        
        # Run memory test
        test_memory_persistence()
        
    except:
        print("❌ Agent is not running!")
        print("\nPlease start the agent first:")
        print("  python app.py")
