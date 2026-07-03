# QR Code SDS — เอกสารความปลอดภัยสารเคมี

เว็บ + QR Code สำหรับเปิดไฟล์ PDF (SDS) 9 รายการ โฮสต์บน **GitHub Pages**

## โครงสร้าง
```
docs/            ← GitHub Pages เสิร์ฟจากโฟลเดอร์นี้
  index.html     ← หน้ารวมรายการ 9 เอกสาร
  pdf/           ← ไฟล์ PDF (ชื่อ ASCII)
  qr/            ← รูป QR 9 ไฟล์ (พิมพ์ได้ / โชว์บนเว็บ)
generate_qr.py   ← สคริปต์สร้าง QR (พารามิเตอร์ BASE_URL)
```

## วิธีสร้าง QR ใหม่ (ถ้า URL เปลี่ยน)
```bash
py generate_qr.py https://<username>.github.io/<repo>
```
> ใช้ `py` (ไม่ใช่ `python`) บนเครื่องนี้ เพราะ `python` เป็น Store stub
> ต้องมี: `py -m pip install "qrcode[pil]"`

## วิธี deploy (GitHub Pages)
1. สร้าง repo ใหม่บน GitHub (เช่นชื่อ `<repo>`)
2. ในโฟลเดอร์ `qr-site/`:
   ```bash
   git init && git add . && git commit -m "QR SDS site"
   git branch -M main
   git remote add origin https://github.com/<username>/<repo>.git
   git push -u origin main
   ```
3. GitHub → repo → **Settings → Pages** → Source = `Deploy from a branch`,
   Branch = `main`, Folder = `/docs` → Save
4. รอ ~1 นาที เว็บจะขึ้นที่ `https://<username>.github.io/<repo>/`
5. ตรวจว่าเปิด `https://<username>.github.io/<repo>/pdf/EX-SF-02-KEROSENE.pdf` ได้
6. ถ้า URL จริงต่างจากที่ใส่ตอน gen QR → รัน `generate_qr.py` ใหม่ แล้ว commit/push อีกครั้ง

## ตรวจสอบ QR (decode)
QR ทั้ง 9 ถูก decode ยืนยันแล้วว่าตรงกับ URL ไฟล์ PDF (ดู `generate_qr.py`)
