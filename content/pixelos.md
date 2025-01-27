+++
disableToc = false
title = "PixelArch OS"
weight = 8
+++

![pixelarch-logo](https://tea-cup.midori-ai.xyz/download/pixalarch-banner.png)

## PixelArch OS: A Docker-Optimized Arch Linux Distribution

PixelArch OS is a lightweight and efficient Arch Linux distribution specifically designed for Docker environments. It offers a streamlined platform for developing, deploying, and managing containerized applications.

**Key Features:**

- **Arch-Based:** Built on the foundation of Arch Linux, known for its flexibility and extensive package selection.
- **Docker-Optimized:** Tailored for efficient Docker usage, allowing for seamless integration with your containerized workflows.
- **Frequent Updates:** Regularly receives security and performance updates, ensuring a secure and up-to-date environment.
- **Package Management:** Utilizes the powerful yay package manager alongside the traditional pacman, providing a flexible and efficient way to manage software packages.
- **Minimal Footprint:** Designed to be lightweight and resource-efficient, ideal for running in Docker containers.

## Getting Started

{{< tabs >}}
{{% tab title="Distrobox" %}}
Each level builds upon the last, adding more features and configurations:

- **Level 1: Quartz** - The base installation, like a blank canvas.
- **Level 2: Amethyst** - Essential tools (like `curl`, `wget`, `docker`, and more) and a few quality-of-life improvements.
- **Level 3: Topaz** -  Specialized software for development. Comes with `python`, `nodejs`, and `rust` preinstalled.
- **Level 4: Emerald** - Remote shell and tunnel support (via `tmate`, `rdp` or `ssh`), and a full [Enlightenment](https://wiki.archlinux.org/title/Enlightenment) Desktop preinstalled.

{{< tabs >}}
{{% tab title="Quartz" %}}
Image Size - ``530mb``

- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:quartz -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)


{{% /tab %}}
{{% tab title="Amethyst" %}}
Image Size - ``870mb``

- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:amethyst -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{% tab title="Topaz" %}}
Image Size - ``1.15gb``

- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:topaz -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{% tab title="Emerald" %}}
Image Size - ``3.5gb``

- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:emerald -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{< /tabs >}}


{{% /tab %}}
{{% tab title="Docker Compose" %}}
### 1. Clone the Repository

```bash
git clone https://github.com/lunamidori5/Midori-AI-Cluster-OS.git
```

### 2. Navigate to the `pixelarch_os` Directory

```bash
cd Midori-AI-Cluster-OS/pixelarch_os
```

### 3. Run the Image and Access the Shell

**a. Edit the `docker-compose.yaml` file:**

Each level builds upon the last, adding more features and configurations:

- **Level 1: Quartz** - The base installation, like a blank canvas.
- **Level 2: Amethyst** - Essential tools (like `curl`, `wget`, `docker`, and more) and a few quality-of-life improvements.
- **Level 3: Topaz** -  Specialized software for development. Comes with `python`, `nodejs`, and `rust` preinstalled.
- **Level 4: Emerald** - Remote shell and tunnel support (via `tmate`, `rdp` or `ssh`), and a full [Enlightenment](https://wiki.archlinux.org/title/Enlightenment) Desktop preinstalled. (Better for Distrobox, docker it will not work)

{{< tabs >}}
{{% tab title="Quartz" %}}
Image Size - ``530mb``

```yaml
services:
  pixelarch-os:
    image: lunamidori5/pixelarch:quartz
    tty: true
    restart: always
    privileged: false
    command: ["sleep", "infinity"]
```

{{% /tab %}}
{{% tab title="Amethyst" %}}
Image Size - ``870mb``

```yaml
services:
  pixelarch-os:
    image: lunamidori5/pixelarch:amethyst
    tty: true
    restart: always
    privileged: true
    command: ["sleep", "infinity"]
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock
```

{{% /tab %}}
{{% tab title="Topaz" %}}
Image Size - ``1.15gb``

```yaml
services:
  pixelarch-os:
    image: lunamidori5/pixelarch:topaz
    tty: true
    restart: always
    privileged: true
    command: ["sleep", "infinity"]
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock
```

{{% /tab %}}
{{% tab title="Emerald" %}}
Image Size - ``3.5gb``

```yaml
services:
  pixelarch-os:
    image: lunamidori5/pixelarch:emerald
    tty: true
    restart: always
    privileged: true
    command: ["sleep", "infinity"]
    volumes:
    - /var/run/docker.sock:/var/run/docker.sock
```

{{% /tab %}}
{{< /tabs >}}

**b. Start the container in detached mode:**

```bash
docker compose up -d
```

**c. Access the container shell:**

```bash
docker exec -it pixelarch_os-pixelarch-os-1 /bin/bash
```
*Note: The container name might differ from pixelarch-os, check your Docker Compose output or `docker ps -a` for the actual name.*

{{% /tab %}}
{{% tab title="WSL2 (Not Recommened)" %}}

Midori AI recommends switching to Linux off of windows, if you still wish to use Pixelarch in WSL2 here is how, No support will be give to fix bugs on windows.

### 1. Setup the docker image

```bash
docker run -t --name wsl_export lunamidori5/pixelarch:quartz ls /
```

### 2. Export the `pixelarch` os from docker

```bash
docker export wsl_export > /mnt/c/temp/pixelarch.tar
```

### 3. Clean up the docker iamge

```bash
docker rm wsl_export
```

### 4. Import Pixelarch into WSL

```batch
cd C:\temp
mkdir E:\wslDistroStorage\pixelarch
wsl --import Pixelarch E:\wslDistroStorage\pixelarch .\pixelarch.tar
```

{{% /tab %}}
{{% tab title="Docker Run (Not Recommened)" %}}

### 1. Clone the Repository

```bash
git clone https://github.com/lunamidori5/Midori-AI-Cluster-OS.git
```

### 2. Navigate to the `pixelarch_os` Directory

```bash
cd Midori-AI-Cluster-OS/pixelarch_os
```

### 3. Build the Image and Access the Shell

Build the Docker Image
```bash
docker build -t pixelarch -f arch_dockerfile .
```
Run the docker bash shell
```bash
docker run -it pixelarch /bin/bash
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

**Note:**

* Replace `<package_name>` with the actual name of the package you want to install or update.
* The `-Syu` flag performs a full system update, including package updates and dependencies.


## Support and Assistance

If you encounter any issues or require further assistance, please feel free to reach out through the following channels:

* **Midori AI Discord:** https://discord.gg/xdgCx3VyHU
* **Midori AI Email:** [Email Us](mailto:contact-us@midori-ai.xyz)