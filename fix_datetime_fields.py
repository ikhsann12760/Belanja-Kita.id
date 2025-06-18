#!/usr/bin/env python3
"""
Script untuk memperbaiki field datetime yang NULL di database
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv('config.env')

# Database configuration
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'ecommerce')

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def fix_datetime_fields():
    """Fix NULL datetime fields in database"""
    
    try:
        # Create database engine
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("🔄 Memperbaiki field datetime yang NULL...")
            
            current_time = datetime.utcnow()
            
            # Fix bank_account table
            print("📝 Memperbaiki tabel bank_account...")
            try:
                # Update created_at yang NULL
                conn.execute(text("""
                    UPDATE bank_account 
                    SET created_at = :current_time 
                    WHERE created_at IS NULL
                """), {"current_time": current_time})
                
                # Update updated_at yang NULL
                conn.execute(text("""
                    UPDATE bank_account 
                    SET updated_at = :current_time 
                    WHERE updated_at IS NULL
                """), {"current_time": current_time})
                
                conn.commit()
                print("✅ Field datetime di tabel bank_account berhasil diperbaiki")
            except Exception as e:
                print(f"⚠️  Error saat memperbaiki bank_account: {e}")
            
            # Fix payment table
            print("📝 Memperbaiki tabel payment...")
            try:
                # Update created_at yang NULL
                conn.execute(text("""
                    UPDATE payment 
                    SET created_at = :current_time 
                    WHERE created_at IS NULL
                """), {"current_time": current_time})
                
                # Update updated_at yang NULL
                conn.execute(text("""
                    UPDATE payment 
                    SET updated_at = :current_time 
                    WHERE updated_at IS NULL
                """), {"current_time": current_time})
                
                conn.commit()
                print("✅ Field datetime di tabel payment berhasil diperbaiki")
            except Exception as e:
                print(f"⚠️  Error saat memperbaiki payment: {e}")
            
            # Fix order table
            print("📝 Memperbaiki tabel order...")
            try:
                # Update payment_date yang NULL (jika ada)
                conn.execute(text("""
                    UPDATE "order" 
                    SET payment_date = :current_time 
                    WHERE payment_date IS NULL AND payment_status = 'paid'
                """), {"current_time": current_time})
                
                conn.commit()
                print("✅ Field payment_date di tabel order berhasil diperbaiki")
            except Exception as e:
                print(f"⚠️  Error saat memperbaiki order: {e}")
            
            print("\n🎉 Perbaikan field datetime selesai!")
            print("\n📊 Ringkasan perbaikan:")
            print("   ✅ Tabel bank_account - created_at, updated_at")
            print("   ✅ Tabel payment - created_at, updated_at")
            print("   ✅ Tabel order - payment_date (untuk order yang sudah dibayar)")
            
    except Exception as e:
        print(f"❌ Error saat memperbaiki database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fix_datetime_fields() 