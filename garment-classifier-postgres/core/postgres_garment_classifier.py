#!/usr/bin/env python3
"""
PostgreSQL Garment Classifier for Render.com
Classifies garment images from PostgreSQL database and updates garment_title and garment_description columns.
"""

import os
import json
import psycopg2
import pandas as pd
from pathlib import Path
from collections import Counter
import numpy as np
import logging
import tempfile
from datetime import datetime
import requests
from urllib.parse import urlparse
from enhanced_garment_classifier import EnhancedGarmentClassifier

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class PostgresGarmentClassifier:
    def __init__(self, db_config, confidence_threshold=0.15, backup_table=True):
        """
        Initialize the PostgreSQL garment classifier.
        
        Args:
            db_config (dict): Database configuration
                {
                    'host': 'your-render-host.render.com',
                    'port': 5432,
                    'database': 'your_database_name',
                    'user': 'your_username',
                    'password': 'your_password'
                }
            confidence_threshold (float): Minimum confidence for classification
            backup_table (bool): Whether to create a backup table before updates
        """
        self.db_config = db_config
        self.classifier = EnhancedGarmentClassifier(confidence_threshold=confidence_threshold)
        self.backup_table = backup_table
        
        # Category mapping for broad categories
        self.broad_category_mapping = self.get_broad_category_mapping()
        
        # Test database connection
        self.test_connection()
    
    def test_connection(self):
        """Test database connection."""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT version();")
                    version = cursor.fetchone()
                    logger.info(f"✅ Connected to PostgreSQL: {version[0]}")
        except Exception as e:
            logger.error(f"❌ Failed to connect to database: {e}")
            raise
    
    def get_broad_category_mapping(self):
        """Map specific subcategories to broader categories."""
        return {
            # Lehenga variations → Lehenga
            "Fishtail_Lehenga": "Lehenga",
            "A-line_Lehenga": "Lehenga", 
            "Circular_Lehenga": "Lehenga",
            "Panelled_Lehenga": "Lehenga",
            "Trail_Lehenga": "Lehenga",
            "Cape_Lehenga": "Lehenga",
            "Jacket_Lehenga": "Lehenga",
            "Indo-Western_Lehenga": "Lehenga",
            "Lehenga_Choli": "Lehenga",
            "Crop_Top_with_Lehenga": "Lehenga",
            "Bralette_+_Lehenga_Set": "Lehenga",
            
            # Saree variations → Saree
            "Banarasi_Saree": "Saree",
            "Kanjeevaram_Saree": "Saree",
            "Bandhani_Saree": "Saree",
            "Paithani_Saree": "Saree",
            "Chanderi_Saree": "Saree",
            "Dhoti_Saree": "Saree",
            "Half_Saree": "Saree",
            "Pre-stitched_Saree": "Saree",
            "Saree_Gown": "Saree",
            "Draped_Saree": "Saree",
            "Saree_(Generic)": "Saree",
            
            # Suit variations → Suit
            "Punjabi_Suit": "Suit",
            "Patiala_Suit": "Suit",
            "Straight_Suit": "Suit",
            "Churidar_Suit": "Suit",
            "Anarkali_Suit": "Suit",
            "Sharara_Suit": "Suit",
            "Gharara_Suit": "Suit",
            "Palazzo_Suit": "Suit",
            "Tulip_Pants_Suit": "Suit",
            "Pant_Style_Suit": "Suit",
            "Layered_Suit": "Suit",
            "Blazer_+_Skirt_Set": "Suit",
            "Top_+_Skirt_Set": "Suit",
            "Coord_Set_(Generic)": "Suit",
            "Indo-Western_Coord_Set": "Suit",
            
            # Kurti variations → Kurti
            "Peplum_Kurti": "Kurti",
            "Angrakha_Kurti": "Kurti",
            "Longline_Kurti": "Kurti",
            "Kaftan_Kurti": "Kurti",
            "A-line_Kurti": "Kurti",
            "Cape_Kurti": "Kurti",
            "Flared_Kurti": "Kurti",
            "Straight_Kurti": "Kurti",
            
            # Gown variations → Gown
            "Indo-Western_Gown": "Gown",
            "One-Shoulder_Gown": "Gown",
            "Ruffle_Gown": "Gown",
            "Jacket_Gown": "Gown",
            "Cape_Gown": "Gown",
            "Ethnic_Gown": "Gown",
            "Draped_Gown": "Gown",
            
            # Choli variations → Choli
            "Chaniya_Choli": "Choli",
            
            # Traditional variations → Traditional
            "Mundum_Neriyathum": "Traditional",
            "Mekhela_Sador": "Traditional",
            
            # Cape variations → Cape
            "Cape_+_Dhoti_Set": "Cape",
            
            # Keep some specific categories as they are
            "Salwar_Kameez": "Salwar_Kameez",
            "Kurti": "Kurti",
            "Saree": "Saree",
            "Lehenga": "Lehenga",
            "Gown": "Gown",
            "Suit": "Suit",
            "Choli": "Choli",
            "Traditional": "Traditional",
            "Cape": "Cape",
            "Others": "Others",
            "Electronics": "Electronics",
            "Furniture": "Furniture"
        }
    
    def map_to_broad_category(self, specific_category):
        """Convert specific category to broad category."""
        return self.broad_category_mapping.get(specific_category, specific_category)
    
    def get_table_schema(self, table_name):
        """Get table schema to understand the structure."""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""
                        SELECT column_name, data_type, is_nullable
                        FROM information_schema.columns
                        WHERE table_name = %s
                        ORDER BY ordinal_position;
                    """, (table_name,))
                    columns = cursor.fetchall()
                    return columns
        except Exception as e:
            logger.error(f"❌ Failed to get table schema: {e}")
            return []
    
    def create_backup_table(self, table_name):
        """Create a backup table before making changes."""
        backup_table_name = f"{table_name}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    # Create backup table
                    cursor.execute(f"CREATE TABLE {backup_table_name} AS SELECT * FROM {table_name};")
                    conn.commit()
                    logger.info(f"✅ Created backup table: {backup_table_name}")
                    return backup_table_name
        except Exception as e:
            logger.error(f"❌ Failed to create backup table: {e}")
            return None
    
    def get_images_to_process(self, table_name, image_column, id_column, where_clause=""):
        """
        Get images from database that need processing.
        
        Args:
            table_name (str): Name of the table
            image_column (str): Column containing image URLs/paths
            id_column (str): Primary key column
            where_clause (str): Optional WHERE clause to filter records
        """
        try:
            with psycopg2.connect(**self.db_config) as conn:
                query = f"""
                    SELECT {id_column}, {image_column}
                    FROM {table_name}
                    WHERE {image_column} IS NOT NULL 
                    AND {image_column} != ''
                    {f'AND {where_clause}' if where_clause else ''}
                    ORDER BY {id_column};
                """
                
                df = pd.read_sql_query(query, conn)
                logger.info(f"📊 Found {len(df)} images to process in table '{table_name}'")
                return df
                
        except Exception as e:
            logger.error(f"❌ Failed to get images from database: {e}")
            return pd.DataFrame()
    
    def download_image_from_url(self, image_url, local_path):
        """Download image from URL to local path."""
        try:
            response = requests.get(image_url, timeout=30, stream=True)
            response.raise_for_status()
            
            with open(local_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
        except Exception as e:
            logger.error(f"❌ Failed to download {image_url}: {e}")
            return False
    
    def generate_natural_title(self, broad_category, confidence):
        """Generate a natural, fashion-expert-like title (max 150 characters) with varied phrases."""
        readable_category = broad_category.replace('_', ' ').title()
        
        # Fashion adjectives based on confidence
        if confidence >= 0.9:
            adjectives = ["Exquisite", "Magnificent", "Breathtaking", "Gorgeous", "Stunning", "Elegant", "Beautiful"]
        elif confidence >= 0.7:
            adjectives = ["Stylish", "Fashionable", "Chic", "Modern", "Sophisticated", "Trendy", "Contemporary"]
        elif confidence >= 0.5:
            adjectives = ["Classic", "Timeless", "Versatile", "Refined", "Elegant", "Traditional", "Sophisticated"]
        else:
            adjectives = ["Unique", "Distinctive", "Special", "Notable", "Remarkable", "Unusual", "Extraordinary"]
        
        import random
        adjective = random.choice(adjectives)
        
        # Create varied title options without repetitive phrases
        title_variations = [
            f"{adjective} {readable_category}",
            f"{readable_category} - {adjective} Design",
            f"{adjective} {readable_category} Collection",
            f"{readable_category} - {adjective} Style",
            f"{adjective} {readable_category} Ensemble",
            f"{readable_category} - {adjective} Piece",
            f"{adjective} {readable_category} Attire",
            f"{readable_category} - {adjective} Look",
            f"{adjective} {readable_category} Outfit",
            f"{readable_category} - {adjective} Fashion",
            f"{adjective} {readable_category} Wear",
            f"{readable_category} - {adjective} Choice",
            f"{adjective} {readable_category} Selection",
            f"{readable_category} - {adjective} Creation",
            f"{adjective} {readable_category} Masterpiece"
        ]
        
        # Choose the best title that fits within 150 characters
        for title in title_variations:
            if len(title) <= 150:
                return title
        
        # Fallback to simple category name if all variations are too long
        return readable_category[:150]
    
    def generate_natural_description(self, broad_category, confidence):
        """Generate a natural, designer-like description (max 200 characters)."""
        readable_category = broad_category.replace('_', ' ').title()
        
        # Fashion designer language based on confidence
        if confidence >= 0.9:
            style_phrases = [
                "exquisitely crafted", "masterfully designed", "breathtakingly beautiful",
                "artistically rendered", "professionally tailored", "luxuriously styled"
            ]
            appeal_phrases = [
                "A true masterpiece that celebrates rich heritage.",
                "This piece showcases the finest in ethnic fashion.",
                "A stunning example of contemporary elegance."
            ]
        elif confidence >= 0.7:
            style_phrases = [
                "beautifully designed", "elegantly crafted", "sophisticatedly styled",
                "professionally made", "artistically created", "carefully tailored"
            ]
            appeal_phrases = [
                "Perfectly balances traditional charm with modern sophistication.",
                "A stunning example of contemporary Indian fashion.",
                "Offers the perfect blend of cultural heritage and style."
            ]
        elif confidence >= 0.5:
            style_phrases = [
                "well-crafted", "carefully designed", "thoughtfully styled",
                "skillfully made", "attractively created", "nicely tailored"
            ]
            appeal_phrases = [
                "Captures the essence of traditional Indian fashion beautifully.",
                "Showcases the timeless appeal of ethnic wear.",
                "Offers a wonderful introduction to authentic fashion."
            ]
        else:
            style_phrases = [
                "uniquely styled", "distinctively crafted", "specially designed",
                "unusually made", "notably created", "remarkably tailored"
            ]
            appeal_phrases = [
                "Offers a distinctive take on traditional fashion.",
                "Stands out in the world of ethnic wear.",
                "Brings a fresh perspective to classic fashion."
            ]
        
        import random
        style_phrase = random.choice(style_phrases)
        appeal_phrase = random.choice(appeal_phrases)
        
        # Create shorter, natural description (max 200 characters)
        description = f"A {style_phrase} {readable_category.lower()}. {appeal_phrase}"
        
        # Ensure it fits within 200 characters
        if len(description) > 200:
            # Try shorter variations
            short_descriptions = [
                f"Beautiful {readable_category.lower()} with elegant design.",
                f"Stylish {readable_category.lower()} for modern women.",
                f"Elegant {readable_category.lower()} with traditional charm.",
                f"Sophisticated {readable_category.lower()} for special occasions.",
                f"Chic {readable_category.lower()} with contemporary appeal."
            ]
            for short_desc in short_descriptions:
                if len(short_desc) <= 200:
                    return short_desc
            
            # Final fallback
            return f"Beautiful {readable_category.lower()}."[:200]
        
        return description
    
    def classify_database_image(self, image_url, record_id):
        """Classify a single image from database URL."""
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp_file:
            local_path = tmp_file.name
        
        try:
            # Download image from URL
            if not self.download_image_from_url(image_url, local_path):
                return None
            
            # Classify image
            result = self.classifier.classify_image(local_path)
            result['record_id'] = record_id
            result['image_url'] = image_url
            
            # Generate broad category, title, and description
            specific_category = result.get('final_classification', 'Unknown')
            broad_category = self.map_to_broad_category(specific_category)
            confidence = result.get('confidence', 0.0)
            
            title = self.generate_natural_title(broad_category, confidence)
            description = self.generate_natural_description(broad_category, confidence)
            
            result.update({
                'broad_category': broad_category,
                'title': title,
                'description': description,
                'processed_at': datetime.now().isoformat()
            })
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Failed to classify image for record {record_id}: {e}")
            return None
        finally:
            # Clean up temporary file
            if os.path.exists(local_path):
                os.unlink(local_path)
    
    def update_database_record(self, table_name, id_column, record_id, title, description):
        """Update a single record in the database."""
        try:
            with psycopg2.connect(**self.db_config) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(f"""
                        UPDATE {table_name}
                        SET garment_title = %s, garment_description = %s
                        WHERE {id_column} = %s;
                    """, (title, description, record_id))
                    conn.commit()
                    return True
        except Exception as e:
            logger.error(f"❌ Failed to update record {record_id}: {e}")
            return False
    
    def process_database_images(self, table_name, image_column, id_column, 
                              where_clause="", max_images=None, batch_size=10):
        """
        Process images from database and update garment_title and garment_description columns.
        
        Args:
            table_name (str): Name of the table
            image_column (str): Column containing image URLs/paths
            id_column (str): Primary key column
            where_clause (str): Optional WHERE clause to filter records
            max_images (int): Maximum number of images to process (None for all)
            batch_size (int): Number of images to process in each batch
        """
        logger.info(f"🚀 Starting PostgreSQL garment classification process")
        logger.info(f"📊 Table: {table_name}")
        logger.info(f"🖼️ Image Column: {image_column}")
        logger.info(f"🆔 ID Column: {id_column}")
        logger.info(f"🔍 Where Clause: {where_clause or 'None'}")
        logger.info(f"📊 Max Images: {max_images or 'All'}")
        
        # Create backup table if requested
        backup_table_name = None
        if self.backup_table:
            backup_table_name = self.create_backup_table(table_name)
        
        # Get images to process
        images_df = self.get_images_to_process(table_name, image_column, id_column, where_clause)
        
        if images_df.empty:
            logger.warning("⚠️ No images found to process")
            return None
        
        # Limit number of images if specified
        if max_images:
            images_df = images_df.head(max_images)
        
        logger.info(f"🔄 Processing {len(images_df)} images in batches of {batch_size}...")
        
        # Process images in batches
        results = []
        total_processed = 0
        total_updated = 0
        
        for i in range(0, len(images_df), batch_size):
            batch_df = images_df.iloc[i:i+batch_size]
            logger.info(f"📦 Processing batch {i//batch_size + 1}/{(len(images_df)-1)//batch_size + 1}")
            
            batch_results = []
            for _, row in batch_df.iterrows():
                record_id = row[id_column]
                image_url = row[image_column]
                
                logger.info(f"📸 Processing record {record_id}: {image_url}")
                result = self.classify_database_image(image_url, record_id)
                
                if result:
                    # Update database
                    if self.update_database_record(table_name, id_column, record_id, 
                                                 result['title'], result['description']):
                        total_updated += 1
                        logger.info(f"✅ Updated record {record_id}: {result['title']}")
                    else:
                        logger.error(f"❌ Failed to update record {record_id}")
                    
                    batch_results.append(result)
                    total_processed += 1
                else:
                    logger.warning(f"⚠️ Failed to classify record {record_id}")
            
            results.extend(batch_results)
            
            # Save batch results as backup
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            batch_file = f"batch_results_{timestamp}_batch_{i//batch_size + 1}.json"
            with open(batch_file, 'w') as f:
                json.dump(batch_results, f, indent=2)
            logger.info(f"💾 Batch results saved to: {batch_file}")
        
        # Save final results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        final_file = f"postgres_classification_results_{timestamp}.json"
        with open(final_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        logger.info(f"✅ Classification Complete!")
        logger.info(f"📊 Total Images: {len(images_df)}")
        logger.info(f"🔄 Processed: {total_processed}")
        logger.info(f"✅ Updated: {total_updated}")
        logger.info(f"💾 Results saved to: {final_file}")
        if backup_table_name:
            logger.info(f"💾 Backup table: {backup_table_name}")
        
        return {
            'total_images': len(images_df),
            'processed_images': total_processed,
            'updated_images': total_updated,
            'backup_table': backup_table_name,
            'results_file': final_file
        }

def main():
    """Example usage of PostgreSQL garment classifier."""
    
    # Database configuration for Render.com
    DB_CONFIG = {
        'host': 'your-render-host.render.com',
        'port': 5432,
        'database': 'your_database_name',
        'user': 'your_username',
        'password': 'your_password'
    }
    
    # Table configuration
    TABLE_NAME = "your_garments_table"
    IMAGE_COLUMN = "image_url"  # Column containing image URLs
    ID_COLUMN = "id"  # Primary key column
    WHERE_CLAUSE = ""  # Optional: "garment_title IS NULL OR garment_title = ''"
    MAX_IMAGES = 100  # Optional: limit number of images to process
    
    try:
        # Initialize classifier
        classifier = PostgresGarmentClassifier(
            db_config=DB_CONFIG,
            confidence_threshold=0.15,
            backup_table=True  # Create backup table before updates
        )
        
        # Process images and update database
        results = classifier.process_database_images(
            table_name=TABLE_NAME,
            image_column=IMAGE_COLUMN,
            id_column=ID_COLUMN,
            where_clause=WHERE_CLAUSE,
            max_images=MAX_IMAGES,
            batch_size=10
        )
        
        if results:
            print(f"\n🎉 Database Update Complete!")
            print(f"📊 Total Images: {results['total_images']}")
            print(f"🔄 Processed: {results['processed_images']}")
            print(f"✅ Updated: {results['updated_images']}")
            print(f"💾 Backup Table: {results['backup_table']}")
            print(f"📄 Results File: {results['results_file']}")
        else:
            print("❌ Database update failed")
            
    except Exception as e:
        logger.error(f"❌ Main process failed: {e}")

if __name__ == "__main__":
    main() 