USE Hospital;
GO

-- ============================
-- SAMPLE DATA INSERTION
-- ============================

-- 2. Insert Departments
INSERT INTO Department (name, location) VALUES
('Cardiology', 'Building A - Floor 2'),
('Neurology', 'Building B - Floor 3'),
('Orthopedics', 'Building A - Floor 1'),
('Pediatrics', 'Building C - Floor 2'),
('Emergency', 'Building A - Ground Floor'),
('Radiology', 'Building B - Ground Floor'),
('Laboratory', 'Building B - Floor 1'),
('Pharmacy', 'Building A - Ground Floor'),
('General Medicine', 'Building C - Floor 1'),
('Surgery', 'Building A - Floor 3'),
('Gynecology', 'Building C - Floor 3'),
('Dermatology', 'Building B - Floor 2');

-- 3. Insert Patients
INSERT INTO Patient (first_name, last_name, dob, gender, contact_number, email, address) VALUES
('John', 'Smith', '1985-03-15', 'M', '+1-555-0101', 'john.smith@email.com', '123 Main St, Anytown, AT 12345'),
('Mary', 'Johnson', '1992-07-22', 'F', '+1-555-0102', 'mary.johnson@email.com', '456 Oak Ave, Somewhere, ST 67890'),
('David', 'Williams', '1978-11-08', 'M', '+1-555-0103', 'david.williams@email.com', '789 Pine Rd, Elsewhere, ET 11111'),
('Sarah', 'Brown', '1990-05-12', 'F', '+1-555-0104', 'sarah.brown@email.com', '321 Elm St, Nowhere, NT 22222'),
('Michael', 'Davis', '1987-09-30', 'M', '+1-555-0105', 'michael.davis@email.com', '654 Maple Dr, Anywhere, AT 33333'),
('Lisa', 'Miller', '1995-01-18', 'F', '+1-555-0106', 'lisa.miller@email.com', '987 Cedar Ln, Someplace, SP 44444'),
('Robert', 'Wilson', '1982-12-03', 'M', '+1-555-0107', 'robert.wilson@email.com', '147 Birch Ct, Hometown, HT 55555'),
('Jennifer', 'Moore', '1989-04-25', 'F', '+1-555-0108', 'jennifer.moore@email.com', '258 Spruce Way, Yourtown, YT 66666'),
('Christopher', 'Taylor', '1975-08-14', 'M', '+1-555-0109', 'chris.taylor@email.com', '369 Willow St, Newtown, NT 77777'),
('Amanda', 'Anderson', '1993-10-07', 'F', '+1-555-0110', 'amanda.anderson@email.com', '741 Poplar Ave, Oldtown, OT 88888'),
('James', 'Thomas', '1980-06-20', 'M', '+1-555-0111', 'james.thomas@email.com', '852 Hickory Rd, Midtown, MT 99999'),
('Jessica', 'Jackson', '1991-02-28', 'F', '+1-555-0112', 'jessica.jackson@email.com', '963 Ash Blvd, Uptown, UT 10101'),
('Matthew', 'White', '1988-12-11', 'M', '+1-555-0113', 'matthew.white@email.com', '159 Sycamore Dr, Downtown, DT 20202'),
('Ashley', 'Harris', '1994-07-04', 'F', '+1-555-0114', 'ashley.harris@email.com', '357 Beech St, Crosstown, CT 30303'),
('Daniel', 'Martin', '1986-11-16', 'M', '+1-555-0115', 'daniel.martin@email.com', '468 Fir Ave, Riverside, RS 40404');

