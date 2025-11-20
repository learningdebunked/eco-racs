#!/usr/bin/env python3
"""
Automated Instacart Dataset Download Script

This script downloads the Instacart dataset using the Kaggle API.
Requires: pip install kaggle
"""

import os
import sys
import subprocess
from pathlib import Path
import zipfile


def check_kaggle_cli():
    """Check if Kaggle CLI is installed"""
    try:
        subprocess.run(['kaggle', '--version'], 
                      capture_output=True, 
                      check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_kaggle_credentials():
    """Check if Kaggle credentials are configured"""
    kaggle_json = Path.home() / '.kaggle' / 'kaggle.json'
    return kaggle_json.exists()


def download_file(filename, competition='instacart-market-basket-analysis'):
    """Download a single file from Kaggle"""
    print(f"\nDownloading {filename}...")
    
    try:
        # Download file
        cmd = [
            'kaggle', 'competitions', 'download',
            '-c', competition,
            '-f', filename,
            '-p', 'data/raw',
            '-q'
        ]
        
        subprocess.run(cmd, check=True)
        
        # Unzip
        zip_path = Path('data/raw') / f'{filename}.zip'
        if zip_path.exists():
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('data/raw')
            zip_path.unlink()  # Delete zip file
        
        print(f"✅ {filename} downloaded successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False


def verify_downloads():
    """Verify downloaded files"""
    import pandas as pd
    
    files = {
        "products.csv": 49688,
        "orders.csv": 3421083,
        "order_products__train.csv": 1384617,
    }
    
    print("\n" + "="*70)
    print("VERIFICATION")
    print("="*70)
    print()
    
    all_good = True
    for filename, expected_rows in files.items():
        filepath = Path('data/raw') / filename
        
        if not filepath.exists():
            print(f"❌ {filename}: NOT FOUND")
            all_good = False
            continue
        
        # Check file size
        size_mb = filepath.stat().st_size / (1024 * 1024)
        
        # Load and check rows
        try:
            df = pd.read_csv(filepath)
            actual_rows = len(df)
            
            if actual_rows == expected_rows:
                print(f"✅ {filename}: {actual_rows:,} rows, {size_mb:.1f} MB")
            else:
                print(f"⚠️  {filename}: {actual_rows:,} rows (expected {expected_rows:,}), {size_mb:.1f} MB")
        except Exception as e:
            print(f"❌ {filename}: Error reading file - {e}")
            all_good = False
    
    return all_good


def main():
    print("="*70)
    print("INSTACART DATASET DOWNLOAD")
    print("="*70)
    
    # Check Kaggle CLI
    if not check_kaggle_cli():
        print("\n❌ Kaggle CLI not found!")
        print("\nInstall with:")
        print("  pip install kaggle")
        print("\nThen setup credentials:")
        print("  1. Go to: https://www.kaggle.com/settings")
        print("  2. Click 'Create New API Token'")
        print("  3. Move kaggle.json to ~/.kaggle/")
        print("  4. Run: chmod 600 ~/.kaggle/kaggle.json")
        return 1
    
    # Check credentials
    if not check_kaggle_credentials():
        print("\n❌ Kaggle credentials not found!")
        print("\nSetup credentials:")
        print("  1. Go to: https://www.kaggle.com/settings")
        print("  2. Click 'Create New API Token'")
        print("  3. Move kaggle.json to ~/.kaggle/")
        print("  4. Run: chmod 600 ~/.kaggle/kaggle.json")
        return 1
    
    print("\n✅ Kaggle CLI configured")
    
    # Create data directory
    print("\nCreating data directory...")
    Path('data/raw').mkdir(parents=True, exist_ok=True)
    print("✅ data/raw/ created")
    
    # Download files
    print("\n" + "="*70)
    print("DOWNLOADING FILES")
    print("="*70)
    print("\n(This may take 5-10 minutes depending on your connection)")
    
    files_to_download = [
        ('products.csv', '~2 MB'),
        ('orders.csv', '~104 MB'),
        ('order_products__train.csv', '~551 MB'),
    ]
    
    success_count = 0
    for i, (filename, size) in enumerate(files_to_download, 1):
        print(f"\n[{i}/{len(files_to_download)}] {filename} ({size})")
        if download_file(filename):
            success_count += 1
    
    # Optional files
    print("\n" + "="*70)
    response = input("\nDownload optional files (aisles.csv, departments.csv)? [y/N]: ")
    
    if response.lower() in ['y', 'yes']:
        print("\nDownloading optional files...")
        download_file('aisles.csv')
        download_file('departments.csv')
    
    # Verify
    if success_count == len(files_to_download):
        all_good = verify_downloads()
        
        print("\n" + "="*70)
        print("DOWNLOAD COMPLETE")
        print("="*70)
        
        if all_good:
            print("\n✅ All files downloaded and verified successfully!")
            print("\nFiles location: data/raw/")
            print("\nNext steps:")
            print("  1. Process data: python3 scripts/process_data.py")
            print("  2. Test integration: python3 scripts/test_data_integration.py")
            print("  3. Run system: python3 examples/basic_usage.py")
            return 0
        else:
            print("\n⚠️  Some files have issues. Please check and re-download if needed.")
            return 1
    else:
        print("\n❌ Some downloads failed. Please check your connection and try again.")
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Download cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
