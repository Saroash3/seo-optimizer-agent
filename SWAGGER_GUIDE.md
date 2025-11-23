# 📚 Swagger API Documentation Guide

## What is Swagger?

Swagger (OpenAPI) provides **interactive API documentation** where you can:
- 🔍 Browse all endpoints visually
- 📝 See request/response examples
- 🧪 **Test APIs directly in your browser** (no Postman needed!)
- 📖 View detailed schemas and data models
- 📥 Download API specification

---

## 🚀 Setup Instructions

### Step 1: Install Swagger Dependencies

```bash
pip install flask-swagger-ui==4.11.1 PyYAML==6.0.1
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

### Step 2: Start the Agent

```bash
python app.py
```

You should see:
```
INFO - Starting SEO Optimizer Agent v1.0.0
 * Running on http://0.0.0.0:5000
```

### Step 3: Open Swagger UI

**Open your web browser and go to:**
```
http://localhost:5000/api/docs
```

🎉 **You'll see a beautiful interactive API documentation!**

---

## 🎯 How to Use Swagger UI

### 1. Browse Endpoints

The Swagger UI shows all 5 endpoints organized by tags:
- **Health & Monitoring** (Health Check, Status)
- **Registration** (Register with Supervisor)
- **Analysis** (Analyze Content - main feature)
- **History** (Get Task History)

### 2. Expand an Endpoint

Click on any endpoint (e.g., `POST /analyze`) to see:
- Description
- Parameters
- Request body schema
- Response examples
- Try it out button

### 3. Test an Endpoint (Interactive!)

**Example: Testing POST /analyze**

1. Click on **`POST /analyze`** to expand it

2. Click **"Try it out"** button (top right)

3. The request body becomes editable

4. Modify the example or paste this:
```json
{
  "content": {
    "title": "10 SEO Tips for Beginners",
    "body": "SEO is important for websites. Search engine optimization helps improve ranking. Good SEO includes keywords, quality content, and proper structure. Understanding SEO basics is essential.",
    "target_keywords": ["SEO", "optimization", "ranking"]
  }
}
```

5. Click **"Execute"** button

6. **See the response below!** 
   - Response code: 200
   - Response body: Full analysis results
   - Response time
   - cURL command (you can copy it!)

### 4. View Schemas

Scroll down to **"Schemas"** section to see:
- `AnalysisRequest` - Request format
- `AnalysisResponse` - Response format
- `KeywordAnalysis` - Keyword data structure
- `ReadabilityMetrics` - Readability scores
- And more...

---

## 📸 What You'll See

### Homepage
When you visit `http://localhost:5000/`, you'll see:
```json
{
  "message": "Welcome to SEO Optimizer Agent API",
  "version": "1.0.0",
  "documentation": "/api/docs",
  "health_check": "/health",
  "endpoints": {
    "analyze": "/analyze",
    "status": "/status",
    "register": "/register",
    "history": "/history/<task_id>"
  }
}
```

### Swagger UI Page
- **Top**: API title, version, description
- **Middle**: All endpoints grouped by tags
- **Bottom**: Schema definitions

---

## 🎬 Testing All Endpoints in Swagger

### Test 1: Health Check
1. Expand `GET /health`
2. Click "Try it out"
3. Click "Execute"
4. See: `{"status": "healthy", ...}`

### Test 2: Analyze Content
1. Expand `POST /analyze`
2. Click "Try it out"
3. Select an example or modify request
4. Click "Execute"
5. See full analysis results with scores and recommendations

### Test 3: Get Status
1. Expand `GET /status`
2. Click "Try it out"
3. Click "Execute"
4. See agent statistics and memory info

### Test 4: Get History
1. First, run an analysis (Test 2) and note the `task_id`
2. Expand `GET /history/{task_id}`
3. Click "Try it out"
4. Enter the `task_id` in the parameter field
5. Click "Execute"
6. See historical analysis results

---

## 💡 Swagger Features

### 1. Multiple Examples
Swagger shows different use cases:
- **Basic Analysis**: Simple request
- **Detailed Analysis**: With URL and options

Click on the example dropdown to switch between them.

### 2. Response Codes
Each endpoint shows possible responses:
- ✅ **200**: Success
- ❌ **400**: Bad request
- ❌ **404**: Not found
- ❌ **500**: Server error

### 3. Data Types & Validation
Swagger shows:
- Required fields (marked with `*`)
- Data types (string, integer, boolean)
- Format (date-time, email, uri)
- Min/max values
- Enums (allowed values)

