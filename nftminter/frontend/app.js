// Configuration
const API_BASE_URL = "https://ai-nft-minter-580832663068.us-central1.run.app";

// State
let currentTab = "single";
let walletConnected = false;
let userAddress = null;

// Notification System
function showNotification(type, title, message) {
  const container = document.getElementById("notificationContainer");
  const notification = document.createElement("div");
  notification.className = `notification ${type}`;

  const icons = {
    success: "✓",
    error: "✕",
    warning: "⚠",
    info: "ℹ",
  };

  notification.innerHTML = `
        <div class="notification-icon">${icons[type] || icons.info}</div>
        <div class="notification-content">
            <div class="notification-title">${title}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">✕</button>
        <div class="notification-progress"></div>
    `;

  container.appendChild(notification);

  // Auto remove after 5 seconds
  setTimeout(() => {
    notification.classList.add("removing");
    setTimeout(() => {
      notification.remove();
    }, 300);
  }, 5000);
}

// Tab Switching
function switchTab(tab) {
  currentTab = tab;

  // Update tab buttons
  document.querySelectorAll(".tab-button").forEach((btn) => {
    btn.classList.remove("active");
  });
  document.querySelector(`[data-tab="${tab}"]`).classList.add("active");

  // Update tab content
  document.querySelectorAll(".tab-content").forEach((content) => {
    content.classList.remove("active");
  });
  document.getElementById(`${tab}-tab`).classList.add("active");
}

// Wallet Connection
async function connectWallet() {
  if (typeof window.ethereum === "undefined") {
    showNotification(
      "error",
      "MetaMask Not Found",
      "Please install MetaMask extension to continue"
    );
    return;
  }

  try {
    showNotification(
      "info",
      "Connecting...",
      "Please approve the connection request in MetaMask"
    );

    const accounts = await window.ethereum.request({
      method: "eth_requestAccounts",
    });

    userAddress = accounts[0];
    walletConnected = true;

    // Get network
    const chainId = await window.ethereum.request({
      method: "eth_chainId",
    });

    const networkNames = {
      "0x1": "Ethereum Mainnet",
      "0xaa36a7": "Sepolia Testnet",
      "0x5": "Goerli Testnet",
      "0x539": "Ganache Local",
    };

    const networkName = networkNames[chainId] || `Chain ID: ${chainId}`;

    // Get balance
    const balance = await window.ethereum.request({
      method: "eth_getBalance",
      params: [userAddress, "latest"],
    });
    const balanceInEth = (parseInt(balance, 16) / 1e18).toFixed(4);

    // Update UI
    document.getElementById("connectWallet").style.display = "none";
    document.getElementById("walletInfo").style.display = "block";
    document.getElementById("walletAddress").textContent =
      userAddress.slice(0, 6) + "..." + userAddress.slice(-4);
    document.getElementById("networkName").textContent = networkName;
    document.getElementById(
      "walletBalance"
    ).textContent = `${balanceInEth} ETH`;

    // Hide form overlays
    document.getElementById("singleFormOverlay").style.display = "none";
    document.getElementById("batchFormOverlay").style.display = "none";

    showNotification(
      "success",
      "Wallet Connected",
      `Connected to ${userAddress.slice(0, 6)}...${userAddress.slice(-4)}`
    );

    // Listen for account changes
    window.ethereum.on("accountsChanged", (accounts) => {
      if (accounts.length === 0) {
        location.reload();
      } else {
        userAddress = accounts[0];
        document.getElementById("walletAddress").textContent =
          userAddress.slice(0, 6) + "..." + userAddress.slice(-4);
        showNotification(
          "info",
          "Account Changed",
          "Wallet account has been changed"
        );
      }
    });

    // Listen for network changes
    window.ethereum.on("chainChanged", () => {
      location.reload();
    });
  } catch (error) {
    console.error("Error connecting wallet:", error);
    showNotification(
      "error",
      "Connection Failed",
      error.message || "Failed to connect to MetaMask"
    );
  }
}

// Check if wallet is already connected
async function checkWalletConnection() {
  if (typeof window.ethereum !== "undefined") {
    const accounts = await window.ethereum.request({
      method: "eth_accounts",
    });

    if (accounts.length > 0) {
      await connectWallet();
    } else {
      // Show overlays if wallet not connected
      document.getElementById("singleFormOverlay").style.display = "flex";
      document.getElementById("batchFormOverlay").style.display = "flex";
    }
  } else {
    // Show overlays if MetaMask not installed
    document.getElementById("singleFormOverlay").style.display = "flex";
    document.getElementById("batchFormOverlay").style.display = "flex";
  }
}

