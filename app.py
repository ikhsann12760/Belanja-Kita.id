from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from config.env
load_dotenv('config.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

# PostgreSQL Database Configuration
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'ecommerce')

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='customer', lazy=True)
    
    # Customer Profile Fields
    full_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    postal_code = db.Column(db.String(10))
    province = db.Column(db.String(50))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(10))  # Male, Female, Other
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bank_name = db.Column(db.String(100), nullable=False)  # BCA, Mandiri, BNI, dll
    account_number = db.Column(db.String(50), nullable=False)
    account_holder = db.Column(db.String(100), nullable=False)
    account_type = db.Column(db.String(50))  # Savings, Current, Business
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text)  # Additional notes
    
    # Relationships
    payments = db.relationship('Payment', backref='bank_account', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    products = db.relationship('Product', backref='category', lazy=True)

class ProductImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    alt_text = db.Column(db.String(200))  # Alt text for accessibility
    is_primary = db.Column(db.Boolean, default=False)  # Primary/main image
    sort_order = db.Column(db.Integer, default=0)  # For ordering images
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    product = db.relationship('Product', backref='images')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Changed to Numeric for better precision
    stock = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(200))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Additional fields for better product management
    sku = db.Column(db.String(50), unique=True)  # Stock Keeping Unit
    weight = db.Column(db.Numeric(8, 2))  # Weight in grams
    dimensions = db.Column(db.String(100))  # Length x Width x Height in cm
    brand = db.Column(db.String(100))  # Product brand
    model = db.Column(db.String(100))  # Product model
    color = db.Column(db.String(50))  # Product color
    material = db.Column(db.String(100))  # Product material
    warranty = db.Column(db.String(100))  # Warranty information
    is_featured = db.Column(db.Boolean, default=False)  # Featured product
    is_active = db.Column(db.Boolean, default=True)  # Product status
    min_stock = db.Column(db.Integer, default=5)  # Minimum stock level for alerts
    tags = db.Column(db.Text)  # Product tags for search
    meta_title = db.Column(db.String(200))  # SEO meta title
    meta_description = db.Column(db.Text)  # SEO meta description

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_number = db.Column(db.String(20), unique=True, nullable=False)  # Auto-generated order number
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)
    
    # Shipping Information
    recipient_name = db.Column(db.String(100), nullable=False)
    recipient_phone = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    shipping_city = db.Column(db.String(50), nullable=False)
    shipping_postal_code = db.Column(db.String(10), nullable=False)
    shipping_province = db.Column(db.String(50), nullable=False)
    courier = db.Column(db.String(50), nullable=False)  # JNE, SiCepat, etc.
    shipping_cost = db.Column(db.Numeric(10, 2), default=0)
    tracking_number = db.Column(db.String(50))  # Auto-generated tracking number
    notes = db.Column(db.Text)  # Additional notes from customer
    payment_method = db.Column(db.String(50), nullable=False)  # Payment method (COD, Transfer, E-Wallet, etc.)
    
    # Payment Information
    payment_status = db.Column(db.String(50), default='pending')  # pending, paid, failed, refunded
    payment_date = db.Column(db.DateTime)
    payment_reference = db.Column(db.String(100))  # Reference number from payment gateway
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'))  # For bank transfers
    
    # Relationships
    payment = db.relationship('Payment', backref='order', uselist=False)

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(50), default='pending')
    payment_date = db.Column(db.DateTime)
    bank_account_id = db.Column(db.Integer, db.ForeignKey('bank_account.id'))
    reference_number = db.Column(db.String(100))  # Bank reference, payment gateway reference
    transaction_id = db.Column(db.String(100))  # Payment gateway transaction ID
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    notes = db.Column(db.Text)  # Admin notes about payment

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    product = db.relationship('Product', backref='order_items')

class CustomerSupport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)  # Complaint, Question, Suggestion, Technical
    priority = db.Column(db.String(20), default='medium')  # Low, Medium, High, Urgent
    status = db.Column(db.String(20), default='open')  # Open, In Progress, Resolved, Closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = db.Column(db.DateTime)
    resolved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin_notes = db.Column(db.Text)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='support_tickets')
    admin = db.relationship('User', foreign_keys=[resolved_by], backref='resolved_tickets')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Utility Functions
def generate_order_number():
    """Generate unique order number"""
    import random
    import string
    
    while True:
        # Format: BK-YYYYMMDD-XXXX (Belanja Kita - Date - Random)
        date_part = datetime.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.digits, k=4))
        order_number = f"BK-{date_part}-{random_part}"
        
        # Check if order number already exists
        if not Order.query.filter_by(order_number=order_number).first():
            return order_number

def generate_tracking_number(courier):
    """Generate tracking number based on courier"""
    import random
    import string
    
    # Courier prefixes
    courier_prefixes = {
        'jne': 'JNE',
        'sicepat': 'SIC',
        'jnt': 'JNT',
        'pos': 'POS',
        'ninja': 'NIN'
    }
    
    prefix = courier_prefixes.get(courier.lower(), 'TRK')
    
    while True:
        # Format: PREFIX-YYYYMMDD-XXXXX
        date_part = datetime.now().strftime('%Y%m%d')
        random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
        tracking_number = f"{prefix}-{date_part}-{random_part}"
        
        # Check if tracking number already exists
        if not Order.query.filter_by(tracking_number=tracking_number).first():
            return tracking_number

def generate_sku(category_name, product_name):
    """Generate SKU based on category and product name"""
    import random
    import string
    
    # Get category prefix (first 3 letters)
    category_prefix = category_name[:3].upper()
    
    # Get product prefix (first 3 letters)
    product_prefix = product_name[:3].upper()
    
    while True:
        # Format: CAT-PRO-XXXX
        random_part = ''.join(random.choices(string.digits, k=4))
        sku = f"{category_prefix}-{product_prefix}-{random_part}"
        
        # Check if SKU already exists
        if not Product.query.filter_by(sku=sku).first():
            return sku

# Routes
@app.route('/')
def index():
    products = Product.query.all()
    categories = Category.query.all()
    
    # Get users for admin order creation
    users = []
    if current_user.is_authenticated and current_user.is_admin:
        users = User.query.filter_by(is_admin=False).all()
    
    return render_template('index.html', products=products, categories=categories, users=users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login berhasil!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan!', 'error')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email sudah digunakan!', 'error')
            return render_template('register.html')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registrasi berhasil! Silakan login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout berhasil!', 'success')
    return redirect(url_for('index'))

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('product_detail.html', product=product)

@app.route('/products')
def products():
    # Get filter parameters
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    
    # Base query - only active products
    products_query = Product.query.filter_by(is_active=True)
    
    # Apply category filter
    if category_filter:
        products_query = products_query.filter_by(category_id=category_filter)
    
    # Apply search filter
    if search_query:
        products_query = products_query.filter(
            Product.name.ilike(f'%{search_query}%') |
            Product.description.ilike(f'%{search_query}%') |
            Product.brand.ilike(f'%{search_query}%')
        )
    
    # Get filtered products
    products = products_query.all()
    categories = Category.query.all()
    
    return render_template('products.html', 
                         products=products, 
                         categories=categories,
                         selected_category=category_filter,
                         search_query=search_query)

@app.route('/admin')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    # Get filter parameters
    category_filter = request.args.get('category', 'all')
    
    # Get all categories for filter dropdown
    categories = Category.query.all()
    
    # Filter products based on category
    if category_filter == 'all':
        products = Product.query.all()
    else:
        products = Product.query.filter_by(category_id=category_filter).all()
    
    orders = Order.query.all()
    users = User.query.all()
    
    return render_template('admin/dashboard.html', 
                         products=products, 
                         orders=orders, 
                         users=users, 
                         categories=categories,
                         selected_category=category_filter)

