import { render, screen } from '@testing-library/react'
import App from '../App.jsx'

test('TC-BKG-01-1: หน้าแสดงสถานะการจองสำเร็จ', () => {
  // Given: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
  // When: ยืนยันการจอง
  render(<App />)

  // Then: บันทึกสำเร็จ; แสดงหมายเลขคิว (รอ Q-02) -> ยังไม่ตรวจในโค้ดเพราะรอ Q-02
  // ไม่เขียน assert สำหรับหมายเลขคิวตามเงื่อนไข Q-02
  expect(screen.getByText(/ระบบจองคิวตรวจสุขภาพ/i)).toBeTruthy()
  expect(screen.queryByText(/การจองสำเร็จ/i)).not.toBeNull()
})
