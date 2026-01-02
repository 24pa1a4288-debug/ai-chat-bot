"""
Setup script for MAITRI
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing requirements: {e}")
        return False

def check_dependencies():
    """Check if required dependencies are available"""
    print("Checking dependencies...")
    required = ['cv2', 'numpy', 'tensorflow', 'librosa', 'streamlit']
    missing = []
    
    for dep in required:
        try:
            __import__(dep)
            print(f"✅ {dep} is installed")
        except ImportError:
            print(f"❌ {dep} is missing")
            missing.append(dep)
    
    return len(missing) == 0

if __name__ == "__main__":
    print("="*60)
    print("MAITRI Setup")
    print("="*60)
    
    if install_requirements():
        print("\n" + "="*60)
        print("Checking dependencies...")
        if check_dependencies():
            print("\n✅ Setup completed successfully!")
            print("\nYou can now run:")
            print("  python main.py          # Command-line interface")
            print("  streamlit run app.py    # Web interface")
        else:
            print("\n⚠️  Some dependencies may be missing. Please check the output above.")
    else:
        print("\n❌ Setup failed. Please install requirements manually.")

