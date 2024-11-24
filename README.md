# <center>blobdash</center>
<center>

### yet another simple self-hosted dashboard

![UV Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fastral-sh%2Fuv%2Frefs%2Fheads%2Fmain%2Fassets%2Fbadge%2Fv0.json&style=for-the-badge)
![Python Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fthcrt%2Fblobdash%2Frefs%2Fheads%2Fmain%2F.python-version&query=%24&style=for-the-badge&label=Python)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/thcrt/blobdash/build.yml?branch=main&style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fthcrt%2Fblobdash%2Fpkgs%2Fcontainer%2Fblobdash)
![GitHub License](https://img.shields.io/github/license/thcrt/blobdash?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fthcrt%2Fblobdash%2Fblob%2Fmain%2FLICENSE)
![GitHub Release](https://img.shields.io/github/v/release/thcrt/blobdash?style=for-the-badge)
![Free Palestine Badge](https://img.shields.io/badge/Free%20-%20Palestine%20-%20red?style=for-the-badge)

<img style="display: inline; height: 15rem;" src="./docs/screenshots/desktop.png"> <img style="display: inline; height: 15rem;" src="./docs/screenshots/phone-lg.png"> <img style="display: inline; height: 15rem;" src="./docs/screenshots/phone-sm.png">


</center>

## Installation

Designed to be used with Docker and docker-compose. An example `compose.yaml` file can be found at [`docs/examples/compose.example.yaml`](docs/examples/compose.example.yaml).

## Configuration

Blobdash uses [TOML](https://toml.io/) for configuration. It checks for a file named `blobdash.toml`
both in its working directory (in the Docker image, this is at `/app/blobdash.toml`) and in the root
directory (`/blobdash.toml`). If both are present, values in `/blobdash.toml` will override those
set in `/app/blobdash.toml`.

An example configuration file is present in this repository at
[`docs/examples/blobdash.example.toml`](docs/examples/blobdash.example.toml). Documentation on the
configuration file is present at [`docs/configuration.md`](docs/configuration.md).
