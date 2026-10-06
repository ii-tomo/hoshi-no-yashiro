# 鳥居の絵（黒背景のPNG）を、宇宙神社の空間に置ける形（RGBAのwebp）にする
# 使い方: このフォルダの一つ上（hoshi-no-yashiro）で  python docs/make_torii.py <元のPNG> <出力.webp> [持ち上げ倍率]
#   持ち上げ倍率は既定1.45（星々の鳥居）。星めぐりの鳥居は元が明るいので 1.0（2026-10-06）
#
# 加工は CONCEPT.md「画像の四角い枠を消す処理」と同じ（2026-07-20 に星々の鳥居で決めたもの）:
#   ・RGBは1.45倍に持ち上げる（鳥居の存在感を残す）
#   ・輝度からアルファを作る（smoothstep 0.04〜0.20）＝暗い星空のもやだけ透明になり、鳥居と地面の光は残る
#   ・縁120pxをコサインでフェード（板の四角い枠を消す）
#   黒つぶし方式は鳥居まで暗くなるので使わない（試して失敗）
import sys
import numpy as np
from PIL import Image

SIZE, EDGE = 768, 120


def process(src, dst, gain=1.45):
    im = Image.open(src).convert('RGB').resize((SIZE, SIZE), Image.LANCZOS)
    a = np.asarray(im).astype(np.float32) / 255
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    t = np.clip((lum - 0.04) / (0.20 - 0.04), 0, 1)
    alpha = t * t * (3 - 2 * t)
    yy, xx = np.mgrid[0:SIZE, 0:SIZE]
    d = np.minimum(np.minimum(xx, SIZE - 1 - xx), np.minimum(yy, SIZE - 1 - yy)).astype(np.float32)
    alpha *= 0.5 - 0.5 * np.cos(np.pi * np.clip(d / EDGE, 0, 1))
    rgb = np.clip(a * gain, 0, 1)
    out = (np.dstack([rgb, alpha]) * 255 + 0.5).astype(np.uint8)
    Image.fromarray(out, 'RGBA').save(dst, 'WEBP', quality=85, method=6)


if __name__ == '__main__':
    process(sys.argv[1], sys.argv[2], float(sys.argv[3]) if len(sys.argv) > 3 else 1.45)
    print('saved', sys.argv[2])
