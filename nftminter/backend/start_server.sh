#!/bin/bash

echo "🚀 Starting AI NFT Minter API Server..."
echo ""
echo "📋 Endpoints:"
echo "  - API Root:       http://localhost:8000"
echo "  - Documentation:  http://localhost:8000/docs"
echo "  - Health Check:   http://localhost:8000/health"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

cd "$(dirname "$0")"
python main.py
