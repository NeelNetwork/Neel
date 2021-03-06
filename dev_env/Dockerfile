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

# This Dockerfile is for running protogen, lint, and unit-tests

FROM ubuntu:xenial

RUN echo "deb apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 8AA7AF1F1091A5FD" && \
    echo 'deb http://repo.sawtooth.me/ubuntu/1.0/stable xenial universe' >> /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -y --allow-unauthenticated -q \
        python3-pip \
        python3-sawtooth-sdk \
        python3-sawtooth-rest-api \
        python3-sawtooth-cli \
        python3-sawtooth-signing \
        cron-apt \
        curl

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash - \
    && apt-get install -y nodejs

RUN pip3 install \
    pylint==1.8.1 \
    pycodestyle==2.3.1 \
    grpcio-tools==1.7.0 \
    nose2==0.7.2 \
    bcrypt \
    pycrypto \
    rethinkdb \
    sanic \
    itsdangerous

WORKDIR /project/neel

ENV PATH $PATH:/project/neel/bin
