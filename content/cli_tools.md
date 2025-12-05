+++
disableToc = false
title = "Midori AI CLI"
weight = 8
+++

![command_line_tools_banner_photo](https://tea-cup.midori-ai.xyz/download/command_line_tools_banner_photo.png)

{{% notice warning %}}
**SUNSET NOTICE**: The Midori AI CLI tools are being sunset and will be removed on January 1st, 2026 in favor of our new Python packages. Please plan to migrate to our new Python-based tools.
{{% /notice %}}

Our tools include our `downloader`, `uploader`, `file-manager`, `hf-downloader`, `login program`, and `updater`

To try them out, pick your system from the tabs and try the command! (Warning the updater needs root to work)

{{< tabs >}}
{{% tab title="PixelArch OS" %}}

[PixelArch OS]({{%relref "pixelos" %}}) already has our tools baked in, but if you are running a nonstandard copy of the os or one of the tools is not installed right, please feel free to run this command.

```bash
curl -k --disable --disable-eprt -s https://tea-cup.midori-ai.xyz/download/pixelarch-midori-ai-updater > updater && sudo chmod +x updater && sudo mv updater /usr/local/bin/midori_ai_updater && sudo midori_ai_updater
```
{{% /tab %}}
{{% tab title="Arch Based OS" %}}
```bash
curl -k --disable --disable-eprt -s https://tea-cup.midori-ai.xyz/download/pixelarch-midori-ai-updater > updater && sudo chmod +x updater && sudo mv updater /usr/local/bin/midori_ai_updater && sudo midori_ai_updater
```
{{% /tab %}}
{{% tab title="Ubuntu Based OS" %}}
```bash
curl -k --disable --disable-eprt -s https://tea-cup.midori-ai.xyz/download/standard-linux-midori-ai-updater > updater && sudo chmod +x updater && sudo mv updater /usr/local/bin/midori_ai_updater && sudo midori_ai_updater
```
{{% /tab %}}
{{< /tabs >}}


## Support and Assistance

If you encounter any issues or require further assistance, please feel free to reach out through the following channels:

* **Midori AI Discord:** https://discord.gg/xdgCx3VyHU
* **Midori AI Email:** [Email Us](mailto:contact-us@midori-ai.xyz)