from brownie import AINFTMinter, accounts, network, config
import os

def get_account():
    """
    Get the appropriate account based on the active network.
    For local networks (ganache/development), use accounts[0].
    For live networks (sepolia), use the account from private key in .env.
    """
    active_network = network.show_active()
    
    if active_network in ["development", "ganache", "ganache-local"]:
        print(f"Using local account: {accounts[0]}")
        return accounts[0]
    else:
        if "PRIVATE_KEY" in os.environ:
            account = accounts.add(config["wallets"]["from_key"])
            print(f"Using account from private key: {account.address}")
            return account
        else:
            raise ValueError("PRIVATE_KEY not found in environment variables. Please set it in your .env file.")

def mint_nft(contract_address, recipient_address, token_uri):
    """
    Mint an NFT using an already deployed contract.
    
    Args:
        contract_address: The address of the deployed AINFTMinter contract
        recipient_address: The address that will receive the NFT
        token_uri: The metadata URI for the NFT (IPFS or HTTP URL)
    
    Usage:
        Local:   brownie run scripts/mint.py mint_nft 0xContractAddress 0xRecipientAddress "ipfs://..."
        Sepolia: brownie run scripts/mint.py mint_nft 0xContractAddress 0xRecipientAddress "ipfs://..." --network sepolia
    """
    account = get_account()
    active_network = network.show_active()
    
    print(f"\n🎨 Minting NFT...")
    print(f"Network: {active_network}")
    print(f"Contract: {contract_address}")
    print(f"Minter: {account.address}")
    print(f"Recipient: {recipient_address}")
    print(f"Token URI: {token_uri}")
    
    # Load the deployed contract
    minter = AINFTMinter.at(contract_address)
    
    # Mint the NFT
    tx = minter.mintNFT(recipient_address, token_uri, {"from": account})
    tx.wait(1)
    
    # Get the token ID from the return value
    token_id = tx.return_value
    
    print(f"\n✅ NFT minted successfully!")
    print(f"Token ID: {token_id}")
    print(f"Owner: {minter.ownerOf(token_id)}")
    print(f"Token URI: {minter.tokenURI(token_id)}")
    print(f"Total Supply: {minter.totalSupply()}")
    
    # For live networks, provide block explorer link
    if active_network == "sepolia":
        print(f"View on Etherscan: https://sepolia.etherscan.io/tx/{tx.txid}")
        print(f"View NFT: https://sepolia.etherscan.io/token/{contract_address}?a={token_id}")
    
    return token_id

def main():
    """
    Example usage - modify these values before running.
    """
    # CHANGE THESE VALUES:
    contract_address = "0x8c07F2Ca4015b71B82784cB578aEAee51fE99E54"  # Your deployed contract address
    
    # Get recipient based on network
    active_network = network.show_active()
    if active_network in ["development", "ganache", "ganache-local"]:
        recipient_address = accounts[1].address  # Use second account on local network
    else:
        recipient_address = get_account().address  # Use deployer on live network
    
    # Example metadata URI (replace with your actual IPFS URI)
    token_uri = "ipfs://QmYourActualTokenMetadataHashHere"
    
    # Mint the NFT
    token_id = mint_nft(contract_address, recipient_address, token_uri)
    
    return token_id