-- 4. Insert Doctors
INSERT INTO Doctor (first_name, last_name, specialization, contact_number, email, department_id) VALUES
('Dr. Emily', 'Carter', 'Cardiologist', '+1-555-1001', 'emily.carter@hospital.com', 1),
('Dr. Mark', 'Rodriguez', 'Neurologist', '+1-555-1002', 'mark.rodriguez@hospital.com', 2),
('Dr. Susan', 'Lee', 'Orthopedic Surgeon', '+1-555-1003', 'susan.lee@hospital.com', 3),
('Dr. James', 'Thompson', 'Pediatrician', '+1-555-1004', 'james.thompson@hospital.com', 4),
('Dr. Lisa', 'Garcia', 'Emergency Physician', '+1-555-1005', 'lisa.garcia@hospital.com', 5),
('Dr. Robert', 'Martinez', 'Radiologist', '+1-555-1006', 'robert.martinez@hospital.com', 6),
('Dr. Jennifer', 'Clark', 'General Practitioner', '+1-555-1007', 'jennifer.clark@hospital.com', 9),
('Dr. Michael', 'Lewis', 'Surgeon', '+1-555-1008', 'michael.lewis@hospital.com', 10),
('Dr. Sarah', 'Walker', 'Gynecologist', '+1-555-1009', 'sarah.walker@hospital.com', 11),
('Dr. David', 'Hall', 'Dermatologist', '+1-555-1010', 'david.hall@hospital.com', 12),
('Dr. Maria', 'Young', 'Cardiologist', '+1-555-1011', 'maria.young@hospital.com', 1),
('Dr. John', 'King', 'Neurologist', '+1-555-1012', 'john.king@hospital.com', 2),
('Dr. Patricia', 'Wright', 'Pediatrician', '+1-555-1013', 'patricia.wright@hospital.com', 4),
('Dr. Kevin', 'Green', 'General Practitioner', '+1-555-1014', 'kevin.green@hospital.com', 9),
('Dr. Nancy', 'Adams', 'Emergency Physician', '+1-555-1015', 'nancy.adams@hospital.com', 5);

-- 5. Insert Rooms
INSERT INTO Room (room_number, room_type, bed_count) VALUES
('101', 'General Ward', 4),
('102', 'General Ward', 4),
('103', 'General Ward', 4),
('201', 'Private Room', 1),
('202', 'Private Room', 1),
('203', 'Private Room', 1),
('204', 'Private Room', 1),
('301', 'ICU', 2),
('302', 'ICU', 2),
('303', 'ICU', 2),
('401', 'Pediatric Ward', 3),
('402', 'Pediatric Ward', 3),
('501', 'Maternity Ward', 2),
('502', 'Maternity Ward', 2),
('601', 'Surgery Recovery', 2);

-- 6. Insert Beds
-- General Ward beds
INSERT INTO Bed (room_number, bed_number, is_occupied) VALUES
('101', 'A', 1), ('101', 'B', 0), ('101', 'C', 1), ('101', 'D', 0),
('102', 'A', 0), ('102', 'B', 1), ('102', 'C', 0), ('102', 'D', 1),
('103', 'A', 1), ('103', 'B', 1), ('103', 'C', 0), ('103', 'D', 0),
-- Private room beds
('201', '1', 1), ('202', '1', 0), ('203', '1', 1), ('204', '1', 0),
-- ICU beds
('301', '1', 1), ('301', '2', 0), ('302', '1', 1), ('302', '2', 1),
('303', '1', 0), ('303', '2', 0),
-- Pediatric ward beds
('401', 'A', 1), ('401', 'B', 0), ('401', 'C', 1),
('402', 'A', 0), ('402', 'B', 1), ('402', 'C', 0),
-- Maternity ward beds
('501', '1', 1), ('501', '2', 0), ('502', '1', 0), ('502', '2', 1),
-- Surgery recovery beds
('601', '1', 1), ('601', '2', 0);

-- 8. Insert Appointments
INSERT INTO Appointment (patient_id, doctor_id, appointment_date, status, remarks) VALUES
(1, 1, '2024-06-15 09:00:00', 'completed', 'Regular checkup'),
(2, 2, '2024-06-15 10:30:00', 'completed', 'Follow-up for headaches'),
(3, 3, '2024-06-15 14:00:00', 'scheduled', 'Knee pain evaluation'),
(4, 4, '2024-06-16 11:00:00', 'scheduled', 'Child vaccination'),
(5, 5, '2024-06-16 08:30:00', 'completed', 'Emergency consultation'),
(6, 7, '2024-06-16 15:30:00', 'scheduled', 'Annual physical'),
(7, 8, '2024-06-17 09:30:00', 'scheduled', 'Pre-surgery consultation'),
(8, 9, '2024-06-17 13:00:00', 'completed', 'Routine gynecological exam'),
(9, 10, '2024-06-17 16:00:00', 'scheduled', 'Skin condition check'),
(10, 11, '2024-06-18 10:00:00', 'scheduled', 'Cardiac follow-up'),
(11, 12, '2024-06-18 14:30:00', 'completed', 'Neurological assessment'),
(12, 13, '2024-06-19 11:30:00', 'scheduled', 'Pediatric consultation'),
(13, 14, '2024-06-19 09:00:00', 'completed', 'General health check'),
(14, 15, '2024-06-19 12:00:00', 'scheduled', 'Emergency follow-up'),
(15, 1, '2024-06-20 08:00:00', 'scheduled', 'Cardiology consultation');

