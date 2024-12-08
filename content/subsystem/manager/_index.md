+++
disableToc = false
title = "Midori AI Subsystem Manager V2"
weight = 1
+++

![Midori AI photo](https://tea-cup.midori-ai.xyz/download/logosubsystem.png)

**How Docker Works**

Docker is a containerization platform that allows you to package and run applications in isolated and portable environments called containers. Containers share the host operating system kernel but have their own dedicated file system, processes, and resources. This isolation allows applications to run independently of the host environment and each other, ensuring consistent and predictable behavior.

[**Midori AI Subsystem** - Github Link](https://github.com/lunamidori5/Midori-AI-Subsystem-Manager)

The Midori AI Subsystem extends Docker's capabilities by providing a modular and extensible platform for managing AI workloads. Each AI system is encapsulated within  its own dedicated Docker image, which contains the necessary software and dependencies. This approach provides several benefits:

* **Simplified Deployment:** The Midori AI Subsystem provides a streamlined and efficient way to deploy AI systems using Docker container technology.
* **Eliminates Guesswork:** Standardized configurations and settings reduce complexities, enabling seamless setup and management of AI programs.

{{% notice style="warning" title="Notice" %}}
**Warnings / Heads up**
- This program is in beta! By using it you take on risk, please see the disclaimer in the footnotes

**Known Issues**
- Server Rework is underway! Thank you for giving us lots of room to grow!
- **Report Issuses** -> [Github Issue](https://github.com/lunamidori5/Midori-AI/issues/new/choose)
{{% /notice %}}

## Install Midori AI Subsystem Manager

{{< tabs >}}

{{% tab title="V2 (UV)" %}}
### Prerequisites
- [Docker Engine](https://docs.docker.com/engine/install/) and [Docker Compose](https://docs.docker.com/compose/install/)
- [UV](https://docs.astral.sh/uv/getting-started/installation/)
- [git](https://git-scm.com/downloads)

### Quick install with script

Copy and paste this into a SH or Batch file then run it.

```bash
git clone https://github.com/lunamidori5/Midori-AI-Subsystem-Manager.git
cd Midori-AI-Subsystem-Manager/
cd subsystem-manager-2-uv/
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
{{% /tab %}}

{{% tab title="V2 (Docker)" %}}
Coming soon! Please use UV for now.
{{% /tab %}}

{{% tab title="V1 (SUNSETTING)" %}}
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

*For your safety we have posted the code of this program onto github, please check it out! - [Github](https://github.com/lunamidori5/Midori-AI/tree/master/other_files)

**If you would like to give to help us get better servers - [Give Support](https://paypal.me/midoricookieclub?country.x=US&locale.x=en_US)

***If you or someone you know would like a new backend supported by Midori AI Subsystem please reach out to us at [contact-us@midori-ai.xyz](mailto:contact-us@midori-ai.xyz)
