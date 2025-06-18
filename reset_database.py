#!/usr/bin/env python3
"""
Database Reset Script
This script drops all tables and recreates them with the correct schema.
"""

import os
from dotenv import load_dotenv
from app import app, db, User, Category, Product, Order, OrderItem, CustomerSupport
from werkzeug.security import generate_password_hash
from datetime import datetime, date
from sqlalchemy import text

# Load environment variables
load_dotenv('config.env')

def reset_database():
    """Drop all tables and recreate them"""
    
    with app.app_context():
        # Drop all tables
        db.drop_all()
        print("✅ Semua tabel berhasil dihapus")
        
        # Create all tables
        db.create_all()
        print("✅ Semua tabel berhasil dibuat ulang")
        
        # Add payment_method column to order table if it doesn't exist
        try:
            db.session.execute(text("ALTER TABLE \"order\" ADD COLUMN payment_method VARCHAR(50) NOT NULL DEFAULT 'cod'"))
            db.session.commit()
            print("Added payment_method column to order table")
        except Exception as e:
            print(f"Payment method column might already exist: {e}")
            db.session.rollback()
        
        # Create default admin user
        admin = User(
            username='admin',
            email='admin@belanjakita.id',
            password_hash=generate_password_hash('admin123'),
            is_admin=True,
            full_name='Administrator',
            phone='081234567890',
            address='Jl. Admin No. 1',
            city='Jakarta',
            postal_code='12345',
            province='DKI Jakarta',
            date_of_birth=date(1990, 1, 1),
            gender='Male',
            is_active=True
        )
        db.session.add(admin)
        print("✅ Admin user berhasil dibuat")
        
        # Create default categories
        categories = [
            Category(name='Elektronik', description='Produk elektronik dan gadget'),
            Category(name='Pakaian', description='Pakaian dan fashion'),
            Category(name='Makanan', description='Makanan dan minuman'),
            Category(name='Buku', description='Buku dan literatur'),
            Category(name='Olahraga', description='Perlengkapan olahraga'),
            Category(name='Hobi', description='Produk hobi dan rekreasi')
        ]
        for category in categories:
            db.session.add(category)
        print("✅ Kategori default berhasil dibuat")
        
        # Create sample customer
        customer = User(
            username='customer',
            email='customer@example.com',
            password_hash=generate_password_hash('customer123'),
            is_admin=False,
            full_name='John Doe',
            phone='081234567891',
            address='Jl. Customer No. 1',
            city='Bandung',
            postal_code='40111',
            province='Jawa Barat',
            date_of_birth=date(1995, 5, 15),
            gender='Male',
            is_active=True
        )
        db.session.add(customer)
        
        # Commit to get IDs
        db.session.commit()
        
        # Create sample products
        products = [
            Product(
                name='Smartphone Samsung Galaxy A54',
                description='Smartphone Android terbaru dengan kamera 50MP, layar 6.4 inch, dan baterai 5000mAh. Dilengkapi dengan processor Exynos 1380 dan RAM 8GB.',
                price=4500000,
                stock=25,
                category_id=1,  # Elektronik
                image_url='uploads/NarutoCoverTankobon1.jpg',
                sku='ELE-SMA-0001',
                brand='Samsung',
                model='Galaxy A54',
                color='Hitam',
                material='Gorilla Glass',
                weight=202.0,
                dimensions='15.8x7.6x0.8',
                warranty='1 tahun',
                min_stock=5,
                tags='smartphone, android, samsung, kamera',
                meta_title='Samsung Galaxy A54 - Smartphone Android Terbaru',
                meta_description='Smartphone Samsung Galaxy A54 dengan kamera 50MP dan layar 6.4 inch. Dapatkan harga terbaik di Belanja Kita.id',
                is_featured=True,
                is_active=True
            ),
            Product(
                name='Sepatu Nike Air Max 270',
                description='Sepatu olahraga dengan teknologi Air Max untuk kenyamanan maksimal. Cocok untuk running dan casual wear.',
                price=2500000,
                stock=15,
                category_id=2,  # Pakaian
                image_url='uploads/NarutoCoverTankobon1.jpg',
                sku='PAK-SEP-0001',
                brand='Nike',
                model='Air Max 270',
                color='Putih',
                material='Mesh dan Foam',
                weight=320.0,
                dimensions='30x12x8',
                warranty='6 bulan',
                min_stock=3,
                tags='sepatu, nike, olahraga, running',
                meta_title='Nike Air Max 270 - Sepatu Olahraga Terbaik',
                meta_description='Sepatu Nike Air Max 270 dengan teknologi Air Max untuk kenyamanan maksimal. Tersedia di Belanja Kita.id',
                is_featured=True,
                is_active=True
            ),
            Product(
                name='Laptop ASUS ROG Strix G15',
                description='Laptop gaming dengan processor AMD Ryzen 7, GPU RTX 3060, RAM 16GB, dan SSD 512GB. Performa gaming yang luar biasa.',
                price=15000000,
                stock=8,
                category_id=1,  # Elektronik
                image_url='uploads/NarutoCoverTankobon1.jpg',
                sku='ELE-LAP-0001',
                brand='ASUS',
                model='ROG Strix G15',
                color='Hitam',
                material='Plastik dan Metal',
                weight=2100.0,
                dimensions='35.4x25.9x2.3',
                warranty='2 tahun',
                min_stock=2,
                tags='laptop, gaming, asus, rog',
                meta_title='ASUS ROG Strix G15 - Laptop Gaming Terbaik',
                meta_description='Laptop gaming ASUS ROG Strix G15 dengan processor AMD Ryzen 7 dan GPU RTX 3060. Performa gaming terbaik.',
                is_featured=True,
                is_active=True
            ),
            Product(
                name='Buku Novel "Laskar Pelangi"',
                description='Novel bestseller karya Andrea Hirata yang mengisahkan perjuangan anak-anak di Belitung untuk mendapatkan pendidikan.',
                price=85000,
                stock=50,
                category_id=4,  # Buku
                image_url='uploads/NarutoCoverTankobon1.jpg',
                sku='BUK-NOV-0001',
                brand='Bentang Pustaka',
                model='Paperback',
                color='Putih',
                material='Kertas',
                weight=350.0,
                dimensions='20x13x2',
                warranty='-',
                min_stock=10,
                tags='buku, novel, indonesia, pendidikan',
                meta_title='Laskar Pelangi - Novel Bestseller Andrea Hirata',
                meta_description='Novel Laskar Pelangi karya Andrea Hirata. Kisah inspiratif tentang perjuangan pendidikan di Belitung.',
                is_featured=False,
                is_active=True
            ),
            Product(
                name='Raket Badminton Yonex Voltric Z-Force II',
                description='Raket badminton profesional dengan teknologi Tri-Voltage System untuk power dan kontrol yang optimal.',
                price=2800000,
                stock=12,
                category_id=5,  # Olahraga
                image_url='uploads/NarutoCoverTankobon1.jpg',
                sku='OLA-RAK-0001',
                brand='Yonex',
                model='Voltric Z-Force II',
                color='Hitam Merah',
                material='Carbon Fiber',
                weight=85.0,
                dimensions='68x22x1',
                warranty='1 tahun',
                min_stock=3,
                tags='raket, badminton, yonex, olahraga',
                meta_title='Yonex Voltric Z-Force II - Raket Badminton Profesional',
                meta_description='Raket badminton Yonex Voltric Z-Force II dengan teknologi Tri-Voltage System. Untuk pemain profesional.',
                is_featured=False,
                is_active=True
            )
        ]
        for product in products:
            db.session.add(product)
        
        # Create sample order
        order = Order(
            user_id=customer.id,
            order_number='BK-20250618-0001',
            total_amount=2525000,
            status='pending',
            recipient_name='John Doe',
            recipient_phone='081234567891',
            shipping_address='Jl. Customer No. 1, RT 001 RW 002',
            shipping_city='Bandung',
            shipping_postal_code='40111',
            shipping_province='Jawa Barat',
            courier='jne',
            shipping_cost=15000,
            tracking_number='JNE-20250618-ABC123',
            notes='Tolong dibungkus dengan rapi',
            payment_method='transfer'
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=1,  # Samsung Galaxy A54
            quantity=1,
            price=4500000
        )
        db.session.add(order_item)
        
        # Create sample support ticket
        support_ticket = CustomerSupport(
            user_id=customer.id,
            subject='Pertanyaan tentang produk',
            message='Saya ingin bertanya tentang spesifikasi lengkap smartphone Samsung Galaxy A54. Apakah ada warna lain selain hitam?',
            category='Question',
            priority='medium',
            status='open'
        )
        db.session.add(support_ticket)
        
        db.session.commit()
        
        print("✅ Database berhasil direset!")
        print("\n📋 Informasi Login Admin:")
        print("Username: admin")
        print("Password: admin123")
        print("\nCustomer credentials:")
        print("Username: customer")
        print("Password: customer123")

if __name__ == "__main__":
    print("🔄 PostgreSQL Database Reset")
    print("=" * 40)
    
    # Confirm before proceeding
    response = input("⚠️  This will DELETE ALL DATA in the database. Continue? (y/N): ")
    
    if response.lower() == 'y':
        reset_database()
        print("\n🎉 Database reset successful!")
        print("You can now run: python app.py")
    else:
        print("❌ Database reset cancelled.") 