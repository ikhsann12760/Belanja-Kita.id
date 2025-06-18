// Main JavaScript for E-Commerce Store

// Global Variables
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let wishlist = JSON.parse(localStorage.getItem('wishlist')) || [];

// Hero Section Animations
function initHeroAnimations() {
    const floatingIcons = document.querySelectorAll('.floating-icon');
    const heroMainIcon = document.querySelector('.hero-main-icon');
    
    // Add click effects to floating icons
    floatingIcons.forEach((icon, index) => {
        icon.addEventListener('click', function() {
            // Create ripple effect
            createRippleEffect(this);
            
            // Show tooltip with product category
            const categories = ['Elektronik', 'Pakaian', 'Makanan', 'Buku'];
            const category = categories[index] || 'Produk';
            showTooltip(this, `Lihat ${category}`);
            
            // Animate icon
            this.style.transform = 'scale(1.3) rotate(15deg)';
            setTimeout(() => {
                this.style.transform = '';
            }, 300);
        });
        
        // Add hover sound effect (optional)
        icon.addEventListener('mouseenter', function() {
            // You can add sound effects here if needed
            this.style.filter = 'drop-shadow(0 0 20px rgba(255,255,255,0.6))';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.filter = 'drop-shadow(0 0 10px rgba(255,255,255,0.2))';
        });
    });
    
    // Add click effect to main hero icon
    if (heroMainIcon) {
        heroMainIcon.addEventListener('click', function() {
            createRippleEffect(this);
            showTooltip(this, 'Belanja Kita.id');
            
            // Pulse animation
            this.style.animation = 'pulse 0.5s ease-in-out';
            setTimeout(() => {
                this.style.animation = 'pulse 2s infinite';
            }, 500);
        });
    }
}

