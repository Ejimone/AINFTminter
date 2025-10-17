"""
Test script for NFT Generator
Run this to verify your setup is working correctly
"""

import os
from pathlib import Path

print("🧪 Testing AI NFT Generator Setup\n")
print("=" * 50)

# Check 1: Python version
print("\n✓ Python version check...")
import sys
print(f"  Python {sys.version}")

# Check 2: Required modules
print("\n✓ Checking required modules...")
modules_to_check = [
    ("fastapi", "FastAPI"),
    ("uvicorn", "Uvicorn"),
    ("pydantic", "Pydantic"),
    ("google.genai", "Google GenAI"),
    ("dotenv", "python-dotenv"),
]

all_installed = True
for module, name in modules_to_check:
    try:
        __import__(module)
        print(f"  ✓ {name}")
    except ImportError as e:
        print(f"  ✗ {name} - NOT INSTALLED")
        all_installed = False

# Check 3: Environment variables
print("\n✓ Checking environment variables...")
env_file = Path(".env")
if env_file.exists():
    print(f"  ✓ .env file found")
    from dotenv import load_dotenv
    load_dotenv()
    
    if os.getenv("GOOGLE_API_KEY"):
        key = os.getenv("GOOGLE_API_KEY")
        masked_key = f"{key[:10]}...{key[-4:]}" if len(key) > 14 else f"{key[:6]}..."
        print(f"  ✓ GOOGLE_API_KEY configured ({masked_key})")
    else:
        print(f"  ⚠️  GOOGLE_API_KEY not set in .env")
        print(f"     Add: GOOGLE_API_KEY=your_api_key_here")
else:
    print(f"  ⚠️  .env file not found")
    print(f"     Copy .env.example to .env and add your API key")

# Check 4: Output directories
print("\n✓ Checking output directories...")
output_dir = Path("generated_nfts")
if output_dir.exists():
    print(f"  ✓ generated_nfts directory exists")
else:
    print(f"  ℹ️  generated_nfts will be created on first run")

print("\n" + "=" * 50)
print("\n🎯 Setup Summary:")

if env_file.exists() and os.getenv("GOOGLE_API_KEY") and all_installed:
    print("✅ All set! You're ready to generate NFTs.")
    print("\nNext steps:")
    print("  1. Start the API server: python main.py")
    print("  2. Or test generation: python test_setup.py --generate")
    print("  3. Visit docs: http://localhost:8000/docs")
else:
    print("⚠️  Setup incomplete. Please:")
    if not all_installed:
        print("  1. Install dependencies: pip install -r requirements.txt")
    if not env_file.exists() or not os.getenv("GOOGLE_API_KEY"):
        print("  2. Copy .env.example to .env")
        print("  3. Add your GOOGLE_API_KEY from https://aistudio.google.com/app/apikey")
    print("  4. Run this test again")

print("\n" + "=" * 50)

# Optional: Test generation if --generate flag is passed
if len(sys.argv) > 1 and sys.argv[1] == "--generate":
    print("\n🎨 Testing image generation...")
    
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Cannot test generation without GOOGLE_API_KEY")
        sys.exit(1)
    
    try:
        from generateNft import generate_nft_from_prompt
        
        print("Generating test NFT (this may take 10-30 seconds)...")
        result = generate_nft_from_prompt(
            prompt="A small cute robot painting on a canvas, digital art style"
        )
        
        if result["success"]:
            print(f"\n✅ Test NFT generated successfully!")
            print(f"   Image: {result['image_path']}")
            print(f"   Metadata: {result['metadata_path']}")
        else:
            print(f"\n❌ Generation failed: {result.get('error')}")
    
    except Exception as e:
        print(f"\n❌ Error during test generation: {e}")
        import traceback
        traceback.print_exc()
