# AI NFT Minter - Frontend

A beautiful, modern frontend for generating AI-powered NFTs. Built with vanilla HTML, CSS, and JavaScript with Radix UI design principles and aesthetic opaque colors.

## 🎨 Features

- **Single NFT Generation**: Generate unique NFTs with custom names and descriptions
- **Batch Generation**: Create multiple images at once from different prompts
- **Modern Design**: Dark theme with opaque colors (no gradients) for a professional look
- **Responsive**: Works perfectly on desktop, tablet, and mobile devices
- **Real-time Feedback**: Loading states and progress indicators
- **IPFS Integration**: Direct links to view images and metadata on IPFS

## 🚀 Quick Start

### Option 1: Open Directly in Browser

Simply open `index.html` in your web browser:

```bash
# From the frontend directory
open index.html
```

Or double-click the `index.html` file.

### Option 2: Use a Local Server (Recommended)

For the best experience, serve the files with a local HTTP server:

```bash
# Using Python 3
python3 -m http.server 8000

# Using Node.js (if you have http-server installed)
npx http-server -p 8000

# Using PHP
php -S localhost:8000
```

Then visit: `http://localhost:8000`

## 📝 Usage

### Generate Single NFT

1. Click on the **"Single NFT"** tab
2. Enter a descriptive prompt for your image
3. Provide a name for your NFT (required)
4. Optionally add a description
5. Click **"Generate NFT"**
6. Wait 10-30 seconds for AI generation
7. View your generated NFT with IPFS links

**Example Prompt:**
```
A futuristic cityscape at sunset with flying cars and neon lights
```

### Batch Generate Images

1. Click on the **"Batch Generate"** tab
2. Enter one prompt per line (up to 10 prompts)
3. Click **"Generate Batch"**
4. Wait for all images to be generated
5. View results in a beautiful grid layout

**Example Prompts:**
```
A serene mountain landscape with a lake
A cyberpunk city at night
An abstract geometric pattern
A peaceful garden with cherry blossoms
```

## 🎨 Design Features

- **Dark Theme**: Professional dark mode with carefully chosen colors
- **Opaque Colors**: No gradients, just solid aesthetic colors
- **Color Palette**:
  - Primary: `#6366F1` (Indigo)
  - Secondary: `#8B5CF6` (Purple)
  - Accent: `#EC4899` (Pink)
  - Success: `#10B981` (Green)
  - Error: `#EF4444` (Red)
- **Typography**: Inter font family for clean, modern text
- **Animations**: Smooth transitions and loading states
- **Shadows**: Subtle depth for card elements

## 🔧 Configuration

The API endpoint is configured in `app.js`:

```javascript
const API_BASE_URL = 'https://ai-nft-minter-580832663068.us-central1.run.app';
```

To change the backend URL, edit this constant in the `app.js` file.

## 📁 File Structure

```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # All styling (opaque colors)
├── app.js             # JavaScript functionality
└── README.md          # This file
```

## 🌐 API Endpoints

### Generate Single NFT
```bash
POST /api/v1/generate-nft
Content-Type: application/json

{
  "prompt": "string",
  "name": "string",
  "description": "string" (optional)
}
```

### Generate Batch
```bash
POST /api/v1/generate-batch
Content-Type: application/json

{
  "prompts": ["string", "string", ...]
}
```

## 🎯 Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Opera 76+

## 📱 Responsive Breakpoints

- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## 🎨 Customization

### Change Colors

Edit the CSS variables in `styles.css`:

```css
:root {
    --primary: #6366F1;
    --secondary: #8B5CF6;
    --accent: #EC4899;
    /* ... more colors */
}
```

### Modify Animations

All animations are defined in `styles.css` with the `@keyframes` rule:

```css
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}
```

## 🔍 Testing

To test the API endpoints manually:

```bash
# Test single NFT generation
curl -X 'POST' \
  'https://ai-nft-minter-580832663068.us-central1.run.app/api/v1/generate-nft' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompt": "a dancing robot",
  "name": "Dancing Robot NFT",
  "description": "An AI-generated dancing robot"
}'

# Test batch generation
curl -X 'POST' \
  'https://ai-nft-minter-580832663068.us-central1.run.app/api/v1/generate-batch' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "prompts": [
    "a beautiful sunset",
    "a mountain landscape",
    "a cyberpunk city"
  ]
}'
```

## 🚨 Troubleshooting

### Images Not Loading
- Check that the backend API is running
- Verify the IPFS gateway is accessible
- Check browser console for errors

### CORS Issues
- Ensure the backend has CORS enabled
- Try using a local server instead of opening HTML directly

### Slow Generation
- AI image generation takes 10-30 seconds
- Batch generation takes proportionally longer
- Check your internet connection

## 📄 License

Part of the AI NFT Minter project - An AI-powered NFT minting platform combining generative AI with blockchain technology.

## 🤝 Contributing

This is a portfolio project. Feel free to fork and customize for your own use!

## 📬 Support

For issues or questions about the backend API, refer to the main project documentation.

---

**Built with ❤️ using vanilla HTML, CSS, and JavaScript**
