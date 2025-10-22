// Bridge Exchange - Telegram WebApp JavaScript

// Initialize Telegram WebApp
const tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// Global state
let currentScreen = 'home';
let currentOrderSide = 'buy';

// API Configuration
const API_BASE = 'http://localhost:8000/api';

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    // Set Telegram theme
    tg.setHeaderColor('#1a0b2e');
    tg.setBackgroundColor('#1a0b2e');
    
    // Show home screen by default
    showScreen('home');
    
    // Load user data
    loadUserData();
}

function setupEventListeners() {
    // Amount slider
    const amountSlider = document.getElementById('amount-slider');
    if (amountSlider) {
        amountSlider.addEventListener('input', function() {
            const percentage = this.value;
            const availableBalance = 1000; // Mock balance
            const amount = (availableBalance * percentage) / 100;
            document.getElementById('order-amount').value = amount.toFixed(2);
        });
    }
    
    // Exchange amount calculation
    const sendAmount = document.getElementById('send-amount');
    const receiveAmount = document.getElementById('receive-amount');
    
    if (sendAmount && receiveAmount) {
        sendAmount.addEventListener('input', calculateExchange);
    }
}

// Screen Navigation
function showScreen(screenName) {
    // Hide all screens
    const screens = document.querySelectorAll('.screen');
    screens.forEach(screen => screen.classList.remove('active'));
    
    // Show selected screen
    const targetScreen = document.getElementById(screenName + '-screen');
    if (targetScreen) {
        targetScreen.classList.add('active');
        currentScreen = screenName;
    }
}

function showHome() {
    showScreen('home');
}

function showExchange() {
    showScreen('exchange');
}

function showTrade() {
    showScreen('trade');
}

function showGames() {
    showScreen('games');
}

function showAssets() {
    showScreen('assets');
}

// Modal Functions
function showModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.add('active');
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.classList.remove('active');
    }
}

function showDeposit() {
    showModal('deposit-modal');
}

function showWithdraw() {
    showModal('withdraw-modal');
}

function showBuy() {
    showModal('deposit-modal'); // Same as deposit for now
}

function showPay() {
    // Show QR code or payment interface
    tg.showAlert('Payment QR code would be displayed here');
}

function showMore() {
    tg.showAlert('More options:\n• Invoices\n• Flight tickets\n• Service payments\n• Promo codes\n• Fees');
}

// Exchange Functions
function showConverter() {
    // Switch to converter tab
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelector('.tab').classList.add('active');
}

function showBuySell() {
    // Switch to buy/sell tab
    document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
    document.querySelectorAll('.tab')[1].classList.add('active');
}

function calculateExchange() {
    const sendAmount = parseFloat(document.getElementById('send-amount').value) || 0;
    const sendCurrency = document.getElementById('send-currency').value;
    const receiveCurrency = document.getElementById('receive-currency').value;
    
    // Mock exchange rates
    const rates = {
        'USDT': { 'BTC': 0.000023, 'ETH': 0.0004 },
        'BTC': { 'USDT': 43000, 'ETH': 15 },
        'ETH': { 'USDT': 2800, 'BTC': 0.065 }
    };
    
    if (rates[sendCurrency] && rates[sendCurrency][receiveCurrency]) {
        const rate = rates[sendCurrency][receiveCurrency];
        const receiveAmount = sendAmount * rate;
        document.getElementById('receive-amount').value = receiveAmount.toFixed(8);
    }
}

function executeExchange() {
    const sendAmount = document.getElementById('send-amount').value;
    const receiveAmount = document.getElementById('receive-amount').value;
    
    if (!sendAmount || !receiveAmount) {
        tg.showAlert('Please enter amounts');
        return;
    }
    
    tg.showConfirm(
        `Exchange ${sendAmount} ${document.getElementById('send-currency').value} for ${receiveAmount} ${document.getElementById('receive-currency').value}?`,
        function(confirmed) {
            if (confirmed) {
                tg.showAlert('Exchange executed successfully!');
                // Reset form
                document.getElementById('send-amount').value = '';
                document.getElementById('receive-amount').value = '';
            }
        }
    );
}

// Trading Functions
function setOrderSide(side) {
    currentOrderSide = side;
    
    // Update tab appearance
    document.querySelectorAll('.order-tab').forEach(tab => tab.classList.remove('active'));
    document.querySelector(`[onclick="setOrderSide('${side}')"]`).classList.add('active');
    
    // Update button text
    const button = document.querySelector('.buy-btn');
    if (side === 'buy') {
        button.textContent = 'Buy BTC';
        button.className = 'buy-btn';
    } else {
        button.textContent = 'Sell BTC';
        button.className = 'sell-btn';
    }
}

