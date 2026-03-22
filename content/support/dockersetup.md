+++
disableToc = false
title = "Docker Setup"
weight = 1
+++

![docker-setup-banner](https://tea-cup.midori-ai.xyz/download/logo_color1.png)

## Setup

{{< tabs >}}
{{% tab title="Ubuntu/Debian" %}}

[Docker Setup](https://docs.docker.com/engine/install/ubuntu)

```bash
# Install Docker!
# Remove `--dry-run` if your ready to install.
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh --dry-run

# Setup the docker user
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

# Test it out (standard)!
docker run --rm hello-world

# Test it out (Pixelarch!)
docker run --rm lunamidori5/pixelarch:emerald /bin/bash -lc 'echo hello world'
```

{{% /tab %}}
{{% tab title="Fedora/RHEL" %}}

[Docker Setup](https://docs.docker.com/engine/install/fedora)

On `RPM`-based distributions such as `CentOS`, `Fedora`, or `RHEL`, start Docker manually with the appropriate `systemctl` or `service` command. Non-root users cannot run Docker commands by default. We will set that up next.

```bash
# Setup
sudo dnf install dnf-plugins-core

# on Fedora 40
sudo dnf config-manager --add-repo https://download.docker.com/linux/fedora/docker-ce.repo

# on Fedora 41 and newer
sudo dnf config-manager addrepo --from-repofile="https://download.docker.com/linux/fedora/docker-ce.repo"

# Install the docker packages
sudo dnf install docker-ce docker-ce-cli containerd.io

# Setup the docker user
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

# Start the docker socket
sudo systemctl enable docker
sudo systemctl start docker

# Test it out (standard)!
docker run --rm hello-world

# Test it out (Pixelarch!)
docker run --rm lunamidori5/pixelarch:emerald /bin/bash -lc 'echo hello world'
```

{{% /tab %}}
{{% tab title="Arch Flavors" %}}
Use your package manager—`yay`, `paru`, `pacman`, or whatever you have installed.
We use `yay` in the example, but the steps are the same for all of them.

```bash
# Install Docker!
yay -Syu --noconfirm docker docker-compose && yay -Yccc --noconfirm

# Setup the docker user
sudo groupadd docker
sudo usermod -aG docker $USER
newgrp docker

# Go read the docker setup page on using systemd or init or whatever
echo "Stop by https://wiki.archlinux.org/title/Docker"

# Test it out (standard)!
docker run --rm hello-world

# Test it out (Pixelarch!)
docker run --rm lunamidori5/pixelarch:emerald /bin/bash -lc 'echo hello world'
```

{{% /tab %}}
{{% tab title="openSUSE" %}}

```bash
# TODO: install docker
# TODO: start/enable the docker service
# TODO: verify with: docker run --rm hello-world
```

{{% /tab %}}
{{< /tabs >}}
