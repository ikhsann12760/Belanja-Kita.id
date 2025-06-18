# Setup PostgreSQL untuk Belanja Kita.id

Panduan lengkap untuk mengubah aplikasi e-commerce dari SQLite ke PostgreSQL.

## 📋 Prerequisites

1. **Python 3.7+** sudah terinstall
2. **PostgreSQL** sudah terinstall dan berjalan
3. **pip** untuk menginstall dependencies

## 🚀 Langkah-langkah Setup

### 1. Install PostgreSQL

#### Option A: Install PostgreSQL di Windows
1. Download PostgreSQL dari [https://www.postgresql.org/download/windows/](https://www.postgresql.org/download/windows/)
2. Install dengan default settings
3. Catat password untuk user `postgres`
4. PostgreSQL akan berjalan di port 5432

#### Option B: Menggunakan Docker (Recommended)
```bash
# Pull dan run PostgreSQL container
docker run --name postgres-belanjakita -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres

# Untuk menjalankan ulang container yang sudah ada
docker start postgres-belanjakita
```

### 2. Install Python Dependencies

```bash
# Install semua dependencies termasuk psycopg2
pip install -r requirements.txt
```

### 3. Konfigurasi Database

1. **Edit file `config.env`** sesuai dengan konfigurasi PostgreSQL Anda:

```env
# Flask Configuration
SECRET_KEY=your-super-secret-key-change-this-in-production

# PostgreSQL Database Configuration
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=belanjakita
```

2. **Jalankan script setup database**:

```bash
python setup_database.py
```

Script ini akan:
- Membuat database `belanjakita` jika belum ada
- Test koneksi ke database
- Memberikan feedback jika ada masalah

### 4. Jalankan Aplikasi

```bash
python app.py
```

Aplikasi akan:
- Membuat semua tabel secara otomatis
- Membuat user admin default (username: `admin`, password: `admin123`)
- Membuat kategori default

## 🔧 Troubleshooting

### Error: "connection to server at localhost failed"
- Pastikan PostgreSQL service berjalan
- Cek apakah port 5432 tidak diblokir firewall
- Untuk Docker: pastikan container berjalan dengan `docker ps`

### Error: "authentication failed"
- Periksa username dan password di `config.env`
- Untuk PostgreSQL default: username `postgres`, password sesuai yang di-set saat install

### Error: "database does not exist"
- Jalankan `python setup_database.py` untuk membuat database
- Atau buat manual dengan psql:
```sql
CREATE DATABASE belanjakita;
```

### Error: "psycopg2 module not found"
- Install psycopg2: `pip install psycopg2-binary`
- Atau install dari requirements: `pip install -r requirements.txt`

## 📊 Perbedaan dengan SQLite

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| **Type** | File-based | Client-Server |
| **Concurrency** | Single writer | Multi-writer |
| **Performance** | Good for small apps | Excellent for production |
| **Data Types** | Basic | Advanced (JSON, Arrays, etc.) |
| **Backup** | File copy | pg_dump |
| **Scalability** | Limited | High |

## 🔄 Migrasi Data (Opsional)

Jika Anda sudah punya data di SQLite dan ingin migrasi ke PostgreSQL:

1. **Export data dari SQLite**:
```bash
python -c "
import sqlite3
import json
conn = sqlite3.connect('ecommerce.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM user')
users = cursor.fetchall()
print(json.dumps(users))
conn.close()
"
```

2. **Import ke PostgreSQL** (buat script custom sesuai kebutuhan)

## 🛠️ Development Tips

### Menggunakan pgAdmin (GUI)
1. Install pgAdmin dari [https://www.pgadmin.org/](https://www.pgadmin.org/)
2. Connect ke database dengan credentials dari `config.env`
3. Browse dan edit data secara visual

### Backup Database
```bash
# Backup
pg_dump -h localhost -U postgres -d belanjakita > backup.sql

# Restore
psql -h localhost -U postgres -d belanjakita < backup.sql
```

### Monitor Database
```sql
-- Cek ukuran database
SELECT pg_size_pretty(pg_database_size('belanjakita'));

-- Cek tabel terbesar
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

## 🎯 Next Steps

Setelah setup PostgreSQL berhasil:

1. **Test semua fitur aplikasi**
2. **Tambah data produk dan kategori**
3. **Test user registration dan login**
4. **Test admin panel**
5. **Deploy ke production** (jika diperlukan)

## 📞 Support

Jika mengalami masalah:
1. Cek error message dengan teliti
2. Pastikan PostgreSQL berjalan
3. Verifikasi konfigurasi di `config.env`
4. Test koneksi dengan `python setup_database.py` 