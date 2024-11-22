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
To execute the source build, manually input each command or consolidate them into a batch/bash file. Support for `Windows-based` source builds is currently unavailable. The `midori_ai_updater` is not supported to be build from source as it will try to download the pre built programs.

```bash
# Download all of the files
curl -k --disable --disable-eprt -s https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/Webserver/Programs/Downloader/helper_app.py > helper_app.py
curl -k --disable --disable-eprt -s https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/Webserver/Programs/Login_program/midori_ai_login_app.py > midori_ai_login_app.py
curl -k --disable --disable-eprt -s https://raw.githubusercontent.com/lunamidori5/Midori-AI-Subsystem-Manager/master/subsystem-manager-uv/yaml_edit.py > yaml_edit.py
curl -k --disable --disable-eprt -s https://raw.githubusercontent.com/lunamidori5/Midori-AI-Subsystem-Manager/master/midori_ai_manager/huggingface_downloader.py > huggingface_downloader.py
curl -k --disable --disable-eprt -s https://raw.githubusercontent.com/lunamidori5/Midori-AI-Subsystem-Manager/master/Subsystem-Manager/subsystem-manager-uv/requirements.txt > requirements.txt
curl -k --disable --disable-eprt -s https://raw.githubusercontent.com/lunamidori5/Midori-AI/master/Webserver/Programs/File_manager/file_manager.py > midori_ai_file_manager.py

# Edit these commands to use a venv or uv as needed
pip install pyinstaller pytz
pip install -r requirements.txt

# Edit these commands to use a venv or uv as needed
# The Midori AI uploader is not hosted online, so we need to pull it using our downloader
python3 helper_app.py git_uploader.py

# Edit these commands to use a venv or uv as needed
pyinstaller --onefile --clean helper_app.py
pyinstaller --onefile --clean midori_ai_login_app.py
pyinstaller --onefile --clean yaml_edit.py
pyinstaller --onefile --clean midori_ai_file_manager.py
pyinstaller --onefile --clean huggingface_downloader.py
pyinstaller --onefile --clean git_uploader.py

# Feel free to move these where ever you would like.
```
{{% /tab %}}
{{< /tabs >}}


## Support and Assistance

If you encounter any issues or require further assistance, please feel free to reach out through the following channels:

* **Midori AI Discord:** https://discord.gg/xdgCx3VyHU
* **Midori AI Email:** [Email Us](mailto:contact-us@midori-ai.xyz)