+++
disableToc = false
title = "PixelArch OS"
weight = 1
+++

![pixelarch-logo](https://tea-cup.midori-ai.xyz/download/pixalarch-banner.png)

## PixelArch OS: A Docker-Optimized Arch Linux Distribution

PixelArch OS is a lightweight and efficient Arch Linux distribution designed for containerized environments. It provides a streamlined platform for developing, deploying, and managing Docker-based workflows.

**Key Features:**

- **Arch-Based:** Built on the foundation of Arch Linux, known for its flexibility and extensive package selection.
- **Docker-Optimized:** Tailored for efficient Docker usage, allowing for seamless integration with your containerized workflows.
- **Frequent Updates:** Regularly receives security and performance updates, ensuring a secure and up-to-date environment.
- **Package Management:** Utilizes the powerful yay package manager alongside the traditional pacman, providing a flexible and efficient way to manage software packages.
- **Minimal Footprint:** Designed to be lightweight and resource-efficient, ideal for running in Docker containers.

## PixelArch Flavors: A Tiered Approach

PixelArch is offered in nine layers, with each flavor building on the previous one. The package lists below show what each tier adds.

{{< tabs >}}
{{% tab title="Quartz" %}}
Level 1: Quartz

The foundation: a minimal base system providing a clean slate for your specific needs.

{{% /tab %}}

{{% tab title="Obsidian" %}}
Level 2: Obsidian

Adds the core utility layer:

- `curl`
- `wget`
- `tar`
- `xz`
- `zip`
- `unzip`
- `tree`
- `nano`
- `lolcat`
{{% /tab %}}

{{% tab title="Lapis" %}}
Level 3: Lapis

Adds the shell and terminal workflow layer:

- `zsh`
- `fish`
- `tmux`
- `bash-completion`
- `zsh-completions`
- `starship`
{{% /tab %}}

{{% tab title="Amethyst" %}}
Level 4: Amethyst

Adds the editor, search, and container workflow layer:

- `neovim`
- `ripgrep`
- `jq`
- `fastfetch`
- `docker`
- `docker-compose`
{{% /tab %}}

{{% tab title="Citrine" %}}
Level 5: Citrine

Adds the Python and build tooling layer:

- `python`
- `python-pip`
- `python-pyfiglet`
- `python-virtualenv`
- `uv`
- `gcc`
{{% /tab %}}

{{% tab title="Topaz" %}}
Level 6: Topaz

Adds the Node.js layer:

- `nodejs`
- `npm`
- `nvm`
- `bun`
{{% /tab %}}

{{% tab title="Sapphire" %}}
Level 7: Sapphire

Adds the Rust and compatibility layer:

- `rust`
- `wine`
- `xorg-server-xvfb`
{{% /tab %}}

{{% tab title="Ruby" %}}
Level 8: Ruby

Adds the remote access, privacy, and text browsing layer:

- `openssh`
- `tmate`
- `tor`
- `torsocks`
- `torbrowser-launcher`
- `lynx`
{{% /tab %}}

{{% tab title="Emerald" %}}
Level 9: Emerald

Adds the LLM agents and developer CLI layer:

- `gemini-cli`
- `claude-code`
- `openai-codex`
- `github-copilot-cli`
- `github-cli`
{{% /tab %}}
{{< /tabs >}}

## Getting Started

{{< tabs >}}
{{% tab title="Distrobox" %}}

{{< tabs >}}
{{% tab title="Quartz" %}}
- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:quartz -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)


{{% /tab %}}
{{% tab title="Obsidian" %}}
- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:obsidian -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{% tab title="Lapis" %}}
- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:lapis -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{% tab title="Amethyst" %}}
- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:amethyst -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{% tab title="Citrine" %}}
- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:citrine -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{% tab title="Topaz" %}}
- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:topaz -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{% tab title="Sapphire" %}}
- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:sapphire -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{% tab title="Ruby" %}}
- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:ruby -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{% tab title="Emerald" %}}
- Step 1. Setup the OS (`distrobox create -i lunamidori5/pixelarch:emerald -n PixelArch --root`)
- Step 2. Enter the OS (`distrobox enter PixelArch --root`)

{{% /tab %}}
{{< /tabs >}}


