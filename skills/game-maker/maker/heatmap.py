#!/usr/bin/env python3
"""Grid heat map: compare a character's game file (.glb) with the drawing it came from.

usage: python3 heatmap.py --drawing D.png --glb character.glb --out DIR [--clip NAME --time T]
                          [--fine 32] [--coarse 8] [--yaw DEG]

What it does
 1. Loads the .glb with Three.js (dump_glb.mjs) in its rest pose (or a clip at a time).
 2. Renders it straight from the front (orthographic, flat colours, no lighting) and adds
    cartoon outlines at the drawing's own line weight: round the silhouette and between two
    light-coloured parts (a dark part already reads as ink, as in the drawing).
 3. Lines the render up with the drawing (best overlap of the two silhouettes: scale + shift).
 4. Lays a grid over the drawing's character and checks every square three ways:
      SHAPE  - is there character where the drawing has character (and not where it doesn't)?
      DARK   - do the dark details line up (mask, eyes, pupils, smile, boots, fists, outlines)?
      COLOUR - is the square's average colour the same (ignores stripe phase, judges the mix)?
    A square fails if any check is over its limit. A few pixels of misalignment are forgiven.
 5. Writes heatmap.png (drawing | render | ghost overlay, failing squares in red),
    report.md (failing areas ranked, each with what is wrong and which parts are there),
    report.json, render_match.png and region_N.png close-ups (drawing left, render right).
"""
import argparse, json, os, subprocess, sys
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi
from scipy.signal import fftconvolve
from skimage.color import rgb2lab

HERE = os.path.dirname(os.path.abspath(__file__))
LIM_SHAPE, LIM_DARK, LIM_COLOUR = 12.0, 12.0, 14.0   # % of square, % of square, colour distance
DARK_L = 35.0


def load_rgb(p):
    return np.asarray(Image.open(p).convert('RGB')).astype(np.float32) / 255.0


def border_median(a):
    return np.median(np.concatenate([a[:6].reshape(-1, a.shape[-1]), a[-6:].reshape(-1, a.shape[-1]),
                                     a[:, :6].reshape(-1, a.shape[-1]), a[:, -6:].reshape(-1, a.shape[-1])]), 0)


def fg_mask(lab, bg, thr=22.0):
    m = np.linalg.norm(lab - bg, axis=2) > thr
    m = ndi.binary_opening(m, iterations=1)
    lbl, n = ndi.label(m)
    if n:
        sizes = ndi.sum(m, lbl, range(1, n + 1))
        m = np.isin(lbl, 1 + np.where(sizes > max(400, 0.002 * m.size))[0])
    return ndi.binary_fill_holes(m)


def ink_width(lab):
    L = lab[..., 0] < 30
    runs = []
    for r in range(0, L.shape[0], 8):
        d = np.diff(np.concatenate([[0], L[r].astype(np.int8), [0]]))
        w = np.where(d == -1)[0] - np.where(d == 1)[0]
        runs += list(w[(w >= 4) & (w <= 0.03 * L.shape[1])])
    return float(np.median(runs)) if runs else 0.016 * L.shape[1]


def dump(glb, prefix, clip, t):
    prefix = os.path.abspath(prefix)   # the node loader runs from this folder; keep relative --out paths working
    args =['node', os.path.join(HERE, 'dump_glb.mjs'), os.path.abspath(glb), prefix] + ([clip, str(t)] if clip else [])
    r = subprocess.run(args, cwd=HERE, capture_output=True, text=True)
    if r.returncode:
        sys.exit('could not load the .glb: ' + r.stderr.strip())
    meta = json.load(open(prefix + '.json'))
    n = meta['ntri']
    raw = open(prefix + '.bin', 'rb').read()
    o = 0
    pos = np.frombuffer(raw, np.float32, n * 9, o).reshape(n, 3, 3); o += n * 36
    col = np.frombuffer(raw, np.float32, n * 9, o).reshape(n, 3, 3); o += n * 36
    part = np.frombuffer(raw, np.int32, n, o); o += n * 4
    side = np.frombuffer(raw, np.int8, n, o)
    return pos.copy(), col.copy(), part.copy(), side.copy(), meta