@app.route('/admin/products')
@login_required
def admin_products():
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    # Get filter parameters
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    stock_filter = request.args.get('stock', '')
    
    # Base query
    products_query = Product.query
    
    # Apply category filter
    if category_filter:
        products_query = products_query.filter_by(category_id=category_filter)
    
    # Apply search filter
    if search_query:
        products_query = products_query.filter(
            Product.name.ilike(f'%{search_query}%') |
            Product.description.ilike(f'%{search_query}%') |
            Product.sku.ilike(f'%{search_query}%') |
            Product.brand.ilike(f'%{search_query}%')
        )
    
    # Apply stock filter
    if stock_filter == 'in_stock':
        products_query = products_query.filter(Product.stock > 0)
    elif stock_filter == 'out_of_stock':
        products_query = products_query.filter(Product.stock == 0)
    elif stock_filter == 'low_stock':
        products_query = products_query.filter(Product.stock <= Product.min_stock)
    
    # Get filtered products
    products = products_query.all()
    categories = Category.query.all()
    
    return render_template('admin/products.html', 
                         products=products, 
                         categories=categories,
                         selected_category=category_filter,
                         search_query=search_query,
                         stock_filter=stock_filter)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        category_id = int(request.form.get('category_id'))
        
        # Get category for SKU generation
        category = Category.query.get(category_id)
        
        # Additional fields
        brand = request.form.get('brand', '')
        model = request.form.get('model', '')
        color = request.form.get('color', '')
        material = request.form.get('material', '')
        weight = float(request.form.get('weight', 0)) if request.form.get('weight') else None
        dimensions = request.form.get('dimensions', '')
        warranty = request.form.get('warranty', '')
        min_stock = int(request.form.get('min_stock', 5))
        tags = request.form.get('tags', '')
        meta_title = request.form.get('meta_title', '')
        meta_description = request.form.get('meta_description', '')
        is_featured = 'is_featured' in request.form
        is_active = 'is_active' in request.form
        
        # Create product first
        product = Product(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
            sku=generate_sku(category.name, name),
            brand=brand,
            model=model,
            color=color,
            material=material,
            weight=weight,
            dimensions=dimensions,
            warranty=warranty,
            min_stock=min_stock,
            tags=tags,
            meta_title=meta_title,
            meta_description=meta_description,
            is_featured=is_featured,
            is_active=is_active
        )
        
        db.session.add(product)
        db.session.flush()  # Get product ID
        
        # Handle multiple image uploads
        images = request.files.getlist('product_images')
        image_primary_list = request.form.getlist('image_primary')
        image_order_list = request.form.getlist('image_order')
        
        if not images or not images[0].filename:
            flash('Minimal 1 gambar produk harus diupload!', 'error')
            db.session.rollback()
            categories = Category.query.all()
            return render_template('admin/add_product.html', categories=categories)
        
        # Process each image
        for i, image in enumerate(images):
            if image and image.filename:
                # Validate file size (5MB max)
                if len(image.read()) > 5 * 1024 * 1024:
                    flash(f'Gambar {image.filename} terlalu besar. Maksimal 5MB.', 'error')
                    db.session.rollback()
                    categories = Category.query.all()
                    return render_template('admin/add_product.html', categories=categories)
                
                # Reset file pointer
                image.seek(0)
                
                # Save image
                filename = secure_filename(f"{product.id}_{i}_{image.filename}")
                image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                image_url = f'uploads/{filename}'
                
                # Check if this is primary image
                is_primary = i < len(image_primary_list) and image_primary_list[i] == '1'
                sort_order = i < len(image_order_list) and int(image_order_list[i]) or i
                
                # Create ProductImage record
                product_image = ProductImage(
                    product_id=product.id,
                    image_url=image_url,
                    alt_text=f"Gambar {product.name}",
                    is_primary=is_primary,
                    sort_order=sort_order
                )
                
                db.session.add(product_image)
        
        # Set first image as primary if no primary image set
        if not any(img.is_primary for img in product.images):
            if product.images:
                product.images[0].is_primary = True
        
        # Set main image_url for backward compatibility
        primary_image = next((img for img in product.images if img.is_primary), None)
        if primary_image:
            product.image_url = primary_image.image_url
        
        db.session.commit()
        flash('Produk berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/products/edit/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        product.category_id = int(request.form.get('category_id'))
        
        # Additional fields
        product.brand = request.form.get('brand', '')
        product.model = request.form.get('model', '')
        product.color = request.form.get('color', '')
        product.material = request.form.get('material', '')
        product.weight = float(request.form.get('weight', 0)) if request.form.get('weight') else None
        product.dimensions = request.form.get('dimensions', '')
        product.warranty = request.form.get('warranty', '')
        product.min_stock = int(request.form.get('min_stock', 5))
        product.tags = request.form.get('tags', '')
        product.meta_title = request.form.get('meta_title', '')
        product.meta_description = request.form.get('meta_description', '')
        product.is_featured = 'is_featured' in request.form
        product.is_active = 'is_active' in request.form
        
        # Handle new image uploads
        images = request.files.getlist('product_images')
        image_primary_list = request.form.getlist('image_primary')
        image_order_list = request.form.getlist('image_order')
        
        # Process new images if any
        if images and images[0].filename:
            # Count existing images
            existing_count = len(product.images)
            max_images = 10
            
            if existing_count + len(images) > max_images:
                flash(f'Maksimal {max_images} gambar per produk!', 'error')
                categories = Category.query.all()
                return render_template('admin/edit_product.html', product=product, categories=categories)
            
            # Process each new image
            for i, image in enumerate(images):
                if image and image.filename:
                    # Validate file size (5MB max)
                    if len(image.read()) > 5 * 1024 * 1024:
                        flash(f'Gambar {image.filename} terlalu besar. Maksimal 5MB.', 'error')
                        categories = Category.query.all()
                        return render_template('admin/edit_product.html', product=product, categories=categories)
                    
                    # Reset file pointer
                    image.seek(0)
                    
                    # Save image
                    filename = secure_filename(f"{product.id}_{existing_count + i}_{image.filename}")
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    image_url = f'uploads/{filename}'
                    
                    # Check if this is primary image
                    is_primary = i < len(image_primary_list) and image_primary_list[i] == '1'
                    sort_order = existing_count + (i < len(image_order_list) and int(image_order_list[i]) or i)
                    
                    # Create ProductImage record
                    product_image = ProductImage(
                        product_id=product.id,
                        image_url=image_url,
                        alt_text=f"Gambar {product.name}",
                        is_primary=is_primary,
                        sort_order=sort_order
                    )
                    
                    db.session.add(product_image)
            
            # Set first new image as primary if no primary image set
            if not any(img.is_primary for img in product.images):
                if product.images:
                    product.images[0].is_primary = True
        
        # Update main image_url for backward compatibility
        primary_image = next((img for img in product.images if img.is_primary), None)
        if primary_image:
            product.image_url = primary_image.image_url
        
        db.session.commit()
        flash('Produk berhasil diperbarui!', 'success')
        return redirect(url_for('admin_products'))
    
    categories = Category.query.all()
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/products/delete/<int:product_id>', methods=['POST'])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    
    # Delete image file if exists
    if product.image_url:
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], product.image_url.replace('uploads/', '')))
        except:
            pass
    
    db.session.delete(product)
    db.session.commit()
    flash('Produk berhasil dihapus!', 'success')
    return redirect(url_for('admin_products'))

@app.route('/admin/categories')
@login_required
def admin_categories():
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        flash('Kategori berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/add_category.html')

