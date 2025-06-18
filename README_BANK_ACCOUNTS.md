# Sistem Manajemen Rekening Bank - Belanja Kita.id

## 📋 Overview

Sistem manajemen rekening bank memungkinkan admin untuk mengelola multiple rekening bank untuk menerima pembayaran transfer dari customer. Sistem ini terintegrasi dengan sistem pembayaran dan order management.

## 🗄️ Struktur Database

### Tabel `bank_account`
```sql
CREATE TABLE bank_account (
    id SERIAL PRIMARY KEY,
    bank_name VARCHAR(100) NOT NULL,           -- Nama bank (BCA, Mandiri, BNI, dll)
    account_number VARCHAR(50) NOT NULL,       -- Nomor rekening
    account_holder VARCHAR(100) NOT NULL,      -- Nama pemilik rekening
    account_type VARCHAR(50),                  -- Tipe rekening (Savings, Current, Business, Personal)
    is_active BOOLEAN DEFAULT TRUE,            -- Status aktif/nonaktif
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT                                 -- Catatan tambahan
);
```

### Tabel `payment`
```sql
CREATE TABLE payment (
    id SERIAL PRIMARY KEY,
    order_id INTEGER NOT NULL REFERENCES "order"(id),
    amount NUMERIC(10,2) NOT NULL,             -- Jumlah pembayaran
    payment_method VARCHAR(50) NOT NULL,       -- Metode pembayaran
    payment_status VARCHAR(50) DEFAULT 'pending', -- Status pembayaran
    payment_date TIMESTAMP,                    -- Tanggal pembayaran
    bank_account_id INTEGER REFERENCES bank_account(id), -- Rekening yang digunakan
    reference_number VARCHAR(100),             -- Nomor referensi bank
    transaction_id VARCHAR(100),               -- ID transaksi payment gateway
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    notes TEXT                                 -- Catatan admin
);
```

### Field Baru di Tabel `order`
```sql
ALTER TABLE "order" ADD COLUMN payment_status VARCHAR(50) DEFAULT 'pending';
ALTER TABLE "order" ADD COLUMN payment_date TIMESTAMP;
ALTER TABLE "order" ADD COLUMN payment_reference VARCHAR(100);
ALTER TABLE "order" ADD COLUMN bank_account_id INTEGER REFERENCES bank_account(id);
```

## 🔐 Keamanan & Akses

### Admin Only Access
- **Semua route bank account hanya bisa diakses oleh admin**
- Validasi `@login_required` dan `current_user.is_admin`
- Customer tidak bisa melihat atau mengakses halaman bank account

### Routes yang Dilindungi:
```python
@app.route('/admin/bank-accounts')                    # List rekening
@app.route('/admin/bank-accounts/add')               # Tambah rekening
@app.route('/admin/bank-accounts/edit/<id>')         # Edit rekening
@app.route('/admin/bank-accounts/delete/<id>')       # Hapus rekening
@app.route('/admin/bank-accounts/<id>')              # Detail rekening
```

## 🎯 Fitur Utama

### 1. **Manajemen Rekening Bank**
- ✅ Tambah rekening bank baru
- ✅ Edit informasi rekening
- ✅ Aktif/nonaktif rekening
- ✅ Hapus rekening (dengan validasi)
- ✅ Lihat detail rekening

### 2. **Tracking Pembayaran**
- ✅ Riwayat pembayaran per rekening
- ✅ Statistik pembayaran (total, berhasil, pending)
- ✅ Total uang yang diterima per rekening
- ✅ Link ke detail order

### 3. **Integrasi dengan Order**
- ✅ Pilih rekening saat konfirmasi transfer
- ✅ Update status pembayaran
- ✅ Referensi pembayaran
- ✅ Tanggal pembayaran

### 4. **Validasi & Keamanan**
- ✅ Validasi rekening tidak bisa dihapus jika sudah digunakan
- ✅ Validasi field wajib
- ✅ Sanitasi input
- ✅ Error handling

## 🚀 Cara Penggunaan

### Untuk Admin:

#### 1. **Akses Menu Bank Account**
```
Admin Panel → Rekening Bank
atau
Dashboard → Quick Actions → Rekening Bank
```

#### 2. **Tambah Rekening Baru**
1. Klik "Tambah Rekening"
2. Isi informasi:
   - Nama Bank (BCA, Mandiri, BNI, dll)
   - Nomor Rekening
   - Pemilik Rekening
   - Tipe Rekening (opsional)
   - Catatan (opsional)
3. Klik "Simpan Rekening"

#### 3. **Edit Rekening**
1. Klik tombol "Edit" di daftar rekening
2. Ubah informasi yang diperlukan
3. Centang/uncentang "Rekening Aktif"
4. Klik "Update Rekening"

#### 4. **Lihat Detail & Statistik**
1. Klik tombol "Detail" di daftar rekening
2. Lihat informasi lengkap rekening
3. Lihat statistik pembayaran
4. Lihat riwayat pembayaran

