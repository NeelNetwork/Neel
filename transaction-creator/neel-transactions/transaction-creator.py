#   Copyright (c) 2019 Neel Network

#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:

#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.

#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.
#   --------------------------------------------------------------------------

from neel_addressing import addresser

from neel_transactions.common import make_header_and_batch
from neel_transactions.protobuf import payload_pb2


def create_asset(txn_key, batch_key, name, description, rules):
    """Create a CreateAsset txn and wrap it in a batch and list.
    Args:
        txn_key (sawtooth_signing.Signer): The txn signer key pair.
        batch_key (sawtooth_signing.Signer): The batch signer key pair.
        name (str): The name of the asset.
        description (str): A description of the asset.
        rules (list): List of protobuf.rule_pb2.Rule
    Returns:
        tuple: List of Batch, signature tuple
    """

    inputs = [addresser.make_asset_address(asset_id=name),
              addresser.make_account_address(
                  account_id=txn_key.get_public_key().as_hex())]

    outputs = [addresser.make_asset_address(asset_id=name)]

    asset = payload_pb2.CreateAsset(
        name=name,
        description=description,
        rules=rules
    )

    payload = payload_pb2.TransactionPayload(
        payload_type=payload_pb2.TransactionPayload.CREATE_ASSET,
        create_asset=asset)

    return make_header_and_batch(
        payload=payload,
        inputs=inputs,
        outputs=outputs,
        txn_key=txn_key,
        batch_key=batch_key)


