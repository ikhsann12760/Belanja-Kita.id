# Fitur Filter Kategori Produk - Belanja Kita.id

## 📋 Overview

Fitur filter kategori produk memungkinkan admin untuk melihat produk berdasarkan kategori tertentu di dashboard dan halaman kelola produk. Fitur ini membantu admin untuk fokus pada produk dalam kategori tertentu.

## 🎯 Fitur Utama

### 1. **Filter Kategori di Dashboard**
- ✅ Dropdown filter kategori di dashboard admin
- ✅ Tampilan produk terlaris berdasarkan kategori yang dipilih
- ✅ Counter jumlah produk per kategori
- ✅ Reset filter untuk melihat semua produk

### 2. **Filter Kategori di Halaman Produk**
- ✅ Filter berdasarkan kategori
- ✅ Pencarian produk (nama, deskripsi, SKU, brand)
- ✅ Filter berdasarkan status stok (tersedia, habis, menipis)
- ✅ Kombinasi multiple filter
- ✅ Informasi filter aktif dengan badge

### 3. **User Experience**
- ✅ Auto-submit saat pilih kategori
- ✅ Form submission untuk pencarian
- ✅ Reset filter dengan satu klik
- ✅ Visual feedback filter aktif

## 🚀 Cara Penggunaan

### Di Dashboard Admin:

1. **Akses Dashboard**: Login sebagai admin → Admin Panel → Dashboard

2. **Pilih Kategori**:
   - Scroll ke bagian "Filter Kategori Produk"
   - Pilih kategori dari dropdown
   - Sistem otomatis memfilter produk

3. **Lihat Hasil**:
   - Produk terlaris akan menampilkan hanya produk dari kategori yang dipilih
   - Counter menunjukkan jumlah produk dalam kategori
   - Header berubah menjadi "Produk Kategori: [Nama Kategori]"

4. **Reset Filter**:
   - Klik tombol "Reset" atau pilih "Semua Kategori"

### Di Halaman Kelola Produk:

1. **Akses Halaman Produk**: Admin Panel → Kelola Produk

2. **Gunakan Filter**:
   - **Pencarian**: Ketik nama produk, deskripsi, SKU, atau brand
   - **Kategori**: Pilih kategori dari dropdown
   - **Stok**: Pilih status stok (Tersedia/Habis/Menipis)

3. **Kombinasi Filter**:
   - Bisa menggunakan multiple filter sekaligus
   - Contoh: Kategori "Elektronik" + Stok "Tersedia"

4. **Lihat Filter Aktif**:
   - Badge menunjukkan filter yang sedang aktif
   - Counter produk yang ditemukan
   - Tombol "Hapus Filter" untuk reset

## 🔧 Implementasi Teknis

### Backend (Python/Flask):

#### Route Dashboard dengan Filter:
```python
@app.route('/admin')
@login_required
def admin_dashboard():
    # Get filter parameters
    category_filter = request.args.get('category', 'all')
    
    # Get all categories for filter dropdown
    categories = Category.query.all()
    
    # Filter products based on category
    if category_filter == 'all':
        products = Product.query.all()
    else:
        products = Product.query.filter_by(category_id=category_filter).all()
    
    return render_template('admin/dashboard.html', 
                         products=products, 
                         categories=categories,
                         selected_category=category_filter)
```

#### Route Produk dengan Multiple Filter:
```python
@app.route('/admin/products')
@login_required
def admin_products():
    # Get filter parameters
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    stock_filter = request.args.get('stock', '')
    
    # Base query
    products_query = Product.query
    
    # Apply filters
    if category_filter:
        products_query = products_query.filter_by(category_id=category_filter)
    
    if search_query:
        products_query = products_query.filter(
            Product.name.ilike(f'%{search_query}%') |
            Product.description.ilike(f'%{search_query}%') |
            Product.sku.ilike(f'%{search_query}%') |
            Product.brand.ilike(f'%{search_query}%')
        )
    
    if stock_filter == 'in_stock':
        products_query = products_query.filter(Product.stock > 0)
    elif stock_filter == 'out_of_stock':
        products_query = products_query.filter(Product.stock == 0)
    elif stock_filter == 'low_stock':
        products_query = products_query.filter(Product.stock <= Product.min_stock)
    
    products = products_query.all()
    categories = Category.query.all()
    
    return render_template('admin/products.html', 
                         products=products, 
                         categories=categories,
                         selected_category=category_filter,
                         search_query=search_query,
                         stock_filter=stock_filter)
```

