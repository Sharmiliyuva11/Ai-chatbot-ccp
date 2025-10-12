#!/usr/bin/env python3
"""
Test runner for reminder system tests
"""
import unittest
import sys
import os

# Add the parent directory to sys.path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def run_all_tests():
    """Run all reminder system tests"""
    # Discover and run all tests in the tests directory
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


def run_specific_test(test_module):
    """Run tests from a specific module"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_module)
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Run reminder system tests')
    parser.add_argument(
        '--module', 
        help='Run tests from specific module (e.g., test_reminder_controller)',
        choices=[
            'test_reminder_controller',
            'test_reminder_scheduler', 
            'test_email_service',
            'test_reminder_integration',
            'test_pdf_controller',
            'test_pdf_service'
        ]
    )
    
    args = parser.parse_args()
    
    if args.module:
        print(f"Running tests from {args.module}...")
        success = run_specific_test(args.module)
    else:
        print("Running all reminder system tests...")
        success = run_all_tests()
    
    if success:
        print("\n✅ All tests passed!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)