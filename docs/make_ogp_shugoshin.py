# ogp-shugoshin.jpg（守護神の入口 shugoshin.html のリンクを貼ったときに出る看板の絵・1200×630）を作る
# 使い方: このフォルダの一つ上（hoshi-no-yashiro）で  python docs/make_ogp_shugoshin.py [字体のフォルダ]
# 字体は Noto Serif JP。Windows標準の可変フォント、なければ指定フォルダの NotoSerifJP-400.ttf / -600.ttf
# 絵は守護神のうち三貴子（月読命・天照大御神・須佐之男命）。まん中を大きく、両脇を夜空に沈める
import os
import random
import sys
from PIL import Image, ImageDraw, ImageFont, ImageChops

W, H = 1200, 630
WIN_FONT = r'C:\Windows\Fonts\NotoSerifJP-VF.ttf'
FONT_DIR = sys.argv[1] if len(sys.argv) > 1 else '.'

def font(size, weight):
    if os.path.exists(WIN_FONT):
        f = ImageFont.truetype(WIN_FONT, size)
        try:
            f.set_variation_by_axes([weight])
        except Exception:
            pass
        return f
    return ImageFont.truetype(os.path.join(FONT_DIR, 'NotoSerifJP-%d.ttf' % (600 if weight >= 550 else 400)), size)

# 夜空（ogp.png と同じ色）
bg = Image.new('RGB', (W, H))
px = bg.load()
cx, cy = W / 2, H / 2
for y in range(H):
    for x in range(W):
        d = min(1.0, (((x - cx) / (W * .62)) ** 2 + ((y - cy) / (H * .75)) ** 2) ** .5)
        t = d * d
        px[x, y] = (round(13 - 7 * t), round(13 - 7 * t), round(46 - 20 * t))
rnd = random.Random(12)
stars = Image.new('RGB', (W, H))
sd = ImageDraw.Draw(stars)
for _ in range(220):
    x, y = rnd.randrange(W), rnd.randrange(H)
    b = rnd.choice([70, 90, 110, 140, 180])
    r = 1 if rnd.random() < .85 else 2
    sd.ellipse((x - r / 2, y - r / 2, x + r / 2, y + r / 2), fill=(b, b, min(255, b + 30)))
bg = ImageChops.add(bg, stars)

def fade_mask(w, h, edge):
    # 縁 edge px を、なめらかに夜空へ溶かす（上下左右とも）
    m = Image.new('L', (w, h))
    mp = m.load()
    for y in range(h):
        for x in range(w):
            e = min(x, w - 1 - x, y, h - 1 - y) / edge
            e = max(0.0, min(1.0, e))
            mp[x, y] = round(255 * e * e * (3 - 2 * e))
    return m

def place(num, cx, cy, h, bright):
    im = Image.open('img/guardian-%d.webp' % num).convert('RGB')
    w = round(im.width * h / im.height)
    im = im.resize((w, h), Image.LANCZOS)
    if bright != 1:
        im = im.point(lambda v: round(v * bright))
    bg.paste(im, (cx - w // 2, cy - h // 2), fade_mask(w, h, 70))

# 両脇を先に、まん中をあとに（重なりはまん中が上）
place(2, 150, 320, 520, .62)   # 月読命
place(1, 450, 320, 520, .62)   # 須佐之男命
place(3, 300, 315, 640, 1)     # 天照大御神

d = ImageDraw.Draw(bg)
X = 640
d.text((X, 150), '誕生日でわかる', font=font(32, 500), fill=(255, 224, 158))
d.text((X, 200), 'あなたの守護神', font=font(66, 600), fill=(236, 236, 255))
d.text((X, 318), '記紀の十二柱から、', font=font(27, 400), fill=(184, 184, 221))
d.text((X, 364), 'あなたを守る一柱を、おみちびきします。', font=font(27, 400), fill=(184, 184, 221))
d.text((X, 452), '星の社 ── 八百万の神々', font=font(24, 500), fill=(200, 200, 232))
d.text((X, 496), 'hoshi-no-yashiro.pages.dev/shugoshin', font=font(21, 400), fill=(143, 143, 192))

bg.save('ogp-shugoshin.jpg', quality=90, optimize=True)   # 写真に近い絵なので JPEG（PNGだと700KBになる）
print('ogp-shugoshin.jpg', bg.size)
