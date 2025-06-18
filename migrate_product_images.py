#!/usr/bin/env python3
"""
Migration script untuk menambahkan tabel ProductImage dan memigrasikan gambar produk yang ada
"""

import os
import sys
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db, Product, ProductImage

def migrate_product_images():
    """Migrate existing product images to new ProductImage table"""
    with app.app_context():
        print("🔄 Memulai migrasi gambar produk...")
        
        # Create ProductImage table
        try:
            db.create_all()
            print("✅ Tabel ProductImage berhasil dibuat")
        except Exception as e:
            print(f"❌ Error membuat tabel: {e}")
            return
        
        # Get all products with existing images
        products_with_images = Product.query.filter(Product.image_url.isnot(None)).all()
        
        migrated_count = 0
        for product in products_with_images:
            if product.image_url and product.image_url.strip():
                # Check if image already migrated
                existing_image = ProductImage.query.filter_by(
                    product_id=product.id,
                    image_url=product.image_url
                ).first()
                
                if not existing_image:
                    # Create new ProductImage record
                    product_image = ProductImage(
                        product_id=product.id,
                        image_url=product.image_url,
                        alt_text=f"Gambar {product.name}",
                        is_primary=True,  # Set as primary image
                        sort_order=0
                    )
                    
                    try:
                        db.session.add(product_image)
                        db.session.commit()
                        migrated_count += 1
                        print(f"✅ Migrasi gambar untuk produk: {product.name}")
                    except Exception as e:
                        print(f"❌ Error migrasi gambar untuk {product.name}: {e}")
                        db.session.rollback()
                else:
                    print(f"⏭️  Gambar sudah ada untuk produk: {product.name}")
        
        print(f"\n🎉 Migrasi selesai! {migrated_count} gambar berhasil dimigrasikan")
        
        # Show statistics
        total_products = Product.query.count()
        products_with_images = ProductImage.query.count()
        
        print(f"\n📊 Statistik:")
        print(f"   - Total produk: {total_products}")
        print(f"   - Produk dengan gambar: {products_with_images}")
        
        if products_with_images > 0:
            print(f"\n📋 Daftar produk dengan gambar:")
            product_images = ProductImage.query.join(Product).order_by(Product.name).all()
            for img in product_images:
                print(f"   - {img.product.name}: {img.image_url}")

def cleanup_old_image_urls():
    """Clean up old image_url field from Product table after migration"""
    with app.app_context():
        print("\n🧹 Membersihkan field image_url lama...")
        
        try:
            # Update all products to set image_url to None
            Product.query.update({Product.image_url: None})
            db.session.commit()
            print("✅ Field image_url berhasil dibersihkan")
        except Exception as e:
            print(f"❌ Error membersihkan field image_url: {e}")
            db.session.rollback()

if __name__ == '__main__':
    print("🚀 Product Image Migration Tool")
    print("=" * 50)
    
    # Run migration
    migrate_product_images()
    
    # Ask if user wants to cleanup old image_url field
    response = input("\n❓ Apakah Anda ingin membersihkan field image_url lama? (y/N): ")
    if response.lower() in ['y', 'yes']:
        cleanup_old_image_urls()
    
    print("\n✨ Migrasi selesai!") 