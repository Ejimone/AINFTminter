// Configuration
const API_BASE_URL = 'https://ai-nft-minter-580832663068.us-central1.run.app';

// State
let currentTab = 'single';
let userAccount = null;
let web3 = null;

// MetaMask Integration
async function connectWallet() {
    if (typeof window.ethereum === 'undefined') {
        showResult('error', '❌ MetaMask Not Found', `
            <div class="error-alert">
                <strong>MetaMask not detected!</strong><br>
                Please install MetaMask to connect your wallet.
                <br><br>
                <a href="https://metamask.io/" target="_blank" class="metadata-link">
                    Download MetaMask →
                </a>
            </div>
        `);
        return;
    }

    try {
        // Request account access
        const accounts = await window.ethereum.request({
            method: 'eth_requestAccounts'
        });

        userAccount = accounts[0];

        // Get network
        const chainId = await window.ethereum.request({
            method: 'eth_chainId'
        });

        const networkNames = {
            '0x1': 'Ethereum Mainnet',
            '0xaa36a7': 'Sepolia Testnet',
            '0x5': 'Goerli Testnet',
            '0x539': 'Ganache Local'
        };

        const networkName = networkNames[chainId] || `Unknown (${chainId})`;

        // Check if on Sepolia
        if (chainId !== '0xaa36a7') {
            const switchNetwork = confirm(
                `You're on ${networkName}.\n\n` +
                `This app works on Sepolia Testnet.\n\n` +
                `Switch to Sepolia now?`
            );

            if (switchNetwork) {
                try {
                    await window.ethereum.request({
                        method: 'wallet_switchEthereumChain',
                        params: [{ chainId: '0xaa36a7' }]
                    });
                } catch (switchError) {
                    // Network not added, try to add it
                    if (switchError.code === 4902) {
                        await window.ethereum.request({
                            method: 'wallet_addEthereumChain',
                            params: [{
                                chainId: '0xaa36a7',
                                chainName: 'Sepolia Testnet',
                                nativeCurrency: {
                                    name: 'Sepolia ETH',
                                    symbol: 'ETH',
                                    decimals: 18
                                },
                                rpcUrls: ['https://sepolia.infura.io/v3/'],
                                blockExplorerUrls: ['https://sepolia.etherscan.io/']
                            }]
                        });
                    }
                }
            }
        }

        // Get balance
        const balance = await window.ethereum.request({
            method: 'eth_getBalance',
            params: [userAccount, 'latest']
        });
        
        const ethBalance = parseInt(balance, 16) / Math.pow(10, 18);

        // Update UI
        document.getElementById('connectWallet').style.display = 'none';
        document.getElementById('walletInfo').style.display = 'block';
        document.getElementById('walletAddress').textContent = 
            userAccount.slice(0, 6) + '...' + userAccount.slice(-4);
        document.getElementById('networkName').textContent = networkName;
        document.getElementById('walletBalance').textContent = 
            `${ethBalance.toFixed(4)} ETH`;

        // Listen for account changes
        window.ethereum.on('accountsChanged', (accounts) => {
            if (accounts.length === 0) {
                location.reload();
            } else {
                userAccount = accounts[0];
                document.getElementById('walletAddress').textContent = 
                    userAccount.slice(0, 6) + '...' + userAccount.slice(-4);
            }
        });

        // Listen for network changes
        window.ethereum.on('chainChanged', () => {
            location.reload();
        });

    } catch (error) {
        console.error('Error connecting wallet:', error);
        showResult('error', '❌ Connection Failed', `
            <div class="error-alert">
                <strong>Failed to connect wallet:</strong><br>
                ${error.message}
            </div>
        `);
    }
}

// Check if already connected on page load
async function checkWalletConnection() {
    if (typeof window.ethereum !== 'undefined') {
        const accounts = await window.ethereum.request({
            method: 'eth_accounts'
        });

        if (accounts.length > 0) {
            await connectWallet();
        }
    }
}

// Tab Switching
function switchTab(tab) {
    currentTab = tab;
    
    // Update tab buttons
    document.querySelectorAll('.tab-button').forEach(btn => {
        btn.classList.remove('active');
    });
    document.querySelector(`[data-tab="${tab}"]`).classList.add('active');
    
    // Update tab content
    document.querySelectorAll('.tab-content').forEach(content => {
        content.classList.remove('active');
    });
    document.getElementById(`${tab}-tab`).classList.add('active');
}

