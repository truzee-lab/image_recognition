# 🚀 Truzee Image Recognition System

**Complete AI-powered garment classification system** with PostgreSQL, S3, and Google Sheets integration.

## 🎯 What This Repository Contains

This repository provides **plug-and-play solutions** for classifying garment images and updating databases with natural, fashion-expert-like titles and descriptions.

## 📁 Repository Structure

```
image_recognition/
├── README.md                           # This file
├── .gitignore                          # Git ignore rules
├── garment-classifier-postgres/        # PostgreSQL integration
│   ├── README.md                       # PostgreSQL setup guide
│   ├── requirements.txt                # Dependencies
│   ├── setup.py                        # Auto-installation
│   ├── config.py                       # Database configuration
│   ├── core/                           # Core ML classifier
│   ├── examples/                       # Usage examples
│   └── docs/                           # Documentation
├── reference_images_pinterest/         # 31 garment categories
├── POSTGRES_SUMMARY.md                 # PostgreSQL solution summary
├── POSTGRES_SETUP_GUIDE.md             # PostgreSQL setup guide
├── S3_GOOGLE_SHEETS_SUMMARY.md         # S3/Google Sheets solution summary
└── S3_GOOGLE_SHEETS_SETUP_GUIDE.md     # S3/Google Sheets setup guide
```

## 🚀 Quick Start

### **PostgreSQL Integration (Recommended)**

For classifying images from your PostgreSQL database on Render.com:

```bash
# Clone and setup
git clone https://github.com/truzee-lab/image_recognition.git
cd image_recognition/garment-classifier-postgres
python setup.py

# Configure database in config.py
# Test and run
python examples/01_test_connection.py
python examples/02_safe_test.py
python examples/03_full_classification.py
```

### **S3 + Google Sheets Integration**

For classifying images from Amazon S3 and storing results in Google Sheets:

```bash
# Setup S3/Google Sheets classifier
cd image_recognition
pip install -r requirements_s3_google_sheets.txt
python s3_google_sheets_classifier.py
```

## 🎯 Key Features

### **AI-Powered Classification**
- ✅ **31 Garment Categories** - Lehenga, Saree, Suit, Kurti, Gown, etc.
- ✅ **Natural Language Generation** - Human-like titles and descriptions
- ✅ **High Accuracy** - CLIP-based few-shot learning with reference images
- ✅ **Confidence Scoring** - Reliable classification with confidence thresholds

### **Database Integration**
- ✅ **PostgreSQL Support** - Direct updates to Render.com databases
- ✅ **Automatic Backups** - Safe processing with backup tables
- ✅ **Batch Processing** - Efficient handling of large datasets
- ✅ **Error Recovery** - Graceful handling of failed operations

### **Cloud Integration**
- ✅ **Amazon S3** - Download images from S3 buckets
- ✅ **Google Sheets** - Store results in formatted spreadsheets
- ✅ **Progress Tracking** - Real-time updates during processing
- ✅ **Flexible Filtering** - WHERE clauses for targeted updates

## 📊 What Gets Generated

| Output | Description | Example |
|--------|-------------|---------|
| **garment_title** | Natural title (≤150 chars) | `Elegant Lehenga` |
| **garment_description** | Natural description (≤200 chars) | `A beautifully designed lehenga. Perfectly balances traditional charm with modern sophistication.` |

## 🔍 Supported Garment Categories

The system recognizes **31 garment categories** including:
- **Lehenga** (Fishtail, A-line, Circular, etc.)
- **Saree** (Banarasi, Kanjeevaram, Bandhani, etc.)
- **Suit** (Punjabi, Patiala, Anarkali, etc.)
- **Kurti** (Peplum, Angrakha, Longline, etc.)
- **Gown** (Indo-Western, One-Shoulder, Ruffle, etc.)
- **Traditional** (Mundum Neriyathum, Mekhela Sador)
- **Others** (Non-garment items)

## 🛡️ Safety & Best Practices

### **Always Use Backup**
```python
# PostgreSQL - Automatic backup tables
classifier = PostgresGarmentClassifier(backup_table=True)

# S3/Google Sheets - Backup spreadsheets
classifier = S3GoogleSheetsClassifier(backup_sheet=True)
```

### **Test on Small Dataset First**
```python
# Process just 5 images for testing
results = classifier.process_images(max_images=5)
```

### **Use WHERE Clauses for Safety**
```python
# Only process records with empty titles
results = classifier.process_images(
    where_clause="garment_title IS NULL OR garment_title = ''"
)
```

## 📈 Performance & Scalability

- **Batch Processing** - Process 1000+ images efficiently
- **Memory Optimization** - Adjustable batch sizes
- **Progress Tracking** - Real-time updates for long operations
- **Error Handling** - Graceful handling of failed downloads

## 🔧 Configuration

### **PostgreSQL Configuration**
Edit `garment-classifier-postgres/config.py`:
```python
DB_CONFIG = {
    'host': 'your-db-name.render.com',
    'port': 5432,
    'database': 'your_database_name',
    'user': 'your_username',
    'password': 'your_password'
}
```

### **S3/Google Sheets Configuration**
Edit environment variables:
```bash
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
GOOGLE_SHEETS_CREDENTIALS_FILE=path/to/credentials.json
```

## 📚 Documentation

- **[PostgreSQL Setup Guide](POSTGRES_SETUP_GUIDE.md)** - Complete PostgreSQL integration guide
- **[S3/Google Sheets Setup Guide](S3_GOOGLE_SHEETS_SETUP_GUIDE.md)** - Complete S3/Google Sheets integration guide
- **[PostgreSQL Summary](POSTGRES_SUMMARY.md)** - PostgreSQL solution overview
- **[S3/Google Sheets Summary](S3_GOOGLE_SHEETS_SUMMARY.md)** - S3/Google Sheets solution overview

## 🔧 Troubleshooting

### **Common Issues**

#### 1. **Database Connection Error**
- Check your database configuration
- Verify your Render.com database is running
- Check your database credentials

#### 2. **Image Download Failed**
- Check if image URLs are accessible
- Verify URL format and accessibility
- Some URLs might be blocked or require authentication

#### 3. **Memory Issues**
- Reduce batch size for processing
- Process fewer images at once
- Monitor system resources during processing

## 🎉 Ready for Production!

Your garment classification system is now **production-ready** with:

✅ **Multiple Integration Options** - PostgreSQL, S3, Google Sheets  
✅ **Automatic Safety** - Backup tables and error handling  
✅ **Natural Language** - Human-like titles and descriptions  
✅ **Batch Processing** - Efficient handling of large datasets  
✅ **Progress Tracking** - Real-time updates during processing  
✅ **Flexible Filtering** - WHERE clauses for targeted updates  
✅ **Complete Documentation** - Setup and usage guides  
✅ **Ready-to-use Examples** - Working code examples  

## 📝 License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Your AI-powered garment classification system is ready to transform your image databases with professional-quality titles and descriptions!** 🚀 
