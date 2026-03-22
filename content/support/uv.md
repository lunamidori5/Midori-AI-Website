+++
disableToc = false
title = "UV (Python)"
weight = 2
+++

![uv-banner](https://tea-cup.midori-ai.xyz/download/logo_color1.png)

## UV (Python)

{{< tabs >}}
{{% tab title="Ubuntu/Debian" %}}

[uv Installation](https://docs.astral.sh/uv/getting-started/installation/)

```bash
# Install uv!
curl -LsSf https://astral.sh/uv/install.sh | sh

# Load uv in this shell session.
. "$HOME/.local/bin/env"

# Test it out!
uv --version
```

{{% /tab %}}
{{% tab title="Fedora/RHEL" %}}

### Fedora

```bash
# Install uv.
sudo dnf install -y uv

# Test it out!
uv --version
```

### RHEL

```bash
# Install uv with the official installer.
command -v curl >/dev/null || sudo dnf install -y curl-minimal
sudo dnf install -y ca-certificates
curl -LsSf https://astral.sh/uv/install.sh | sh

# Load uv in this shell session.
export PATH="$HOME/.local/bin:$PATH"

# Test it out!
uv --version
```

{{% /tab %}}
{{% tab title="Arch/Manjaro" %}}
Use your package manager, `yay`, `paru`, `pacman`, what ever you have installed.
We are going to be showing with `yay`, but its the same for all of them.

```bash
# Install uv!
yay -Syu --noconfirm uv && yay -Yccc --noconfirm

# Test it out!
uv --version
```

{{% /tab %}}
{{% tab title="openSUSE" %}}

### openSUSE Tumbleweed

```bash
# Install uv.
sudo zypper install -y uv

# Test it out!
uv --version
```

### openSUSE Leap

```bash
# Install prerequisites for the official installer.
sudo zypper install -y curl ca-certificates tar gzip

# Install uv.
curl -LsSf https://astral.sh/uv/install.sh | sh

# Load uv in this shell session.
export PATH="$HOME/.local/bin:$PATH"

# Test it out!
uv --version
```

{{% /tab %}}
{{< /tabs >}}

## Common Commands

```bash
# Create/sync a project environment.
uv venv
uv sync

# Run a project command.
uv run <command>

# Add a dependency.
uv add <package>
```

## Real Repo Example

```bash
# Clone a real uv project.
git clone https://github.com/Midori-AI-OSS/Agents-Runner
cd Agents-Runner

# Install dependencies from the project.
uv sync

# Run a quick command in the project environment.
uv run python -V

# Project quick start (requires Docker + ffmpeg).
uv run main.py
```