#### 5. **Hapus Rekening**
1. Klik tombol "Hapus" di daftar rekening
2. Konfirmasi penghapusan
3. **Note**: Rekening yang sudah digunakan tidak bisa dihapus

### Untuk Customer:
- Customer **TIDAK** bisa mengakses menu bank account
- Customer hanya bisa memilih metode pembayaran "Transfer Bank"
- Admin akan mengirimkan nomor rekening setelah order dikonfirmasi

## 📊 Statistik & Laporan

### Per Rekening:
- Total pembayaran
- Pembayaran berhasil
- Pembayaran pending
- Total uang diterima

### Per Periode:
- Grafik pembayaran per bulan
- Top rekening yang paling sering digunakan
- Analisis metode pembayaran

## 🔧 Konfigurasi

### Contoh Rekening Default:
```sql
INSERT INTO bank_account (bank_name, account_number, account_holder, account_type, notes) 
VALUES 
('BCA', '1234567890', 'Belanja Kita.id', 'Business', 'Rekening utama untuk pembayaran'),
('Mandiri', '0987654321', 'Belanja Kita.id', 'Business', 'Rekening alternatif'),
('BNI', '1122334455', 'Belanja Kita.id', 'Business', 'Rekening untuk transfer cepat');
```

### Status Pembayaran:
- `pending` - Menunggu pembayaran
- `paid` - Sudah dibayar
- `failed` - Pembayaran gagal
- `refunded` - Dikembalikan

## 🛠️ Troubleshooting

### Error: "Tidak dapat menghapus rekening yang sudah digunakan"
**Solusi**: Rekening yang sudah digunakan dalam pembayaran tidak bisa dihapus. Nonaktifkan saja rekening tersebut.

### Error: "Column bank_account_id does not exist"
**Solusi**: Jalankan script migrasi:
```bash
python migrate_payment_method.py
```

### Error: "Access denied"
**Solusi**: Pastikan user yang login memiliki role admin.

### Rekening tidak muncul di pilihan pembayaran
**Solusi**: Pastikan rekening berstatus "Aktif" (`is_active = true`).

### Error: "'None' has no attribute 'strftime'"
**Solusi**: Error ini terjadi karena field datetime bernilai NULL. Jalankan script perbaikan:
```bash
python fix_datetime_fields.py
```

**Penyebab**: Field `created_at` atau `updated_at` di database bernilai NULL
**Pencegahan**: 
- Field datetime sudah diset `NOT NULL` dengan default value
- Trigger auto-update sudah ditambahkan
- Template sudah ditambahkan validasi `if field else 'N/A'`

### Error: "UndefinedError: 'None' has no attribute 'strftime'"
**Solusi**: 
1. Jalankan script perbaikan data:
   ```bash
   python fix_datetime_fields.py
   ```
2. Pastikan template menggunakan validasi:
   ```jinja2
   {{ field.strftime('%d/%m/%Y %H:%M') if field else 'N/A' }}
   ```
3. Restart aplikasi Flask

### Database connection error
**Solusi**: 
1. Cek file `config.env` - pastikan kredensial database benar
2. Pastikan PostgreSQL server berjalan
3. Cek koneksi database dengan:
   ```bash
   python -c "from app import db; print('Database connected')"
   ```

## 📱 Template Files

### Admin Templates:
- `templates/admin/bank_accounts.html` - Daftar rekening
- `templates/admin/add_bank_account.html` - Tambah rekening
- `templates/admin/edit_bank_account.html` - Edit rekening
- `templates/admin/bank_account_detail.html` - Detail rekening

### Navigation Updates:
- `templates/base.html` - Menu admin dropdown
- `templates/admin/dashboard.html` - Quick actions

## 🔄 Workflow Pembayaran

### Transfer Bank:
1. Customer checkout dengan pilihan "Transfer Bank"
2. Admin terima notifikasi order baru
3. Admin pilih rekening bank yang akan digunakan
4. Admin kirim nomor rekening ke customer
5. Customer transfer ke rekening tersebut
6. Admin konfirmasi pembayaran
7. Status order berubah menjadi "paid"
8. Barang dikirim

### Tracking:
- Semua pembayaran tercatat di tabel `payment`
- Admin bisa lihat riwayat pembayaran per rekening
- Statistik pembayaran otomatis terupdate

## 📞 Support

Jika mengalami masalah dengan sistem rekening bank:
1. Cek log error di console
2. Pastikan database migration sudah dijalankan
3. Cek permission user admin
4. Hubungi developer untuk bantuan teknis

## 🔮 Fitur Future

### Rencana Pengembangan:
- [ ] Integrasi dengan payment gateway
- [ ] Notifikasi otomatis saat ada pembayaran
- [ ] Export laporan ke Excel/PDF
- [ ] Dashboard analitik pembayaran
- [ ] Multi-currency support
- [ ] API untuk integrasi dengan sistem lain 