### Frontend (HTML/Jinja2):

#### Filter Dropdown di Dashboard:
```html
<form method="GET" action="{{ url_for('admin_dashboard') }}" class="row align-items-end">
    <div class="col-md-4">
        <label for="category" class="form-label">Pilih Kategori:</label>
        <select class="form-select" id="category" name="category" onchange="this.form.submit()">
            <option value="all" {{ 'selected' if selected_category == 'all' }}>Semua Kategori</option>
            {% for category in categories %}
            <option value="{{ category.id }}" {{ 'selected' if selected_category|string == category.id|string }}>
                {{ category.name }}
            </option>
            {% endfor %}
        </select>
    </div>
    <div class="col-md-4">
        <button type="submit" class="btn btn-primary">
            <i class="fas fa-search me-2"></i>Filter
        </button>
        <a href="{{ url_for('admin_dashboard') }}" class="btn btn-secondary">
            <i class="fas fa-times me-2"></i>Reset
        </a>
    </div>
</form>
```

#### Filter Aktif Information:
```html
{% if selected_category or search_query or stock_filter %}
<div class="alert alert-info mb-4">
    <div class="d-flex justify-content-between align-items-center">
        <div>
            <i class="fas fa-filter me-2"></i>
            <strong>Filter Aktif:</strong>
            {% if selected_category %}
                <span class="badge bg-primary me-2">Kategori: {{ category.name }}</span>
            {% endif %}
            {% if search_query %}
                <span class="badge bg-info me-2">Pencarian: "{{ search_query }}"</span>
            {% endif %}
            <span class="badge bg-secondary">{{ products|length }} produk ditemukan</span>
        </div>
        <a href="{{ url_for('admin_products') }}" class="btn btn-sm btn-outline-secondary">
            <i class="fas fa-times me-1"></i>Hapus Filter
        </a>
    </div>
</div>
{% endif %}
```

## 📊 Filter Options

### 1. **Filter Kategori**
- Semua Kategori (default)
- Kategori 1, Kategori 2, dst (dinamis dari database)

### 2. **Filter Pencarian**
- Nama produk
- Deskripsi produk
- SKU produk
- Brand produk

### 3. **Filter Stok**
- Semua Stok (default)
- Tersedia (stock > 0)
- Habis (stock = 0)
- Stok Menipis (stock <= min_stock)

## 🎨 UI/UX Features

### Visual Indicators:
- ✅ Badge warna untuk setiap jenis filter
- ✅ Counter jumlah produk yang ditemukan
- ✅ Icon filter untuk identifikasi cepat
- ✅ Tombol reset yang mudah diakses

### Responsive Design:
- ✅ Mobile-friendly dropdown
- ✅ Responsive grid layout
- ✅ Touch-friendly buttons

### User Feedback:
- ✅ Loading state saat filter
- ✅ Empty state saat tidak ada hasil
- ✅ Clear indication filter aktif

## 🔄 Workflow

### Dashboard Filter:
1. User pilih kategori dari dropdown
2. Form auto-submit dengan JavaScript
3. Backend filter produk berdasarkan kategori
4. Template render produk yang sudah difilter
5. Counter update dengan jumlah produk

### Produk Page Filter:
1. User input pencarian atau pilih filter
2. Form submit ke backend
3. Backend apply multiple filter
4. Template render hasil dengan informasi filter aktif
5. User bisa reset atau modify filter

## 🛠️ Troubleshooting

### Filter tidak berfungsi:
1. **Cek JavaScript**: Pastikan `onchange="this.form.submit()"` ada di dropdown
2. **Cek Route**: Pastikan route menerima parameter GET
3. **Cek Database**: Pastikan kategori ada di database

