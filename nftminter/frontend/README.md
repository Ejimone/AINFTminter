# AI NFT Minter - Frontend

Minimalistic frontend for the AI NFT Minter application.

## Features

- ✨ Clean, modern UI
- 🎨 AI-powered NFT generation
- 📤 IPFS upload visualization
- 🔗 Blockchain minting with live status
- 📱 Fully responsive design
- 🖼️ NFT preview after minting

## Usage

### Option 1: Local Testing

Simply open `index.html` in your browser:

```bash
# macOS
open frontend/index.html

# Or use Python's built-in server
cd frontend
python3 -m http.server 8080
# Then visit: http://localhost:8080
```

### Option 2: Deploy to GitHub Pages

1. Create a new repository on GitHub
2. Push your frontend code:

```bash
cd frontend
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/ai-nft-minter-frontend.git
git push -u origin main
```

3. Enable GitHub Pages:

   - Go to repository Settings → Pages
   - Source: Deploy from branch `main`
   - Folder: `/` (root)
   - Save

4. Your frontend will be live at: `https://YOUR_USERNAME.github.io/ai-nft-minter-frontend/`

### Option 3: Deploy to Vercel

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd frontend
vercel
```

### Option 4: Deploy to Netlify

1. Go to https://app.netlify.com/
2. Drag and drop the `frontend` folder
3. Done! Your site is live

## Configuration

Update the **Backend API URL** in the UI to point to your deployed backend:

- **Local**: `http://localhost:8000`
- **Google Cloud Run**: `https://ai-nft-minter-backend-XXXXXXXX-uc.a.run.app`

## Customization

Edit `index.html` to customize:

- Colors (line 18-19: gradient)
- Fonts (line 12)
- Form fields
- Button text
- Footer

## Screenshot

The UI includes:

1. API URL configuration
2. NFT prompt input (describe your image)
3. NFT name and description
4. Live minting progress with 3 steps:
   - 🎨 AI image generation
   - 📤 IPFS upload
   - ⛓️ Blockchain minting
5. Success display with:
   - Token ID
   - Etherscan link
   - IPFS links
   - NFT preview image

## Browser Support

- ✅ Chrome/Edge (recommended)
- ✅ Firefox
- ✅ Safari
- ✅ Mobile browsers

## Development

No build step required! Pure HTML, CSS, and vanilla JavaScript.

To make changes:

1. Edit `index.html`
2. Refresh browser
3. Done!

## Next Steps

1. Deploy backend to Google Cloud Run (see `backend/DEPLOYMENT.md`)
2. Update API URL in frontend
3. Deploy frontend to hosting service
4. Share your NFT minter with the world! 🚀
