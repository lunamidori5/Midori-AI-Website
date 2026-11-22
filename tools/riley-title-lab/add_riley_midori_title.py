#!/usr/bin/env python3
"""Riley Midori Title Lab — renders editable static artwork and seamless title loops.

Uses the original image unchanged. The *lettering* gets a shifting gradient while
its black offset and background stay stationary. The HTML builder exports the
settings JSON that this script loads, including text-edge smoothing controls.

Install: uv run --no-project --with pillow --with numpy

Static:
    python add_riley_midori_title.py riley_midori_original.png --settings my-colors.json

Smooth GIF (after choosing colors):
    python add_riley_midori_title.py riley_midori_original.png --settings my-colors.json --animate --format gif --fps 24 --duration 3.2

Animated WebP (usually smaller and richer colors than GIF):
    python add_riley_midori_title.py riley_midori_original.png --settings my-colors.json --animate --format webp --fps 24 --duration 3.2

Scaled output, with Lanczos-resampled source art:
    python add_riley_midori_title.py riley_midori_original.png --settings my-colors.json --res 1.1 --animate --format webp

The open .ora layer file is importable into GIMP; GIMP can save it as .xcf.
Fonts are *not* distributed; supply --font if the original local font is unavailable.
"""
from __future__ import annotations

import argparse
import base64
import json
from io import BytesIO
from pathlib import Path
import math
import zipfile
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape

import numpy as np
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

SPECTRUM = [
    {"at":0.00,"color":"#c7f8ff"},
    {"at":0.17,"color":"#57d8f4"},
    {"at":0.37,"color":"#6ef5df"},
    {"at":0.60,"color":"#c0a5ff"},
    {"at":0.81,"color":"#f19add"},
    {"at":1.00,"color":"#d4ecff"},
]

DEFAULTS = {
    "schema":"io.riley-title-lab.v1",
    "title":"Riley Midori",
    "paletteName":"Spectral",
    "stops":SPECTRUM,
    "geometry":{"x":0.50,"y":0.765,"scale":1.0,"angle":0},
    "layers":{
        "blackOffset":True,"offsetX":11,"offsetY":13,"offsetColor":"#03050b","blackOpacity":0.98,
        "shadow":True,"shadowOpacity":0.70,"shadowBlur":11,
        "keyline":True,"keylineRadius":2,
        "chroma":True,"chromaOpacity":0.68,
        "glow":True,"glowOpacity":0.12,
        "highlights":True,"highlightOpacity":0.33,
        "textAA":0.38,"edgeCrispness":0.22,
    },
    "animation":{"mode":"gentle","duration":3.2,"fps":24,"swing":0.13},
}

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "C:/Windows/Fonts/georgiab.ttf",
    "C:/Windows/Fonts/timesbd.ttf",
    "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
]


def choose_font(font: str | None):
    if font:
        if not Path(font).is_file():
            raise FileNotFoundError(font)
        return font
    for path in FONT_CANDIDATES:
        if Path(path).is_file():
            return path
    raise FileNotFoundError("No serif font found. Use --font /path/to/your/font.ttf")


def hex_rgb(s):
    s=str(s).lstrip("#")
    if len(s)!=6:
        raise ValueError(f"Not a six-digit hex color: {s}")
    return tuple(int(s[i:i+2],16) for i in (0,2,4))


def load_settings(path):
    if not path:
        return json.loads(json.dumps(DEFAULTS))
    data=json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema")!="io.riley-title-lab.v1":
        raise ValueError("Unsupported settings schema. Export settings from the Title Lab HTML builder.")
    out=json.loads(json.dumps(DEFAULTS))
    for key in ("title","paletteName","stops"):
        if key in data:
            out[key]=data[key]
    for key in ("geometry","layers","animation"):
        out[key].update(data.get(key,{}) or {})
    stops=out["stops"]
    if not 2 <= len(stops) <= 14:
        raise ValueError("At least two, at most 14 gradient stops required")
    times=[float(x["at"]) for x in stops]
    if times!=sorted(times) or times[0]!=0 or times[-1]!=1:
        raise ValueError("Gradient stops must be sorted from 0.0 to 1.0")
    for s in stops:
        hex_rgb(s["color"])
    for k in ("offsetColor",):
        hex_rgb(out["layers"][k])
    out["title"]=str(out["title"])[:80]
    return out


def png_bytes(img):
    b=BytesIO();img.save(b,"PNG",compress_level=6);return b.getvalue()


def rgba_from_mask(mask, color, alpha):
    layer=Image.new("RGBA",mask.size,(*hex_rgb(color),0))
    if alpha<=0:
        return layer
    if alpha>=1:
        layer.putalpha(mask)
    else:
        layer.putalpha(mask.point(lambda a:round(a*alpha)))
    return layer


def moved(mask,dx,dy):
    canvas=Image.new("L",mask.size,0)
    canvas.paste(mask,(round(dx),round(dy)))
    return canvas


def render_text_mask(w,h,text,fontpath,nominal_size,x,y,scale):
    # Create the actual text mask at 3x final resolution for anti-aliased edges.
    k=3
    size=max(20,int(round(nominal_size*scale*k)))
    limit=int(w*min(0.98,max(0.83,0.83*scale))*k)
    while size>k*20:
        font=ImageFont.truetype(fontpath,size)
        tracking=int(round(size*0.025))
        width=sum(font.getlength(ch) for ch in text) + max(0,len(text)-1)*tracking
        if width <=limit:
            break
        size-=k
    bbox=font.getbbox(text)
    height=bbox[3]-bbox[1]
    left=round(x*w*k-width/2)
    top=round(y*h*k-height/2)
    baseline=top-bbox[1]
    raw=Image.new("L",(w*k,h*k),0)
    d=ImageDraw.Draw(raw)
    cursor=left
    for ch in text:
        d.text((round(cursor),baseline),ch,fill=255,font=font)
        cursor +=font.getlength(ch)+tracking
    mask=raw.resize((w,h),Image.Resampling.LANCZOS)
    return mask,{"size":round(size/k),"x":x,"y":y,"tracking":round(tracking/k),"span_left":round(left/k),"span_right":round((left+width)/k),"glyph_top":round(top/k),"glyph_bottom":round((top+height)/k)}


def use_precise_title_mask(path, w, h, x, y, scale):
    """Reposition the shipped glyph alpha, preserving exact lettering across machines.

    Only valid for the text "Riley Midori". This raster asset is NOT a font file.
    """
    im=Image.open(path).convert("RGBA")
    alpha=im.getchannel("A")
    bb=alpha.getbbox()
    if bb is None:
        raise ValueError("Provided title mask is empty")
    origW,origH=im.size
    bx0,by0,bx1,by1=bb
    bxw,byh=bx1-bx0,by1-by0
    sx,sy=w/origW,h/origH
    newW=max(1,round(bxw*sx*scale))
    newH=max(1,round(byh*sy*scale))
    # Builder and Python apply the same geometric transform to the same mask.
    left=round((bx0+(x-.5)*origW-(scale-1)*bxw/2)*sx)
    top=round((by0+(y-.765)*origH-(scale-1)*byh/2)*sy)
    crop=alpha.crop(bb).resize((newW,newH),Image.Resampling.LANCZOS)
    canvas=Image.new("L",(w,h),0)
    canvas.paste(crop,(left,top))
    size=round(190*(h/941)*scale)
    geo={"size":size,"x":x,"y":y,"tracking":round(size*.025),
         "span_left":left,"span_right":left+newW,"glyph_top":top,"glyph_bottom":top+newH}
    return canvas,geo

