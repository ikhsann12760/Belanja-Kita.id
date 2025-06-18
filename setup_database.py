#!/usr/bin/env python3
"""
Database Setup Script for PostgreSQL
This script helps you set up the PostgreSQL database for the e-commerce application.
"""

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

def create_database():
    """Create the database if it doesn't exist"""
    
    # Database connection parameters
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '12345')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'E_commerce')
    
    try:
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database='postgres'  # Connect to default postgres database
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (DB_NAME,))
        exists = cursor.fetchone()
        
        if not exists:
            # Create database
            cursor.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"✅ Database '{DB_NAME}' berhasil dibuat!")
        else:
            print(f"ℹ️  Database '{DB_NAME}' sudah ada.")
        
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"❌ Error saat membuat database: {e}")
        print("\nPastikan PostgreSQL sudah terinstall dan berjalan.")
        print("Untuk Windows, Anda bisa menggunakan:")
        print("1. PostgreSQL installer dari https://www.postgresql.org/download/windows/")
        print("2. Atau menggunakan Docker: docker run --name postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres")
        return False
    
    return True

def test_connection():
    """Test connection to the database"""
    
    # Database connection parameters
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'ecommerce')
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        
        print(f"✅ Koneksi ke database berhasil!")
        print(f"📊 PostgreSQL version: {version[0]}")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Error saat koneksi ke database: {e}")
        return False

def main():
    print("🚀 PostgreSQL Database Setup")
    print("=" * 40)
    
    # Check if config.env exists
    if not os.path.exists('config.env'):
        print("❌ File config.env tidak ditemukan!")
        print("Buat file config.env dengan konfigurasi database Anda.")
        return
    
    print("📋 Konfigurasi database dari config.env:")
    load_dotenv('config.env')
    print(f"   User: {os.getenv('DB_USER', 'postgres')}")
    print(f"   Host: {os.getenv('DB_HOST', 'localhost')}")
    print(f"   Port: {os.getenv('DB_PORT', '5432')}")
    print(f"   Database: {os.getenv('DB_NAME', 'ecommerce')}")
    print()
    
    # Create database
    if create_database():
        # Test connection
        test_connection()
        
        print("\n🎉 Setup database selesai!")
        print("Sekarang Anda bisa menjalankan aplikasi dengan:")
        print("   python app.py")
    else:
        print("\n❌ Setup database gagal!")

if __name__ == "__main__":
    main() 