def cull(pos, side):
    x, y = pos[..., 0], pos[..., 1]
    a = (x[:, 1] - x[:, 0]) * (y[:, 2] - y[:, 0]) - (x[:, 2] - x[:, 0]) * (y[:, 1] - y[:, 0])
    return np.where(side == 2, a != 0, np.where(side == 1, a < 0, a > 0))


def raster(pos, col, part, s, tx, ty, H, W, ss=2):
    """Z-buffered raster at ss x resolution, vertex colours interpolated. Nearest surface wins
    (+Z is toward the viewer), so decals that sit a hair above a body still show."""
    Hs, Ws = H * ss, W * ss
    X = (pos[..., 0] * s + tx) * ss
    Y = (-pos[..., 1] * s + ty) * ss
    Z = pos[..., 2]
    x0 = np.clip(np.floor(X.min(1)).astype(int), 0, Ws - 1); x1 = np.clip(np.ceil(X.max(1)).astype(int), 0, Ws - 1)
    y0 = np.clip(np.floor(Y.min(1)).astype(int), 0, Hs - 1); y1 = np.clip(np.ceil(Y.max(1)).astype(int), 0, Hs - 1)
    bw, bh = x1 - x0 + 1, y1 - y0 + 1
    ok = (X.max(1) >= 0) & (X.min(1) < Ws) & (Y.max(1) >= 0) & (Y.min(1) < Hs)
    zbuf = np.full(Hs * Ws, -np.inf, np.float32)
    frags = []
    big = np.maximum(bw, bh)
    for lo, hi in ((0, 8), (8, 16), (16, 32), (32, 64), (64, 128), (128, 256), (256, 100000)):
        sel = np.where(ok & (big > lo) & (big <= hi) | (ok & (lo == 0) & (big == 0)))[0]
        if not sel.size:
            continue
        n = min(hi, int(big[sel].max()))
        step = max(1, int(4e6 // (n * n)))
        gx, gy = np.meshgrid(np.arange(n), np.arange(n))
        gx, gy = gx.ravel(), gy.ravel()
        for c0 in range(0, sel.size, step):
            t = sel[c0:c0 + step]
            px = x0[t, None] + gx[None] + 0.5
            py = y0[t, None] + gy[None] + 0.5
            inb = (gx[None] < bw[t, None]) & (gy[None] < bh[t, None])
            ax, ay = X[t, 0, None], Y[t, 0, None]
            bx, by = X[t, 1, None], Y[t, 1, None]
            cx, cy = X[t, 2, None], Y[t, 2, None]
            den = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
            den = np.where(np.abs(den) < 1e-9, 1e-9, den)
            w0 = ((by - cy) * (px - cx) + (cx - bx) * (py - cy)) / den
            w1 = ((cy - ay) * (px - cx) + (ax - cx) * (py - cy)) / den
            w2 = 1 - w0 - w1
            e = -1e-4
            inside = inb & (w0 >= e) & (w1 >= e) & (w2 >= e)
            ti, k = np.nonzero(inside)
            if not ti.size:
                continue
            tt = t[ti]
            a0, a1, a2 = w0[ti, k], w1[ti, k], w2[ti, k]
            z = a0 * Z[tt, 0] + a1 * Z[tt, 1] + a2 * Z[tt, 2]
            pix = (y0[tt] + gy[k]) * Ws + (x0[tt] + gx[k])
            np.maximum.at(zbuf, pix, z.astype(np.float32))
            frags.append((pix, z.astype(np.float32), tt, a0.astype(np.float32), a1.astype(np.float32), a2.astype(np.float32)))
    img = np.zeros((Hs * Ws, 3), np.float32)
    pid = np.full(Hs * Ws, -1, np.int32)
    for pix, z, tt, a0, a1, a2 in frags:
        win = z >= zbuf[pix]
        pw, tw = pix[win], tt[win]
        img[pw] = (a0[win, None] * col[tw, 0] + a1[win, None] * col[tw, 1] + a2[win, None] * col[tw, 2])
        pid[pw] = part[tw]
    return img.reshape(Hs, Ws, 3), pid.reshape(Hs, Ws)


def sil_raster(pos, s, tx, ty, H, W):
    m = np.zeros((H, W), np.uint8)
    pts = np.round(np.stack([pos[..., 0] * s + tx, -pos[..., 1] * s + ty], -1) * 16).astype(np.int32)
    for p in pts:
        cv2.fillConvexPoly(m, p, 1, shift=4)
    return m.astype(bool)


def core(m, cap):
    """Silhouette weighted by thickness: thin tips (wrapper ends, cape) count less than the body."""
    d = ndi.distance_transform_edt(m)
    return (np.minimum(d, cap) / cap).astype(np.float32)


def align(pos, dmask):
    """Scale + shift that best overlaps the THICK parts of both silhouettes, so the main body
    anchors the fit and a short cape or narrow wrapper shows up as a local difference."""
    H, W = dmask.shape
    ys, xs = np.where(dmask)
    X, Y = pos[..., 0].ravel(), -pos[..., 1].ravel()
    s0 = (ys.max() - ys.min()) / max(Y.max() - Y.min(), 1e-6)
    q = 2
    cap = 0.06 * (ys.max() - ys.min()) / q
    dm = cv2.resize(dmask.astype(np.uint8), (W // q, H // q), interpolation=cv2.INTER_NEAREST) > 0
    Wd = core(dm, cap)
    nd = np.sqrt((Wd ** 2).sum())
    best = (-1, None)
    for k in np.linspace(0.75, 1.3, 56):
        s = s0 * k
        tx = (xs.min() + xs.max()) / 2 - s * (X.min() + X.max()) / 2
        ty = (ys.min() + ys.max()) / 2 - s * (Y.min() + Y.max()) / 2
        rm = sil_raster(pos, s / q, tx / q, ty / q, H // q, W // q)
        if rm.sum() < 10:
            continue
        Wr = core(rm, cap)
        corr = fftconvolve(Wd, Wr[::-1, ::-1], mode='same') / (nd * np.sqrt((Wr ** 2).sum()))
        iy, ix = np.unravel_index(np.argmax(corr), corr.shape)
        if corr[iy, ix] > best[0]:
            best = (corr[iy, ix], (s, tx + (ix - (W // q) // 2) * q, ty + (iy - (H // q) // 2) * q))
    s, tx, ty = best[1]
    capf = cap * q
    Wd1 = core(dmask, capf)
    Wr1 = core(sil_raster(pos, s, tx, ty, H, W), capf)
    bi, bt = -1, (tx, ty)
    for ddx in range(-3, 4):
        for ddy in range(-3, 4):
            v = (Wd1 * np.roll(np.roll(Wr1, ddy, 0), ddx, 1)).sum()
            if v > bi:
                bi, bt = v, (tx + ddx, ty + ddy)
    rm = sil_raster(pos, s, bt[0], bt[1], H, W)
    iou = (rm & dmask).sum() / (rm | dmask).sum()
    return s, bt[0], bt[1], iou


def add_ink(img, pid, ink_px, ink_rgb, ss=2, de_thr=12.0):
    lab = rgb2lab(np.clip(img, 0, 1))
    light = lab[..., 0] > DARK_L
    edge = np.zeros(pid.shape, bool)
    for dy, dx in ((0, 1), (1, 0), (0, -1), (-1, 0)):
        b_p = np.roll(np.roll(pid, dy, 0), dx, 1)
        b_l = np.roll(np.roll(lab, dy, 0), dx, 1)
        b_light = np.roll(np.roll(light, dy, 0), dx, 1)
        sil = (pid >= 0) & (b_p < 0)
        inner = (pid >= 0) & (b_p >= 0) & (pid != b_p) & light & b_light & \
                (np.linalg.norm(lab - b_l, axis=2) > de_thr)
        edge |= sil | inner
    r = max(1, int(round(ink_px * ss / 2)))
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    ink = cv2.dilate(edge.astype(np.uint8), k) > 0
    # silhouette ink sits half outside the body, like the drawing's outline
    out = img.copy()
    out[ink] = ink_rgb
    return out, (pid >= 0) | ink


def hexc(rgb):
    return '#%02x%02x%02x' % tuple(np.clip(np.round(np.asarray(rgb) * 255), 0, 255).astype(int))


def col_label(i):
    s, i = '', i + 1
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--drawing', required=True)
    ap.add_argument('--glb', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--clip'); ap.add_argument('--time', type=float, default=0)
    ap.add_argument('--fine', type=int, default=32)
    ap.add_argument('--coarse', type=int, default=8)
    ap.add_argument('--yaw', type=float, default=0, help='turn the model (degrees) if it does not face +Z')
    ap.add_argument('--tol', type=int, default=0, help='pixels of misalignment forgiven (0 = auto)')
    ap.add_argument('--ink', default='auto')
    ap.add_argument('--top', type=int, default=8)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    D = load_rgb(a.drawing)
    H, W = D.shape[:2]
    Dlab = rgb2lab(D)
    bg = border_median(Dlab)
    bg_rgb = border_median(D)
    dmask = fg_mask(Dlab, bg)
    ink_px = ink_width(Dlab) if a.ink == 'auto' else float(a.ink)
    dark_d = (Dlab[..., 0] < DARK_L)
    ink_rgb = np.median(D[dark_d], 0) if dark_d.any() else np.array([0.1, 0.1, 0.1])
    tol = a.tol or max(2, int(round(0.01 * W)))

    pos, col, part, side, meta = dump(a.glb, os.path.join(a.out, '_tris'), a.clip, a.time)
    if a.yaw:
        t = np.radians(a.yaw); c, s_ = np.cos(t), np.sin(t)
        x, z = pos[..., 0].copy(), pos[..., 2].copy()
        pos[..., 0], pos[..., 2] = c * x + s_ * z, -s_ * x + c * z
    keep = cull(pos, side)
    pos, col, part = pos[keep], col[keep], part[keep]
    names = meta['names']

    s, tx, ty, iou = align(pos, dmask)
    ss = 2
    img, pid = raster(pos, col, part, s, tx, ty, H, W, ss)
    img, fgm = add_ink(img, pid, ink_px, ink_rgb, ss)
    img[~fgm] = bg_rgb
    R = cv2.resize(img, (W, H), interpolation=cv2.INTER_AREA)
    pid1 = pid[::ss, ::ss]
    Image.fromarray((np.clip(R, 0, 1) * 255).astype(np.uint8)).save(os.path.join(a.out, 'render_match.png'))
    Rlab = rgb2lab(np.clip(R, 0, 1))
    rmask = np.linalg.norm(Rlab - bg, axis=2) > 22
    rmask = ndi.binary_fill_holes(rmask)
    dark_r = Rlab[..., 0] < DARK_L

    # tolerance: forgive `tol` px of misalignment
    kr = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * tol + 1, 2 * tol + 1))
    dil = lambda m: cv2.dilate(m.astype(np.uint8), kr) > 0
    shape_bad = (dmask & ~dil(rmask)) | (rmask & ~dil(dmask))
    shape_missing = dmask & ~dil(rmask)
    dark_bad = (dark_d & ~dil(dark_r)) | (dark_r & ~dil(dark_d))
    dark_missing = dark_d & ~dil(dark_r)
    light_both = dmask & rmask & ~dark_d & ~dark_r

    ys, xs = np.where(dmask)
    pad = 0.04 * max(np.ptp(ys), np.ptp(xs))
    gy0, gy1 = max(0, ys.min() - pad), min(H, ys.max() + pad)
    gx0, gx1 = max(0, xs.min() - pad), min(W, xs.max() + pad)
    union = dmask | rmask

    def score_grid(n):
        ey = np.linspace(gy0, gy1, n + 1).round().astype(int)
        ex = np.linspace(gx0, gx1, n + 1).round().astype(int)
        sh = np.zeros((n, n)); dk = np.zeros((n, n)); co = np.zeros((n, n)); act = np.zeros((n, n), bool)
        for i in range(n):
            for j in range(n):
                sl = (slice(ey[i], ey[i + 1]), slice(ex[j], ex[j + 1]))
                area = (ey[i + 1] - ey[i]) * (ex[j + 1] - ex[j])
                act[i, j] = union[sl].sum() >= 0.03 * area
                if not act[i, j]:
                    continue
                sh[i, j] = 100 * shape_bad[sl].sum() / area
                dk[i, j] = 100 * dark_bad[sl].sum() / area
                lb = light_both[sl]
                if lb.sum() >= 0.08 * area:
                    co[i, j] = float(np.linalg.norm(Dlab[sl][lb].mean(0) - Rlab[sl][lb].mean(0)))
        badness = np.maximum.reduce([sh / LIM_SHAPE, dk / LIM_DARK, co / LIM_COLOUR])
        return dict(ey=ey, ex=ex, shape=sh, dark=dk, colour=co, active=act, bad=badness, fail=(badness > 1) & act)

    F = score_grid(a.fine)
    C = score_grid(a.coarse)
    pass_f = 100.0 * (1 - F['fail'].sum() / max(F['active'].sum(), 1))
    pass_c = 100.0 * (1 - C['fail'].sum() / max(C['active'].sum(), 1))
    inter = (dmask & rmask).sum()
    shape_iou = inter / (dmask | rmask).sum()
    dark_match = (dark_d & dil(dark_r)).sum() / max(dark_d.sum(), 1)       # drawing's dark found in render
    dark_prec = (dark_r & dil(dark_d)).sum() / max(dark_r.sum(), 1)        # render's dark that belongs
    dark_f = 2 * dark_match * dark_prec / max(dark_match + dark_prec, 1e-6)
    miss = float((dmask & ~rmask).sum() / dmask.sum() * 100)
    extra = float((rmask & ~dmask).sum() / dmask.sum() * 100)
    lb = light_both
    col_gap = float(np.linalg.norm(Dlab[lb].mean(0) - Rlab[lb].mean(0))) if lb.any() else 0.0

    # regions = failing fine squares grouped by the coarse cell they sit in (A1, B3, ...)
    _, (ny, nx) = ndi.distance_transform_edt(pid1 < 0, return_indices=True)
    nearest_pid = pid1[ny, nx]
    ey, ex = F['ey'], F['ex']
    ci = np.clip(np.searchsorted(C['ey'], (ey[:-1] + ey[1:]) / 2) - 1, 0, a.coarse - 1)
    cj = np.clip(np.searchsorted(C['ex'], (ex[:-1] + ex[1:]) / 2) - 1, 0, a.coarse - 1)
    regions = []
    for gi in range(a.coarse):
        for gj in range(a.coarse):
            sub = F['fail'] & (ci[:, None] == gi) & (cj[None, :] == gj)
            if not sub.any():
                continue
            cells = np.argwhere(sub)
            regions.append((f"{col_label(gj)}{gi + 1}", cells))
    reg_out = []
    for cell_name, cells in regions:
        i0, j0 = cells.min(0); i1, j1 = cells.max(0)
        sev = float(sum(F['bad'][i, j] - 1 for i, j in cells))
        m = np.zeros((H, W), bool)
        for i, j in cells:
            m[ey[i]:ey[i + 1], ex[j]:ex[j + 1]] = True
        causes = []
        sh_cells = sum(F['shape'][i, j] > LIM_SHAPE for i, j in cells)
        dk_cells = sum(F['dark'][i, j] > LIM_DARK for i, j in cells)
        co_cells = sum(F['colour'][i, j] > LIM_COLOUR for i, j in cells)
        parts_here = pid1[m & (pid1 >= 0)]
        top_parts = [names[p] for p, _ in sorted(zip(*np.unique(parts_here, return_counts=True)), key=lambda t: -t[1])[:3]] if parts_here.size else []
        if sh_cells:
            mi, ex_ = (shape_missing & m).sum(), (shape_bad & ~shape_missing & m).sum()
            near = nearest_pid[shape_missing & m]
            near_parts = [names[p] for p, _ in sorted(zip(*np.unique(near[near >= 0], return_counts=True)), key=lambda t: -t[1])[:2]] if near.size else []
            if mi >= ex_:
                causes.append(f"SHAPE: drawing has character here, render does not (render too small/short here)"
                              + (f"; nearest render part: {', '.join(near_parts)}" if near_parts else ''))
            else:
                causes.append("SHAPE: render sticks out where the drawing is background (too big/long here)")
        if dk_cells:
            mi, ex_ = (dark_missing & m).sum(), (dark_bad & ~dark_missing & m).sum()
            if mi >= ex_:
                causes.append("DARK: drawing has dark detail here (mask/eye/pupil/smile/boot/fist/outline) that the render lacks or has elsewhere")
            else:
                causes.append("DARK: render has dark detail here that the drawing does not (wrong size, place or shape)")
        if co_cells:
            both = light_both & m
            if both.any():
                dl, rl = Dlab[both].mean(0), Rlab[both].mean(0)
                hint = []
                if rl[0] - dl[0] > 6: hint.append('too light')
                if dl[0] - rl[0] > 6: hint.append('too dark')
                if rl[1] - dl[1] > 6: hint.append('too red/pink')
                if dl[1] - rl[1] > 6: hint.append('not red enough')
                if rl[2] - dl[2] > 6: hint.append('too yellow')
                if dl[2] - rl[2] > 6: hint.append('too blue')
                causes.append(f"COLOUR: average drawing {hexc(np.median(D[both], 0))} vs render {hexc(np.median(R[both], 0))}"
                              + (f" (render {', '.join(hint)})" if hint else ''))
        reg_out.append(dict(
            id=0, cell=cell_name, severity=round(sev, 2), squares=int(len(cells)),
            where=f"cell {cell_name}: {(ex[j0] + ex[j1 + 1]) / 2 / W * 100:.0f}% across, {(ey[i0] + ey[i1 + 1]) / 2 / H * 100:.0f}% down",
            fine_rows=[int(i0), int(i1)], fine_cols=[int(j0), int(j1)],
            box_px=[int(ex[j0]), int(ey[i0]), int(ex[j1 + 1]), int(ey[i1 + 1])],
            render_parts=top_parts, problems=causes))
    regions = sorted(reg_out, key=lambda r: -r['severity'])
    for k, r in enumerate(regions, 1):
        r['id'] = k

    # ---- images ----
    try:
        font = ImageFont.truetype('DejaVuSans-Bold.ttf', max(14, W // 50))
        big = ImageFont.truetype('DejaVuSans-Bold.ttf', 30)
    except Exception:
        font = big = ImageFont.load_default()
    cy_, cx_ = C['ey'], C['ex']

    def panel(base):
        g = base.mean(2, keepdims=True)
        washed = 0.35 * base + 0.65 * (0.55 + 0.45 * g)        # faded, so red squares stand out
        im = Image.fromarray((np.clip(washed, 0, 1) * 255).astype(np.uint8)).convert('RGBA')
        ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
        n = a.fine
        for i in range(n):
            for j in range(n):
                if not F['active'][i, j]:
                    continue
                v = F['bad'][i, j]
                box = [ex[j], ey[i], ex[j + 1] - 1, ey[i + 1] - 1]
                if v > 1:
                    d.rectangle(box, fill=(225, 0, 0, int(min(210, 90 + (v - 1) * 60))))
                elif v > 0.7:
                    d.rectangle(box, fill=(255, 160, 0, 90))
                d.rectangle(box, outline=(90, 90, 90, 50))
        for i in range(a.coarse + 1):
            d.line([(cx_[0], cy_[i]), (cx_[-1], cy_[i])], fill=(0, 80, 220, 255), width=3)
            d.line([(cx_[i], cy_[0]), (cx_[i], cy_[-1])], fill=(0, 80, 220, 255), width=3)
        for j in range(a.coarse):
            d.text(((cx_[j] + cx_[j + 1]) / 2 - 8, max(0, cy_[0] - W // 30)), col_label(j), fill=(0, 80, 220, 255), font=font)
        for i in range(a.coarse):
            d.text((max(0, cx_[0] - W // 28), (cy_[i] + cy_[i + 1]) / 2 - 10), str(i + 1), fill=(0, 80, 220, 255), font=font)
        for r in regions[:a.top]:
            x0, y0, x1, y1 = r['box_px']
            d.rectangle([x0 - 2, y0 - 2, x1 + 2, y1 + 2], outline=(0, 0, 0, 255), width=4)
            d.rectangle([x0 - 4, y0 - 4 - 30, x0 + 30, y0 - 4], fill=(0, 0, 0, 255))
            d.text((x0 + 2, y0 - 34), str(r['id']), fill=(255, 255, 255, 255), font=font)
        return Image.alpha_composite(im, ov).convert('RGB')

    raw_r = Image.fromarray((np.clip(R, 0, 1) * 255).astype(np.uint8))
    ghost = Image.fromarray((np.clip(0.5 * D + 0.5 * R, 0, 1) * 255).astype(np.uint8))
    sheet = Image.new('RGB', (W * 3 + 40, 2 * H + 110), (255, 255, 255))
    top_row = [Image.fromarray((D * 255).astype(np.uint8)), raw_r, ghost]
    for k in range(3):
        sheet.paste(top_row[k], (k * (W + 20), 60))
    for k, base in enumerate([D, R, 0.5 * D + 0.5 * R]):
        sheet.paste(panel(base), (k * (W + 20), H + 100))
    dd = ImageDraw.Draw(sheet)
    dd.text((10, 14), f"DRAWING   |   YOUR MODEL, FRONT VIEW, LINED UP   |   GHOST OVERLAY (both at 50%)          "
                      f"fine squares passing {pass_f:.0f}%   coarse {pass_c:.0f}%   shape overlap {shape_iou * 100:.0f}%   dark details {dark_f * 100:.0f}%",
            fill=(0, 0, 0), font=big)
    dd.text((10, H + 66), "HEAT MAP: red = failing square (darker = worse), orange = close to failing; numbered boxes = areas in report.md",
            fill=(160, 0, 0), font=big)
    sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(os.path.join(a.out, 'heatmap.png'))

    for r in regions[:a.top]:
        x0, y0, x1, y1 = r['box_px']
        mg = int(0.04 * W)
        x0, y0, x1, y1 = max(0, x0 - mg), max(0, y0 - mg), min(W, x1 + mg), min(H, y1 + mg)
        cd = (np.clip(D[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8)
        cr = (np.clip(R[y0:y1, x0:x1], 0, 1) * 255).astype(np.uint8)
        k = 320 / max(1, max(cd.shape[:2]))
        cd = cv2.resize(cd, None, fx=k, fy=k); cr = cv2.resize(cr, None, fx=k, fy=k)
        gap = np.full((cd.shape[0], 14, 3), 255, np.uint8)
        Image.fromarray(np.concatenate([cd, gap, cr], 1)).save(os.path.join(a.out, f"region_{r['id']}.png"))

    rep = dict(fine_squares_passing_pct=round(pass_f, 1), coarse_squares_passing_pct=round(pass_c, 1),
               shape_overlap_pct=round(shape_iou * 100, 1), dark_details_match_pct=round(dark_f * 100, 1),
               missing_area_pct=round(miss, 1), extra_area_pct=round(extra, 1), overall_colour_gap=round(col_gap, 1),
               limits=dict(shape_pct=LIM_SHAPE, dark_pct=LIM_DARK, colour=LIM_COLOUR, tolerance_px=tol),
               fine=a.fine, coarse=a.coarse, ink_px=round(ink_px, 1), fit=dict(scale=s, tx=tx, ty=ty),
               failing_fine_squares=int(F['fail'].sum()), active_fine_squares=int(F['active'].sum()),
               regions=regions)
    json.dump(rep, open(os.path.join(a.out, 'report.json'), 'w'), indent=1)
    lines = ["# Likeness heat map",
             f"- **Fine squares passing: {pass_f:.1f}%** ({int(F['fail'].sum())} of {int(F['active'].sum())} fail, {a.fine}x{a.fine} grid)",
             f"- Coarse squares passing: {pass_c:.1f}% ({a.coarse}x{a.coarse}, blue labels A1..)",
             f"- Shape overlap {shape_iou * 100:.1f}% (missing {miss:.1f}%, extra {extra:.1f}% of the drawing's area) · dark details match {dark_f * 100:.1f}% · overall colour gap {col_gap:.1f}",
             "", "## Failing areas, worst first",
             "Numbers match the black-labelled boxes in heatmap.png. region_N.png is a close-up: drawing left, your model right."]
    for r in regions[:a.top]:
        lines.append(f"{r['id']}. **{r['where']}** · {r['squares']} squares · severity {r['severity']} · your parts here: "
                     f"{', '.join(r['render_parts']) or 'none'}")
        for c in r['problems']:
            lines.append(f"   - {c}")
    if len(regions) > a.top:
        lines.append(f"... plus {len(regions) - a.top} smaller areas (report.json)")
    open(os.path.join(a.out, 'report.md'), 'w').write('\n'.join(lines) + '\n')
    print('\n'.join(lines[:5]))


if __name__ == '__main__':
    main()
