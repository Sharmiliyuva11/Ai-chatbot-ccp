import unittest
from unittest.mock import patch, MagicMock, Mock, mock_open
import os
import sys
import tempfile

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.pdf_service import extract_pdf_text, generate_pdf_questions, explain_pdf, answer_from_pdf


class TestPDFService(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_pdf_text = """
        Express JS is a minimal and flexible web application framework for Node.js.
        It provides a robust set of features for web and mobile applications.
        Express is used for building web applications and APIs.
        Key features include routing, middleware, templating engines.
        """
        
        # Create temporary test file
        self.test_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.pdf')
        self.test_file_path = self.test_file.name
        self.test_file.close()
    
    def tearDown(self):
        """Clean up after each test method."""
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)
    
    @patch('services.pdf_service.PyPDF2.PdfReader')
    def test_extract_pdf_text_success(self, mock_pdf_reader):
        """Test successful PDF text extraction"""
        # Mock PDF reader and pages
        mock_page1 = Mock()
        mock_page1.extract_text.return_value = "Page 1 content. "
        mock_page2 = Mock()
        mock_page2.extract_text.return_value = "Page 2 content."
        
        mock_reader = Mock()
        mock_reader.pages = [mock_page1, mock_page2]
        mock_pdf_reader.return_value = mock_reader
        
        # Mock file opening
        with patch('builtins.open', mock_open(read_data='pdf_binary_content')):
            result = extract_pdf_text(self.test_file_path)
        
        self.assertEqual(result, "Page 1 content. Page 2 content.")
        mock_pdf_reader.assert_called_once()
    
    @patch('services.pdf_service.PyPDF2.PdfReader')
    def test_extract_pdf_text_file_not_found(self, mock_pdf_reader):
        """Test PDF text extraction with file not found error"""
        mock_pdf_reader.side_effect = FileNotFoundError("File not found")
        
        result = extract_pdf_text("/non/existent/path.pdf")
        
        self.assertIn("Error extracting PDF", result)
        self.assertIn("No such file or directory", result)
    
    @patch('services.pdf_service.PyPDF2.PdfReader')
    def test_extract_pdf_text_corrupted_file(self, mock_pdf_reader):
        """Test PDF text extraction with corrupted file"""
        mock_pdf_reader.side_effect = Exception("Corrupted PDF file")
        
        result = extract_pdf_text(self.test_file_path)
        
        self.assertIn("Error extracting PDF", result)
        self.assertIn("Corrupted PDF file", result)
    
    @patch('services.pdf_service.generate_groq_response')
    def test_explain_pdf_success(self, mock_groq_response):
        """Test successful PDF explanation"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': 'Express JS is a web framework for Node.js that simplifies web development.'
        }
        
        result = explain_pdf(self.sample_pdf_text)
        
        self.assertTrue(result['success'])
        self.assertIn('Express JS is a web framework', result['reply'])
        
        # Verify the prompt was constructed correctly
        mock_groq_response.assert_called_once()
        call_args = mock_groq_response.call_args[0][0]
        self.assertIn('Explain the following study material', call_args)
        self.assertIn('Express JS', call_args)
    
    @patch('services.pdf_service.generate_groq_response')
    def test_explain_pdf_api_failure(self, mock_groq_response):
        """Test PDF explanation with API failure"""
        mock_groq_response.side_effect = Exception("API connection failed")
        
        result = explain_pdf(self.sample_pdf_text)
        
        self.assertFalse(result['success'])
        self.assertIn('Failed to explain PDF content', result['error'])
        self.assertIn('API connection failed', result['error'])
    
    @patch('services.pdf_service.generate_groq_response')
    def test_generate_pdf_questions_success(self, mock_groq_response):
        """Test successful PDF questions generation"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': '''
            Here are 10 multiple-choice questions based on the study material:
            
            1. What is Express JS?
            A) A web framework for Node.js
            B) A database system
            C) A programming language
            D) An operating system
            Correct answer: A
            '''
        }
        
        result = generate_pdf_questions(self.sample_pdf_text)
        
        self.assertTrue(result['success'])
        self.assertIn('multiple-choice questions', result['reply'])
        
        # Verify the prompt includes MCQ generation request
        mock_groq_response.assert_called_once()
        call_args = mock_groq_response.call_args[0][0]
        self.assertIn('generate 10 multiple-choice questions', call_args)
        self.assertIn('4 options each', call_args)
    
    @patch('services.pdf_service.generate_groq_response')
    def test_answer_from_pdf_mcq_intent(self, mock_groq_response):
        """Test answer generation with MCQ intent"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': 'Generated 10 MCQs based on Express JS content.'
        }
        
        test_queries = [
            'generate mcq from this pdf',
            'I need multiple choice questions',
            'Create MCQ based on this content'
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                result = answer_from_pdf(self.sample_pdf_text, query)
                
                self.assertTrue(result['success'])
                self.assertIn('MCQs', result['reply'])
                
                # Verify MCQ-specific prompt was used
                call_args = mock_groq_response.call_args[0][0]
                self.assertIn('multiple-choice questions', call_args)
    
    @patch('services.pdf_service.generate_groq_response')
    def test_answer_from_pdf_12_mark_intent(self, mock_groq_response):
        """Test answer generation with 12 mark intent"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': '''
            **12-Mark Answer: Express JS Framework**
            
            Express JS is a minimal web framework for Node.js (3 marks).
            It provides routing, middleware, and templating features (4 marks).
            Used for building APIs and web applications efficiently (3 marks).
            Performance benefits include event-driven architecture (2 marks).
            '''
        }
        
        test_queries = [
            'give me 12 mark questions',
            'generate 12m question from pdf',
            'I need 12 marks questions'
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                result = answer_from_pdf(self.sample_pdf_text, query)
                
                self.assertTrue(result['success'])
                self.assertIn('12-Mark', result['reply'])
                
                # Verify mark-based prompt was used
                call_args = mock_groq_response.call_args[0][0]
                self.assertIn('12-mark question', call_args)
                self.assertIn('expected length and depth', call_args)
    
    @patch('services.pdf_service.generate_groq_response')
    def test_answer_from_pdf_16_mark_intent(self, mock_groq_response):
        """Test answer generation with 16 mark intent"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': '''
            **16-Mark Answer: Comprehensive Express JS Analysis**
            
            Detailed analysis of Express JS framework covering:
            - Definition and architecture (4 marks)
            - Key features and components (4 marks)  
            - Implementation patterns (4 marks)
            - Performance and scalability (4 marks)
            '''
        }
        
        test_queries = [
            'can you give me 16 mark questions',
            'generate 16m questions from this pdf',
            'I need 16 marks answer format'
        ]
        
        for query in test_queries:
            with self.subTest(query=query):
                result = answer_from_pdf(self.sample_pdf_text, query)
                
                self.assertTrue(result['success'])
                self.assertIn('16-Mark', result['reply'])
                
                # Verify mark-based prompt was used
                call_args = mock_groq_response.call_args[0][0]
                self.assertIn('16-mark question', call_args)
    
    @patch('services.pdf_service.generate_groq_response')
    def test_answer_from_pdf_general_query(self, mock_groq_response):
        """Test answer generation with general query"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': 'Express JS is a web framework that simplifies Node.js development.'
        }
        
        result = answer_from_pdf(self.sample_pdf_text, 'What is Express JS?')
        
        self.assertTrue(result['success'])
        self.assertIn('Express JS is a web framework', result['reply'])
        
        # Verify general query prompt was used
        call_args = mock_groq_response.call_args[0][0]
        self.assertIn('answer the user\'s question', call_args)
        self.assertIn('What is Express JS?', call_args)
    
    @patch('services.pdf_service.generate_groq_response')
    def test_answer_from_pdf_various_mark_formats(self, mock_groq_response):
        """Test mark detection with various formats"""
        mock_groq_response.return_value = {
            'success': True,
            'reply': 'Mock response for mark-based question'
        }
        
        test_cases = [
            ('give me 5 mark question', '5'),
            ('create 10m questions', '10'),
            ('I need 15 marks answer', '15'),
            ('generate 20mark question', '20')
        ]
        
        for query, expected_marks in test_cases:
            with self.subTest(query=query, expected_marks=expected_marks):
                result = answer_from_pdf(self.sample_pdf_text, query)
                
                self.assertTrue(result['success'])
                
                # Verify correct mark value was detected and used in prompt
                call_args = mock_groq_response.call_args[0][0]
                self.assertIn(f'{expected_marks}-mark question', call_args)
    
    @patch('services.pdf_service.generate_groq_response')
    def test_answer_from_pdf_groq_service_failure(self, mock_groq_response):
        """Test answer generation with Groq service failure"""
        mock_groq_response.side_effect = Exception("Groq API rate limit exceeded")
        
        result = answer_from_pdf(self.sample_pdf_text, 'What is Express JS?')
        
        self.assertFalse(result['success'])
        self.assertIn('Failed to generate answer', result['error'])
        self.assertIn('Groq API rate limit exceeded', result['error'])
    
    def test_answer_from_pdf_text_truncation(self):
        """Test that long text is properly truncated to 4000 characters"""
        # Create very long text (over 4000 characters)
        long_text = "Express JS framework. " * 200  # ~4400 characters
        
        with patch('services.pdf_service.generate_groq_response') as mock_groq_response:
            mock_groq_response.return_value = {'success': True, 'reply': 'Test response'}
            
            answer_from_pdf(long_text, 'What is Express JS?')
            
            # Verify the text was truncated to 4000 characters in the prompt
            call_args = mock_groq_response.call_args[0][0]
            # Extract the material section from the prompt
            material_start = call_args.find('Material:') + len('Material:')
            material_text = call_args[material_start:].strip()
            self.assertLessEqual(len(material_text), 4000)
    
    @patch('services.pdf_service.generate_groq_response')
    def test_generate_pdf_questions_text_truncation(self, mock_groq_response):
        """Test that PDF questions generation truncates long text properly"""
        mock_groq_response.return_value = {'success': True, 'reply': 'Test MCQs'}
        
        # Create very long text
        long_text = "Express JS content. " * 250  # ~5000 characters
        
        generate_pdf_questions(long_text)
        
        # Verify the text was truncated in the prompt
        call_args = mock_groq_response.call_args[0][0]
        # The prompt should contain only first 4000 chars of the text
        self.assertLess(len(call_args), 4200)  # Some buffer for prompt text
    
    @patch('services.pdf_service.generate_groq_response')
    def test_explain_pdf_text_truncation(self, mock_groq_response):
        """Test that PDF explanation truncates long text properly"""
        mock_groq_response.return_value = {'success': True, 'reply': 'Test explanation'}
        
        # Create very long text
        long_text = "Express JS details. " * 250  # ~5000 characters
        
        explain_pdf(long_text)
        
        # Verify the text was truncated in the prompt
        call_args = mock_groq_response.call_args[0][0]
        self.assertLess(len(call_args), 4200)  # Some buffer for prompt text


if __name__ == '__main__':
    unittest.main()