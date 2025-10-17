from brownie import AINFTMinter, accounts
from pytest import fixture


def test_mintNFT():
    # Arrange
    deployer = accounts[0]
    minter = AINFTMinter.deploy({"from": deployer})
    recipient = accounts[1]
    tokenURI = "https://example.com/nft/1"

    # Act
    tx = minter.mintNFT(recipient, tokenURI, {"from": deployer})
    tx.wait(1)

    # Assert
    tokenId = tx.return_value  # Get the actual token ID returned by mintNFT
    assert minter.ownerOf(tokenId) == recipient
    assert minter.tokenURI(tokenId) == tokenURI
    assert tokenId == 1  # First token should have ID 1



def test_supportsInterface():
    # Arrange
    deployer = accounts[0]
    minter = AINFTMinter.deploy({"from": deployer})
    interface_id_ERC721 = "0x80ac58cd"
    interface_id_ERC721Metadata = "0x5b5e139f"

    # Act & Assert
    assert minter.supportsInterface(interface_id_ERC721)
    assert minter.supportsInterface(interface_id_ERC721Metadata)

def test_totalSupply():
    # Arrange
    deployer = accounts[0]
    minter = AINFTMinter.deploy({"from": deployer})
    recipient = accounts[1]
    tokenURI1 = "https://example.com/nft/1"
    tokenURI2 = "https://example.com/nft/2"

    # Act
    tx1 = minter.mintNFT(recipient, tokenURI1, {"from": deployer})
    tx1.wait(1)
    tx2 = minter.mintNFT(recipient, tokenURI2, {"from": deployer})
    tx2.wait(1)

    # Assert
    assert minter.totalSupply() == 2