// Show/Hide Loading
function showLoading(title, text, steps = []) {
  const overlay = document.getElementById("loadingOverlay");
  const loadingTitle = document.getElementById("loadingTitle");
  const loadingText = document.getElementById("loadingText");
  const loadingSteps = document.getElementById("loadingSteps");

  loadingTitle.textContent = title;
  loadingText.textContent = text;

  // Create loading steps
  if (steps.length > 0) {
    loadingSteps.innerHTML = steps
      .map(
        (step, index) => `
            <div class="loading-step" id="step-${index}">
                <span class="step-icon">⏳</span>
                <span class="step-text">${step}</span>
            </div>
        `
      )
      .join("");
  } else {
    loadingSteps.innerHTML = "";
  }

  overlay.style.display = "flex";
}

function hideLoading() {
  document.getElementById("loadingOverlay").style.display = "none";
}

function updateStep(stepIndex, complete = false) {
  const step = document.getElementById(`step-${stepIndex}`);
  if (step) {
    if (complete) {
      step.classList.add("complete");
      step.querySelector(".step-icon").textContent = "✓";
    } else {
      step.classList.add("active");
      step.querySelector(".step-icon").textContent = "⏳";
    }
  }
}

// Show Result
function showResult(type, title, content) {
  const resultDiv = document.getElementById(`${currentTab}Result`);
  const resultTitle = resultDiv.querySelector(".result-title");
  const resultContent = resultDiv.querySelector(".result-content");

  // Remove previous status classes
  resultDiv.classList.remove("result-success", "result-error");

  // Add new status class
  if (type === "success") {
    resultDiv.classList.add("result-success");
  } else if (type === "error") {
    resultDiv.classList.add("result-error");
  }

  resultTitle.textContent = title;
  resultContent.innerHTML = content;
  resultDiv.style.display = "block";

  // Scroll to result
  resultDiv.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function closeResult(tab) {
  document.getElementById(`${tab}Result`).style.display = "none";
}

// Format IPFS URL
function formatIpfsUrl(ipfsUri) {
  return ipfsUri.replace("ipfs://", "https://gateway.pinata.cloud/ipfs/");
}

// Generate Only (without minting)
async function generateOnly() {
  if (!walletConnected) {
    showNotification(
      "warning",
      "Wallet Required",
      "Please connect your wallet first"
    );
    return;
  }

  const prompt = document.getElementById("prompt").value.trim();
  const name = document.getElementById("name").value.trim();
  const description = document.getElementById("description").value.trim();

  if (!prompt || !name) {
    showNotification(
      "error",
      "Validation Error",
      "Please fill in all required fields"
    );
    return;
  }

  const btn = document.getElementById("generateOnlyBtn");
  btn.disabled = true;

  showLoading("Generating NFT", "Creating your AI-generated image...", [
    "Generating AI image...",
    "Uploading to IPFS...",
    "Creating metadata...",
  ]);

  try {
    updateStep(0);

    const response = await fetch(`${API_BASE_URL}/api/v1/generate-nft`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        prompt: prompt,
        name: name,
        description: description || undefined,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    updateStep(0, true);
    updateStep(1, true);
    updateStep(2, true);

    setTimeout(() => {
      hideLoading();
      showNotification(
        "success",
        "NFT Generated",
        "Your NFT has been generated successfully!"
      );

      showResult(
        "success",
        "NFT Generated Successfully",
        `
                <div class="success-alert">
                    <strong>Success!</strong> Your NFT has been generated and uploaded to IPFS.
                </div>
                
                <div class="nft-preview">
                    <img src="${formatIpfsUrl(
                      data.image_ipfs_uri
                    )}" alt="${name}" class="nft-image" />
                </div>
            `
      );

      document.getElementById("singleNftForm").reset();
    }, 500);
  } catch (error) {
    console.error("Error generating NFT:", error);
    hideLoading();
    showNotification("error", "Generation Failed", error.message);

    showResult(
      "error",
      "Generation Failed",
      `
            <div class="error-alert">
                <strong>Error:</strong> ${error.message}
            </div>
            <p class="mt-2" style="color: var(--text-secondary);">
                Please check the API endpoint and try again.
            </p>
        `
    );
  } finally {
    btn.disabled = false;
  }
}

// Single NFT Form Handler
document
  .getElementById("singleNftForm")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    if (!walletConnected) {
      showNotification(
        "warning",
        "Wallet Required",
        "Please connect your wallet first"
      );
      return;
    }

    const prompt = document.getElementById("prompt").value.trim();
    const name = document.getElementById("name").value.trim();
    const description = document.getElementById("description").value.trim();

    if (!prompt || !name) {
      showNotification(
        "error",
        "Validation Error",
        "Please fill in all required fields"
      );
      return;
    }

    const btn = document.getElementById("generateBtn");
    btn.disabled = true;

    showLoading(
      "Generating and Minting NFT",
      "This process may take 10-30 seconds...",
      ["Generating AI image...", "Uploading to IPFS...", "Creating metadata..."]
    );

    try {
      updateStep(0);

      const response = await fetch(`${API_BASE_URL}/api/v1/generate-nft`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          prompt: prompt,
          name: name,
          description: description || undefined,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(
          error.detail || `HTTP error! status: ${response.status}`
        );
      }

      const data = await response.json();

      updateStep(0, true);
      updateStep(1, true);
      updateStep(2, true);

      setTimeout(() => {
        hideLoading();
        showNotification(
          "success",
          "NFT Minted",
          "Your NFT has been successfully minted!"
        );

        showResult(
          "success",
          "NFT Generated Successfully",
          `
                <div class="success-alert">
                    <strong>Success!</strong> Your NFT has been generated and uploaded to IPFS.
                </div>
                
                <div class="nft-preview">
                    <img src="${formatIpfsUrl(
                      data.image_ipfs_uri
                    )}" alt="${name}" class="nft-image" />
                </div>
            `
        );

        document.getElementById("singleNftForm").reset();
      }, 500);
    } catch (error) {
      console.error("Error generating NFT:", error);
      hideLoading();
      showNotification("error", "Generation Failed", error.message);

      showResult(
        "error",
        "Generation Failed",
        `
            <div class="error-alert">
                <strong>Error:</strong> ${error.message}
            </div>
            <p class="mt-2" style="color: var(--text-secondary);">
                Please check the API endpoint and try again.
            </p>
        `
      );
    } finally {
      btn.disabled = false;
    }
  });

