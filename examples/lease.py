###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Crossbar.io Technologies GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

from twisted.internet.task import react
from twisted.internet.defer import inlineCallbacks

import txaio
from txaioetcd import Client
from txaioetcd.types import Expired


@inlineCallbacks
def main(reactor):
    # create an etcd client
    etcd = Client(reactor, u'http://localhost:2379')

    # retrieve etcd cluster status
    status = yield etcd.status()
    print(status)

    print('creating lease with 5s TTL')
    lease = yield etcd.lease(5)
    print(lease)

    print('refreshing lease every 4s, 5 times ..')
    for i in range(5):
        rev = yield lease.refresh()
        print(rev)
        yield txaio.sleep(4)

    print('sleeping for 6s ..')
    yield txaio.sleep(6)

    print('refreshing lease')
    try:
        yield lease.refresh()
    except Expired:
        print('leave expired (expected)')

    print('creating lease with 5s TTL')
    lease = yield etcd.lease(5)
    print(lease)

    print('sleeping for 2s ..')
    yield txaio.sleep(2)

    print('revoking lease')
    res = yield lease.revoke()
    print(res)
    print('refreshing lease')

    try:
        yield lease.refresh()
    except Expired:
        print('leave expired (expected)')

if __name__ == '__main__':
    txaio.start_logging(level='info')
    react(main)
