"""
Focused tests for PDF question format generation
Tests the specific issue mentioned: system should generate questions in requested formats (12 marks, 16 marks)
instead of defaulting to MCQs
"""
import unittest
from unittest.mock import patch
import sys
import os
import re

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pdf_service import answer_from_pdf


class TestPDFQuestionFormats(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_pdf_content = """
        Express JS is a minimal and flexible web application framework for Node.js that provides
        a robust set of features for web and mobile applications. It is the de facto standard
        for Node.js server-side development and is known for its simplicity and performance.
        
        Key Features:
        1. Routing - Handle different HTTP methods and URL patterns
        2. Middleware - Extensible request processing pipeline
        3. Template Engines - Support for various rendering engines
        4. Static File Serving - Built-in static file handling
        5. Error Handling - Comprehensive error management
        
        Architecture:
        Express follows a minimalist approach, providing only essential features while
        allowing developers to add functionality through middleware and third-party packages.
        """
    
    @patch('services.pdf_service.generate_groq_response')
    def test_12_mark_question_format_detection(self, mock_groq_response):
        """Test that system correctly detects and generates 12-mark questions"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': '''
            **Question: Explain Express JS framework and its key features. (12 marks)**
            
            **Answer:**
            
            **Introduction to Express JS (3 marks):**
            Express JS is a minimal and flexible web application framework for Node.js that provides a robust set of features for web and mobile applications. It serves as the de facto standard for server-side development in the Node.js ecosystem.
            
            **Key Features (6 marks):**
            1. **Routing System (2 marks):** Express provides a powerful routing system that allows developers to handle different HTTP methods (GET, POST, PUT, DELETE) and URL patterns efficiently.
            
            2. **Middleware Support (2 marks):** The framework uses middleware functions that have access to request and response objects, enabling extensible request processing pipelines.
            
            3. **Template Engine Integration (2 marks):** Express supports various template engines like EJS, Pug, and Handlebars for dynamic content rendering.
            
            **Architecture Benefits (3 marks):**
            Express follows a minimalist approach, providing essential features while allowing developers to extend functionality through middleware and third-party packages. This makes it highly flexible and performant for various web application needs.
            '''
        }
        
        test_queries = [
            "can u give me question from this pdf in the form of 12 marks",
            "generate 12 mark questions from this content",
            "I need 12m questions based on this pdf",
            "create questions worth 12 marks"
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                result = answer_from_pdf(self.sample_pdf_content, query)
                
                # Verify success
                self.assertTrue(result['success'], f"Failed for query: {query}")
                
                # Verify it's a 12-mark format response
                response = result['reply']
                self.assertIn('12 marks', response.lower(), 
                             f"Response should mention 12 marks for query: {query}")
                
                # Verify the prompt was constructed for 12-mark questions
                call_args = mock_groq_response.call_args[0][0]
                self.assertIn('12-mark question', call_args,
                             f"Prompt should include 12-mark specification for query: {query}")
    
    @patch('services.pdf_service.generate_groq_response')
    def test_16_mark_question_format_detection(self, mock_groq_response):
        """Test that system correctly detects and generates 16-mark questions"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': '''
            **Question: Provide a comprehensive analysis of Express JS framework, its architecture, features, and use cases. (16 marks)**
            
            **Answer:**
            
            **1. Introduction and Overview (4 marks):**
            Express JS is a fast, unopinionated, minimalist web framework for Node.js. Created by TJ Holowaychuk and now maintained by the Node.js Foundation, it has become the de facto standard for Node.js web applications.
            
            **2. Core Architecture (4 marks):**
            - Built on top of Node.js HTTP module
            - Implements middleware pattern for request processing
            - Event-driven, non-blocking I/O architecture
            - Modular design allowing extensibility
            
            **3. Key Features and Components (4 marks):**
            - Robust routing system with HTTP verb support
            - Middleware ecosystem for functionality extension
            - Template engine abstraction layer
            - Static file serving capabilities
            - Built-in error handling mechanisms
            
            **4. Use Cases and Applications (4 marks):**
            - RESTful API development and microservices
            - Single-page application backends
            - Real-time applications with WebSocket support
            - Enterprise web applications requiring scalability
            '''
        }
        
        test_queries = [
            "can u give me question from this pdf in the form of 16 marks",
            "generate 16 mark questions from this material",
            "I need 16m question format",
            "create detailed 16 marks questions"
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                result = answer_from_pdf(self.sample_pdf_content, query)
                
                # Verify success
                self.assertTrue(result['success'], f"Failed for query: {query}")
                
                # Verify it's a 16-mark format response
                response = result['reply']
                self.assertIn('16 marks', response.lower(), 
                             f"Response should mention 16 marks for query: {query}")
                
                # Verify the prompt was constructed for 16-mark questions
                call_args = mock_groq_response.call_args[0][0]
                self.assertIn('16-mark question', call_args,
                             f"Prompt should include 16-mark specification for query: {query}")
    
    @patch('services.pdf_service.generate_groq_response')
    def test_mcq_format_detection(self, mock_groq_response):
        """Test that system correctly detects and generates MCQ questions when requested"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': '''
            **Multiple Choice Questions based on Express JS:**

            **1. What is Express JS?**
            A) A web application framework for Node.js
            B) A JavaScript runtime environment
            C) A templating engine for web development
            D) A database management system
            **Correct answer: A) A web application framework for Node.js**

            **2. What is the primary purpose of Express JS?**
            A) To simplify the process of building and maintaining server-side applications
            B) To provide a robust set of features for front-end development
            C) To act as a bridge between the front-end and back-end of a web application
            D) To handle HTTP requests and responses only
            **Correct answer: A) To simplify the process of building and maintaining server-side applications**
            '''
        }
        
        test_queries = [
            "generate mcq questions from this pdf",
            "I need multiple choice questions",
            "create MCQ based on this content",
            "give me multiple choice format"
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                result = answer_from_pdf(self.sample_pdf_content, query)
                
                # Verify success
                self.assertTrue(result['success'], f"Failed for query: {query}")
                
                # Verify it's MCQ format response
                response = result['reply']
                self.assertIn('multiple choice', response.lower(), 
                             f"Response should mention multiple choice for query: {query}")
                self.assertIn('correct answer', response.lower(),
                             f"Response should include correct answers for query: {query}")
                
                # Verify the prompt was constructed for MCQ questions
                call_args = mock_groq_response.call_args[0][0]
                self.assertIn('multiple-choice questions', call_args,
                             f"Prompt should include MCQ specification for query: {query}")
    
    def test_mark_value_extraction_regex(self):
        """Test the regex pattern used to extract mark values from queries"""
        test_cases = [
            ("give me 12 mark questions", "12"),
            ("create 16m questions", "16"),
            ("I need 5 marks format", "5"),
            ("generate 20mark questions", "20"),
            ("show me 8 mark answers", "8"),
            ("no marks mentioned here", None),
            ("this has marks but no number", None),
        ]
        
        # Test the regex pattern used in answer_from_pdf function
        mark_pattern = r'(\d+)\s*(m|mark)'
        
        for query, expected_mark in test_cases:
            with self.subTest(query=query, expected=expected_mark):
                match = re.search(mark_pattern, query.lower())
                if expected_mark:
                    self.assertIsNotNone(match, f"Should find mark value in: {query}")
                    self.assertEqual(match.group(1), expected_mark, 
                                   f"Should extract {expected_mark} from: {query}")
                else:
                    self.assertIsNone(match, f"Should not find mark value in: {query}")
    
    @patch('services.pdf_service.generate_groq_response')
    def test_format_priority_when_mixed_requests(self, mock_groq_response):
        """Test behavior when query contains multiple format indicators"""
        mock_groq_response.return_value = {'success': True, 'reply': 'Test response'}
        
        # Test that mark-based takes priority over MCQ when both are mentioned
        mixed_query = "give me 12 mark questions and also mcq from this pdf"
        result = answer_from_pdf(self.sample_pdf_content, mixed_query)
        
        # Should prioritize mark-based format since the regex check comes first
        call_args = mock_groq_response.call_args[0][0]
        self.assertIn('12-mark questions', call_args,
                     "Should prioritize mark-based format when both are mentioned")
        self.assertNotIn('multiple-choice', call_args,
                        "Should not use MCQ format when mark-based is detected")
    
    @patch('services.pdf_service.generate_groq_response')
    def test_case_insensitive_format_detection(self, mock_groq_response):
        """Test that format detection works regardless of case"""
        mock_groq_response.return_value = {'success': True, 'reply': 'Test response'}
        
        test_cases = [
            "Give Me 12 MARK Questions",
            "GENERATE 16M QUESTIONS", 
            "Create MCQ Questions",
            "I NEED MULTIPLE CHOICE FORMAT"
        ]
        
        for query in test_cases:
            with self.subTest(query=query):
                result = answer_from_pdf(self.sample_pdf_content, query)
                self.assertTrue(result['success'], 
                               f"Should work with case variations: {query}")
    
    @patch('services.pdf_service.generate_groq_response')
    def test_default_behavior_without_format_specification(self, mock_groq_response):
        """Test default behavior when no specific format is requested"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': 'Express JS is a web framework for Node.js that simplifies development.'
        }
        
        # Query without specific format indicators
        general_query = "What is Express JS and how is it used?"
        result = answer_from_pdf(self.sample_pdf_content, general_query)
        
        self.assertTrue(result['success'])
        
        # Should use general answer format, not MCQ or mark-based
        call_args = mock_groq_response.call_args[0][0]
        self.assertIn('answer the user\'s question', call_args,
                     "Should use general answer format for non-specific queries")
        self.assertNotIn('multiple-choice', call_args,
                        "Should not default to MCQ format")
        self.assertNotIn('-mark question', call_args,
                        "Should not default to mark-based format")


if __name__ == '__main__':
    unittest.main()