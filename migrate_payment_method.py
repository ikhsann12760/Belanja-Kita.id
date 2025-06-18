#!/usr/bin/env python3
"""
Migration script untuk menambahkan tabel BankAccount dan Payment
serta field payment_method ke tabel Order
"""

import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv('config.env')

# Database configuration
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'ecommerce')

DATABASE_URL = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

def migrate_database():
    """Migrate database to add payment-related tables and fields"""
    
    try:
        # Create database engine
        engine = create_engine(DATABASE_URL)
        
        with engine.connect() as conn:
            print("🔄 Memulai migrasi database...")
            
            # 1. Add payment_method column to order table if not exists
            print("📝 Menambahkan kolom payment_method ke tabel order...")
            try:
                conn.execute(text("""
                    ALTER TABLE "order" 
                    ADD COLUMN IF NOT EXISTS payment_method VARCHAR(50) NOT NULL DEFAULT 'cod'
                """))
                conn.commit()
                print("✅ Kolom payment_method berhasil ditambahkan")
            except Exception as e:
                print(f"⚠️  Kolom payment_method sudah ada atau error: {e}")
            
            # 2. Add payment_status column to order table
            print("📝 Menambahkan kolom payment_status ke tabel order...")
            try:
                conn.execute(text("""
                    ALTER TABLE "order" 
                    ADD COLUMN IF NOT EXISTS payment_status VARCHAR(50) DEFAULT 'pending'
                """))
                conn.commit()
                print("✅ Kolom payment_status berhasil ditambahkan")
            except Exception as e:
                print(f"⚠️  Kolom payment_status sudah ada atau error: {e}")
            
            # 3. Add payment_date column to order table
            print("📝 Menambahkan kolom payment_date ke tabel order...")
            try:
                conn.execute(text("""
                    ALTER TABLE "order" 
                    ADD COLUMN IF NOT EXISTS payment_date TIMESTAMP
                """))
                conn.commit()
                print("✅ Kolom payment_date berhasil ditambahkan")
            except Exception as e:
                print(f"⚠️  Kolom payment_date sudah ada atau error: {e}")
            
            # 4. Add payment_reference column to order table
            print("📝 Menambahkan kolom payment_reference ke tabel order...")
            try:
                conn.execute(text("""
                    ALTER TABLE "order" 
                    ADD COLUMN IF NOT EXISTS payment_reference VARCHAR(100)
                """))
                conn.commit()
                print("✅ Kolom payment_reference berhasil ditambahkan")
            except Exception as e:
                print(f"⚠️  Kolom payment_reference sudah ada atau error: {e}")
            
            # 5. Create bank_account table
            print("🏦 Membuat tabel bank_account...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS bank_account (
                        id SERIAL PRIMARY KEY,
                        bank_name VARCHAR(100) NOT NULL,
                        account_number VARCHAR(50) NOT NULL,
                        account_holder VARCHAR(100) NOT NULL,
                        account_type VARCHAR(50),
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        notes TEXT
                    )
                """))
                conn.commit()
                print("✅ Tabel bank_account berhasil dibuat")
            except Exception as e:
                print(f"⚠️  Tabel bank_account sudah ada atau error: {e}")
            
            # 6. Add bank_account_id column to order table
            print("📝 Menambahkan kolom bank_account_id ke tabel order...")
            try:
                conn.execute(text("""
                    ALTER TABLE "order" 
                    ADD COLUMN IF NOT EXISTS bank_account_id INTEGER REFERENCES bank_account(id)
                """))
                conn.commit()
                print("✅ Kolom bank_account_id berhasil ditambahkan")
            except Exception as e:
                print(f"⚠️  Kolom bank_account_id sudah ada atau error: {e}")
            
            # 7. Create payment table
            print("💳 Membuat tabel payment...")
            try:
                conn.execute(text("""
                    CREATE TABLE IF NOT EXISTS payment (
                        id SERIAL PRIMARY KEY,
                        order_id INTEGER NOT NULL REFERENCES "order"(id),
                        amount NUMERIC(10,2) NOT NULL,
                        payment_method VARCHAR(50) NOT NULL,
                        payment_status VARCHAR(50) DEFAULT 'pending',
                        payment_date TIMESTAMP,
                        bank_account_id INTEGER REFERENCES bank_account(id),
                        reference_number VARCHAR(100),
                        transaction_id VARCHAR(100),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                        notes TEXT
                    )
                """))
                conn.commit()
                print("✅ Tabel payment berhasil dibuat")
            except Exception as e:
                print(f"⚠️  Tabel payment sudah ada atau error: {e}")
            
            # 8. Insert sample bank accounts
            print("🏦 Menambahkan contoh rekening bank...")
            try:
                # Check if bank accounts already exist
                result = conn.execute(text("SELECT COUNT(*) FROM bank_account"))
                count = result.scalar()
                
                if count == 0:
                    conn.execute(text("""
                        INSERT INTO bank_account (bank_name, account_number, account_holder, account_type, notes) 
                        VALUES 
                        ('BCA', '1234567890', 'Belanja Kita.id', 'Business', 'Rekening utama untuk pembayaran'),
                        ('Mandiri', '0987654321', 'Belanja Kita.id', 'Business', 'Rekening alternatif'),
                        ('BNI', '1122334455', 'Belanja Kita.id', 'Business', 'Rekening untuk transfer cepat')
                    """))
                    conn.commit()
                    print("✅ Contoh rekening bank berhasil ditambahkan")
                else:
                    print("ℹ️  Rekening bank sudah ada, skip insert")
            except Exception as e:
                print(f"⚠️  Error saat menambah rekening bank: {e}")
            
            # 9. Create triggers for updated_at
            print("🔄 Membuat trigger untuk auto-update updated_at...")
            try:
                # Trigger for bank_account table
                conn.execute(text("""
                    CREATE OR REPLACE FUNCTION update_updated_at_column()
                    RETURNS TRIGGER AS $$
                    BEGIN
                        NEW.updated_at = CURRENT_TIMESTAMP;
                        RETURN NEW;
                    END;
                    $$ language 'plpgsql';
                """))
                
                # Create trigger for bank_account
                conn.execute(text("""
                    DROP TRIGGER IF EXISTS update_bank_account_updated_at ON bank_account;
                    CREATE TRIGGER update_bank_account_updated_at
                        BEFORE UPDATE ON bank_account
                        FOR EACH ROW
                        EXECUTE FUNCTION update_updated_at_column();
                """))
                
                # Create trigger for payment
                conn.execute(text("""
                    DROP TRIGGER IF EXISTS update_payment_updated_at ON payment;
                    CREATE TRIGGER update_payment_updated_at
                        BEFORE UPDATE ON payment
                        FOR EACH ROW
                        EXECUTE FUNCTION update_updated_at_column();
                """))
                
                conn.commit()
                print("✅ Trigger auto-update updated_at berhasil dibuat")
            except Exception as e:
                print(f"⚠️  Error saat membuat trigger: {e}")
            
            print("\n🎉 Migrasi database selesai!")
            print("\n📊 Ringkasan perubahan:")
            print("   ✅ Tabel bank_account - untuk menyimpan rekening bank")
            print("   ✅ Tabel payment - untuk tracking pembayaran")
            print("   ✅ Field payment_method di tabel order")
            print("   ✅ Field payment_status di tabel order")
            print("   ✅ Field payment_date di tabel order")
            print("   ✅ Field payment_reference di tabel order")
            print("   ✅ Field bank_account_id di tabel order")
            print("   ✅ Contoh rekening bank (BCA, Mandiri, BNI)")
            print("   ✅ Trigger auto-update updated_at")
            
    except Exception as e:
        print(f"❌ Error saat migrasi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    migrate_database() 