"""
Launcher for Smart Academic Assistant Pro
Runs both Streamlit frontend and FastAPI backend
"""

import subprocess
import sys
import time
import threading
import os

def run_streamlit():
    """Run Streamlit app"""
    print("🎨 Starting Streamlit Frontend...")
    
    # Option 1: If your streamlit file is in the current directory
    streamlit_file = "your_streamlit_app.py"  # CHANGE THIS TO YOUR ACTUAL FILE NAME
    
    # Option 2: If you want to use the current file (if this is your main app)
    # streamlit_file = __file__.replace('run_all.py', 'your_actual_app_name.py')
    
    # Check if file exists
    if not os.path.exists(streamlit_file):
        print(f"❌ Error: Cannot find {streamlit_file}")
        print("Please update the streamlit_file variable with your actual Streamlit app filename")
        print("Your current directory contains:")
        for file in os.listdir('.'):
            print(f"  - {file}")
        return
    
    subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_file, "--server.port", "8501"])

def run_fastapi():
    """Run FastAPI server"""
    print("🚀 Starting FastAPI Backend...")
    subprocess.run([sys.executable, "-m", "uvicorn", "fastapi_server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

if __name__ == "__main__":
    print("=" * 60)
    print("🎓 Smart Academic Assistant Pro - Starting Services")
    print("=" * 60)
    
    # Check if requirements are installed
    missing_packages = []
    try:
        import fastapi
    except ImportError:
        missing_packages.append("fastapi")
    try:
        import uvicorn
    except ImportError:
        missing_packages.append("uvicorn")
    try:
        from jose import jwt
    except ImportError:
        try:
            import jwt
        except ImportError:
            missing_packages.append("python-jose[cryptography]")
    
    if missing_packages:
        print(f"⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ Packages installed")
    
    # Start FastAPI in a separate thread
    fastapi_thread = threading.Thread(target=run_fastapi, daemon=True)
    fastapi_thread.start()
    
    # Wait for FastAPI to start
    print("⏳ Waiting for FastAPI to start...")
    time.sleep(3)
    
    # Start Streamlit (this will run in main thread)
    run_streamlit()