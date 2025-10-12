#!/usr/bin/env python3
"""
Test script for generating 16-mark questions from Unit 2.pdf
"""

import sys
import os

# Add the current directory to path so we can import services
sys.path.append(os.path.dirname(__file__))

from services.pdf_service import extract_pdf_text, answer_from_pdf

def test_16_mark_question():
    """Test generating a 16-mark question from Unit 2.pdf"""
    
    # Path to the PDF
    pdf_path = os.path.join("uploads", "Unit 2.pdf")
    
    if not os.path.exists(pdf_path):
        print(f"❌ PDF not found at: {pdf_path}")
        return
    
    print("🔄 Extracting text from Unit 2.pdf...")
    text = extract_pdf_text(pdf_path)
    
    if not text:
        print("❌ Failed to extract text from PDF")
        return
    
    print(f"✅ Extracted {len(text)} characters from PDF")
    print(f"📖 Content preview: {text[:200]}...")
    
    print("\n🔄 Generating 16-mark question...")
    
    # Test 16-mark question generation
    query = "give me 16 mark question"
    result = answer_from_pdf(text, query)
    
    if result.get('success'):
        print("\n✅ Successfully generated 16-mark question:")
        print("=" * 60)
        print(result['reply'])
        print("=" * 60)
    else:
        print(f"❌ Failed to generate question: {result.get('error')}")

if __name__ == "__main__":
    test_16_mark_question()