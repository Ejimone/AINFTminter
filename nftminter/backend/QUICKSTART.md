# AI NFT Generator - Quick Start Guide

## ✅ Setup Complete!

Your AI-powered NFT generation backend is now fully configured and ready to use!

## 🎯 What's Been Implemented

### Core Features

- ✅ **AI Image Generation**: Uses Google Imagen 3.0 to create unique artwork
- ✅ **NFT Metadata**: Automatically generates OpenSea-compatible metadata
- ✅ **FastAPI Server**: REST API with interactive documentation
- ✅ **Batch Processing**: Generate multiple NFTs at once
- ✅ **Auto-save**: All images and metadata saved locally

### Files Created

```
backend/
├── generateNft.py       # NFT generation logic with AI
├── main.py              # FastAPI server with endpoints
├── requirements.txt     # Python dependencies
├── .env                 # Your API keys (configured ✅)
├── .env.example         # Template for others
├── .gitignore           # Protect sensitive files
├── start_server.sh      # Quick server start script
├── test_setup.py        # Setup verification
├── test_api.py          # API testing script
└── README.md            # Full documentation
```

## 🚀 How to Use

### Option 1: Start the API Server

```bash
cd backend
python main.py
```

Or use the start script:

```bash
cd backend
./start_server.sh
```

The server will be available at:

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs (Use this!)
- **Health Check**: http://localhost:8000/health

### Option 2: Direct Script Usage

```python
from generateNft import generate_nft_from_prompt

result = generate_nft_from_prompt(
    prompt="A mystical dragon flying over a cyberpunk city at sunset"
)

print(f"Image: {result['image_path']}")
print(f"Metadata: {result['metadata_path']}")
```

## 📝 API Examples

### Generate a Single NFT

**Using curl:**

```bash
curl -X POST "http://localhost:8000/api/v1/generate-nft" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic city with flying cars, neon lights, digital art",
    "name": "Cyberpunk City #1",
    "description": "A unique AI-generated cyberpunk cityscape"
  }'
```

**Using Python:**

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/generate-nft",
    json={
        "prompt": "A beautiful landscape with mountains and aurora",
        "name": "Aurora Vista #1"
    }
)

result = response.json()
print(result)
```

**Using the Interactive Docs (Easiest!):**

1. Start the server
2. Open http://localhost:8000/docs
3. Click on `/api/v1/generate-nft`
4. Click "Try it out"
5. Fill in the prompt
6. Click "Execute"

### Generate Multiple NFTs (Batch)

```bash
curl -X POST "http://localhost:8000/api/v1/generate-batch" \
  -H "Content-Type: application/json" \
  -d '{
    "prompts": [
      "A futuristic robot in a garden",
      "An abstract cosmic landscape",
      "A minimalist mountain scene"
    ]
  }'
```

## 🎨 Example Prompts

Try these prompts for great results:

1. **Fantasy**: "A magical forest with glowing mushrooms and fireflies, ethereal lighting"
2. **Sci-Fi**: "A space station orbiting a purple planet, detailed, cinematic"
3. **Abstract**: "Swirling colors representing emotions, abstract expressionism"
4. **Nature**: "A serene Japanese garden with cherry blossoms, peaceful atmosphere"
5. **Cyberpunk**: "Neon-lit street in a futuristic Tokyo, rain-soaked, night scene"
6. **Minimalist**: "Simple geometric shapes in pastel colors, clean design"

## 📂 Output Structure

Generated files are saved in `generated_nfts/`:

```
generated_nfts/
├── images/
│   └── nft_20241017_123456_abc12345.png
└── metadata/
    └── nft_20241017_123456_abc12345.json
```

### Metadata Format (OpenSea Compatible)

```json
{
  "name": "AI Generated NFT - nft_20241017_123456",
  "description": "AI-generated artwork created from prompt: '...'",
  "image": "generated_nfts/images/nft_20241017_123456_abc12345.png",
  "prompt": "Your original prompt",
  "attributes": [
    {
      "trait_type": "Generation Method",
      "value": "Google Imagen 3.0"
    },
    {
      "trait_type": "Aspect Ratio",
      "value": "1:1"
    },
    {
      "trait_type": "Created",
      "value": "2024-10-17T12:34:56"
    }
  ]
}
```

## 🔗 Integration with Smart Contract

After generating an NFT:

1. **Upload to IPFS** (you'll need to implement this or use a service)
2. **Get IPFS URI**: `ipfs://Qm...`
3. **Mint NFT** using your smart contract:

```python
from brownie import AINFTMinter, accounts

minter = AINFTMinter.at("your_contract_address")
recipient = accounts[0].address
token_uri = "ipfs://Qm...YourMetadataHash"

tx = minter.mintNFT(recipient, token_uri, {"from": accounts[0]})
token_id = tx.return_value
print(f"Minted NFT #{token_id}")
```

## 🧪 Testing

### Test Setup

```bash
cd backend
python test_setup.py
```

### Test API (server must be running)

```bash
cd backend
python test_api.py
```

### Test Generation (generates a real NFT)

```bash
cd backend
python test_setup.py --generate
```

## 🛠️ Troubleshooting

### "GOOGLE_API_KEY not found"

**Fixed!** The `.env` file is now properly loaded. If you still see this:

1. Check `.env` exists in the `backend/` folder
2. Verify `GOOGLE_API_KEY` is set in `.env`
3. Restart the server

### API Key Issues

- Get your key from: https://aistudio.google.com/app/apikey
- Make sure there are no quotes around the value in `.env`
- Example: `GOOGLE_API_KEY=AIzaSy...` (no quotes)

### Generation Fails

- Check API quota/rate limits
- Verify prompt doesn't violate content policies
- Ensure good internet connection

### Module Import Errors

```bash
pip install -r requirements.txt
```

## 📊 API Endpoints Reference

| Endpoint                      | Method | Description              |
| ----------------------------- | ------ | ------------------------ |
| `/`                           | GET    | API information          |
| `/health`                     | GET    | Health check             |
| `/api/v1/generate-nft`        | POST   | Generate single NFT      |
| `/api/v1/generate-batch`      | POST   | Generate multiple NFTs   |
| `/api/v1/image/{filename}`    | GET    | Retrieve generated image |
| `/api/v1/metadata/{filename}` | GET    | Retrieve metadata JSON   |
| `/docs`                       | GET    | Interactive API docs     |

## 🎯 Next Steps

1. ✅ **Backend Complete** - You're here!
2. **IPFS Integration** - Upload images to IPFS for permanent storage
3. **Frontend** - Build a React/Next.js UI
4. **Blockchain Integration** - Connect everything to your smart contract
5. **Deploy** - Put it online for others to use

## 📚 Additional Resources

- **Google AI Studio**: https://aistudio.google.com/
- **OpenSea Metadata**: https://docs.opensea.io/docs/metadata-standards
- **IPFS**: https://ipfs.tech/
- **Pinata (IPFS)**: https://www.pinata.cloud/
- **NFT.Storage**: https://nft.storage/

## 🎉 You're All Set!

Your AI NFT Generator backend is fully functional. Start the server and begin creating unique AI-powered artwork!

```bash
cd backend
python main.py
# Then visit: http://localhost:8000/docs
```

Happy minting! 🚀✨
