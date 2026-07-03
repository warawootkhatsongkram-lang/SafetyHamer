#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สร้าง QR Code 9 อัน ชี้ไปยังไฟล์ PDF (SDS) ที่โฮสต์บน GitHub Pages
- ป้ายกำกับใต้ QR = ชื่อสารเคมี (รองรับไทยด้วยฟอนต์ Tahoma)
- error correction ระดับ H เพื่อความทนทานเวลาพิมพ์

ใช้งาน:
    py generate_qr.py <BASE_URL>
ตัวอย่าง:
    py generate_qr.py https://myuser.github.io/qr-sds
ถ้าไม่ใส่ ใช้ค่าจาก env QR_BASE_URL หรือ placeholder (สำหรับทดสอบ)
"""
import os
import sys
from urllib.parse import quote

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "docs", "qr")
FONT_PATH = r"C:\Windows\Fonts\tahoma.ttf"       # ฟอนต์รองรับไทย
FONT_BOLD_PATH = r"C:\Windows\Fonts\tahomabd.ttf"

# (รหัสเอกสาร, ชื่อสารเคมีสำหรับป้าย, ชื่อไฟล์ PDF ใน docs/pdf/)
ITEMS = [
    ("EX-SF-02", "KEROSENE (น้ำมันก๊าด)", "EX-SF-02-KEROSENE.pdf"),
    ("EX-SF-03", "PN331 PHOSPHATE",        "EX-SF-03-PN331-PHOSPHATE.pdf"),
    ("EX-SF-04", "PF18 PHOSPHATE",         "EX-SF-04-PF18-PHOSPHATE.pdf"),
    ("EX-SF-05", "PK33 PHOSPHATE",         "EX-SF-05-PK33-PHOSPHATE.pdf"),
    ("EX-SF-06", "PD10 PHOSPHATE",         "EX-SF-06-PD10-PHOSPHATE.pdf"),
    ("EX-SF-07", "AC55 PHOSPHATE",         "EX-SF-07-AC55-PHOSPHATE.pdf"),
    ("EX-SF-08", "RTL2000 EDP",            "EX-SF-08-RTL2000-EDP.pdf"),
    ("EX-SF-09", "RTL2001 EDP",            "EX-SF-09-RTL2001-EDP.pdf"),
    ("EX-SF-10", "RTL2002 EDP",            "EX-SF-10-RTL2002-EDP.pdf"),
]

PLACEHOLDER = "https://USERNAME.github.io/REPO"


def load_font(path, size, fallback_size=None):
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def text_w(draw, text, font):
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0]


def build_label_qr(url, code, name):
    """สร้างภาพ QR + ป้ายชื่อสารเคมีด้านล่าง คืนค่า PIL.Image"""
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_H, box_size=10, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    W = qr_img.width
    pad = 24
    code_font = load_font(FONT_BOLD_PATH, 30)
    name_font = load_font(FONT_PATH, 26)

    # พื้นที่ข้อความ 2 บรรทัด
    line_h_code = 40
    line_h_name = 36
    label_h = pad + line_h_code + line_h_name + pad

    canvas = Image.new("RGB", (W, qr_img.height + label_h), "white")
    canvas.paste(qr_img, (0, 0))
    draw = ImageDraw.Draw(canvas)

    y = qr_img.height + pad
    # บรรทัด 1: รหัสเอกสาร (ตัวหนา)
    draw.text(((W - text_w(draw, code, code_font)) // 2, y), code,
              font=code_font, fill="black")
    y += line_h_code
    # บรรทัด 2: ชื่อสารเคมี — ย่อฟอนต์ถ้ากว้างเกิน
    nf = name_font
    if text_w(draw, name, nf) > W - 2 * pad:
        nf = load_font(FONT_PATH, 20)
    draw.text(((W - text_w(draw, name, nf)) // 2, y), name,
              font=nf, fill=(40, 40, 40))
    return canvas


def main():
    base = (sys.argv[1] if len(sys.argv) > 1
            else os.environ.get("QR_BASE_URL", PLACEHOLDER)).rstrip("/")
    is_placeholder = base == PLACEHOLDER
    os.makedirs(OUT_DIR, exist_ok=True)

    print(f"BASE_URL = {base}")
    if is_placeholder:
        print("  [!] ยังเป็น PLACEHOLDER — QR นี้ใช้ทดสอบเท่านั้น ยังสแกนใช้จริงไม่ได้")

    for code, name, pdf in ITEMS:
        url = f"{base}/pdf/{quote(pdf)}"
        img = build_label_qr(url, code, name)
        out = os.path.join(OUT_DIR, f"{code}.png")
        img.save(out)
        print(f"  OK {code:9s} -> {url}")

    print(f"\nสร้างเสร็จ {len(ITEMS)} ไฟล์ ที่ {OUT_DIR}")


if __name__ == "__main__":
    main()
