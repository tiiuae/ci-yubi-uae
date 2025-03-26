# SPDX-FileCopyrightText: 2023 Technology Innovation Institute (TII)
# SPDX-License-Identifier: Apache-2.0
""" Signature Verification Script """
import argparse

import logging

import sys
import os
import time

import json
import base64
import requests

from sha256tree import sha256sum

LOG = logging.getLogger(os.path.abspath(__file__))


# Default certificate to be used if no argument is given
CERTIFICATE_NAME="INT-Ghaf-Devenv-Common"

# Azure Function (verify-signature) URL
# Please change it based to correspond to your deployment
#URL = "http://localhost:7071/api/VerifySignature"
URL = "https://ghaf-ci-signverify.azurewebsites.net/api/verifysignature"

def main():
    """Send REST API request to VerifySignature Azure Function"""
    path = "."
    certificate_name = CERTIFICATE_NAME
    sigfile = "signature.bin"

    parser = argparse.ArgumentParser(description="Parse arguments")
    parser.add_argument("--keyvault", default="ghaf-devenv-kv", help="Specify the keyvault name. Default is ghaf-devenv-kv.")
    parser.add_argument("--path", default=".",
                        help="Specify the path. Default is current directory.")
    parser.add_argument("--cert", default=CERTIFICATE_NAME, help="Specify the certificate name.")
    parser.add_argument("--sigfile", default="signature.bin", help="Specify the signature file.")

    args = parser.parse_args()

    path=args.path
    certificate_name = args.cert
    sigfile = args.sigfile
    keyvault = args.keyvault

    digest = base64.b64encode(sha256sum(path, 1024 * 1024, True)).decode('utf-8')
    if os.path.getsize(sigfile) != 64:
        LOG.info("Wrong signature size!")
        return -3

    with open(sigfile, "rb") as file:
        sig = file.read()

    signature = base64.b64encode(sig).decode('utf-8')

    data = {
        "keyvault": keyvault,
        "certificateName": certificate_name,
        "Hash": digest,
        "Signature": signature
    }

    headers = {"Content-Type": "application/json"}
    LOG.info (json.dumps(data))

    try:
        status_code=0
        count = 3
        while (status_code!=200 and count > 0):
            response = requests.post(URL, headers=headers, data=json.dumps(data), timeout=20)
            status_code=response.status_code
            if status_code!=200:
                count -= 1
                LOG.error("Error %i Response text: '%s'", status_code, response.text)
                time.sleep(3)
        if count<1:
            LOG.error("All requests failed! Give up.")
            return -5

        LOG.error("Signature verification result: %s", response.json())
        return 0 if response.json().get('is_valid', False) else 1
    except requests.exceptions.RequestException as e:
        LOG.error("An error occurred while making the request: %s", str(e))
        return -2


if __name__ == "__main__":
    sys.exit(main())
