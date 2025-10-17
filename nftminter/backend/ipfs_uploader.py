"""
IPFS Uploader using Pinata
Handles uploading images and metadata to IPFS
"""

import os
import json
import requests
from pathlib import Path
from typing import Optional, Dict
from dotenv import load_dotenv

load_dotenv()


class IPFSUploader:
    """Handle IPFS uploads using Pinata API"""
    
    def __init__(self, jwt: Optional[str] = None):
        """
        Initialize IPFS uploader with Pinata.
        
        Args:
            jwt: Pinata JWT token. If None, will use PINATA_JWT env var.
        """
        self.jwt = jwt or os.getenv("PINATA_JWT")
        if not self.jwt:
            raise ValueError("PINATA_JWT not found. Please set it in your .env file.")
        
        self.base_url = "https://api.pinata.cloud"
        self.headers = {
            "Authorization": f"Bearer {self.jwt}"
        }
    
    def upload_image(self, image_path: str) -> Dict[str, str]:
        """
        Upload an image to IPFS via Pinata.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            dict: Contains IPFS CID and full URI
        """
        print(f"📤 Uploading image to IPFS (Pinata): {image_path}")
        
        if not Path(image_path).exists():
            raise FileNotFoundError(f"Image not found: {image_path}")
        
        try:
            # Upload the file
            with open(image_path, 'rb') as f:
                files = {
                    'file': f
                }
                response = requests.post(
                    f"{self.base_url}/pinning/pinFileToIPFS",
                    headers=self.headers,
                    files=files
                )
            
            response.raise_for_status()
            data = response.json()
            
            cid = data["IpfsHash"]
            ipfs_uri = f"ipfs://{cid}"
            gateway_url = f"https://gateway.pinata.cloud/ipfs/{cid}"
            
            print(f"✅ Image uploaded to IPFS!")
            print(f"   CID: {cid}")
            print(f"   IPFS URI: {ipfs_uri}")
            print(f"   Gateway URL: {gateway_url}")
            
            return {
                "cid": cid,
                "ipfs_uri": ipfs_uri,
                "gateway_url": gateway_url
            }
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error uploading image to IPFS: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"   Response: {e.response.text}")
            raise Exception(f"IPFS upload failed: {str(e)}")
    
    def upload_metadata(self, metadata: dict, filename: str = "metadata.json") -> Dict[str, str]:
        """
        Upload NFT metadata to IPFS via Pinata.
        
        Args:
            metadata: NFT metadata dictionary
            filename: Name for the metadata file
            
        Returns:
            dict: Contains IPFS CID and full URI
        """
        print(f"📤 Uploading metadata to IPFS (Pinata)...")
        
        try:
            # Upload JSON directly using pinJSONToIPFS endpoint
            response = requests.post(
                f"{self.base_url}/pinning/pinJSONToIPFS",
                headers={
                    **self.headers,
                    "Content-Type": "application/json"
                },
                json={
                    "pinataContent": metadata,
                    "pinataMetadata": {
                        "name": filename
                    }
                }
            )
            
            response.raise_for_status()
            data = response.json()
            
            cid = data["IpfsHash"]
            ipfs_uri = f"ipfs://{cid}"
            gateway_url = f"https://gateway.pinata.cloud/ipfs/{cid}"
            
            print(f"✅ Metadata uploaded to IPFS!")
            print(f"   CID: {cid}")
            print(f"   IPFS URI: {ipfs_uri}")
            print(f"   Gateway URL: {gateway_url}")
            
            return {
                "cid": cid,
                "ipfs_uri": ipfs_uri,
                "gateway_url": gateway_url
            }
        
        except requests.exceptions.RequestException as e:
            print(f"❌ Error uploading metadata to IPFS: {str(e)}")
            if hasattr(e.response, 'text'):
                print(f"   Response: {e.response.text}")
            raise Exception(f"IPFS metadata upload failed: {str(e)}")
    
    def upload_nft_complete(self, image_path: str, metadata: dict) -> Dict[str, str]:
        """
        Complete NFT upload: image + metadata with updated image URI.
        
        Args:
            image_path: Path to the NFT image
            metadata: NFT metadata (will be updated with IPFS image URI)
            
        Returns:
            dict: Contains all IPFS URIs and CIDs
        """
        print(f"\n🚀 Starting complete NFT upload to IPFS...")
        
        # Step 1: Upload image
        image_result = self.upload_image(image_path)
        
        # Step 2: Update metadata with IPFS image URI
        metadata["image"] = image_result["ipfs_uri"]
        
        # Step 3: Upload metadata
        metadata_result = self.upload_metadata(metadata)
        
        print(f"\n✅ Complete NFT uploaded to IPFS!")
        
        return {
            "image_cid": image_result["cid"],
            "image_ipfs_uri": image_result["ipfs_uri"],
            "image_gateway_url": image_result["gateway_url"],
            "metadata_cid": metadata_result["cid"],
            "metadata_ipfs_uri": metadata_result["ipfs_uri"],
            "metadata_gateway_url": metadata_result["gateway_url"]
        }


# Standalone function for quick upload
def upload_to_ipfs(image_path: str, metadata: dict, jwt: Optional[str] = None) -> Dict[str, str]:
    """
    Quick function to upload an NFT to IPFS via Pinata.
    
    Args:
        image_path: Path to the image file
        metadata: NFT metadata dictionary
        jwt: Optional Pinata JWT token
        
    Returns:
        dict: IPFS upload results
    """
    uploader = IPFSUploader(jwt=jwt)
    return uploader.upload_nft_complete(image_path, metadata)


# Example usage
if __name__ == "__main__":
    # Test upload (requires PINATA_JWT in .env)
    print("🧪 Testing IPFS uploader with Pinata...")
    
    # You would normally have these from generateNft.py
    test_image = "generated_nfts/images/test_image.png"
    test_metadata = {
        "name": "Test NFT",
        "description": "Testing IPFS upload with Pinata",
        "image": "placeholder",  # Will be replaced with IPFS URI
        "attributes": []
    }
    
    try:
        uploader = IPFSUploader()
        result = uploader.upload_nft_complete(test_image, test_metadata)
        print(f"\n✅ Test successful!")
        print(f"Use this URI for minting: {result['metadata_ipfs_uri']}")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
