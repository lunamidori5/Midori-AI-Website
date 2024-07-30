+++
disableToc = false
title = "PixelArch OS"
weight = 8
+++

## PixelArch OS: A Docker-Optimized Arch Linux Distribution

PixelArch OS is a lightweight and efficient Arch Linux distribution specifically designed for Docker environments. It offers a streamlined platform for developing, deploying, and managing containerized applications.

**Key Features:**

- **Arch-Based:** Built on the foundation of Arch Linux, known for its flexibility and extensive package selection.
- **Docker-Optimized:** Tailored for efficient Docker usage, allowing for seamless integration with your containerized workflows.
- **Frequent Updates:** Regularly receives security and performance updates, ensuring a secure and up-to-date environment.
- **Package Management:** Utilizes the powerful yay package manager alongside the traditional pacman, providing a flexible and efficient way to manage software packages.
- **Minimal Footprint:** Designed to be lightweight and resource-efficient, ideal for running in Docker containers.

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/lunamidori5/Midori-AI-Cluster-OS.git
```

### 2. Navigate to the `aiclusteros` Directory

```bash
cd Midori-AI-Cluster-OS/aiclusteros
```

### 3. Build the Docker Image

```bash
docker build -t pixelarch -f arch_dockerfile .
```

### 4. Run the Image and Access the Shell

**Using `docker-compose`:**

**a. Edit the `docker-compose.yaml` file:**

```yaml
services:
  pixelarch-os:
    build:
      context: .
      dockerfile: ./arch_dockerfile
    tty: true
    restart: always
    command: ["sleep", "infinity"]
```

**b. Start the container in detached mode:**

```bash
docker compose up -d
```

**c. Access the container shell:**

```bash
docker exec -it aiclusteros-pixelarch-os-1 /bin/bash
```
*Note: The container name might differ from pixelarch-os, check your Docker Compose output or `docker ps -a` for the actual name.*

**Using `docker run`:** (Not Recommened)

```bash
docker run -it pixelarch /bin/bash
```

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

**Note:**

* Replace `<package_name>` with the actual name of the package you want to install or update.
* The `-Syu` flag performs a full system update, including package updates and dependencies.


## Support and Assistance

If you encounter any issues or require further assistance, please feel free to reach out through the following channels:

* **Midori AI Discord:** https://discord.gg/xdgCx3VyHU
* **Midori AI Email:** [Email Us](mailto:contact-us@midori-ai.xyz)