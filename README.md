# read_email_python

โปรเจกต์นี้เป็นตัวอย่างสคริปต์ภาษา Python สำหรับการอ่านอีเมลจากเซิร์ฟเวอร์ (เช่น Gmail, Outlook) ด้วยการใช้โปรโตคอล IMAP โดยเน้นการดึงข้อมูลอีเมลและแสดงผลลัพธ์ในรูปแบบที่อ่านง่าย เหมาะสำหรับผู้ที่ต้องการเรียนรู้การใช้งาน Python ในการจัดการอีเมลอัตโนมัติ

## คุณสมบัติ

- เชื่อมต่อกับเซิร์ฟเวอร์อีเมลผ่าน IMAP
- ดึงอีเมลจากโฟลเดอร์ที่ต้องการ เช่น Inbox
- อ่านหัวข้อ, ผู้ส่ง, วันที่ และเนื้อหาของอีเมล
- รองรับหลายภาษา (Unicode)
- สามารถต่อยอดเพื่อค้นหา/กรองอีเมล หรือดาวน์โหลดไฟล์แนบได้

## การติดตั้ง

1. clone โปรเจกต์นี้
   ```bash
   git clone https://github.com/pathompongn/read_email_python.git
   cd read_email_python
   ```
2. ติดตั้งไลบรารีที่จำเป็น
   ```bash
   pip install -r requirements.txt
   ```
   หรือถ้าไม่มีไฟล์ requirements.txt ให้ติดตั้งไลบรารีหลักๆ เช่น
   ```bash
   pip install imapclient pyzmail36
   ```

## วิธีใช้งาน

1. แก้ไขไฟล์ `config.py` หรือแก้ไขตัวแปรในสคริปต์หลักให้ตรงกับอีเมลของคุณ
2. รันไฟล์หลัก
   ```bash
   python read_email.py
   ```
3. ผลลัพธ์จะแสดงข้อมูลอีเมลบนหน้าจอ

## หมายเหตุด้านความปลอดภัย

- แนะนำให้ใช้รหัสผ่านแอปพลิเคชัน (App Password) แทนรหัสผ่านหลักของบัญชีอีเมล
- ระวังอย่าแชร์ข้อมูลความลับ (เช่น user, password) ลงในโค้ดหรือ repository

## ตัวอย่างโค้ดเบื้องต้น

```python
import imapclient
import pyzmail36

IMAP_SERVER = 'imap.gmail.com'
EMAIL_ACCOUNT = 'your_email@gmail.com'
PASSWORD = 'your_app_password'

with imapclient.IMAPClient(IMAP_SERVER) as client:
    client.login(EMAIL_ACCOUNT, PASSWORD)
    client.select_folder('INBOX', readonly=True)
    messages = client.search(['UNSEEN'])
    for uid in messages:
        raw_message = client.fetch([uid], ['BODY[]', 'FLAGS'])
        message = pyzmail36.PyzMessage.factory(raw_message[uid][b'BODY[]'])
        print('From:', message.get_addresses('from'))
        print('Subject:', message.get_subject())
        print('Text:', message.text_part.get_payload().decode(message.text_part.charset))
```

## License

This project is licensed under the MIT License.
