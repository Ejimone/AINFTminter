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
from ipfs_uploader import IPFSUploader
from blockchain_minter import BlockchainMinter

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
    image_ipfs_uri: Optional[str] = None
    metadata_ipfs_uri: Optional[str] = None
    error: Optional[str] = None


class BatchGenerateRequest(BaseModel):
    prompts: List[str] = Field(..., description="List of prompts to generate NFTs", min_items=1, max_items=10)


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    api_configured: bool


class MintNFTRequest(BaseModel):
    prompt: str = Field(..., description="Text prompt to generate NFT image", min_length=3)
    name: str = Field(..., description="Name for the NFT")
    description: Optional[str] = Field(None, description="Optional description")
    recipient_address: Optional[str] = Field(None, description="Recipient address (defaults to minter)")
    network: str = Field("sepolia", description="Blockchain network (sepolia, ganache-local)")


class MintNFTResponse(BaseModel):
    success: bool
    message: str
    token_id: Optional[int] = None
    transaction_hash: Optional[str] = None
    image_ipfs_uri: Optional[str] = None
    metadata_ipfs_uri: Optional[str] = None
    explorer_url: Optional[str] = None
    contract_address: Optional[str] = None
    error: Optional[str] = None


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

# Initialize IPFS Uploader (optional, will check on use)
try:
    ipfs_uploader = IPFSUploader()
    print("✅ IPFS Uploader initialized (Pinata)")
except ValueError as e:
    print(f"⚠️  Warning: {e}")
    print("IPFS uploads will fail without PINATA_JWT")
    ipfs_uploader = None

# Initialize Blockchain Minter (optional, will check on use)
try:
    contract_address = os.getenv("CONTRACT_ADDRESS")
    if contract_address:
        blockchain_minter = BlockchainMinter()
        print(f"✅ Blockchain Minter initialized (Contract: {contract_address})")
    else:
        blockchain_minter = None
        print("⚠️  Warning: CONTRACT_ADDRESS not set. Minting will fail without it.")
