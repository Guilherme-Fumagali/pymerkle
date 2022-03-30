Decoupling commitments from proofs
++++++++++++++++++++++++++++++++++

*Commitments* are by default inscribed in Merkle-proofs. One can
however imagine scenarios where proof validation proceeds against the
root-hash as provided in an independent way (e.g., from a trusted third
party). Moreover, one might desire explicit control over whether
the requested proof is an audit or a consistency proof. It
thus makes sense to decouple commitments from proofs and avail
explicit methods for audit and consistency proof requests.

Note that, remaining at the level of challenge-commitment schema, commitments
can already be ommited from proof generation as follows:

.. code-block:: python

    >>> merkle_proof = tree.merkleProof(challenge, commit=False)
    >>> merkle_proof

        ----------------------------------- PROOF ------------------------------------

        uuid        : 82cd9e02-f8ee-11e9-9e85-701ce71deb6a

        timestamp   : 1572203889 (Sun Oct 27 21:18:09 2019)
        provider    : 8002ea42-f8ee-11e9-9e85-701ce71deb6a

        hash-type   : SHA256
        encoding    : UTF-8
        raw_bytes   : TRUE
        security    : ACTIVATED

        proof-index : 4
        proof-path  :

           [0]   +1   f4f03b7a24e147d418063b4bf46cb26830128033706f8ed062503c7be9b32207
           [1]   +1   f73c75c5b8c061589903b892d366e32272e0915bb9a55528173f46f59f18819b
           [2]   +1   0236486b4a79d4072151b0f873a84470f9b699246824cea4b41f861670f9b298
           [3]   -1   41a4362341b66d09babd8d446ff3b409233afb0384a4b852a483da3ab8dcaf4c
           [4]   +1   770d9762ab112b4b0d4adabd756c57e3fd5fc73b46c5694648a6b949d3482e45
           [5]   +1   c60111d752059e7042c5b4dc2de3dbf5462fb0f4102bf58381b78a671ca4e3d6
           [6]   -1   e1cf3cf7e6245ea3001e717699e29e167d961e1c2b4e98affc8105acf74db7c1
           [7]   -1   cdf58a543b5a0c018455517672ac323dba40461b9df5e1e05b9a76a87d2d5ffe
           [8]   +1   9b792adfe21274a1cdd3ebdcc5209e66676e72dbaca18c226d38f9e4ea9dabb7
           [9]   -1   dc4613426d4293a2786dc3da4c9f5ab94541a78561fd4af9fa8476c7c4940896
          [10]   -1   d1135d516fc6147b90e5d6255aa0b8482613dd29a252ab12e5344d14e98c7878

        commitment  : None

        status      : UNVALIDATED

        -------------------------------- END OF PROOF --------------------------------

    >>>


In this case, proof validation proceeds like in the following sections.


Audit proof
===========

