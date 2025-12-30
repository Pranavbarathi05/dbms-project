-- Initial Admin User Setup Script
-- Run this after creating all tables

-- This script creates an initial admin user
-- Default credentials:
-- Username: admin
-- Password: admin123 (CHANGE THIS IMMEDIATELY IN PRODUCTION!)

-- The password hash below is for 'admin123' using bcrypt
INSERT INTO users (username, email, full_name, hashed_password, role, is_active, created_at)
VALUES (
    'admin',
    'admin@hospital.example.com',
    'System Administrator',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLa.eqLG',  -- Password: admin123
    'admin',
    TRUE,
    NOW()
);

-- Create sample users for testing (optional)
INSERT INTO users (username, email, full_name, hashed_password, role, is_active, created_at)
VALUES 
    ('dr.smith', 'dr.smith@hospital.example.com', 'Dr. John Smith', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLa.eqLG', 'doctor', TRUE, NOW()),
    ('nurse.jane', 'nurse.jane@hospital.example.com', 'Jane Doe', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLa.eqLG', 'nurse', TRUE, NOW()),
    ('receptionist', 'reception@hospital.example.com', 'Sarah Johnson', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzpLa.eqLG', 'receptionist', TRUE, NOW());

-- Verify users were created
SELECT id, username, email, role, is_active FROM users;

-- Note: All sample users have password 'admin123'
-- IMPORTANT: Change passwords immediately after first login!
