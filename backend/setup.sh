#!/bin/bash

# Hospital Management System - Quick Setup Script

echo "🏥 Hospital Management System - Security Setup"
echo "=============================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if MySQL is running
if ! command -v mysql &> /dev/null; then
    echo "⚠️  MySQL client not found. Make sure MySQL/MariaDB is installed."
else
    echo "✅ MySQL client found"
fi
echo ""

# Create virtual environment
echo "📦 Setting up virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created - PLEASE UPDATE WITH YOUR VALUES!"
else
    echo "ℹ️  .env file already exists"
fi
echo ""

# Create database
echo "🗄️  Setting up database..."
echo "Please ensure MySQL is running and you have the credentials."
read -p "Create database 'hospital_db'? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS hospital_db;"
    echo "✅ Database created"
fi
echo ""

# Create tables
echo "📊 Creating database tables..."
python3 -c "from database import Base, engine; Base.metadata.create_all(bind=engine); print('✅ Tables created')"
echo ""

# Initialize admin user
echo "👤 Creating admin user..."
read -p "Create initial admin user? (y/n) " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3 init_admin.py
fi
echo ""

echo "=============================================="
echo "✅ Setup Complete!"
echo ""
echo "📚 Next Steps:"
echo "1. Update .env file with your configuration"
echo "2. Start server: uvicorn main:app --reload"
echo "3. Visit API docs: http://localhost:8000/docs"
echo "4. Login with username: admin, password: admin123"
echo "5. ⚠️  CHANGE DEFAULT PASSWORDS IMMEDIATELY!"
echo ""
echo "📖 Read SECURITY_README.md for detailed documentation"
echo "=============================================="