function placeOrder() {
    const amount = document.getElementById('order-amount').value;
    const price = document.getElementById('order-price').value;
    
    if (!amount) {
        tg.showAlert('Please enter amount');
        return;
    }
    
    const orderType = price ? 'limit' : 'market';
    const confirmText = orderType === 'limit' 
        ? `Place ${currentOrderSide} order: ${amount} BTC at ${price} USDT?`
        : `Place ${currentOrderSide} market order: ${amount} BTC?`;
    
    tg.showConfirm(confirmText, function(confirmed) {
        if (confirmed) {
            tg.showAlert('Order placed successfully!');
            // Reset form
            document.getElementById('order-amount').value = '';
            document.getElementById('order-price').value = '';
        }
    });
}

// Services Functions
function selectService(service) {
    const services = {
        'steam': 'Steam Gift Cards',
        'playstation': 'PlayStation Store Cards',
        'netflix': 'Netflix Subscriptions',
        'spotify': 'Spotify Premium'
    };
    
    tg.showAlert(`Selected: ${services[service]}\nThis would open the service selection interface.`);
}

// Assets Functions
function toggleAssetType(type) {
    document.querySelectorAll('.toggle-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelector(`[onclick="toggleAssetType('${type}')"]`).classList.add('active');
    
    // Filter assets based on type
    const assetItems = document.querySelectorAll('.asset-item');
    assetItems.forEach(item => {
        if (type === 'crypto') {
            item.style.display = 'flex';
        } else {
            // Hide crypto assets, show fiat
            item.style.display = 'none';
        }
    });
}

// API Functions
async function loadUserData() {
    try {
        // Mock user data - in production, this would come from the API
        const userData = {
            id: 1,
            telegram_id: 123456789,
            username: 'testuser',
            level: 1,
            is_premium: false
        };
        
        // Update UI with user data
        document.querySelector('.user-level').textContent = `Level ${userData.level}`;
        
    } catch (error) {
        console.error('Error loading user data:', error);
    }
}

async function createDeposit() {
    const asset = document.getElementById('deposit-asset').value;
    const amount = document.getElementById('deposit-amount').value;
    
    if (!amount || parseFloat(amount) <= 0) {
        tg.showAlert('Please enter a valid amount');
        return;
    }
    
    try {
        // Mock API call
        tg.showAlert(`Creating deposit: ${amount} ${asset}\nThis would create a CryptoPay invoice.`);
        closeModal('deposit-modal');
        
        // Reset form
        document.getElementById('deposit-amount').value = '';
        
    } catch (error) {
        tg.showAlert('Error creating deposit');
        console.error('Deposit error:', error);
    }
}

async function createWithdraw() {
    const asset = document.getElementById('withdraw-asset').value;
    const amount = document.getElementById('withdraw-amount').value;
    const address = document.getElementById('withdraw-address').value;
    
    if (!amount || parseFloat(amount) <= 0) {
        tg.showAlert('Please enter a valid amount');
        return;
    }
    
    if (!address) {
        tg.showAlert('Please enter withdrawal address');
        return;
    }
    
    try {
        // Mock API call
        tg.showAlert(`Creating withdrawal: ${amount} ${asset} to ${address}\nThis would create a withdrawal request.`);
        closeModal('withdraw-modal');
        
        // Reset form
        document.getElementById('withdraw-amount').value = '';
        document.getElementById('withdraw-address').value = '';
        
    } catch (error) {
        tg.showAlert('Error creating withdrawal');
        console.error('Withdrawal error:', error);
    }
}

// Utility Functions
function formatCurrency(amount, currency = 'USDT') {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2,
        maximumFractionDigits: 8
    }).format(amount);
}

function formatNumber(number, decimals = 2) {
    return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(number);
}

// Error handling
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    tg.showAlert('An error occurred. Please try again.');
});

// Handle Telegram WebApp events
tg.onEvent('viewportChanged', function() {
    // Handle viewport changes
    console.log('Viewport changed');
});

tg.onEvent('themeChanged', function() {
    // Handle theme changes
    console.log('Theme changed');
});

// Export functions for global access
window.showScreen = showScreen;
window.showHome = showHome;
window.showExchange = showExchange;
window.showTrade = showTrade;
window.showGames = showGames;
window.showAssets = showAssets;
window.showDeposit = showDeposit;
window.showWithdraw = showWithdraw;
window.showBuy = showBuy;
window.showPay = showPay;
window.showMore = showMore;
window.showConverter = showConverter;
window.showBuySell = showBuySell;
window.executeExchange = executeExchange;
window.setOrderSide = setOrderSide;
window.placeOrder = placeOrder;
window.selectService = selectService;
window.toggleAssetType = toggleAssetType;
window.createDeposit = createDeposit;
window.createWithdraw = createWithdraw;
window.closeModal = closeModal;
