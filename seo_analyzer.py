"""
SEO Analyzer Module
Contains all SEO analysis logic and scoring algorithms
"""

import re
from collections import Counter
import logging

logger = logging.getLogger(__name__)


class SEOAnalyzer:
    """
    Main SEO analysis engine
    Analyzes content for various SEO metrics
    """
    
    def __init__(self):
        self.stop_words = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'been', 'be',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        ])
    
    def analyze(self, title, body, target_keywords=None, url=''):
        """
        Perform complete SEO analysis on content
        
        Args:
            title: Page/article title
            body: Main content body
            target_keywords: List of keywords to optimize for
            url: Optional URL for context
            
        Returns:
            Dictionary containing complete analysis results
        """
        logger.info("Starting SEO analysis")
        
        if target_keywords is None:
            target_keywords = []
        
        # Combine title and body for full text analysis
        full_text = f"{title} {body}"
        
        # Perform individual analyses
        keyword_analysis = self._analyze_keywords(full_text, target_keywords)
        readability = self._calculate_readability(body)
        meta_analysis = self._analyze_meta_tags(title)
        heading_analysis = self._analyze_heading_structure(body)
        content_analysis = self._analyze_content_quality(body)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(
            keyword_analysis,
            readability,
            meta_analysis,
            heading_analysis,
            content_analysis
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            keyword_analysis,
            readability,
            meta_analysis,
            heading_analysis,
            content_analysis
        )
        
        return {
            "overall_score": overall_score,
            "keyword_analysis": keyword_analysis,
            "readability": readability,
            "meta_analysis": meta_analysis,
            "heading_structure": heading_analysis,
            "content_quality": content_analysis,
            "recommendations": recommendations
        }
    
    def _analyze_keywords(self, text, target_keywords):
        """
        Analyze keyword usage and density
        """
        text_lower = text.lower()
        word_count = len(text.split())
        
        keyword_data = {}
        for keyword in target_keywords:
            keyword_lower = keyword.lower()
            count = text_lower.count(keyword_lower)
            density = (count / word_count * 100) if word_count > 0 else 0
            
            keyword_data[keyword] = {
                "count": count,
                "density": round(density, 2),
                "status": self._evaluate_keyword_density(density)
            }
        
        return {
            "keywords": keyword_data,
            "total_words": word_count,
            "unique_words": len(set(text.lower().split()))
        }
    
    def _evaluate_keyword_density(self, density):
        """
        Evaluate if keyword density is optimal
        """
        if density < 1.0:
            return "too_low"
        elif 1.0 <= density <= 3.0:
            return "optimal"
        elif 3.0 < density <= 5.0:
            return "acceptable"
        else:
            return "too_high"
    
    def _calculate_readability(self, text):
        """
        Calculate readability score using simplified Flesch Reading Ease
        """
        if not text or len(text.strip()) == 0:
            return {
                "score": 0,
                "level": "No content",
                "grade": "N/A"
            }
        
        # Count sentences
        sentences = len(re.findall(r'[.!?]+', text))
        if sentences == 0:
            sentences = 1
        
        # Count words
        words = len(text.split())
        
        # Count syllables (simplified)
        syllables = self._count_syllables(text)
        
        # Flesch Reading Ease formula (simplified)
        if words > 0 and sentences > 0:
            avg_sentence_length = words / sentences
            avg_syllables_per_word = syllables / words
            
            score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_syllables_per_word)
            score = max(0, min(100, score))  # Clamp between 0-100
        else:
            score = 0
        
        # Determine reading level
        level, grade = self._get_reading_level(score)
        
        return {
            "score": round(score, 1),
            "level": level,
            "grade": grade,
            "avg_sentence_length": round(words / sentences, 1),
            "total_sentences": sentences,
            "total_words": words
        }
    
    def _count_syllables(self, text):
        """
        Simplified syllable counting
        """
        text = text.lower()
        vowels = 'aeiou'
        syllable_count = 0
        
        words = re.findall(r'\b\w+\b', text)
        
        for word in words:
            word_syllables = 0
            previous_was_vowel = False
            
            for char in word:
                is_vowel = char in vowels
                if is_vowel and not previous_was_vowel:
                    word_syllables += 1
                previous_was_vowel = is_vowel
            
            # Adjust for silent e
            if word.endswith('e'):
                word_syllables -= 1
            
            # Minimum 1 syllable per word
            if word_syllables == 0:
                word_syllables = 1
            
            syllable_count += word_syllables
        
        return syllable_count
    
    def _get_reading_level(self, score):
        """
        Convert Flesch score to reading level
        """
        if score >= 90:
            return "Very Easy", "5th grade"
        elif score >= 80:
            return "Easy", "6th grade"
        elif score >= 70:
            return "Fairly Easy", "7th grade"
        elif score >= 60:
            return "Standard", "8th-9th grade"
        elif score >= 50:
            return "Fairly Difficult", "10th-12th grade"
        elif score >= 30:
            return "Difficult", "College"
        else:
            return "Very Difficult", "College graduate"
    
    def _analyze_meta_tags(self, title):
        """
        Analyze meta tag quality (title for now)
        """
        title_length = len(title)
        
        # Optimal title length is 50-60 characters
        if 50 <= title_length <= 60:
            title_quality = "optimal"
        elif 40 <= title_length < 50 or 60 < title_length <= 70:
            title_quality = "acceptable"
        elif title_length < 40:
            title_quality = "too_short"
        else:
            title_quality = "too_long"
        
        return {
            "title_length": title_length,
            "title_quality": title_quality,
            "title_present": len(title.strip()) > 0
        }
    
    def _analyze_heading_structure(self, body):
        """
        Analyze heading structure (H1, H2, H3, etc.)
        """
        # Find headings (simplified - looking for markdown-style headers)
        h1_count = len(re.findall(r'^# .+', body, re.MULTILINE))
        h2_count = len(re.findall(r'^## .+', body, re.MULTILINE))
        h3_count = len(re.findall(r'^### .+', body, re.MULTILINE))
        
        total_headings = h1_count + h2_count + h3_count
        
        # Evaluate structure quality
        if h1_count == 1 and h2_count >= 2:
            structure_quality = "excellent"
        elif h1_count == 1 and h2_count >= 1:
            structure_quality = "good"
        elif total_headings > 0:
            structure_quality = "needs_improvement"
        else:
            structure_quality = "poor"
        
        return {
            "h1_count": h1_count,
            "h2_count": h2_count,
            "h3_count": h3_count,
            "total_headings": total_headings,
            "structure_quality": structure_quality
        }
    
    def _analyze_content_quality(self, body):
        """
        Analyze overall content quality
        """
        word_count = len(body.split())
        char_count = len(body)
        paragraph_count = len([p for p in body.split('\n\n') if p.strip()])
        
        # Determine content length quality
        if word_count >= 1000:
            length_quality = "excellent"
        elif word_count >= 500:
            length_quality = "good"
        elif word_count >= 300:
            length_quality = "acceptable"
        else:
            length_quality = "too_short"
        
        return {
            "word_count": word_count,
            "character_count": char_count,
            "paragraph_count": paragraph_count,
            "length_quality": length_quality
        }
    
    def _calculate_overall_score(self, keyword_analysis, readability, 
                                 meta_analysis, heading_analysis, content_analysis):
        """
        Calculate overall SEO score (0-100)
        """
        score = 0
        
        # Keyword score (25 points)
        keyword_scores = [
            25 if kw['status'] == 'optimal' else 
            15 if kw['status'] == 'acceptable' else 
            5 if kw['status'] == 'too_low' else 10
            for kw in keyword_analysis['keywords'].values()
        ]
        score += sum(keyword_scores) / len(keyword_scores) if keyword_scores else 0
        
        # Readability score (20 points)
        if readability['score'] >= 60:
            score += 20
        elif readability['score'] >= 40:
            score += 15
        else:
            score += 10
        
        # Meta tags score (20 points)
        if meta_analysis['title_quality'] == 'optimal':
            score += 20
        elif meta_analysis['title_quality'] == 'acceptable':
            score += 15
        else:
            score += 10
        
        # Heading structure score (20 points)
        heading_scores = {
            'excellent': 20,
            'good': 15,
            'needs_improvement': 10,
            'poor': 5
        }
        score += heading_scores.get(heading_analysis['structure_quality'], 5)
        
        # Content quality score (15 points)
        content_scores = {
            'excellent': 15,
            'good': 12,
            'acceptable': 8,
            'too_short': 4
        }
        score += content_scores.get(content_analysis['length_quality'], 4)
        
        return min(100, max(0, round(score)))
    
    def _generate_recommendations(self, keyword_analysis, readability, 
                                  meta_analysis, heading_analysis, content_analysis):
        """
        Generate actionable SEO recommendations
        """
        recommendations = []
        
        # Keyword recommendations
        for keyword, data in keyword_analysis['keywords'].items():
            if data['status'] == 'too_low':
                recommendations.append(
                    f"Increase usage of keyword '{keyword}' - current density {data['density']}% is too low (aim for 1-3%)"
                )
            elif data['status'] == 'too_high':
                recommendations.append(
                    f"Reduce keyword '{keyword}' usage - density {data['density']}% may be considered keyword stuffing"
                )
        
        # Readability recommendations
        if readability['score'] < 60:
            recommendations.append(
                f"Improve readability (current score: {readability['score']}) - use shorter sentences and simpler words"
            )
        
        # Meta tag recommendations
        if meta_analysis['title_quality'] == 'too_short':
            recommendations.append(
                f"Expand your title - current length {meta_analysis['title_length']} chars (optimal: 50-60 chars)"
            )
        elif meta_analysis['title_quality'] == 'too_long':
            recommendations.append(
                f"Shorten your title - current length {meta_analysis['title_length']} chars (optimal: 50-60 chars)"
            )
        
        # Heading recommendations
        if heading_analysis['h1_count'] == 0:
            recommendations.append("Add an H1 heading to your content")
        elif heading_analysis['h1_count'] > 1:
            recommendations.append(f"Use only one H1 heading (currently {heading_analysis['h1_count']})")
        
        if heading_analysis['h2_count'] < 2:
            recommendations.append("Add more H2 subheadings to structure your content (aim for at least 2-3)")
        
        # Content quality recommendations
        if content_analysis['length_quality'] == 'too_short':
            recommendations.append(
                f"Expand content length - current {content_analysis['word_count']} words (aim for 500+ words)"
            )
        
        if not recommendations:
            recommendations.append("Great job! Your content is well-optimized for SEO")
        
        return recommendations
