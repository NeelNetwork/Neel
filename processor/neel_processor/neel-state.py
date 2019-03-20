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

from marketplace_addressing import addresser
from marketplace_processor.protobuf import asset_pb2
from marketplace_processor.protobuf import rule_pb2


class NeelState(object):

    def __init__(self, context, timeout=2):
        self._context = context
        self._timeout = timeout
        self._state_entries = []

    def get_asset(self, name):
        address = addresser.make_asset_address(asset_id=name)

        self._state_entries.extend(self._context.get_state(
            addresses=[address],
            timeout=self._timeout))

        return self._get_asset(address=address, name=name)

    def _get_asset(self, address, name):

        container = _get_asset_container(self._state_entries, address)

        asset = None
        try:
            asset = _get_asset_from_container(container, name)
        except KeyError:
            # We are fine with returning None for an asset that doesn't exist
            pass
        return asset

    def set_asset(self, name, description, owners, rules):
        address = addresser.make_asset_address(name)

        container = _get_asset_container(self._state_entries, address)

        try:
            asset = _get_asset_from_container(container, name)
        except KeyError:
            asset = container.entries.add()

        asset.name = name
        asset.description = description
        asset.owners.extend(owners)
        asset.rules.extend(rules)

        state_entries_send = {}
        state_entries_send[address] = container.SerializeToString()
        return self._context.set_state(
            state_entries_send,
            self._timeout)

    def get_account(self, public_key):
        address = addresser.make_account_address(account_id=public_key)

        self._state_entries.extend(self._context.get_state(
            addresses=[address],
            timeout=self._timeout))

        container = _get_account_container(self._state_entries, address)
        account = None
        try:
            account = _get_account_from_container(
                container,
                identifier=public_key)
        except KeyError:
            # We are fine with returning None for an account that doesn't
            # exist in state.
            pass
        return account


def _get_asset_container(state_entries, address):
    try:
        entry = _find_in_state(state_entries, address)
        container = asset_pb2.AssetContainer()
        container.ParseFromString(entry.data)
    except KeyError:
        container = asset_pb2.AssetContainer()
    return container


def _get_asset_from_container(container, name):
    for asset in container.entries:
        if asset.name == name:
            return asset
    raise KeyError(
        "Asset with name {} is not in container".format(name))


def _get_account_container(state_entries, address):
    try:
        entry = _find_in_state(state_entries, address)
        container = account_pb2.AccountContainer()
        container.ParseFromString(entry.data)
    except KeyError:
        container = account_pb2.AccountContainer()

    return container


def _get_account_from_container(container, identifier):
    for account in container.entries:
        if account.public_key == identifier:
            return account
    raise KeyError(
        "Account with identifier {} is not in container.".format(identifier))


def _find_in_state(state_entries, address):
    for entry in state_entries:
        if entry.address == address:
            return entry
    raise KeyError("Address {} not found in state".format(address))