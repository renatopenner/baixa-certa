#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera a arte do Baixa Certa: favicons, logo SVG e imagem social (og-image).

Uso: python scripts/arte.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

RAIZ = Path(__file__).resolve().parent.parent
IMG = RAIZ / "img"
IMG.mkdir(exist_ok=True)

AZUL = (10, 124, 191)
CIANO = (18, 181, 208)
TINTA = (10, 26, 43)
CINZA = (91, 115, 137)

FONTES = Path("C:/Windows/Fonts")


def fonte(nome: str, tamanho: int) -> ImageFont.FreeTypeFont:
    for cand in (FONTES / nome, FONTES / "segoeuib.ttf", FONTES / "arialbd.ttf"):
        if cand.exists():
            return ImageFont.truetype(str(cand), tamanho)
    return ImageFont.load_default()


def gradiente(tamanho: int, a=AZUL, b=CIANO) -> Image.Image:
    img = Image.new("RGB", (tamanho, tamanho), a)
    px = img.load()
    for y in range(tamanho):
        for x in range(tamanho):
            t = (x + y) / (2 * (tamanho - 1))
            px[x, y] = (
                round(a[0] + (b[0] - a[0]) * t),
                round(a[1] + (b[1] - a[1]) * t),
                round(a[2] + (b[2] - a[2]) * t),
            )
    return img


def marca(tamanho: int) -> Image.Image:
    """Quadrado arredondado com gradiente e seta de download branca."""
    escala = 4  # desenha grande e reduz (antialiasing)
    t = tamanho * escala
    base = gradiente(t)
    mask = Image.new("L", (t, t), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, t - 1, t - 1), radius=int(t * 0.27), fill=255)
    img = Image.new("RGBA", (t, t), (0, 0, 0, 0))
    img.paste(base, (0, 0), mask)

    d = ImageDraw.Draw(img)
    lw = int(t * 0.085)
    # haste da seta
    d.line([(t * 0.5, t * 0.24), (t * 0.5, t * 0.56)], fill=(255, 255, 255, 255), width=lw)
    # ponta da seta
    d.line([(t * 0.315, t * 0.42), (t * 0.5, t * 0.59), (t * 0.685, t * 0.42)],
           fill=(255, 255, 255, 255), width=lw, joint="curve")
    # bandeja
    d.line([(t * 0.30, t * 0.73), (t * 0.70, t * 0.73)], fill=(255, 255, 255, 255), width=lw)
    return img.resize((tamanho, tamanho), Image.LANCZOS)


def favicons() -> None:
    for tam, nome in ((64, "favicon-64.png"), (180, "apple-touch-icon.png"), (192, "icon-192.png")):
        marca(tam).save(IMG / nome)
    # SVG equivalente ao PNG, para navegadores modernos
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
<stop offset="0" stop-color="#0a7cbf"/><stop offset="1" stop-color="#12b5d0"/></linearGradient></defs>
<rect width="48" height="48" rx="13" fill="url(#g)"/>
<path d="M24 12.5v14.2" stroke="#fff" stroke-width="4" stroke-linecap="round"/>
<path d="m17.2 21.4 6.8 6.8 6.8-6.8" stroke="#fff" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
<path d="M15 34.6h18" stroke="#fff" stroke-width="3.4" stroke-linecap="round" opacity=".9"/>
</svg>
'''
    (IMG / "favicon.svg").write_text(svg, encoding="utf-8")


def og_image() -> None:
    L, A = 1200, 630
    img = Image.new("RGB", (L, A), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # brilho suave no canto superior direito
    brilho = Image.new("RGB", (L, A), (255, 255, 255))
    bd = ImageDraw.Draw(brilho)
    for r in range(520, 0, -8):
        alpha = int(26 * (1 - r / 520))
        bd.ellipse((L - 300 - r, -220 - r, L - 300 + r, -220 + r),
                   fill=(18 + (255 - 18) * 0 // 1, 181, 208))
    brilho = Image.blend(img, brilho, 0.16)
    img = brilho
    d = ImageDraw.Draw(img)

    # grade de pontos discreta
    for y in range(40, A, 34):
        for x in range(40, L, 34):
            if x > 620 and y < 420:
                d.ellipse((x, y, x + 2, y + 2), fill=(226, 235, 243))

    # marca
    m = marca(132)
    img.paste(m, (84, 88), m)

    f_marca = fonte("segoeuib.ttf", 58)
    f_h1 = fonte("segoeuib.ttf", 76)
    f_sub = fonte("segoeui.ttf", 30)
    f_pe = fonte("segoeuib.ttf", 22)

    # "BAIXA" escuro + "CERTA" azul
    x = 244
    y = 108
    d.text((x, y), "BAIXA", font=f_marca, fill=TINTA)
    larg = d.textlength("BAIXA", font=f_marca)
    d.text((x + larg + 14, y), "CERTA", font=f_marca, fill=AZUL)

    d.text((84, 286), "Baixe certo.", font=f_h1, fill=TINTA)
    d.text((84, 378), "O link é do fabricante.", font=f_h1, fill=AZUL)

    d.text((84, 500),
           "Apps gratuitos com download direto do site oficial — sem instalador falso.",
           font=f_sub, fill=CINZA)
    d.text((84, 552), "baixa.pennertech.com.br", font=f_pe, fill=AZUL)
    d.text((360, 552), "·  Penner Tech", font=f_pe, fill=CINZA)

    img.save(IMG / "og-image.png", optimize=True)
    print("og-image.png", (IMG / "og-image.png").stat().st_size, "bytes")


if __name__ == "__main__":
    favicons()
    og_image()
    print("arte gerada")
