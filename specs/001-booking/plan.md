# Plan: จองคิวตรวจสุขภาพ (Booking) — Technical Plan

สรุปสั้น ๆ: แผนนี้สอดคล้องกับ `SPEC-BKG-001` โดยแบ่งงานตามข้อกำหนดหลัก (FR/NFR/AC) เพื่อให้ทีมพัฒนาและทดสอบได้ชัดเจน

1. ขอบเขตงานและ Deliverables
   - API: `GET /availability`, `POST /bookings`, `GET /bookings/{id}`
   - Database: ตาราง `bookings`, `time_slots`, `booking_retry_queue`, audit log per DOM-PDPA-01
   - Worker: background worker สำหรับ re-send message (retry ทุก 10 นาที ตาม ASM-03)
   - Tests: unit tests, integration tests (HIS mock), performance test script สำหรับ AC-BKG-05

2. Mapping ระหว่างงานกับข้อกำหนด
   - FR-BKG-01 → `GET /availability`, caching และ pagination (30 วันข้างหน้า)
   - FR-BKG-02 → ใน `POST /bookings` ตรวจสอบสถานะคิวในวันเดียวกันก่อนสร้าง (reject และคืนหมายเลขเดิม)
   - FR-BKG-03 → เมื่อยืนยันเจอเต็ม ให้ API คืนรหัสสถานะและรายการช่วงเวลาใกล้เคียง 3 ตัว
   - FR-BKG-04 → ทำเป็น transaction: create booking → decrement slot → generate queue number → enqueue notification request
   - FR-BKG-05, NFR-REL-02 → Worker อ่าน `booking_retry_queue` และพยายามส่งตาม policy (retry ทุก 10 นาที, persistence)
   - FR-BKG-06 → `POST /availability` คำนวณตามแพ็กเกจที่ส่งมาพร้อมคำขอ
   - NFRs → TLS, audit log, performance script (p95 target)

3. Database schema (สรุป)
   - `time_slots` (id, date, start_time, end_time, capacity, remaining)
   - `bookings` (id, hn, user_id, time_slot_id, package_id, status, queue_number, created_at)
   - `booking_retry_queue` (id, booking_id, payload, next_retry_at, attempts)
   - `audit_logs` (id, actor, action, target_id, timestamp)

4. Transactional behaviour and concurrency
   - ใช้ DB transaction เมื่อสร้าง booking และลด `time_slots.remaining` เพื่อป้องกัน over-commit
   - สำหรับ high concurrency ให้พิจารณา optimistic locking (version) หรือ SELECT ... FOR UPDATE

5. Integration with HIS and Notification
   - HIS: ข้อมูลผู้รับบริการนำจาก `IF-HIS-01` โดยรับ HN หลังการแมตช์ (HIS mock ใน test)
   - Notification: push request เข้า `booking_retry_queue` แบบ asynchronous (ไม่รอผลการส่ง)

6. Retry worker design
   - Scheduled worker poll `booking_retry_queue` ดูรายการที่ `next_retry_at <= now`
   - พยายามส่งข้อความ แล้วเมื่อไม่สำเร็จ ตั้ง `next_retry_at = now + 10 minutes` และเพิ่ม `attempts`
   - เก็บ log ของแต่ละความพยายามเพื่อ AC-BKG-04

7. Performance and testing
   - สร้าง performance script สำหรับ `GET /availability` ที่จำลอง 200 concurrent users และวัด p95
   - Unit tests ครอบคลุม business rules (FR-BKG-02, FR-BKG-03, FR-BKG-04, FR-BKG-06)
   - Integration tests กับ HIS mock และ notification mock

8. Deliverable checklist
   - [ ] API endpoints implemented
   - [ ] DB migrations และ schema
   - [ ] Background worker + retry queue
   - [ ] Tests (unit, integration, perf)
   - [ ] Updated `specs/001-booking/spec.md` (Draft v2)

9. Open implementation questions (จาก spec)
   - Q1, Q3–Q8 ยังต้องการคำตอบก่อน release; ถ้าทีมอนุมัติ ASM-03 ให้ถือเป็นข้อสมมติฐาน

10. เวลาโดยประมาณ
    - Est. 2 sprint: API + DB + basic worker + tests (ทีม 3 คน)
