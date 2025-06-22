#!/usr/bin/env python3
"""
Example 4: Custom Usage - Advanced Options
Demonstrates different configuration options and use cases
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

def example_filtered_processing():
    """Example: Process only records with empty titles."""
    print("\n🚀 Example A: Filtered Processing - Only Empty Titles")
    print("-" * 50)
    
    try:
        classifier = PostgresGarmentClassifier(
            db_config=DB_CONFIG,
            confidence_threshold=0.15,
            backup_table=True
        )
        
        results = classifier.process_database_images(
            table_name=TABLE_NAME,
            image_column=IMAGE_COLUMN,
            id_column=ID_COLUMN,
            where_clause="garment_title IS NULL OR garment_title = ''",
            max_images=10,  # Limit to 10 images for demo
            batch_size=5
        )
        
        if results:
            print(f"✅ Filtered processing completed!")
            print(f"📊 Processed: {results['processed_images']} images")
            print(f"✅ Updated: {results['updated_images']} records")
        else:
            print("❌ Filtered processing failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def example_limited_processing():
    """Example: Process only first N images."""
    print("\n🚀 Example B: Limited Processing - First 20 Images")
    print("-" * 50)
    
    try:
        classifier = PostgresGarmentClassifier(
            db_config=DB_CONFIG,
            confidence_threshold=0.15,
            backup_table=True
        )
        
        results = classifier.process_database_images(
            table_name=TABLE_NAME,
            image_column=IMAGE_COLUMN,
            id_column=ID_COLUMN,
            max_images=20,  # Only first 20 images
            batch_size=5
        )
        
        if results:
            print(f"✅ Limited processing completed!")
            print(f"📊 Processed: {results['processed_images']} images")
            print(f"✅ Updated: {results['updated_images']} records")
        else:
            print("❌ Limited processing failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def example_lower_confidence():
    """Example: Lower confidence threshold for more results."""
    print("\n🚀 Example C: Lower Confidence - More Results")
    print("-" * 50)
    
    try:
        classifier = PostgresGarmentClassifier(
            db_config=DB_CONFIG,
            confidence_threshold=0.1,  # Lower threshold
            backup_table=True
        )
        
        results = classifier.process_database_images(
            table_name=TABLE_NAME,
            image_column=IMAGE_COLUMN,
            id_column=ID_COLUMN,
            max_images=10,  # Limit for demo
            batch_size=5
        )
        
        if results:
            print(f"✅ Lower confidence processing completed!")
            print(f"📊 Processed: {results['processed_images']} images")
            print(f"✅ Updated: {results['updated_images']} records")
        else:
            print("❌ Lower confidence processing failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def example_small_batches():
    """Example: Small batch size for memory optimization."""
    print("\n🚀 Example D: Small Batches - Memory Optimization")
    print("-" * 50)
    
    try:
        classifier = PostgresGarmentClassifier(
            db_config=DB_CONFIG,
            confidence_threshold=0.15,
            backup_table=True
        )
        
        results = classifier.process_database_images(
            table_name=TABLE_NAME,
            image_column=IMAGE_COLUMN,
            id_column=ID_COLUMN,
            max_images=15,  # Limit for demo
            batch_size=2    # Small batch size
        )
        
        if results:
            print(f"✅ Small batch processing completed!")
            print(f"📊 Processed: {results['processed_images']} images")
            print(f"✅ Updated: {results['updated_images']} records")
        else:
            print("❌ Small batch processing failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    """Main function."""
    print("🚀 Example 4: Custom Usage - Advanced Options")
    print("=" * 60)
    print("This example demonstrates different configuration options.")
    print("Each example processes a limited number of images for demonstration.")
    print()
    
    # Run different examples
    example_filtered_processing()
    example_limited_processing()
    example_lower_confidence()
    example_small_batches()
    
    print("\n" + "=" * 60)
    print("🎉 All examples completed!")
    print("\n📝 Configuration Tips:")
    print("1. Use WHERE clauses to filter specific records")
    print("2. Use max_images to limit processing")
    print("3. Adjust batch_size for memory optimization")
    print("4. Lower confidence_threshold for more results")
    print("5. Always use backup_table=True for safety")
    
    print("\n📚 See config.py for more configuration options")

if __name__ == "__main__":
    main() 