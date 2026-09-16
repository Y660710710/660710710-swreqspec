# Plan: จองคิวตรวจสุขภาพ (Booking)

1. สรุปแนวทาง
   ฟีเจอร์นี้ให้ผู้รับบริการที่ยืนยันตัวตนแล้วเลือกแพ็กเกจ วัน และช่วงเวลาตรวจสุขภาพ แล้วได้รับหมายเลขคิว ระบบจะตรวจสอบว่าผู้รับบริการไม่มีคิวซ้ำในวันเดียวกัน, บันทึกการจองเป็นทรานแซคชัน, ลดจำนวนที่นั่ง และส่งคำขอแจ้งเตือนแบบ asynchronous (มี retry ตาม ASM-03).
   ทีมพัฒนาใช้สถาปัตยกรรมเว็บแอปแบบ client-server: frontend แสดง availability และฟอร์มจอง, backend เป็น API ที่จัดการธุรกิจหลักและ worker สำหรับส่งข้อความซ้ำ

2. เทคโนโลยีที่ใช้

| สิ่งที่เลือก | มาจาก | หมายเหตุ |
|---|---|---|
| Database: MySQL | CON-TECH-01 | ตาม Constraint ของโรงพยาบาล |
| Backend: Python + FastAPI | ทีมเลือกเอง ไม่ได้มาจาก spec | เหมาะสำหรับ API และ worker |
| Frontend: React (Vite) | ทีมเลือกเอง ไม่ได้มาจาก spec | SPA แสดง availability และ flow การจอง |
| Worker: Celery / RQ / Background task | ทีมเลือกเอง ไม่ได้มาจาก spec | สำหรับ retry queue และ background jobs |
| Transport security: TLS 1.2+ | NFR-SEC-01 (Quality Requirement) | ต้องใช้ TLS ในการสื่อสารทั้งหมด |

3. โมเดลข้อมูล (entities) — ฟิลด์สำคัญและ FR ที่รองรับ

- `time_slots` — (id, date, start_time, end_time, capacity, remaining, version)
  - รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04

- `bookings` — (id, hn, user_id, time_slot_id, package_id, status, queue_number, created_at)
  - หมายเหตุ: ห้ามเก็บ `national_id` ตาม IF-HIS-01
  - รองรับ: FR-BKG-02, FR-BKG-04, FR-BKG-05, FR-BKG-06

- `booking_retry_queue` — (id, booking_id, payload, next_retry_at, attempts, last_error)
  - รองรับ: FR-BKG-05, NFR-REL-02, AC-BKG-04

- `audit_logs` — (id, actor, action, target_type, target_id, timestamp)
  - รองรับ: DOM-PDPA-01, AC-BKG-06

4. API / หน้าจอ (method path — input/output สำคัญ — FR ที่รองรับ)

- `GET /availability?start={date}&days=30&package={id}`
  - Input: date range, package_id
  - Output: list of time_slots (with remaining)
  - รองรับ: FR-BKG-01, FR-BKG-06, AC-BKG-05

- `POST /bookings`
  - Input: user_id (จาก IDP), hn (จาก HIS match), time_slot_id, package_id
  - Output: booking id, queue_number หรือ error "already_has_booking" / "slot_full" พร้อม 3 ช่วงเวลาใกล้เคียง
  - รองรับ: FR-BKG-02, FR-BKG-03, FR-BKG-04, FR-BKG-06, AC-BKG-01..AC-BKG-04

- `GET /bookings/{id}`
  - Input: booking id
  - Output: booking details (queue_number, status, time_slot)
  - รองรับ: FR-BKG-04, AC-BKG-01

- หน้าจอหลัก (frontend)
  - หน้าเลือกแพ็กเกจและวันที่ → เรียก `GET /availability` (รองรับ FR-BKG-01, FR-BKG-06)
  - หน้าแสดงสรุปการจองและหมายเลขคิว (รองรับ FR-BKG-04, FR-BKG-05)

5. ตารางตรวจ Constraints

