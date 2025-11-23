# 🚀 Quick Start Guide - SEO Optimizer Agent

## Step-by-Step Setup (5 Minutes)

### 1️⃣ Install Python Dependencies

```bash
cd seo_agent
pip install -r requirements.txt
```

### 2️⃣ Create Data Directory

```bash
mkdir data
```

### 3️⃣ Start the Agent

```bash
python app.py
```

You should see:
```
INFO - Starting SEO Optimizer Agent v1.0.0
INFO - Agent ID: seo_optimizer_001
* Running on http://0.0.0.0:5000
```

### 4️⃣ Test the Agent (Open New Terminal)

**Option A: Run Test Suite**
```bash
python test_agent.py
```

**Option B: Run Supervisor Demo**
```bash
python sample_supervisor.py
```

**Option C: Manual Test with cURL**
```bash
curl http://localhost:5000/health
```

## 🎯 What Each File Does

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application with API endpoints |
| `seo_analyzer.py` | SEO analysis logic (keywords, readability, etc.) |
| `memory_manager.py` | Handles short-term and long-term memory |
| `test_agent.py` | Automated test suite |
| `sample_supervisor.py` | Mock supervisor for testing |
| `requirements.txt` | Python dependencies |

## 📡 Quick API Test

### Health Check
```bash
curl http://localhost:5000/health
```

### Analyze Content
```bash
curl -X POST http://localhost:5000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "content": {
      "title": "My Article Title",
      "body": "Article content goes here with some keywords...",
      "target_keywords": ["keyword1", "keyword2"]
    }
  }'
```

## 🛠️ Troubleshooting

### "Address already in use"
```bash
# Use different port
PORT=8080 python app.py
```

### "Module not found"
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### "Permission denied" (data directory)
```bash
# Check permissions
chmod 755 data/
```

## 📚 Next Steps for Your Project

1. ✅ **Code is done** - You have a working agent!
2. 📊 **Create WBS** - Break down remaining tasks
3. 📅 **Make Gantt Chart** - Timeline for deliverables
4. 📝 **Write Report** - Document everything
5. 🎨 **Make Slides** - Prepare presentation

## 🎓 For Your Project Report

**What to include:**
- This codebase demonstrates all requirements
- Architecture: Flask API with modular design
- Memory: Short-term (in-memory) + Long-term (JSON file)
- API Contract: JSON request/response format (see README)
- Integration: Health checks, registration, status endpoints
- Logging: Console and file logging

**Key Features to Highlight:**
- ✅ Working HTTP API
- ✅ Supervisor communication ready
- ✅ Memory management system
- ✅ Comprehensive logging
- ✅ Health monitoring
- ✅ Test suite included

## 📞 Need Help?

Check the full `README.md` for detailed documentation!

---

**Project**: AI Agent System - SEO Optimizer  
**Course**: Software Project Management  
**Institution**: FAST-NUCES Islamabad
