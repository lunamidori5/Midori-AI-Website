+++
disableToc = false
title = "PixelGen OS"
weight = 2
+++

![pixelgen-logo](https://tea-cup.midori-ai.xyz/download/pixelgen-banner.png)

## PixelGen OS: A Docker-Optimized Gentoo Linux Distribution

PixelGen OS is a Gentoo Linux-based operating system designed for advanced users who want maximum performance and customization in containerized environments. It leverages Gentoo’s source-based package management within Docker containers, providing flexible, optimized builds for specialized workloads.

**Key Features:**

- **Gentoo-Based:** Built on Gentoo Linux for deep system customization.
- **Source-Based Compilation:** Compile packages with your preferred `CFLAGS`, `USE` flags, and optimization settings.
- **Docker-Optimized:** Designed for consistent container deployments while keeping Gentoo’s flexibility.
- **Portage Package Manager:** Uses Portage (`emerge`) for fine-grained dependency and build control.
- **Pacaptr Compatibility Layer:** Includes `pacaptr` for `yay`/`pacman`-style command aliases to ease transitions.
- **Performance-Focused:** Ships with an opinionated `make.conf` you can tune for your target hardware.

## Getting Started

{{< tabs >}}
{{% tab title="Docker Compose" %}}

### 1. Create a `docker-compose.yaml`

```yaml
services:
  pixelgen-os:
    image: lunamidori5/pixelgen
    tty: true
    restart: always
    privileged: true
    command: ["sleep", "infinity"]
```

### 2. Start the container in detached mode

```bash
docker compose up -d
```

### 3. Access the container shell

```bash
docker compose exec pixelgen-os /bin/bash
```

{{% /tab %}}
{{% tab title="Build Locally" %}}

### 1. Clone the repository

```bash
git clone https://github.com/lunamidori5/Midori-AI-Pixelarch-OS.git
```

### 2. Build the PixelGen image

```bash
cd Midori-AI-Pixelarch-OS/pixelgen_os
docker build -t pixelgen -f gentoo_dockerfile .
```

### 3. Run the image

```bash
docker run -it --rm pixelgen /bin/bash
```

{{% /tab %}}
{{< /tabs >}}

## Package Management

Use the `yay` package manager to install and update software:

```bash
yay -Syu <package_name>
```

**Example:**

```bash
yay -Syu vim
```

This will install or update the `vim` text editor.
* Replace `<package_name>` with the actual name of the package you want to install or update.
* The `-Syu` flag performs a full system update, including package updates and dependencies.

## Support and Assistance

If you encounter any issues or require further assistance, please feel free to reach out through the following channels:

* **Midori AI Discord:** https://discord.gg/xdgCx3VyHU
* **Midori AI Email:** [Email Us](mailto:contact-us@midori-ai.xyz)
