"""
Manual verification interface for Pine Ridge test automation
"""

import sys
from typing import Dict, Any, Optional
from datetime import datetime

from .logger import Logger


class VerificationResult:
    """Result of manual verification"""
    
    def __init__(self, passed: bool, comment: str = "", timestamp: datetime = None):
        self.passed = passed
        self.comment = comment
        self.timestamp = timestamp or datetime.now()
    
    def __str__(self):
        return f"{'PASS' if self.passed else 'FAIL'} - {self.comment}"


class ManualVerificationInterface:
    """Interface for manual verification of test results"""
    
    def __init__(self):
        self.logger = Logger.get_logger(__name__)
    
    def display_verification_prompt(self, test_step: str, instructions: str) -> None:
        """Display verification prompt to user"""
        
        print("\n" + "="*80)
        print(f"MANUAL VERIFICATION REQUIRED")
        print("="*80)
        print(f"Test Step: {test_step}")
        print(f"Instructions: {instructions}")
        print("="*80)
        print()
    
    def get_verification_result(self, 
                              test_step: str, 
                              instructions: str,
                              chrome_screenshot: Optional[str] = None,
                              safari_screenshot: Optional[str] = None) -> VerificationResult:
        """Get manual verification result from user"""
        
        self.logger.info(f"Requesting manual verification for: {test_step}")
        
        # Display verification prompt
        self.display_verification_prompt(test_step, instructions)
        
        # Show screenshot information if available
        if chrome_screenshot:
            print(f"Chrome Publisher Screenshot: {chrome_screenshot}")
        if safari_screenshot:
            print(f"Safari Subscriber Screenshot: {safari_screenshot}")
        
        print("\nPlease verify the test step manually.")
        print("You should see both Chrome and Safari browser windows.")
        print("Chrome should be publishing audio, Safari should be receiving it.")
        print()
        
        # Get user input
        while True:
            try:
                print("Options:")
                print("  p - PASS (audio is heard from Chrome to Safari)")
                print("  f - FAIL (audio is not heard or there are issues)")
                print("  r - RETRY (restart the verification)")
                print("  q - QUIT (abort the test)")
                
                choice = input("\nEnter your choice (p/f/r/q): ").lower().strip()
                
                if choice == 'p':
                    comment = input("Optional comment (press Enter to skip): ").strip()
                    result = VerificationResult(True, comment)
                    self.logger.info(f"Manual verification PASSED: {comment}")
                    return result
                
                elif choice == 'f':
                    comment = input("Please describe the issue: ").strip()
                    result = VerificationResult(False, comment)
                    self.logger.info(f"Manual verification FAILED: {comment}")
                    return result
                
                elif choice == 'r':
                    print("Retrying verification...")
                    continue
                
                elif choice == 'q':
                    result = VerificationResult(False, "Test aborted by user")
                    self.logger.info("Manual verification aborted by user")
                    return result
                
                else:
                    print("Invalid choice. Please enter 'p', 'f', 'r', or 'q'.")
                    
            except KeyboardInterrupt:
                print("\nTest interrupted by user")
                return VerificationResult(False, "Test interrupted by user")
            except EOFError:
                print("\nInput stream closed")
                return VerificationResult(False, "Input stream closed")
    
    def display_test_results(self, result: VerificationResult) -> None:
        """Display final test results"""
        
        print("\n" + "="*80)
        print("TEST RESULTS")
        print("="*80)
        print(f"Status: {'PASS' if result.passed else 'FAIL'}")
        print(f"Timestamp: {result.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        if result.comment:
            print(f"Comment: {result.comment}")
        print("="*80)
        print()
    
    def prompt_for_retry(self, error_message: str) -> bool:
        """Ask user if they want to retry after an error"""
        
        print(f"\nError occurred: {error_message}")
        
        while True:
            try:
                choice = input("Do you want to retry? (y/n): ").lower().strip()
                
                if choice in ['y', 'yes']:
                    return True
                elif choice in ['n', 'no']:
                    return False
                else:
                    print("Please enter 'y' for yes or 'n' for no.")
                    
            except (KeyboardInterrupt, EOFError):
                return False