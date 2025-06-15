USE Hospital;
GO

-- Drop existing tables (optional safety cleanup for development/testing)
-- DROP TABLE IF EXISTS Bill_Item, Billing, Admission, Bed, Room, Medical_Record, Appointment, Doctor, Patient, Department, Staff, Users;

-- 1. Users (moved to top since other tables might reference it)
CREATE TABLE Users (
    user_id INT IDENTITY(1,1) PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('Admin', 'Appointment', 'Patient'))
);
GO

-- 2. Department
CREATE TABLE Department (
    department_id INT PRIMARY KEY IDENTITY,
    name VARCHAR(100),
    location VARCHAR(100)
);

-- 3. Patient
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

-- 4. Doctor
CREATE TABLE Doctor (
    doctor_id INT PRIMARY KEY IDENTITY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    specialization VARCHAR(100),
    contact_number VARCHAR(20),
    email VARCHAR(100),
    department_id INT FOREIGN KEY REFERENCES Department(department_id)
);

-- 5. Appointment
CREATE TABLE Appointment (
    appointment_id INT PRIMARY KEY IDENTITY,
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    doctor_id INT FOREIGN KEY REFERENCES Doctor(doctor_id),
    appointment_date DATETIME,
    status VARCHAR(20),
    remarks TEXT
);

-- 6. Medical_Record
CREATE TABLE Medical_Record (
    record_id INT PRIMARY KEY IDENTITY,
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    doctor_id INT FOREIGN KEY REFERENCES Doctor(doctor_id),
    visit_date DATE,
    diagnosis TEXT,
    notes TEXT
);

-- 7. Room
CREATE TABLE Room (
    room_number VARCHAR(10) PRIMARY KEY,
    room_type VARCHAR(50),
    bed_count INT
);

-- 8. Bed
CREATE TABLE Bed (
    room_number VARCHAR(10) FOREIGN KEY REFERENCES Room(room_number),
    bed_number VARCHAR(10) NOT NULL,
    is_occupied BIT NOT NULL,
    PRIMARY KEY (room_number, bed_number)
);

-- 9. Admission
CREATE TABLE Admission (
    admission_id INT PRIMARY KEY IDENTITY,
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    room_number VARCHAR(10),
    bed_number VARCHAR(10),
    doctor_id INT FOREIGN KEY REFERENCES Doctor(doctor_id),
    admission_date DATE,
    discharge_date DATE,
    FOREIGN KEY (room_number, bed_number) REFERENCES Bed(room_number, bed_number)
);

-- 10. Billing
CREATE TABLE Billing (
    bill_id INT PRIMARY KEY IDENTITY,
    patient_id INT FOREIGN KEY REFERENCES Patient(patient_id),
    admission_id INT FOREIGN KEY REFERENCES Admission(admission_id),
    total_amount DECIMAL(10,2),
    paid_amount DECIMAL(10,2),
    billing_date DATE
);

-- 11. Bill_Item
CREATE TABLE Bill_Item (
    item_id INT PRIMARY KEY IDENTITY,
    bill_id INT FOREIGN KEY REFERENCES Billing(bill_id),
    description VARCHAR(200),
    amount DECIMAL(10,2)
);

