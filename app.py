"""
SEO Optimizer Agent - Main Application
Flask-based HTTP API for SEO content analysis
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from datetime import datetime
import logging
import os
from seo_analyzer import SEOAnalyzer
from memory_manager import MemoryManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('seo_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)

# Swagger UI Configuration
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI
API_URL = '/swagger.yaml'  # URL for OpenAPI spec

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "SEO Optimizer Agent API",
        'docExpansion': 'list',
        'defaultModelsExpandDepth': 3,
        'displayRequestDuration': True
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Agent configuration
AGENT_CONFIG = {
    "agent_id": "seo_optimizer_001",
    "name": "SEO Optimizer Agent",
    "version": "1.0.0",
    "capabilities": [
        "keyword_analysis",
        "readability_check",
        "meta_tag_analysis",
        "heading_structure_check",
        "content_optimization"
    ]
}

# Initialize components
seo_analyzer = SEOAnalyzer()
memory_manager = MemoryManager()


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for supervisor monitoring
    """
    logger.info("Health check requested")
    return jsonify({
        "status": "healthy",
        "agent_id": AGENT_CONFIG["agent_id"],
        "agent_name": AGENT_CONFIG["name"],
        "version": AGENT_CONFIG["version"],
        "timestamp": datetime.now().isoformat(),
        "uptime": "operational"
    }), 200


@app.route('/swagger.yaml')
def swagger_spec():
    """
    Serve the OpenAPI specification file
    """
    return send_from_directory('.', 'swagger.yaml')


@app.route('/')
def home():
    """
    Root endpoint - redirect to API documentation
    """
    return jsonify({
        "message": "Welcome to SEO Optimizer Agent API",
        "version": AGENT_CONFIG["version"],
        "documentation": "/api/docs",
        "health_check": "/health",
        "endpoints": {
            "analyze": "/analyze",
            "status": "/status",
            "register": "/register",
            "history": "/history/<task_id>"
        }
    }), 200


@app.route('/register', methods=['POST'])
def register():
    """
    Register agent with supervisor
    """
    try:
        supervisor_info = request.json
        logger.info(f"Registration request from supervisor: {supervisor_info}")
        
        registration_response = {
            "agent_id": AGENT_CONFIG["agent_id"],
            "name": AGENT_CONFIG["name"],
            "version": AGENT_CONFIG["version"],
            "capabilities": AGENT_CONFIG["capabilities"],
            "endpoints": {
                "health": "/health",
                "analyze": "/analyze",
                "status": "/status"
            },
            "status": "registered",
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info("Agent successfully registered with supervisor")
        return jsonify(registration_response), 200
        
    except Exception as e:
        logger.error(f"Registration failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": f"Registration failed: {str(e)}"
        }), 500


@app.route('/analyze', methods=['POST'])
def analyze_content():
    """
    Main endpoint for SEO content analysis
    Accepts content and returns SEO recommendations
    """
    try:
        # Parse request
        data = request.json
        logger.info(f"Analysis request received for task: {data.get('task_type', 'unknown')}")
        
        # Validate request
        if not data or 'content' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing required 'content' field"
            }), 400
        
        content = data['content']
        task_id = data.get('task_id', f"task_{datetime.now().timestamp()}")
        
        # Store request in short-term memory
        memory_manager.store_session(task_id, data)
        
        # Perform SEO analysis
        analysis_result = seo_analyzer.analyze(
            title=content.get('title', ''),
            body=content.get('body', ''),
            target_keywords=content.get('target_keywords', []),
            url=content.get('url', '')
        )
        
        # Build response
        response = {
            "agent_id": AGENT_CONFIG["agent_id"],
            "task_id": task_id,
            "status": "success",
            "analysis": analysis_result,
            "timestamp": datetime.now().isoformat()
        }
        
        # Store result in memory
        memory_manager.store_result(task_id, response)
        
        logger.info(f"Analysis completed successfully for task: {task_id}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        return jsonify({
            "agent_id": AGENT_CONFIG["agent_id"],
            "status": "error",
            "message": f"Analysis failed: {str(e)}",
            "timestamp": datetime.now().isoformat()
        }), 500


@app.route('/status', methods=['GET'])
def get_status():
    """
    Get current agent status and statistics
    """
    try:
        stats = memory_manager.get_statistics()
        
        return jsonify({
            "agent_id": AGENT_CONFIG["agent_id"],
            "status": "operational",
            "statistics": stats,
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Status check failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route('/history/<task_id>', methods=['GET'])
def get_task_history(task_id):
    """
    Retrieve analysis history for a specific task
    """
    try:
        result = memory_manager.get_result(task_id)
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({
                "status": "error",
                "message": f"Task {task_id} not found"
            }), 404
            
    except Exception as e:
        logger.error(f"History retrieval failed: {str(e)}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == '__main__':
    logger.info(f"Starting {AGENT_CONFIG['name']} v{AGENT_CONFIG['version']}")
    logger.info(f"Agent ID: {AGENT_CONFIG['agent_id']}")
    
    # Run Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