| Constraint ID | ถูกนำไปใช้ที่ไหนใน plan | สถานะ |
|---|---|---|
| CON-TECH-01 | Database: MySQL — schema และ migrations | ใช้แล้ว |
| DOM-PDPA-01 | `audit_logs` เก็บการเข้าถึงข้อมูลการจอง (actor, timestamp, target) | ใช้แล้ว |
| IF-IDP-01 | Authentication precondition — API รับ token/identity จาก IDP ก่อนเรียก `POST /bookings` | ใช้แล้ว |
| IF-HIS-01 | เมื่อรับ hn จาก HIS ใช้ HN เป็นตัวอ้างอิง และไม่เก็บเลขบัตรประชาชนใน `bookings` | ใช้แล้ว |
| IF-NOT-01 | Notification ส่งแบบ asynchronous — push เข้า `booking_retry_queue` และ worker ส่งข้อความ | ใช้แล้ว |

6. แผนทดสอบจาก Acceptance Criteria

| AC ID | ชื่อ test | ทดสอบอย่างไร |
|---|---|---|
| AC-BKG-01 | test_AC_BKG_01_record_booking_and_decrement | Mock time_slot remaining =1, call `POST /bookings`, assert booking created, queue_number returned, time_slot.remaining == 0 |
| AC-BKG-02 | test_AC_BKG_02_reject_if_existing_same_day | Create existing booking for user on same date, call `POST /bookings`, expect 409 with existing queue_number |
| AC-BKG-03 | test_AC_BKG_03_slot_full_offers_alternatives | Simulate concurrent confirm that consumes last slot, call `POST /bookings`, expect error "slot_full" and 3 alternatives, and no duplicate booking |
| AC-BKG-04 | test_AC_BKG_04_persist_when_notification_down | Make notification service fail, call `POST /bookings`, assert booking persisted, queue_number returned, and `booking_retry_queue` has entry with next_retry_at within 10 minutes |
| AC-BKG-05 | test_AC_BKG_05_performance_availability_p95 | Run performance script simulating 200 concurrent users calling `GET /availability`, measure p95 <= 2s on staging environment |
| AC-BKG-06 | test_AC_BKG_06_audit_log_on_access | Call booking detail endpoint and assert `audit_logs` contains actor, timestamp, target_id |

7. ลำดับงาน (5–10 ขั้น)

1. สร้าง DB schema และ migration (`time_slots`, `bookings`, `booking_retry_queue`, `audit_logs`) — (FR-BKG-01, FR-BKG-04, DOM-PDPA-01)
2. พัฒนา `GET /availability` และ caching สำหรับ 30 วัน — (FR-BKG-01, AC-BKG-05)
3. พัฒนา `POST /bookings` transactional flow (ตรวจ existing booking, create booking, decrement slot, generate queue) — (FR-BKG-02, FR-BKG-04, AC-BKG-01..AC-BKG-03)
4. พัฒนา worker สำหรับ notification retry และ queue — (FR-BKG-05, NFR-REL-02, AC-BKG-04)
5. เขียน integration tests กับ HIS mock และ notification mock — (IF-HIS-01, IF-NOT-01)
6. เขียน performance test script และรันบน staging — (NFR-PERF-01, AC-BKG-05)
7. เพิ่ม audit logging และตรวจสอบการเข้าถึง — (DOM-PDPA-01, AC-BKG-06)

8. สิ่งที่ยังไม่ทำ (Open Questions)

- Q-01: "ช่วงเวลาใกล้เคียง" นับเฉพาะวันเดียวกัน หรือรวมวันถัดไปด้วย? — ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบ (affects FR-BKG-03 alternatives)
- Q-02: หมายเลขคิวรีเซ็ตรายวัน หรือนับต่อเนื่อง? — ส่วนที่เกี่ยวข้องกับข้อนี้จะยังไม่สร้างจนกว่าจะได้คำตอบ (affects queue_number generation)

---

โปรดตรวจสอบ: ผมไม่เปลี่ยน Open Questions จาก `spec.md` — ส่วนที่เกี่ยวข้องกับ Q-01/Q-02 จะยังไม่สร้างจนกว่าจะได้คำตอบจากทีม

