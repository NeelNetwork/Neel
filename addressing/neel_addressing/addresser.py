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

import enum
import hashlib


FAMILY_NAME = 'neel'


NS = hashlib.sha512(FAMILY_NAME.encode()).hexdigest()[:6]


class AssetSpace(enum.IntEnum):
    START = 1
    STOP = 50


@enum.unique
class AddressSpace(enum.IntEnum):
    ASSET = 0

    OTHER_FAMILY = 100


def _hash(identifier):
    return hashlib.sha512(identifier.encode()).hexdigest()


def _compress(address, start, stop):
    return "%.2X".lower() % (int(address, base=16) % (stop - start) + start)


def make_asset_address(asset_id):
    full_hash = _hash(asset_id)

    return NS + _compress(
        full_hash,
        AssetSpace.START,
        AssetSpace.STOP) + full_hash[:62]


def make_account_address(account_id):
    full_hash = _hash(account_id)

    return NS + _compress(
        full_hash,
        50,
        125) + full_hash[:62]


def _contains(num, space):
    return space.START <= num < space.STOP


def address_is(address):

    if address[:len(NS)] != NS:
        return AddressSpace.OTHER_FAMILY

    infix = int(address[6:8], 16)
    
    if _contains(infix, AssetSpace):
        result = AddressSpace.ASSET
    else:
        result = AddressSpace.OTHER_FAMILY

    return result