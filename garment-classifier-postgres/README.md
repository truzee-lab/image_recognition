# 🚀 PostgreSQL Garment Classifier for Render.com

**Plug-and-play solution** to classify garment images from your PostgreSQL database and automatically update `garment_title` and `garment_description` columns with natural, fashion-expert-like text.

## 🎯 What This Does

- **📸 Classifies garment images** from URLs stored in your PostgreSQL database
- **📝 Generates natural titles** (max 150 characters) like "Elegant Lehenga", "Chic Suit"
- **📄 Creates engaging descriptions** (max 200 characters) with designer-like language
- **🔄 Updates your database directly** with automatic backup tables
- **🛡️ Safe and reliable** with error handling and progress tracking

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/yourusername/garment-classifier-postgres.git
cd garment-classifier-postgres
python setup.py
```

### 2. Configure Database
Edit `config.py` with your Render.com database details:
```python
DB_CONFIG = {
    'host': 'your-db-name.render.com',
    'port': 5432,
    'database': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password'
}
```

### 3. Test and Run
```bash
# Test connection
python examples/01_test_connection.py

# Safe test with 5 images
python examples/02_safe_test.py

# Full classification
python examples/03_full_classification.py
```

## 📊 Database Updates

The system updates your database with:

| Column | Description | Example |
|--------|-------------|---------|
| **garment_title** | Natural title (≤150 chars) | `Elegant Lehenga` |
| **garment_description** | Natural description (≤200 chars) | `A beautifully designed lehenga. Perfectly balances traditional charm with modern sophistication.` |

### Before Update
```sql
id: 1
image_url: "https://example.com/lehenga_001.jpg"
garment_title: NULL
garment_description: NULL
```

### After Update
```sql
id: 1
image_url: "https://example.com/lehenga_001.jpg"
garment_title: "Elegant Lehenga"
garment_description: "A beautifully designed lehenga. Perfectly balances traditional charm with modern sophistication."
```

## 🎯 Features

### **Safety First**
- ✅ **Automatic Backup Tables** - Creates timestamped backup before updates
- ✅ **Batch Processing** - Processes images in small batches (default: 10)
- ✅ **Error Recovery** - Continues processing even if some images fail
- ✅ **Progress Tracking** - Real-time updates during processing

### **Natural Language Generation**
- ✅ **Varied Titles** - "Elegant Lehenga", "Chic Suit", "Beautiful Saree" (no repetitive phrases)
- ✅ **Engaging Descriptions** - Designer-like language with cultural context
- ✅ **Broad Categories** - Simplified categories (Lehenga, Saree, Suit, etc.)

### **Database Integration**
- ✅ **Direct Updates** - Updates existing columns in your table
- ✅ **URL Support** - Downloads images from URLs stored in database
- ✅ **Flexible Filtering** - Use WHERE clauses to filter records
- ✅ **Connection Testing** - Verifies database connection before processing

## 📁 Repository Structure

```
garment-classifier-postgres/
├── README.md                           # This file
├── requirements.txt                    # All dependencies
├── setup.py                           # Auto-installation script
├── config.py                          # Database configuration
├── core/
│   ├── enhanced_garment_classifier.py  # Core ML classifier
│   └── postgres_garment_classifier.py  # PostgreSQL integration
├── reference_images_pinterest/         # 31 garment categories
├── examples/
│   ├── 01_test_connection.py          # Test database connection
│   ├── 02_safe_test.py                # Test with 5 images
│   ├── 03_full_classification.py      # Full classification
│   └── 04_custom_usage.py             # Advanced options
└── docs/                              # Detailed documentation
```

## 🎨 Usage Examples

### **Basic Usage - Update All Images**
```python
from core.postgres_garment_classifier import PostgresGarmentClassifier
from config import DB_CONFIG, TABLE_NAME, IMAGE_COLUMN, ID_COLUMN

