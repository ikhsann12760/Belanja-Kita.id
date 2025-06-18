# Fitur Multiple Images untuk Produk

Dokumentasi lengkap untuk fitur multiple images pada produk yang memungkinkan admin menambahkan lebih dari 1 foto untuk setiap produk.

## Fitur yang Tersedia

### 1. Upload Multiple Images
- **Drag & Drop**: Upload gambar dengan drag and drop
- **File Picker**: Upload gambar melalui file picker
- **Multiple Selection**: Pilih beberapa gambar sekaligus
- **Validation**: Validasi tipe file dan ukuran (maksimal 5MB per gambar)
- **Preview**: Preview gambar sebelum upload

### 2. Image Management
- **Primary Image**: Set gambar utama untuk produk
- **Sort Order**: Atur urutan tampilan gambar
- **Delete Images**: Hapus gambar yang tidak diinginkan
- **Reorder**: Drag and drop untuk mengatur urutan

### 3. Backward Compatibility
- **Legacy Support**: Tetap mendukung field `image_url` lama
- **Migration**: Script migrasi untuk data lama
- **Fallback**: Fallback ke gambar utama jika tidak ada gambar

## Struktur Database

### Model ProductImage
```python
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
```

### Model Product (Updated)
```python
class Product(db.Model):
    # ... existing fields ...
    image_url = db.Column(db.String(200))  # Legacy field for backward compatibility
    # ... other fields ...
    
    # New relationship
    images = db.relationship('ProductImage', backref='product', cascade='all, delete-orphan')
```

## File yang Dimodifikasi

### 1. `app.py`
- **Model ProductImage**: Model baru untuk multiple images
- **Route add_product**: Update untuk handle multiple images
- **Route edit_product**: Update untuk handle multiple images
- **Route set_primary_image**: Set gambar utama
- **Route delete_product_image**: Hapus gambar
- **Route reorder_product_images**: Atur urutan gambar

### 2. `templates/admin/add_product.html`
- **Multiple Image Upload**: Interface untuk upload multiple images
- **Drag & Drop**: Area drag and drop dengan visual feedback
- **Image Preview**: Preview gambar sebelum upload
- **Image Management**: Set primary, delete, reorder

### 3. `templates/admin/edit_product.html`
- **Existing Images**: Tampilkan gambar yang sudah ada
- **New Image Upload**: Upload gambar tambahan
- **Image Management**: Kelola gambar existing dan baru

### 4. `migrate_product_images.py`
- **Migration Script**: Script untuk migrasi data lama
- **Data Migration**: Pindahkan gambar dari field `image_url` ke tabel `ProductImage`
- **Cleanup**: Bersihkan field `image_url` lama

## Cara Penggunaan

### 1. Migrasi Data Lama
```bash
python migrate_product_images.py
```

### 2. Upload Multiple Images (Add Product)
1. Buka halaman "Tambah Produk"
2. Drag & drop gambar atau klik "Pilih File"
3. Preview gambar yang diupload
4. Set gambar utama dengan klik icon bintang
5. Atur urutan dengan drag and drop
6. Hapus gambar yang tidak diinginkan
7. Submit form

### 3. Edit Product Images
1. Buka halaman "Edit Produk"
2. Lihat gambar yang sudah ada
3. Upload gambar tambahan jika diperlukan
4. Set gambar utama dengan klik icon bintang
5. Hapus gambar dengan klik icon trash
6. Atur urutan dengan drag and drop
7. Submit form

### 4. API Endpoints

#### Set Primary Image
```http
POST /admin/products/images/{image_id}/set-primary
```

#### Delete Image
```http
POST /admin/products/images/{image_id}/delete
```

#### Reorder Images
```http
POST /admin/products/images/reorder
Content-Type: application/json

{
    "image_ids": [1, 3, 2, 4]
}
```

## Validasi dan Batasan

### File Validation
- **Tipe File**: Hanya gambar (JPG, PNG, GIF)
- **Ukuran File**: Maksimal 5MB per gambar
- **Jumlah File**: Maksimal 10 gambar per produk
- **Required**: Minimal 1 gambar per produk