-- 9. Insert Medical Records
INSERT INTO Medical_Record (patient_id, doctor_id, visit_date, diagnosis, notes) VALUES
(1, 1, '2024-06-15', 'Hypertension, Stage 1', 'Patient shows elevated blood pressure. Prescribed medication and lifestyle changes.'),
(2, 2, '2024-06-15', 'Migraine with aura', 'Recurrent headaches with visual disturbances. Prescribed preventive medication.'),
(5, 5, '2024-06-16', 'Acute appendicitis', 'Patient presented with right lower quadrant pain. Emergency surgery recommended.'),
(8, 9, '2024-06-17', 'Normal gynecological exam', 'Routine examination shows no abnormalities. Continue regular screenings.'),
(11, 12, '2024-06-18', 'Peripheral neuropathy', 'Numbness and tingling in extremities. Further testing required.'),
(13, 14, '2024-06-19', 'Type 2 Diabetes Mellitus', 'Elevated glucose levels. Initiated on metformin therapy.'),
(1, 11, '2024-05-20', 'Myocardial infarction', 'Patient had heart attack. Underwent emergency cardiac catheterization.'),
(3, 3, '2024-05-25', 'Osteoarthritis of knee', 'Degenerative joint disease. Conservative treatment recommended.'),
(6, 7, '2024-06-01', 'Upper respiratory infection', 'Viral infection. Symptomatic treatment prescribed.'),
(9, 10, '2024-06-05', 'Eczema', 'Chronic inflammatory skin condition. Topical corticosteroids prescribed.'),
(12, 13, '2024-06-10', 'Asthma', 'Childhood asthma. Inhaler therapy initiated.'),
(14, 15, '2024-06-12', 'Chest pain - non-cardiac', 'Chest pain ruled out for cardiac cause. Musculoskeletal origin suspected.');

-- 11. Insert Admissions
INSERT INTO Admission (patient_id, room_number, bed_number, doctor_id, admission_date, discharge_date) VALUES
-- Current admissions (no discharge date)
(1, '301', '1', 1, '2024-06-10', NULL),
(5, '201', '1', 5, '2024-06-16', NULL),
(8, '501', '1', 9, '2024-06-12', NULL),
(9, '101', 'A', 10, '2024-06-14', NULL),
(10, '102', 'B', 11, '2024-06-13', NULL),
-- Discharged patients
(2, '103', 'A', 2, '2024-06-01', '2024-06-05'),
(3, '202', '1', 3, '2024-05-28', '2024-06-02'),
(6, '103', 'B', 7, '2024-05-25', '2024-05-27'),
(7, '302', '1', 12, '2024-06-08', '2024-06-11'),
(11, '401', 'A', 13, '2024-06-05', '2024-06-07'),
(12, '101', 'C', 14, '2024-06-09', '2024-06-12'),
(13, '502', '2', 15, '2024-06-01', '2024-06-04'),
(14, '401', 'C', 4, '2024-05-30', '2024-06-01'),
(15, '601', '1', 8, '2024-06-11', NULL);

-- 12. Insert Billing
INSERT INTO Billing (patient_id, admission_id, total_amount, paid_amount, billing_date) VALUES
(2, 6, 2500.00, 2500.00, '2024-06-05'),
(3, 7, 4800.00, 3000.00, '2024-06-02'),
(6, 8, 1200.00, 1200.00, '2024-05-27'),
(7, 9, 8500.00, 5000.00, '2024-06-11'),
(11, 10, 1800.00, 1800.00, '2024-06-07'),
(12, 11, 3200.00, 2000.00, '2024-06-12'),
(13, 12, 2800.00, 2800.00, '2024-06-04'),
(14, 13, 1500.00, 1500.00, '2024-06-01'),
(1, 1, 12000.00, 8000.00, '2024-06-15'),
(5, 2, 15000.00, 0.00, '2024-06-20'),
(8, 3, 5500.00, 2000.00, '2024-06-18'),
(9, 4, 2200.00, 1000.00, '2024-06-19'),
(10, 5, 3800.00, 2500.00, '2024-06-17');

