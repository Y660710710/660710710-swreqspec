# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ต้องลบของเก่า

---

## 2569-09-16 10:00 คำสั่ง: /clarify specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces
- ไฟล์: specs/001-booking/spec.md (v1 → v2)

### คำถามที่ AI ถาม (ทั้งหมด)

1. Q1: "ช่วงเวลาใกล้เคียง" คำนวณอย่างไร — รวมวันถัดไปหรือเฉพาะวันเดียวกัน และเรียงตามเกณฑ์ใด
2. Q2: นโยบายการส่งข้อความยืนยันเมื่อล้มเหลวเป็นอย่างไร — จำนวนครั้ง, ระยะเวลาระหว่าง retry, backoff และการถือว่าสถานะ "ล้มเหลวถาวร" หรือไม่
3. Q3: กรณีหมายเลขบัตรประชาชนแมตช์กับหลาย HN ใน HIS ให้ทำอย่างไร และถ้า HIS ไม่ตอบต้อง fallback แบบไหน
4. Q4: หมายเลขคิวรีเซ็ตรายวันหรือนับต่อเนื่อง (Q-02) — ต้องรีเซ็ตทุกวันหรือไม่ และเวลารีเซ็ตคือเมื่อใด
5. Q5: นิยามของ "ผู้ใช้ใหม่" และขอบเขตการทดสอบ NFR-USE-01 คืออะไร
6. Q6: ข้อความใน Goal "ยืนยันภายใน 3 นาที" นับจากจุดเริ่มต้นไหนถึงไหน
7. Q7: เมื่อลูกค้าเปลี่ยนแพ็กเกจระหว่างเลือกเวลา (FR-BKG-06) ควรทำอย่างไรกับที่นั่งที่สำรองไว้
8. Q8: เงื่อนไขการทดสอบ performance p95 ระบุ endpoint, dataset ขนาด, และ environment หรือไม่

### คำตอบของทีมและเหตุผล

1. Q2: ตอบว่า "ทุก 10 นาที" (ระยะห่างการส่งซ้ำของข้อความยืนยัน)

### สิ่งที่แก้ใน spec.md (v1 → v2)

- เปลี่ยน `Status` เป็น `Draft v2` และอัปเดตวันที่เป็น `2569-09-16`
- เพิ่ม `ASM-03` ในหัวข้อ Assumptions: "กรณีส่งข้อความยืนยันไม่สำเร็จ ระบบจะพยายามส่งซ้ำทุก 10 นาที"

---

## 2026-09-16 10:12 คำสั่ง: /plan

- เครื่องมือ: GitHub Copilot (Codespaces)
- ไฟล์ต้นทาง: specs/001-booking/spec.md (Status: Draft v1)
- ผลลัพธ์: สร้าง `specs/001-booking/plan.md` (Draft v1) ร่างตามแม่แบบ plan.prompt.md
- หมายเหตุ: spec ยังเป็น Draft v1 — ทีมควรยืนยันสถานะหรือให้คำตอบ Open Questions ก่อน implement

---

## 2026-09-23 00:00 คำสั่ง: /tasks

- เครื่องมือ: GitHub Copilot
- ไฟล์ต้นทาง: specs/001-booking/spec.md และ specs/001-booking/plan.md
- ผลลัพธ์: สร้าง [specs/001-booking/tasks.md](specs/001-booking/tasks.md) โดยแยกงานย่อย 12 task พร้อมตารางตรวจ AC/Constraint และรายการ Open Questions ที่ยังรอ Q-02
- หมายเหตุ: spec อยู่ในสถานะ Draft v2 จึงไม่หยุดตามเงื่อนไข /tasks และรอคำตอบ Q-02 ใน T-09 เท่านั้น

---

## 2026-09-23 00:05 คำสั่ง: /implement T-01

- เครื่องมือ: GitHub Copilot
- ไฟล์ที่สร้าง/แก้: [backend/app/db/models.py](backend/app/db/models.py), [backend/app/db/session.py](backend/app/db/session.py), [backend/app/db/migrations/001_init.py](backend/app/db/migrations/001_init.py), [backend/app/db/migrations/__init__.py](backend/app/db/migrations/__init__.py), [backend/app/__init__.py](backend/app/__init__.py), [backend/app/db/__init__.py](backend/app/db/__init__.py), [backend/tests/conftest.py](backend/tests/conftest.py), [backend/tests/test_T_01_db_setup.py](backend/tests/test_T_01_db_setup.py)
- ผลทดสอบ: รัน `cd backend && pytest tests/test_T_01_db_setup.py -q` ผลลัพธ์ `1 passed in 0.01s`
- สิ่งที่เกือบต้องเดาแต่ไม่เดา: ไม่มี ข้อมูลเพียงพอสำหรับ T-01 ชัดเจนจาก spec/plan และได้ใช้ schema ตามที่ระบุโดยตรง ไม่มีการสมมติฐานเพิ่มเติม

---
