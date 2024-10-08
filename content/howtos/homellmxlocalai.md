+++
disableToc = false
title = "HA-OS (HomeLLM) x LocalAI"
weight = 10
+++

_____

Home Assistant is an open-source home automation platform that allows users to control and monitor various smart devices in their homes. It supports a wide range of devices, including lights, thermostats, security systems, and more. The platform is designed  to be user-friendly and customizable, enabling users to create automations and routines to make their homes more convenient and efficient. Home Assistant can be accessed through a web interface or a mobile app, and it can be installed on a variety of hardware platforms, such as Raspberry Pi or a dedicated server.

Currently, Home Assistant supports conversation-based agents and services. As of writing this, OpenAIs API is supported as a conversation agent; however, access to your homes devices and entities is possible through custom components. Local based services, such as LocalAI, are also available as a drop-in replacement for OpenAI services.

_____

In this guide I will detail the steps I've taken to get [Home-LLM](https://github.com/acon96/home-llm) and [Local-AI](https://github.com/mudler/LocalAI/) working together in conjunction with [Home-Assistant](https://www.home-assistant.io/)!

This guide assumes that you already have [Local-AI](https://github.com/mudler/LocalAI/) running (in or out of the subsystem). 
If that is not done, you can [Follow this How To]({{%relref "howtos/by_hand/easy-setup-docker" %}}) or [Install Using Midori AI Subsystem](https://io.midori-ai.xyz/subsystem/manager/)!

_____

- 1: You will first need to [follow this guide to install Home-LLM](https://github.com/acon96/home-llm/blob/develop/docs/Setup.md)into your [Home-Assistant](https://www.home-assistant.io/) installation.


     If you simply want to install the [Home-LLM](https://github.com/acon96/home-llm) component through HACS,  you  can press on this button:

     [Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/redirect/hacs_repository/?category=Integration&repository=home-llm&owner=acon96) 

- 2: Add `Home LLM Conversation` integration to HA. 
    - 1: Access the `Settings` page.
    - 2: Click on `Devices & services`.
    - 3: Click on `+ ADD INTEGRATION` on the lower-right part of the screen.
    - 4: Type and then select `Local LLM Conversation`.
    - 5: Select the `Generic OpenAI Compatible API`.
    - 6: Enter the hostname or IP Address of your LocalAI host.
    - 7: Enter the used port (Default is `8080` / `38080`).
    - 8: Enter `mistral-7b-instruct-v0.3` as the `Model Name*`
      - Leave `API Key` empty
      - Do not check `Use HTTPS`
      - leave `API Path*` as `/v1` 
    - 9: Press `Next`
    - 10: Select `Assist` under `Selected LLM API`
    - 11: Make sure the `Prompt Format*` is set to `Mistral`
    - 12: Make sure `Enable in context learning (ICL) examples` is checked.
    - 13: Press `Sumbit`
    - 14: Press `Finish`

![photo](https://github.com/maxi1134/Home-Assistant-Config/blob/master/assets/home_llm_guide/home_llm_installation_video.gif?raw=true)


- 3:  Configure the Voice assistant.
  - 1: Access the `Settings` page.
  - 2: Click on `Voice assistants`.
  - 3: Click on `+ ADD ASSISTANT`.
  - 4: Name the Assistant `HomeLLM`.
  - 5: Select `English` as the Language.
  - 6: Set the `Conversation agent` to the newly created `LLM Model 'mistral-7b-instruct-v0.3' (remote)`.
  - 7: Set your `Speech-to-text` `Wake word`, and `Text-to-speech` to the ones you use. Leave to `None` if you don't have any. 
  - 8: Click `Create`
  
- 4: Select the newly created voice assistant as the default one.
    - While remaining on the `Voice assistants` page click on the newly create assistant, and press the start at the top-right corner.


There you go! Your Assistant should now be working with Local-AI through Home-LLM!
 - Make sure that the entities you want to control are exposted to Assist within Home-Assistant!

{{% notice style="warning" title="Notice" %}}
**Important Note:** 

Any devices you choose to expose to the model will be added to the context and may have their state changed by the model. Only expose devices that you are comfortable with the model modifying, even if the modification is not what you intended. The model may occasionally hallucinate and issue commands to the wrong device. Use at your own risk. 

{{% /notice %}}
