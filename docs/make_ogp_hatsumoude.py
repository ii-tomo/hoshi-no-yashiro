# ogp-hatsumoude.jpg（初詣の入口 hatsumoude.html のリンクを貼ったときに出る看板の絵・1200×630）を作る
# 使い方: このフォルダの一つ上（hoshi-no-yashiro）で  python docs/make_ogp_hatsumoude.py [字体のフォルダ]
# 字体は Noto Serif JP。Windows標準の可変フォント、なければ指定フォルダの NotoSerifJP-400.ttf / -600.ttf
# 絵は鳥居くぐりと同じ光の鳥居（img/torii-hikari.webp）。黒い背景はアプリと同じく足し合わせで夜空に溶かす。
# 年は入れない（毎年そのまま使えるように）
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
rnd = random.Random(101)
stars = Image.new('RGB', (W, H))
sd = ImageDraw.Draw(stars)
for _ in range(240):
    x, y = rnd.randrange(W), rnd.randrange(H)
    b = rnd.choice([70, 90, 110, 140, 180])
    r = 1 if rnd.random() < .85 else 2
    sd.ellipse((x - r / 2, y - r / 2, x + r / 2, y + r / 2), fill=(b, b, min(255, b + 30)))
bg = ImageChops.add(bg, stars)

# 光の鳥居: 黒い背景ごと足し合わせる（黒は足しても変わらない＝夜空に溶ける）。縁はなめらかに落とす
torii = Image.open('img/torii-hikari.webp').convert('RGB').resize((600, 600), Image.LANCZOS)
mask = Image.new('L', torii.size)
mp = mask.load()
for y in range(600):
    for x in range(600):
        e = max(0.0, min(1.0, min(x, 599 - x, y, 599 - y) / 80))
        mp[x, y] = round(255 * e * e * (3 - 2 * e))
torii = Image.composite(torii, Image.new('RGB', torii.size), mask)
layer = Image.new('RGB', (W, H))
layer.paste(torii, (300 - 300, 330 - 300))
bg = ImageChops.add(bg, layer)

d = ImageDraw.Draw(bg)
X = 620
d.text((X, 150), '年に一度の、おみくじ', font=font(30, 500), fill=(255, 224, 158))
d.text((X, 200), '星の社で、初詣を', font=font(62, 600), fill=(236, 236, 255))
d.text((X, 314), '鳥居をくぐり、柏手を打って、', font=font(27, 400), fill=(184, 184, 221))
d.text((X, 360), '今年の一柱をおみちびきします。', font=font(27, 400), fill=(184, 184, 221))
d.text((X, 448), '星の社 ── 八百万の神々', font=font(24, 500), fill=(200, 200, 232))
d.text((X, 492), 'hoshi-no-yashiro.pages.dev/hatsumoude', font=font(21, 400), fill=(143, 143, 192))

bg.save('ogp-hatsumoude.jpg', quality=90, optimize=True)   # 写真に近い絵なので JPEG
print('ogp-hatsumoude.jpg', bg.size)
