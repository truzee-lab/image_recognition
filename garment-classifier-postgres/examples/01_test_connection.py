#!/usr/bin/env python3
"""
Example 1: Test Database Connection
Validates connection to your PostgreSQL database on Render.com
"""

import sys
import os

# Add the parent directory to the path so we can import from core
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.postgres_garment_classifier import PostgresGarmentClassifier
from config import DB_CONFIG
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_connection():
    """Test database connection."""
    print("🚀 Example 1: Test Database Connection")
    print("=" * 50)
    
    try:
        # Initialize classifier (this will test connection)
        print("🔌 Testing database connection...")
        classifier = PostgresGarmentClassifier(
            db_config=DB_CONFIG,
            confidence_threshold=0.15,
            backup_table=False  # Don't create backup for testing
        )
        
        print("✅ Database connection successful!")
        
        # Test getting table schema
        print("\n📊 Testing table schema retrieval...")
        schema = classifier.get_table_schema("your_garments_table")
        if schema:
            print("✅ Table schema retrieved successfully!")
            print("Columns:")
            for column in schema:
                print(f"  - {column[0]} ({column[1]}, nullable: {column[2]})")
        else:
            print("❌ Failed to get table schema")
            print("   Make sure your table name is correct in config.py")
        
        print("\n🎉 Connection test completed successfully!")
        print("✅ Your database is ready for garment classification!")
        
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check your database configuration in config.py")
        print("2. Verify your Render.com database is running")
        print("3. Check your database credentials")
        print("4. Ensure your IP is whitelisted (if required)")
        return False
    
    return True

def main():
    """Main function."""
    success = test_connection()
    
    if success:
        print("\n📝 Next steps:")
        print("1. Update TABLE_NAME in config.py if needed")
        print("2. Run: python examples/02_safe_test.py")
        print("3. Run: python examples/03_full_classification.py")
    else:
        print("\n🔧 Please fix the connection issues before proceeding")
    
    return success

if __name__ == "__main__":
    main() 