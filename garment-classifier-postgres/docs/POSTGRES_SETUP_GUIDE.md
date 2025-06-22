# 🚀 PostgreSQL Garment Classifier for Render.com - Setup Guide

## 📋 Overview

This system allows you to:
1. **Connect to your PostgreSQL database** on Render.com
2. **Classify garment images** stored as URLs in your database
3. **Generate natural titles and descriptions** (150 chars max for titles, 200 chars max for descriptions)
4. **Update existing columns** (`garment_title` and `garment_description`) directly in your database
5. **Create automatic backups** before making changes
6. **Process images in batches** with progress tracking

---

## 🛠️ Prerequisites

### 1. **Render.com PostgreSQL Database**
- Active PostgreSQL database on Render.com
- Database connection details (host, port, database name, username, password)
- Table with image URLs and columns for `garment_title` and `garment_description`

### 2. **Python Environment**
- Python 3.8+
- Virtual environment (recommended)

### 3. **Database Table Structure**
Your table should have these columns:
```sql
CREATE TABLE your_garments_table (
    id SERIAL PRIMARY KEY,
    image_url TEXT NOT NULL,
    garment_title TEXT,
    garment_description TEXT,
    -- other columns...
);
```

---

## 📦 Installation

### 1. **Install Dependencies**
```bash
pip install -r requirements_postgres.txt
```

### 2. **Verify Enhanced Garment Classifier**
Make sure you have the `enhanced_garment_classifier.py` file in your project directory.

---

## 🔧 Configuration

### 1. **Get Render.com Database Details**

#### From Render.com Dashboard:
1. Go to your Render.com dashboard
2. Select your PostgreSQL database
3. Go to "Connections" tab
4. Copy the connection details:
   - **Host**: `your-db-name.render.com`
   - **Port**: `5432`
   - **Database**: `your_database_name`
   - **Username**: `your_username`
   - **Password**: `your_password`

### 2. **Update Configuration in Script**
```python
# In postgres_garment_classifier.py, update these values:

DB_CONFIG = {
    'host': 'your-db-name.render.com',
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
```

---

## 🚀 Usage

### 1. **Basic Usage - Update All Images**
```python
from postgres_garment_classifier import PostgresGarmentClassifier

# Database configuration
DB_CONFIG = {
    'host': 'your-db-name.render.com',
    'port': 5432,
    'database': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password'
}

# Initialize classifier
classifier = PostgresGarmentClassifier(
    db_config=DB_CONFIG,
    confidence_threshold=0.15,
    backup_table=True  # Creates backup before updates
)

# Process all images
results = classifier.process_database_images(
    table_name="your_garments_table",
    image_column="image_url",
    id_column="id"
)

print(f"Updated {results['updated_images']} records")
```

### 2. **Filtered Usage - Only Empty Titles**
```python
# Process only records with empty titles
results = classifier.process_database_images(
    table_name="your_garments_table",
    image_column="image_url",
    id_column="id",
    where_clause="garment_title IS NULL OR garment_title = ''"
)
```

### 3. **Limited Usage - First N Images**
```python
# Process only first 50 images
results = classifier.process_database_images(
    table_name="your_garments_table",
    image_column="image_url",
    id_column="id",
    max_images=50
)
```

### 4. **Advanced Usage - All Options**
```python
# Process with all options
results = classifier.process_database_images(
    table_name="your_garments_table",
    image_column="image_url",
    id_column="id",
    where_clause="garment_title IS NULL",
    max_images=25,
    batch_size=5  # Process 5 images at a time
)
```

### 5. **Command Line Usage**
```bash
python postgres_garment_classifier.py
```

---

## 📊 Database Updates

The system will update your database with:

| Column | Description | Example |
|--------|-------------|---------|
| **garment_title** | Natural title (≤150 chars) | `Elegant Lehenga` |
| **garment_description** | Natural description (≤200 chars) | `A beautifully designed lehenga. Perfectly balances traditional charm with modern sophistication.` |

---

## 🎯 Features

### **Safety Features**
- **Automatic Backup**: Creates backup table before updates
- **Batch Processing**: Processes images in small batches
- **Error Handling**: Continues processing even if some images fail
- **Progress Tracking**: Real-time updates during processing

### **Natural Language Generation**
- **Titles**: Varied, non-repetitive phrases (max 150 characters)
- **Descriptions**: Short, engaging descriptions (max 200 characters)
- **Broad Categories**: Simplified categories for better user experience

