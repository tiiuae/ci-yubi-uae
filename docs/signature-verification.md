# Signature Verification Script Documentation

## Overview

The verify.py script verifies the authenticity of a digital signature by calling an Azure Function, which interacts with Azure Key Vault for the actual signature verification process. The result is provided in a JSON format, where the key is_valid indicates whether the signature is valid (true) or not (false).

## Prerequisites

- python3 environment is required with requests module installed.
- Azure Function is offering public access, thus no special access on cloud level is needed.

## Usage

### Command-line Parameters

The script accepts the following parameters:

    --path:
        Description: Specify the directory and filename to verify.
        Default: The current directory (.).
        Usage:
        Provide the path where and filename (optional) to be verified. The script can verify both files and folders.

    --cert:
        Description: (optional) Specify the name of the certificate stored in Azure Key Vault that is used to verify the signature.
        Default: INT-Ghaf-Devenv-Common.
        Usage:
        If no certificate name is provided, the script will default to using INT-Ghaf-Devenv-Common certificate stored in Azure Key Vault. You do not need to have the certificate locally.

    --sigfile:
        Description: Specify the binary file that contains the digital signature.
        Default: signature.bin.
        Usage:
        If your signature file has a different name or location, specify it using this argument.

### Example Command

`python verify.py --path=/path/to/your/file --cert=mycert --sigfile=custom_signature.bin`

In this example, the script will:

    Verify the signature of the file /path/to/your/file.
    Use the mycert certificate stored in Azure Key Vault for verification.
    Use custom_signature.bin as the signature file.

If the certificate name is omitted, the script will use the default INT-Ghaf-Devenv-Common certificate:

`python verify.py --path /path/to/your/file --sigfile custom_signature.bin`

Output

The script generates a JSON file that contains 'is_valid' key:

    is_valid: A boolean value indicating whether the signature is valid (true) or invalid (false).

Example Output

`{'is_valid': True, 'message': 'Signature verification result'}`

or

`{'is_valid': False, 'message': 'Signature verification result'}`

## Usage on Ubuntu

1. Ensure Python3 is installed: On most Ubuntu systems, Python3 is pre-installed. Verify by running:

`python3 --version`

If not, you can install it by running:

`sudo apt-get install python3`

2. Set up a Python virtual environment (recommended to avoid conflicts):

`python3 -m venv verify-env
source verify-env/bin/activate`

3. Install required dependencies:

`pip3 install requests`

4. Run the script

`python3 verify.py --path=<file_path> --sigfile=<signature_file>`

Replace <file_path> and <signature_file> with the respective paths to your image and signature files.

## Usage on Ghaf / Nix:

If you are using Ghaf or Nix, you can utilize the flake to simplify the process. No need to manually set up environment:

`nix run github:tiiuae/ci-yubi/bdb2dbf#verify -- --path=<file_path> --sigfile=<signature_file>`

Replace <file_path> and <signature_file> with the respective paths to your image and signature files.

The above command will handle everything, including environment setup.

## Conclusion

This signature verification script allows you to securely verify digital signatures using certificates stored in Azure Key Vault. By providing the path to the file, the certificate name, and the signature file, you can quickly determine the validity of a signature in a standardized JSON format.
