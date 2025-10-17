#!/bin/bash

# Deploy AI NFT Minter to Google Cloud Run
set -e

echo "Deploying AI NFT Minter to Google Cloud Run..."

gcloud run deploy ai-nft-minter \
  --source . \
  --platform managed \
  --region us-central1 \
  --project rendulum \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 2 \
  --timeout 300 \
  --min-instances 0 \
  --max-instances 10 \
  --port 8080 \
  --set-env-vars GOOGLE_API_KEY=AIzaSyBu_8pZ6Fk_1mvvn3JG8pAP_-6xs9YdGJ0 \
  --set-env-vars PINATA_JWT=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI4ZGViMGZlYy1hYmQyLTQ2ZDEtYmZlOS01NTJmMWU4Y2NhNGIiLCJlbWFpbCI6ImV2aWRlbmNlZWppbW9uZUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJGUkExIn0seyJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MSwiaWQiOiJOWUMxIn1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiN2YzMjFlMzc1NGVmOTQwMzI3YTgiLCJzY29wZWRLZXlTZWNyZXQiOiJkY2M2YjJmMDM5NGZlOGNjZGE5OTU4MTg5MDkyN2UxMzkzNmQwNmU2M2E5Yzg0ZjkzODlkODRhMmVhMjIyNTM1IiwiZXhwIjoxNzkyMjIzNTYwfQ.gs5POgfSKxYO3uf5iMRu9iPzICxOhu6w6uAYCP0V2QI \
  --set-env-vars PRIVATE_KEY=f71950fbd423431d8d60498dfa30c41034b08c71c45b797dc20b094006bf5688 \
  --set-env-vars CONTRACT_ADDRESS=0x49814e7E1d141F6bE2b21b6C4433D083A6A486c0 \
  --set-env-vars WEB3_INFURA_PROJECT_ID=66308c62e2cb49e8bac4b4cd96143144

echo "Deployment completed!"