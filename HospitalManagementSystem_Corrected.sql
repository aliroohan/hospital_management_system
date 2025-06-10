USE Hospital;
GO

-- Drop existing tables (optional safety cleanup for development/testing)
-- DROP TABLE IF EXISTS Prescription_Medicine, Bill_Item, Billing, Admission, Bed, Room, Pharmacy, Medical_Record, Appointment, Doctor, Patient, Department, Staff, Users;

-- 1. Department
CREATE TABLE Department (
    department_id INT PRIMARY KEY IDENTITY,
    name VARCHAR(100),
    location VARCHAR(100)
);

-- 2. Patient
CREATE TABLE Patient (
    patient_id INT PRIMARY KEY IDENTITY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    dob DATE,
    gender CHAR(1),
    contact_number VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(200)
);

-- 3. Doctor
CREATE TABLE Doctor (
    doctor_id INT PRIMARY KEY IDENTITY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    specialization VARCHAR(100),
    contact_number VARCHAR(20),
    email VARCHAR(100),
    department_id INT FOREIGN KEY REFERENCES Department(department_id)
);

-- 4. Appointment
CREATE TABLE Appointment (
    appointment_id INT PRIMARY KEY IDENTITY,
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    doctor_id INT FOREIGN KEY REFERENCES Doctor(doctor_id),
    appointment_date DATETIME,
    status VARCHAR(20),
    remarks TEXT
);

-- 5. Medical_Record
CREATE TABLE Medical_Record (
    record_id INT PRIMARY KEY IDENTITY,
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    doctor_id INT FOREIGN KEY REFERENCES Doctor(doctor_id),
    visit_date DATE,
    diagnosis TEXT,
    notes TEXT
);

-- 6. Pharmacy
CREATE TABLE Pharmacy (
    medicine_id INT PRIMARY KEY IDENTITY,
    name VARCHAR(100),
    stock_quantity INT,
    unit_price DECIMAL(10,2),
    expiry_date DATE
);

-- 7. Prescription_Medicine
CREATE TABLE Prescription_Medicine (
    record_id INT FOREIGN KEY REFERENCES Medical_Record(record_id),
    medicine_id INT FOREIGN KEY REFERENCES Pharmacy(medicine_id),
    dosage VARCHAR(100),
    duration VARCHAR(50),
    instructions TEXT,
    PRIMARY KEY (record_id, medicine_id)
);

-- 8. Room
CREATE TABLE Room (
    room_id INT PRIMARY KEY IDENTITY,
    room_number VARCHAR(10),
    room_type VARCHAR(50),
    bed_count INT
);

-- 9. Bed
CREATE TABLE Bed (
    bed_id INT PRIMARY KEY IDENTITY,
    room_id INT FOREIGN KEY REFERENCES Room(room_id),
    bed_number VARCHAR(10),
    is_occupied BIT
);

-- 10. Admission
CREATE TABLE Admission (
    admission_id INT PRIMARY KEY IDENTITY,
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    room_id INT FOREIGN KEY REFERENCES Room(room_id),
    bed_id INT FOREIGN KEY REFERENCES Bed(bed_id),
    doctor_id INT FOREIGN KEY REFERENCES Doctor(doctor_id),
    admission_date DATE,
    discharge_date DATE
);

-- 11. Billing
CREATE TABLE Billing (
    bill_id INT PRIMARY KEY IDENTITY,
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    admission_id INT FOREIGN KEY REFERENCES Admission(admission_id),
    total_amount DECIMAL(10,2),
    paid_amount DECIMAL(10,2),
    billing_date DATE
);

-- 12. Bill_Item
CREATE TABLE Bill_Item (
    item_id INT PRIMARY KEY IDENTITY,
    bill_id INT FOREIGN KEY REFERENCES Billing(bill_id),
    description VARCHAR(200),
    amount DECIMAL(10,2)
);

-- 13. Staff
CREATE TABLE Staff (
    staff_id INT PRIMARY KEY IDENTITY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(50),
    shift VARCHAR(50),
    department_id INT FOREIGN KEY REFERENCES Department(department_id),
    contact_number VARCHAR(20)
);

-- 14. Users
CREATE TABLE Users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('Admin', 'Appointment', 'Patient', 'Pharmacist'))
);
GO

-- ============================
-- STORED PROCEDURES
-- ============================

GO

-- 1. Register new patient
CREATE OR ALTER PROCEDURE RegisterPatient
    @first_name VARCHAR(50),
    @last_name VARCHAR(50),
    @dob DATE,
    @gender CHAR(1),
    @contact_number VARCHAR(20),
    @email VARCHAR(100),
    @address VARCHAR(200)
AS
BEGIN
    INSERT INTO Patient(first_name, last_name, dob, gender, contact_number, email, address)
    VALUES (@first_name, @last_name, @dob, @gender, @contact_number, @email, @address);
END;
GO


-- 2. Book Appointment
CREATE PROCEDURE BookAppointment
    @patient_id INT,
    @doctor_id INT,
    @appointment_date DATETIME,
    @remarks TEXT
