#!/usr/bin/env python3
"""
Setup script for Solana Risk Dashboard
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing packages: {e}")
        return False

def create_env_file():
    """Create .env file template"""
    env_content = """# Solana Risk Dashboard - Environment Variables
# Copy this file to .env and add your API keys

# Google Gemini API Key (for AI insights)
# Get from: https://aistudio.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Helius API Key (for Solana wallet data)
# Get from: https://helius.xyz
HELIUS_API_KEY=your_helius_api_key_here

# CoinGecko API Key (optional, for higher rate limits)
# Get from: https://www.coingecko.com/en/api
COINGECKO_API_KEY=your_coingecko_api_key_here
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(env_content)
        print("✅ Created .env template file")
        print("📝 Please edit .env file and add your API keys")
    else:
        print("⚠️  .env file already exists")

def main():
    """Main setup function"""
    print("🚀 Solana Risk Dashboard Setup")
    print("=" * 40)
    
    # Install packages
    if not install_requirements():
        print("❌ Setup failed during package installation")
        return False
    
    # Create env file
    create_env_file()
    
    print("\n🎉 Setup complete!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: streamlit run app.py")
    print("3. Open http://localhost:8501 in your browser")
    
    return True

if __name__ == "__main__":
    main()
