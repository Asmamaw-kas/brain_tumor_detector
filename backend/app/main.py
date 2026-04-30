from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback
from .utils import preprocess_image
from .model import model

# Initialize FastAPI app
app = FastAPI(
    title="Brain Tumor Detection API",
    description="API for detecting brain tumors from MRI images",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Brain Tumor Detection API",
        "status": "active",
        "endpoints": {
            "predict": "/predict (POST) - Upload an image for prediction",
            "health": "/health (GET) - Check API health"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model.model is not None
    }

@app.post("/predict")
async def predict_tumor(file: UploadFile = File(...)):
    """
    Predict whether an MRI image contains a brain tumor
    
    - **file**: Upload an image file (JPEG, PNG, etc.)
    """
    try:
        # Validate file type
        if not file.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400,
                detail="File must be an image (JPEG, PNG, etc.)"
            )
        
        # Read image bytes
        image_bytes = await file.read()
        
        # Validate file size (max 10MB)
        if len(image_bytes) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=400,
                detail="File size should be less than 10MB"
            )
        
        # Preprocess the image
        processed_image = preprocess_image(image_bytes)
        
        # Get prediction
        result = model.predict(processed_image)
        
        # Return result
        return JSONResponse(
            content={
                "success": True,
                "filename": file.filename,
                "result": result
            },
            status_code=200
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during prediction: {str(e)}"
        )

# Optional: Add startup event
@app.on_event("startup")
async def startup_event():
    print("🚀 Brain Tumor Detection API is starting up...")
    print(f"📊 Model loaded successfully: {model.model is not None}")

@app.on_event("shutdown")
async def shutdown_event():
    print("👋 Shutting down Brain Tumor Detection API...")