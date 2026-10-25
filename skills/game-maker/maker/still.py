#!/usr/bin/env python3
"""still.png from character.glb: front three-quarter view, soft toon shading, ink outlines, light background.
usage: python3 still.py <character.glb> <still.png> [yaw_degrees=32]
Reads the .glb through Three.js (still_dump.mjs), so it shows what a game will load. No screen or GPU needed.
(From run E's render_still.py; camera now frames any character from its bounding box.)"""
import sys, os, subprocess, tempfile, numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
glb, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
yaw_deg = float(sys.argv[3]) if len(sys.argv) > 3 else 32.0
src = os.path.join(tempfile.mkdtemp(), 'tris.bin')
subprocess.run(['node', os.path.join(HERE, 'still_dump.mjs'), glb, src], cwd=HERE, check=True, capture_output=True)
raw = open(src, 'rb').read()
n = int(np.frombuffer(raw, np.float32, 1)[0]); o = 4
P = np.frombuffer(raw, np.float32, n * 9, o).reshape(n, 3, 3); o += n * 36
Nn = np.frombuffer(raw, np.float32, n * 9, o).reshape(n, 3, 3); o += n * 36
C = np.frombuffer(raw, np.float32, n * 9, o).reshape(n, 3, 3); o += n * 36
ID = np.frombuffer(raw, np.int32, n, o)

W = H = 1000; SS = 2; Ws, Hs = W * SS, H * SS
lo, hi = P.reshape(-1, 3).min(0), P.reshape(-1, 3).max(0)
target = (lo + hi) / 2
size = float(np.max(hi - lo))
yaw = np.radians(yaw_deg); dist = size * 2.5
eye = target + dist * np.array([np.sin(yaw) * np.cos(0.16), np.sin(0.16), np.cos(yaw) * np.cos(0.16)])
f = target - eye; f /= np.linalg.norm(f)
r = np.cross(f, [0, 1, 0]); r /= np.linalg.norm(r); u = np.cross(r, f)
fov = np.radians(28); foc = (Hs / 2) / np.tan(fov / 2)

def proj(X):
    d = X - eye
    z = d @ f
    return np.stack([Ws / 2 + foc * (d @ r) / z, Hs / 2 - foc * (d @ u) / z, z], -1)

S = proj(P.reshape(-1, 3)).reshape(n, 3, 3)
light = np.array([-0.45, 0.75, 0.6]); light /= np.linalg.norm(light)
lin2srgb = lambda c: np.where(c <= 0.0031308, 12.92 * c, 1.055 * np.power(np.clip(c, 0, 1), 1 / 2.4) - 0.055)

bg = np.array([0.965, 0.93, 0.87])
img = np.ones((Hs, Ws, 3)) * bg
zb = np.full((Hs, Ws), np.inf); idb = np.full((Hs, Ws), -1, np.int32)
# ground shadow: soft ellipse under the feet
gp = np.array([[target[0] + 0.5 * (hi[0] - lo[0]) * np.cos(a), lo[1], target[2] + 0.5 * max(hi[2] - lo[2], 0.3 * size) * np.sin(a)] for a in np.linspace(0, 2 * np.pi, 64)])
gs = proj(gp)
from PIL import ImageDraw
sh = Image.new('L', (Ws, Hs), 0); ImageDraw.Draw(sh).polygon([tuple(q[:2]) for q in gs], fill=255)
sh = np.asarray(sh.filter(ImageFilter.GaussianBlur(30))) / 255.0
img = img * (1 - 0.16 * sh[..., None])

view = -f
for t in range(n):
    s = S[t]
    if (s[:, 2] <= 0).any(): continue
    x0, x1 = int(max(0, np.floor(s[:, 0].min()))), int(min(Ws - 1, np.ceil(s[:, 0].max())))
    y0, y1 = int(max(0, np.floor(s[:, 1].min()))), int(min(Hs - 1, np.ceil(s[:, 1].max())))
    if x1 < x0 or y1 < y0: continue
    (ax, ay, az), (bx, by, bz), (cx, cy, cz) = s
    den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
    if abs(den) < 1e-9: continue
    yy, xx = np.mgrid[y0:y1 + 1, x0:x1 + 1] + 0.5
    w0 = ((by - cy) * (xx - cx) + (cx - bx) * (yy - cy)) / den
    w1 = ((cy - ay) * (xx - cx) + (ax - cx) * (yy - cy)) / den
    w2 = 1 - w0 - w1
    m = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
    if not m.any(): continue
    z = w0 * az + w1 * bz + w2 * cz
    sub = zb[y0:y1 + 1, x0:x1 + 1]
    m &= z < sub
    if not m.any(): continue
    nrm = w0[..., None] * Nn[t, 0] + w1[..., None] * Nn[t, 1] + w2[..., None] * Nn[t, 2]
    nrm /= np.linalg.norm(nrm, axis=-1, keepdims=True) + 1e-9
    # double-sided: flip normals facing away from camera
    vd = eye - (w0[..., None] * P[t, 0] + w1[..., None] * P[t, 1] + w2[..., None] * P[t, 2])
    flip = (nrm * vd).sum(-1) < 0; nrm[flip] *= -1
    col = w0[..., None] * C[t, 0] + w1[..., None] * C[t, 1] + w2[..., None] * C[t, 2]
    ndl = (nrm @ light)
    shade = 0.62 + 0.38 * np.clip(ndl * 1.4 + 0.15, 0, 1)  # soft toon
    hv = light + view; hv /= np.linalg.norm(hv)
    spec = np.clip(nrm @ hv, 0, 1) ** 40 * 0.25
    c = lin2srgb(col * shade[..., None]) + spec[..., None]
    sub[m] = z[m]
    img[y0:y1 + 1, x0:x1 + 1][m] = np.clip(c[m], 0, 1)
    idb[y0:y1 + 1, x0:x1 + 1][m] = ID[t]

# ink outlines: silhouette + part boundaries + depth jumps
fg = idb >= 0
edge = np.zeros_like(fg)
for dy, dx in [(0, 1), (1, 0), (1, 1), (1, -1)]:
    a = np.roll(np.roll(idb, dy, 0), dx, 1); za = np.roll(np.roll(zb, dy, 0), dx, 1)
    edge |= (a != idb) | (np.abs(np.where(np.isinf(za), 99, za) - np.where(np.isinf(zb), 99, zb)) > 0.08 * size)
lum = img.mean(-1)
dark_part = ndi.binary_dilation(lum < 0.2, iterations=1)
edge &= ~(dark_part & np.roll(dark_part, 1, 0) & np.roll(dark_part, 1, 1))
edge = ndi.binary_dilation(edge, iterations=4)
img[edge] = np.array([0.1, 0.1, 0.09])
im = Image.fromarray((img * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
im.save(out)
print('saved', out)
