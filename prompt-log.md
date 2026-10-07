# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 13.45 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง (draft)
- AC: AC-BKG-01
- สถานะตาราง: ยังไม่มีแถวสถานะ "ใช้ได้" ใน [specs/001-booking/test-cases.md](specs/001-booking/test-cases.md)
- ผล: เพิ่มแถวร่าง 3 แถวสำหรับ AC-BKG-01 ตามหลักทางปกติ / ขอบ / ทางผิด โดยแยก Then เป็น "บันทึกสำเร็จ", "แสดงหมายเลขคิว (รอ Q-02)", และ "ที่นั่งว่างเป็น 0"
- ข้อคำถาม: Q-02 ยังไม่ตอบ จึงยังไม่ได้กำหนดรูปแบบหมายเลขคิว และข้อความแจ้งตอนปฏิเสธการจองสำหรับเงื่อนไขทางผิดยังไม่ได้ระบุใน spec
- สรุป: หยุดก่อนเขียนโค้ด test ต้องให้ทีมตรวจแถวในตาราง และเปลี่ยนสถานะเป็น "ใช้ได้" ก่อน แล้วสั่ง /testcases อีกครั้ง

---

## 2569-10-07 15.20 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: เขียน test
- AC: AC-BKG-01
- ตาราง: [specs/001-booking/test-cases.md](specs/001-booking/test-cases.md) มีแถว 3 แถวสถานะ "ใช้ได้"
- ไฟล์ที่แก้: [backend/tests/test_AC_BKG_01.py](backend/tests/test_AC_BKG_01.py), [frontend/src/__tests__/TC-BKG-01-1.test.jsx](frontend/src/__tests__/TC-BKG-01-1.test.jsx)
- ผลทดสอบ: backend 3 passed; frontend 1 failed
- รายละเอียด backend: 3 tests ผ่าน โดยตรวจว่า POST /bookings คืน 201, ตาราง bookings มี 1 รายการ, และ slot.remaining = 0 สำหรับกรณีสำเร็จ หรือ 401 สำหรับกรณีไม่ได้ยืนยันตัวตน
- รายละเอียด frontend: หน้าจอไม่แสดงข้อความ "การจองสำเร็จ" จึงไม่ผ่าน เนื่องจาก task ที่ตรวจ AC นี้ยังไม่สร้างหน้าจอแสดงผลจริง (T-06 รอ Q-02) และไม่ใช่ข้อผิดพลาดของ test
- สรุป: ระบบหลังบ้านตรงกับ AC-BKG-01 ส่วน UI ยังติดงานที่ยังไม่ได้สร้าง

---

## 2569-10-07 15:50 คำสั่ง: /verify specs/001-booking/

- โหมด: ตรวจความครบของ requirement
- ผล test: backend 6 passed, frontend 1 failed / 1 passed
- จำนวนแถวตามสถานะ: ครบ 3, ยังไม่ถึง 10, รอ Q-xx 0, ช่องโหว่ 2
- ข้อค้นพบใหม่: F-001 (ตัวเลขไม่ตรง spec: 14 วันแทน 30 วัน), F-002 (เดา Q-xx: รูปแบบคิว A001), F-003 (ช่องโหว่: booking เมื่อ remaining == 0), F-004 (AC-BKG-01 มี test อ่อน: ไม่ตรวจ queue_no และ 3 ตัวเลือก)
- ไฟล์ที่สร้าง: [specs/001-booking/rtm.md](specs/001-booking/rtm.md)
- สรุป: โค้ดและ test ของระบบมีความครอบคลุมบางส่วน แต่ยังมีข้อค้นพบที่ต้องให้ทีมตัดสินก่อนยืนยันว่า feature ครบตาม spec
