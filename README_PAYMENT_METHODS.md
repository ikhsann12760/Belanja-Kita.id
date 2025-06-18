# Metode Pembayaran - Belanja Kita.id

## 📋 Daftar Metode Pembayaran yang Tersedia

### 1. **COD (Cash on Delivery)**
- **Deskripsi**: Bayar di tempat saat barang diterima
- **Proses**: Customer membayar langsung kepada kurir saat barang sampai
- **Keuntungan**: Tidak perlu transfer atau kartu kredit
- **Kekurangan**: Biaya tambahan untuk COD

### 2. **Transfer Bank**
- **Deskripsi**: Transfer ke rekening bank kami
- **Proses**: 
  1. Customer checkout dengan pilihan transfer bank
  2. Admin mengirimkan nomor rekening via email/SMS
  3. Customer transfer sesuai total pembayaran
  4. Admin konfirmasi pembayaran
  5. Barang dikirim
- **Keuntungan**: Aman dan terpercaya
- **Kekurangan**: Proses manual, memerlukan konfirmasi admin

### 3. **E-Wallet**
- **Deskripsi**: GoPay, OVO, DANA, LinkAja
- **Proses**: 
  1. Customer pilih e-wallet yang diinginkan
  2. Sistem redirect ke payment gateway e-wallet
  3. Customer scan QR atau input nomor
  4. Pembayaran diproses otomatis
  5. Barang dikirim setelah pembayaran berhasil
- **Keuntungan**: Cepat dan mudah
- **Kekurangan**: Memerlukan saldo e-wallet

### 4. **QRIS**
- **Deskripsi**: Scan QRIS untuk pembayaran
- **Proses**:
  1. Customer pilih QRIS
  2. Sistem generate QR code
  3. Customer scan dengan aplikasi bank/e-wallet
  4. Pembayaran diproses otomatis
  5. Barang dikirim setelah pembayaran berhasil
- **Keuntungan**: Universal, bisa digunakan berbagai aplikasi
- **Kekurangan**: Memerlukan aplikasi yang support QRIS

### 5. **Kartu Kredit/Debit**
- **Deskripsi**: Visa, Mastercard, JCB
- **Proses**:
  1. Customer pilih kartu kredit/debit
  2. Sistem redirect ke payment gateway
  3. Customer input data kartu
  4. Pembayaran diproses otomatis
  5. Barang dikirim setelah pembayaran berhasil
- **Keuntungan**: Aman dan terpercaya
- **Kekurangan**: Memerlukan kartu kredit/debit

## 🔧 Implementasi Teknis

### Database Schema
```sql
ALTER TABLE "order" ADD COLUMN payment_method VARCHAR(50) NOT NULL DEFAULT 'cod';
```

### Model Order
```python
class Order(db.Model):
    # ... existing fields ...
    payment_method = db.Column(db.String(50), nullable=False)  # Payment method
```

### Validasi
- **Backend**: Memastikan `payment_method` dipilih sebelum checkout
- **Frontend**: JavaScript validation untuk memastikan user memilih metode pembayaran

### Template Updates
- `checkout.html`: Menambahkan section metode pembayaran
- `order_detail.html`: Menampilkan metode pembayaran yang dipilih
- `admin/order_detail.html`: Admin dapat melihat metode pembayaran
- `admin/orders.html`: Kolom metode pembayaran di daftar pesanan
- `admin/print_order.html`: Metode pembayaran di invoice

## 🚀 Cara Penggunaan

### Untuk Customer:
1. Pilih produk dan tambahkan ke keranjang
2. Klik "Checkout"
3. Isi informasi pengiriman
4. **Pilih metode pembayaran** (wajib)
5. Klik "Bayar Sekarang"
6. Ikuti instruksi pembayaran sesuai metode yang dipilih

### Untuk Admin:
1. Buka "Kelola Pesanan" di admin dashboard
2. Lihat kolom "Pembayaran" untuk melihat metode yang dipilih customer
3. Klik "Detail" untuk melihat informasi lengkap
4. Proses pembayaran sesuai metode yang dipilih customer

## 📊 Status Pembayaran

### COD:
- Status: Pending → Processing → Shipped → Delivered
- Pembayaran: Saat barang diterima

### Transfer Bank:
- Status: Pending → Processing → Shipped → Delivered
- Pembayaran: Setelah admin konfirmasi transfer

### E-Wallet/QRIS/Kartu Kredit:
- Status: Pending → Processing → Shipped → Delivered
- Pembayaran: Otomatis setelah checkout berhasil

## 🔒 Keamanan

- Semua metode pembayaran menggunakan HTTPS
- Data kartu kredit tidak disimpan di database
- Validasi backend untuk mencegah manipulasi
- Logging untuk audit trail pembayaran

## 🛠️ Troubleshooting

### Error: "column order.payment_method does not exist"
**Solusi**: Jalankan script migrasi:
```bash
python migrate_payment_method.py
```

### Error: "Metode pembayaran harus dipilih"
**Solusi**: Pastikan customer memilih salah satu metode pembayaran sebelum checkout

### Error: Payment gateway tidak merespons
**Solusi**: 
1. Cek koneksi internet
2. Coba metode pembayaran lain
3. Hubungi admin untuk bantuan

## 📞 Support

Jika mengalami masalah dengan pembayaran:
1. Cek FAQ di halaman support
2. Buat tiket support baru
3. Hubungi admin via email/telepon
4. Cek status pesanan di halaman "Riwayat Pesanan" 