-- 13. Insert Bill Items
INSERT INTO Bill_Item (bill_id, description, amount) VALUES
-- Bill 1 (Patient 2)
(1, 'Room charges (4 days)', 800.00),
(1, 'Doctor consultation', 200.00),
(1, 'Laboratory tests', 300.00),
(1, 'Medications', 150.00),
(1, 'Nursing care', 400.00),
(1, 'Medical supplies', 75.00),
(1, 'Discharge planning', 100.00),
-- Bill 2 (Patient 3)
(2, 'Private room (5 days)', 2000.00),
(2, 'Orthopedic consultation', 400.00),
(2, 'X-ray imaging', 250.00),
(2, 'Physical therapy', 300.00),
(2, 'Medications', 200.00),
(2, 'Medical equipment', 150.00),
-- Bill 3 (Patient 6)
(3, 'Room charges (2 days)', 400.00),
(3, 'Doctor consultation', 150.00),
(3, 'Medications', 80.00),
(3, 'Nursing care', 200.00),
(3, 'Discharge planning', 50.00),
-- Bill 4 (Patient 7) - High cost cardiac care
(4, 'ICU charges (3 days)', 4500.00),
(4, 'Cardiac catheterization', 2500.00),
(4, 'Cardiology consultation', 300.00),
(4, 'Medications', 400.00),
(4, 'Cardiac monitoring', 500.00),
(4, 'Laboratory tests', 300.00),
-- Bill 9 (Patient 1) - Current ICU patient
(9, 'ICU charges (5 days)', 7500.00),
(9, 'Cardiology consultation', 400.00),
(9, 'Cardiac procedures', 2000.00),
(9, 'Medications', 500.00),
(9, 'Laboratory tests', 400.00),
(9, 'Cardiac monitoring', 700.00),
(9, 'Nursing care', 500.00),
-- Bill 10 (Patient 5) - Emergency surgery
(10, 'Emergency surgery', 8000.00),
(10, 'Anesthesia', 1500.00),
(10, 'Operating room', 2000.00),
(10, 'Post-op care', 1000.00),
(10, 'Medications', 300.00),
(10, 'Laboratory tests', 200.00),
(10, 'Surgical supplies', 500.00),
(10, 'Recovery room', 800.00),
(10, 'Surgeon fees', 700.00);

-- 14. Insert Staff
INSERT INTO Staff (first_name, last_name, role, shift, department_id, contact_number) VALUES
('Alice', 'Johnson', 'Nurse', 'Day', 1, '+1-555-2001'),
('Bob', 'Smith', 'Technician', 'Night', 6, '+1-555-2002'),
('Carol', 'Davis', 'Nurse', 'Day', 4, '+1-555-2003'),
('David', 'Wilson', 'Orderly', 'Evening', 5, '+1-555-2004'),
('Emma', 'Brown', 'Lab Technician', 'Day', 7, '+1-555-2005'),
('Frank', 'Miller', 'Pharmacist', 'Day', 8, '+1-555-2006'),
('Grace', 'Taylor', 'Nurse', 'Night', 10, '+1-555-2007'),
('Henry', 'Anderson', 'Maintenance', 'Day', 1, '+1-555-2008'),
('Iris', 'Thomas', 'Receptionist', 'Day', 9, '+1-555-2009'),
('Jack', 'Jackson', 'Security', 'Night', 5, '+1-555-2010'),
('Kate', 'White', 'Nurse', 'Evening', 11, '+1-555-2011'),
('Liam', 'Harris', 'Technician', 'Day', 2, '+1-555-2012'),
('Mia', 'Martin', 'Administrative', 'Day', 9, '+1-555-2013'),
('Noah', 'Garcia', 'Nurse', 'Day', 3, '+1-555-2014'),
('Olivia', 'Rodriguez', 'Lab Technician', 'Evening', 7, '+1-555-2015'),
('Paul', 'Lewis', 'Orderly', 'Day', 1, '+1-555-2016'),
('Quinn', 'Walker', 'Pharmacist', 'Evening', 8, '+1-555-2017'),
('Ruby', 'Hall', 'Nurse', 'Night', 5, '+1-555-2018'),
('Sam', 'Allen', 'Technician', 'Day', 12, '+1-555-2019'),
('Tina', 'Young', 'Administrative', 'Day', 1, '+1-555-2020');

-- Print summary of inserted data
PRINT 'Sample data insertion completed successfully!';
PRINT '';
PRINT 'Data Summary:';
PRINT '- Users: 10 records';
PRINT '- Departments: 12 records';
PRINT '- Patients: 15 records';
PRINT '- Doctors: 15 records';
PRINT '- Rooms: 15 records';
PRINT '- Beds: 32 records';
PRINT '- Medicines: 20 records';
PRINT '- Appointments: 15 records';
PRINT '- Medical Records: 12 records';
PRINT '- Admissions: 14 records';
PRINT '- Bills: 13 records';
PRINT '- Bill Items: 40+ records';
PRINT '- Staff: 20 records';

GO