except ValueError as e:
    print(f"⚠️  Warning: {e}")
    blockchain_minter = None


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
    Generate a single NFT from a text prompt and upload to IPFS.
    
    This endpoint uses Google's Imagen model to create unique AI-generated artwork
    and uploads both image and metadata to IPFS for decentralized storage.
    """
    if not nft_generator:
        raise HTTPException(
            status_code=503,
            detail="NFT Generator not initialized. Please configure GOOGLE_API_KEY."
        )
    
    if not ipfs_uploader:
        raise HTTPException(
            status_code=503,
            detail="IPFS Uploader not initialized. Please configure PINATA_JWT."
        )
    
    try:
        print(f"\n🎨 Generating NFT from prompt: {request.prompt}")
        
        # Step 1: Generate the NFT image
        result = nft_generator.generate_image(
            prompt=request.prompt,
            output_filename=request.name.replace(" ", "_").lower() if request.name else None
        )
        
        if not result["success"]:
            raise HTTPException(status_code=500, detail=result.get("error", "Generation failed"))
        
        # Step 2: Update metadata with custom name/description
        metadata = result["metadata"]
        if request.name:
            metadata["name"] = request.name
        if request.description:
            metadata["description"] = request.description
        
        print(f"✅ Image generated: {result['image_path']}")
        
        # Step 3: Upload to IPFS
        print("📤 Uploading to IPFS...")
        ipfs_result = ipfs_uploader.upload_nft_complete(
            image_path=result["image_path"],
            metadata=metadata
        )
        
        print(f"✅ Uploaded to IPFS:")
        print(f"   Image: {ipfs_result['image_ipfs_uri']}")
        print(f"   Metadata: {ipfs_result['metadata_ipfs_uri']}")
        
        return GenerateNFTResponse(
            success=True,
            message="NFT generated and uploaded to IPFS successfully",
            image_path=result["image_path"],
            metadata_path=result["metadata_path"],
            metadata=metadata,
            prompt=result["prompt"],
            filename=result["filename"],
            image_ipfs_uri=ipfs_result["image_ipfs_uri"],
            metadata_ipfs_uri=ipfs_result["metadata_ipfs_uri"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error generating NFT: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error generating NFT: {str(e)}")


@app.post("/api/v1/generate-batch", response_model=dict)
async def generate_batch(request: BatchGenerateRequest, background_tasks: BackgroundTasks):
    """
    Generate multiple NFTs from a list of prompts and upload to IPFS.
    
    This is useful for creating NFT collections. Limited to 10 prompts per request.
    Each generated image is uploaded to IPFS for decentralized storage.
    """
    if not nft_generator:
        raise HTTPException(
            status_code=503,
            detail="NFT Generator not initialized. Please configure GOOGLE_API_KEY."
        )
    
    if not ipfs_uploader:
        raise HTTPException(
            status_code=503,
            detail="IPFS Uploader not initialized. Please configure PINATA_JWT."
        )
    
    try:
        print(f"\n🎨 Starting batch generation for {len(request.prompts)} prompts...")
        
        # Generate all images locally first
        results = nft_generator.generate_batch(request.prompts)
        
        # Process each successful result to upload to IPFS
        for i, result in enumerate(results):
            if result.get("success"):
                try:
                    print(f"📤 Uploading image {i+1}/{len(results)} to IPFS...")
                    
                    # Upload to IPFS
                    ipfs_result = ipfs_uploader.upload_nft_complete(
                        image_path=result["image_path"],
                        metadata=result["metadata"]
                    )
                    
                    # Add IPFS URIs to the result
                    result["ipfs_uri"] = ipfs_result["image_ipfs_uri"]
                    result["image_ipfs_uri"] = ipfs_result["image_ipfs_uri"]
                    result["metadata_ipfs_uri"] = ipfs_result["metadata_ipfs_uri"]
                    result["status"] = "success"  # Ensure status is set correctly
                    
                    print(f"✅ Image {i+1} uploaded: {ipfs_result['image_ipfs_uri']}")
                    
                except Exception as e:
                    print(f"❌ Failed to upload image {i+1} to IPFS: {str(e)}")
                    result["success"] = False
                    result["status"] = "error"
                    result["error"] = f"IPFS upload failed: {str(e)}"
            else:
                result["status"] = "error"  # Ensure failed generations have error status
        
        successful = [r for r in results if r.get("success") and r.get("status") == "success"]
        failed = [r for r in results if not r.get("success") or r.get("status") == "error"]
        
        print(f"✅ Batch generation complete: {len(successful)} succeeded, {len(failed)} failed")
        
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


@app.post("/api/v1/mint-nft", response_model=MintNFTResponse)
async def mint_nft_complete(request: MintNFTRequest):
    """
    Complete end-to-end NFT minting: Generate → Upload to IPFS → Mint on Blockchain.
    
    This endpoint:
    1. Generates an AI image from the prompt
    2. Uploads the image to IPFS
    3. Creates and uploads metadata to IPFS
    4. Mints the NFT on the blockchain
    
    Returns the minted token ID and transaction details.
    """
    # Check all services are initialized
    if not nft_generator:
        raise HTTPException(
            status_code=503,
            detail="NFT Generator not initialized. Please configure GOOGLE_API_KEY."
        )
    
    if not ipfs_uploader:
        raise HTTPException(
            status_code=503,
            detail="IPFS Uploader not initialized. Please configure PINATA_JWT."
        )
    
    # Check if contract address is configured
    contract_address = os.getenv("CONTRACT_ADDRESS")
    if not contract_address:
        raise HTTPException(
            status_code=503,
            detail="Blockchain Minter not initialized. Please configure CONTRACT_ADDRESS and PRIVATE_KEY."
        )
    
    try:
        print(f"\n🚀 Starting complete NFT minting process...")
        print(f"📝 Prompt: {request.prompt}")
        
        # Step 1: Generate the AI image
        print("\n[1/4] Generating AI image...")
        generation_result = nft_generator.generate_image(
            prompt=request.prompt,
            output_filename=request.name.replace(" ", "_").lower() if request.name else None
        )
        
        if not generation_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Image generation failed: {generation_result.get('error')}"
            )
        
        # Update metadata with custom name/description
        metadata = generation_result["metadata"]
        metadata["name"] = request.name
        if request.description:
            metadata["description"] = request.description
        
        print(f"✅ Image generated: {generation_result['image_path']}")
        
        # Step 2: Upload to IPFS
        print("\n[2/4] Uploading to IPFS...")
        ipfs_result = ipfs_uploader.upload_nft_complete(
            image_path=generation_result["image_path"],
            metadata=metadata
        )
        
        print(f"✅ Uploaded to IPFS:")
        print(f"   Image: {ipfs_result['image_ipfs_uri']}")
        print(f"   Metadata: {ipfs_result['metadata_ipfs_uri']}")
        
        # Step 3: Mint on blockchain
        print("\n[3/4] Minting on blockchain...")
        
        # Set recipient address
        recipient = request.recipient_address
        if not recipient or recipient == "string" or not recipient.startswith('0x') or len(recipient) != 42:
            # Use minter's address as recipient if not specified or invalid
            from eth_account import Account
            private_key = os.getenv("PRIVATE_KEY")
            if not private_key.startswith('0x'):
                private_key = '0x' + private_key
            account = Account.from_key(private_key)
            recipient = account.address
            print(f"Using minter address as recipient: {recipient}")
        else:
            print(f"Using provided recipient address: {recipient}")
        
        # Create blockchain minter for this request (supports different networks)
        minter = BlockchainMinter()
        
        mint_result = minter.mint_nft(
            recipient_address=recipient,
            token_uri=ipfs_result["metadata_ipfs_uri"]
        )
        
        if not mint_result["success"]:
            raise HTTPException(
                status_code=500,
                detail=f"Blockchain minting failed: {mint_result.get('error')}"
            )
        
        print(f"✅ Minted on blockchain:")
        print(f"   Token ID: {mint_result['token_id']}")
        print(f"   Transaction: {mint_result['transaction_hash']}")
        
        # Step 4: Return complete result
        print("\n[4/4] Complete! NFT successfully minted! 🎉")
        
        return MintNFTResponse(
            success=True,
            message=f"NFT '{request.name}' minted successfully!",
            token_id=mint_result["token_id"],
            transaction_hash=mint_result["transaction_hash"],
            image_ipfs_uri=ipfs_result["image_ipfs_uri"],
            metadata_ipfs_uri=ipfs_result["metadata_ipfs_uri"],
            explorer_url=mint_result.get("explorer_url"),
            contract_address=mint_result["contract_address"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"\n❌ Error in complete minting process: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Minting process failed: {str(e)}"
        )


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