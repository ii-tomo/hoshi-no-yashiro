param([string[]]$Only = @())
$ErrorActionPreference = "Stop"
$OutputEncoding = New-Object System.Text.UTF8Encoding $false
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$base = "C:\Users\momo_\workspace\いいとも制作室\01_Projects\瞑想宇宙\Tool\hoshi-no-yashiro\img\_erabi"
$ref  = Join-Path $base "guardian-3_amaterasu.png"
$gen  = "C:\Users\momo_\.codex\generated_images"
$yobu = "C:\Users\momo_\workspace\いいとも制作室\04_Automations\AIを呼ぶ.ps1"

$kami = [ordered]@{
  "hi" = @{ na = "日の神"; iro = "朝焼けの淡い黄・薄桃・やわらかな白（#ffe09e あたり）"; nai = "炎・火の粉・月・三日月";
    sugata = "胸の前で、朝日を映す丸い円鏡（銅鏡）を両手でそっと掲げている。鏡からいちばん明るい朝の光が出る。後光は、地平線から昇る朝日の光芒。衣の裾は朝の光の粒になってほどけていく。見本の絵とは持ち物も姿勢も変え、見本と似た水晶玉は持たない。";
    fun = "夜明けとともに最初に目覚め、一日のはじまりをそっと照らす、すがすがしい明るさ" }
  "kaze" = @{ na = "風の神"; iro = "若葉の薄緑・翡翠・白（#a8ffc8 あたり）"; nai = "炎・火の粉・月・三日月・金だけの衣";
    sugata = "片手をやさしく前へ差し伸べ、長い領巾（ひれ）が大きくたなびいて渦を巻き、遠くへ流れていく。若葉や花びらが風に乗って舞う。後光は、風の流れが描く淡い緑の輪。髪も衣も風になびく。";
    fun = "とどまるものをやさしくほどき、抱えた迷いを遠くへ運んでくれる、軽やかさ" }
  "yama" = @{ na = "山の神"; iro = "砂色・苔の緑・土の茶・少しの金（#c8b89e あたり）"; nai = "炎・火の粉・月・三日月";
    sugata = "両手を下腹の前で静かに重ね、どっしりと立つ。衣は岩と苔の質感の重ねで、肩や裾に小さな山並みと木々が浮かぶ。裾は岩肌から星屑へほどけていく。後光は、山の稜線のような光の輪。";
    fun = "動かぬことの強さを知り、揺れる心に静かに根を張ってくれる、落ち着き" }
  "mizu" = @{ na = "水の神"; iro = "水色・澄んだ青・白（#9ecfff あたり）"; nai = "炎・火の粉・月・三日月・金だけの衣";
    sugata = "流れる水の帯を身にまとい、両手のひらから澄んだ水の雫がこぼれ落ちて、星になっていく。後光は、水面に広がる波紋の輪。髪は水の流れのように揺れる。";
    fun = "すべてを流し清め、今日の疲れは今日のうちに流していいと伝える、澄んだやさしさ" }
  "kaminari" = @{ na = "雷の神"; iro = "藤色・薄紫・青白い光（#d0a8ff あたり）"; nai = "炎・火の粉・月・三日月・太鼓・鬼のような姿";
    sugata = "静かに目を閉じて集中しているような立ち姿で、片手の指先を軽く掲げ、その指先に小さな一閃の稲妻が宿っている。衣と髪に、細い稲妻の光の筋が静かに走る。後光は、細い稲妻が輪になったもの。";
    fun = "ひらめきは静けさの中に落ちる。荒々しい雷ではなく、集中の果てにくれる一閃の、澄んだ静けさ" }
  "tsuki" = @{ na = "月の神"; iro = "銀・青白・淡い藍（#d8d8f0 あたり）"; nai = "炎・火の粉・金だけの衣・水晶玉";
    sugata = "両手で銀の紗（薄く透ける布）をふわりと広げ、そっとかけようとしている。背に細い三日月。紗から月の光の粒がこぼれる。後光は、月のにじみ。眠りに誘うような、ゆったりした姿勢。";
    fun = "眠れぬ夜の枕元に立ち、まぶたにそっと銀の紗をかけてくれる、静かな安らぎ" }
  "hoshi" = @{ na = "星の神"; iro = "桃色・薄紅・藍（#ff9ecf あたり）"; nai = "炎・火の粉・月・三日月・水晶玉";
    sugata = "両手のひらを上に向けて、小さな願いの星をひとつ大切に預かっている。そこからいちばん明るい光が出る。まわりに小さな星がいくつも漂う。後光は、星々が連なった輪。衣の裾は星座の線と星屑にほどけていく。";
    fun = "願いを預かり、忘れた頃に光にして返してくれる、遠くやさしい神秘" }
}

foreach ($id in $kami.Keys) {
  if ($Only.Count -gt 0 -and $Only -notcontains $id) { continue }
  $k = $kami[$id]
  $p = @"
添付の絵は「画風と質感」の見本です。絵の中身（神さま・持ち物・色）はまねしないでください。この画風で、日本の神さま「$($k.na)」を一枚描いてください。縦長 3:4。
描かないもの: $($k.nai)。全体の色は $($k.iro) にする。
背景は濃紺〜黒の宇宙（星と淡い星雲）。人の姿で、正面からやや見上げる構図。
$($k.sugata)
いちばん大事: 顔は描かない。見本の絵と同じく、顔のあるところはまぶしい光の玉になっていて、目・鼻・口・まゆは一切見えない。その光が後光につながる。白い楕円・仮面のような顔も描かない。剣や武器は持たない。
雰囲気は「$($k.fun)」。文字やサインは入れない。

# 終わり方
- 画像生成を1回だけ行い、保存やコマンドはしない（保存はこちらでやる）。
- 最後に、作った画像のパスを1行書いて終わる。
"@
  $t0 = Get-Date
  try { & $yobu -Prompt $p -Shigoto "八柱のお姿" -Omosa "並" -Yobisaki codex -Images @($ref) | Out-Null } catch { "[$id] 呼び出しで止まった: $($_.Exception.Message)" }
  $png = Get-ChildItem $gen -Recurse -Filter *.png | Where-Object { $_.LastWriteTime -gt $t0 } | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if ($png) {
    $n = 1; while (Test-Path (Join-Path $base "$($k.na)_$n.png")) { $n++ }
    $dst = Join-Path $base "$($k.na)_$n.png"
    Copy-Item $png.FullName $dst
    "[$id] できた: $dst"
  } else { "[$id] 絵が見つからない" }
}
"ぜんぶ終わり"
