"""
Hashing machinery for data insertion and proof verification
"""

import hashlib
from pymerkle.constants import ENCODINGS, ALGORITHMS


class UnsupportedParameter(Exception):
    """
    Raised when a hashing engine with unsupported parameters is requested
    """
    pass


class HashEngine:
    """
    :param algorithm: [optional] hash algorith
    :type algorithm: str
    :param encoding: [optional] encoding scheme
    :type encoding: str
    :param security: [optional] defense against 2nd-preimage attack
    :type security: bool
    """

    def __init__(self, algorithm='sha256', encoding='utf-8', security=True):
        algorith, encoding = self.validate_parameters(algorithm, encoding)

        self.algorithm = algorithm
        self.encoding = encoding
        self.security = security

        self.prefx00 = '\x00'.encode(encoding) if security else bytes()
        self.prefx01 = '\x01'.encode(encoding) if security else bytes()


    @staticmethod
    def validate_parameters(algorithm, encoding):
        validated = []

        for (provided, supported) in (
            (algorithm, ALGORITHMS),
            (encoding, ENCODINGS)
        ):
            normalized = provided.lower().replace('-', '_')
            if normalized not in supported:
                raise UnsupportedParameter('%s is not supported' % provided)

            validated += [normalized]

        return validated


    def consume(self, buffer):
        """
        Returns the hash digest of the provided input

        :param buffer:
        :type buffer: bytes
        :rtype: bytes
        """
        hasher = getattr(hashlib, self.algorithm)()

        update = hasher.update
        chunksize = 1024
        offset = 0
        chunk = buffer[offset: chunksize]
        while chunk:
            update(chunk)
            offset += chunksize
            chunk = buffer[offset: offset + chunksize]

        checksum = hasher.hexdigest()

        return checksum.encode(self.encoding)


    def hash_entry(self, data):
        """
        Compute the hash of the provided data

        .. note:: Prepends ``\\x00`` if security mode is enabled

        :type data: bytes or str
        :rtype: bytes
        """
        if not isinstance(data, bytes):
            data = data.encode(self.encoding)

        buffer = self.prefx00 + data
        digest = self.consume(buffer)

        return digest


    def hash_pair(self, left, right):
        """
        Compute the hash of the concatenation of the provided values

        .. note:: Prepends ``\\x01`` to each argument if security mode is
            enabled

        :param left: first value
        :type left: bytes
        :param right: second value
        :type right: bytes
        :rtype: bytes
        """
        buffer = self.prefx01 + left + self.prefx01 + right
        digest = self.consume(buffer)

        return digest
