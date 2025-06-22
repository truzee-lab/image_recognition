# 🚀 S3 to Google Sheets Garment Classifier - Setup Guide

## 📋 Overview

This system allows you to:
1. **Classify garment images** stored in Amazon S3
2. **Generate natural titles and descriptions** (150 chars max for titles, 200 chars max for descriptions)
3. **Store results in Google Sheets** with automatic formatting
4. **Process images in batches** with progress tracking
5. **Maintain data backups** locally

---

## 🛠️ Prerequisites

### 1. **AWS S3 Setup**
- AWS account with S3 access
- S3 bucket with garment images
- AWS credentials configured (via AWS CLI or environment variables)

### 2. **Google Sheets API Setup**
- Google Cloud Project
- Google Sheets API enabled
- Service account credentials JSON file

### 3. **Python Environment**
- Python 3.8+
- Virtual environment (recommended)

---

## 📦 Installation

### 1. **Install Dependencies**
```bash
pip install -r requirements_s3_google_sheets.txt
```

### 2. **AWS Credentials Setup**
```bash
# Option 1: AWS CLI
aws configure

# Option 2: Environment Variables
export AWS_ACCESS_KEY_ID="your-access-key"
export AWS_SECRET_ACCESS_KEY="your-secret-key"
export AWS_DEFAULT_REGION="your-region"
```

### 3. **Google Sheets API Setup**

#### Step 1: Create Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API and Google Drive API

#### Step 2: Create Service Account
1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Fill in details and create
4. Add roles: "Editor" for Google Sheets API

#### Step 3: Download Credentials
1. Click on your service account
2. Go to "Keys" tab
3. Click "Add Key" → "Create New Key"
4. Choose JSON format
5. Download and save securely

---

## 🔧 Configuration

### 1. **Update Configuration in Script**
```python
# In s3_google_sheets_classifier.py, update these values:

S3_BUCKET = "your-s3-bucket-name"
GOOGLE_CREDS_PATH = "path/to/your/google-credentials.json"
S3_PREFIX = "garments/"  # Optional: filter images by prefix
MAX_IMAGES = 100  # Optional: limit number of images to process
SPREADSHEET_NAME = "Garment_Classifications_Results"
```

### 2. **S3 Bucket Structure**
```
your-s3-bucket/
├── garments/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── subfolder/
│       ├── image3.jpg
│       └── image4.jpg
└── other-files/
```

---

## 🚀 Usage

### 1. **Basic Usage**
```python
from s3_google_sheets_classifier import S3GoogleSheetsClassifier

# Initialize classifier
classifier = S3GoogleSheetsClassifier(
    s3_bucket="your-bucket-name",
    google_creds_path="path/to/credentials.json"
)

# Process all images in bucket
results = classifier.process_s3_images(
    spreadsheet_name="My_Garment_Classifications"
)

print(f"Spreadsheet URL: {results['spreadsheet_url']}")
```

### 2. **Advanced Usage**
```python
# Process specific folder with limits
results = classifier.process_s3_images(
    prefix="garments/summer_collection/",
    max_images=50,
    spreadsheet_name="Summer_Collection_Classifications"
)
```

### 3. **Command Line Usage**
```bash
python s3_google_sheets_classifier.py
```

---

## 📊 Google Sheets Output

The system creates a spreadsheet with the following columns:

| Column | Description |
|--------|-------------|
| **S3_Image_Key** | S3 path to the image |
| **Title** | Natural title (≤150 chars) |
| **Description** | Natural description (≤200 chars) |
| **Broad_Category** | Simplified category (Lehenga, Saree, etc.) |
| **Specific_Category** | Detailed category (Fishtail_Lehenga, etc.) |
| **Confidence** | Classification confidence (0-1) |
| **Is_Garment** | Whether image is classified as garment |
| **Processed_At** | Timestamp of processing |
| **Top_Prediction** | Top alternative prediction |
| **Top_Confidence** | Confidence of top alternative |

---

## 🎯 Features

### **Natural Language Generation**
- **Titles**: Varied, non-repetitive phrases (max 150 characters)
- **Descriptions**: Short, engaging descriptions (max 200 characters)
- **Broad Categories**: Simplified categories for better user experience

### **S3 Integration**
- **Batch Processing**: Process multiple images efficiently
- **Prefix Filtering**: Filter images by S3 prefix/folder
- **Progress Tracking**: Real-time progress updates
- **Error Handling**: Graceful handling of failed downloads

### **Google Sheets Features**
- **Auto-formatting**: Headers with colors and bold text
- **Multiple Worksheets**: Support for multiple data sheets
- **Existing Spreadsheet**: Can append to existing sheets
- **Backup**: Local JSON backup of all results

---

## 🔍 Example Output

### **Sample Google Sheets Row**
```
S3_Image_Key: garments/summer_collection/lehenga_001.jpg
Title: Elegant Lehenga
Description: A beautifully designed lehenga. Perfectly balances traditional charm with modern sophistication.
Broad_Category: Lehenga
Specific_Category: Fishtail_Lehenga
Confidence: 0.87
Is_Garment: TRUE
Processed_At: 2025-01-20T10:30:45.123456
Top_Prediction: A-line_Lehenga
Top_Confidence: 0.82
```

---

## ⚙️ Customization

### 1. **Modify Title Generation**
```python
def generate_natural_title(self, broad_category, confidence):
    # Add your custom title logic here
    pass
```

### 2. **Modify Description Generation**
```python
def generate_natural_description(self, broad_category, confidence):
    # Add your custom description logic here
    pass
```

### 3. **Add Custom Categories**
```python
def get_broad_category_mapping(self):
    mapping = {
        # Add your custom mappings
        "Custom_Category": "Broad_Category"
    }
    return mapping
```

---

## 🛡️ Security Best Practices

### 1. **AWS Security**
- Use IAM roles with minimal required permissions
- Enable S3 bucket encryption
- Use VPC endpoints for S3 access

### 2. **Google Sheets Security**
- Store credentials securely (not in code)
- Use service account with minimal permissions
- Regularly rotate service account keys

### 3. **Data Privacy**
- Ensure images don't contain sensitive information
- Review classification results before sharing
- Implement data retention policies

---

## 🔧 Troubleshooting

### **Common Issues**

#### 1. **AWS Credentials Error**
```bash
# Check AWS credentials
aws sts get-caller-identity
```

#### 2. **Google Sheets Permission Error**
- Ensure service account has "Editor" role
- Check if spreadsheet is shared with service account email

#### 3. **S3 Access Denied**
- Verify bucket permissions
- Check IAM policies for S3 access

#### 4. **Memory Issues with Large Images**
- Consider image resizing before processing
- Process images in smaller batches

---

## 📈 Performance Optimization

### 1. **Batch Processing**
```python
# Process in smaller batches for better memory management
results = classifier.process_s3_images(max_images=100)
```

### 2. **Prefix Filtering**
```python
# Process specific folders only
results = classifier.process_s3_images(prefix="garments/active/")
```

### 3. **Parallel Processing**
```python
# For large datasets, consider implementing parallel processing
# (Advanced: Use multiprocessing or asyncio)
```

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review AWS and Google Cloud documentation
3. Ensure all dependencies are correctly installed
4. Verify credentials and permissions

---

## 🎉 Ready to Use!

Your S3 to Google Sheets garment classifier is now ready to process images and generate professional-quality titles and descriptions! 🚀 