#!/usr/bin/env python3
"""
Auto-installation script for PostgreSQL Garment Classifier
Handles dependency installation and configuration validation
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    try:
        # Install from requirements.txt
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_dependencies():
    """Check if all required packages are installed."""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'torch', 'torchvision', 'clip', 'Pillow', 'numpy',
        'psycopg2', 'pandas', 'requests', 'tqdm'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
        return False
    
    print("✅ All dependencies are installed")
    return True

def validate_config():
    """Validate configuration file."""
    print("🔧 Validating configuration...")
    
    try:
        from config import DB_CONFIG, TABLE_NAME, IMAGE_COLUMN, ID_COLUMN
        
        # Check if config has been updated
        if DB_CONFIG['host'] == 'your-db-name.render.com':
            print("⚠️  Configuration not updated yet")
            print("   Please update config.py with your database details")
            return False
        
        print("✅ Configuration file is valid")
        return True
        
    except ImportError as e:
        print(f"❌ Configuration error: {e}")
        return False

def check_reference_images():
    """Check if reference images are available."""
    print("🖼️  Checking reference images...")
    
    reference_dir = "reference_images_pinterest"
    if not os.path.exists(reference_dir):
        print(f"❌ Reference directory '{reference_dir}' not found")
        return False
    
    # Count categories
    categories = [d for d in os.listdir(reference_dir) 
                 if os.path.isdir(os.path.join(reference_dir, d))]
    
    print(f"✅ Found {len(categories)} garment categories")
    return True

def create_example_files():
    """Create example files if they don't exist."""
    print("📝 Creating example files...")
    
    # Create __init__.py files
    init_files = [
        "core/__init__.py",
        "examples/__init__.py"
    ]
    
    for init_file in init_files:
        if not os.path.exists(init_file):
            with open(init_file, 'w') as f:
                f.write("# Package initialization\n")
            print(f"✅ Created {init_file}")

def main():
    """Main setup function."""
    print("🚀 PostgreSQL Garment Classifier - Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return False
    
    # Install dependencies
    if not install_dependencies():
        return False
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Check reference images
    if not check_reference_images():
        return False
    
    # Create example files
    create_example_files()
    
    # Validate configuration
    config_valid = validate_config()
    
    print("\n" + "=" * 50)
    print("🎉 Setup Complete!")
    
    if config_valid:
        print("✅ Ready to use!")
        print("\n📝 Next steps:")
        print("1. Run: python examples/01_test_connection.py")
        print("2. Run: python examples/02_safe_test.py")
        print("3. Run: python examples/03_full_classification.py")
    else:
        print("⚠️  Configuration needed!")
        print("\n📝 Next steps:")
        print("1. Update config.py with your database details")
        print("2. Run: python examples/01_test_connection.py")
        print("3. Run: python examples/02_safe_test.py")
        print("4. Run: python examples/03_full_classification.py")
    
    print("\n📚 See README.md for detailed instructions")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 