# -*- coding: utf-8 -*-
"""
Generador de codigos QR con la identidad visual de Hop Invaders / Sin Hueso.

Dibuja el QR una sola vez como lista de primitivas (rects, rects redondeados,
circulos) y luego la exporta a SVG (vectorial, para imprenta) y a PNG
(supersampling 4x, para pantalla / stickers).

Uso:
    python tools/qr_gen.py
Salida:
    qr/hop-invaders-qr.svg  + .png
    qr/instagram-qr.svg     + .png
"""

import os
import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(ROOT, "qr")

# Paleta tomada de index.html
CREAM = "#f4efe6"
DEEP = "#04141c"
TEAL = "#0d3b4f"
GOLD = "#d9971e"
GOLD_HI = "#f2b53a"

SS = 4          # factor de supersampling para el PNG
PNG_SIZE = 2000  # lado final del PNG en px

# Invader clasico 11x8 (1 = pixel encendido)
INVADER = [
    "..X.....X..",
    "...X...X...",
    "..XXXXXXX..",
    ".XX.XXX.XX.",
    "XXXXXXXXXXX",
    "X.XXXXXXX.X",
    "X.X.....X.X",
    "...XX.XX...",
]


# --------------------------------------------------------------------------
# Primitivas
# --------------------------------------------------------------------------
def rect(x, y, w, h, fill, r=0.0):
    return {"t": "r", "x": x, "y": y, "w": w, "h": h, "r": r,
            "fill": fill, "stroke": None, "sw": 0}


def ring(x, y, w, h, stroke, sw, r=0.0):
    """Marco: (x,y,w,h) es la caja EXTERIOR y sw el grosor hacia adentro."""
    return {"t": "r", "x": x, "y": y, "w": w, "h": h, "r": r,
            "fill": None, "stroke": stroke, "sw": sw}


def circle(cx, cy, rad, fill=None, stroke=None, sw=0):
    """rad es el radio EXTERIOR; sw el grosor hacia adentro."""
    return {"t": "c", "cx": cx, "cy": cy, "rad": rad,
            "fill": fill, "stroke": stroke, "sw": sw}


# --------------------------------------------------------------------------
# Construccion del dibujo
# --------------------------------------------------------------------------
def build(data, style):
    """Devuelve (lista de primitivas, lado del lienzo en unidades de modulo)."""
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, border=0, box_size=1)
    qr.add_data(data)
    qr.make(fit=True)
    m = qr.get_matrix()
    n = len(m)

    quiet = 4                      # zona silenciosa obligatoria
    pad = 4                        # margen decorativo extra de la tarjeta
    cap = 7 if style["caption"] else 0   # banda para el texto
    side = n + 2 * (quiet + pad)
    ox = oy = quiet + pad          # origen del QR dentro de la tarjeta
    height = side + cap

    ops = []
    # Tarjeta
    ops.append(rect(0, 0, side, height, style["bg"], r=3.0))
    # Marco decorativo: vive en el borde de la tarjeta, muy por fuera de la
    # zona silenciosa, asi que no interfiere con la lectura.
    if style.get("frame"):
        ops.append(ring(0.7, 0.7, side - 1.4, height - 1.4,
                        style["frame"], 0.9, r=2.6))

    # Modulos reservados: los 3 patrones de deteccion (7x7) y sus separadores
    def is_finder(r, c):
        return ((r < 7 and c < 7) or
                (r < 7 and c >= n - 7) or
                (r >= n - 7 and c < 7))

    # Hueco central para el logo (impar, centrado)
    hole = style["hole"]
    h0 = (n - hole) // 2
    h1 = h0 + hole

    # Modulos de datos
    for r in range(n):
        for c in range(n):
            if not m[r][c] or is_finder(r, c):
                continue
            if h0 <= r < h1 and h0 <= c < h1:
                continue
            s = style["dot_scale"]
            off = (1 - s) / 2
            ops.append(rect(ox + c + off, oy + r + off, s, s,
                            style["fg"], r=style["dot_round"] * s))

    # Patrones de deteccion: anillo exterior + nucleo redondeado
    for (r, c) in [(0, 0), (0, n - 7), (n - 7, 0)]:
        x, y = ox + c, oy + r
        ops.append(ring(x, y, 7, 7, style["finder"], 1.0, r=style["finder_r"]))
        ops.append(rect(x + 2, y + 2, 3, 3, style["finder"],
                        r=style["finder_r"] * 0.5))

    # Logo central
    ops += style["logo"](ox + h0, oy + h0, hole, style)

    return ops, side, height, n