### 4. Copy cURL Command
After executing a request, Swagger generates the cURL command:
```bash
curl -X 'POST' \
  'http://localhost:5000/analyze' \
  -H 'Content-Type: application/json' \
  -d '{...}'
```
Copy and use it in terminal!

---

## 📥 Download API Specification

### Download OpenAPI Spec
**Visit:**
```
http://localhost:5000/swagger.yaml
```

This downloads the complete API specification that can be:
- Imported into Postman
- Used with API client generators
- Shared with other developers
- Used for API testing tools

---

## 🎯 For Your Presentation

### Why Swagger is Impressive

**Show in your demo:**

1. **Open Swagger UI** (`http://localhost:5000/api/docs`)
   - "This is our interactive API documentation"

2. **Show organized endpoints**
   - "All 5 endpoints are documented with examples"

3. **Live test an analysis**
   - Click "Try it out" on POST /analyze
   - Execute with sample content
   - "See? Real-time analysis in the browser!"

4. **Show the schemas**
   - "Every data structure is fully documented"
   - Scroll to schemas section

**Say this:**
> "We've implemented industry-standard OpenAPI 3.0 documentation with Swagger UI. This allows any developer or supervisor system to understand and test our API without reading code. Everything is interactive and self-documenting."

**Time needed:** 2 minutes
**Impact:** Shows professionalism and industry best practices! 🚀

---

## 🔧 Customization

### Change Swagger UI URL
Edit in `app.py`:
```python
SWAGGER_URL = '/api/docs'  # Change this
```

Then access at your custom URL.

### Add Authentication
To add API key authentication (future):
```yaml
# In swagger.yaml
components:
  securitySchemes:
    ApiKeyAuth:
      type: apiKey
      in: header
      name: X-API-Key
```

### Add More Examples
In `swagger.yaml`, under each endpoint's `requestBody`:
```yaml
examples:
  example1:
    summary: Example 1
    value: {...}
  example2:
    summary: Example 2
    value: {...}
```

---

## 📊 For Your Report

### Section: API Documentation

**Include:**

1. **Screenshot of Swagger UI homepage**
   - Shows all endpoints organized

2. **Screenshot of expanded /analyze endpoint**
   - Shows request/response schemas

3. **Screenshot of successful execution**
   - Shows "Try it out" feature

4. **Mention in text:**
   > "We implemented OpenAPI 3.0 specification with Swagger UI for interactive API documentation. This provides self-service documentation and testing capabilities for any developer or system integrating with our agent."

---

## 🐛 Troubleshooting

### Swagger UI not loading
**Check:**
1. Is flask-swagger-ui installed?
   ```bash
   pip install flask-swagger-ui
   ```

2. Is swagger.yaml in the same directory as app.py?
   ```bash
   ls -la swagger.yaml
   ```

3. Check browser console for errors (F12)

### swagger.yaml not found
**Fix:**
Make sure swagger.yaml is in the project root:
```bash
/seo_agent/
  ├── app.py
  ├── swagger.yaml  ← Must be here
  └── ...
```

### 404 on /api/docs
**Check:**
1. Flask app is running
2. Swagger blueprint is registered (check app.py)
3. Try: `http://localhost:5000/api/docs/` (with trailing slash)

---

## 🎓 Learning Resources

- [OpenAPI Specification](https://swagger.io/specification/)
- [Swagger UI Documentation](https://swagger.io/tools/swagger-ui/)
- [OpenAPI Tutorial](https://swagger.io/docs/specification/about/)

---

## ✅ Verification Checklist

Test that everything works:

- [ ] Agent starts: `python app.py`
- [ ] Homepage works: `http://localhost:5000/`
- [ ] Swagger UI loads: `http://localhost:5000/api/docs`
- [ ] All 5 endpoints visible
- [ ] "Try it out" works on /analyze
- [ ] Request executes successfully
- [ ] Response shows analysis results
- [ ] Can download swagger.yaml

---

## 🚀 Benefits of Swagger

### For Development
- ✅ Test APIs without writing code
- ✅ See all endpoints at a glance
- ✅ Validate request/response formats
- ✅ Generate client code

### For Documentation
- ✅ Self-documenting API
- ✅ Always up-to-date
- ✅ Interactive examples
- ✅ Industry standard format

### For Your Project
- ✅ Shows professionalism
- ✅ Makes integration easy
- ✅ Demonstrates best practices
- ✅ Impressive in presentations!

---

**Your API is now fully documented with Swagger! 🎉**

Access it at: **http://localhost:5000/api/docs**