{{% /tab %}}
{{% tab title="Docker Compose" %}}
### 1. Create a `docker-compose.yaml`

Pick a flavor and create a `docker-compose.yaml` with the matching image tag:

{{< tabs >}}
{{% tab title="Quartz" %}}

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
{{% tab title="Obsidian" %}}

```yaml
services:
  pixelarch-os:
    image: lunamidori5/pixelarch:obsidian
    tty: true
    restart: always
    privileged: false
    command: ["sleep", "infinity"]
```

{{% /tab %}}
{{% tab title="Lapis" %}}

```yaml
services:
  pixelarch-os:
    image: lunamidori5/pixelarch:lapis
    tty: true
    restart: always
    privileged: false
    command: ["sleep", "infinity"]
```

{{% /tab %}}
{{% tab title="Amethyst" %}}

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
{{% tab title="Citrine" %}}

```yaml
services:
  pixelarch-os:
    image: lunamidori5/pixelarch:citrine
    tty: true
    restart: always
    privileged: true
    command: ["sleep", "infinity"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

{{% /tab %}}
{{% tab title="Topaz" %}}

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
{{% tab title="Sapphire" %}}

```yaml
services:
  pixelarch-os:
    image: lunamidori5/pixelarch:sapphire
    tty: true
    restart: always
    privileged: true
    command: ["sleep", "infinity"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

{{% /tab %}}
{{% tab title="Ruby" %}}

```yaml
services:
  pixelarch-os:
    image: lunamidori5/pixelarch:ruby
    tty: true
    restart: always
    privileged: true
    command: ["sleep", "infinity"]
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
```

{{% /tab %}}
{{% tab title="Emerald" %}}

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

### 2. Start the container in detached mode

```bash
docker compose up -d
```

### 3. Access the container shell

```bash
docker compose exec pixelarch-os /bin/bash
```

{{% /tab %}}
{{% tab title="WSL2 (Not Recommended)" %}}

Midori AI recommends switching to Linux instead of Windows. If you still want to use PixelArch in WSL2, follow the steps below. No Windows-specific support is provided.

### 1. Setup the docker image

```bash
docker run -t --name wsl_export lunamidori5/pixelarch:quartz ls /
```

### 2. Export the PixelArch filesystem from docker

```bash
docker export wsl_export > /mnt/c/temp/pixelarch.tar
```

### 3. Clean up the docker image

```bash
docker rm wsl_export
```

### 4. Import PixelArch into WSL

```batch
cd C:\\temp
mkdir E:\\wslDistroStorage\\pixelarch
wsl --import Pixelarch E:\\wslDistroStorage\\pixelarch .\\pixelarch.tar
```

{{% /tab %}}
{{% tab title="Docker Run (Not Recommended)" %}}

### 1. Use PixelArch shell

{{< tabs >}}
{{% tab title="Quartz" %}}

```bash
docker run -it --rm lunamidori5/pixelarch:quartz /bin/bash
```


{{% /tab %}}
{{% tab title="Obsidian" %}}

```bash
docker run -it --rm lunamidori5/pixelarch:obsidian /bin/bash
```

{{% /tab %}}
{{% tab title="Lapis" %}}

```bash
docker run -it --rm lunamidori5/pixelarch:lapis /bin/bash
```

{{% /tab %}}
{{% tab title="Amethyst" %}}

```bash
docker run -it --rm lunamidori5/pixelarch:amethyst /bin/bash
```

{{% /tab %}}
{{% tab title="Citrine" %}}

```bash
docker run -it --rm lunamidori5/pixelarch:citrine /bin/bash
```

{{% /tab %}}
{{% tab title="Topaz" %}}

```bash
docker run -it --rm lunamidori5/pixelarch:topaz /bin/bash
```

{{% /tab %}}
{{% tab title="Sapphire" %}}

```bash
docker run -it --rm lunamidori5/pixelarch:sapphire /bin/bash
```

{{% /tab %}}
{{% tab title="Ruby" %}}

```bash
docker run -it --rm lunamidori5/pixelarch:ruby /bin/bash
```

{{% /tab %}}
{{% tab title="Emerald" %}}

```bash
docker run -it --rm lunamidori5/pixelarch:emerald /bin/bash
```

{{% /tab %}}
{{< /tabs >}}
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