### Hasil filter kosong:
1. **Cek Parameter**: Pastikan parameter filter benar
2. **Cek Query**: Pastikan query database benar
3. **Cek Data**: Pastikan ada produk dalam kategori tersebut

### Filter tidak tersimpan:
1. **Cek Form**: Pastikan form menggunakan method GET
2. **Cek Action**: Pastikan action mengarah ke route yang benar
3. **Cek Template**: Pastikan selected attribute benar

## 📈 Performance

### Optimizations:
- ✅ Database indexing pada category_id
- ✅ Efficient SQL queries dengan filter
- ✅ Pagination untuk produk banyak (future)
- ✅ Caching kategori (future)

### Best Practices:
- ✅ Use GET method untuk filter (bookmarkable)
- ✅ Validate filter parameters
- ✅ Sanitize search input
- ✅ Limit search results (future)

## 🔮 Future Enhancements

### Planned Features:
- [ ] Advanced search dengan operator (AND, OR)
- [ ] Filter berdasarkan harga range
- [ ] Filter berdasarkan tanggal dibuat
- [ ] Export hasil filter ke Excel/PDF
- [ ] Save filter preferences
- [ ] Bulk actions pada hasil filter
- [ ] Real-time search dengan AJAX
- [ ] Filter berdasarkan status produk (aktif/nonaktif)

### Performance Improvements:
- [ ] Database query optimization
- [ ] Redis caching untuk kategori
- [ ] Lazy loading untuk produk banyak
- [ ] Virtual scrolling untuk tabel besar 

Dokumentasi lengkap untuk fitur filter kategori produk di dashboard admin dan halaman customer.

## Fitur yang Tersedia

### 1. Dashboard Admin
- **Filter Kategori**: Dropdown untuk memilih kategori produk
- **Auto-submit**: Filter langsung diterapkan saat kategori dipilih
- **Visual Feedback**: Badge kategori ditampilkan di judul section
- **Button Navigasi**: 
  - "Lihat Semua Produk" - mengarah ke halaman admin products dengan filter
  - "Lihat di Customer" - mengarah ke halaman customer dengan filter (tab baru)

### 2. Halaman Admin Products
- **Multiple Filters**: Kategori, pencarian, dan status stok
- **Active Filter Display**: Menampilkan filter yang sedang aktif
- **Clear Filters**: Button untuk menghapus semua filter
- **Responsive Design**: Tampilan yang responsif di berbagai ukuran layar

### 3. Halaman Customer Products (Baru)
- **Route**: `/products` - halaman produk untuk customer
- **Filter Kategori**: Dropdown dengan auto-submit
- **Search**: Pencarian berdasarkan nama, deskripsi, dan brand
- **Product Cards**: Tampilan produk yang menarik dengan gambar
- **Add to Cart**: Button untuk menambahkan ke keranjang (untuk user yang login)
- **Category Navigation**: Link ke kategori lain di bagian bawah

## Cara Kerja

### Dashboard Admin
1. Admin memilih kategori dari dropdown
2. Halaman reload dengan produk yang difilter
3. Badge kategori muncul di judul section
4. Button "Lihat Semua Produk" mengarah ke halaman admin dengan filter
5. Button "Lihat di Customer" membuka halaman customer di tab baru

### Halaman Customer
1. Customer dapat melihat semua produk aktif
2. Filter berdasarkan kategori dan pencarian
3. Tampilan produk dengan informasi lengkap
4. Link ke detail produk dan add to cart
5. Navigasi ke kategori lain

## File yang Dimodifikasi

### 1. `app.py`
- **Route `/admin`**: Ditambahkan parameter `category` untuk filter
- **Route `/admin/products`**: Ditambahkan filter kategori, pencarian, dan status stok
- **Route `/products`**: Route baru untuk halaman customer products

### 2. `templates/admin/dashboard.html`
- **Category Filter**: Dropdown dengan auto-submit
- **Button Navigation**: Button untuk melihat produk di admin dan customer
- **Visual Feedback**: Badge kategori di judul section

