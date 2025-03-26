# ci-yubi-uae

YubiHSM/Yubikey related code for CI/CD for sigver in the UAE. Forked from ci-yubi.

## Usage with nix

The `sigver` scripts are callable as nix apps:

```sh
nix run github:tiiuae/ci-yubi-uae#sign -- --help

nix run github:tiiuae/ci-yubi-uae#verify -- --help
```