### **Database Integration**
- **Direct Updates**: Updates existing columns in your table
- **URL Support**: Downloads images from URLs stored in database
- **Flexible Filtering**: Use WHERE clauses to filter records
- **Batch Results**: Saves results as JSON files for backup

---

## 🔍 Example Output

### **Database Record Before**
```sql
id: 1
image_url: "https://example.com/lehenga_001.jpg"
garment_title: NULL
garment_description: NULL
```

### **Database Record After**
```sql
id: 1
image_url: "https://example.com/lehenga_001.jpg"
garment_title: "Elegant Lehenga"
garment_description: "A beautifully designed lehenga. Perfectly balances traditional charm with modern sophistication."
```

---

## ⚙️ Customization

### 1. **Modify Title Generation**
```python
def generate_natural_title(self, broad_category, confidence):
    # Add your custom title logic here
    return "Your Custom Title"
```

### 2. **Modify Description Generation**
```python
def generate_natural_description(self, broad_category, confidence):
    # Add your custom description logic here
    return "Your custom description."
```

### 3. **Add Custom Categories**
```python
def get_broad_category_mapping(self):
    mapping = {
        # Add your custom mappings
        "Your_Custom_Category": "Your_Broad_Category"
    }
    return mapping
```

---

## 🛡️ Safety & Best Practices

### 1. **Always Use Backup**
```python
# Always enable backup table creation
classifier = PostgresGarmentClassifier(
    db_config=DB_CONFIG,
    backup_table=True  # This is the default
)
```

### 2. **Test on Small Dataset First**
```python
# Test with just a few images first
results = classifier.process_database_images(
    table_name="your_garments_table",
    image_column="image_url",
    id_column="id",
    max_images=5  # Start with just 5 images
)
```

### 3. **Use WHERE Clauses for Safety**
```python
# Only process records that need updating
results = classifier.process_database_images(
    table_name="your_garments_table",
    image_column="image_url",
    id_column="id",
    where_clause="garment_title IS NULL OR garment_title = ''"
)
```

### 4. **Monitor Progress**
- Check the generated JSON files for detailed results
- Monitor the backup table for safety
- Review logs for any errors

---

## 🔧 Troubleshooting

### **Common Issues**

#### 1. **Database Connection Error**
```bash
# Check your database configuration
# Verify host, port, database name, username, and password
```

#### 2. **Table Not Found**
```bash
# Verify table name and column names
# Check if table exists in your database
```

#### 3. **Image Download Failed**
- Check if image URLs are accessible
- Verify URL format and accessibility
- Some URLs might be blocked or require authentication

#### 4. **Memory Issues**
- Reduce batch size: `batch_size=5`
- Process fewer images: `max_images=50`
- Monitor system resources during processing

#### 5. **Permission Errors**
- Ensure database user has UPDATE permissions
- Check if user can create backup tables

---

## 📈 Performance Optimization

### 1. **Batch Processing**
```python
# Adjust batch size based on your system
results = classifier.process_database_images(
    batch_size=5  # Smaller batches for better memory management
)
```

### 2. **Filter Records**
```python
# Only process records that need updating
results = classifier.process_database_images(
    where_clause="garment_title IS NULL"
)
```

### 3. **Limit Processing**
```python
# Process in smaller chunks
results = classifier.process_database_images(
    max_images=100  # Process 100 images at a time
)
```

---

## 🔄 Backup and Recovery

### **Automatic Backup**
The system creates a backup table automatically:
```sql
-- Backup table name format:
your_garments_table_backup_20250120_143022
```

### **Manual Recovery**
If you need to restore from backup:
```sql
-- Drop current table
DROP TABLE your_garments_table;

-- Restore from backup
CREATE TABLE your_garments_table AS 
SELECT * FROM your_garments_table_backup_20250120_143022;
```

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review PostgreSQL and Render.com documentation
3. Ensure all dependencies are correctly installed
4. Verify database credentials and permissions

---

## 🎉 Ready to Use!

Your PostgreSQL garment classifier is now ready to update your Render.com database with professional-quality titles and descriptions! 🚀

### **Next Steps**
1. **Update database configuration** in the script
2. **Test with a small dataset** first
3. **Run the classification** on your full dataset
4. **Monitor results** and backup files
5. **Customize as needed** for your specific use case

**Your garment classification system is now ready to process images from your PostgreSQL database and generate professional-quality titles and descriptions!** 🚀 