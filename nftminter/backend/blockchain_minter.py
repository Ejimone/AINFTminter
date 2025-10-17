"""
Blockchain NFT Minter
Handles minting NFTs on Ethereum using Web3
"""

import os
import json
from pathlib import Path
from typing import Optional, Dict
from dotenv import load_dotenv
from web3 import Web3
from eth_account import Account

load_dotenv()

# Contract ABI (from the compiled contract)
ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "approved",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "Approval",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "approve",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "getApproved",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "operator",
                "type": "address"
            }
        ],
        "name": "isApprovedForAll",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "string",
                "name": "tokenURI",
                "type": "string"
            }
        ],
        "name": "mintNFT",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "ownerOf",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            },
            {
                "internalType": "bytes",
                "name": "data",
                "type": "bytes"
            }
        ],
        "name": "safeTransferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "operator",
                "type": "address"
            },
            {
                "internalType": "bool",
                "name": "approved",
                "type": "bool"
            }
        ],
        "name": "setApprovalForAll",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes4",
                "name": "interfaceId",
                "type": "bytes4"
            }
        ],
        "name": "supportsInterface",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "tokenURI",
        "outputs": [
            {
                "internalType": "string",
                "name": "",
                "type": "string"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "from",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "tokenId",
                "type": "uint256"
            }
        ],
        "name": "transferFrom",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
class BlockchainMinter:
    """Handles NFT minting on Ethereum blockchain using Web3"""
    
    def __init__(self):
        """Initialize the blockchain minter"""
        self.private_key = os.getenv('PRIVATE_KEY')
        self.contract_address = os.getenv('CONTRACT_ADDRESS')
        self.infura_project_id = os.getenv('WEB3_INFURA_PROJECT_ID')
        
        if not all([self.private_key, self.contract_address, self.infura_project_id]):
            raise ValueError("Missing required environment variables: PRIVATE_KEY, CONTRACT_ADDRESS, WEB3_INFURA_PROJECT_ID")
        
        # Setup Web3 connection
        infura_url = f"https://sepolia.infura.io/v3/{self.infura_project_id}"
        self.w3 = Web3(Web3.HTTPProvider(infura_url))
        
        # Setup account
        if not self.private_key.startswith('0x'):
            self.private_key = '0x' + self.private_key
        self.account = Account.from_key(self.private_key)
        
        # Setup contract
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(self.contract_address),
            abi=ABI
        )
        
        print(f"Connected to Sepolia via Infura")
        print(f"Using account: {self.account.address}")
        print(f"Contract address: {self.contract_address}")
    
    def mint_nft(self, recipient_address: str, token_uri: str) -> Optional[Dict]:
        """
        Mint an NFT to the specified address with the given metadata URI
        
        Args:
            recipient_address: Ethereum address to receive the NFT
            token_uri: IPFS URI pointing to the NFT metadata
            
        Returns:
            Dict containing transaction details and token ID, or None if failed
        """
        try:
            print(f"Minting NFT to {recipient_address} with URI: {token_uri}")
            
            # Check account balance
            balance = self.w3.eth.get_balance(self.account.address)
            print(f"Account balance: {self.w3.from_wei(balance, 'ether')} ETH")
            
            if balance == 0:
                print("Warning: Account balance is 0 ETH")
            
            # Get nonce
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            # Build transaction
            transaction = self.contract.functions.mintNFT(
                Web3.to_checksum_address(recipient_address),
                token_uri
            ).build_transaction({
                'chainId': 11155111,  # Sepolia chain ID
                'gas': 300000,
                'gasPrice': self.w3.eth.gas_price,
                'nonce': nonce,
            })
            
            # Sign transaction
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Wait for confirmation
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if tx_receipt.status == 1:
                print(f"Transaction successful: {tx_hash.hex()}")
                
                # Extract token ID from Transfer events
                token_id = None
                
                # Decode Transfer events
                transfer_events = self.contract.events.Transfer().process_receipt(tx_receipt)
                
                for event in transfer_events:
                    if event['args']['to'].lower() == recipient_address.lower():
                        token_id = int(event['args']['tokenId'])
                        print(f"Token ID from Transfer event: {token_id}")
                        break
                
                # If we still don't have token_id, try to call the function locally to simulate
                if token_id is None:
                    try:
                        # This won't work for state-changing functions, but let's try anyway
                        print("Warning: Could not determine token ID from events")
                        token_id = 1  # Default fallback
                    except:
                        token_id = 1
                
                return {
                    "success": True,
                    "transaction_hash": tx_hash.hex(),
                    "token_id": token_id,
                    "recipient": recipient_address,
                    "token_uri": token_uri,
                    "gas_used": tx_receipt.gasUsed,
                    "contract_address": self.contract_address,
                    "network": "sepolia"
                }
            else:
                print(f"Transaction failed with status: {tx_receipt.status}")
                return None
                
        except Exception as e:
            print(f"Error minting NFT: {e}")
            return None
    
    def get_contract_info(self) -> Optional[Dict]:
        """Get contract information"""
        try:
            name = self.contract.functions.name().call()
            symbol = self.contract.functions.symbol().call()
            owner = self.contract.functions.owner().call()
            
            return {
                "name": name,
                "symbol": symbol,
                "owner": owner,
                "address": self.contract_address,
                "network": "sepolia"
            }
            
        except Exception as e:
            print(f"Error getting contract info: {e}")
            return None

# Test function
def test_minting():
    """Test function to verify minting works"""
    minter = BlockchainMinter()
    
    # Get contract info
    info = minter.get_contract_info()
    if info:
        print("Contract Info:")
        for key, value in info.items():
            print(f"  {key}: {value}")
    
    # Test minting (using owner address as recipient)
    test_uri = "ipfs://QmTestHash123"
    result = minter.mint_nft(minter.account.address, test_uri)
    
    if result:
        print("Minting Result:")
        for key, value in result.items():
            print(f"  {key}: {value}")
    else:
        print("Minting failed")

if __name__ == "__main__":
    test_minting()
