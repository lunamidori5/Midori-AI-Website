+++
disableToc = false
title = "Midori AI Subsystem Manager V2"
weight = 1
+++

![Midori AI photo](https://tea-cup.midori-ai.xyz/download/logosubsystem.png)

The ``Midori AI Subsystem`` offers an innovative solution for managing AI workloads through its advanced integration with containerization technologies. Leveraging the lightweight and efficient design of [PixelArch OS](https://io.midori-ai.xyz/pixelos/), this system empowers developers, researchers, and hobbyists test AI systems effortlessly across a variety of environments.

At the heart of the Midori AI Subsystem is [PixelArch OS](https://io.midori-ai.xyz/pixelos/), a custom Arch Linux-based operating system optimized for containerized workloads. It provides a lightweight, streamlined environment tailored for modern AI development. 

* Simplified Deployment: Deploy AI systems effortlessly with pre-configured or built-on-request container images tailored to your needs.
* Platform Versatility: Supports Docker, Podman, LXC, and other systems, allowing you to choose the best fit for your infrastructure.
* Seamless Experimentation: Experiment with various AI tools and models in isolated environments without worrying about conflicts or resource constraints.
* Effortless Scalability: Scale AI workloads efficiently by leveraging containerization technologies.
* Standardized Configurations: Reduce guesswork with standardized setups for AI programs.
* Unleash Creativity: Focus on innovating and developing AI solutions while the Subsystem handles system configuration and compatibility.


{{% notice  style="warning" title="Notice" %}}
**SUNSET NOTICE**: The Midori AI CLI tools are being sunset and will be removed on January 1st, 2026 in favor of our new Python packages. Please plan to migrate to our new Python-based tools.
{{% /notice %}}

## Install Midori AI Subsystem Manager

{{< tabs >}}

{{% tab title="V2 (UV)" %}}
### Prerequisites
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [UV](https://docs.astral.sh/uv/getting-started/installation/)
- [git](https://git-scm.com/downloads)

### Quick install with script

Copy and paste this into a SH or Batch file then run it.

```bash
git clone https://github.com/lunamidori5/subsystem-manager.git
cd subsystem-manager
uv run main.py
```

### Running the program

Open a terminal and run:

```bash
uv run main.py
```

### Running the program as root

Open a terminal and run:

```bash
sudo uv run main.py
```

The application will attempt to automatically launch the web UI. If the automatic launch is unsuccessful, a link to the web UI will be provided in the application output. Please use this link to manually open the web UI. Automatic updates are implemented through continuous integration with GitHub. While manual rebuilds are generally unnecessary, the application will rebuild as needed to maintain stability and incorporate the latest changes.

{{% /tab %}}

{{% tab title="V2 (Docker)" %}}
### Prerequisites
- [Docker Engine](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Running the program

Open a terminal and run:

```bash
docker run -p 39090:8000 --privileged --name subsystem_manager --restart always -d -v /var/run/docker.sock:/var/run/docker.sock lunamidori5/pixelarch:subsystem
```

### Running the program (With GPU)

Open a terminal and run:

```bash
docker run --gpus all -p 39090:8000 --privileged --name subsystem_manager --restart always -d -v /var/run/docker.sock:/var/run/docker.sock lunamidori5/pixelarch:subsystem
```

Access the user interface by navigating to your IP address on port 39090. Please allow 2-10 minutes for the initial build process to complete. The system automatically updates upon each GitHub push. While a manual rebuild is typically unnecessary, the application will rebuild as required.

{{% /tab %}}

{{% tab title="V1 (SUNSETTING)" %}}
Do not use, will no longer work...
[Click here to go to the old install page](subsystemv1/)
{{% /tab %}}

{{< /tabs >}}

[![Auto Lint, Test, and Build.](https://github.com/lunamidori5/Midori-AI/actions/workflows/Auto_Test_Build.yaml/badge.svg)](https://github.com/lunamidori5/Midori-AI/actions/workflows/Auto_Test_Build.yaml)

{{% notice style="info" title="Notice" %}}
Reminder to always use your computers IP address not ``localhost`` when using the Midori AI Subsystem!
{{% /notice %}}

## Support and Assistance

If you encounter any issues or require further assistance, please feel free to reach out through the following channels:

* **Midori AI Github:** [Github Issue](https://github.com/lunamidori5/Midori-AI/issues/new/choose)
* **Midori AI Email:** [Email Us](mailto:contact-us@midori-ai.xyz)
* **Midori AI Discord:** [Join our Discord server](https://discord.gg/xdgCx3VyHU)


## ----- Disclaimer -----

The functionality of this product is subject to a variety of factors that are beyond our control, and we cannot guarantee that it will work flawlessly in all situations. We have taken every possible measure to ensure that the product functions as intended, but there may be instances where it does not perform as expected. Please be aware that we cannot be held responsible for any issues that arise due to the product's functionality not meeting your expectations. By using this product, you acknowledge and accept the inherent risks associated with its use, and you agree to hold us harmless for any damages or losses that may result from its functionality not being guaranteed.

## ----- Footnotes -----

*For your safety we have posted the code of this program onto github, please check it out! - [Github](https://github.com/lunamidori5/Midori-AI-Subsystem-Manager/tree/master/subsystem-manager-2-uv)

**If you would like to give to help us get better servers - [Give Support](https://paypal.me/midoricookieclub?country.x=US&locale.x=en_US)

***If you or someone you know would like a new backend supported by Midori AI Subsystem please reach out to us at [contact-us@midori-ai.xyz](mailto:contact-us@midori-ai.xyz)