@app.route('/admin/categories/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        db.session.commit()
        flash('Kategori berhasil diperbarui!', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/edit_category.html', category=category)

@app.route('/admin/categories/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category(category_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('admin_categories'))
    
    category = Category.query.get_or_404(category_id)
    
    # Check if category has products
    if category.products:
        flash('Tidak dapat menghapus kategori yang memiliki produk!', 'error')
        return redirect(url_for('admin_categories'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Kategori berhasil dihapus!', 'success')
    return redirect(url_for('admin_categories'))

# User Profile Routes
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'POST':
        current_user.username = request.form.get('username')
        current_user.email = request.form.get('email')
        
        # Check if new password is provided
        new_password = request.form.get('new_password')
        if new_password:
            current_user.password_hash = generate_password_hash(new_password)
        
        db.session.commit()
        flash('Profil berhasil diperbarui!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('edit_profile.html', user=current_user)

# Shopping Cart Routes
@app.route('/cart')
@login_required
def cart():
    # Get cart from session
    cart_items = session.get('cart', {})
    products = []
    total = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(product_id)
        if product:
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': float(product.price) * quantity
            })
            total += float(product.price) * quantity
    
    return render_template('cart.html', cart_items=products, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Handle both form data and JSON data
    if request.is_json:
        data = request.get_json()
        quantity = int(data.get('quantity', 1))
    else:
        quantity = int(request.form.get('quantity', 1))
    
    # Check stock availability
    if product.stock < quantity:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
            return jsonify({
                'success': False,
                'message': f'Stok tidak mencukupi. Tersedia: {product.stock} unit'
            }), 400
        else:
            flash(f'Stok tidak mencukupi. Tersedia: {product.stock} unit', 'error')
            return redirect(url_for('product_detail', product_id=product_id))
    
    # Get current cart from session
    cart = session.get('cart', {})
    
    # Add or update quantity
    if str(product_id) in cart:
        cart[str(product_id)] += quantity
    else:
        cart[str(product_id)] = quantity
    
    # Update session
    session['cart'] = cart
    
    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
        return jsonify({
            'success': True,
            'message': f'{product.name} berhasil ditambahkan ke keranjang!',
            'cart_count': len(cart)
        })
    else:
        flash(f'{product.name} berhasil ditambahkan ke keranjang!', 'success')
        return redirect(url_for('product_detail', product_id=product_id))

@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    
    if str(product_id) in cart:
        del cart[str(product_id)]
        session['cart'] = cart
        flash('Produk berhasil dihapus dari keranjang!', 'success')
    
    return redirect(url_for('cart'))

@app.route('/update_cart/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    quantity = int(request.form.get('quantity', 1))
    
    if quantity <= 0:
        return redirect(url_for('remove_from_cart', product_id=product_id))
    
    cart = session.get('cart', {})
    cart[str(product_id)] = quantity
    session['cart'] = cart
    
    flash('Keranjang berhasil diperbarui!', 'success')
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    cart_items = session.get('cart', {})
    
    if not cart_items:
        flash('Keranjang belanja kosong!', 'error')
        return redirect(url_for('cart'))
    
    if request.method == 'POST':
        # Get shipping information
        recipient_name = request.form.get('recipient_name')
        recipient_phone = request.form.get('recipient_phone')
        shipping_address = request.form.get('shipping_address')
        shipping_city = request.form.get('shipping_city')
        shipping_postal_code = request.form.get('shipping_postal_code')
        shipping_province = request.form.get('shipping_province')
        courier = request.form.get('courier')
        notes = request.form.get('notes', '')
        
        # Validate required fields
        if not all([recipient_name, recipient_phone, shipping_address, shipping_city, shipping_postal_code, shipping_province, courier]):
            flash('Semua field pengiriman harus diisi!', 'error')
            return redirect(url_for('checkout'))
        
        # Get and validate payment method
        payment_method = request.form.get('payment_method')
        if not payment_method:
            flash('Metode pembayaran harus dipilih!', 'error')
            return redirect(url_for('checkout'))
        
        # Calculate shipping cost based on courier and location
        shipping_cost = calculate_shipping_cost(courier, shipping_province)
        
        # Create order
        total_amount = 0
        order_items = []
        
        for product_id, quantity in cart_items.items():
            product = Product.query.get(product_id)
            if product and product.stock >= quantity:
                total_amount += float(product.price) * quantity
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'price': float(product.price)
                })
        
        if not order_items:
            flash('Tidak ada produk yang tersedia!', 'error')
            return redirect(url_for('cart'))
        
        # Add shipping cost to total
        total_amount += shipping_cost
        
        # Create order with shipping information
        order = Order(
            user_id=current_user.id,
            order_number=generate_order_number(),
            total_amount=total_amount,
            status='pending',
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_postal_code=shipping_postal_code,
            shipping_province=shipping_province,
            courier=courier,
            shipping_cost=shipping_cost,
            tracking_number=generate_tracking_number(courier),
            notes=notes,
            payment_method=payment_method
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order items
        for item in order_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
            
            # Update stock
            item['product'].stock -= item['quantity']
        
        # Clear cart
        session.pop('cart', None)
        
        db.session.commit()
        flash('Pesanan berhasil dibuat!', 'success')
        return redirect(url_for('order_detail', order_id=order.id))
    
    # Calculate total for display
    products = []
    subtotal = 0
    
    for product_id, quantity in cart_items.items():
        product = Product.query.get(product_id)
        if product:
            products.append({
                'product': product,
                'quantity': quantity,
                'subtotal': float(product.price) * quantity
            })
            subtotal += float(product.price) * quantity
    
    # Available couriers
    couriers = [
        {'code': 'jne', 'name': 'JNE Express', 'description': 'Pengiriman 2-3 hari kerja'},
        {'code': 'sicepat', 'name': 'SiCepat Express', 'description': 'Pengiriman 1-2 hari kerja'},
        {'code': 'jnt', 'name': 'J&T Express', 'description': 'Pengiriman 2-3 hari kerja'},
        {'code': 'pos', 'name': 'POS Indonesia', 'description': 'Pengiriman 3-5 hari kerja'},
        {'code': 'ninja', 'name': 'Ninja Express', 'description': 'Pengiriman 1-2 hari kerja'}
    ]
    
    # Available provinces
    provinces = [
        'DKI Jakarta', 'Jawa Barat', 'Jawa Tengah', 'Jawa Timur', 'Banten',
        'Sumatera Utara', 'Sumatera Barat', 'Sumatera Selatan', 'Lampung',
        'Kalimantan Barat', 'Kalimantan Tengah', 'Kalimantan Selatan', 'Kalimantan Timur',
        'Sulawesi Utara', 'Sulawesi Tengah', 'Sulawesi Selatan', 'Sulawesi Tenggara',
        'Bali', 'Nusa Tenggara Barat', 'Nusa Tenggara Timur', 'Maluku', 'Papua'
    ]
    
    # Available payment methods
    payment_methods = [
        {'code': 'cod', 'name': 'Cash on Delivery (COD)', 'description': 'Bayar di tempat saat barang diterima'},
        {'code': 'transfer', 'name': 'Transfer Bank', 'description': 'Transfer ke rekening bank kami'},
        {'code': 'ewallet', 'name': 'E-Wallet', 'description': 'GoPay, OVO, DANA, LinkAja'},
        {'code': 'qris', 'name': 'QRIS', 'description': 'Scan QRIS untuk pembayaran'},
        {'code': 'credit_card', 'name': 'Kartu Kredit/Debit', 'description': 'Visa, Mastercard, JCB'}
    ]
    
    return render_template('checkout.html', 
                         cart_items=products, 
                         subtotal=subtotal,
                         couriers=couriers,
                         provinces=provinces,
                         payment_methods=payment_methods)

def calculate_shipping_cost(courier, province):
    """Calculate shipping cost based on courier and province"""
    base_costs = {
        'jne': 15000,
        'sicepat': 12000,
        'jnt': 13000,
        'pos': 10000,
        'ninja': 14000
    }
    
    # Add cost based on province (simplified)
    province_costs = {
        'DKI Jakarta': 0,
        'Jawa Barat': 5000,
        'Jawa Tengah': 8000,
        'Jawa Timur': 10000,
        'Banten': 3000,
        'Sumatera Utara': 15000,
        'Sumatera Barat': 12000,
        'Sumatera Selatan': 10000,
        'Lampung': 8000,
        'Kalimantan Barat': 20000,
        'Kalimantan Tengah': 18000,
        'Kalimantan Selatan': 16000,
        'Kalimantan Timur': 22000,
        'Sulawesi Utara': 25000,
        'Sulawesi Tengah': 22000,
        'Sulawesi Selatan': 20000,
        'Sulawesi Tenggara': 23000,
        'Bali': 12000,
        'Nusa Tenggara Barat': 15000,
        'Nusa Tenggara Timur': 18000,
        'Maluku': 30000,
        'Papua': 35000
    }
    
    base_cost = base_costs.get(courier, 15000)
    province_cost = province_costs.get(province, 15000)
    
    return base_cost + province_cost

@app.route('/orders')
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    return render_template('orders.html', orders=orders)

@app.route('/order/<int:order_id>')
@login_required
def order_detail(order_id):
    order = Order.query.get_or_404(order_id)
    
    # Check if user owns this order
    if order.user_id != current_user.id and not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('order_history'))
    
    return render_template('order_detail.html', order=order)

# Admin Order Management Routes
@app.route('/admin/orders')
@login_required
def admin_orders():
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/orders/<int:order_id>')
@login_required
def admin_order_detail(order_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    return render_template('admin/order_detail.html', order=order)

@app.route('/admin/orders/<int:order_id>/update', methods=['POST'])
@login_required
def update_order_status(order_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    
    new_status = request.form.get('status')
    tracking_number = request.form.get('tracking_number', '')
    
    if new_status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
        order.status = new_status
        if tracking_number:
            order.tracking_number = tracking_number
        
        db.session.commit()
        flash(f'Status pesanan berhasil diupdate menjadi {new_status}', 'success')
    else:
        flash('Status tidak valid!', 'error')
    
    return redirect(url_for('admin_order_detail', order_id=order_id))

@app.route('/admin/orders/<int:order_id>/print')
@login_required
def print_order(order_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    order = Order.query.get_or_404(order_id)
    return render_template('admin/print_order.html', order=order)

# Customer Management Routes
@app.route('/admin/customers')
@login_required
def admin_customers():
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    customers = User.query.filter_by(is_admin=False).order_by(User.created_at.desc()).all()
    return render_template('admin/customers.html', customers=customers)

@app.route('/admin/customers/<int:customer_id>')
@login_required
def admin_customer_detail(customer_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    customer = User.query.get_or_404(customer_id)
    orders = Order.query.filter_by(user_id=customer_id).order_by(Order.created_at.desc()).all()
    support_tickets = CustomerSupport.query.filter_by(user_id=customer_id).order_by(CustomerSupport.created_at.desc()).all()
    
    return render_template('admin/customer_detail.html', 
                         customer=customer, 
                         orders=orders, 
                         support_tickets=support_tickets)

@app.route('/admin/customers/<int:customer_id>/toggle_status', methods=['POST'])
@login_required
def toggle_customer_status(customer_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    customer = User.query.get_or_404(customer_id)
    customer.is_active = not customer.is_active
    db.session.commit()
    
    status = 'aktif' if customer.is_active else 'nonaktif'
    flash(f'Status customer {customer.username} berhasil diubah menjadi {status}', 'success')
    return redirect(url_for('admin_customer_detail', customer_id=customer_id))

# Customer Support Management Routes
@app.route('/admin/support')
@login_required
def admin_support():
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    # Get filter parameters
    status_filter = request.args.get('status', 'all')
    priority_filter = request.args.get('priority', 'all')
    category_filter = request.args.get('category', 'all')
    
    # Build query
    query = CustomerSupport.query
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    if priority_filter != 'all':
        query = query.filter_by(priority=priority_filter)
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)
    
    support_tickets = query.order_by(CustomerSupport.created_at.desc()).all()
    
    return render_template('admin/support.html', 
                         support_tickets=support_tickets,
                         status_filter=status_filter,
                         priority_filter=priority_filter,
                         category_filter=category_filter)

@app.route('/admin/support/<int:ticket_id>')
@login_required
def admin_support_detail(ticket_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    ticket = CustomerSupport.query.get_or_404(ticket_id)
    return render_template('admin/support_detail.html', ticket=ticket)

@app.route('/admin/support/<int:ticket_id>/update', methods=['POST'])
@login_required
def update_support_ticket(ticket_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    ticket = CustomerSupport.query.get_or_404(ticket_id)
    status = request.form.get('status')
    priority = request.form.get('priority')
    admin_notes = request.form.get('admin_notes')
    
    if status:
        ticket.status = status
        if status == 'resolved':
            ticket.resolved_at = datetime.utcnow()
            ticket.resolved_by = current_user.id
    
    if priority:
        ticket.priority = priority
    
    if admin_notes:
        ticket.admin_notes = admin_notes
    
    ticket.updated_at = datetime.utcnow()
    
    try:
        db.session.commit()
        flash('Tiket support berhasil diperbarui!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'error')
    
    return redirect(url_for('admin_support_detail', ticket_id=ticket_id))

# Customer Support Routes (for customers)
@app.route('/support', methods=['GET', 'POST'])
@login_required
def customer_support():
    if request.method == 'POST':
        subject = request.form.get('subject')
        message = request.form.get('message')
        category = request.form.get('category')
        priority = request.form.get('priority')
        
        if not all([subject, message, category]):
            flash('Semua field harus diisi!', 'error')
            return redirect(url_for('customer_support'))
        
        support_ticket = CustomerSupport(
            user_id=current_user.id,
            subject=subject,
            message=message,
            category=category,
            priority=priority
        )
        
        db.session.add(support_ticket)
        db.session.commit()
        
        flash('Tiket support berhasil dibuat! Tim kami akan segera menghubungi Anda.', 'success')
        return redirect(url_for('customer_support'))
    
    # Get user's support tickets
    support_tickets = CustomerSupport.query.filter_by(user_id=current_user.id).order_by(CustomerSupport.created_at.desc()).all()
    
    return render_template('support.html', support_tickets=support_tickets)

@app.route('/support/<int:ticket_id>')
@login_required
def support_ticket_detail(ticket_id):
    ticket = CustomerSupport.query.get_or_404(ticket_id)
    
    # Check if user owns this ticket
    if ticket.user_id != current_user.id and not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('customer_support'))
    
    return render_template('support_detail.html', ticket=ticket)

@app.route('/admin/products/<int:product_id>')
@login_required
def admin_product_detail(product_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    product = Product.query.get_or_404(product_id)
    return render_template('admin/product_detail.html', product=product)

@app.route('/order/create', methods=['POST'])
@login_required
def create_order():
    """Create order directly from dashboard (for customers)"""
    if current_user.is_admin:
        return jsonify({'success': False, 'message': 'Admin tidak dapat menggunakan endpoint ini'}), 403
    
    try:
        # Get form data
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
        recipient_name = request.form.get('recipient_name')
        recipient_phone = request.form.get('recipient_phone')
        shipping_address = request.form.get('shipping_address')
        shipping_city = request.form.get('shipping_city')
        shipping_postal_code = request.form.get('shipping_postal_code')
        shipping_province = request.form.get('shipping_province')
        courier = request.form.get('courier')
        notes = request.form.get('notes', '')
        
        # Validate required fields
        if not all([product_id, quantity, recipient_name, recipient_phone, shipping_address, 
                   shipping_city, shipping_postal_code, shipping_province, courier]):
            return jsonify({'success': False, 'message': 'Semua field wajib diisi'}), 400
        
        # Get and validate payment method
        payment_method = request.form.get('payment_method')
        if not payment_method:
            return jsonify({'success': False, 'message': 'Metode pembayaran harus dipilih'}), 400
        
        # Get product
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Produk tidak ditemukan'}), 404
        
        # Check stock
        if product.stock < quantity:
            return jsonify({'success': False, 'message': f'Stok tidak mencukupi. Tersedia: {product.stock} unit'}), 400
        
        # Calculate costs
        subtotal = float(product.price) * quantity
        shipping_cost = calculate_shipping_cost(courier, shipping_province)
        total_amount = subtotal + shipping_cost
        
        # Create order
        order = Order(
            user_id=current_user.id,
            order_number=generate_order_number(),
            total_amount=total_amount,
            status='pending',
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_postal_code=shipping_postal_code,
            shipping_province=shipping_province,
            courier=courier,
            shipping_cost=shipping_cost,
            tracking_number=generate_tracking_number(courier),
            notes=notes,
            payment_method=payment_method
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity,
            price=float(product.price)
        )
        db.session.add(order_item)
        
        # Update stock
        product.stock -= quantity
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pesanan berhasil dibuat',
            'order_id': order.id,
            'order_number': order.order_number
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}), 500

@app.route('/admin/order/create', methods=['POST'])
@login_required
def admin_create_order():
    """Create order directly from dashboard (for admins)"""
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Akses ditolak'}), 403
    
    try:
        # Get form data
        customer_id = int(request.form.get('customer_id'))
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity'))
        recipient_name = request.form.get('recipient_name')
        recipient_phone = request.form.get('recipient_phone')
        shipping_address = request.form.get('shipping_address')
        shipping_city = request.form.get('shipping_city')
        shipping_postal_code = request.form.get('shipping_postal_code')
        shipping_province = request.form.get('shipping_province')
        courier = request.form.get('courier')
        notes = request.form.get('notes', '')
        
        # Validate required fields
        if not all([customer_id, product_id, quantity, recipient_name, recipient_phone, shipping_address, 
                   shipping_city, shipping_postal_code, shipping_province, courier]):
            return jsonify({'success': False, 'message': 'Semua field wajib diisi'}), 400
        
        # Get and validate payment method
        payment_method = request.form.get('payment_method')
        if not payment_method:
            return jsonify({'success': False, 'message': 'Metode pembayaran harus dipilih'}), 400
        
        # Get customer
        customer = User.query.get(customer_id)
        if not customer or customer.is_admin:
            return jsonify({'success': False, 'message': 'Customer tidak valid'}), 400
        
        # Get product
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'success': False, 'message': 'Produk tidak ditemukan'}), 404
        
        # Check stock
        if product.stock < quantity:
            return jsonify({'success': False, 'message': f'Stok tidak mencukupi. Tersedia: {product.stock} unit'}), 400
        
        # Calculate costs
        subtotal = float(product.price) * quantity
        shipping_cost = calculate_shipping_cost(courier, shipping_province)
        total_amount = subtotal + shipping_cost
        
        # Create order
        order = Order(
            user_id=customer_id,
            order_number=generate_order_number(),
            total_amount=total_amount,
            status='pending',
            recipient_name=recipient_name,
            recipient_phone=recipient_phone,
            shipping_address=shipping_address,
            shipping_city=shipping_city,
            shipping_postal_code=shipping_postal_code,
            shipping_province=shipping_province,
            courier=courier,
            shipping_cost=shipping_cost,
            tracking_number=generate_tracking_number(courier),
            notes=notes,
            payment_method=payment_method
        )
        db.session.add(order)
        db.session.flush()  # Get order ID
        
        # Create order item
        order_item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity,
            price=float(product.price)
        )
        db.session.add(order_item)
        
        # Update stock
        product.stock -= quantity
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Pesanan berhasil dibuat',
            'order_id': order.id,
            'order_number': order.order_number
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}), 500

# Bank Account Management Routes
@app.route('/admin/bank-accounts')
@login_required
def admin_bank_accounts():
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    try:
        bank_accounts = BankAccount.query.order_by(BankAccount.created_at.desc()).all()
        return render_template('admin/bank_accounts.html', bank_accounts=bank_accounts)
    except Exception as e:
        flash(f'Error saat memuat data rekening bank: {str(e)}', 'error')
        return render_template('admin/bank_accounts.html', bank_accounts=[])

@app.route('/admin/bank-accounts/add', methods=['GET', 'POST'])
@login_required
def add_bank_account():
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        bank_name = request.form.get('bank_name')
        account_number = request.form.get('account_number')
        account_holder = request.form.get('account_holder')
        account_type = request.form.get('account_type')
        notes = request.form.get('notes')
        
        if not all([bank_name, account_number, account_holder]):
            flash('Semua field wajib diisi!', 'error')
            return render_template('admin/add_bank_account.html')
        
        bank_account = BankAccount(
            bank_name=bank_name,
            account_number=account_number,
            account_holder=account_holder,
            account_type=account_type,
            notes=notes
        )
        
        try:
            db.session.add(bank_account)
            db.session.commit()
            flash('Rekening bank berhasil ditambahkan!', 'success')
            return redirect(url_for('admin_bank_accounts'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'error')
    
    return render_template('admin/add_bank_account.html')

@app.route('/admin/bank-accounts/edit/<int:account_id>', methods=['GET', 'POST'])
@login_required
def edit_bank_account(account_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    bank_account = BankAccount.query.get_or_404(account_id)
    
    if request.method == 'POST':
        bank_name = request.form.get('bank_name')
        account_number = request.form.get('account_number')
        account_holder = request.form.get('account_holder')
        account_type = request.form.get('account_type')
        notes = request.form.get('notes')
        is_active = request.form.get('is_active') == 'on'
        
        if not all([bank_name, account_number, account_holder]):
            flash('Semua field wajib diisi!', 'error')
            return render_template('admin/edit_bank_account.html', bank_account=bank_account)
        
        bank_account.bank_name = bank_name
        bank_account.account_number = account_number
        bank_account.account_holder = account_holder
        bank_account.account_type = account_type
        bank_account.notes = notes
        bank_account.is_active = is_active
        bank_account.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash('Rekening bank berhasil diperbarui!', 'success')
            return redirect(url_for('admin_bank_accounts'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {e}', 'error')
    
    return render_template('admin/edit_bank_account.html', bank_account=bank_account)

@app.route('/admin/bank-accounts/delete/<int:account_id>', methods=['POST'])
@login_required
def delete_bank_account(account_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    bank_account = BankAccount.query.get_or_404(account_id)
    
    # Check if account is being used in payments
    payments_count = Payment.query.filter_by(bank_account_id=account_id).count()
    if payments_count > 0:
        flash(f'Tidak dapat menghapus rekening yang sudah digunakan dalam {payments_count} pembayaran!', 'error')
        return redirect(url_for('admin_bank_accounts'))
    
    try:
        db.session.delete(bank_account)
        db.session.commit()
        flash('Rekening bank berhasil dihapus!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'error')
    
    return redirect(url_for('admin_bank_accounts'))

@app.route('/admin/bank-accounts/<int:account_id>')
@login_required
def admin_bank_account_detail(account_id):
    if not current_user.is_admin:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('index'))
    
    try:
        bank_account = BankAccount.query.get_or_404(account_id)
        payments = Payment.query.filter_by(bank_account_id=account_id).order_by(Payment.created_at.desc()).all()
        
        return render_template('admin/bank_account_detail.html', bank_account=bank_account, payments=payments)
    except Exception as e:
        flash(f'Error saat memuat detail rekening bank: {str(e)}', 'error')
        return redirect(url_for('admin_bank_accounts'))

@app.route('/admin/products/images/<int:image_id>/set-primary', methods=['POST'])
@login_required
def set_primary_image(image_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Akses ditolak!'}), 403
    
    try:
        # Get the image
        image = ProductImage.query.get_or_404(image_id)
        
        # Remove primary flag from all images of this product
        ProductImage.query.filter_by(product_id=image.product_id).update({'is_primary': False})
        
        # Set this image as primary
        image.is_primary = True
        
        # Update product's main image_url for backward compatibility
        image.product.image_url = image.image_url
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Gambar utama berhasil diubah'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

@app.route('/admin/products/images/<int:image_id>/delete', methods=['POST'])
@login_required
def delete_product_image(image_id):
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Akses ditolak!'}), 403
    
    try:
        # Get the image
        image = ProductImage.query.get_or_404(image_id)
        product = image.product
        
        # Delete image file
        try:
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], image.image_url.replace('uploads/', '')))
        except:
            pass  # File might not exist
        
        # Delete from database
        db.session.delete(image)
        
        # If this was the primary image, set another image as primary
        if image.is_primary and product.images:
            # Get remaining images
            remaining_images = [img for img in product.images if img.id != image_id]
            if remaining_images:
                remaining_images[0].is_primary = True
                product.image_url = remaining_images[0].image_url
            else:
                product.image_url = None
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Gambar berhasil dihapus'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

@app.route('/admin/products/images/reorder', methods=['POST'])
@login_required
def reorder_product_images():
    if not current_user.is_admin:
        return jsonify({'success': False, 'message': 'Akses ditolak!'}), 403
    
    try:
        data = request.get_json()
        image_ids = data.get('image_ids', [])
        
        # Update sort order for each image
        for index, image_id in enumerate(image_ids):
            image = ProductImage.query.get(image_id)
            if image:
                image.sort_order = index
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Urutan gambar berhasil diperbarui'
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        }), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@belanjakita.id',
                password_hash=generate_password_hash('admin123'),
                is_admin=True
            )
            db.session.add(admin)
            
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
            
            db.session.commit()
    
    app.run(debug=True) 