def refine_mask(mask, aa=0.38, crisp=0.22, scale_ratio=1.0):
    """Gently smooth jagged raster edges, then restore a little edge definition.

    aa and crisp are normalized 0..1 controls used by the HTML lab and JSON settings.
    """
    aa=max(0.0, min(1.0, float(aa or 0.0)))
    crisp=max(0.0, min(1.0, float(crisp or 0.0)))
    out=mask
    if aa>0:
        blur_radius=(0.18 + aa*0.95) * max(0.7, scale_ratio)
        out=out.filter(ImageFilter.GaussianBlur(radius=blur_radius))
    if crisp>0:
        out=out.filter(ImageFilter.UnsharpMask(radius=max(0.5, 0.65*max(0.7, scale_ratio)), percent=int(70 + crisp*140), threshold=1))
    return out

def gradient_layer(mask,stops,angle=0,phase=0):
    bb=mask.getbbox()
    if not bb:
        raise ValueError("No visible title glyphs")
    x0,y0,x1,y1=bb
    bw,bh=x1-x0,y1-y0
    theta=math.radians(float(angle))
    ux,uy=math.cos(theta),math.sin(theta)
    projection_length=abs(ux)*(bw-1)+abs(uy)*(bh-1)
    projection_length=max(projection_length,1e-6)
    yy,xx=np.mgrid[0:bh,0:bw]
    t=(ux*(xx-(bw-1)/2)+uy*(yy-(bh-1)/2))/projection_length + .5 + float(phase)
    t=np.clip(t,0,1)
    ts=np.array([float(c["at"]) for c in stops],dtype=np.float32)
    rgb=np.empty((bh,bw,4),dtype=np.uint8)
    colors=[hex_rgb(c["color"]) for c in stops]
    for i in range(3):
        rgb[:,:,i]=np.clip(np.interp(t,ts,[c[i] for c in colors]),0,255).astype('uint8')
    rgb[:,:,3]=np.asarray(mask.crop(bb))
    layer=Image.new("RGBA",mask.size,(0,0,0,0))
    layer.paste(Image.fromarray(rgb,"RGBA"),(x0,y0))
    return layer


def add_layers_static(img, cfg, font, maskasset=None):
    w,h=img.size
    g=cfg["geometry"];la=cfg["layers"]
    original_ref_scale=h/941
    if maskasset is not None and cfg["title"]=="Riley Midori":
        mask,geo=use_precise_title_mask(maskasset,w,h,float(g["x"]),float(g["y"]),float(g["scale"]))
    else:
        if font is None:
            raise FileNotFoundError('A text font is required for a different name; use --font')
        mask,geo=render_text_mask(w,h,cfg["title"],font,round(190*original_ref_scale),float(g["x"]),float(g["y"]),float(g["scale"]))
    ratio=w/1672
    mask=refine_mask(mask, la.get("textAA",0.38), la.get("edgeCrispness",0.22), ratio)
    offx=round(float(la["offsetX"])*ratio)
    offy=round(float(la["offsetY"])*ratio)
    # layer list is top-to-bottom for ORA/GIMP
    layers=[("00 Original illustration (unchanged)",img.convert('RGBA'))]
    if la.get("shadow",True):
        m=moved(mask,offx+round(5*ratio),offy+round(6*ratio))
        m=m.filter(ImageFilter.GaussianBlur(float(la.get("shadowBlur",11))*ratio))
        layers.append(("01 Soft shadow",rgba_from_mask(m,"#020309",float(la.get("shadowOpacity",.70)))))
    if la.get("glow",True):
        m=mask.filter(ImageFilter.GaussianBlur(max(1,round(9*ratio))))
        layers.append(("02 Ambient cyan glow",rgba_from_mask(m,"#98eaff",float(la.get("glowOpacity",.12)))))
    if la.get("blackOffset",True):
        m=moved(mask,offx,offy)
        m=m.filter(ImageFilter.MaxFilter(max(3,round(9*ratio)//2*2+1)))
        layers.append(("03 Solid black offset",rgba_from_mask(m,la.get("offsetColor","#03050b"),float(la.get("blackOpacity",.98)))))
    if la.get("keyline",True):
        radius=max(1,round(float(la.get("keylineRadius",2))*ratio))
        m=mask.filter(ImageFilter.MaxFilter(radius*2+1))
        layers.append(("04 Fine dark keyline",rgba_from_mask(m,"#060712",.92)))
    if la.get("chroma",True):
        m1=ImageChops.subtract(moved(mask,-round(3*ratio),0),mask)
        m2=ImageChops.subtract(moved(mask,round(3*ratio),round(1*ratio)),mask)
        ch=rgba_from_mask(m1,"#50f3ff",float(la.get("chromaOpacity",.68)))
        ch.alpha_composite(rgba_from_mask(m2,"#f272de",float(la.get("chromaOpacity",.68))*.8))
        layers.append(("05 Chromatic edges",ch))
    base=Image.new("RGBA",img.size,(0,0,0,0))
    for _,layer in layers:
        base.alpha_composite(layer)
    glint=None
    if la.get("highlights",True):
        edgetop=ImageChops.subtract(mask,moved(mask,0,max(1,round(2*ratio))))
        glint=rgba_from_mask(edgetop,"#f3fdff",float(la.get("highlightOpacity",.33)))
    return {"base":base,"layers":layers,"mask":mask,"geo":geo,"glint":glint}


def merge(layers):
    out=Image.new("RGBA",layers[0][1].size,(0,0,0,0))
    for _,layer in layers:
        out.alpha_composite(layer)
    return out


def frame_from_setup(static,cfg,phase):
    grad=gradient_layer(static["mask"],cfg["stops"],cfg["geometry"].get("angle",0),phase)
    img=static["base"].copy()
    img.alpha_composite(grad)
    if static["glint"]:
        img.alpha_composite(static["glint"])
    return img


def save_ora(path, layers, merged):
    w,h=merged.size
    root=ET.Element("image",{"w":str(w),"h":str(h),"name":"Riley Midori - color lab layers","version":"0.0.1"})
    stack=ET.SubElement(root,"stack")
    with zipfile.ZipFile(path,'w') as z:
        z.writestr('mimetype','image/openraster',compress_type=zipfile.ZIP_STORED)
        for idx,(name,img) in enumerate(reversed(layers)):
            src=f"data/layer{idx:02d}.png"
            ET.SubElement(stack,'layer',{'name':name,'src':src,'x':'0','y':'0','opacity':'1.0','visibility':'visible','composite-op':'svg:src-over'})
            z.writestr(src,png_bytes(img),compress_type=zipfile.ZIP_DEFLATED,compresslevel=5)
        z.writestr('stack.xml',ET.tostring(root,encoding='utf-8',xml_declaration=True))
        z.writestr('mergedimage.png',png_bytes(merged),compress_type=zipfile.ZIP_DEFLATED,compresslevel=5)
        thumb=merged.copy();thumb.thumbnail((256,256));z.writestr('Thumbnails/thumbnail.png',png_bytes(thumb))


def save_svg(path,img,cfg,geo):
    # SVG lives at static coordinates and uses editable text. The embedded source image is unmodified.
    w,h=img.size;g=cfg['geometry'];l=cfg['layers']
    baseline=round((geo['glyph_top']+geo['glyph_bottom'])/2 +geo['size']*.31)
    cx=round(float(g['x'])*w);sx=round(float(l['offsetX'])*w/1672);sy=round(float(l['offsetY'])*h/941)
    stops=''.join('<stop offset="%.1f%%" stop-color="%s"/>'%(100*float(c['at']),c['color']) for c in cfg['stops'])
    b64=base64.b64encode(png_bytes(img.convert('RGB'))).decode('ascii')
    name=escape(cfg['title']);wght=round(geo['size']);tracking=geo['tracking']
    svg=f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
<defs>
 <linearGradient id="riley-spectrum" x1="0%" x2="100%" y1="0%" y2="0%">{stops}</linearGradient>
 <filter id="ssoft"><feGaussianBlur stdDeviation="7"/></filter>
</defs>
<image width="{w}" height="{h}" href="data:image/png;base64,{b64}"/>
<g text-anchor="middle" font-family="Noto Serif Display,Georgia,serif" font-weight="900" font-size="{wght}" letter-spacing="{tracking}">
 <text x="{cx+sx+5}" y="{baseline+sy+6}" fill="{l['offsetColor']}" opacity="0.65" filter="url(#ssoft)">{name}</text>
 <text x="{cx+sx}" y="{baseline+sy}" fill="{l['offsetColor']}" stroke="{l['offsetColor']}" stroke-width="4" paint-order="stroke fill">{name}</text>
 <text x="{cx}" y="{baseline}" fill="#060712" stroke="#060712" stroke-width="3" paint-order="stroke fill">{name}</text>
 <text x="{cx}" y="{baseline}" fill="url(#riley-spectrum)">{name}</text>
</g>
</svg>'''
    path.write_text(svg,encoding='utf-8')


def write_static(img,cfg,font,out,maskasset):
    static=add_layers_static(img,cfg,font,maskasset)
    grad=gradient_layer(static['mask'],cfg['stops'],cfg['geometry'].get('angle',0),0)
    ls=static['layers']+ [('06 Gradient lettering',grad)]
    if static['glint']:
        ls.append(('07 Pale highlights',static['glint']))
    preview=merge(ls)
    png=out.with_name(out.name+'-preview.png')
    preview.convert('RGB').save(png,optimize=True)
    ora=out.with_suffix('.ora');save_ora(ora,ls,preview)
    svg=out.with_suffix('.svg');save_svg(svg,img,cfg,static['geo'])
    print('Static title:',png,ora,svg)
    return png


def animate(img,cfg,font,out,fmt,duration,fps,maskasset):
    if fmt not in ('gif','webp','apng'):
        raise ValueError('Choose gif, webp, or apng')
    count=max(2,int(round(fps*duration)))
    if count>240:
        raise ValueError('Too many frames: choose <=240')
    static=add_layers_static(img,cfg,font,maskasset)
    swing=float(cfg['animation'].get('swing',.13))
    mode=cfg['animation'].get('mode','gentle')
    # Accurate closed loop: frame k uses sin(2 pi k / frame_count), so the
    # next frame after the last one mathematically matches frame 0.
    def each_frame(k):
        phase=swing * (1.45 if mode=='lively' else 1.0) * math.sin(2*math.pi*(k/count)) if mode!='off' else 0
        return frame_from_setup(static,cfg,phase).convert('RGB')
    ext={'gif':'.gif','webp':'.webp','apng':'.png'}[fmt]
    dest=out.with_name(out.name+'-loop'+ext)
    delay=round(1000/fps)
    if fmt=='gif':
        # GIF delays are stored in centiseconds. Distribute the rounding
        # remainder across frames so the total loop duration stays accurate.
        total_delay_cs=round(duration*100)
        base_delay_cs,remainder_cs=divmod(total_delay_cs,count)
        frame_delays=[10*(base_delay_cs+int(((i+1)*remainder_cs)//count > (i*remainder_cs)//count)) for i in range(count)]
    print(f'Writing {count} frames at {img.width}x{img.height}, {fps} fps, {duration:g}s, format={fmt}...')
    if fmt=='gif':
        # GIF is limited to 256 indexed colors. Use one stable global palette
        # across frames to reduce color flicker; animation is title-only. Keep
        # the preceding frame so Pillow can encode only changed rectangles.
        frames=[]
        p0=each_frame(0).quantize(colors=255,method=Image.Quantize.MEDIANCUT,dither=Image.Dither.FLOYDSTEINBERG)
        frames.append(p0)
        for i in range(1,count):
            frames.append(each_frame(i).quantize(palette=p0,dither=Image.Dither.FLOYDSTEINBERG))
        frames[0].save(dest,format='GIF',save_all=True,append_images=frames[1:],duration=frame_delays,loop=0,optimize=True,disposal=1)
    else:
        frames=[each_frame(k) for k in range(count)]
        if fmt=='webp':
            frames[0].save(dest,format='WEBP',save_all=True,append_images=frames[1:],duration=delay,loop=0,quality=92,method=5)
        else:
            frames[0].save(dest,format='PNG',save_all=True,append_images=frames[1:],duration=delay,loop=0,disposal=0,blend=0)
    print('Animated title loop:',dest)
    return dest


def main():
    p=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('input',type=Path,help='Original illustration PNG')
    p.add_argument('--settings',type=Path,default=None,help='JSON saved from the HTML Title Lab')
    p.add_argument('--output',type=Path,default=None,help='Output filename prefix')
    p.add_argument('--font',default=None,help='Optional TrueType/OpenType font path (not packaged)')
    p.add_argument('--mask',type=Path,default=None,help='Optional original lettering alpha mask; auto-detected beside this script')
    p.add_argument('--text',default=None,help='Override title text')
    p.add_argument('--x',type=float,default=None,help='Override horizontal fraction')
    p.add_argument('--y',type=float,default=None,help='Override vertical fraction')
    p.add_argument('--size',type=int,default=None,help='Legacy override for maximum original-size font height in pixels')
    p.add_argument('--offset-x',type=int,default=None,help='Legacy override: black backing shift X (pixels at source size)')
    p.add_argument('--offset-y',type=int,default=None,help='Legacy override: black backing shift Y (pixels at source size)')
    p.add_argument('--animate',action='store_true',help='Animate title gradient only; preserve original scene')
    p.add_argument('--format',choices=['gif','webp','apng'],default='gif',help='Animation format')
    p.add_argument('--fps',type=int,default=None,help='Frames per second, 8–30 recommended')
    p.add_argument('--duration',type=float,default=None,help='Duration in seconds, e.g. 3.2')
    p.add_argument('--res',type=float,default=1.0,help='Output resolution multiplier from 0.5 to 2.0; uses Lanczos resampling')
    args=p.parse_args()
    if not 0.5 <= args.res <= 2.0:
        p.error('res must be between 0.5 and 2.0')
    cfg=load_settings(args.settings)
    if args.text:
        cfg['title']=args.text
    for k in ('x','y'):
        if getattr(args,k) is not None:
            cfg['geometry'][k]=getattr(args,k)
    if args.size is not None:
        cfg['geometry']['scale']=args.size/190
    if args.offset_x is not None:
        cfg['layers']['offsetX']=args.offset_x
    if args.offset_y is not None:
        cfg['layers']['offsetY']=args.offset_y
    if not (0.05<float(cfg['geometry']['x'])<.95 and .3<float(cfg['geometry']['y'])<.98):
        p.error('Title position must be inside the image')
    if not args.input.is_file():
        p.error(f'Original illustration not found: {args.input}')
    img=Image.open(args.input).convert('RGB')
    if args.res!=1.0:
        img=img.resize((max(1,round(img.width*args.res)),max(1,round(img.height*args.res))),Image.Resampling.LANCZOS)
    default_mask=Path(__file__).with_name('riley_midori_title_mask.png')
    maskasset=args.mask or (default_mask if default_mask.is_file() else None)
    if maskasset and not maskasset.is_file():
        p.error(f'Title mask not found: {maskasset}')
    # Exact title needs no installed font when its alpha mask is supplied.
    font=choose_font(args.font) if (args.font or maskasset is None or cfg['title']!='Riley Midori') else None
    out=args.output or args.input.with_name('riley_midori_colorlab')
    out.parent.mkdir(parents=True,exist_ok=True)
    if args.animate:
        animation=cfg['animation']
        fps=args.fps or int(animation.get('fps',24))
        duration=args.duration or float(animation.get('duration',3.2))
        if not (1<=fps<=60 and .2<=duration<=20):
            p.error('fps 1–60, duration 0.2–20 seconds')
        animate(img,cfg,font,out,args.format,duration,fps,maskasset)
    else:
        write_static(img,cfg,font,out,maskasset)


if __name__=='__main__':
    main()
