
+++
disableToc = false
title = "Easy Setup - Docker"
weight = 2
+++

{{% notice note %}}
It is highly recommended to check out the [Midori AI Subsystem Manager]({{%relref "subsystem/manager" %}}) for setting up LocalAI. It does all of this for you!
{{% /notice %}}

{{% notice Note %}}
- You will need about 10gb of RAM Free
- You will need about 150gb of space free on C drive for ``Docker compose``
{{% /notice %}}

We are going to run `localai` with `docker compose` for this set up.

Lets setup our folders for ``localai`` (run these to make the folders for you if you wish)
```batch
mkdir "localai"
cd LocalAI
mkdir "models"
mkdir "images"
```

At this point we want to set up our `.env` file, here is a copy for you to use if you wish, Make sure this is in the ``LocalAI`` folder.

```bash
## Set number of threads.
## Note: prefer the number of physical cores. Overbooking the CPU degrades performance notably.
LOCALAI_THREADS=2

## **do not change this at all, this must be here to work**
LOCALAI_ADDRESS=0.0.0.0:8080

## Define galleries.
## models will to install will be visible in `/models/available`
LOCALAI_GALLERIES=[{"name":"model-gallery", "url":"github:go-skynet/model-gallery/index.yaml"}, {"url": "github:go-skynet/model-gallery/huggingface.yaml","name":"huggingface"}]

## Default path for models
LOCALAI_MODELS_PATH=/models

## Enable debug mode
LOCALAI_DEBUG=true

## Disables COMPEL (Lets Stable Diffuser work)
LOCALAI_COMPEL=0

## Enable/Disable single backend (useful if only one GPU is available)
# SINGLE_ACTIVE_BACKEND=true

## Specify a build type. Available: cublas, openblas, clblas.
LOCALAI_BUILD_TYPE=cublas

# LOCALAI_REBUILD=true
LOCALAI_SINGLE_ACTIVE_BACKEND=true

## Enable go tags, available: stablediffusion, tts
## stablediffusion: image generation with stablediffusion
## tts: enables text-to-speech with go-piper 
## (requires LOCALAI_REBUILD=true)
#
# LOCALAI_GO_TAGS=tts

## Path where to store generated images
# LOCALAI_IMAGE_PATH=/tmp

## Specify a default upload limit in MB (whisper)
# LOCALAI_UPLOAD_LIMIT

# LOCALAI_HUGGINGFACEHUB_API_TOKEN=Token here
```


Now that we have the `.env` set lets set up our `docker-compose.yaml` file.
It will use a container from [quay.io](https://quay.io/repository/go-skynet/local-ai?tab=tags).

{{< tabs >}}
{{% tab title="Vanilla / CPU Images" %}}
Recommened Midori AI - LocalAI Images
- `lunamidori5/localai_cpu:master`

For a full list of tags or images please [check our docker repo](https://hub.docker.com/r/lunamidori5/localai_cpu/tags)

Base LocalAI Images
- `master`
- `latest`

Core Images - Smaller images without predownload python dependencies
{{% /tab %}}

{{% tab title="GPU Images CUDA 11" %}}

Images with Nvidia accelleration support

> If you do not know which version of CUDA do you have available, you can check with `nvidia-smi` or `nvcc --version`

Recommened Midori AI - LocalAI Images (Only Nvidia works for now)
- `lunamidori5/localai_nvidia_gpu:master`
- `lunamidori5/localai_hipblas_gpu:master`
- `lunamidori5/localai_intelf16_gpu:master`
- `lunamidori5/localai_intelf32_gpu:master`

For a full list of tags or images please [check our docker repo](https://hub.docker.com/r/lunamidori5)

Base LocalAI Images
- `master-cublas-cuda11`
- `master-cublas-cuda11-core`
- `master-cublas-cuda11-extras`

Core Images - Smaller images without predownload python dependencies
{{% /tab %}}

{{% tab title="GPU Images CUDA 12" %}}

Images with Nvidia accelleration support

> If you do not know which version of CUDA do you have available, you can check with `nvidia-smi` or `nvcc --version`

Recommened Midori AI - LocalAI Images (Only Nvidia works for now)
- `lunamidori5/localai_nvidia_gpu:master`
- `lunamidori5/localai_hipblas_gpu:master`
- `lunamidori5/localai_intelf16_gpu:master`
- `lunamidori5/localai_intelf32_gpu:master`

For a full list of tags or images please [check our docker repo](https://hub.docker.com/r/lunamidori5)

Base LocalAI Images
- `master-cublas-cuda12`
- `master-cublas-cuda12-core`
- `master-cublas-cuda12-extras`

Core Images - Smaller images without predownload python dependencies

{{% /tab %}}

{{< /tabs >}}

{{< tabs >}}
{{% tab title="CPU Only" %}}
Also note this `docker-compose.yaml` file is for `CPU` only.

```docker

services:
  localai-midori-ai-backend:
    image: lunamidori5/localai_cpu:master
    ## use this for localai's base 
    ## image: quay.io/go-skynet/local-ai:master
    tty: true # enable colorized logs
    restart: always # should this be on-failure ?
    ports:
      - 8080:8080
    env_file:
      - .env
    volumes:
      - ./models:/models
      - ./images/:/tmp/generated/images/
    command: ["local-ai"]
```
{{% /tab %}}

{{% tab title="GPU and CPU" %}}
Also note this `docker-compose.yaml` file is for `CUDA` only.

Please change the image to what you need.

```docker

services:
  localai-midori-ai-backend:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    ## use this for localai's base 
    ## image: quay.io/go-skynet/local-ai:CHANGEMETOIMAGENEEDED
    image: lunamidori5/localai_nvidia_gpu:master
    tty: true # enable colorized logs
    restart: always # should this be on-failure ?
    ports:
      - 8080:8080
    env_file:
      - .env
    volumes:
      - ./models:/models
      - ./images/:/tmp/generated/images/
    command: ["local-ai"]
```
{{% /tab %}}
{{< /tabs >}}


Make sure to save that in the root of the `LocalAI` folder. Then lets spin up the Docker run this in a `CMD` or `BASH`

```bash
docker compose up -d --pull always
```


Now we are going to let that set up, once it is done, lets check to make sure our huggingface / localai galleries are working (wait until you see this screen to do this)

You should see (This is outdated and needs to be updated to show the new ready text):
```
┌───────────────────────────────────────────────────┐
│                   Fiber v2.42.0                   │
│               http://127.0.0.1:8080               │
│       (bound on host 0.0.0.0 and port 8080)       │
│                                                   │
│ Handlers ............. 1  Processes ........... 1 │
│ Prefork ....... Disabled  PID ................. 1 │
└───────────────────────────────────────────────────┘
```

Now that we got that setup, lets go setup a [model]({{%relref "easy-model" %}})
