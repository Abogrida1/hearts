#!/usr/bin/env python3
"""
YouTube Downloader App - Quick Start for Render
تطبيق تحميل YouTube - تشغيل سريع لـ Render
"""

import os
import sys
import subprocess
import time

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ مطلوب")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} تم اكتشافه")
    return True

def install_requirements():
    """Install required packages"""
    print("📦 جاري تثبيت المتطلبات...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ تم تثبيت المتطلبات بنجاح")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل في تثبيت المتطلبات: {e}")
        return False

def test_app():
    """Test the Flask application"""
    print("🚀 جاري اختبار التطبيق...")
    
    try:
        # Import and test the app
        from app import create_app
        
        app = create_app()
        print("✅ تم إنشاء تطبيق Flask بنجاح")
        
        # Test basic functionality
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/health')
            if response.status_code == 200:
                print("✅ نقطة الصحة تعمل")
            else:
                print(f"❌ فشلت نقطة الصحة: {response.status_code}")
            
            # Test index endpoint
            response = client.get('/')
            if response.status_code == 200:
                print("✅ نقطة الصفحة الرئيسية تعمل")
            else:
                print(f"❌ فشلت نقطة الصفحة الرئيسية: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ فشل في اختبار التطبيق: {e}")
        return False

def run_app():
    """Run the Flask application"""
    print("🌐 جاري بدء الخادم المحلي...")
    print("📱 افتح المتصفح واذهب إلى: http://localhost:5000")
    print("⏹️  اضغط Ctrl+C لإيقاف الخادم")
    print("-" * 50)
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n🛑 تم إيقاف الخادم بواسطة المستخدم")
    except Exception as e:
        print(f"❌ فشل في تشغيل التطبيق: {e}")

def show_deploy_info():
    """Show deployment information"""
    print("\n🚀 معلومات النشر على Render:")
    print("=" * 40)
    print("1️⃣ ارفع الكود على GitHub")
    print("2️⃣ اذهب إلى https://render.com")
    print("3️⃣ أنشئ Web Service جديد")
    print("4️⃣ اربط مستودع GitHub")
    print("5️⃣ التطبيق سيعمل تلقائياً!")
    print("\n🔗 رابط التطبيق: https://your-app.onrender.com")
    print("✅ خطة مجانية")
    print("✅ SSL تلقائي")
    print("✅ نشر تلقائي")
    print("✅ قاعدة بيانات مجانية (اختياري)")

def main():
    """Main function"""
    print("🎯 YouTube Downloader App - Render Ready")
    print("تطبيق تحميل YouTube - جاهز لـ Render")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    # Test app
    if not test_app():
        return
    
    # Show deployment info
    show_deploy_info()
    
    # Ask user if they want to run locally
    print("\n" + "=" * 50)
    choice = input("هل تريد تشغيل التطبيق محلياً؟ (y/n): ").lower().strip()
    
    if choice in ['y', 'yes', 'نعم', 'y']:
        run_app()
    else:
        print("👋 شكراً لك! التطبيق جاهز للنشر على Render")

if __name__ == "__main__":
    main()