def logo_invader(x, y, size, style):
    """Invader dorado sobre placa oscura, dentro del hueco central.

    La placa va en color oscuro a proposito: el dorado no tiene contraste
    suficiente contra el fondo crema para un lector de celular.
    """
    gw, gh = len(INVADER[0]), len(INVADER)
    px = size * 0.86 / gw                   # tamano de cada pixel del sprite
    w, h = gw * px, gh * px
    bx = x + (size - w) / 2
    by = y + (size - h) / 2
    ops = [rect(x - 0.5, y - 0.5, size + 1, size + 1, style["bg"]),
           rect(x, y, size, size, DEEP, r=0.9)]
    for ry, row in enumerate(INVADER):
        for cx_, ch in enumerate(row):
            if ch == "X":
                ops.append(rect(bx + cx_ * px, by + ry * px, px, px, GOLD_HI))
    return ops


def logo_camera(x, y, size, style):
    """Glifo de camara (Instagram) dentro del hueco central."""
    ops = [rect(x, y, size, size, style["bg"], r=1.0)]
    m = size * 0.16
    sw = size * 0.085
    ops.append(ring(x + m, y + m, size - 2 * m, size - 2 * m,
                    style["logo_color"], sw, r=size * 0.24))
    ops.append(circle(x + size / 2, y + size / 2, size * 0.155,
                      stroke=style["logo_color"], sw=sw))
    ops.append(circle(x + size - m - sw * 1.5, y + m + sw * 1.5, sw * 0.55,
                      fill=style["logo_color"]))
    return ops