// Show/Hide Loading
function showLoading(title, text, steps = []) {
    const overlay = document.getElementById('loadingOverlay');
    const loadingTitle = document.getElementById('loadingTitle');
    const loadingText = document.getElementById('loadingText');
    const loadingSteps = document.getElementById('loadingSteps');
    
    loadingTitle.textContent = title;
    loadingText.textContent = text;
    
    // Create loading steps
    if (steps.length > 0) {
        loadingSteps.innerHTML = steps.map((step, index) => `
            <div class="loading-step" id="step-${index}">
                <span class="step-icon">⏳</span>
                <span class="step-text">${step}</span>
            </div>
        `).join('');
    } else {
        loadingSteps.innerHTML = '';
    }
    
    overlay.style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function updateStep(stepIndex, complete = false) {
    const step = document.getElementById(`step-${stepIndex}`);
    if (step) {
        if (complete) {
            step.classList.add('complete');
            step.querySelector('.step-icon').textContent = '✅';
        } else {
            step.classList.add('active');
            step.querySelector('.step-icon').textContent = '⏳';
        }
    }
}

// Show Result
function showResult(type, title, content) {
    const resultDiv = document.getElementById(`${currentTab}Result`);
    const resultTitle = resultDiv.querySelector('.result-title');
    const resultContent = resultDiv.querySelector('.result-content');
    
    // Remove previous status classes
    resultDiv.classList.remove('result-success', 'result-error');
    
    // Add new status class
    if (type === 'success') {
        resultDiv.classList.add('result-success');
    } else if (type === 'error') {
        resultDiv.classList.add('result-error');
    }
    
    resultTitle.textContent = title;
    resultContent.innerHTML = content;
    resultDiv.style.display = 'block';
    
    // Scroll to result
    resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function closeResult(tab) {
    document.getElementById(`${tab}Result`).style.display = 'none';
}

// Format IPFS URL
function formatIpfsUrl(ipfsUri) {
    return ipfsUri.replace('ipfs://', 'https://gateway.pinata.cloud/ipfs/');
}

// Single NFT Form Handler
document.getElementById('singleNftForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const prompt = document.getElementById('prompt').value.trim();
    const name = document.getElementById('name').value.trim();
    const description = document.getElementById('description').value.trim();
    
    if (!prompt || !name) {
        showResult('error', '❌ Validation Error', `
            <div class="error-alert">
                <strong>Error:</strong> Please fill in all required fields.
            </div>
        `);
        return;
    }
    
    // Disable button
    const btn = document.getElementById('generateBtn');
    btn.disabled = true;
    
    // Show loading with steps
    showLoading(
        'Generating Your NFT',
        'This process may take 10-30 seconds...',
        [
            'Generating AI image...',
            'Uploading to IPFS...',
            'Creating metadata...'
        ]
    );
    
    try {
        // Start first step
        updateStep(0);
        
        const response = await fetch(`${API_BASE_URL}/api/v1/generate-nft`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                prompt: prompt,
                name: name,
                description: description || undefined
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP error! status: ${response.status}`);
        }
        
                const data = await response.json();
                
                // Show success result with NFT viewing capabilities
                showNFTResult(data, false);
                
                // Reset form
                document.getElementById('singleNftForm').reset();
        }, 500);    } catch (error) {
        console.error('Error generating NFT:', error);
        hideLoading();
        
        showResult('error', '❌ Generation Failed', `
            <div class="error-alert">
                <strong>Error:</strong> ${error.message}
            </div>
            <p class="mt-2">
                Please check the following:
                <ul style="margin-top: 0.5rem; margin-left: 1.5rem; color: var(--text-secondary);">
                    <li>API endpoint is accessible</li>
                    <li>Your prompt is appropriate</li>
                    <li>Backend service is running</li>
                </ul>
            </p>
        `);
    } finally {
        btn.disabled = false;
    }
});

// Batch Form Handler
document.getElementById('batchForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const promptsText = document.getElementById('prompts').value.trim();
    const prompts = promptsText.split('\n').filter(p => p.trim().length > 0);
    
    if (prompts.length === 0) {
        showResult('error', '❌ Validation Error', `
            <div class="error-alert">
                <strong>Error:</strong> Please enter at least one prompt.
            </div>
        `);
        return;
    }
    
    if (prompts.length > 10) {
        showResult('error', '❌ Validation Error', `
            <div class="error-alert">
                <strong>Error:</strong> Maximum 10 prompts allowed. You entered ${prompts.length}.
            </div>
        `);
        return;
    }
    
    // Disable button
    const btn = document.getElementById('batchBtn');
    btn.disabled = true;
    
    // Show loading
    showLoading(
        'Generating Batch Images',
        `Generating ${prompts.length} image${prompts.length > 1 ? 's' : ''}... This may take a while.`,
        []
    );
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/v1/generate-batch`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                prompts: prompts
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Hide loading
        setTimeout(() => {
            hideLoading();
            
            // Build batch results grid
            const resultsGrid = data.results.map((result, index) => {
                if (result.status === 'success') {
                    return `
                        <div class="batch-item">
                            <img src="${formatIpfsUrl(result.ipfs_uri)}" alt="Generated image ${index + 1}" />
                            <div class="batch-prompt">${result.prompt}</div>
                            <div style="margin-top: 0.5rem;">
                                <a href="${formatIpfsUrl(result.ipfs_uri)}" target="_blank" class="metadata-link" style="font-size: 0.875rem;">
                                    View on IPFS →
                                </a>
                            </div>
                        </div>
                    `;
                } else {
                    return `
                        <div class="batch-item" style="border-color: var(--error);">
                            <div style="padding: 1rem; text-align: center;">
                                <span style="font-size: 2rem;">❌</span>
                                <div class="batch-prompt" style="color: var(--error); margin-top: 0.5rem;">
                                    ${result.prompt}
                                </div>
                                <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem;">
                                    ${result.error || 'Generation failed'}
                                </div>
                            </div>
                        </div>
                    `;
                }
            }).join('');
            
            const successCount = data.results.filter(r => r.status === 'success').length;
            const failCount = data.results.filter(r => r.status === 'error').length;
            
            // Show results
            showResult('success', '🎨 Batch Generation Complete', `
                <div class="${failCount > 0 ? 'error-alert' : 'success-alert'}">
                    <strong>Results:</strong> ${successCount} successful, ${failCount} failed
                </div>
                
                <div class="batch-grid">
                    ${resultsGrid}
                </div>
            `);
            
            // Reset form
            document.getElementById('batchForm').reset();
        }, 500);
        
    } catch (error) {
        console.error('Error generating batch:', error);
        hideLoading();
        
        showResult('error', '❌ Batch Generation Failed', `
            <div class="error-alert">
                <strong>Error:</strong> ${error.message}
            </div>
            <p class="mt-2">
                Please check the following:
                <ul style="margin-top: 0.5rem; margin-left: 1.5rem; color: var(--text-secondary);">
                    <li>API endpoint is accessible</li>
                    <li>Your prompts are appropriate</li>
                    <li>Backend service is running</li>
                </ul>
            </p>
        `);
    } finally {
        btn.disabled = false;
    }
});

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    console.log('AI NFT Minter initialized');
    console.log('API Base URL:', API_BASE_URL);
    
    // Check wallet connection on load
    checkWalletConnection();
});

