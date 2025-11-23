"""
Memory Manager Module
Handles short-term (session) and long-term (persistent) memory for the agent
"""

import json
import os
from datetime import datetime
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Manages agent memory with short-term and long-term storage
    
    Short-term memory: Current session data (in-memory)
    Long-term memory: Historical analysis data (file-based)
    """
    
    def __init__(self, long_term_storage_path='data/long_term_memory.json'):
        # Short-term memory (current session)
        self.sessions = {}  # Store current analysis sessions
        self.results = {}   # Store analysis results
        
        # Long-term memory setup
        self.long_term_path = long_term_storage_path
        self.long_term_memory = self._load_long_term_memory()
        
        # Statistics
        self.stats = defaultdict(int)
        
        logger.info("Memory Manager initialized")
    
    def _load_long_term_memory(self):
        """
        Load historical data from persistent storage
        """
        if not os.path.exists(self.long_term_path):
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.long_term_path), exist_ok=True)
            return {
                "analyses": [],
                "patterns": {},
                "user_preferences": {}
            }
        
        try:
            with open(self.long_term_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load long-term memory: {e}")
            return {
                "analyses": [],
                "patterns": {},
                "user_preferences": {}
            }
    
    def _save_long_term_memory(self):
        """
        Save data to persistent storage
        """
        try:
            with open(self.long_term_path, 'w') as f:
                json.dump(self.long_term_memory, f, indent=2)
            logger.info("Long-term memory saved successfully")
        except Exception as e:
            logger.error(f"Failed to save long-term memory: {e}")
    
    def store_session(self, task_id, session_data):
        """
        Store current analysis session in short-term memory
        
        Args:
            task_id: Unique task identifier
            session_data: Session information and request data
        """
        self.sessions[task_id] = {
            "data": session_data,
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.stats['total_sessions'] += 1
        logger.info(f"Session stored: {task_id}")
    
    def store_result(self, task_id, result_data):
        """
        Store analysis result in short-term memory and archive to long-term
        
        Args:
            task_id: Task identifier
            result_data: Analysis results
        """
        # Store in short-term memory
        self.results[task_id] = {
            "result": result_data,
            "timestamp": datetime.now().isoformat()
        }
        
        # Update session status
        if task_id in self.sessions:
            self.sessions[task_id]['status'] = 'completed'
        
        # Archive to long-term memory
        self._archive_to_long_term(task_id, result_data)
        
        self.stats['total_analyses'] += 1
        logger.info(f"Result stored: {task_id}")
    
    def _archive_to_long_term(self, task_id, result_data):
        """
        Archive analysis to long-term memory for pattern recognition
        """
        # Create archive entry
        archive_entry = {
            "task_id": task_id,
            "timestamp": datetime.now().isoformat(),
            "overall_score": result_data.get('analysis', {}).get('overall_score', 0),
            "keywords_analyzed": list(result_data.get('analysis', {}).get('keyword_analysis', {}).get('keywords', {}).keys())
        }
        
        # Add to analyses list
        self.long_term_memory['analyses'].append(archive_entry)
        
        # Keep only last 100 analyses to prevent file bloat
        if len(self.long_term_memory['analyses']) > 100:
            self.long_term_memory['analyses'] = self.long_term_memory['analyses'][-100:]
        
        # Update patterns
        self._update_patterns(result_data)
        
        # Save to disk
        self._save_long_term_memory()
    
    def _update_patterns(self, result_data):
        """
        Extract and update SEO patterns from analysis results
        """
        analysis = result_data.get('analysis', {})
        
        # Track average scores
        if 'average_scores' not in self.long_term_memory['patterns']:
            self.long_term_memory['patterns']['average_scores'] = {
                'overall': [],
                'readability': []
            }
        
        overall_score = analysis.get('overall_score', 0)
        readability_score = analysis.get('readability', {}).get('score', 0)
        
        self.long_term_memory['patterns']['average_scores']['overall'].append(overall_score)
        self.long_term_memory['patterns']['average_scores']['readability'].append(readability_score)
        
        # Keep only last 50 scores for averaging
        for key in self.long_term_memory['patterns']['average_scores']:
            if len(self.long_term_memory['patterns']['average_scores'][key]) > 50:
                self.long_term_memory['patterns']['average_scores'][key] = \
                    self.long_term_memory['patterns']['average_scores'][key][-50:]
    
    def get_result(self, task_id):
        """
        Retrieve result from short-term memory
        
        Args:
            task_id: Task identifier
            
        Returns:
            Result data or None if not found
        """
        return self.results.get(task_id)
    
    def get_session(self, task_id):
        """
        Retrieve session from short-term memory
        
        Args:
            task_id: Task identifier
            
        Returns:
            Session data or None if not found
        """
        return self.sessions.get(task_id)
    
    def get_statistics(self):
        """
        Get memory statistics and patterns
        
        Returns:
            Dictionary containing statistics
        """
        # Calculate pattern insights
        patterns = self.long_term_memory.get('patterns', {})
        average_scores = patterns.get('average_scores', {})
        
        avg_overall = 0
        avg_readability = 0
        
        if average_scores.get('overall'):
            avg_overall = sum(average_scores['overall']) / len(average_scores['overall'])
        
        if average_scores.get('readability'):
            avg_readability = sum(average_scores['readability']) / len(average_scores['readability'])
        
        return {
            "short_term": {
                "active_sessions": len([s for s in self.sessions.values() if s['status'] == 'active']),
                "completed_sessions": len([s for s in self.sessions.values() if s['status'] == 'completed']),
                "total_results_cached": len(self.results)
            },
            "long_term": {
                "total_analyses_archived": len(self.long_term_memory.get('analyses', [])),
                "average_overall_score": round(avg_overall, 1),
                "average_readability_score": round(avg_readability, 1)
            },
            "lifetime_stats": dict(self.stats)
        }
    
    def clear_short_term_memory(self):
        """
        Clear all short-term memory (sessions and results)
        Useful for cleanup or reset
        """
        self.sessions.clear()
        self.results.clear()
        logger.info("Short-term memory cleared")
    
    def get_historical_patterns(self):
        """
        Get insights from long-term memory patterns
        
        Returns:
            Dictionary containing pattern insights
        """
        patterns = self.long_term_memory.get('patterns', {})
        
        return {
            "patterns": patterns,
            "total_historical_analyses": len(self.long_term_memory.get('analyses', []))
        }
    
    def set_user_preference(self, preference_key, preference_value):
        """
        Store user preference in long-term memory
        
        Args:
            preference_key: Preference identifier
            preference_value: Preference value
        """
        self.long_term_memory['user_preferences'][preference_key] = {
            "value": preference_value,
            "updated_at": datetime.now().isoformat()
        }
        self._save_long_term_memory()
        logger.info(f"User preference set: {preference_key}")
    
    def get_user_preference(self, preference_key):
        """
        Retrieve user preference from long-term memory
        
        Args:
            preference_key: Preference identifier
            
        Returns:
            Preference value or None if not found
        """
        pref = self.long_term_memory.get('user_preferences', {}).get(preference_key)
        return pref.get('value') if pref else None
