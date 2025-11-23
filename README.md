# SEO Optimizer Agent

A Flask-based AI Agent that analyzes content for SEO optimization and provides actionable recommendations. Part of the Supervisor-Worker (Registry) architecture system.

## 🎯 Features

- **Keyword Analysis**: Analyzes keyword density and distribution
- **Readability Scoring**: Calculates Flesch Reading Ease scores
- **Meta Tag Analysis**: Evaluates title length and quality
- **Heading Structure Check**: Validates H1, H2, H3 hierarchy
- **Content Quality Assessment**: Evaluates word count and structure
- **Memory Management**: Short-term (session) and long-term (historical) memory
- **Health Monitoring**: Built-in health check and status endpoints
- **Comprehensive Logging**: Activity tracking and error logging
- **Interactive API Documentation**: Swagger UI for testing and exploration

## 📋 Requirements

- Python 3.8 or higher
- Flask 3.0.0
- See `requirements.txt` for full dependencies

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd seo_agent
```

### 2. Create Virtual Environment (Recommended)

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Create Data Directory

```bash
mkdir data
```

## ▶️ Running the Agent

### Basic Run

```bash
python app.py
```

The agent will start on `http://localhost:5000`

### Custom Port

```bash
PORT=8080 python app.py
```

## 🌐 Interactive API Documentation (Swagger UI)

Once the agent is running, access the **Swagger UI** for interactive API documentation:

**URL:** `http://localhost:5000/api/docs`

**Features:**
- 📚 Browse all 5 API endpoints with descriptions
- 🧪 Test APIs directly in your browser (no Postman needed!)
- 📖 View detailed request/response schemas
- 📋 Multiple examples for each endpoint
- 📥 Download OpenAPI 3.0 specification
- 🔄 Copy cURL commands

**Quick Start with Swagger:**
1. Open browser: `http://localhost:5000/api/docs`
2. Click on `POST /analyze`
3. Click "Try it out"
4. Click "Execute"
5. See results instantly!

For detailed Swagger instructions, see [SWAGGER_GUIDE.md](SWAGGER_GUIDE.md)

## 📡 API Endpoints

### 1. Health Check
**GET** `/health`

Returns agent status and health information.

**Response:**
```json
{
  "status": "healthy",
  "agent_id": "seo_optimizer_001",
  "agent_name": "SEO Optimizer Agent",
  "version": "1.0.0",
  "timestamp": "2025-11-22T10:30:00",
  "uptime": "operational"
}
```

### 2. Register with Supervisor
**POST** `/register`

Registers the agent with the supervisor system.

**Request:**
```json
{
  "supervisor_id": "supervisor_001",
  "supervisor_url": "http://supervisor:5001"
}
```

**Response:**
```json
{
  "agent_id": "seo_optimizer_001",
  "name": "SEO Optimizer Agent",
  "version": "1.0.0",
  "capabilities": [
    "keyword_analysis",
    "readability_check",
    "meta_tag_analysis",
    "heading_structure_check",
    "content_optimization"
  ],
  "endpoints": {
    "health": "/health",
    "analyze": "/analyze",
    "status": "/status"
  },
  "status": "registered"
}
```

### 3. Analyze Content (Main Function)
**POST** `/analyze`

Performs SEO analysis on provided content.

**Request:**
```json
{
  "task_id": "task_001",
  "task_type": "analyze_content",
  "content": {
    "title": "10 Best Practices for Web Development",
    "body": "Web development has evolved significantly over the years...",
    "target_keywords": ["web development", "best practices", "coding"],
    "url": "https://example.com/article"
  },
  "options": {
    "detailed_analysis": true
  }
}
```

**Response:**
```json
{
  "agent_id": "seo_optimizer_001",
  "task_id": "task_001",
  "status": "success",
  "analysis": {
    "overall_score": 75,
    "keyword_analysis": {
      "keywords": {
        "web development": {
          "count": 5,
          "density": 2.5,
          "status": "optimal"
        }
      },
      "total_words": 200,
      "unique_words": 150
    },
    "readability": {
      "score": 68.5,
      "level": "Standard",
      "grade": "8th-9th grade",
      "avg_sentence_length": 15.2,
      "total_sentences": 12,
      "total_words": 200
    },
    "meta_analysis": {
      "title_length": 42,
      "title_quality": "too_short",
      "title_present": true
    },
    "heading_structure": {
      "h1_count": 1,
      "h2_count": 3,
      "h3_count": 2,
      "total_headings": 6,
      "structure_quality": "excellent"
    },
    "content_quality": {
      "word_count": 200,
      "character_count": 1200,
      "paragraph_count": 5,
      "length_quality": "too_short"
    },
    "recommendations": [
      "Expand your title - current length 42 chars (optimal: 50-60 chars)",
      "Expand content length - current 200 words (aim for 500+ words)"
    ]
  },
  "timestamp": "2025-11-22T10:35:00"
}
```