// Generate Only (no minting)
async function generateOnly() {
    const prompt = document.getElementById('prompt').value.trim();
    const name = document.getElementById('name').value.trim();
    const description = document.getElementById('description').value.trim();
    
    if (!prompt || !name) {
        showResult('error', '❌ Validation Error', `
            <div class="error-alert">
                <strong>Error:</strong> Please fill in all required fields.
            </div>
        `);
        return;
    }
    
    await generateNFT(prompt, name, description, false);
}

// Generate NFT (with or without minting)
async function generateNFT(prompt, name, description, shouldMint = true) {
    // Disable buttons
    const generateBtn = document.getElementById('generateBtn');
    const generateOnlyBtn = document.getElementById('generateOnlyBtn');
    generateBtn.disabled = true;
    generateOnlyBtn.disabled = true;
    
    const steps = shouldMint ? [
        'Generating AI image...',
        'Uploading to IPFS...',
        'Creating metadata...',
        'Minting on blockchain...'
    ] : [
        'Generating AI image...',
        'Uploading to IPFS...',
        'Creating metadata...'
    ];
    
    // Show loading with steps
    showLoading(
        shouldMint ? 'Generating & Minting NFT' : 'Generating NFT',
        shouldMint ? 'This process may take 30-60 seconds...' : 'This process may take 10-30 seconds...',
        steps
    );
    
    try {
        const endpoint = shouldMint ? '/api/v1/mint-nft' : '/api/v1/generate-nft';
        const requestBody = shouldMint ? {
            prompt: prompt,
            name: name,
            description: description || undefined,
            recipient_address: userAccount,
            network: 'sepolia'
        } : {
            prompt: prompt,
            name: name,
            description: description || undefined
        };
        
        // Start first step
        updateStep(0);
        
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Mark all steps complete
        for (let i = 0; i < steps.length; i++) {
            updateStep(i, true);
        }
        
        // Hide loading after a brief moment
        setTimeout(() => {
            hideLoading();
            showNFTResult(data, shouldMint);
            document.getElementById('singleNftForm').reset();
        }, 500);
        
    } catch (error) {
        console.error('Error generating NFT:', error);
        hideLoading();
        
        showResult('error', shouldMint ? '❌ Minting Failed' : '❌ Generation Failed', `
            <div class="error-alert">
                <strong>Error:</strong> ${error.message}
            </div>
            <p class="mt-2">
                Please check the following:
                <ul style="margin-top: 0.5rem; margin-left: 1.5rem; color: var(--text-secondary);">
                    <li>API endpoint is accessible</li>
                    <li>Your prompt is appropriate</li>
                    <li>Backend service is running</li>
                    ${shouldMint ? '<li>MetaMask is connected and on Sepolia network</li>' : ''}
                </ul>
            </p>
        `);
    } finally {
        generateBtn.disabled = false;
        generateOnlyBtn.disabled = false;
    }
}

