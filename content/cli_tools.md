+++
disableToc = false
title = "Midori AI CLI"
weight = 9
+++

![command_line_tools_banner_photo](https://tea-cup.midori-ai.xyz/download/command_line_tools_banner_photo.png)

Our tools include our `downloader`, `uploader`, `file-manager`, `hf-downloader`, `login program`, and `updater`

To try them out, pick your system from the tabs and try the command! (Warning the updater needs root to work)

{{< tabs >}}
{{% tab title="PixelArch OS" %}}

[PixelArch OS]({{%relref "pixelos" %}}) already has our tools baked in, but if you are running a nonstandard copy of the os or one of the tools is not installed right, please feel free to run this command.

```bash
curl -k --disable --disable-eprt -s https://tea-cup.midori-ai.xyz/download/pixelarch-midori-ai-updater > updater && sudo chmod +x updater && sudo mv updater /usr/local/bin/midori-ai-updater && sudo midori-ai-updater
```
{{% /tab %}}
{{% tab title="Arch Based OS" %}}
```bash
curl -k --disable --disable-eprt -s https://tea-cup.midori-ai.xyz/download/pixelarch-midori-ai-updater > updater && sudo chmod +x updater && sudo mv updater /usr/local/bin/midori-ai-updater && sudo midori-ai-updater
```
{{% /tab %}}
{{% tab title="Ubuntu Based OS" %}}
```bash
curl -k --disable --disable-eprt -s https://tea-cup.midori-ai.xyz/download/standard-linux-midori-ai-updater > updater && sudo chmod +x updater && sudo mv updater /usr/local/bin/midori-ai-updater && sudo midori-ai-updater
```
{{% /tab %}}
{{% tab title="Build from source" %}}
```bash
COMEING SOON
```
{{% /tab %}}
{{< /tabs >}}


## Support and Assistance

If you encounter any issues or require further assistance, please feel free to reach out through the following channels:

* **Midori AI Discord:** https://discord.gg/xdgCx3VyHU
* **Midori AI Email:** [Email Us](mailto:contact-us@midori-ai.xyz)