"""
merkle-tree cryptography
"""

from pymerkle_logsTransparentes.tree import MerkleTree
from pymerkle_logsTransparentes.proof import MerkleProof, verify_inclusion, verify_consistency


__version__ = '4.0.0'

__all__ = (
    'MerkleTree',
    'MerkleProof',
    'verify_inclusion',
    'verify_consistency',
)
