"""ジッグラト — 敵メック・コンセプトアート（正面図）
LEGO由来: 砂色の階段状装甲 + ライラック紫の帯 + グレーの傾斜コックピット + 肩のミサイルポッド"""
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import math

JP = "/usr/share/fonts/truetype/fonts-japanese-gothic.ttf"
f_big = ImageFont.truetype(JP, 26)
f_mid = ImageFont.truetype(JP, 22)
f_sm  = ImageFont.truetype(JP, 18)

W, H = 1000, 1000
img = Image.new("RGB", (W, H), (18, 22, 28))
d = ImageDraw.Draw(img, "RGBA")

# --- 背景: 戦場グリッド + ビネット ---
for gx in range(0, W, 50):
    d.line([(gx, 0), (gx, H)], fill=(40, 50, 60, 60), width=1)
for gy in range(0, H, 50):
    d.line([(0, gy), (W, gy)], fill=(40, 50, 60, 60), width=1)
# 地面のグロー
d.ellipse([180, 760, 820, 920], fill=(90, 70, 120, 70))

# パレット（LEGOカラー）
TAN   = (216, 196, 154)
TAN_D = (180, 160, 120)   # 影
TAN_L = (236, 220, 184)   # ハイライト
LILAC = (184, 156, 200)
LILAC_D = (150, 120, 168)
STEEL = (154, 161, 168)
STEEL_D = (110, 118, 126)
DARK  = (40, 46, 52)
TUBE  = (58, 68, 80)
WARN  = (255, 90, 58)
EYE   = (120, 200, 255)

cx = W // 2

def block(x0, y0, x1, y1, base, top=None, side=None, edge=(20,24,28)):
    """簡易アイソメ風: 天面ハイライト + 側面シャドウ"""
    top = top or tuple(min(255, c+24) for c in base)
    side = side or tuple(max(0, c-34) for c in base)
    th = 10  # 天面の厚み
    sd = 10  # 側面の厚み
    # 側面（右）
    d.polygon([(x1, y0), (x1+sd, y0-th), (x1+sd, y1-th), (x1, y1)], fill=side)
    # 天面
    d.polygon([(x0, y0), (x0+sd, y0-th), (x1+sd, y0-th), (x1, y0)], fill=top)
    # 正面
    d.rectangle([x0, y0, x1, y1], fill=base, outline=edge, width=2)

def studs(x0, x1, y, base):
    """LEGOのポッチ"""
    n = max(1, int((x1 - x0) // 30))
    light = tuple(min(255, c+30) for c in base)
    shade = tuple(max(0, c-30) for c in base)
    for i in range(n):
        sx = x0 + 15 + i * ((x1 - x0 - 10) / max(1, n))
        d.ellipse([sx-9, y-16, sx+9, y-4], fill=light, outline=shade, width=1)

# === 脚（ずんぐり） ===
for s in (-1, 1):
    lx = cx + s*95
    block(lx-46, 720, lx+46, 820, TAN, side=TAN_D)      # 太もも
    block(lx-52, 815, lx+52, 855, STEEL, side=STEEL_D)  # 足首
    block(lx-62, 850, lx+62, 895, DARK)                 # 足

# === 肩のミサイルポッド ×2（ご要望: 肩にミサイル搭載） ===
for s in (-1, 1):
    px = cx + s*250
    block(px-70, 440, px+70, 580, STEEL, side=STEEL_D)  # ポッド筐体
    # 2x2 + 中央 のミサイル発射筒
    for ox in (-38, 0, 38):
        for oy in (-30, 30):
            tx, ty = px+ox, 510+oy
            d.ellipse([tx-20, ty-20, tx+20, ty+20], fill=TUBE, outline=(20,24,28), width=3)
            d.ellipse([tx-9, ty-9, tx+9, ty+9], fill=WARN, outline=(120,30,20), width=2)  # 弾頭
    # ロックオン警告灯
    d.ellipse([px-12, 410, px+12, 434], fill=WARN)
    d.ellipse([px-6, 416, px+6, 428], fill=(255, 200, 170))

# === 胴体: 階段状(ジッグラト)の砂色装甲 ===
# 紫の基部帯
block(cx-180, 690, cx+180, 740, LILAC, side=LILAC_D)
studs(cx-180, cx+180, 690, LILAC)
# 第1段（最も広い）
block(cx-160, 600, cx+160, 700, TAN, side=TAN_D)
# 中段の紫アクセント帯
block(cx-150, 575, cx+150, 605, LILAC, side=LILAC_D)
# 第2段
block(cx-125, 490, cx+125, 580, TAN, side=TAN_D)
studs(cx-125, cx+125, 490, TAN)
# 第3段（最上段）
block(cx-92, 410, cx+92, 495, TAN, side=TAN_D)

# === グレーの傾斜コックピット（LEGOのダークグレー6x6プレート相当） ===
d.polygon([(cx-86, 470), (cx+86, 470), (cx+70, 405), (cx-70, 405)], fill=STEEL, outline=(20,24,28))
d.polygon([(cx-70, 405), (cx+70, 405), (cx+62, 392), (cx-62, 392)], fill=STEEL_D)  # 天面
# 発光バイザー（アイ）
for gx in range(cx-58, cx+58, 4):
    d.line([(gx, 446), (gx, 462)], fill=EYE, width=3)
glow = Image.new("RGB", (W, H), (0,0,0))
gd = ImageDraw.Draw(glow)
gd.rectangle([cx-60, 444, cx+60, 464], fill=(60,140,220))
glow = glow.filter(ImageFilter.GaussianBlur(14))
img = Image.blend(img, Image.new("RGB",(W,H),(0,0,0)), 0)
img = Image.composite(Image.new("RGB",(W,H),(160,210,255)), img, glow.convert("L").point(lambda v: min(255,v*2)))
d = ImageDraw.Draw(img, "RGBA")

# === キャプション ===
d.rectangle([0, 0, W, 80], fill=(0, 0, 0, 150))
d.text((28, 12), "STEEL DIVISION  //  ENEMY UNIT", fill=(180, 200, 220), font=f_sm)
d.text((28, 38), "ZIGGURAT級 重装ミサイルメック 「ジッグラト」", fill=(230, 215, 180), font=f_mid)
d.text((W-250, 928), "肩部ミサイルポッド ×2", fill=(255, 140, 110), font=f_sm)

img.save("/home/user/mech/concept_ziggurat.png")
print("saved")
