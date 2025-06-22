#!/usr/bin/env python3
"""
Example 2: Safe Test - Process Just 5 Images
Tests the classification system with a small dataset to ensure everything works
"""

import sys
import os

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.postgres_garment_classifier import PostgresGarmentClassifier
from config import DB_CONFIG, TABLE_NAME, IMAGE_COLUMN, ID_COLUMN
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def safe_test():
    """Run a safe test with just 5 images."""
    print("🚀 Example 2: Safe Test - Process Just 5 Images")
    print("=" * 50)
    
    try:
        # Initialize classifier
        print("🔧 Initializing classifier...")
        classifier = PostgresGarmentClassifier(
            db_config=DB_CONFIG,
            confidence_threshold=0.15,
            backup_table=True  # Always backup for safety
        )
        
        print("✅ Classifier initialized successfully!")
        
        # Process just 5 images for testing
        print("\n📸 Processing 5 images for testing...")
        results = classifier.process_database_images(
            table_name=TABLE_NAME,
            image_column=IMAGE_COLUMN,
            id_column=ID_COLUMN,
            max_images=5,  # Just 5 images for testing
            batch_size=2   # Small batch size
        )
        
        if results:
            print(f"\n✅ Test successful!")
            print(f"📊 Total Images: {results['total_images']}")
            print(f"🔄 Processed: {results['processed_images']}")
            print(f"✅ Updated: {results['updated_images']}")
            print(f"💾 Backup Table: {results['backup_table']}")
            print(f"📄 Results File: {results['results_file']}")
            
            print("\n🎉 Safe test completed successfully!")
            print("✅ You can now run the full classification with confidence!")
            
            return True
        else:
            print("❌ Test failed - no results returned")
            return False
            
    except Exception as e:
        print(f"❌ Safe test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your database configuration")
        print("2. Verify your table has images to process")
        print("3. Check the logs for specific errors")
        return False

def main():
    """Main function."""
    success = safe_test()
    
    if success:
        print("\n📝 Next steps:")
        print("1. Review the results in the generated JSON file")
        print("2. Check your database to see the updated records")
        print("3. Run: python examples/03_full_classification.py")
        print("4. Or run: python examples/04_custom_usage.py for advanced options")
    else:
        print("\n🔧 Please fix the issues before proceeding to full classification")
    
    return success

if __name__ == "__main__":
    main() 