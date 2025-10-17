"""
AI-Powered NFT Generator
Generates images using Google's Gemini 2.5 Flash Image model
"""

import os
import json
import hashlib
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()


class NFTGenerator:
    """Handle AI image generation and NFT metadata creation"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the NFT Generator with Google Gemini AI.
        
        Args:
            api_key: Google AI API key. If None, will use GOOGLE_API_KEY env var.
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found. Please set it in your .env file.")
        
        # Initialize the Gemini client
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash-image"

        
        # Create directories for storing generated content
        self.output_dir = Path("generated_nfts")
        self.images_dir = self.output_dir / "images"
        self.metadata_dir = self.output_dir / "metadata"
        
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_image(self, prompt: str, output_filename: Optional[str] = None) -> dict:
        """
        Generate an image using Google's Gemini 2.5 Flash Image model.
        
        Args:
            prompt: Text description of the image to generate
            output_filename: Optional custom filename (without extension)
            
        Returns:
            dict: Contains image path, metadata, and generation info
        """
        print(f"🎨 Generating NFT image from prompt: '{prompt}'")
        
        try:
            # Create filename
            if not output_filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                prompt_hash = hashlib.md5(prompt.encode()).hexdigest()[:8]
                output_filename = f"nft_{timestamp}_{prompt_hash}"
            
            # Enhance prompt to ensure image generation
            enhanced_prompt = f"Create a detailed, high-quality digital artwork image of: {prompt}. Style: digital art, vibrant colors, professional NFT artwork."
            
            # Prepare the content for Gemini
            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(text=enhanced_prompt),
                    ],
                ),
            ]
            
            # Configure to generate images
            generate_content_config = types.GenerateContentConfig(
                response_modalities=["IMAGE"],  # Only request IMAGE, not TEXT
                temperature=1.0,
            )
            
            # Generate the image
            print("⏳ Generating image with AI (this may take 10-30 seconds)...")
            image_data = None
            mime_type = None
            
            for chunk in self.client.models.generate_content_stream(
                model=self.model,
                contents=contents,
                config=generate_content_config,
            ):
                if (
                    chunk.candidates is None
                    or chunk.candidates[0].content is None
                    or chunk.candidates[0].content.parts is None
                ):
                    continue
                
                # Check if we have image data
                if (chunk.candidates[0].content.parts[0].inline_data and 
                    chunk.candidates[0].content.parts[0].inline_data.data):
                    inline_data = chunk.candidates[0].content.parts[0].inline_data
                    image_data = inline_data.data
                    mime_type = inline_data.mime_type
                    print("✅ Image data received from AI!")
                    break
                elif chunk.text:
                    # Skip text responses
                    print(f"💭 AI says: {chunk.text}")
            
            if not image_data:
                raise Exception("No image data received from Gemini API. The prompt might be too vague or inappropriate. Try a more descriptive prompt like 'A golden Bitcoin coin floating in space with stars'.")
            
            # Determine file extension from mime type
            file_extension = mimetypes.guess_extension(mime_type) or ".png"
            image_path = self.images_dir / f"{output_filename}{file_extension}"
            
            # Save the image
            with open(image_path, "wb") as f:
                f.write(image_data)
            
            print(f"✅ Image generated successfully: {image_path}")
            
            # Create metadata
            metadata = self.create_metadata(
                name=f"AI Generated NFT - {output_filename}",
                description=f"AI-generated artwork created from prompt: '{prompt}'",
                image_path=str(image_path),
                prompt=prompt,
                attributes=[
                    {"trait_type": "Generation Method", "value": "Gemini 2.5 Flash Image"},
                    {"trait_type": "Created", "value": datetime.now().isoformat()},
                ]
            )
            
            # Save metadata
            metadata_path = self.metadata_dir / f"{output_filename}.json"
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            print(f"✅ Metadata saved: {metadata_path}")
            
            return {
                "success": True,
                "image_path": str(image_path),
                "metadata_path": str(metadata_path),
                "metadata": metadata,
                "prompt": prompt,
                "filename": output_filename
            }
            
        except Exception as e:
            print(f"❌ Error generating image: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "prompt": prompt
            }
    
    def create_metadata(
        self,
        name: str,
        description: str,
        image_path: str,
        prompt: str,
        attributes: Optional[list] = None,
        external_url: Optional[str] = None
    ) -> dict:
        """
        Create NFT metadata following OpenSea standards.
        
        Args:
            name: NFT name
            description: NFT description
            image_path: Path to the image file
            prompt: Original prompt used to generate the image
            attributes: List of trait dictionaries
            external_url: Optional external URL
            
        Returns:
            dict: NFT metadata in OpenSea format
        """
        metadata = {
            "name": name,
            "description": description,
            "image": image_path,  # Will be replaced with IPFS URI after upload
            "prompt": prompt,
            "attributes": attributes or [],
        }
        
        if external_url:
            metadata["external_url"] = external_url
        
        return metadata
    
    def generate_batch(self, prompts: list[str]) -> list[dict]:
        """
        Generate multiple NFTs from a list of prompts.
        
        Args:
            prompts: List of text prompts
            
        Returns:
            list: Results for each generation
        """
        results = []
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n📦 Generating NFT {i}/{len(prompts)}")
            result = self.generate_image(prompt)
            results.append(result)
        
        print(f"\n✅ Batch generation complete! {len(results)} NFTs generated.")
        return results
    
    def update_metadata_with_ipfs(self, metadata_path: str, ipfs_image_uri: str, ipfs_metadata_uri: Optional[str] = None) -> dict:
        """
        Update metadata file with IPFS URIs after uploading to IPFS.
        
        Args:
            metadata_path: Path to the metadata JSON file
            ipfs_image_uri: IPFS URI for the image (e.g., ipfs://Qm...)
            ipfs_metadata_uri: Optional IPFS URI for the metadata itself
            
        Returns:
            dict: Updated metadata
        """
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        # Update image URI to IPFS
        metadata["image"] = ipfs_image_uri
        
        if ipfs_metadata_uri:
            metadata["metadata_uri"] = ipfs_metadata_uri
        
        # Save updated metadata
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Updated metadata with IPFS URI: {metadata_path}")
        return metadata


# Standalone function for quick generation
def generate_nft_from_prompt(prompt: str, api_key: Optional[str] = None) -> dict:
    """
    Quick function to generate a single NFT from a prompt.
    
    Args:
        prompt: Text description of the desired image
        api_key: Optional Google AI API key
        
    Returns:
        dict: Generation results including paths and metadata
    """
    generator = NFTGenerator(api_key=api_key)
    return generator.generate_image(prompt)


# Example usage
if __name__ == "__main__":
    # Example: Generate a single NFT
    result = generate_nft_from_prompt(
        prompt="A mystical dragon flying over a cyberpunk city at sunset, digital art, vibrant colors"
    )
    
    if result["success"]:
        print(f"\n🎉 NFT Generated Successfully!")
        print(f"Image: {result['image_path']}")
        print(f"Metadata: {result['metadata_path']}")
    else:
        print(f"\n❌ Generation failed: {result['error']}")




