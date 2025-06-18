# Belanja Kita.id

Website e-commerce lengkap yang dibangun dengan Python Flask untuk backend dan HTML/CSS/JavaScript untuk frontend.

## 🚀 Fitur Utama

### Untuk Customer
- ✅ **Sistem Autentikasi** - Login/Register dengan validasi
- ✅ **Katalog Produk** - Browse produk dengan filter dan search
- ✅ **Detail Produk** - Informasi lengkap produk dengan galeri gambar
- ✅ **Shopping Cart** - Keranjang belanja dengan localStorage
- ✅ **Checkout & Pembayaran** - Multiple payment methods (COD, Transfer, E-Wallet, QRIS, Kartu Kredit)
- ✅ **Riwayat Pesanan** - Track status pesanan dan tracking number
- ✅ **Customer Support** - Sistem tiket support dan complaint
- ✅ **Responsive Design** - Tampilan optimal di semua device
- ✅ **Wishlist** - Simpan produk favorit
- ✅ **Rating & Review** - Sistem ulasan produk

### Untuk Admin
- ✅ **Dashboard Admin** - Statistik dan grafik penjualan
- ✅ **Manajemen Produk** - CRUD produk dengan upload gambar
- ✅ **Manajemen Kategori** - Kelola kategori produk
- ✅ **Manajemen Order** - Lihat dan update status pesanan dengan tracking number
- ✅ **Manajemen Customer** - Kelola data customer dan status aktif/nonaktif
- ✅ **Customer Support** - Kelola tiket support dan complaint
- ✅ **Print Invoice** - Generate dan print invoice pesanan
- ✅ **Export Data** - Export data ke Excel/CSV

## 🛠️ Teknologi yang Digunakan

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **SQLAlchemy** - ORM database
- **Flask-Login** - Autentikasi user
- **Flask-WTF** - Form handling
- **Werkzeug** - File upload dan security
- **SQLite** - Database (bisa diganti MySQL/PostgreSQL)

### Frontend
- **HTML5** - Struktur halaman
- **CSS3** - Styling dan responsive design
- **JavaScript (ES6+)** - Interaksi dinamis
- **Bootstrap 5** - UI framework
- **Font Awesome** - Icons
- **Chart.js** - Grafik dan visualisasi data

## 📁 Struktur Proyek

```
belanja_kita/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # Dokumentasi proyek
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── register.html     # Register page
│   ├── product_detail.html # Product detail page
│   └── admin/            # Admin templates
│       ├── dashboard.html # Admin dashboard
│       ├── products.html  # Product management
│       └── add_product.html # Add product form
├── static/               # Static files
│   ├── css/
│   │   └── style.css     # Custom CSS
│   ├── js/
│   │   └── main.js       # Main JavaScript
│   └── uploads/          # Uploaded images
└── ecommerce.db          # SQLite database
```

## 🚀 Cara Menjalankan

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan Aplikasi
```bash
python app.py
```

### 3. Akses Website
- **Customer**: http://localhost:5000
- **Admin**: http://localhost:5000/admin
  - Username: `admin`
  - Password: `admin123`

## 📊 Database Schema

### Tables
- **users** - Data customer dan admin dengan profile lengkap
- **categories** - Kategori produk
- **products** - Data produk dengan detail lengkap (SKU, brand, warranty, dll)
- **orders** - Data pesanan dengan shipping info dan payment method
- **order_items** - Item dalam pesanan
- **customer_support** - Tiket support dan complaint

### Default Data
- Admin user: `admin/admin123`
- Kategori: Elektronik, Pakaian, Makanan

## 🎨 Fitur UI/UX

### Design System
- **Color Scheme**: Blue primary (#007bff)
- **Typography**: Segoe UI font family
- **Components**: Bootstrap 5 components
- **Animations**: CSS transitions dan keyframes
- **Responsive**: Mobile-first approach

### Interactive Elements
- Hover effects pada cards dan buttons
- Smooth scrolling
- Loading spinners
- Toast notifications
- Modal dialogs
- Form validation

## 🔧 Konfigurasi

### Environment Variables
```python
SECRET_KEY = 'your-secret-key-here'
DATABASE_URI = 'sqlite:///ecommerce.db'
UPLOAD_FOLDER = 'static/uploads'
```

### File Upload
- **Max Size**: 2MB
- **Allowed Types**: JPG, PNG, GIF
- **Storage**: Local filesystem

## 📱 Responsive Design

### Breakpoints
- **Mobile**: < 576px
- **Tablet**: 576px - 768px
- **Desktop**: > 768px

### Features
- Mobile-friendly navigation
- Touch-friendly buttons
- Optimized images
- Flexible grid system

## 🔒 Security Features

- Password hashing dengan Werkzeug
- CSRF protection
- File upload validation
- SQL injection prevention
- XSS protection
- Session management

## 🚀 Deployment

### Production Setup
1. Set environment variables
2. Use production database (MySQL/PostgreSQL)
3. Configure web server (Nginx/Apache)
4. Set up SSL certificate
5. Configure file upload storage

### Recommended Hosting
- **Heroku** - Easy deployment
- **DigitalOcean** - VPS hosting
- **AWS** - Scalable cloud
- **Vercel** - Static hosting

## 📈 Monitoring & Analytics

### Built-in Analytics
- Sales charts
- Product statistics
- User analytics
- Order tracking

### External Integration
- Google Analytics
- Facebook Pixel
- Payment gateways
- Email services

## 🔄 Future Enhancements

### Planned Features
- [ ] Payment gateway integration
- [ ] Email notifications
- [ ] Advanced search filters
- [ ] Product variants
- [ ] Inventory management
- [ ] Multi-language support
- [ ] API endpoints
- [ ] Mobile app

### Performance Optimizations
- [ ] Image optimization
- [ ] Caching system
- [ ] CDN integration
- [ ] Database indexing
- [ ] Lazy loading

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Support

- **Email**: support@ecommerce.com
- **Documentation**: [Wiki](https://github.com/username/ecommerce/wiki)
- **Issues**: [GitHub Issues](https://github.com/username/ecommerce/issues)

## 🙏 Acknowledgments

- Bootstrap team for UI framework
- Flask community for web framework
- Font Awesome for icons
- Chart.js for data visualization

---

**Made with ❤️ by [Your Name]** 