# NFT Minter - Quick Start Guide

## 🎬 Netflix-Inspired UI

Your AI NFT Minter now features a sleek, Netflix-inspired design with:
- **Black and Red Theme**: Professional dark theme with Netflix's iconic red accent
- **No Icons/Emojis**: Clean, text-only interface
- **Cool Animated Notifications**: Smooth slide-in notifications with progress bars
- **MetaMask Required**: Users must connect wallet before generating NFTs

## 🚀 How to Use

### 1. Open the Application

```bash
# Option 1: Open directly in browser
open index.html

# Option 2: Use a local server (recommended)
python3 -m http.server 8000
# Then visit: http://localhost:8000
```

### 2. Connect Your Wallet

- Click the **"CONNECT METAMASK"** button
- Approve the connection in your MetaMask extension
- Your wallet address, network, and balance will be displayed
- Forms will become available after connection

**Note:** Forms are locked until wallet is connected!

### 3. Generate Single NFT

**Tab: Single NFT**

1. Enter your image prompt (e.g., "A futuristic cityscape at sunset")
2. Enter NFT name (required)
3. Enter description (optional)
4. Choose action:
   - **GENERATE ONLY**: Creates the NFT without minting
   - **GENERATE & MINT NFT**: Creates and mints to blockchain

### 4. Batch Generate Images

**Tab: Batch Generate**

1. Enter multiple prompts (one per line, max 10)
2. Click **"GENERATE BATCH"**
3. View all generated images in a grid layout

## 🎨 Design Features

### Color Palette
- **Primary Red**: `#E50914` (Netflix red)
- **Background**: Pure black `#000000`
- **Cards**: Dark gray `#181818`
- **Text**: White and gray tones
- **Success**: Green `#46D369`
- **Error**: Red `#E50914`

### Typography
- Font: Inter (Google Fonts)
- Uppercase labels and buttons
- Letter spacing for emphasis
- Clean, readable hierarchy

### Animations
1. **Notifications**
   - Slide in from right with bounce effect
   - Auto-dismiss after 5 seconds
   - Smooth slide out animation
   - Progress bar indicating time remaining

2. **Forms**
   - Fade in when switching tabs
   - Scale animations on hover
   - Smooth transitions

3. **Loading States**
   - Spinning loader
   - Step-by-step progress indicators
   - Backdrop blur effect

## 🔔 Notification Types

The app shows different notification styles:

- **Success** (Green): NFT generated, wallet connected
- **Error** (Red): Generation failed, validation errors
- **Warning** (Orange): Missing requirements
- **Info** (Red): General information, connecting status

## 🔒 Security Features

- **Wallet Gating**: All generation features require MetaMask connection
- **Form Overlays**: Visual lock on forms until wallet connected
- **Account Monitoring**: Detects wallet changes and updates UI
- **Network Detection**: Shows current network and balance

## 🎯 User Experience

### Before Wallet Connection
- Forms display overlay with "Connect Your Wallet" message
- Only wallet connection button is active
- Clear call-to-action to connect

### After Wallet Connection
- Overlays disappear instantly
- Full access to all features
- Wallet info displayed in header
- Notifications confirm connection

## 📱 Responsive Design

The UI is fully responsive:
- **Mobile**: Single column layout, stacked forms
- **Tablet**: Optimized spacing and sizing
- **Desktop**: Full-width grid layouts, side-by-side buttons

## 🛠️ Technical Stack

- **HTML5**: Semantic structure
- **CSS3**: Custom properties, animations, flexbox/grid
- **Vanilla JavaScript**: No frameworks, pure ES6+
- **Web3**: MetaMask integration via window.ethereum
- **Radix UI**: Design principles (loaded via CDN)

## 📋 API Endpoints Used

```bash
# Single NFT Generation
POST /api/v1/generate-nft
Body: { prompt, name, description }

# Batch Generation
POST /api/v1/generate-batch
Body: { prompts: [] }
```

## 🎭 Demo Scenarios

### Success Flow
1. User opens app → Sees locked forms
2. Clicks "Connect MetaMask" → Wallet connects
3. Forms unlock with smooth animation
4. User enters NFT details → Clicks generate
5. Loading overlay appears with progress
6. Success notification slides in
7. Result card displays with image
8. User can view on IPFS

### Error Handling
1. User tries to generate without wallet → Warning notification
2. Invalid prompt → Error notification with details
3. API error → Error notification with retry suggestion
4. Network issues → Informative error messages

## 🎨 Customization

To change the primary color from Netflix red to another color:

```css
/* In styles.css */
:root {
  --primary: #YOUR_COLOR;
  --primary-hover: #YOUR_HOVER_COLOR;
}
```

## 🐛 Troubleshooting

**Forms won't unlock:**
- Check if MetaMask is installed
- Refresh the page
- Check browser console for errors

**Notifications not showing:**
- Check if JavaScript is enabled
- Verify app.js is loaded correctly

**Images not loading:**
- Verify API endpoint is accessible
- Check IPFS gateway status
- Review browser console for CORS errors

## 📞 Support

For issues with:
- **Frontend**: Check browser console, verify files loaded
- **Backend API**: Check API endpoint in app.js
- **MetaMask**: Ensure extension is installed and unlocked

---

**Enjoy your Netflix-inspired NFT Minter! 🎬🎨**