AS
BEGIN
    INSERT INTO Appointment(patient_id, doctor_id, appointment_date, status, remarks)
    VALUES (@patient_id, @doctor_id, @appointment_date, 'scheduled', @remarks);
END;

GO

-- 3. Create Medical Record
CREATE PROCEDURE CreateMedicalRecord
    @patient_id INT,
    @doctor_id INT,
    @visit_date DATE,
    @diagnosis TEXT,
    @notes TEXT
AS
BEGIN
    INSERT INTO Medical_Record(patient_id, doctor_id, visit_date, diagnosis, notes)
    VALUES (@patient_id, @doctor_id, @visit_date, @diagnosis, @notes);
END;

GO

-- 4. Add Medicine to Prescription
CREATE PROCEDURE AddPrescription
    @record_id INT,
    @medicine_id INT,
    @dosage VARCHAR(100),
    @duration VARCHAR(50),
    @instructions TEXT
AS
BEGIN
    INSERT INTO Prescription_Medicine(record_id, medicine_id, dosage, duration, instructions)
    VALUES (@record_id, @medicine_id, @dosage, @duration, @instructions);
END;

GO

CREATE OR ALTER PROCEDURE AdmitPatient
    @patient_id INT,
    @room_id INT,
    @bed_id INT,
    @doctor_id INT,
    @admission_date DATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Ensure the bed is not already occupied
    IF EXISTS (
        SELECT 1
        FROM Bed
        WHERE bed_id = @bed_id AND is_occupied = 1
    )
    BEGIN
        RAISERROR('The selected bed is already occupied.', 16, 1);
        RETURN;
    END

    -- Admit the patient
    INSERT INTO Admission (patient_id, room_id, bed_id, doctor_id, admission_date)
    VALUES (@patient_id, @room_id, @bed_id, @doctor_id, @admission_date);

    -- (Optional) The bed is marked as occupied automatically by a trigger
END;
GO

-- 6. Generate Bill
CREATE PROCEDURE GenerateBill
    @patient_id INT,
    @admission_id INT,
    @total_amount DECIMAL(10,2),
    @paid_amount DECIMAL(10,2),
    @billing_date DATE
AS
BEGIN
    INSERT INTO Billing(patient_id, admission_id, total_amount, paid_amount, billing_date)
    VALUES (@patient_id, @admission_id, @total_amount, @paid_amount, @billing_date);
END;

GO

-- 7. Add Bill Item
CREATE PROCEDURE AddBillItem
    @bill_id INT,
    @description VARCHAR(200),
    @amount DECIMAL(10,2)
AS
BEGIN
    INSERT INTO Bill_Item(bill_id, description, amount)
    VALUES (@bill_id, @description, @amount);
END;

GO

-- 8. Discharge Patient
CREATE PROCEDURE DischargePatient
    @admission_id INT,
    @discharge_date DATE
AS
BEGIN
    UPDATE Admission SET discharge_date = @discharge_date WHERE admission_id = @admission_id;
END;

GO

-- 9. Add New Medicine
CREATE PROCEDURE AddMedicine
    @name VARCHAR(100),
    @stock_quantity INT,
    @unit_price DECIMAL(10,2),
    @expiry_date DATE
AS
BEGIN
    INSERT INTO Pharmacy(name, stock_quantity, unit_price, expiry_date)
    VALUES (@name, @stock_quantity, @unit_price, @expiry_date);
END;

GO

-- 10. Update Stock
CREATE PROCEDURE UpdateMedicineStock
    @medicine_id INT,
    @quantity INT
AS
BEGIN
    UPDATE Pharmacy SET stock_quantity = stock_quantity + @quantity WHERE medicine_id = @medicine_id;
END;

-- ============================
-- TRIGGERS
-- ============================

GO

-- 1. Trigger: Set bed to occupied after admission
CREATE OR ALTER TRIGGER trg_UpdateBedStatusAfterAdmission
ON Admission
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE b
    SET b.is_occupied = 1
    FROM Bed b
    INNER JOIN inserted i ON b.bed_id = i.bed_id;
END;
GO

-- 2. Trigger: Decrease stock when medicine is prescribed
CREATE OR ALTER TRIGGER trg_UpdateStockAfterPrescription
ON Prescription_Medicine
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE p
    SET p.stock_quantity = p.stock_quantity - 1
    FROM Pharmacy p
    INNER JOIN inserted i ON p.medicine_id = i.medicine_id;
END;
GO

-- 3. Trigger: Free bed on discharge
CREATE OR ALTER TRIGGER trg_ReleaseBedOnDischarge
ON Admission
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE b
    SET b.is_occupied = 0
    FROM Bed b
    INNER JOIN inserted i ON b.bed_id = i.bed_id
    INNER JOIN deleted d ON i.admission_id = d.admission_id
    WHERE d.discharge_date IS NULL AND i.discharge_date IS NOT NULL;
END;
GO
