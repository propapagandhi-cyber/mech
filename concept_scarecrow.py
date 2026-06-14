"""スケアクロウ — 敵メック・コンセプトアート（正面図）
LEGOの形状を踏襲（色は独自）:
箱型胴体＋胸部ビューポート / 左右に長く張り出した細腕＋先端の砲 /
上部前方の太い砲 / 背面の高い格子マスト（クレーン状）/ 柱状の脚"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont

JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
f_mid = ImageFont.truetype(JP, 22)
f_sm  = ImageFont.truetype(JP, 18)

W, H = 1000, 1000
img = Image.new("RGB", (W, H), (18, 22, 28))
d = ImageDraw.Draw(img, "RGBA")

# 背景グリッド＋地面グロー
for gx in range(0, W, 50):
    d.line([(gx, 0), (gx, H)], fill=(40, 50, 60, 60), width=1)
for gy in range(0, H, 50):
    d.line([(0, gy), (W, gy)], fill=(40, 50, 60, 60), width=1)
d.ellipse([220, 820, 780, 940], fill=(70, 90, 120, 70))

# パレット（独自色: スチール基調）
STEEL = (138, 147, 160)
STEEL_D = (96, 104, 116)
STEEL_L = (174, 182, 194)
DARK  = (40, 46, 52)
GUN   = (58, 66, 76)
WARN  = (255, 90, 58)
BEAC  = (255, 60, 47)
EYE   = (120, 200, 255)
cx = W // 2

def block(x0, y0, x1, y1, base, side=None, top=None, edge=(20,24,28), sd=10, th=10):
    side = side or tuple(max(0, c-34) for c in base)
    top  = top  or tuple(min(255, c+22) for c in base)
    d.polygon([(x1, y0), (x1+sd, y0-th), (x1+sd, y1-th), (x1, y1)], fill=side)
    d.polygon([(x0, y0), (x0+sd, y0-th), (x1+sd, y0-th), (x1, y0)], fill=top)
    d.rectangle([x0, y0, x1, y1], fill=base, outline=edge, width=2)

# === 背面の高い格子マスト（クレーン状トラス）— 胴体の後ろ ===
mx = cx + 6
d.line([(mx-16, 470), (mx-16, 120)], fill=STEEL_D, width=8)
d.line([(mx+16, 470), (mx+16, 120)], fill=STEEL_D, width=8)
for y in range(140, 470, 34):                      # 斜材(トラス)
    d.line([(mx-16, y), (mx+16, y-17)], fill=(150,158,168), width=4)
    d.line([(mx+16, y), (mx-16, y-17)], fill=(150,158,168), width=4)
    d.line([(mx-16, y), (mx+16, y)], fill=(120,128,138), width=3)
block(mx-22, 108, mx+22, 132, STEEL)               # マスト頂部
d.ellipse([mx-9, 92, mx+9, 110], fill=BEAC, outline=(120,30,20), width=2)  # 頂部標識灯
d.ellipse([mx-5, 96, mx+5, 106], fill=(255, 190, 170))

# === 脚（真っ直ぐな柱状） ===
for s in (-1, 1):
    lx = cx + s*78
    block(lx-26, 700, lx+26, 850, STEEL, side=STEEL_D)   # 柱状の脚
    for yy in range(720, 850, 26):                       # ブロック段の境目
        d.line([(lx-26, yy), (lx+26, yy)], fill=(60,66,74), width=2)
    block(lx-30, 845, lx+30, 880, STEEL_L)               # 足首
    block(lx-38, 875, lx+38, 915, DARK)                  # 足

# === 左右に長く張り出した細腕 ×2（最大の特徴） ===
ay = 470
for s in (-1, 1):
    sxj = cx + s*120
    block(sxj-22, ay-22, sxj+22, ay+22, STEEL_D)         # 肩関節
    inner = cx + s*55
    outer = cx + s*430
    d.polygon([(inner, ay-14), (outer, ay-14), (outer, ay+14), (inner, ay+14)],
              fill=STEEL, outline=(20,24,28))            # 細い腕ビーム
    d.polygon([(inner, ay-14), (outer, ay-14), (outer-8, ay-22), (inner-8, ay-22)],
              fill=STEEL_L)                              # 上面ハイライト
    # 先端の砲身
    tipx = cx + s*470
    d.rectangle([min(tipx, outer), ay-9, max(tipx, outer), ay+9], fill=GUN, outline=(20,24,28), width=2)
    d.ellipse([tipx-12, ay-12, tipx+12, ay+12], fill=WARN, outline=(120,30,20), width=2)
    d.ellipse([tipx-6, ay-6, tipx+6, ay+6], fill=(255,200,170))

# === 上部前方の太い砲（円筒キャノン）＋小型センサー ===
d.rectangle([cx-48, 388, cx+48, 452], fill=GUN, outline=(20,24,28), width=2)   # 砲身基部
d.ellipse([cx-48, 388, cx+10, 452], fill=STEEL_D, outline=(20,24,28), width=2) # 円筒の丸み(左)
d.ellipse([cx+34, 392, cx+62, 448], fill=DARK, outline=(20,24,28), width=2)    # 砲口
d.polygon([(cx-60, 392), (cx-30, 360), (cx-18, 372), (cx-48, 404)], fill=DARK) # 上面アングルセンサー

# === 箱型の胴体＋胸部ビューポート ===
block(cx-78, 470, cx+78, 700, STEEL, side=STEEL_D)
d.rectangle([cx-72, 478, cx+72, 492], fill=STEEL_D)         # 上部リブ
# 胸部の凹んだビューポート＋発光バイザー
d.rectangle([cx-50, 540, cx+50, 610], fill=DARK, outline=(20,24,28), width=3)
for gx in range(cx-44, cx+44, 5):
    d.line([(gx, 560), (gx, 592)], fill=EYE, width=3)

# 発光ブルーム（バイザー）
glow = Image.new("RGB", (W, H), (0,0,0))
gd = ImageDraw.Draw(glow)
gd.rectangle([cx-46, 558, cx+46, 594], fill=(60,140,220))
glow = glow.filter(ImageFilter.GaussianBlur(16))
img = Image.composite(Image.new("RGB",(W,H),(150,205,255)), img,
                      glow.convert("L").point(lambda v: min(255, v*2)))
d = ImageDraw.Draw(img, "RGBA")

# === キャプション ===
d.rectangle([0, 0, W, 80], fill=(0, 0, 0, 150))
d.text((28, 12), "STEEL DIVISION  //  ENEMY UNIT", fill=(180, 200, 220), font=f_sm)
d.text((28, 38), "SCARECROW級 長距離火力支援機 「スケアクロウ」", fill=(210, 220, 230), font=f_mid)
d.text((28, 930), "張り出した両腕の砲 ＋ 背面の高い格子マスト（射程特化）", fill=(255, 140, 110), font=f_sm)

img.save("/home/user/mech/concept_scarecrow.png")
print("saved")
