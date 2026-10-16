import math, sys

U = 5            # tamaño de cada pixel de la cuadrícula (px)
W, H = 200, 44   # cuadrícula 200x44 -> lienzo 1000x220

FONT = {
 'A': [".###.","#...#","#...#","#####","#...#","#...#","#...#"],
 'B': ["####.","#...#","#...#","####.","#...#","#...#","####."],
 'C': [".####","#....","#....","#....","#....","#....",".####"],
 'D': ["####.","#...#","#...#","#...#","#...#","#...#","####."],
 'E': ["#####","#....","#....","####.","#....","#....","#####"],
 'F': ["#####","#....","#....","####.","#....","#....","#...."],
 'G': [".####","#....","#....","#..##","#...#","#...#",".####"],
 'H': ["#...#","#...#","#...#","#####","#...#","#...#","#...#"],
 'I': ["#####","..#..","..#..","..#..","..#..","..#..","#####"],
 'J': ["....#","....#","....#","....#","#...#","#...#",".###."],
 'K': ["#...#","#..#.","#.#..","##...","#.#..","#..#.","#...#"],
 'L': ["#....","#....","#....","#....","#....","#....","#####"],
 'M': ["#...#","##.##","#.#.#","#.#.#","#...#","#...#","#...#"],
 'N': ["#...#","##..#","##..#","#.#.#","#..##","#..##","#...#"],
 'O': [".###.","#...#","#...#","#...#","#...#","#...#",".###."],
 'P': ["####.","#...#","#...#","####.","#....","#....","#...."],
 'R': ["####.","#...#","#...#","####.","#.#..","#..#.","#...#"],
 'S': [".####","#....","#....",".###.","....#","....#","####."],
 'T': ["#####","..#..","..#..","..#..","..#..","..#..","..#.."],
 'U': ["#...#","#...#","#...#","#...#","#...#","#...#",".###."],
 'V': ["#...#","#...#","#...#","#...#","#...#",".#.#.","..#.."],
 'W': ["#...#","#...#","#...#","#.#.#","#.#.#","##.##","#...#"],
 'Y': ["#...#","#...#",".#.#.","..#..","..#..","..#..","..#.."],
 'É': ["..##.",  "#####","#....","#....","####.","#....","#....","#####"],
 ',': [".....",".....",".....",".....",".....","..#..",".#..."],
 '.': [".....",".....",".....",".....",".....",".....","..#.."],
 '·': [".....",".....",".....","..#..",".....",".....","....."],
 ' ': ["....."]*7,
}

def text_path(s, x0, y0, px):
    """Devuelve el path d de un texto; x0,y0 en px, px = tamaño del pixel de fuente."""
    d = []
    cx = x0
    for ch in s:
        g = FONT[ch]
        off = 7 - len(g)  # alinea por la base (el acento de É queda arriba)
        for r, row in enumerate(g):
            c = 0
            while c < 5:
                if row[c] == '#':
                    e = c
                    while e < 5 and row[e] == '#':
                        e += 1
                    d.append(f"M{cx + c*px} {y0 + (r+off)*px}h{(e-c)*px}v{px}h-{(e-c)*px}z")
                    c = e
                else:
                    c += 1
        cx += 6 * px
    return "".join(d)

grid = {}  # (x,y) -> color

def put(x, y, c):
    if 0 <= x < W and 0 <= y < H:
        grid[(x, y)] = c

# --- cielo en bandas con dithering ---
bands = [(0,"#140c2b"),(7,"#1c1038"),(14,"#2a1548"),(20,"#3f1b57"),(26,"#5c2260"),(31,"#85305f"),(35,"#b0445c")]
for i, (r0, col) in enumerate(bands):
    r1 = bands[i+1][0] if i+1 < len(bands) else 38
    for y in range(r0, r1):
        for x in range(W):
            put(x, y, col)
    if i+1 < len(bands):
        for x in range(1, W, 2):
            put(x, r1-1, bands[i+1][1])

# --- sol (Hinomaru) ---
cx, cy, R = 150, 15, 7.5
for y in range(H):
    for x in range(W):
        dd = math.hypot(x + .5 - cx, y + .5 - cy)
        if dd <= R:
            put(x, y, "#e63946" if dd > 4.5 else "#f0505a")

# --- monte Fuji ---
px0, top = 140, 24
for y in range(top, 38):
    hw = (y - top) * 2 + 1
    for x in range(px0 - hw, px0 + hw):
        col = "#33215c" if x < px0 else "#27184a"
        depth = 3 + ((x * 7) % 3) - 1
        if y - top < depth:
            col = "#f4ecf7" if x < px0 else "#cdbfe0"
        put(x, y, col)

# --- suelo ---
for y in range(38, H):
    for x in range(W):
        put(x, y, "#0f0820")