### Business Rules
- **Primary Image**: Hanya 1 gambar utama per produk
- **Auto Primary**: Gambar pertama otomatis jadi utama
- **Fallback**: Jika gambar utama dihapus, gambar pertama jadi utama
- **Backward Compatibility**: Field `image_url` tetap diisi dengan gambar utama

## Frontend Features

### 1. Drag & Drop Interface
- Visual feedback saat drag over
- Drop zone yang jelas
- Error handling untuk file invalid

### 2. Image Preview
- Thumbnail preview untuk setiap gambar
- Hover overlay dengan actions
- Primary badge untuk gambar utama
- Sort handle untuk reordering

### 3. Image Management
- Set primary dengan icon bintang
- Delete dengan icon trash
- Reorder dengan drag and drop
- Real-time updates

### 4. Responsive Design
- Grid layout yang responsif
- Mobile-friendly interface
- Touch support untuk mobile

## JavaScript Libraries

### 1. SortableJS
- Drag and drop reordering
- Smooth animations
- Touch support

### 2. SweetAlert2
- Beautiful alerts
- Confirmation dialogs
- Success/error messages

## CSS Styling

### 1. Upload Area
```css
.upload-area {
    border: 2px dashed #dee2e6;
    border-radius: 8px;
    padding: 40px;
    text-align: center;
    transition: all 0.3s ease;
    background-color: #f8f9fa;
}

.upload-area.dragover {
    border-color: #007bff;
    background-color: #e3f2fd;
}
```

### 2. Image Preview
```css
.image-preview-item {
    position: relative;
    border: 1px solid #dee2e6;
    border-radius: 8px;
    overflow: hidden;
    background: white;
}

.image-preview-item.primary {
    border-color: #28a745;
    border-width: 2px;
}
```

## Error Handling

### 1. File Validation Errors
- File type validation
- File size validation
- Number of files validation

### 2. Server Errors
- Database errors
- File system errors
- Permission errors

### 3. User Feedback
- Success messages
- Error messages
- Loading states

## Performance Considerations

### 1. Image Optimization
- File size validation (5MB max)
- Efficient file handling
- Proper cleanup

### 2. Database Optimization
- Indexed foreign keys
- Efficient queries
- Proper relationships

### 3. Frontend Optimization
- Lazy loading for images
- Efficient DOM manipulation
- Memory management

## Security Considerations

### 1. File Upload Security
- File type validation
- File size limits
- Secure filename generation
- Path traversal prevention

### 2. Access Control
- Admin-only access
- CSRF protection
- Input validation

### 3. Data Integrity
- Database constraints
- Transaction handling
- Error rollback

## Troubleshooting

### 1. Migration Issues
- Check database permissions
- Verify file paths
- Check disk space

### 2. Upload Issues
- Check file permissions
- Verify upload directory
- Check file size limits

### 3. Display Issues
- Check image paths
- Verify file existence
- Check browser console

## Future Enhancements

### 1. Image Processing
- Auto-resize images
- Generate thumbnails
- Image compression
- WebP support

### 2. Advanced Features
- Image cropping
- Image filters
- Bulk upload
- Image search

### 3. Performance
- CDN integration
- Image lazy loading
- Caching strategies
- Progressive loading

## Testing

### 1. Unit Tests
- Model validation
- Route functionality
- File handling

### 2. Integration Tests
- End-to-end workflows
- Database operations
- File system operations

### 3. User Acceptance Tests
- Upload workflows
- Management features
- Error scenarios

## Deployment Notes

### 1. Database Migration
- Run migration script
- Backup existing data
- Test in staging first

### 2. File System
- Ensure upload directory exists
- Set proper permissions
- Configure backup strategy

### 3. Monitoring
- Monitor disk usage
- Track upload errors
- Monitor performance

## Support

Untuk bantuan teknis atau pertanyaan tentang fitur multiple images, silakan:

1. Periksa log error
2. Cek dokumentasi ini
3. Hubungi tim development
4. Buat issue di repository

---

**Versi**: 1.0  
**Tanggal**: 2024  
**Author**: Development Team 