# 🚀 Google Cloud Deployment Guide

## Prerequisites

1. **Google Cloud Account** - https://cloud.google.com/
2. **Google Cloud CLI (gcloud)** - Install: https://cloud.google.com/sdk/docs/install
3. **Docker** (optional, for local testing) - https://www.docker.com/

## Step 1: Set Up Google Cloud Project

```bash
# Login to Google Cloud
gcloud auth login

# Create a new project (or use existing)
gcloud projects create ai-nft-minter --name="AI NFT Minter"

# Set as active project
gcloud config set project ai-nft-minter

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable secretmanager.googleapis.com
```

## Step 2: Store Secrets in Secret Manager

```bash
# Store sensitive environment variables as secrets
echo -n "AIzaSyBu_8pZ6Fk_1mvvn3JG8pAP_-6xs9YdGJ0" | \
  gcloud secrets create GOOGLE_API_KEY --data-file=-

echo -n "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." | \
  gcloud secrets create PINATA_JWT --data-file=-

echo -n "f71950fbd423431d8d60498dfa30c41034b08c71c45b797dc20b094006bf5688" | \
  gcloud secrets create PRIVATE_KEY --data-file=-

echo -n "0x49814e7E1d141F6bE2b21b6C4433D083A6A486c0" | \
  gcloud secrets create CONTRACT_ADDRESS --data-file=-

echo -n "66308c62e2cb49e8bac4b4cd96143144" | \
  gcloud secrets create WEB3_INFURA_PROJECT_ID --data-file=-
```

## Step 3: Deploy to Cloud Run

### Option A: Deploy with Cloud Build (Recommended)

```bash
# Navigate to backend directory
cd /Users/evidencejimone/AINFTminter/nftminter/backend

# Submit build to Cloud Build
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_GOOGLE_API_KEY="$(gcloud secrets versions access latest --secret=GOOGLE_API_KEY)",_PINATA_JWT="$(gcloud secrets versions access latest --secret=PINATA_JWT)",_PRIVATE_KEY="$(gcloud secrets versions access latest --secret=PRIVATE_KEY)",_CONTRACT_ADDRESS="$(gcloud secrets versions access latest --secret=CONTRACT_ADDRESS)",_WEB3_INFURA_PROJECT_ID="$(gcloud secrets versions access latest --secret=WEB3_INFURA_PROJECT_ID)"
```

### Option B: Deploy Directly with gcloud

```bash
# Deploy to Cloud Run
gcloud run deploy ai-nft-minter-backend \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-secrets GOOGLE_API_KEY=GOOGLE_API_KEY:latest,PINATA_JWT=PINATA_JWT:latest,PRIVATE_KEY=PRIVATE_KEY:latest,CONTRACT_ADDRESS=CONTRACT_ADDRESS:latest,WEB3_INFURA_PROJECT_ID=WEB3_INFURA_PROJECT_ID:latest
```

## Step 4: Test Deployment

```bash
# Get the service URL
SERVICE_URL=$(gcloud run services describe ai-nft-minter-backend --platform managed --region us-central1 --format 'value(status.url)')

# Test health endpoint
curl $SERVICE_URL/health

# Test NFT generation (takes ~30 seconds)
curl -X POST $SERVICE_URL/api/v1/mint-nft \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A futuristic city with flying cars at sunset",
    "name": "Future City NFT",
    "description": "AI-generated futuristic cityscape"
  }'
```

## Step 5: Set Up Custom Domain (Optional)

```bash
# Map custom domain
gcloud run domain-mappings create --service ai-nft-minter-backend --domain api.yournftminter.com --region us-central1
```

## Monitoring & Logs

```bash
# View logs
gcloud run services logs read ai-nft-minter-backend --region us-central1 --limit 50

# View service details
gcloud run services describe ai-nft-minter-backend --region us-central1
```

## Cost Optimization

- **Free Tier**: 2 million requests/month, 360,000 GB-seconds
- **Auto-scaling**: Scales to 0 when not in use
- **Estimated Cost**: ~$5-20/month for moderate usage

## Troubleshooting

### Build Fails

```bash
# Check build logs
gcloud builds log $(gcloud builds list --limit=1 --format='value(id)')
```

### Container Crashes

```bash
# Check container logs
gcloud run services logs read ai-nft-minter-backend --region us-central1
```

### Secrets Not Loading

```bash
# Grant Cloud Run service account access to secrets
gcloud secrets add-iam-policy-binding GOOGLE_API_KEY \
  --member="serviceAccount:$(gcloud projects describe ai-nft-minter --format='value(projectNumber)')-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"
```

## Update Deployment

```bash
# After making code changes
gcloud run deploy ai-nft-minter-backend \
  --source . \
  --platform managed \
  --region us-central1
```

## Your Deployed Backend URL

After deployment, your API will be available at:

```
https://ai-nft-minter-backend-XXXXXXXX-uc.a.run.app
```

Save this URL - you'll need it for the frontend!