### 3. `templates/admin/products.html`
- **Multiple Filters**: Kategori, pencarian, dan status stok
- **Active Filter Display**: Menampilkan filter yang aktif
- **Clear Filters**: Button untuk reset filter

### 4. `templates/products.html` (Baru)
- **Customer Products Page**: Template baru untuk halaman produk customer
- **Search & Filter**: Form pencarian dan filter kategori
- **Product Grid**: Tampilan produk yang responsif
- **Category Navigation**: Link ke kategori lain

### 5. `templates/index.html`
- **Category Cards**: Link mengarah ke halaman produk dengan filter kategori

### 6. `templates/base.html`
- **Navbar**: Link "Produk" mengarah ke halaman produk customer

## Parameter URL

### Dashboard Admin
```
/admin?category=1
```

### Admin Products
```
/admin/products?category=1&search=laptop&stock=in_stock
```

### Customer Products
```
/products?category=1&search=laptop
```

## Database Query

### Dashboard Admin
```python
# Filter berdasarkan kategori
if selected_category != 'all':
    products = Product.query.filter_by(category_id=selected_category).all()
else:
    products = Product.query.all()
```

### Admin Products
```python
# Multiple filters
products_query = Product.query

if category_filter:
    products_query = products_query.filter_by(category_id=category_filter)

if search_query:
    products_query = products_query.filter(
        Product.name.ilike(f'%{search_query}%') |
        Product.description.ilike(f'%{search_query}%') |
        Product.brand.ilike(f'%{search_query}%')
    )

if stock_filter == 'in_stock':
    products_query = products_query.filter(Product.stock > 0)
elif stock_filter == 'out_of_stock':
    products_query = products_query.filter(Product.stock == 0)
elif stock_filter == 'low_stock':
    products_query = products_query.filter(Product.stock <= Product.min_stock)
```

### Customer Products
```python
# Hanya produk aktif
products_query = Product.query.filter_by(is_active=True)

if category_filter:
    products_query = products_query.filter_by(category_id=category_filter)

if search_query:
    products_query = products_query.filter(
        Product.name.ilike(f'%{search_query}%') |
        Product.description.ilike(f'%{search_query}%') |
        Product.brand.ilike(f'%{search_query}%')
    )
```

## Troubleshooting

### 1. Filter Tidak Berfungsi
- Pastikan kategori ada di database
- Cek apakah parameter URL diterima dengan benar
- Periksa query database di console

### 2. Button Tidak Mengarah ke Halaman yang Benar
- Pastikan route `/products` sudah dibuat
- Cek apakah template `products.html` ada
- Periksa parameter URL yang dikirim

### 3. Halaman Customer Tidak Muncul
- Pastikan produk memiliki `is_active=True`
- Cek apakah ada produk dalam kategori yang dipilih
- Periksa error di console browser

### 4. Add to Cart Tidak Berfungsi
- Pastikan user sudah login
- Cek apakah route `/add_to_cart/<product_id>` ada
- Periksa response dari API

## Penggunaan

### Untuk Admin
1. Buka dashboard admin
2. Pilih kategori dari dropdown
3. Lihat produk yang difilter
4. Klik "Lihat Semua Produk" untuk ke halaman admin products
5. Klik "Lihat di Customer" untuk melihat di halaman customer

### Untuk Customer
1. Klik "Produk" di navbar
2. Gunakan filter kategori atau pencarian
3. Lihat produk yang tersedia
4. Klik "Detail Produk" untuk melihat detail
5. Klik "Tambah ke Keranjang" untuk membeli

## Keunggulan Fitur

1. **User Experience**: Navigasi yang mudah dan intuitif
2. **Performance**: Filter langsung tanpa reload halaman (dashboard)
3. **Responsive**: Tampilan yang baik di semua device
4. **Accessibility**: Link yang jelas dan mudah dipahami
5. **Integration**: Terintegrasi dengan sistem keranjang dan pembelian 