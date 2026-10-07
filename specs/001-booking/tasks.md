# Feature: จองคิวตรวจสุขภาพ (Booking)
Spec ID: SPEC-BKG-001
อ้างอิง plan.md: specs/001-booking/plan.md
วันที่: 2569-09-23

สรุป 2 บรรทัด:
- ทำทั้งหมด 12 task
- มี 1 task ที่ต้องรอ Open Questions

### T-01 สร้างตาราง bookings, slots และ audit log
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/conftest.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: migration สร้างตาราง PostgreSQL ที่จำเป็นสำหรับ slots, bookings, audit_logs และ test SQLite ในหน่วยความจำทำงานได้
- สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้าง API GET /slots และคำนวณช่วงว่าง
- รองรับ: FR-BKG-01, FR-BKG-06, NFR-PERF-01
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: GET /slots คืนข้อมูลช่วงเวลาว่างพร้อม remaining ตามแพ็กเกจ และผลการทดสอบ p95 สำหรับ 200 request อยู่ภายใน 2 วินาที
- สถานะ: พร้อมทำ

### T-03 สร้าง API POST /bookings พื้นฐานและบันทึกการจอง
- รองรับ: FR-BKG-04, IF-IDP-01
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py, backend/app/main.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: API ยืนยันตัวตนก่อนเข้าถึงข้อมูลผู้รับบริการแล้วสร้าง booking ใหม่, ตัด remaining ลง 1 และส่งกลับหมายเลขคิวพร้อมสถานะสำเร็จ
- สถานะ: พร้อมทำ

### T-04 ป้องกันการจองซ้ำในวันเดียวกัน
- รองรับ: FR-BKG-02, IF-IDP-01
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/tests/test_ac_bkg_02.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: เมื่อมีคิวที่ยังไม่ได้ใช้ในวันเดียวกัน ระบบปฏิเสธการจองใหม่และส่งกลับ booking เดิมพร้อมข้อความแจ้งข้อผิดพลาด
- สถานะ: พร้อมทำ

### T-05 เสนอ 3 ช่วงที่ว่างใกล้เคียงเมื่อช่วงเวลาถูกจองเต็ม
- รองรับ: FR-BKG-03, IF-IDP-01
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: backend/app/slots/service.py, backend/app/booking/service.py, backend/tests/test_ac_bkg_03.py
- ต้องทำหลัง: T-03, T-04
- เสร็จเมื่อ: เมื่อช่วง 09.00 น. เต็ม ระบบตอบกลับ 409 พร้อม 3 ทางเลือกที่ใกล้ที่สุดในวันเดียวกันและวันถัดไป และไม่มีการจองซ้อนเกิดขึ้น
- สถานะ: พร้อมทำ

### T-06 ทำคิวส่งข้อความยืนยันแบบ asynchronous และส่งซ้ำ
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/app/notify/queue.py, backend/app/booking/service.py, backend/tests/test_ac_bkg_04.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: เมื่อการส่งข้อความไม่สำเร็จ การจองยังถูกบันทึก แสดงหมายเลขคิว และมีงานคิวส่งซ้ำที่กำหนดส่งภายใน 5 นาที
- สถานะ: พร้อมทำ

### T-07 บันทึก audit log ทุกครั้งที่เข้าถึงข้อมูลการจอง
- รองรับ: DOM-PDPA-01, IF-IDP-01
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/app/audit/middleware.py, backend/app/main.py, backend/tests/test_ac_bkg_06.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ทุก request ที่เข้าถึงข้อมูลการจองบันทึก actor_id, accessed_at และ hn ลง audit log พร้อมมีข้อมูลครบถ้วนสำหรับการตรวจสอบ
- สถานะ: พร้อมทำ

### T-08 เชื่อมต่อ HN จาก HIS ด้วยเลขบัตรประชาชน
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-08
- ไฟล์ที่แตะ: backend/app/his/client.py, backend/app/patient/router.py (ถ้ามี), backend/tests/test_his_lookup.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ระบบแปลงเลขบัตรประชาชนเป็น HN จาก HIS ได้โดยไม่เก็บเลขบัตรประชาชนในตารางการจอง
- สถานะ: พร้อมทำ

### T-09 กำหนดรูปแบบและออกหมายเลขคิวตามวัน
- รองรับ: FR-BKG-04, Q-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-09
- ไฟล์ที่แตะ: backend/app/booking/service.py, backend/app/db/models.py, backend/tests/test_queue_format.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: ได้รูปแบบหมายเลขคิวที่ทีมตอบคำถาม Q-02 แล้วและระบบสร้างเลขคิวตามกรอบที่ชัดเจนโดยไม่มีการเดา
- สถานะ: รอ Q-02

### T-10 สร้างหน้าเลือกแพ็กเกจและช่วงเวลา (ใช้ API จำลอง)
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-10
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/App.jsx, frontend/src/api/client.js
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: ผู้ใช้เลือกแพ็กเกจและวันที่แล้วเห็นช่วงเวลาว่างพร้อมจำนวนที่นั่งคงเหลือจาก API จำลองตามสัญญาใน plan.md
- สถานะ: พร้อมทำ

### T-11 สร้างหน้ายืนยัน และแสดง "ช่วงเวลาเต็ม" พร้อม 3 ตัวเลือก
- รองรับ: FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/src/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-10
- เสร็จเมื่อ: เมื่อ API จำลองตอบ 409 หน้าแสดงข้อความ "ช่วงเวลาเต็ม" พร้อม 3 ตัวเลือกที่ใกล้ที่สุด และผู้ใช้สามารถยืนยันเลือกทางเลือกใหม่ได้
- สถานะ: พร้อมทำ

### T-12 ต่อหน้าจอกับ API จริงและถอด API จำลองออก
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04
- ตรวจด้วย: AC-BKG-03, AC-BKG-05
- ไฟล์ที่แตะ: frontend/src/api/client.js, frontend/src/pages/SlotPicker.jsx, frontend/src/pages/ConfirmBooking.jsx, frontend/src/pages/BookingResult.jsx
- ต้องทำหลัง: T-02, T-05, T-10, T-11
- เสร็จเมื่อ: หน้าเว็บเรียก API จริงผ่าน /api ได้ทั้งหมด และไม่มี mock ที่ซ่อนความจริงของ backend ในหน้าเว็บ
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ AC
| AC ID | task ที่ตรวจ AC นี้ |
|---|---|
| AC-BKG-01 | T-03 |
| AC-BKG-02 | T-04 |
| AC-BKG-03 | T-05, T-11 |
| AC-BKG-04 | T-06 |
| AC-BKG-05 | T-02 |
| AC-BKG-06 | T-07 |

## ตารางตรวจความครบ Constraint
| Constraint ID | task ที่ทำให้เป็นจริง |
|---|---|
| CON-TECH-01 | T-01 |
| DOM-PDPA-01 | T-01, T-07 |
| IF-IDP-01 | T-03, T-04, T-05, T-07 |
| IF-HIS-01 | T-08 |
| IF-NOT-01 | T-06 |

## สิ่งที่ยังไม่ทำ
- Q-02: หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง และมีรูปแบบอย่างไร (เช่น A001)? -> ถามเจ้าหน้าที่เวชระเบียน (ยังไม่ได้คำตอบ) รอใน T-09
