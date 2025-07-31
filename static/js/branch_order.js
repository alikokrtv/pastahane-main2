// Branch Order Management JavaScript
console.log('Branch Order JS loaded');

// Global variables
let orderItems = {};
let totalAmount = 0;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing branch order functionality');
    
    // Wait a bit for products data to be available
    setTimeout(function() {
        if (window.productsData) {
            console.log('Products data found:', window.productsData);
            initializeOrderPage();
        } else {
            console.error('Products data not available');
        }
    }, 100);
});

function initializeOrderPage() {
    console.log('Initializing order page...');
    
    // Use global products data if available
    const products = window.productsData || {};
    
    // Initialize order items from products data
    Object.keys(products).forEach(productId => {
        const product = products[productId];
        orderItems[productId] = {
            quantity: 0,
            price: product.price,
            name: product.name,
            unit: product.unit
        };
    });
    
    // Add event listeners to all buttons
    const minusButtons = document.querySelectorAll('button[data-product-id]');
    
    minusButtons.forEach(button => {
        const productId = button.getAttribute('data-product-id');
        
        if (button.innerHTML.includes('fa-minus')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Minus button clicked for product:', productId);
                changeQuantity(productId, -1);
            });
        } else if (button.innerHTML.includes('fa-plus')) {
            button.addEventListener('click', function(e) {
                e.preventDefault();
                console.log('Plus button clicked for product:', productId);
                changeQuantity(productId, 1);
            });
        }
    });
    
    console.log('Order page initialized successfully');
    console.log('Order items:', orderItems);
}

function changeQuantity(productId, change) {
    console.log(`Changing quantity for product ${productId} by ${change}`);
    
    const input = document.getElementById(`quantity_${productId}`);
    if (!input) {
        console.error(`Input not found for product ${productId}`);
        return;
    }
    
    let currentQuantity = parseInt(input.value) || 0;
    let newQuantity = Math.max(0, currentQuantity + change);
    
    // Update input value
    input.value = newQuantity;
    
    // Update order items
    if (orderItems[productId]) {
        orderItems[productId].quantity = newQuantity;
    }
    
    console.log(`Updated quantity for product ${productId}: ${newQuantity}`);
    
    // Update order summary
    updateOrderSummary();
}

function updateOrderSummary() {
    console.log('Updating order summary...');
    
    totalAmount = 0;
    let totalItems = 0;
    
    // Calculate totals
    Object.keys(orderItems).forEach(productId => {
        const item = orderItems[productId];
        if (item.quantity > 0) {
            totalAmount += item.quantity * item.price;
            totalItems += item.quantity;
        }
    });
    
    // Update total display
    const totalElement = document.querySelector('#order-total, .order-total, [class*="total"]');
    if (totalElement) {
        totalElement.textContent = `₺${totalAmount.toFixed(2)}`;
    }
    
    // Update order summary section if exists
    const summaryElement = document.querySelector('#order-summary, .order-summary');
    if (summaryElement) {
        let summaryHTML = '<h4>Sipariş Özeti</h4>';
        
        Object.keys(orderItems).forEach(productId => {
            const item = orderItems[productId];
            if (item.quantity > 0) {
                summaryHTML += `
                    <div class="flex justify-between py-1">
                        <span>${item.name} x${item.quantity}</span>
                        <span>₺${(item.quantity * item.price).toFixed(2)}</span>
                    </div>
                `;
            }
        });
        
        summaryHTML += `
            <div class="border-t pt-2 mt-2 font-bold">
                <div class="flex justify-between">
                    <span>Toplam:</span>
                    <span>₺${totalAmount.toFixed(2)}</span>
                </div>
            </div>
        `;
        
        summaryElement.innerHTML = summaryHTML;
    }
    
    console.log(`Order summary updated - Total: ₺${totalAmount.toFixed(2)}, Items: ${totalItems}`);
}

// Export functions for global access if needed
window.changeQuantity = changeQuantity;
window.updateOrderSummary = updateOrderSummary;
