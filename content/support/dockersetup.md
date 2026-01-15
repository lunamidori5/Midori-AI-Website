+++
disableToc = false
title = "Docker Setup"
weight = 1
+++

![docker-setup-banner](https://tea-cup.midori-ai.xyz/download/logo_color1.png)

## Docker Setup

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

On `RPM` based distributions, such as `CentOS`, `Fedora` or `RHEL`, you need to start it manually using the appropriate `systemctl` or `service` command. As the message indicates, non-root users can't run Docker commands by default, but we will set it up so non root users can use it..

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
Use your package manager, `yay`, `paru`, `pacman`, what ever you have installed.
We are going to be showing with `yay`, but its the same for all of them.

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
{{% tab title="macOS (Rosetta)" %}}

```bash
# TODO: install Docker Desktop
# TODO: (Apple Silicon) install Rosetta if you need x86_64 tooling:
# softwareupdate --install-rosetta --agree-to-license
# TODO: verify with: docker run --rm hello-world
```

{{% /tab %}}
{{< /tabs >}}