// Batch Form Handler
document.getElementById("batchForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  if (!walletConnected) {
    showNotification(
      "warning",
      "Wallet Required",
      "Please connect your wallet first"
    );
    return;
  }

  const promptsText = document.getElementById("prompts").value.trim();
  const prompts = promptsText.split("\n").filter((p) => p.trim().length > 0);

  if (prompts.length === 0) {
    showNotification(
      "error",
      "Validation Error",
      "Please enter at least one prompt"
    );
    return;
  }

  if (prompts.length > 10) {
    showNotification(
      "error",
      "Too Many Prompts",
      `Maximum 10 prompts allowed. You entered ${prompts.length}`
    );
    return;
  }

  const btn = document.getElementById("batchBtn");
  btn.disabled = true;

  showLoading(
    "Generating Batch Images",
    `Generating ${prompts.length} image${
      prompts.length > 1 ? "s" : ""
    }... This may take a while.`,
    []
  );

  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/generate-batch`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        prompts: prompts,
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || `HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    setTimeout(() => {
      hideLoading();

      const successCount = data.results.filter(
        (r) => r.status === "success"
      ).length;
      const failCount = data.results.filter((r) => r.status === "error").length;

      showNotification(
        "success",
        "Batch Complete",
        `${successCount} images generated successfully`
      );

      const resultsGrid = data.results
        .map((result, index) => {
          if (result.status === "success") {
            return `
                        <div class="batch-item">
                            <img src="${formatIpfsUrl(
                              result.ipfs_uri
                            )}" alt="Generated image ${index + 1}" />
                            <div class="batch-prompt">${result.prompt}</div>
                            <div style="margin-top: 0.5rem;">
                                <a href="${formatIpfsUrl(
                                  result.ipfs_uri
                                )}" target="_blank" class="metadata-link" style="font-size: 0.875rem;">
                                    View on IPFS
                                </a>
                            </div>
                        </div>
                    `;
          } else {
            return `
                        <div class="batch-item" style="border-color: var(--error);">
                            <div style="padding: 1rem; text-align: center;">
                                <span style="font-size: 2rem;">✕</span>
                                <div class="batch-prompt" style="color: var(--error); margin-top: 0.5rem;">
                                    ${result.prompt}
                                </div>
                                <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.5rem;">
                                    ${result.error || "Generation failed"}
                                </div>
                            </div>
                        </div>
                    `;
          }
        })
        .join("");

      showResult(
        "success",
        "Batch Generation Complete",
        `
                <div class="${failCount > 0 ? "error-alert" : "success-alert"}">
                    <strong>Results:</strong> ${successCount} successful, ${failCount} failed
                </div>
                
                <div class="batch-grid">
                    ${resultsGrid}
                </div>
            `
      );

      document.getElementById("batchForm").reset();
    }, 500);
  } catch (error) {
    console.error("Error generating batch:", error);
    hideLoading();
    showNotification("error", "Batch Failed", error.message);

    showResult(
      "error",
      "Batch Generation Failed",
      `
            <div class="error-alert">
                <strong>Error:</strong> ${error.message}
            </div>
            <p class="mt-2" style="color: var(--text-secondary);">
                Please check the API endpoint and try again.
            </p>
        `
    );
  } finally {
    btn.disabled = false;
  }
});

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  console.log("NFT Minter initialized");
  console.log("API Base URL:", API_BASE_URL);
  checkWalletConnection();
});
