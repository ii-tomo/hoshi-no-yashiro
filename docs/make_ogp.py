# ogp.png（リンクを貼ったときに出る看板の絵・1200×630）を作る
# 使い方: このフォルダの一つ上（hoshi-no-yashiro）で  python docs/make_ogp.py
# 鳥居はアプリの空間と同じ img/torii-hoshi.webp（星々の鳥居）。アプリと同じく加算合成で宇宙に溶かす
# 文字の色はアプリの配色（#ececff / #b8b8dd / #8f8fc0）。字体は Noto Serif JP（Windows標準）
import random
from PIL import Image, ImageDraw, ImageFont, ImageChops

W, H = 1200, 630
FONT = r'C:\Windows\Fonts\NotoSerifJP-VF.ttf'

def font(size, weight):
    f = ImageFont.truetype(FONT, size)
    try:
        f.set_variation_by_axes([weight])
    except Exception:
        pass
    return f

# 夜空: 中央がわずかに明るい濃紺（前の ogp.png と同じ色）
bg = Image.new('RGB', (W, H))
px = bg.load()
cx, cy = W / 2, H / 2
for y in range(H):
    for x in range(W):
        d = min(1.0, (((x - cx) / (W * .62)) ** 2 + ((y - cy) / (H * .75)) ** 2) ** .5)
        t = d * d
        px[x, y] = (round(13 - 7 * t), round(13 - 7 * t), round(46 - 20 * t))

# 星屑（毎回同じ並びになるよう種を固定）
rnd = random.Random(88)
stars = Image.new('RGB', (W, H))
sd = ImageDraw.Draw(stars)
for _ in range(260):
    x, y = rnd.randrange(W), rnd.randrange(H)
    b = rnd.choice([70, 90, 110, 140, 180])
    r = 1 if rnd.random() < .85 else 2
    sd.ellipse((x - r / 2, y - r / 2, x + r / 2, y + r / 2), fill=(b, b, min(255, b + 30)))
bg = ImageChops.add(bg, stars)

# 星々の鳥居: RGB×アルファを足す（アプリの AdditiveBlending と同じ考え方）
torii = Image.open('img/torii-hoshi.webp').convert('RGBA')
s = 0.86
torii = torii.resize((round(torii.width * s), round(torii.height * s)), Image.LANCZOS)
r, g, b, a = torii.split()
glow = Image.merge('RGB', (
    ImageChops.multiply(r, a), ImageChops.multiply(g, a), ImageChops.multiply(b, a)))
glow = glow.point(lambda v: min(255, round(v * 1.35)))   # 小さく表示されても沈まないよう持ち上げる（アプリは×1.45）
layer = Image.new('RGB', (W, H))
layer.paste(glow, (300 - torii.width // 2, 330 - torii.height // 2 - 10))
bg = ImageChops.add(bg, layer)

# 文字（配置は前の ogp.png を踏襲）
d = ImageDraw.Draw(bg)
X = 590
d.text((X, 196), '八百万の神々', font=font(66, 600), fill=(236, 236, 255))
d.text((X, 288), '— 星の社 —', font=font(28, 500), fill=(200, 200, 232))
d.text((X, 368), '呼吸で星を生む、小さな宇宙の社。', font=font(27, 400), fill=(184, 184, 221))
d.text((X, 416), '八十八柱の神々と、縁をむすぶ。', font=font(27, 400), fill=(184, 184, 221))
d.text((X, 498), 'hoshi-no-yashiro.pages.dev', font=font(22, 400), fill=(143, 143, 192))

bg.save('ogp.png', optimize=True)
print('ogp.png', bg.size)
