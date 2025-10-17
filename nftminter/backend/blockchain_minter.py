"""
Blockchain NFT Minter
Handles minting NFTs on Ethereum using Brownie
"""

import os
import sys
from pathlib import Path
from typing import Optional, Dict
from dotenv import load_dotenv

# Add parent directory to path to import brownie
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

load_dotenv()

# Import brownie and load the project
import brownie
from brownie import accounts, network

# Load the Brownie project
try:
    brownie_project_path = project_root
    if not brownie.project.check_for_project(brownie_project_path):
        raise ValueError(f"No Brownie project found at {brownie_project_path}")
    
    # Load project to get compiled contracts
    project = brownie.project.load(brownie_project_path, name="AINFTMinterProject")
    # Now we can access AINFTMinter from the loaded project
    AINFTMinter = project.AINFTMinter
except Exception as e:
    print(f"⚠️  Warning: Could not load Brownie project: {e}")
    AINFTMinter = None


class BlockchainMinter:
    """Handle NFT minting on Ethereum blockchain"""
    
    def __init__(self, contract_address: Optional[str] = None, network: str = "sepolia"):
        """
        Initialize blockchain minter.
        
        Args:
            contract_address: Deployed AINFTMinter contract address
            network: Network to use (ganache-local, sepolia, etc.)
        """
        self.contract_address = contract_address or os.getenv("CONTRACT_ADDRESS")
        if not self.contract_address:
            raise ValueError(
                "Contract address not provided. Either pass it or set CONTRACT_ADDRESS in .env"
            )
        
        self.network = network
        self.private_key = os.getenv("PRIVATE_KEY")
        
        if not self.private_key:
            raise ValueError("PRIVATE_KEY not found in .env file")
    
    def mint_nft(self, recipient_address: str, token_uri: str) -> Dict[str, any]:
        """
        Mint an NFT on the blockchain.
        
        Args:
            recipient_address: Address to receive the NFT
            token_uri: IPFS URI for the NFT metadata
            
        Returns:
            dict: Minting result with token ID and transaction hash
        """
        print(f"\n🔗 Minting NFT on blockchain...")
        print(f"   Network: {self.network}")
        print(f"   Contract: {self.contract_address}")
        print(f"   Recipient: {recipient_address}")
        print(f"   Token URI: {token_uri}")
        
        try:
            if AINFTMinter is None:
                raise Exception("AINFTMinter contract not loaded. Make sure Brownie project is compiled.")
            
            # Connect to network - handle both cases
            try:
                active_network = network.show_active()
                if active_network != self.network:
                    print(f"   Switching from {active_network} to {self.network}...")
                    network.disconnect()
                    network.connect(self.network)
            except Exception:
                # Not connected to any network yet
                print(f"   Connecting to {self.network}...")
                network.connect(self.network)
            
            print(f"   ✅ Connected to {network.show_active()}")
            
            # Get account from private key
            account = accounts.add(self.private_key)
            print(f"   Minter: {account.address}")
            
            # Load the deployed contract
            minter = AINFTMinter.at(self.contract_address)
            
            # Mint the NFT
            print("⏳ Sending transaction...")
            tx = minter.mintNFT(recipient_address, token_uri, {"from": account})
            tx.wait(1)
            
            # Get the token ID from the Transfer event (emitted by ERC721)
            # Transfer event: Transfer(address indexed from, address indexed to, uint256 indexed tokenId)
            token_id = None
            if 'Transfer' in tx.events:
                # tx.events can be either a dict of lists or an EventDict
                transfer_events = tx.events['Transfer']
                # Handle both single event and list of events
                if not isinstance(transfer_events, list):
                    transfer_events = [transfer_events]
                
                for event in transfer_events:
                    if event['to'] == recipient_address:
                        token_id = event['tokenId']
                        break
            
            if token_id is None:
                # Fallback: get total supply (works if this is the latest mint)
                print("   ⚠️  Could not find Transfer event, using totalSupply()")
                token_id = minter.totalSupply()
            
            print(f"\n✅ NFT minted successfully!")
            print(f"   Token ID: {token_id}")
            print(f"   Transaction: {tx.txid}")
            
            # Get block explorer link
            explorer_url = self._get_explorer_url(tx.txid, token_id)
            
            result = {
                "success": True,
                "token_id": token_id,
                "transaction_hash": tx.txid,
                "contract_address": self.contract_address,
                "recipient": recipient_address,
                "token_uri": token_uri,
                "network": self.network,
                "explorer_url": explorer_url
            }
            
            if explorer_url:
                print(f"   View on Explorer: {explorer_url}")
            
            return result
        
        except Exception as e:
            print(f"❌ Error minting NFT: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _get_explorer_url(self, tx_hash: str, token_id: int) -> Optional[str]:
        """Get block explorer URL for the transaction"""
        explorers = {
            "sepolia": f"https://sepolia.etherscan.io/tx/{tx_hash}",
            "mainnet": f"https://etherscan.io/tx/{tx_hash}",
            "goerli": f"https://goerli.etherscan.io/tx/{tx_hash}",
        }
        return explorers.get(self.network)
    
    def get_nft_details(self, token_id: int) -> Dict[str, any]:
        """
        Get details of a minted NFT.
        
        Args:
            token_id: The token ID to query
            
        Returns:
            dict: NFT details
        """
        try:
            if AINFTMinter is None:
                raise Exception("AINFTMinter contract not loaded")
            
            # Connect to network if not connected
            try:
                active_network = network.show_active()
                if active_network != self.network:
                    network.disconnect()
                    network.connect(self.network)
            except Exception:
                network.connect(self.network)
            
            minter = AINFTMinter.at(self.contract_address)
            
            owner = minter.ownerOf(token_id)
            token_uri = minter.tokenURI(token_id)
            
            return {
                "success": True,
                "token_id": token_id,
                "owner": owner,
                "token_uri": token_uri,
                "contract_address": self.contract_address
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Standalone function for quick minting
def mint_nft_to_blockchain(
    token_uri: str,
    recipient_address: Optional[str] = None,
    contract_address: Optional[str] = None,
    network_name: str = "sepolia"
) -> Dict[str, any]:
    """
    Quick function to mint an NFT to the blockchain.
    
    Args:
        token_uri: IPFS URI for the NFT metadata
        recipient_address: Optional recipient (defaults to minter)
        contract_address: Optional contract address (uses env var if not provided)
        network_name: Network to use
        
    Returns:
        dict: Minting result
    """
    try:
        minter = BlockchainMinter(contract_address=contract_address, network=network_name)
        
        # Use minter address as recipient if not specified
        if not recipient_address:
            recipient_address = accounts.add(os.getenv("PRIVATE_KEY")).address
        
        return minter.mint_nft(recipient_address, token_uri)
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# Example usage
if __name__ == "__main__":
    # Test minting (requires PRIVATE_KEY and CONTRACT_ADDRESS in .env)
    print("🧪 Testing blockchain minter...")
    
    test_uri = "ipfs://QmTest123..."  # Replace with actual IPFS URI
    
    try:
        result = mint_nft_to_blockchain(test_uri)
        if result["success"]:
            print(f"\n✅ Minting test successful!")
            print(f"Token ID: {result['token_id']}")
        else:
            print(f"\n❌ Minting failed: {result['error']}")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
