# 🚀 Complete NFT Minting Setup Guide

## ✅ What's Already Done

Your AI NFT Minter is now fully integrated with:

- ✅ AI Image Generation (Gemini 2.5 Flash Image)
- ✅ IPFS Storage (NFT.Storage)
- ✅ Blockchain Minting (Ethereum Sepolia)

## 🔑 Get Your NFT.Storage API Key

### Step 1: Sign Up

1. Go to: https://nft.storage/
2. Click **"Sign Up"** (top right)
3. Sign in with **email** or **GitHub**

### Step 2: Create API Key

1. After login, click your profile → **"API Keys"**
2. Click **"+ New Key"**
3. Give it a name (e.g., "AI NFT Minter")
4. **Copy the API key** (you'll only see it once!)

### Step 3: Add to .env File

Open `/backend/.env` and replace:

```bash
# NFT.Storage (IPFS)
NFT_STORAGE_API_KEY=your_nft_storage_api_key_here
```

With your actual key:

```bash
# NFT.Storage (IPFS)
NFT_STORAGE_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## 🔧 Environment Variables Checklist

Make sure your `.env` has all these:

```bash
# Google AI (for image generation)
GOOGLE_API_KEY=AIzaSy...                      ✅ Already set

# NFT.Storage (for IPFS uploads)
NFT_STORAGE_API_KEY=your_key_here             ⚠️  ADD THIS

# Ethereum Wallet (for minting)
PRIVATE_KEY=f71950fbd423...                   ✅ Already set

# Smart Contract (deployed on Sepolia)
CONTRACT_ADDRESS=0x49814e7E1d141F6bE2b21...   ✅ Already set
```

## 🎯 Test the Complete Flow

Once you add your NFT.Storage API key:

### 1. Restart the Server

```bash
cd backend
python main.py
```

### 2. Test with curl

```bash
curl -X POST http://localhost:8000/api/v1/mint-nft \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A dancing monkey making money with a giraffe",
    "name": "Funny Business NFT",
    "description": "My first AI-generated NFT!",
    "network": "sepolia"
  }'
```

### 3. What Happens:

1. 🎨 **AI generates** your image (10-30 seconds)
2. 📤 **Uploads to IPFS** (image + metadata)
3. 🔗 **Mints on Sepolia** blockchain
4. ✅ **Returns** your Token ID and transaction hash!

## 📊 API Endpoints

| Endpoint               | Purpose                               | Connected to Blockchain? |
| ---------------------- | ------------------------------------- | ------------------------ |
| `/api/v1/generate-nft` | Generate image only                   | ❌ No                    |
| `/api/v1/mint-nft`     | **Full flow: Generate → IPFS → Mint** | ✅ Yes                   |

## 🔍 View Your NFT

After minting, you'll get:

- **Token ID**: e.g., `1`
- **Transaction Hash**: `0x123...`
- **Explorer URL**: `https://sepolia.etherscan.io/tx/0x123...`

Click the explorer URL to see your NFT on the blockchain!

## 🎉 Success Looks Like

```json
{
  "success": true,
  "message": "NFT 'Funny Business NFT' minted successfully!",
  "token_id": 1,
  "transaction_hash": "0x123abc...",
  "image_ipfs_uri": "ipfs://QmXyZ...",
  "metadata_ipfs_uri": "ipfs://QmAbc...",
  "explorer_url": "https://sepolia.etherscan.io/tx/0x123abc...",
  "contract_address": "0x49814e7E1d141F6bE2b21b6C4433D083A6A486c0"
}
```

## 💡 Next Steps

After testing:

1. **Build a Frontend** - React/Next.js UI for users
2. **Add Wallet Connect** - Let users connect their wallets
3. **Deploy to Production** - Use mainnet for real NFTs
4. **Create Collections** - Generate batch NFTs with themes

## ❓ Troubleshooting

### "NFT_STORAGE_API_KEY not found"

- Make sure you added the key to `.env`
- Restart the server after editing `.env`

### "PRIVATE_KEY not found"

- Already set in your `.env` ✅

### "CONTRACT_ADDRESS not found"

- Already set: `0x49814e7E1d141F6bE2b21b6C4433D083A6A486c0` ✅

### Minting fails with "insufficient funds"

- Check your Sepolia wallet has ETH
- Get free testnet ETH: https://sepoliafaucet.com/

## 🎓 Understanding the Flow

```
User Request
    ↓
[1] AI Generation (Gemini 2.5 Flash Image)
    ↓ (PNG image + metadata)
[2] IPFS Upload (NFT.Storage)
    ↓ (ipfs:// URIs)
[3] Blockchain Mint (Sepolia)
    ↓ (Transaction hash)
✅ NFT Minted!
```

---

**Ready?** Add your NFT.Storage API key and start minting! 🚀
