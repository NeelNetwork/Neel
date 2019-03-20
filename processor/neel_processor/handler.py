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

from sawtooth_sdk.processor.exceptions import InvalidTransaction
from sawtooth_sdk.processor.handler import TransactionHandler

from neel_addressing import addresser

from neel_processor.asset import asset_creation
from neel_processor.neel_payload import NeelPayload
from neel_processor.neel_state import NeelState


class NeelHandler(TransactionHandler):

    @property
    def family_name(self):
        return addresser.FAMILY_NAME

    @property
    def namespaces(self):
        return [addresser.NS]

    @property
    def family_versions(self):
        return ['1.0']

    def apply(self, transaction, context):

        state = NeelState(context=context, timeout=2)
        payload = NeelPayload(payload=transaction.payload)

        if payload.is_create_asset():
            asset_creation.handle_asset_creation(
                payload.create_asset(),
                header=transaction.header,
                state=state)
        else:
            raise InvalidTransaction("Transaction payload type unknown.")