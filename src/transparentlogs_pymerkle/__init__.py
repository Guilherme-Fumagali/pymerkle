"""
merkle-tree cryptography
"""

from transparentlogs_pymerkle.tree import MerkleTree
from transparentlogs_pymerkle.proof import MerkleProof, verify_inclusion, verify_consistency


__version__ = '4.0.0'

__all__ = (
    'MerkleTree',
    'MerkleProof',
    'verify_inclusion',
    'verify_consistency',
)