for x in range(W):
    put(x, 38, "#1d1236" if (x // 3) % 2 == 0 else "#170e2c")

# --- torii ---
RED, DRK, BLK = "#d62839", "#8f1d2c", "#2b1220"
for y in range(24, 38):
    for x in (178, 179, 190, 191):
        put(x, y, RED if x in (178, 190) else DRK)
for x in range(173, 197):
    put(x, 21, BLK); put(x, 22, RED)
for x in (173, 174, 195, 196):
    put(x, 20, BLK)
for x in range(177, 193):
    put(x, 26, RED); put(x, 27, DRK)
for y in range(23, 26):
    put(184, y, RED); put(185, y, DRK)

# --- convierte la cuadrícula en rects por color (runs horizontales) ---
by_color = {}
for y in range(H):
    x = 0
    while x < W:
        c = grid.get((x, y))
        if c is None:
            x += 1; continue
        e = x
        while e < W and grid.get((e, y)) == c:
            e += 1
        by_color.setdefault(c, []).append(f"M{x*U} {y*U}h{(e-x)*U}v{U}h-{(e-x)*U}z")
        x = e

sky_paths = "".join(f'<path fill="{c}" d="{"".join(p)}"/>' for c, p in by_color.items())

# --- borde pixelado ---
bd = "#7c5aa6"
border = (f'<path fill="{bd}" d="M0 0h{W*U}v{U}h-{W*U}z M0 {(H-1)*U}h{W*U}v{U}h-{W*U}z '
          f'M0 0h{U}v{H*U}h-{U}z M{(W-1)*U} 0h{U}v{H*U}h-{U}z"/>')

# --- estrellas ---
stars_pos = [(20,3),(62,5),(96,2),(112,4),(130,3),(167,4),(190,3),(174,10),(196,14),(128,11)]
stars = "".join(
    f'<rect class="st" style="animation-delay:{(i*0.37)%2.6:.2f}s" x="{x*U}" y="{y*U}" width="{U}" height="{U}" fill="#fff1f2"/>'
    for i, (x, y) in enumerate(stars_pos))

# --- pétalos de sakura ---
petals_cfg = [(140,9,-1),(152,11,-4),(163,8,-6),(172,12,-2),(182,10,-7),(192,9,-3),(100,13,-5),(40,12,-8)]
petals = "".join(
    f'<g class="pt" style="animation-duration:{d}s;animation-delay:{dl}s"><rect x="{x*U}" y="0" width="{2*U}" height="{U}" fill="#f7a8c4"/>'
    f'<rect x="{(x+1)*U}" y="{U}" width="{U}" height="{U}" fill="#ffd0de"/></g>'
    for x, d, dl in petals_cfg)

# --- textos ---
T1 = "HOLA, SOY ANDRÉS V."
T2 = "DESARROLLADOR DE SOFTWARE"
T3 = "JAVA · KOTLIN · PYTHON"
tx = 60
t1y, t2y, t3y = 45, 100, 135
p1, p2, p3 = U, 3, 3
w1, w2, w3 = len(T1)*6*p1, len(T2)*6*p2, len(T3)*6*p3
cursor_x = tx + w3 + 6

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W*U} {H*U}" shape-rendering="crispEdges" role="img" aria-label="Hola, soy Andrés V. Desarrollador de software">
  <defs>
    <clipPath id="c1"><rect class="rv" x="{tx}" y="30" width="{w1+U+4}" height="60"/></clipPath>
    <clipPath id="c2"><rect class="rv" x="{tx}" y="{t2y-3}" width="{w2+8}" height="30"/></clipPath>
    <clipPath id="c3"><rect class="rv" x="{tx}" y="{t3y-3}" width="{w3+8}" height="30"/></clipPath>
    <style>
      .cur {{ fill: #ffd166; }}
      @media (prefers-reduced-motion: no-preference) {{
        @keyframes rev {{ from {{ width: 0; }} }}
        @keyframes blink {{ 0% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
        @keyframes tw {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: .15; }} }}
        @keyframes fall {{ from {{ transform: translate(0, -20px); }} to {{ transform: translate(-70px, 240px); }} }}
        #c1 .rv {{ animation: rev 1.5s steps(19) .4s backwards; }}
        #c2 .rv {{ animation: rev 1.5s steps(25) 2.2s backwards; }}
        #c3 .rv {{ animation: rev 1.3s steps(22) 4.2s backwards; }}
        .cur {{ opacity: 0; animation: blink 1s steps(1) 5.6s infinite; }}
        .st {{ animation: tw 2.6s steps(2) infinite; }}
        .pt {{ animation: fall 9s linear infinite; }}
      }}
    </style>
  </defs>
  {sky_paths}
  {stars}
  {petals}
  <g clip-path="url(#c1)">
    <path fill="#7a1f3d" transform="translate({U} {U})" d="{text_path(T1, tx, t1y, p1)}"/>
    <path fill="#fff1f2" d="{text_path(T1, tx, t1y, p1)}"/>
  </g>
  <g clip-path="url(#c2)">
    <path fill="#0f0820" transform="translate(3 3)" d="{text_path(T2, tx, t2y, p2)}"/>
    <path fill="#f4c2d0" d="{text_path(T2, tx, t2y, p2)}"/>
  </g>
  <g clip-path="url(#c3)">
    <path fill="#0f0820" transform="translate(3 3)" d="{text_path(T3, tx, t3y, p3)}"/>
    <path fill="#ffd166" d="{text_path(T3, tx, t3y, p3)}"/>
  </g>
  <rect class="cur" x="{cursor_x}" y="{t3y}" width="12" height="21"/>
  {border}
</svg>
'''
open(sys.argv[1], "w", encoding="utf-8").write(svg)
print(len(svg), "bytes")