// Create ripple effect
function createRippleEffect(element) {
    const ripple = document.createElement('div');
    ripple.className = 'ripple-effect';
    ripple.style.cssText = `
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple 0.6s linear;
        pointer-events: none;
        top: 50%;
        left: 50%;
        width: 100px;
        height: 100px;
        margin-top: -50px;
        margin-left: -50px;
    `;
    
    element.style.position = 'relative';
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Show tooltip
function showTooltip(element, text) {
    // Remove existing tooltip
    const existingTooltip = document.querySelector('.custom-tooltip');
    if (existingTooltip) {
        existingTooltip.remove();
    }
    
    const tooltip = document.createElement('div');
    tooltip.className = 'custom-tooltip';
    tooltip.textContent = text;
    tooltip.style.cssText = `
        position: absolute;
        background: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 8px 12px;
        border-radius: 6px;
        font-size: 12px;
        white-space: nowrap;
        z-index: 1000;
        top: -40px;
        left: 50%;
        transform: translateX(-50%);
        animation: tooltipFadeIn 0.3s ease-out;
    `;
    
    element.style.position = 'relative';
    element.appendChild(tooltip);
    
    setTimeout(() => {
        tooltip.remove();
    }, 2000);
}

// Add CSS animations for new effects
function addCustomStyles() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ripple {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
        
        @keyframes tooltipFadeIn {
            from {
                opacity: 0;
                transform: translateX(-50%) translateY(10px);
            }
            to {
                opacity: 1;
                transform: translateX(-50%) translateY(0);
            }
        }
        
        .custom-tooltip::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            margin-left: -5px;
            border-width: 5px;
            border-style: solid;
            border-color: rgba(0, 0, 0, 0.8) transparent transparent transparent;
        }
        
        .hero-section {
            position: relative;
        }
        
        .hero-section::after {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: radial-gradient(circle at 20% 80%, rgba(255,255,255,0.1) 0%, transparent 50%),
                        radial-gradient(circle at 80% 20%, rgba(255,255,255,0.1) 0%, transparent 50%);
            pointer-events: none;
            animation: backgroundShift 10s ease-in-out infinite;
        }
        
        @keyframes backgroundShift {
            0%, 100% {
                opacity: 0.3;
            }
            50% {
                opacity: 0.6;
            }
        }
    `;
    document.head.appendChild(style);
}

// Utility Functions
function formatCurrency(amount) {
    return new Intl.NumberFormat('id-ID', {
        style: 'currency',
        currency: 'IDR'
    }).format(amount);
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

function showLoading(element) {
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    element.appendChild(spinner);
    element.disabled = true;
}

function hideLoading(element) {
    const spinner = element.querySelector('.spinner');
    if (spinner) {
        spinner.remove();
    }
    element.disabled = false;
}

// Cart Functions
function addToCart(productId, quantity = 1) {
    // Check if product already in cart
    const existingItem = cart.find(item => item.productId === productId);
    
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push({
            productId: productId,
            quantity: quantity,
            addedAt: new Date().toISOString()
        });
    }
    
    // Save to localStorage
    localStorage.setItem('cart', JSON.stringify(cart));
    
    // Update cart badge
    updateCartBadge();
    
    showNotification('Produk berhasil ditambahkan ke keranjang!', 'success');
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.productId !== productId);
    localStorage.setItem('cart', JSON.stringify(cart));
    updateCartBadge();
    showNotification('Produk berhasil dihapus dari keranjang!', 'info');
}

function updateCartQuantity(productId, quantity) {
    const item = cart.find(item => item.productId === productId);
    if (item) {
        item.quantity = quantity;
        localStorage.setItem('cart', JSON.stringify(cart));
        updateCartBadge();
    }
}

function updateCartBadge() {
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
        cartBadge.textContent = totalItems;
        cartBadge.style.display = totalItems > 0 ? 'inline' : 'none';
    }
}

function getCartTotal() {
    // This would typically fetch product prices from the server
    // For now, we'll use a placeholder
    return cart.reduce((sum, item) => sum + (item.quantity * 100000), 0);
}

// Wishlist Functions
function addToWishlist(productId) {
    if (!wishlist.includes(productId)) {
        wishlist.push(productId);
        localStorage.setItem('wishlist', JSON.stringify(wishlist));
        showNotification('Produk berhasil ditambahkan ke wishlist!', 'success');
    } else {
        showNotification('Produk sudah ada di wishlist!', 'warning');
    }
}

function removeFromWishlist(productId) {
    wishlist = wishlist.filter(id => id !== productId);
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
    showNotification('Produk berhasil dihapus dari wishlist!', 'info');
}

function isInWishlist(productId) {
    return wishlist.includes(productId);
}

// Search Functions
function performSearch(query) {
    // This would typically make an AJAX request to the server
    console.log('Searching for:', query);
    
    // For now, we'll just show a notification
    showNotification(`Mencari: ${query}`, 'info');
}

// Filter Functions
function applyFilters(filters) {
    // This would typically make an AJAX request to the server
    console.log('Applying filters:', filters);
    
    // For now, we'll just show a notification
    showNotification('Filter diterapkan!', 'info');
}

// Product Functions
function viewProduct(productId) {
    window.location.href = `/product/${productId}`;
}

function buyNow(productId, quantity = 1) {
    // Add to cart and redirect to checkout
    addToCart(productId, quantity);
    setTimeout(() => {
        window.location.href = '/checkout';
    }, 1000);
}

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Image Upload Functions
function handleImageUpload(input, previewId) {
    const file = input.files[0];
    if (!file) return;
    
    // Validate file size (2MB max)
    if (file.size > 2 * 1024 * 1024) {
        showNotification('Ukuran file terlalu besar. Maksimal 2MB.', 'error');
        input.value = '';
        return;
    }
    
    // Validate file type
    const allowedTypes = ['image/jpeg', 'image/png', 'image/gif'];
    if (!allowedTypes.includes(file.type)) {
        showNotification('Format file tidak didukung. Gunakan JPG, PNG, atau GIF.', 'error');
        input.value = '';
        return;
    }
    
    // Preview image
    const reader = new FileReader();
    reader.onload = function(e) {
        const preview = document.getElementById(previewId);
        if (preview) {
            preview.src = e.target.result;
            preview.style.display = 'block';
        }
    };
    reader.readAsDataURL(file);
}

// Animation Functions
function animateOnScroll() {
    const elements = document.querySelectorAll('.animate-on-scroll');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

// Lazy Loading
function lazyLoadImages() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        imageObserver.observe(img);
    });
}

// AJAX Functions
function makeRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .catch(error => {
        console.error('Request failed:', error);
        showNotification('Terjadi kesalahan. Silakan coba lagi.', 'error');
        throw error;
    });
}

// Local Storage Functions
function saveToLocalStorage(key, data) {
    try {
        localStorage.setItem(key, JSON.stringify(data));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

function getFromLocalStorage(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (error) {
        console.error('Error reading from localStorage:', error);
        return null;
    }
}

// Theme Functions
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    
    showNotification(`Tema berubah ke ${newTheme === 'dark' ? 'gelap' : 'terang'}`, 'info');
}

function loadTheme() {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
}

// About Us Section Animations
function initAboutAnimations() {
    const aboutIcons = document.querySelectorAll('.floating-about-icon');
    const mainAboutIcon = document.querySelector('.main-about-icon');
    const statNumbers = document.querySelectorAll('.stat-number');
    
    // Add click effects to about icons
    aboutIcons.forEach((icon, index) => {
        icon.addEventListener('click', function() {
            // Create ripple effect
            createRippleEffect(this);
            
            // Show tooltip with feature description
            const features = [
                'Keranjang Belanja',
                'Pembayaran Aman',
                'Pengiriman Cepat',
                'Rating Terbaik',
                'Pelanggan Puas',
                'Keamanan Data'
            ];
            const feature = features[index] || 'Fitur Unggulan';
            showTooltip(this, feature);
            
            // Animate icon
            this.style.transform = 'scale(1.4) rotate(20deg)';
            setTimeout(() => {
                this.style.transform = '';
            }, 400);
        });
        
        // Add hover effects
        icon.addEventListener('mouseenter', function() {
            this.style.filter = 'drop-shadow(0 0 20px rgba(255,255,255,0.6))';
        });
        
        icon.addEventListener('mouseleave', function() {
            this.style.filter = 'drop-shadow(0 0 10px rgba(255,255,255,0.3))';
        });
    });
    
    // Add click effect to main about icon
    if (mainAboutIcon) {
        mainAboutIcon.addEventListener('click', function() {
            createRippleEffect(this);
            showTooltip(this, 'Belanja Kita.id - Tentang Kami');
            
            // Pulse animation
            this.style.animation = 'aboutPulse 0.8s ease-in-out';
            setTimeout(() => {
                this.style.animation = 'aboutPulse 3s ease-in-out infinite';
            }, 800);
        });
    }
    
    // Initialize counter animation
    initCounterAnimation(statNumbers);
}

// Counter animation function
function initCounterAnimation(elements) {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const finalValue = parseInt(target.getAttribute('data-target'));
                animateCounter(target, 0, finalValue, 2000);
                observer.unobserve(target);
            }
        });
    });
    
    elements.forEach(element => {
        observer.observe(element);
    });
}

function animateCounter(element, start, end, duration) {
    const startTime = performance.now();
    const suffix = element.textContent.includes('K') ? 'K' : '+';
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutQuart = 1 - Math.pow(1 - progress, 4);
        const current = Math.floor(start + (end - start) * easeOutQuart);
        
        element.textContent = current + suffix;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        }
    }
    
    requestAnimationFrame(updateCounter);
}

// Feature items animation
function initFeatureAnimations() {
    const featureItems = document.querySelectorAll('.feature-item');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateX(0)';
            }
        });
    });
    
    featureItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-20px)';
        item.style.transition = `all 0.5s ease ${index * 0.1}s`;
        observer.observe(item);
    });
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add custom styles for hero animations
    addCustomStyles();
    
    // Initialize hero animations
    initHeroAnimations();
    
    // Initialize about us animations
    initAboutAnimations();
    
    // Initialize feature animations
    initFeatureAnimations();
    
    // Initialize cart badge
    updateCartBadge();
    
    // Load theme
    loadTheme();
    
    // Initialize animations
    animateOnScroll();
    
    // Initialize lazy loading
    lazyLoadImages();
    
    // Add smooth scrolling to all links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add loading states to forms
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn && !this.classList.contains('no-loading')) {
                showLoading(submitBtn);
            }
        });
    });
    
    // Add confirmation to delete buttons
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Apakah Anda yakin ingin menghapus item ini?')) {
                e.preventDefault();
            }
        });
    });
    
    // Add tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Add popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
});

// Export functions for global use
window.ECommerce = {
    addToCart,
    removeFromCart,
    updateCartQuantity,
    addToWishlist,
    removeFromWishlist,
    isInWishlist,
    performSearch,
    applyFilters,
    viewProduct,
    buyNow,
    validateForm,
    handleImageUpload,
    showNotification,
    formatCurrency,
    toggleTheme,
    makeRequest
}; 