# --------------------------------------------------------------------------
# Exportadores
# --------------------------------------------------------------------------
def to_svg(ops, side, height, style, path, scale=24):
    W, H = side * scale, height * scale
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d" shape-rendering="geometricPrecision">'
        % (W, H, W, H)
    ]
    grad = style.get("gradient")
    if grad:
        stops = "".join(
            '<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in grad)
        out.append(
            '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            '%s</linearGradient></defs>' % stops)

    def col(v):
        return "url(#g)" if v == "GRAD" else v

    for o in ops:
        if o["t"] == "r":
            # SVG centra el trazo: encojo la caja media pluma para que el
            # borde exterior coincida con la caja declarada.
            k = o["sw"] / 2 if o["stroke"] else 0
            a = 'x="%.3f" y="%.3f" width="%.3f" height="%.3f"' % (
                (o["x"] + k) * scale, (o["y"] + k) * scale,
                (o["w"] - 2 * k) * scale, (o["h"] - 2 * k) * scale)
            rr = max(o["r"] - k, 0)
            if rr:
                a += ' rx="%.3f" ry="%.3f"' % (rr * scale, rr * scale)
            a += ' fill="%s"' % (col(o["fill"]) if o["fill"] else "none")
            if o["stroke"]:
                a += ' stroke="%s" stroke-width="%.3f"' % (
                    col(o["stroke"]), o["sw"] * scale)
            out.append("<rect %s/>" % a)
        else:
            k = o["sw"] / 2 if o["stroke"] else 0
            a = 'cx="%.3f" cy="%.3f" r="%.3f"' % (
                o["cx"] * scale, o["cy"] * scale, (o["rad"] - k) * scale)
            a += ' fill="%s"' % (col(o["fill"]) if o["fill"] else "none")
            if o["stroke"]:
                a += ' stroke="%s" stroke-width="%.3f"' % (
                    col(o["stroke"]), o["sw"] * scale)
            out.append("<circle %s/>" % a)

    if style["caption"]:
        out.append(
            '<text x="%.1f" y="%.1f" text-anchor="middle" '
            'font-family="Courier New, monospace" font-weight="bold" '
            'font-size="%.1f" letter-spacing="%.1f" fill="%s">%s</text>'
            % (W / 2, (height - 2.2) * scale, 2.05 * scale, 0.16 * scale,
               style["caption_color"], style["caption"]))
    out.append("</svg>")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(out))


def _gradient_image(size, grad):
    """Degradado diagonal como imagen RGB."""
    import numpy as np
    xs = np.linspace(0, 1, size)
    t = (xs[None, :] + xs[:, None]) / 2          # eje diagonal 0..1
    offs = [float(o) for o, _ in grad]
    cols = []
    for _, c in grad:
        c = c.lstrip("#")
        cols.append([int(c[i:i + 2], 16) for i in (0, 2, 4)])
    cols = np.array(cols, dtype=float)
    out = np.zeros(t.shape + (3,), dtype=float)
    for ch in range(3):
        out[..., ch] = np.interp(t, offs, cols[:, ch])
    return Image.fromarray(out.astype("uint8"), "RGB")


def to_png(ops, side, height, style, path):
    scale = (PNG_SIZE / side) * SS
    W, H = int(round(side * scale)), int(round(height * scale))
    base = Image.new("RGB", (W, H), style["bg"])
    grad = style.get("gradient")
    mask = Image.new("L", (W, H), 0) if grad else None
    dm = ImageDraw.Draw(mask) if grad else None
    d = ImageDraw.Draw(base)

    def draw(target, o, color):
        if o["t"] == "r":
            box = [o["x"] * scale, o["y"] * scale,
                   (o["x"] + o["w"]) * scale, (o["y"] + o["h"]) * scale]
            r = o["r"] * scale
            if o["fill"]:
                if r > 0.5:
                    target.rounded_rectangle(box, radius=r, fill=color)
                else:
                    target.rectangle(box, fill=color)
            if o["stroke"]:
                target.rounded_rectangle(box, radius=max(r, 0),
                                         outline=color,
                                         width=max(1, int(o["sw"] * scale)))
        else:
            box = [(o["cx"] - o["rad"]) * scale, (o["cy"] - o["rad"]) * scale,
                   (o["cx"] + o["rad"]) * scale, (o["cy"] + o["rad"]) * scale]
            if o["fill"]:
                target.ellipse(box, fill=color)
            if o["stroke"]:
                target.ellipse(box, outline=color,
                               width=max(1, int(o["sw"] * scale)))

    for o in ops:
        c = o["fill"] or o["stroke"]
        if c == "GRAD":
            draw(dm, o, 255)
        else:
            draw(d, o, c)

    if grad:
        base.paste(_gradient_image(max(W, H), grad).crop((0, 0, W, H)),
                   (0, 0), mask)

    if style["caption"]:
        fsize = int(2.05 * scale)
        font = None
        for fp in (r"C:\Windows\Fonts\consolab.ttf",
                   r"C:\Windows\Fonts\courbd.ttf"):
            if os.path.exists(fp):
                font = ImageFont.truetype(fp, fsize)
                break
        txt = style["caption"]
        if font:
            # espaciado manual entre letras, como en el SVG
            tr = int(0.16 * scale)
            widths = [font.getlength(ch) for ch in txt]
            total = sum(widths) + tr * (len(txt) - 1)
            cx = (W - total) / 2
            cy = (height - 3.9) * scale
            for ch, wd in zip(txt, widths):
                d.text((cx, cy), ch, font=font, fill=style["caption_color"])
                cx += wd + tr

    base.resize((W // SS, H // SS), Image.LANCZOS).save(path, "PNG")


# --------------------------------------------------------------------------
def make(name, data, style):
    ops, side, height, n = build(data, style)
    os.makedirs(OUT_DIR, exist_ok=True)
    svg = os.path.join(OUT_DIR, name + ".svg")
    png = os.path.join(OUT_DIR, name + ".png")
    to_svg(ops, side, height, style, svg)
    to_png(ops, side, height, style, png)
    print("  %-22s v%s  %dx%d modulos" % (name, (n - 17) // 4, n, n))
    return png


def _lum(hexcol):
    c = hexcol.lstrip("#")
    ch = []
    for i in (0, 2, 4):
        v = int(c[i:i + 2], 16) / 255.0
        ch.append(v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4)
    return 0.2126 * ch[0] + 0.7152 * ch[1] + 0.0722 * ch[2]


def _interp(t, xs, ys):
    for i in range(len(xs) - 1):
        if xs[i] <= t <= xs[i + 1]:
            f = (t - xs[i]) / (xs[i + 1] - xs[i]) if xs[i + 1] > xs[i] else 0
            return ys[i] + f * (ys[i + 1] - ys[i])
    return ys[-1] if t > xs[-1] else ys[0]


def contrast(a, b):
    la, lb = _lum(a), _lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def check_contrast(style):
    """Los lectores binarizan la imagen: todo lo que forme parte del codigo
    tiene que separarse claramente del fondo. Debajo de 4.5:1 el patron se
    pierde al pasar a blanco y negro."""
    bg = style["bg"]
    ok = True
    targets = [("modulos", style["fg"]), ("patrones", style["finder"])]
    if style["fg"] == "GRAD":
        # No basta con revisar las paradas: los tonos intermedios del
        # degradado tambien tienen que separarse del fondo.
        g = style["gradient"]
        offs = [float(o) for o, _ in g]
        cols = [[int(c.lstrip("#")[i:i + 2], 16) for i in (0, 2, 4)]
                for _, c in g]
        targets = []
        for k in range(11):
            t = k / 10.0
            rgb = [int(round(_interp(t, offs, [c[i] for c in cols])))
                   for i in range(3)]
            hexc = "#%02x%02x%02x" % tuple(rgb)
            targets.append(("degradado t=%.1f" % t, hexc))
        targets.append(("patrones", style["finder"]))
    for label, col in targets:
        r = contrast(col, bg)
        if r < 4.5:
            print("  AVISO contraste %s %s: %.1f:1 (minimo 4.5)"
                  % (label, col, r))
            ok = False
    return ok


def verify(png, expected):
    """Decodifica el PNG en varios tamanos, con y sin desenfoque, para
    aproximarse a lo que ve la camara de un celular."""
    import cv2
    img = cv2.imread(png)
    passed, tried = 0, 0
    for f in (1.0, 0.5, 0.25, 0.12):
        im = cv2.resize(img, None, fx=f, fy=f,
                        interpolation=cv2.INTER_AREA) if f != 1.0 else img
        for blur in (0, 3):
            tried += 1
            t = cv2.GaussianBlur(im, (blur, blur), 0) if blur else im
            txt, _, _ = cv2.QRCodeDetector().detectAndDecode(t)
            if txt == expected:
                passed += 1
    print("  decodifica: %s  %d/%d pruebas" %
          ("OK" if passed == tried else
           ("PARCIAL" if passed else "FALLA"), passed, tried))
    return passed == tried


GAME_URL = "https://tavomiramontes.github.io/sinHueso-hop-invaders/"
IG_URL = "https://www.instagram.com/cerveceriasinhueso/"

# Nota: el radio de los patrones de deteccion no puede pasar de ~0.8 modulos.
# Arriba de eso los lectores dejan de reconocerlos (verificado con OpenCV).
GAME_STYLE = {
    "bg": CREAM, "fg": DEEP, "finder": DEEP, "finder_r": 0.0,
    "frame": GOLD,                          # el dorado va en el marco
    "dot_scale": 1.0, "dot_round": 0.0,     # pixel art: modulos cuadrados
    "hole": 9, "logo": logo_invader,
    "caption": "SIN HUESO! HOP INVADERS",
    "caption_color": TEAL,
}

IG_STYLE = {
    "bg": CREAM, "fg": "GRAD", "finder": "#833AB4", "finder_r": 0.8,
    "frame": "#833AB4",
    # Burbujas redondas a modulo completo: separarlas se ve bonito pero el
    # lector pierde la retícula cuando la foto sale nitida y chica.
    "dot_scale": 1.0, "dot_round": 0.5,
    "hole": 9, "logo": logo_camera, "logo_color": "#B02A5B",
    # Tonos de la gama de Instagram, elegidos oscuros: los rosas claros de
    # la marca no alcanzan 4.5:1 contra el fondo crema.
    "gradient": [("0", "#4F5BD5"), ("0.5", "#833AB4"), ("1", "#B02A5B")],
    "caption": "@CERVECERIASINHUESO",
    "caption_color": "#833AB4",
}

if __name__ == "__main__":
    import sys
    ok = True
    for label, name, url, style in (
            ("Hop Invaders", "hop-invaders-qr", GAME_URL, GAME_STYLE),
            ("Instagram", "instagram-qr", IG_URL, IG_STYLE)):
        print(label + ":")
        ok &= check_contrast(style)
        ok &= verify(make(name, url, style), url)
    sys.exit(0 if ok else 1)