// Show NFT Result with enhanced viewing
function showNFTResult(data, wasMinted) {
    const explorerUrl = data.transaction_hash ? 
        `https://sepolia.etherscan.io/tx/${data.transaction_hash}` : null;
    
    const title = wasMinted ? '🎉 NFT Minted Successfully!' : '✨ NFT Generated Successfully!';
    const alertClass = wasMinted ? 'success-alert' : 'success-alert';
    const alertText = wasMinted ? 
        'Your NFT has been generated and minted on the Sepolia blockchain!' :
        'Your NFT has been generated and uploaded to IPFS.';
    
    showResult('success', title, `
        <div class="${alertClass}">
            <strong>Success!</strong> ${alertText}
        </div>
        
        <div class="nft-preview">
            <div class="nft-image-container">
                <img src="${formatIpfsUrl(data.image_ipfs_uri)}" alt="${data.name}" class="nft-image" />
                <div class="nft-overlay">
                    <button class="btn-view-fullsize" onclick="viewFullSize('${formatIpfsUrl(data.image_ipfs_uri)}', '${data.name}')">
                        🔍 View Full Size
                    </button>
                </div>
            </div>
        </div>
        
        <div class="nft-metadata">
            <div class="metadata-item">
                <div class="metadata-label">NFT Name</div>
                <div class="metadata-value">${data.name}</div>
            </div>
            
            <div class="metadata-item">
                <div class="metadata-label">Description</div>
                <div class="metadata-value">${data.description || 'N/A'}</div>
            </div>
            
            ${wasMinted ? `
            <div class="metadata-item highlighted">
                <div class="metadata-label">Token ID</div>
                <div class="metadata-value">#${data.token_id}</div>
            </div>
            
            <div class="metadata-item highlighted">
                <div class="metadata-label">Contract Address</div>
                <div class="metadata-value">
                    <a href="https://sepolia.etherscan.io/address/${data.contract_address}" target="_blank" class="metadata-link">
                        ${data.contract_address}
                    </a>
                </div>
            </div>
            
            <div class="metadata-item highlighted">
                <div class="metadata-label">Transaction</div>
                <div class="metadata-value">
                    <a href="${explorerUrl}" target="_blank" class="metadata-link">
                        ${data.transaction_hash}
                    </a>
                </div>
            </div>
            ` : ''}
            
            <div class="metadata-item">
                <div class="metadata-label">Image IPFS</div>
                <div class="metadata-value">
                    <a href="${formatIpfsUrl(data.image_ipfs_uri)}" target="_blank" class="metadata-link">
                        View on IPFS →
                    </a>
                </div>
            </div>
            
            <div class="metadata-item">
                <div class="metadata-label">Metadata IPFS</div>
                <div class="metadata-value">
                    <a href="${formatIpfsUrl(data.metadata_ipfs_uri)}" target="_blank" class="metadata-link">
                        View Metadata →
                    </a>
                </div>
            </div>
        </div>
        
        ${wasMinted ? `
        <div class="nft-actions">
            <button class="btn-secondary" onclick="shareNFT('${data.name}', '${formatIpfsUrl(data.image_ipfs_uri)}', '${explorerUrl}')">
                📤 Share NFT
            </button>
            <button class="btn-primary" onclick="viewOnOpenSea('${data.contract_address}', '${data.token_id}')">
                🌊 View on OpenSea
            </button>
        </div>
        ` : `
        <div class="nft-actions">
            <button class="btn-primary" onclick="mintExistingNFT('${data.metadata_ipfs_uri}', '${data.name}')">
                ⚡ Mint This NFT
            </button>
        </div>
        `}
    `);
}

