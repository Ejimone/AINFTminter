from brownie import AINFTMinter, accounts, network, config
import os

def get_account():
    active_network = network.show_active()
    
    if active_network in ["development", "ganache", "ganache-local"]:
        # Local network - use pre-funded account
        print(f"Using local account: {accounts[0]}")
        return accounts[0]
    else:
        # Live network - use account from private key
        if "PRIVATE_KEY" in os.environ:
            account = accounts.add(config["wallets"]["from_key"])
            print(f"Using account from private key: {account.address}")
            return account
        else:
            raise ValueError("PRIVATE_KEY not found in environment variables. Please set it in your .env file.")

def deploy():
    """
    Deploy the AINFTMinter contract.
    Works with both local (ganache) and live (sepolia) networks.
    
    Usage:
        Local:   brownie run scripts/deploy.py
        Sepolia: brownie run scripts/deploy.py --network sepolia
    """
    try:
        deployer = get_account()
        active_network = network.show_active()
        
        print(f"Deploying AINFTMinter contract...")
        print(f"Network: {active_network}")
        print(f"Deployer: {deployer.address}")
        print(f"Balance: {deployer.balance() / 1e18} ETH")
        
        # Deploy the contract
        minter = AINFTMinter.deploy({"from": deployer})
        
        print(f"\n✅ Contract deployed successfully!")
        print(f"Contract address: {minter.address}")
        print(f"Network: {active_network}")
        print(f"Deployer: {deployer.address}")
        
        # For live networks, provide block explorer link
        if active_network == "sepolia":
            print(f"View on Etherscan: https://sepolia.etherscan.io/address/{minter.address}")
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
    return minter



def mintNFT(minter, recipient, tokenURI):
    try:
        """Mint an NFT to the specified recipient with the given tokenURI."""
        deployer = get_account()
        print(f"Minting NFT to {recipient} with tokenURI: {tokenURI}")
        tx = minter.mintNFT(recipient, tokenURI, {"from": deployer})
        tx.wait(1)
        tokenId = tx.return_value
        print(f"✅ NFT minted! Token ID: {tokenId}")
        return tokenId
    except Exception as e:
        print(f"❌ Minting failed: {e}")
        return None
    


def supportsInterface(minter, interface_id):
    try:
        """Check if the contract supports a given interface ID."""
        result = minter.supportsInterface(interface_id)
        print(f"Interface {interface_id} supported: {result}")
        return result
    except Exception as e:
        print(f"❌ supportsInterface check failed: {e}")



def totalSupply(minter):
    try:
        """Get the total supply of minted NFTs."""
        supply = minter.totalSupply()
        print(f"Total Supply: {supply}")
        return supply
    except Exception as e:
        print(f"❌ totalSupply check failed: {e}")
        return None


def main():
    """Main function to run the deployment."""
    minter = deploy()
    
    # Optional: Demonstrate minting (comment out for production deployment)
    # Uncomment the lines below to test minting after deployment
    """
    active_network = network.show_active()
    deployer = get_account()
    
    # For local networks, mint to accounts[1], for live networks, mint to deployer
    if active_network in ["development", "ganache", "ganache-local"]:
        recipient = accounts[1].address
    else:
        recipient = deployer.address  # On live networks, mint to yourself
    
    tokenURI = "ipfs://QmYourTokenURIHere"
    mintNFT(minter, recipient, tokenURI)
    supportsInterface(minter, "0x80ac58cd")  # ERC721 interface
    totalSupply(minter)
    """
    
    return minter

