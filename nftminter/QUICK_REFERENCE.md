# Quick Reference Guide

## Deployment Commands

### Deploy to Local Network (Ganache)

```bash
brownie run scripts/deploy.py
```

- Uses built-in Ganache
- No setup required
- Fast and free
- Perfect for testing

### Deploy to Sepolia Testnet

```bash
brownie run scripts/deploy.py --network sepolia
```

- Requires `.env` file with `PRIVATE_KEY`
- Needs Sepolia ETH from faucet
- Real blockchain deployment
- Permanent and public

## Minting NFTs

### Update Contract Address in mint.py

Open `scripts/mint.py` and update the contract address:

```python
contract_address = "0xYourDeployedContractAddress"
```

### Mint on Local Network

```bash
brownie run scripts/mint.py
```

### Mint on Sepolia

```bash
brownie run scripts/mint.py --network sepolia
```

## Recent Deployments

### Sepolia Testnet:

- **Contract 1**: `0x8c07F2Ca4015b71B82784cB578aEAee51fE99E54`
  - [View on Etherscan](https://sepolia.etherscan.io/address/0x8c07F2Ca4015b71B82784cB578aEAee51fE99E54)
- **Contract 2**: `0x49814e7E1d141F6bE2b21b6C4433D083A6A486c0`
  - [View on Etherscan](https://sepolia.etherscan.io/address/0x49814e7E1d141F6bE2b21b6C4433D083A6A486c0)

## Testing

```bash
brownie test tests/test_AINFTMinter.py -v
```

## Network Differences

| Feature        | Local (Ganache)       | Sepolia              |
| -------------- | --------------------- | -------------------- |
| Speed          | Instant               | ~12 seconds/block    |
| Cost           | Free                  | Requires testnet ETH |
| Persistence    | Temporary             | Permanent            |
| Accounts       | Pre-funded (1000 ETH) | Need private key     |
| Block Explorer | N/A                   | Etherscan            |

## Get Sepolia ETH

- https://sepoliafaucet.com/
- https://faucet.quicknode.com/ethereum/sepolia
- https://www.alchemy.com/faucets/ethereum-sepolia

## Environment Variables

Create `.env` file:

```
PRIVATE_KEY=your_private_key_without_0x_prefix
```

⚠️ **Security**: Never commit `.env` file or share private keys!
