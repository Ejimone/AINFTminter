#!/bin/bash

echo "🔍 Checking Google Cloud Run deployment status..."
echo ""

# Get service URL
SERVICE_URL=$(gcloud run services describe ai-nft-minter-backend \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)' 2>/dev/null)

if [ -z "$SERVICE_URL" ]; then
    echo "❌ Service not found or not yet deployed"
    echo ""
    echo "Check build logs:"
    echo "gcloud builds log \$(gcloud builds list --limit=1 --format='value(id)')"
    exit 1
fi

echo "✅ Service deployed!"
echo "📍 URL: $SERVICE_URL"
echo ""

# Test health endpoint
echo "🏥 Testing health endpoint..."
HEALTH_RESPONSE=$(curl -s "$SERVICE_URL/health")

if [ $? -eq 0 ]; then
    echo "✅ Health check passed!"
    echo "$HEALTH_RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$HEALTH_RESPONSE"
else
    echo "❌ Health check failed"
fi

echo ""
echo "🎉 Your backend is ready!"
echo ""
echo "Update your frontend with this URL:"
echo "$SERVICE_URL"
echo ""
echo "Test minting:"
echo "curl -X POST $SERVICE_URL/api/v1/mint-nft \\"
echo "  -H 'Content-Type: application/json' \\"
echo "  -d '{\"prompt\": \"A golden Bitcoin in space\", \"name\": \"Space Bitcoin\"}'"
