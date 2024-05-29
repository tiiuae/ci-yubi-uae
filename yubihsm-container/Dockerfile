# SPDX-FileCopyrightText: 2023 Technology Innovation Institute (TII)
# SPDX-License-Identifier: Apache-2.0

FROM ubuntu:jammy

ENV YUBIHSM_PKCS11_CONF=/app/pkcs11.conf

# Install dependencies
RUN DEBIAN_FRONTEND=noninteractive apt-get update && apt-get install -y \
    software-properties-common \
    usbutils \
    wget \
    pkgconf libssl-dev opensc \
    && rm -rf /var/lib/apt/lists/*
    
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y apt-utils
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y libpcsclite1 libcurl4 libusb-1.0-0 libedit2

# Set working directory
WORKDIR /app


COPY engine.conf /app/engine.conf
COPY pkcs11.conf /app/pkcs11.conf

RUN wget https://github.com/OpenSC/libp11/releases/download/libp11-0.4.12/libp11-0.4.12.tar.gz
RUN tar -xzvf libp11-0.4.12.tar.gz
WORKDIR /app/libp11-0.4.12
RUN ./configure
RUN make
RUN make install

WORKDIR /app

RUN wget https://developers.yubico.com/YubiHSM2/Releases/yubihsm2-sdk-2023-11-ubuntu2310-amd64.tar.gz
RUN tar -xzvf yubihsm2-sdk-2023-11-ubuntu2310-amd64.tar.gz
WORKDIR /app/yubihsm2-sdk
RUN rm -rf libyubihsm-dev_2.4.2_amd64.deb
RUN dpkg -i *.deb

RUN echo 'alias openssl="OPENSSL_CONF=/app/engine.conf openssl"' >> ~/.bashrc
RUN echo 'alias p="pkcs11-tool --module /usr/lib/x86_64-linux-gnu/pkcs11/yubihsm_pkcs11.so"' >> ~/.bashrc

WORKDIR /app
