# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md Draft v2 | tasks.md | test-cases.md
สร้างด้วย /verify เมื่อ 2569-10-07 15:50 | test: ผ่าน 6 ผ่าน / ไม่ผ่าน 1 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | ไม่มี AC | T-02 | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | ไม่มี test เฉพาะ FR นี้ | ช่องโหว่ |
| FR-BKG-02 | AC-BKG-02 | T-04 (พร้อมทำ) | backend/app/booking/service.py: create_booking | ไม่มี test ในโค้ด | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-11, T-12 (พร้อมทำ) | ไม่มีฟังก์ชันที่สร้างช่วงเลือก 3 ตัว หรือตรวจ 409 | ไม่มี test ในโค้ด | ยังไม่ถึง |
| FR-BKG-04 | AC-BKG-01 | T-03, T-06 | backend/app/booking/router.py: create_booking; backend/app/booking/service.py: create_booking, next_queue_no | backend/tests/test_AC_BKG_01.py (3 passed) | ช่องโหว่ |
| FR-BKG-05 | AC-BKG-04 | T-07 (พร้อมทำ) | ไม่มีคิวส่งซ้ำ / queue retry | ไม่มี test ในโค้ด | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02, T-10 | backend/app/slots/router.py: get_slots; backend/app/slots/service.py: list_available_slots | ไม่มี test เฉพาะ FR นี้ | ยังไม่ถึง |
| NFR-PERF-01 | AC-BKG-05 | T-02 | backend/app/slots/service.py: list_available_slots | backend/tests/test_AC_BKG_05.py (passed) | ครบ |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task | ไม่มี TLS/HSTS/HTTPS configuration ใน backend/app | ไม่มี test | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 (พร้อมทำ) | ไม่มี retry queue / schedule ส่งซ้ำ | ไม่มี test ในโค้ด | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task | ไม่มี workflow สำหรับผู้ใช้ใหม่หรือเวลาจอง 3 นาที | ไม่มี test | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 | backend/app/config.py: DATABASE_URL; backend/app/db/session.py: engine | ไม่มี test เฉพาะ constraint แต่ใช้ env PostgreSQL ตาม spec | ครบ |
| DOM-PDPA-01 | AC-BKG-06 | T-08 (พร้อมทำ) | backend/app/db/models.py: AuditLog; ไม่มี middleware หรือ log จริงใน backend/app/main.py | ไม่มี test ในโค้ด | ยังไม่ถึง |
| IF-IDP-01 | AC-BKG-01 (ทางผิด) | T-03 | backend/app/auth/idp.py: get_verified_hn | backend/tests/test_AC_BKG_01.py::test_TC_BKG_01_3_not_verified (passed) | ครบ |
| IF-HIS-01 | ไม่มี AC | T-09 (พร้อมทำ) | ไม่มี HIS client / lookup integration | ไม่มี test ในโค้ด | ยังไม่ถึง |
| IF-NOT-01 | AC-BKG-04 | T-07 (พร้อมทำ) | ไม่มี async notification queue / retry logic | ไม่มี test ในโค้ด | ยังไม่ถึง |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| backend/app/slots/router.py: get_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | ให้แสดงช่วงเวลาเท่านั้น แต่ใช้ DAYS_AHEAD = 14 ไม่ใช่ 30 วันตาม spec |
| backend/app/slots/service.py: list_available_slots | FR-BKG-01, FR-BKG-06 | ไม่ครบ | กรอง `remaining > 0` และระยะเวลา 14 วัน เป็นความคิดที่ไม่ตรง spec |
| backend/app/booking/router.py: create_booking | FR-BKG-04, IF-IDP-01 | ส่วนหนึ่งตรง | ตรวจยืนยันตัวตนแล้วบันทึกได้ แต่ไม่ตรวจช่วงเต็ม = 0 หรือจองซ้ำวันเดียวกัน |
| backend/app/booking/service.py: create_booking | FR-BKG-02, FR-BKG-03, FR-BKG-04 | ไม่ครบ | ไม่มีตรวจการจองซ้ำวันเดียวกัน และ `if slot.remaining < 0` ไม่ใช่ `== 0` จึงให้จองต่อได้แม้เต็ม |
| backend/app/booking/service.py: next_queue_no | FR-BKG-04, Q-02 | ไม่ครบ | ใช้รูปแบบ `A001` และนับต่อวัน โดยไม่มีคำตอบจาก Q-02 |
| backend/app/auth/idp.py: get_verified_hn | IF-IDP-01 | ครบ | ตรวจ token `Bearer verified:<HN>` ก่อนเข้าถึงข้อมูล |
| backend/app/db/models.py: Booking | IF-HIS-01 | ส่วนหนึ่งตรง | เก็บเฉพาะ `hn` และไม่เก็บ national_id แต่มี `BookingRequest.national_id` ใน router เป็น field ที่ไม่ใช้งาน ทำให้สัญญา API ดูคลุมเครือ |

## 3. ข้อค้นพบ
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง
ทีมตัดสิน: แก้โค้ด / แก้ spec / เพิ่ม Q-xx / ไม่ใช่ปัญหา (พร้อมเหตุผล 1 บรรทัด)

| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-001 | ตัวเลขไม่ตรง spec | backend/app/slots/service.py: DAYS_AHEAD = 14 | FR-BKG-01 | spec ระบุภายใน 30 วันข้างหน้า แต่โค้ดแสดงเฉพาะ 14 วัน | แก้โค้ด |
| F-002 | เดา Q-xx | backend/app/booking/service.py: next_queue_no | FR-BKG-04, Q-02 | โค้ดกำหนด `A001` และนับต่อเนื่องทุกวัน แม้ Open Question Q-02 ยังไม่ตอบ | เพิ่ม Q-xx |
| F-003 | โค้ดไม่มี FR / test อ่อน | backend/app/booking/service.py: create_booking | FR-BKG-02, FR-BKG-03 | `if slot.remaining < 0` ไม่ตรวจ `== 0` จึงอนุญาตให้จองแม้ช่วงเวลาว่างเป็น 0 ที่ และไม่มี 3 ตัวเลือกเมื่อเต็ม | แก้โค้ด |
| F-004 | AC ไม่มี test / test อ่อน | backend/tests/test_AC_BKG_01.py | AC-BKG-01 | test ตรวจ 201/remaining อย่างเดียว แต่ไม่ตรวจ queue_no, ไม่ตรวจข้อความแจ้ง / 3 ตัวเลือก ที่เป็นส่วนย่อยของ Then ของ AC | แก้ spec / เพิ่ม test |

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
| - | - | ไม่มีข้อค้นพบเดิมที่แก้แล้วในรอบนี้ |
