# <center>blobdash</center>
<center>

### yet another simple self-hosted dashboard

![UV Badge](https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fastral-sh%2Fuv%2Frefs%2Fheads%2Fmain%2Fassets%2Fbadge%2Fv0.json&style=for-the-badge)
![Python Badge](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2Fthcrt%2Fblobdash%2Frefs%2Fheads%2Fmain%2F.python-version&query=%24&style=for-the-badge&label=Python)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/thcrt/blobdash/build.yml?branch=main&style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fthcrt%2Fblobdash%2Fpkgs%2Fcontainer%2Fblobdash)
![GitHub License](https://img.shields.io/github/license/thcrt/blobdash?style=for-the-badge&link=https%3A%2F%2Fgithub.com%2Fthcrt%2Fblobdash%2Fblob%2Fmain%2FLICENSE)
![GitHub Release](https://img.shields.io/github/v/release/thcrt/blobdash?style=for-the-badge)
![Free Palestine Badge](https://img.shields.io/badge/Free%20-%20Palestine%20-%20red?style=for-the-badge)

</center>

## Installation

Designed to be used with Docker and docker-compose. An example `compose.yaml`:

```yaml
services:
  blobdash:
    image: ghcr.io/thcrt/blobdash:latest  # You should pin a version!
    restart: unless-stopped
    container_name: blobdash

    volumes:
      - ./blobdash.toml:/blobdash.toml
    ports: # If using a reverse proxy, put it in the same network instead
      - '80:8080'
```

Note that you have to create and populate `blobdash.toml` yourself and mount it in the container. The software will not create it automatically, and will throw an error if it isn't present. It checks the root of the container (`/blobdash.toml`) as well as the working directory (which should be `/app/blobdash.toml`).

An example configuration file is in this repository at [`blobdash.example.toml`](./blobdash.example.toml). To get started quickly, copy it and rename the copy to `blobdash.toml` before running `docker compose up`.