// View full size image
function viewFullSize(imageUrl, name) {
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <div class="modal-overlay" onclick="closeModal(this)">
            <div class="modal-content" onclick="event.stopPropagation()">
                <button class="modal-close" onclick="closeModal(this)">✕</button>
                <img src="${imageUrl}" alt="${name}" class="modal-image" />
                <div class="modal-info">
                    <h3>${name}</h3>
                    <a href="${imageUrl}" target="_blank" class="metadata-link">Open in New Tab →</a>
                </div>
            </div>
        </div>
    `;
    document.body.appendChild(modal);
}

function closeModal(element) {
    const modal = element.closest('.image-modal');
    if (modal) {
        document.body.removeChild(modal);
    }
}

// Share NFT
function shareNFT(name, imageUrl, explorerUrl) {
    if (navigator.share) {
        navigator.share({
            title: `Check out my NFT: ${name}`,
            text: 'I just minted this amazing AI-generated NFT!',
            url: explorerUrl
        });
    } else {
        // Fallback - copy to clipboard
        const shareText = `Check out my NFT: ${name}\nImage: ${imageUrl}\nTransaction: ${explorerUrl}`;
        navigator.clipboard.writeText(shareText).then(() => {
            alert('NFT details copied to clipboard!');
        });
    }
}

// View on OpenSea
function viewOnOpenSea(contractAddress, tokenId) {
    const openSeaUrl = `https://testnets.opensea.io/assets/sepolia/${contractAddress}/${tokenId}`;
    window.open(openSeaUrl, '_blank');
}

// Mint existing NFT
async function mintExistingNFT(metadataUri, name) {
    if (!userAccount) {
        showResult('error', '❌ Wallet Not Connected', `
            <div class="error-alert">
                <strong>Please connect your MetaMask wallet first.</strong>
            </div>
        `);
        return;
    }
    
    const shouldMint = confirm(`Do you want to mint "${name}" as an NFT on the blockchain?\n\nThis will require a small gas fee.`);
    if (!shouldMint) return;
    
    showLoading(
        'Minting NFT',
        'Minting your NFT on the blockchain...',
        ['Minting on blockchain...']
    );
    
    try {
        updateStep(0);
        
        const response = await fetch(`${API_BASE_URL}/api/v1/mint-nft`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            body: JSON.stringify({
                prompt: 'Pre-generated NFT',
                name: name,
                description: 'Minted from generated NFT',
                recipient_address: userAccount,
                network: 'sepolia',
                metadata_uri: metadataUri
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        updateStep(0, true);
        
        setTimeout(() => {
            hideLoading();
            showNFTResult(data, true);
        }, 500);
        
    } catch (error) {
        console.error('Error minting NFT:', error);
        hideLoading();
        
        showResult('error', '❌ Minting Failed', `
            <div class="error-alert">
                <strong>Error:</strong> ${error.message}
            </div>
        `);
    }
}

