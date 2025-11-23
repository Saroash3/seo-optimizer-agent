"""
Sample Supervisor Script
Demonstrates how a Supervisor would interact with the SEO Optimizer Agent
This is a mock supervisor for testing and demonstration purposes
"""

import requests
import json
import time
from datetime import datetime

class SimpleSupervisor:
    """
    Mock Supervisor for testing agent communication
    """
    
    def __init__(self, supervisor_id="supervisor_001"):
        self.supervisor_id = supervisor_id
        self.registered_agents = {}
        self.task_queue = []
        self.results = {}
    
    def discover_agent(self, agent_url):
        """
        Discover and register an agent
        """
        print(f"\n🔍 Discovering agent at {agent_url}...")
        
        try:
            # Check agent health
            health_response = requests.get(f"{agent_url}/health", timeout=5)
            
            if health_response.status_code == 200:
                health_data = health_response.json()
                print(f"✅ Agent is healthy: {health_data['agent_name']}")
                
                # Register agent
                registration_data = {
                    "supervisor_id": self.supervisor_id,
                    "supervisor_url": "http://localhost:5001",
                    "timestamp": datetime.now().isoformat()
                }
                
                reg_response = requests.post(
                    f"{agent_url}/register",
                    headers={'Content-Type': 'application/json'},
                    data=json.dumps(registration_data)
                )
                
                if reg_response.status_code == 200:
                    agent_info = reg_response.json()
                    self.registered_agents[agent_info['agent_id']] = {
                        "url": agent_url,
                        "info": agent_info,
                        "status": "active"
                    }
                    print(f"✅ Agent registered: {agent_info['agent_id']}")
                    print(f"   Capabilities: {', '.join(agent_info['capabilities'])}")
                    return agent_info['agent_id']
                else:
                    print(f"❌ Registration failed: {reg_response.status_code}")
                    return None
            else:
                print(f"❌ Agent health check failed: {health_response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error discovering agent: {e}")
            return None
    
    def assign_task(self, agent_id, task_data):
        """
        Assign a task to a specific agent
        """
        if agent_id not in self.registered_agents:
            print(f"❌ Agent {agent_id} not registered")
            return None
        
        agent = self.registered_agents[agent_id]
        agent_url = agent['url']
        
        print(f"\n📤 Assigning task to agent {agent_id}...")
        print(f"   Task Type: {task_data.get('task_type')}")
        
        try:
            response = requests.post(
                f"{agent_url}/analyze",
                headers={'Content-Type': 'application/json'},
                data=json.dumps(task_data),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                task_id = result.get('task_id')
                self.results[task_id] = result
                
                print(f"✅ Task completed successfully")
                print(f"   Task ID: {task_id}")
                print(f"   Overall Score: {result['analysis']['overall_score']}/100")
                
                return result
            else:
                print(f"❌ Task failed: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error assigning task: {e}")
            return None
    
    def get_agent_status(self, agent_id):
        """
        Get status of a specific agent
        """
        if agent_id not in self.registered_agents:
            print(f"❌ Agent {agent_id} not registered")
            return None
        
        agent = self.registered_agents[agent_id]
        agent_url = agent['url']
        
        try:
            response = requests.get(f"{agent_url}/status", timeout=5)
            
            if response.status_code == 200:
                return response.json()
            else:
                return None
                
        except Exception as e:
            print(f"❌ Error getting agent status: {e}")
            return None
    
    def monitor_agents(self):
        """
        Monitor health of all registered agents
        """
        print("\n🔍 Monitoring Registered Agents")
        print("-" * 60)
        
        for agent_id, agent_data in self.registered_agents.items():
            agent_url = agent_data['url']
            
            try:
                response = requests.get(f"{agent_url}/health", timeout=3)
                
                if response.status_code == 200:
                    health = response.json()
                    print(f"✅ {agent_id}: {health['status']}")
                else:
                    print(f"⚠️  {agent_id}: Unhealthy")
                    self.registered_agents[agent_id]['status'] = 'unhealthy'
                    
            except Exception as e:
                print(f"❌ {agent_id}: Offline - {e}")
                self.registered_agents[agent_id]['status'] = 'offline'


def demo_supervisor_workflow():
    """
    Demonstrate a complete supervisor-agent workflow
    """
    print("\n" + "="*60)
    print("  SEO Optimizer Agent - Supervisor Demo")
    print("="*60)
    
    # Initialize supervisor
    supervisor = SimpleSupervisor()
    
    # Discover and register the SEO agent
    agent_url = "http://localhost:5000"
    agent_id = supervisor.discover_agent(agent_url)
    
    if not agent_id:
        print("\n❌ Could not register agent. Make sure the agent is running:")
        print("   python app.py")
        return
    
    # Wait a moment
    time.sleep(1)
    
    # Prepare sample tasks
    tasks = [
        {
            "task_id": "supervisor_task_001",
            "task_type": "analyze_content",
            "content": {
                "title": "Complete Guide to Python Programming",
                "body": """
# Python Programming for Beginners

Python is one of the most popular programming languages. This guide will help you 
learn Python programming from scratch.

## Why Learn Python?

Python programming is versatile and easy to learn. Many developers choose Python 
for web development, data science, and automation.

## Getting Started with Python

1. Install Python on your computer
2. Learn basic syntax and data types
3. Practice with simple programs
4. Build real projects

Python programming opens many career opportunities. Start your Python journey today!
                """,
                "target_keywords": ["Python", "programming", "learn"],
                "url": "https://example.com/python-guide"
            }
        },
        {
            "task_id": "supervisor_task_002",
            "task_type": "analyze_content",
            "content": {
                "title": "SEO Tips",
                "body": "SEO is important. Use keywords. Write good content.",
                "target_keywords": ["SEO", "keywords"],
                "url": "https://example.com/seo"
            }
        }
    ]
    
    # Assign tasks
    print("\n" + "="*60)
    print("  Assigning Tasks to Agent")
    print("="*60)
    
    for task in tasks:
        result = supervisor.assign_task(agent_id, task)
        
        if result:
            # Show key metrics
            analysis = result['analysis']
            print(f"\n   📊 Analysis Summary:")
            print(f"      • Readability: {analysis['readability']['level']}")
            print(f"      • Word Count: {analysis['content_quality']['word_count']}")
            print(f"      • Top Recommendation: {analysis['recommendations'][0][:60]}...")
        
        time.sleep(1)  # Wait between tasks
    
    # Get agent status
    print("\n" + "="*60)
    print("  Agent Status Check")
    print("="*60)
    
    status = supervisor.get_agent_status(agent_id)
    if status:
        print(f"\nAgent Statistics:")
        print(json.dumps(status['statistics'], indent=2))
    
    # Monitor agents
    supervisor.monitor_agents()
    
    print("\n" + "="*60)
    print("  Demo Complete!")
    print("="*60)
    print(f"\n✅ Successfully processed {len(tasks)} tasks")
    print(f"✅ Agent {agent_id} is operational")


if __name__ == "__main__":
    demo_supervisor_workflow()