Generating the correct audit proof based upon a provided checksum proves on
behalf of the server that the data, whose digest coincides with this checksum,
has indeed been encrypted into the Merkle-tree. The client (*auditor*)
verifies correctness of proof (and consequently inclusion of their
data among the tree's encrypted records) by validating it against the
Merkle-tree's current root-hash. It is essential that the auditor does *not*
need to reveal the data itself but only their checksum, whereas the server
publishes the least possible encrypted data (at most two checksums stored by
leaves) along with advertising the current root-hash.

Schema
------

The auditor requests from the server to encrypt a record ``x``, that is, to append
the checksum ``y = h(x)`` as a new leaf to the tree (where ``h`` stands for the
tree's hashing machinery). At a later moment, after further records have
possibly been encrypted, the auditor requests from the server to prove that ``x``
has indeed been encrypted by only revealing ``y``. In formal terms,
``y`` is the *challenge* posed by the auditor to the server. Disclosing at most
one checksum submitted by some other client, the server responds with a proof
of encryption ``p``, consisting of a path of basically interior hashes and a rule
for combining them into a single hash. Having knowledge of ``h``, the auditor
is able to apply this rule, that is, to retrieve from ``p`` a single hash and
compare it against the current root-hash ``c`` of the Merkle-tree (in formal
terms, ``c`` is the server's *commitment* to the produced proof). This is the
*validation* procedure, whose success verifies

1. that the data ``x`` has indeed been encrypted by the server and

2. that the server's current root-hash coincides with ``c``.

It should be stressed that by *current* is meant the tree's root-hash
immediately after generating the proof, that is, *before* any other records are
encrypted. How the auditor knows ``c`` (e.g., from the server itself or a
trusted third party) depends on protocol details. Failure of validation implies
that ``x`` has not been encrypted or that the server's current root-hash does
not coincide with ``c`` or both.

Example
-------

Use as follows the `.auditProof`_ method to produce the audit proof based upon a
desired checksum:

.. code-block:: python

    >>> checksum = b'4e467bd5f3fc6767f12f4ffb918359da84f2a4de9ca44074488b8acf1e10262e'
    >>>
    >>> proof = tree.auditProof(checksum)
    >>> proof

        ----------------------------------- PROOF ------------------------------------

        uuid        : 7ec481d4-fb4d-11e9-bc05-701ce71deb6a

        timestamp   : 1572464586 (Wed Oct 30 21:43:06 2019)
        provider    : 3fc2ae14-fb40-11e9-bc05-701ce71deb6a

        hash-type   : SHA256
        encoding    : UTF-8
        raw_bytes   : TRUE
        security    : ACTIVATED

        proof-index : 5
        proof-path  :

           [0]   +1   3f824b56e7de850906e053efa4e9ed2762a15b9171824241c77b20e0eb44e3b8
           [1]   +1   4d8ced510cab21d23a5fd527dd122d7a3c12df33bc90a937c0a6b91fb6ea0992
           [2]   +1   35f75fd1cfef0437bc7a4cae7387998f909fab1dfe6ced53d449c16090d8aa52
           [3]   -1   73c027eac67a7b43af1a13427b2ad455451e4edfcaced8c2350b5d34adaa8020
           [4]   +1   cbd441af056bf79c65a2154bc04ac2e0e40d7a2c0e77b80c27125f47d3d7cba3
           [5]   +1   4e467bd5f3fc6767f12f4ffb918359da84f2a4de9ca44074488b8acf1e10262e
           [6]   -1   db7f4ee8be8025dbffee11b434f179b3b0d0f3a1d7693a441f19653a65662ad3
           [7]   -1   f235a9eb55315c9a197d069db9c75a01d99da934c5f80f9f175307fb6ac4d8fe
           [8]   +1   e003d116f27c877f6de213cf4d03cce17b94aece7b2ec2f2b19367abf914bcc8
           [9]   -1   6a59026cd21a32aaee21fe6522778b398464c6ea742ccd52285aa727c367d8f2
          [10]   -1   2dca521da60bf0628caa3491065e32afc9da712feb38ff3886d1c8dda31193f8

        commitment  : None

        status      : UNVALIDATED

        -------------------------------- END OF PROOF --------------------------------

    >>>

.. _.auditProof: https://pymerkle.readthedocs.io/en/latest/pymerkle.core.html#pymerkle.core.prover.Prover.auditProof

No commitment is by default included in the produced proof (this behaviour may
be controlled via the *commit* kwarg of `.auditProof`_). In order
to validate the proof, we need to manually provide the commitment as follows:

.. code-block:: python

    >>> commitment = tree.get_commitment()
    >>>
    >>> validateProof(proof, commitment)
    True
    >>>

Commiting after encryption of records would have invalidated the proof:

.. code-block:: python

    >>> tree.encryptRecord('some further data...')
    >>> commitment = tree.get_commitment()
    >>>
    >>> validateProof(proof, commitment)
    False
    >>>

Consistency proof
=================

A consistency proof is a proof that the tree's gradual development is
consistent. More accurately, generating the correct consistency proof based
upon a previous state certifies on behalf of the Merkle-tree that its current
state is indeed a possible later stage of the former: no records have been
back-dated and reencrypted into the tree, no encrypted data have been tampered
and the tree has never been branched or forked. Just like with audit proofs,
the server discloses the least possible of leaf checksums
(actually only one) along with advertising the current root-hash.

Schema
------

Let a *monitor* (a client observing the tree's gradual development) have
knowledge of the tree\'s state at some moment. That is, the monitor records the
tree's root-hash at some point of history. At a later moment, after further data
have possible been encrypted, the monitor requests from the server to prove that
their current state is a valid later stage of the recorded one. In formal terms,
the recorded previous state is the *challenge* posed by the monitor to the server.
Disclosing only one leaf checksum, the server responds with a proof ``p``
consisting of a path of basically interior hashes and a rule for combining them into
a single hash. Having knowledge of the tree's hashing machinery, the monitor is
able to apply this rule, that is, to retrieve from ``p`` a single hash and compare
it against the current root-hash ``c`` of the Merkle-tree (in formal terms, ``c``
is the server's *commitment* to the produced proof). This is the *validation*
procedure, whose success verifies

1. that the tree's current state is indeed a possible evolvement of the recorded state

2. that the server's current root-hash coincides with ``c``.

It should be stressed that by *current* is meant the tree's root-hash
immediately after generating the proof, that is, *before* any other records are
encrypted. How the monitor knows ``c`` (e.g., from the server itself or a
trusted third party) depends on protocol details. Failure of validation implies
tamperedness of data encrypted prior to the recorded state or that the
server's current root-hash does not coincide with ``c``, indicating
tamperedness after the recorded state or that the provider of ``c`` should be
mistrusted.


Example
-------

Let the monitor record the tree's current state:

.. code-block:: python

    >>> subhash = tree.rootHash
    >>> subhash = b'8136f96be3d8bcc439a3037adadb166d30c2ddfd26e2e2704ca014486db2389d'

At some later point of history, the server is requested to provide a consistency
proof for the above state. Use the `.consistencyProof`_ method to produce the
desired proof as follows:

.. code-block:: python

    >>>
    >>> proof = tree.consistencyProof(subhash)
    >>> proof

        ----------------------------------- PROOF ------------------------------------

        uuid        : ff4709a5-fb51-11e9-bc05-701ce71deb6a

        timestamp   : 1572466520 (Wed Oct 30 22:15:20 2019)
        provider    : 3fc2ae14-fb40-11e9-bc05-701ce71deb6a

        hash-type   : SHA256
        encoding    : UTF-8
        raw_bytes   : TRUE
        security    : ACTIVATED

        proof-index : 6
        proof-path  :

           [0]   -1   3f824b56e7de850906e053efa4e9ed2762a15b9171824241c77b20e0eb44e3b8
           [1]   -1   426425d89f65c8f9f0afc57afdb26b3473417677be769658f5e96fa31e21c30c
           [2]   -1   8d5fcc20b209edfc773d74846eba025f318f09c15f5d968fcc2a333348c27627
           [3]   -1   2f3e39eadadccd5c7c3df65fd8e7f9a6825078fa0d77e3c0c18d0324e4bdfde4
           [4]   -1   e69c47e7f733969841f6a083bcbe54ec334f86fce2f943039d1c9c8783546663
           [5]   -1   c3676f416977584e9a6dcbe1f145cd0adfe8123b29c39807779d17589836d160
           [6]   -1   506e3bfa7f8088555b9b2bb0e50a31645e6f1a01be44bab70b7ebebc4368ca84

        commitment  : None

        status      : UNVALIDATED

        -------------------------------- END OF PROOF --------------------------------

    >>>

.. _.consistencyProof: https://pymerkle.readthedocs.io/en/latest/pymerkle.core.html#pymerkle.core.prover.Prover.consistencyProof

No commitment is by default included in the produced proof (this behaviour may
be controlled via the *commit* kwarg of `.consistencyProof`_). Validation may
proceed exactly the same way as above (recall that validation mechanisms are
agnostic of whether a proof is the result of an audit or a consistency proof
request). We will here employ a validator for reference.

.. code-block:: python

    >>> from pymerkle import Validator
    >>>
    >>> validator = Validator()
    >>> validator.update(proof)

In order to run the validator, we need to manually provide the commitment
via the *target* kwarg as follows:

.. code-block:: python

    >>> commitment = tree.get_commitment()
    >>>
    >>> validator.run(target=commitment)
    >>>

Finalization of process implies validity of proof against the acclaimed current
root-hash. Commiting after encryption of records would have instead cause the
validator to crash:

.. code-block:: python

    >>> tree.encryptRecord('some further data...')
    >>> commitment = tree.get_commitment()
    >>>
    >>> validator.run(target=commitment)
    Traceback (most recent call last):
    ...    raiseInvalidMerkleProof
    pymerkle.exceptions.InvalidMerkleProof
    >>>
