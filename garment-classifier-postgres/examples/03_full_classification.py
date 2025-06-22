#!/usr/bin/env python3
"""
Example 3: Full Classification - Process All Images
Runs the complete garment classification on all images in your database
"""

import sys
import os

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.postgres_garment_classifier import PostgresGarmentClassifier
from config import DB_CONFIG, TABLE_NAME, IMAGE_COLUMN, ID_COLUMN, WHERE_CLAUSE, BATCH_SIZE, MAX_IMAGES
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def full_classification():
    """Run full classification on all images."""
    print("🚀 Example 3: Full Classification - Process All Images")
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
        
        # Process all images
        print("\n📸 Processing all images...")
        print(f"📊 Table: {TABLE_NAME}")
        print(f"🖼️ Image Column: {IMAGE_COLUMN}")
        print(f"🆔 ID Column: {ID_COLUMN}")
        print(f"🔍 Where Clause: {WHERE_CLAUSE or 'None'}")
        print(f"📊 Max Images: {MAX_IMAGES or 'All'}")
        print(f"📦 Batch Size: {BATCH_SIZE}")
        
        results = classifier.process_database_images(
            table_name=TABLE_NAME,
            image_column=IMAGE_COLUMN,
            id_column=ID_COLUMN,
            where_clause=WHERE_CLAUSE,
            max_images=MAX_IMAGES,
            batch_size=BATCH_SIZE
        )
        
        if results:
            print(f"\n🎉 Full Classification Complete!")
            print(f"📊 Total Images: {results['total_images']}")
            print(f"🔄 Processed: {results['processed_images']}")
            print(f"✅ Updated: {results['updated_images']}")
            print(f"💾 Backup Table: {results['backup_table']}")
            print(f"📄 Results File: {results['results_file']}")
            
            # Calculate success rate
            if results['total_images'] > 0:
                success_rate = (results['updated_images'] / results['total_images']) * 100
                print(f"📈 Success Rate: {success_rate:.1f}%")
            
            print("\n✅ All images have been classified and updated!")
            print("🎉 Your database now has garment titles and descriptions!")
            
            return True
        else:
            print("❌ Classification failed - no results returned")
            return False
            
    except Exception as e:
        print(f"❌ Full classification failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your database configuration")
        print("2. Verify your table has images to process")
        print("3. Check the logs for specific errors")
        print("4. Try running the safe test first: python examples/02_safe_test.py")
        return False

def main():
    """Main function."""
    print("⚠️  Warning: This will process ALL images in your database!")
    print("   Make sure you have a backup of your data.")
    print("   The system will create an automatic backup table before processing.")
    
    response = input("\nDo you want to continue? (y/N): ").strip().lower()
    if response not in ['y', 'yes']:
        print("❌ Classification cancelled")
        return False
    
    success = full_classification()
    
    if success:
        print("\n📝 Next steps:")
        print("1. Review the results in the generated JSON file")
        print("2. Check your database to see all updated records")
        print("3. Review the backup table for safety")
        print("4. Run: python examples/04_custom_usage.py for advanced options")
    else:
        print("\n🔧 Please fix the issues before proceeding")
    
    return success

if __name__ == "__main__":
    main() 