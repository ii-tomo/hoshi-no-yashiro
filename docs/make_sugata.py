# 八柱のお姿（コウちゃんが描いた縦長のPNG）を、アプリで使う形（img/kami-<id>.webp）にする
# 使い方: このフォルダの一つ上（hoshi-no-yashiro）で  python docs/make_sugata.py <元のPNG> <id>
#   例: python docs/make_sugata.py img/_erabi/火の神.png ho  → img/kami-ho.webp
#   id は 日=hi 風=kaze 山=yama 水=mizu 火=ho 雷=kaminari 月=tsuki 星=hoshi
#
# 守護神の絵（img/guardian-<番号>.webp）と同じ形にそろえる: 縦3:4・幅768・webp
#   ・3:4 でなければ、まん中を残して切る（上下なら上寄り＝頭と後光を残す）
#   ・できたら index.html の SUGATA に id を足す。AI生成なので guide.html にも書き足す
import sys
from PIL import Image

W, H = 768, 1024


def process(src, kid):
    im = Image.open(src).convert('RGB')
    w, h = im.size
    if w * 4 > h * 3:   # 横に広い → 左右を切る
        nw = h * 3 // 4
        x = (w - nw) // 2
        im = im.crop((x, 0, x + nw, h))
    elif w * 4 < h * 3:   # 縦に長い → 下を多めに切る（頭と後光を残す）
        nh = w * 4 // 3
        y = (h - nh) // 4
        im = im.crop((0, y, w, y + nh))
    im = im.resize((W, H), Image.LANCZOS)
    dst = 'img/kami-' + kid + '.webp'
    im.save(dst, 'WEBP', quality=82, method=6)
    print(dst)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(__doc__ or 'python docs/make_sugata.py <元のPNG> <id>')
        sys.exit(1)
    process(sys.argv[1], sys.argv[2])