classifier = PostgresGarmentClassifier(db_config=DB_CONFIG)
results = classifier.process_database_images(
    table_name=TABLE_NAME,
    image_column=IMAGE_COLUMN,
    id_column=ID_COLUMN
)
```

### **Filtered Usage - Only Empty Titles**
```python
results = classifier.process_database_images(
    table_name=TABLE_NAME,
    image_column=IMAGE_COLUMN,
    id_column=ID_COLUMN,
    where_clause="garment_title IS NULL OR garment_title = ''"
)
```

### **Limited Usage - First N Images**
```python
results = classifier.process_database_images(
    table_name=TABLE_NAME,
    image_column=IMAGE_COLUMN,
    id_column=ID_COLUMN,
    max_images=50
)
```

## 🔧 Configuration Options

Edit `config.py` to customize:

```python
# Database Configuration
DB_CONFIG = {
    'host': 'your-db-name.render.com',
    'port': 5432,
    'database': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password'
}

# Table Configuration
TABLE_NAME = "your_garments_table"
IMAGE_COLUMN = "image_url"
ID_COLUMN = "id"

# Classification Settings
CONFIDENCE_THRESHOLD = 0.15
BACKUP_TABLE = True

# Processing Settings
BATCH_SIZE = 10
MAX_IMAGES = None
WHERE_CLAUSE = ""
```

## 🛡️ Safety & Best Practices

### **1. Always Use Backup**
```python
classifier = PostgresGarmentClassifier(
    db_config=DB_CONFIG,
    backup_table=True  # This is the default
)
```

### **2. Test on Small Dataset First**
```python
results = classifier.process_database_images(
    max_images=5  # Start with just 5 images
)
```

### **3. Use WHERE Clauses for Safety**
```python
results = classifier.process_database_images(
    where_clause="garment_title IS NULL OR garment_title = ''"
)
```

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

## 📈 Performance & Scalability

- **Batch Processing** - Process 1000+ images efficiently
- **Memory Optimization** - Adjustable batch sizes
- **Progress Tracking** - Real-time updates for long operations
- **Error Handling** - Graceful handling of failed downloads

## 🔍 Supported Garment Categories

The system recognizes **31 garment categories** including:
- **Lehenga** (Fishtail, A-line, Circular, etc.)
- **Saree** (Banarasi, Kanjeevaram, Bandhani, etc.)
- **Suit** (Punjabi, Patiala, Anarkali, etc.)
- **Kurti** (Peplum, Angrakha, Longline, etc.)
- **Gown** (Indo-Western, One-Shoulder, Ruffle, etc.)
- **Traditional** (Mundum Neriyathum, Mekhela Sador)
- **Others** (Non-garment items)

## 🔧 Troubleshooting

### **Common Issues**

#### 1. **Database Connection Error**
- Check your database configuration in `config.py`
- Verify your Render.com database is running
- Check your database credentials

#### 2. **Table Not Found**
- Verify table name and column names in `config.py`
- Check if table exists in your database

#### 3. **Image Download Failed**
- Check if image URLs are accessible
- Verify URL format and accessibility
- Some URLs might be blocked or require authentication

#### 4. **Memory Issues**
- Reduce batch size: `BATCH_SIZE = 5`
- Process fewer images: `MAX_IMAGES = 50`
- Monitor system resources during processing

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the documentation in `docs/`
3. Check PostgreSQL and Render.com documentation
4. Verify all dependencies are correctly installed

## 🎉 Ready for Production!

Your garment classification system is now **production-ready** with:

✅ **PostgreSQL Integration** - Direct database updates on Render.com  
✅ **Automatic Safety** - Backup tables and error handling  
✅ **Natural Language** - Human-like titles and descriptions  
✅ **Batch Processing** - Efficient handling of large datasets  
✅ **Progress Tracking** - Real-time updates during processing  
✅ **Flexible Filtering** - WHERE clauses for targeted updates  
✅ **Documentation** - Complete setup and usage guides  
✅ **Examples** - Ready-to-use code examples  

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Your garment classification system is now ready to update your PostgreSQL database with professional-quality titles and descriptions!** 🚀 