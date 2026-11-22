# Riley Title Lab

This folder contains a Python renderer for the supplied three-panel artwork. It keeps the source illustration still and animates only the title gradient. The adjacent PNG mask preserves the exact “Riley Midori” lettering.

Run the script from this directory with `uv` and its two dependencies. The supplied Ember settings render 240 frames at 30 fps over 8 seconds.

```sh
uv run --with pillow --with numpy python add_riley_midori_title.py \
  riley_midori_original.png --settings ember_user.json --animate \
  --format webp --res 1.1 \
  --output /home/lunamidori/Downloads/riley-midori-ember-review-1.1x
```

Use `--format gif` for a GIF review file. `--res 1.1` resamples the 1672×941 source to 1839×1035; values from 0.5 to 2 are supported. Outputs are named `<output>-loop.gif` or `<output>-loop.webp`. Prefer WebP for website review because it preserves smoother color transitions and is much smaller than the GIF.

If `uv` cannot write to its configured cache in a sandbox, set `UV_CACHE_DIR=/tmp/riley-title-lab-uv-cache` for the command. Keep generated review files in Downloads. Do not replace or relink the live profile image until the user approves an animation.