### 4. Get Status
**GET** `/status`

Returns current agent statistics and memory usage.

**Response:**
```json
{
  "agent_id": "seo_optimizer_001",
  "status": "operational",
  "statistics": {
    "short_term": {
      "active_sessions": 2,
      "completed_sessions": 15,
      "total_results_cached": 17
    },
    "long_term": {
      "total_analyses_archived": 45,
      "average_overall_score": 72.3,
      "average_readability_score": 65.8
    },
    "lifetime_stats": {
      "total_sessions": 17,
      "total_analyses": 17
    }
  },
  "timestamp": "2025-11-22T10:40:00"
}
```

### 5. Get Task History
**GET** `/history/<task_id>`

Retrieves historical analysis for a specific task.

**Example:** `GET /history/task_001`

## 🧪 Testing the Agent

### Using cURL

**Health Check:**
```bash
curl http://localhost:5000/health
```

**Analyze Content:**
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "test_001",
    "content": {
      "title": "SEO Best Practices",
      "body": "SEO is important for website visibility. Good SEO practices include keyword optimization, quality content, and proper meta tags.",
      "target_keywords": ["SEO", "optimization"]
    }
  }'
```

### Using Python

```python
import requests
import json

# Health check
response = requests.get('http://localhost:5000/health')
print(response.json())

# Analyze content
data = {
    "task_id": "test_001",
    "content": {
        "title": "10 SEO Tips for Beginners",
        "body": "Your article content here...",
        "target_keywords": ["SEO", "tips", "beginners"]
    }
}

response = requests.post(
    'http://localhost:5000/analyze',
    headers={'Content-Type': 'application/json'},
    data=json.dumps(data)
)

print(json.dumps(response.json(), indent=2))
```

## 📊 Memory System

### Short-Term Memory
- Stores current session data
- Keeps recent analysis results in memory
- Clears on application restart

### Long-Term Memory
- Persists analysis history to `data/long_term_memory.json`
- Tracks patterns and trends
- Maintains user preferences
- Keeps last 100 analyses for pattern recognition

## 📝 Logging

All activities are logged to:
- Console output
- `seo_agent.log` file

Log format: `timestamp - logger_name - log_level - message`

## 🏗️ Architecture

```
seo_agent/
├── app.py                    # Main Flask application
├── seo_analyzer.py          # SEO analysis engine
├── memory_manager.py        # Memory management system
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── data/                   # Data storage directory
│   └── long_term_memory.json
└── seo_agent.log          # Log file
```

## 🔧 Configuration

Agent configuration is in `app.py`:

```python
AGENT_CONFIG = {
    "agent_id": "seo_optimizer_001",
    "name": "SEO Optimizer Agent",
    "version": "1.0.0",
    "capabilities": [...]
}
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use a different port
PORT=8080 python app.py
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Memory File Issues
```bash
# Ensure data directory exists
mkdir -p data

# Check permissions
chmod 755 data
```

## 📈 Next Steps

1. **Extend Analysis**: Add more SEO metrics (backlinks, images, etc.)
2. **API Authentication**: Add security for production use
3. **Database Integration**: Replace JSON file with proper database
4. **Rate Limiting**: Implement request rate limiting
5. **Caching**: Add Redis for better performance
6. **Docker Support**: Create Dockerfile for easy deployment

## 📚 SEO Scoring Criteria

- **Overall Score**: 0-100 (weighted combination of all metrics)
- **Keyword Density**: Optimal range 1-3%
- **Readability**: Flesch Reading Ease score
- **Title Length**: 50-60 characters optimal
- **Content Length**: 500+ words recommended
- **Heading Structure**: One H1, multiple H2s

## 👥 Team Information

**Course**: Fundamentals of Software Project Management  
**Project**: AI Agent System - SEO Optimizer  
**Semester**: 7th Semester, FAST-NUCES Islamabad

## 📄 License

Educational project for Software Project Management course.

## 🤝 Contributing

This is a semester project. Team members should follow the project guidelines and submit according to the rubric.

---

**Last Updated**: November 22, 2025
