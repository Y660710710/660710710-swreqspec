# AC-BKG-01: จองคิวสำเร็จ (FR-BKG-04)
# Given / When / Then ตาม TC-BKG-01-1 ถึง TC-BKG-01-3
from app.db.models import Booking, Slot
from tests.conftest import AUTH


def test_TC_BKG_01_1_last_seat(client, db, make_slot):
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ; ที่นั่งว่างของช่วงนั้นเป็น 0
    assert res.status_code == 201
    assert db.get(Slot, slot.id).remaining == 0
    assert db.query(Booking).count() == 1


def test_TC_BKG_01_2_no_seat_left(client, db, make_slot):
    # Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่ โดยมีการจองก่อนหน้า 1 รายการในช่วงเดียวกัน
    slot = make_slot(start="09:00", remaining=1)
    other_slot = make_slot(start="09:00", remaining=1, days_from_today=2)
    client.post("/bookings", json={"slot_id": other_slot.id}, headers=AUTH)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    # Then: บันทึกสำเร็จ; ที่นั่งว่างของช่วงนั้นลดจาก 1 เป็น 0 โดยไม่มีรายการจองซ้อนเกิดขึ้น
    assert res.status_code == 201
    assert db.get(Slot, slot.id).remaining == 0
    assert db.query(Booking).count() == 2


def test_TC_BKG_01_3_not_verified(client, make_slot):
    # Given: ไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
    slot = make_slot(start="09:00", remaining=1)

    # When: ยืนยันการจอง
    res = client.post("/bookings", json={"slot_id": slot.id})

    # Then: ปฏิเสธการจอง และไม่ตัดจำนวนที่นั่ง
    assert res.status_code == 401
    assert res.json()["detail"] == "ยังไม่ได้ยืนยันตัวตน"
