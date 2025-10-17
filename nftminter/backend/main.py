"""
FastAPI Backend for AI-Powered NFT Minter
Provides REST API endpoints for generating and minting NFTs
"""

import os
from typing import Optional, List
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from generateNft import NFTGenerator, generate_nft_from_prompt

# Load environment variables from .env file
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)
print(f"🔧 Loading environment from: {env_path}")
print(f"🔑 GOOGLE_API_KEY found: {'Yes' if os.getenv('GOOGLE_API_KEY') else 'No'}")


# Pydantic models for request/response
class GenerateNFTRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt to generate NFT image", min_length=3)
    name: Optional[str] = Field(None, description="Optional custom name for the NFT")
    description: Optional[str] = Field(None, description="Optional custom description")


class GenerateNFTResponse(BaseModel):
    success: bool
    message: str
    image_path: Optional[str] = None
    metadata_path: Optional[str] = None
    metadata: Optional[dict] = None
    prompt: str
    filename: Optional[str] = None
    error: Optional[str] = None


class BatchGenerateRequest(BaseModel):
    prompts: List[str] = Field(..., description="List of prompts to generate NFTs", min_items=1, max_items=10)


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    api_configured: bool


# Initialize FastAPI app
app = FastAPI(
    title="AI NFT Minter API",
    description="Generate AI-powered NFT images and metadata",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize NFT Generator
try:
    nft_generator = NFTGenerator()
    print("✅ AI NFT Generator initialized successfully")
    print("🎨 Using Gemini 2.5 Flash Image model for real AI generation")
except ValueError as e:
    print(f"⚠️  Warning: {e}")
    print("API will run but generation will fail without GOOGLE_API_KEY")
    nft_generator = None


@app.get("/", response_model=dict)
async def root():
    """Root endpoint with API information"""
    return {
        "name": "AI NFT Minter API",
        "version": "1.0.0",
        "description": "Generate AI-powered NFT images using Google Gemini 2.5 Flash Image",
        "model": "gemini-2.5-flash-image",
        "endpoints": {
            "health": "/health",
            "generate": "/api/v1/generate-nft",
            "batch_generate": "/api/v1/generate-batch",
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "api_configured": nft_generator is not None
    }


@app.post("/api/v1/generate-nft", response_model=GenerateNFTResponse)
async def generate_nft(request: GenerateNFTRequest):
    """
    Generate a single NFT from a text prompt.
    
    This endpoint uses Google's Imagen model to create unique AI-generated artwork
    that can be minted as an NFT on the blockchain.
    """
    if not nft_generator:
        raise HTTPException(
            status_code=503,
            detail="NFT Generator not initialized. Please configure GOOGLE_API_KEY."
        )
    
    try:
        # Generate the NFT
        result = nft_generator.generate_image(
            prompt=request.prompt,
            output_filename=request.name.replace(" ", "_").lower() if request.name else None
        )
        
        if result["success"]:
            # If custom description provided, update metadata
            if request.description:
                result["metadata"]["description"] = request.description
            
            if request.name:
                result["metadata"]["name"] = request.name
            
            return GenerateNFTResponse(
                success=True,
                message="NFT generated successfully",
                image_path=result["image_path"],
                metadata_path=result["metadata_path"],
                metadata=result["metadata"],
                prompt=result["prompt"],
                filename=result["filename"]
            )
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Generation failed"))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating NFT: {str(e)}")


@app.post("/api/v1/generate-batch", response_model=dict)
async def generate_batch(request: BatchGenerateRequest, background_tasks: BackgroundTasks):
    """
    Generate multiple NFTs from a list of prompts.
    
    This is useful for creating NFT collections. Limited to 10 prompts per request.
    """
    if not nft_generator:
        raise HTTPException(
            status_code=503,
            detail="NFT Generator not initialized. Please configure GOOGLE_API_KEY."
        )
    
    try:
        results = nft_generator.generate_batch(request.prompts)
        
        successful = [r for r in results if r.get("success")]
        failed = [r for r in results if not r.get("success")]
        
        return {
            "success": True,
            "message": f"Batch generation complete. {len(successful)} succeeded, {len(failed)} failed.",
            "total": len(results),
            "successful": len(successful),
            "failed": len(failed),
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in batch generation: {str(e)}")


@app.get("/api/v1/image/{filename}")
async def get_image(filename: str):
    """
    Retrieve a generated image by filename.
    """
    image_path = nft_generator.images_dir / filename
    
    if not image_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    
    return FileResponse(image_path)


@app.get("/api/v1/metadata/{filename}")
async def get_metadata(filename: str):
    """
    Retrieve NFT metadata by filename.
    """
    # Support both .json and without extension
    metadata_path = nft_generator.metadata_dir / filename
    if not filename.endswith('.json'):
        metadata_path = nft_generator.metadata_dir / f"{filename}.json"
    
    if not metadata_path.exists():
        raise HTTPException(status_code=404, detail="Metadata not found")
    
    return FileResponse(metadata_path)


# For development/testing
if __name__ == "__main__":
    import uvicorn
    
    print("🚀 Starting AI NFT Minter API...")
    print("📝 API Documentation: http://localhost:8000/docs")
    print("🏥 Health Check: http://localhost:8000/health")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )