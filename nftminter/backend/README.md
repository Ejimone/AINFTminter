# AI NFT Minter Backend

FastAPI backend for generating AI-powered NFT images using Google's Imagen model.

## Features

- 🎨 **AI Image Generation**: Uses Google Imagen 3.0 to create unique artwork
- 📦 **NFT Metadata**: Automatically generates OpenSea-compatible metadata
- 🚀 **REST API**: Easy-to-use endpoints for frontend integration
- 🔄 **Batch Generation**: Generate multiple NFTs at once
- 📊 **Auto-save**: Images and metadata automatically saved locally

## Setup

### 1. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Configure API Key

Get your Google AI API key from: https://aistudio.google.com/app/apikey

Create a `.env` file:

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 3. Run the Server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs (Interactive Swagger UI)
- **Health**: http://localhost:8000/health

## API Endpoints

### Generate Single NFT

```bash
POST /api/v1/generate-nft
```

Request body:

```json
{
  "prompt": "A mystical dragon flying over a cyberpunk city at sunset",
  "name": "Cyber Dragon #1",
  "description": "A unique AI-generated artwork"
}
```

Response:

```json
{
  "success": true,
  "message": "NFT generated successfully",
  "image_path": "generated_nfts/images/nft_20241017_123456_abc12345.png",
  "metadata_path": "generated_nfts/metadata/nft_20241017_123456_abc12345.json",
  "metadata": {
    "name": "Cyber Dragon #1",
    "description": "A unique AI-generated artwork",
    "image": "generated_nfts/images/...",
    "attributes": [...]
  },
  "prompt": "A mystical dragon...",
  "filename": "nft_20241017_123456_abc12345"
}
```

### Generate Batch

```bash
POST /api/v1/generate-batch
```

Request body:

```json
{
  "prompts": [
    "A futuristic city at night",
    "An abstract landscape in purple tones",
    "A cosmic galaxy with stars"
  ]
}
```

### Health Check

```bash
GET /health
```

## Direct Script Usage

You can also use the generator directly without the API:

```python
from generateNft import generate_nft_from_prompt

result = generate_nft_from_prompt(
    prompt="A beautiful sunset over mountains"
)

print(f"Image saved to: {result['image_path']}")
```

## File Structure

```
backend/
├── main.py              # FastAPI server
├── generateNft.py       # NFT generation logic
├── requirements.txt     # Python dependencies
├── .env.example         # Environment variables template
└── generated_nfts/      # Output directory (auto-created)
    ├── images/          # Generated images
    └── metadata/        # NFT metadata JSON files
```

## Generated Files

Each NFT generation creates two files:

1. **Image**: `generated_nfts/images/nft_[timestamp]_[hash].png`
2. **Metadata**: `generated_nfts/metadata/nft_[timestamp]_[hash].json`

### Metadata Format (OpenSea Compatible)

```json
{
  "name": "AI Generated NFT",
  "description": "AI-generated artwork from prompt",
  "image": "ipfs://...",
  "prompt": "Original generation prompt",
  "attributes": [
    {
      "trait_type": "Generation Method",
      "value": "Google Imagen 3.0"
    },
    {
      "trait_type": "Aspect Ratio",
      "value": "1:1"
    }
  ]
}
```

## IPFS Integration (Coming Soon)

The backend includes methods to update metadata with IPFS URIs after uploading to IPFS:

```python
generator.update_metadata_with_ipfs(
    metadata_path="path/to/metadata.json",
    ipfs_image_uri="ipfs://Qm...",
)
```

## Example cURL Requests

Generate NFT:

```bash
curl -X POST "http://localhost:8000/api/v1/generate-nft" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A beautiful landscape with mountains and rivers",
    "name": "Mountain Vista #1"
  }'
```

Health check:

```bash
curl http://localhost:8000/health
```

## Troubleshooting

### "GOOGLE_API_KEY not found"

- Make sure you have a `.env` file with `GOOGLE_API_KEY` set
- Verify the API key is valid at https://aistudio.google.com/

### Image generation fails

- Check your API quota and rate limits
- Ensure the prompt doesn't violate content policies
- Verify internet connection for API calls

### Module import errors

- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Activate your virtual environment if using one

## Next Steps

1. **Frontend Integration**: Connect a React/Next.js frontend to these APIs
2. **IPFS Upload**: Integrate with Pinata or NFT.Storage for decentralized storage
3. **Blockchain Integration**: Use the generated metadata URIs with the smart contract
4. **Authentication**: Add API key authentication for production use

## Security Notes

⚠️ **Important**:

- Never commit `.env` files with real API keys
- In production, add rate limiting and authentication
- Consider using API gateway for production deployment
- Store IPFS uploads permanently for minted NFTs
