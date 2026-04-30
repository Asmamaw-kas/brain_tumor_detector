import uvicorn
import os
import sys
# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

if __name__== "__main__":
    print("🧠 Starting Brain Tumor Detection Server...")
    print("📡 Server will run at: http://localhost:8000")
    print("📚 API Docs at: http://localhost:8000/docs")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )