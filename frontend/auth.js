// Authentication utility functions
const API_BASE_URL = 'http://localhost:8000';

// Get token from localStorage
function getToken() {
    return localStorage.getItem('access_token');
}

// Set token in localStorage
function setToken(token) {
    localStorage.setItem('access_token', token);
}

// Remove token from localStorage
function removeToken() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_info');
}

// Get user info from localStorage
function getUserInfo() {
    const userStr = localStorage.getItem('user_info');
    return userStr ? JSON.parse(userStr) : null;
}

// Set user info in localStorage
function setUserInfo(user) {
    localStorage.setItem('user_info', JSON.stringify(user));
}

// Check if user is authenticated
function isAuthenticated() {
    return getToken() !== null;
}

// Redirect to login if not authenticated
function requireAuth() {
    if (!isAuthenticated()) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

// Make authenticated API request
async function fetchWithAuth(url, options = {}) {
    const token = getToken();
    
    if (!token) {
        window.location.href = 'login.html';
        return;
    }

    const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
        ...options.headers
    };

    try {
        const response = await fetch(url, { ...options, headers });
        
        // If unauthorized, redirect to login
        if (response.status === 401) {
            removeToken();
            window.location.href = 'login.html';
            return;
        }

        return response;
    } catch (error) {
        console.error('Fetch error:', error);
        throw error;
    }
}

// Login function
async function login(username, password) {
    try {
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Login failed');
        }

        const data = await response.json();
        setToken(data.access_token);

        // Get user info
        const userResponse = await fetch(`${API_BASE_URL}/auth/me`, {
            headers: {
                'Authorization': `Bearer ${data.access_token}`
            }
        });

        if (userResponse.ok) {
            const userInfo = await userResponse.json();
            setUserInfo(userInfo);
        }

        return { success: true, data };
    } catch (error) {
        return { success: false, error: error.message };
    }
}

// Logout function
function logout() {
    removeToken();
    window.location.href = 'login.html';
}

// Display user info in navbar
function displayUserInfo() {
    const userInfo = getUserInfo();
    if (userInfo) {
        const navLinks = document.querySelector('.nav-links');
        if (navLinks) {
            const userDiv = document.createElement('div');
            userDiv.style.cssText = 'margin-left: auto; display: flex; align-items: center; gap: 15px;';
            userDiv.innerHTML = `
                <span style="color: white;">👤 ${userInfo.full_name || userInfo.username} (${userInfo.role})</span>
                <button onclick="logout()" style="padding: 8px 15px; background: #dc3545; color: white; border: none; border-radius: 4px; cursor: pointer;">Logout</button>
            `;
            navLinks.appendChild(userDiv);
        }
    }
}

// Check if user has permission for an action
function hasPermission(action) {
    const userInfo = getUserInfo();
    if (!userInfo) return false;
    
    const role = userInfo.role;
    
    // Admin has all permissions
    if (role === 'admin') return true;
    
    // Define permissions per role
    const permissions = {
        'doctor': ['view', 'add', 'edit', 'prescribe'],
        'nurse': ['view', 'add', 'edit', 'admit'],
        'receptionist': ['view', 'add', 'schedule']
    };
    
    return permissions[role]?.includes(action) || false;
}

// Hide/show elements based on permissions
function applyRoleBasedUI() {
    const userInfo = getUserInfo();
    if (!userInfo) return;
    
    const role = userInfo.role;
    
    // Hide delete buttons for non-admins
    if (role !== 'admin') {
        const deleteButtons = document.querySelectorAll('button[onclick*="delete"]');
        deleteButtons.forEach(btn => {
            btn.style.display = 'none';
        });
    }
    
    // Hide edit buttons for receptionists
    if (role === 'receptionist') {
        const editButtons = document.querySelectorAll('button[onclick*="edit"]');
        editButtons.forEach(btn => {
            btn.style.display = 'none';
        });
        
        // Disable edit form fields
        const saveBtn = document.getElementById('saveBtn');
        if (saveBtn && saveBtn.innerText.includes('Update')) {
            saveBtn.style.display = 'none';
        }
    }
    
    // Show role-specific notice
    showRoleNotice(role);
}

// Show role-specific notice
function showRoleNotice(role) {
    const container = document.querySelector('.container');
    if (!container || document.getElementById('roleNotice')) return;
    
    const notices = {
        'admin': '🔓 Administrator: Full system access',
        'doctor': '👨‍⚕️ Doctor: Can manage patients, prescriptions, and appointments',
        'nurse': '👩‍⚕️ Nurse: Can manage patients, admissions, and appointments',
        'receptionist': '📋 Receptionist: Can view and add patients, schedule appointments'
    };
    
    const noticeDiv = document.createElement('div');
    noticeDiv.id = 'roleNotice';
    noticeDiv.style.cssText = 'background: #e3f2fd; padding: 12px; border-radius: 6px; margin-bottom: 20px; border-left: 4px solid #2196f3;';
    noticeDiv.innerHTML = `<strong>${notices[role] || 'User'}</strong>`;
    
    const firstH2 = container.querySelector('h2');
    if (firstH2) {
        container.insertBefore(noticeDiv, firstH2);
    }
}

// Handle login form submission
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const errorDiv = document.getElementById('errorMessage');
        const successDiv = document.getElementById('successMessage');
        
        errorDiv.style.display = 'none';
        successDiv.style.display = 'none';
        
        const result = await login(username, password);
        
        if (result.success) {
            successDiv.textContent = 'Login successful! Redirecting...';
            successDiv.style.display = 'block';
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1000);
        } else {
            errorDiv.textContent = result.error;
            errorDiv.style.display = 'block';
        }
    });
}

// Check authentication on page load (except login page)
if (window.location.pathname.includes('login.html')) {
    // If already logged in, redirect to index
    if (isAuthenticated()) {
        window.location.href = 'index.html';
    }
} else {
    // Require authentication for all other pages
    if (requireAuth()) {
        displayUserInfo();
        applyRoleBasedUI();
    }
}
