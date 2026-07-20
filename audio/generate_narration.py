# オープニングのナレーション音声を生成する（op1.mp3〜op4.mp3）
#
# 前提: VOICEVOXエンジンが起動していること
#   "C:\Users\momo_\Tools\VOICEVOX\vv-engine\run.exe" --host 127.0.0.1 --port 50021
# 実行: python generate_narration.py（このフォルダで）
#
# 声: 青山龍星ノーマル(id=13)・話速0.9（2026-07-20 いいともさん選定）
# クレジット表記「VOICEVOX:青山龍星」をアプリ側(guide.html等)に必ず残すこと
import json, subprocess, shutil, os, re, urllib.request, urllib.parse, sys, io
from pathlib import Path

if (sys.stdout.encoding or "").lower() != "utf-8":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

BASE = "http://127.0.0.1:50021"
OUT = Path(__file__).parent
SPEAKER = 13          # 青山龍星 ノーマル
SPEED = 0.9
PEAK_TARGET_DB = -6.0  # 瞑想アプリなので控えめの音量に揃える

# 音声用テキスト（読み最適化済み）。画面の字幕は index.html 側が正本
# 「八百万」は「やおよろず」表記でないと「ハッピャクマン」と誤読される（2026-07-20確認）
MAKU = [
    "むかし、宇宙は、やおよろずの神々の光で、満ちていた。",
    "星のひとつひとつに神が宿り、ひかりは、歌のように、かわされていた。",
    "けれど、人が空を見上げなくなったとき、神々はひとり、またひとりと、深いねむりについた。",
    "いま、あなたの呼吸だけが、神々を、呼びさますことができる。",
]


def ffmpeg_exe():
    exe = shutil.which("ffmpeg")
    if exe:
        return exe
    root = Path(os.environ["LOCALAPPDATA"]) / "Microsoft/WinGet/Packages"
    hits = list(root.glob("**/ffmpeg.exe"))
    if hits:
        return str(hits[0])
    raise RuntimeError("ffmpegが見つかりません")


FFMPEG = ffmpeg_exe()


def post(path, params, body=None):
    url = f"{BASE}{path}?{urllib.parse.urlencode(params)}"
    data = json.dumps(body).encode() if body is not None else b""
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def peak_db(path):
    p = subprocess.run([FFMPEG, "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"max_volume:\s*(-?[\d.]+) dB", p.stderr)
    return float(m.group(1)) if m else None


for i, text in enumerate(MAKU, 1):
    q = json.loads(post("/audio_query", {"text": text, "speaker": SPEAKER}))
    print(f"幕{i} 読み: {q.get('kana', '')}")
    q["speedScale"] = SPEED
    q["prePhonemeLength"] = 0.3
    q["postPhonemeLength"] = 0.9
    wav = post("/synthesis", {"speaker": SPEAKER}, q)
    tmp = OUT / f"_op{i}.wav"
    tmp.write_bytes(wav)
    peak = peak_db(tmp)
    gain = (PEAK_TARGET_DB - peak) if peak is not None else 0.0
    dest = OUT / f"op{i}.mp3"
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", str(tmp),
                    "-af", f"volume={gain:.1f}dB", "-ar", "44100", "-b:a", "96k", str(dest)],
                   check=True)
    tmp.unlink()
    print(f"OK {dest.name} ({dest.stat().st_size} bytes, peak {peak}dB -> {PEAK_TARGET_DB}dB)")
print("done")
