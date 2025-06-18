import os
import sys
from sqlalchemy import text, inspect
from app import app, db

def migrate_payment_method():
    """Add payment_method column to order table if it doesn't exist"""
    with app.app_context():
        # Check if payment_method column exists
        inspector = inspect(db.engine)
        columns = [col['name'] for col in inspector.get_columns('order')]
        
        if 'payment_method' not in columns:
            print("Adding payment_method column to order table...")
            try:
                db.session.execute(text("ALTER TABLE \"order\" ADD COLUMN payment_method VARCHAR(50) NOT NULL DEFAULT 'cod'"))
                db.session.commit()
                print("✅ payment_method column added successfully!")
            except Exception as e:
                print(f"❌ Error adding payment_method column: {e}")
                db.session.rollback()
                return False
        else:
            print("✅ payment_method column already exists!")
        
        return True

if __name__ == '__main__':
    migrate_payment_method() 