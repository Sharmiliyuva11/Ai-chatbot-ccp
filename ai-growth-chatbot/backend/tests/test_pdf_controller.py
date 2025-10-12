import unittest
from unittest.mock import patch, MagicMock, Mock, mock_open
import json
import os
import tempfile
import sys

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.pdf_routes import pdf_routes
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token


class TestPDFController(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = 'test-secret-key'
        self.app.config['JWT_SECRET_KEY'] = 'jwt-test-secret'
        self.app.config['TESTING'] = True
        
        # Initialize JWT
        self.jwt = JWTManager(self.app)
        
        # Register blueprint
        self.app.register_blueprint(pdf_routes, url_prefix='/api/pdf')
        
        # Create test client
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create test access token
        with self.app.test_request_context():
            self.access_token = create_access_token(identity='test_user_123')
        
        # Sample PDF text content for testing
        self.sample_pdf_text = """
        Express JS is a minimal and flexible web application framework for Node.js.
        It provides a robust set of features for web and mobile applications.
        Express is used for building web applications and APIs.
        Key features include routing, middleware, templating engines.
        """
        
        # Create a temporary directory for test uploads
        self.test_upload_dir = tempfile.mkdtemp()
        self.test_pdf_path = os.path.join(self.test_upload_dir, 'test.pdf')
        
    def tearDown(self):
        """Clean up after each test method."""
        self.app_context.pop()
        # Clean up test files
        if os.path.exists(self.test_pdf_path):
            os.remove(self.test_pdf_path)
        os.rmdir(self.test_upload_dir)
    
    @patch('routes.pdf_routes.extract_pdf_text')
    @patch('routes.pdf_routes.generate_pdf_questions')
    def test_pdf_question_generation_succeeds(self, mock_generate_questions, mock_extract_text):
        """Test happy path: PDF question generation succeeds"""
        # Setup mocks
        mock_extract_text.return_value = self.sample_pdf_text
        mock_generate_questions.return_value = {
            'success': True,
            'reply': 'Generated 10 multiple-choice questions from PDF content.'
        }
        
        # Create test file
        with open(self.test_pdf_path, 'w') as f:
            f.write('test pdf content')
        
        response = self.client.post(
            '/api/pdf/questions',
            data=json.dumps({'path': self.test_pdf_path}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertIn('questions', response_data)
        
        # Verify functions were called correctly
        mock_extract_text.assert_called_once_with(self.test_pdf_path)
        mock_generate_questions.assert_called_once_with(self.sample_pdf_text)
    
    @patch('routes.pdf_routes.extract_pdf_text')
    @patch('routes.pdf_routes.answer_from_pdf')
    def test_generate_12_mark_questions(self, mock_answer_from_pdf, mock_extract_text):
        """Test happy path: Generate 12 mark questions"""
        # Setup mocks
        mock_extract_text.return_value = self.sample_pdf_text
        mock_answer_from_pdf.return_value = {
            'success': True,
            'reply': '''
            **12-Mark Question: Explain Express JS and its key features**
            
            Express JS is a minimal and flexible web application framework built for Node.js that simplifies server-side development. Here is a detailed 12-mark answer:
            
            **Definition and Purpose (3 marks):**
            Express JS is a fast, unopinionated, minimalist web framework for Node.js. It provides a thin layer of fundamental web application features without obscuring Node.js features.
            
            **Key Features (4 marks):**
            1. Routing system for handling different HTTP methods and URLs
            2. Middleware support for request processing
            3. Template engine integration
            4. Static file serving capabilities
            
            **Architecture Benefits (3 marks):**
            - Built on Node.js, leveraging its event-driven, non-blocking I/O model
            - Minimal overhead while providing essential web development features
            - Flexible and unopinionated, allowing developer freedom in application structure
            
            **Use Cases (2 marks):**
            Express is commonly used for building REST APIs, web applications, and microservices due to its simplicity and performance.
            '''
        }
        
        # Create test file
        with open(self.test_pdf_path, 'w') as f:
            f.write('test pdf content')
        
        response = self.client.post(
            '/api/pdf/answer',
            data=json.dumps({
                'path': self.test_pdf_path,
                'query': 'give me question from this pdf in the form of 12 marks'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertIn('answer', response_data)
        self.assertIn('12-mark', response_data['answer'])
        
        # Verify the query was passed correctly to answer_from_pdf
        mock_answer_from_pdf.assert_called_once_with(
            self.sample_pdf_text, 
            'give me question from this pdf in the form of 12 marks'
        )
    
    @patch('routes.pdf_routes.extract_pdf_text')
    @patch('routes.pdf_routes.answer_from_pdf')
    def test_generate_16_mark_questions(self, mock_answer_from_pdf, mock_extract_text):
        """Test happy path: Generate 16 mark questions"""
        # Setup mocks
        mock_extract_text.return_value = self.sample_pdf_text
        mock_answer_from_pdf.return_value = {
            'success': True,
            'reply': '''
            **16-Mark Question: Comprehensive Analysis of Express JS Framework**
            
            Express JS is a comprehensive web application framework for Node.js. Here is a detailed 16-mark answer:
            
            **Introduction and Definition (3 marks):**
            Express JS is a fast, unopinionated, minimalist web framework for Node.js that serves as the de facto standard for Node.js web applications. It was created by TJ Holowaychuk in 2010 and is now maintained by the Node.js Foundation.
            
            **Core Architecture (4 marks):**
            1. Built on top of Node.js HTTP module
            2. Implements middleware pattern for request processing
            3. Provides robust routing system with support for HTTP verbs
            4. Offers template engine abstraction layer
            
            **Key Features and Benefits (5 marks):**
            1. Minimal setup with powerful features
            2. Middleware ecosystem for extended functionality
            3. Template engine integration (Pug, EJS, Handlebars)
            4. Static file serving capabilities
            5. Error handling mechanisms
            
            **Use Cases and Applications (2 marks):**
            - RESTful API development
            - Single-page applications (SPA) backends
            
            **Performance and Scalability (2 marks):**
            Express leverages Node.js event-driven architecture, making it highly scalable for I/O intensive applications while maintaining minimal resource footprint.
            '''
        }
        
        # Create test file
        with open(self.test_pdf_path, 'w') as f:
            f.write('test pdf content')
        
        response = self.client.post(
            '/api/pdf/answer',
            data=json.dumps({
                'path': self.test_pdf_path,
                'query': 'can u give me question from this pdf in the form of 16 marks'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertIn('answer', response_data)
        self.assertIn('16-mark', response_data['answer'])
        
        # Verify the query was passed correctly
        mock_answer_from_pdf.assert_called_once_with(
            self.sample_pdf_text, 
            'can u give me question from this pdf in the form of 16 marks'
        )
    
    @patch('routes.pdf_routes.extract_pdf_text')
    @patch('routes.pdf_routes.answer_from_pdf')
    def test_generate_mcq_questions(self, mock_answer_from_pdf, mock_extract_text):
        """Test happy path: Generate MCQ questions"""
        # Setup mocks
        mock_extract_text.return_value = self.sample_pdf_text
        mock_answer_from_pdf.return_value = {
            'success': True,
            'reply': '''
            Here are 10 multiple-choice questions based on the provided study material:

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
        
        # Create test file
        with open(self.test_pdf_path, 'w') as f:
            f.write('test pdf content')
        
        response = self.client.post(
            '/api/pdf/answer',
            data=json.dumps({
                'path': self.test_pdf_path,
                'query': 'generate mcq questions from this pdf'
            }),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertIn('answer', response_data)
        self.assertIn('multiple-choice questions', response_data['answer'])
        self.assertIn('Correct answer:', response_data['answer'])
    
    def test_invalid_pdf_path_handling(self):
        """Test input verification: Invalid PDF path handling"""
        test_cases = [
            {'path': '/non/existent/path.pdf'},  # Non-existent path
            {'path': ''},  # Empty path
            {'path': None},  # None path
            {}  # Missing path entirely
        ]
        
        for invalid_data in test_cases:
            with self.subTest(invalid_data=invalid_data):
                response = self.client.post(
                    '/api/pdf/questions',
                    data=json.dumps(invalid_data),
                    content_type='application/json',
                    headers={'Authorization': f'Bearer {self.access_token}'}
                )
                
                self.assertEqual(response.status_code, 400)
                response_data = json.loads(response.data)
                self.assertFalse(response_data['success'])
                self.assertEqual(response_data['message'], 'Invalid or missing PDF path')
    
    @patch('routes.pdf_routes.extract_pdf_text')
    def test_empty_pdf_content_handling(self, mock_extract_text):
        """Test input verification: Empty PDF content handling"""
        # Mock empty text extraction
        mock_extract_text.return_value = ""
        
        # Create test file
        with open(self.test_pdf_path, 'w') as f:
            f.write('test pdf content')
        
        response = self.client.post(
            '/api/pdf/questions',
            data=json.dumps({'path': self.test_pdf_path}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Could not extract text from PDF')
        
        # Verify extract was called
        mock_extract_text.assert_called_once_with(self.test_pdf_path)
    
    def test_missing_file_in_upload(self):
        """Test exception handling: Missing file in upload"""
        response = self.client.post(
            '/api/pdf/upload',
            data={},  # No file data
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'No file provided')
    
    @patch('routes.pdf_routes.extract_pdf_text')
    @patch('routes.pdf_routes.generate_pdf_questions')
    def test_groq_service_api_failure(self, mock_generate_questions, mock_extract_text):
        """Test exception handling: Groq service API failure"""
        # Setup mocks
        mock_extract_text.return_value = self.sample_pdf_text
        mock_generate_questions.return_value = {
            'success': False,
            'error': 'Groq API connection failed'
        }
        
        # Create test file
        with open(self.test_pdf_path, 'w') as f:
            f.write('test pdf content')
        
        response = self.client.post(
            '/api/pdf/questions',
            data=json.dumps({'path': self.test_pdf_path}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        # Note: Current implementation returns 200 even on service failure
        # This could be improved to return 400 for service failures
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertFalse(response_data['success'])
        self.assertEqual(response_data['message'], 'Groq API connection failed')
        
        # Verify functions were called
        mock_extract_text.assert_called_once_with(self.test_pdf_path)
        mock_generate_questions.assert_called_once_with(self.sample_pdf_text)
    
    @patch('routes.pdf_routes.extract_pdf_text')
    @patch('routes.pdf_routes.explain_pdf')
    def test_pdf_explain_endpoint_success(self, mock_explain_pdf, mock_extract_text):
        """Test PDF explain/summarize endpoint success"""
        # Setup mocks
        mock_extract_text.return_value = self.sample_pdf_text
        mock_explain_pdf.return_value = {
            'success': True,
            'reply': 'Express JS is a web framework for Node.js that helps build web applications easily.'
        }
        
        # Create test file
        with open(self.test_pdf_path, 'w') as f:
            f.write('test pdf content')
        
        response = self.client.post(
            '/api/pdf/explain',
            data=json.dumps({'path': self.test_pdf_path}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertIn('explanation', response_data)
        
        # Verify functions were called correctly
        mock_extract_text.assert_called_once_with(self.test_pdf_path)
        mock_explain_pdf.assert_called_once_with(self.sample_pdf_text)
    
    @patch('routes.pdf_routes.extract_pdf_text')
    def test_debug_pdf_text_endpoint(self, mock_extract_text):
        """Test debug PDF text extraction endpoint"""
        # Setup mock
        long_text = "Express JS is a framework. " * 100  # Create long text
        mock_extract_text.return_value = long_text
        
        # Create test file
        with open(self.test_pdf_path, 'w') as f:
            f.write('test pdf content')
        
        response = self.client.post(
            '/api/pdf/debug/pdf-text',
            data=json.dumps({'path': self.test_pdf_path}),
            content_type='application/json',
            headers={'Authorization': f'Bearer {self.access_token}'}
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertTrue(response_data['success'])
        self.assertIn('text', response_data)
        self.assertIn('length', response_data)
        self.assertEqual(response_data['length'], len(long_text))
        self.assertEqual(len(response_data['text']), 500)  # Should be truncated to 500 chars


if __name__ == '__main__':
    unittest.main()