-- 12. Staff
CREATE TABLE Staff (
    staff_id INT PRIMARY KEY IDENTITY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    role VARCHAR(50),
    shift VARCHAR(50),
    department_id INT FOREIGN KEY REFERENCES Department(department_id),
    contact_number VARCHAR(20)
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

-- 4. Admit Patient
CREATE OR ALTER PROCEDURE AdmitPatient
    @patient_id INT,
    @room_number VARCHAR(10),
    @bed_number VARCHAR(10),
    @doctor_id INT,
    @admission_date DATE
AS
BEGIN
    SET NOCOUNT ON;

    -- Ensure the bed is not already occupied
    IF EXISTS (
        SELECT 1
        FROM Bed
        WHERE room_number = @room_number 
        AND bed_number = @bed_number 
        AND is_occupied = 1
    )
    BEGIN
        RAISERROR('The selected bed is already occupied.', 16, 1);
        RETURN;
    END

    -- Admit the patient
    INSERT INTO Admission (patient_id, room_number, bed_number, doctor_id, admission_date)
    VALUES (@patient_id, @room_number, @bed_number, @doctor_id, @admission_date);

    -- Update bed status
    UPDATE Bed
    SET is_occupied = 1
    WHERE room_number = @room_number 
    AND bed_number = @bed_number;
END;
GO

-- 5. Generate Bill
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

-- 6. Add Bill Item
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

-- 7. Discharge Patient
CREATE PROCEDURE DischargePatient
    @admission_id INT,
    @discharge_date DATE
AS
BEGIN
    UPDATE Admission SET discharge_date = @discharge_date WHERE admission_id = @admission_id;
END;
GO

-- 8. Get Patient History
CREATE PROCEDURE GetPatientHistory
    @patient_id INT
AS
BEGIN
    SELECT 
        mr.record_id,
        mr.visit_date,
        mr.diagnosis,
        mr.notes,
        CONCAT(d.first_name, ' ', d.last_name) as doctor_name,
        d.specialization
    FROM Medical_Record mr
    JOIN Doctor d ON mr.doctor_id = d.doctor_id
    WHERE mr.patient_id = @patient_id
    ORDER BY mr.visit_date DESC;
END;
GO

-- 9. Get Doctor Schedule
CREATE PROCEDURE GetDoctorSchedule
    @doctor_id INT,
    @start_date DATE,
    @end_date DATE
AS
BEGIN
    SELECT 
        a.appointment_id,
        a.appointment_date,
        a.status,
        CONCAT(p.first_name, ' ', p.last_name) as patient_name,
        p.contact_number
    FROM Appointment a
    JOIN Patient p ON a.patient_id = p.patient_id
    WHERE a.doctor_id = @doctor_id
    AND CAST(a.appointment_date AS DATE) BETWEEN @start_date AND @end_date
    ORDER BY a.appointment_date;
END;
GO

-- 10. Get Department Statistics
CREATE PROCEDURE GetDepartmentStatistics
    @department_id INT
AS
BEGIN
    SELECT 
        d.name as department_name,
        COUNT(DISTINCT doc.doctor_id) as total_doctors,
        COUNT(DISTINCT a.appointment_id) as total_appointments,
        COUNT(DISTINCT mr.record_id) as total_medical_records
    FROM Department d
    LEFT JOIN Doctor doc ON d.department_id = doc.department_id
    LEFT JOIN Appointment a ON doc.doctor_id = a.doctor_id
    LEFT JOIN Medical_Record mr ON doc.doctor_id = mr.doctor_id
    WHERE d.department_id = @department_id
    GROUP BY d.name;
END;
GO

-- User Management Stored Procedures
GO

CREATE PROCEDURE CreateUser
    @username VARCHAR(100),
    @password_hash VARCHAR(255),
    @role VARCHAR(50)
AS
BEGIN
    IF NOT EXISTS (SELECT 1 FROM Users WHERE username = @username)
    BEGIN
        INSERT INTO Users (username, password_hash, role)
        VALUES (@username, @password_hash, @role);
        RETURN 1; -- Success
    END
    RETURN 0; -- Username already exists
END;
GO

CREATE OR ALTER PROCEDURE AuthenticateUser
    @username VARCHAR(100),
    @password_hash VARCHAR(255)
AS
BEGIN
    SELECT user_id, username, role
    FROM Users
    WHERE username = @username AND password_hash = @password_hash;
END;
GO

CREATE OR ALTER PROCEDURE CheckUsernameExists
    @username VARCHAR(100)
AS
BEGIN
    SELECT COUNT(*) as exists_count
    FROM Users
    WHERE username = @username;
END;
GO

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
    INNER JOIN inserted i ON b.room_number = i.room_number AND b.bed_number = i.bed_number;
END;
GO

-- 2. Trigger: Free bed on discharge
CREATE OR ALTER TRIGGER trg_ReleaseBedOnDischarge
ON Admission
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE b
    SET b.is_occupied = 0
    FROM Bed b
    INNER JOIN inserted i ON b.room_number = i.room_number AND b.bed_number = i.bed_number
    INNER JOIN deleted d ON i.admission_id = d.admission_id
    WHERE d.discharge_date IS NULL AND i.discharge_date IS NOT NULL;
END;
GO

-- 3. Trigger: Prevent double booking of appointments
CREATE OR ALTER TRIGGER trg_PreventDoubleBooking
ON Appointment
AFTER INSERT, UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    IF EXISTS (
        SELECT 1
        FROM inserted i
        JOIN Appointment a ON i.doctor_id = a.doctor_id
        WHERE a.appointment_id != i.appointment_id
        AND a.appointment_date = i.appointment_date
        AND a.status != 'cancelled'
    )
    BEGIN
        RAISERROR('This time slot is already booked for the doctor.', 16, 1);
        ROLLBACK TRANSACTION;
    END
END;
GO
