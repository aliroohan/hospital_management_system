CREATE DATABASE HospitalManagement;
GO
USE HospitalManagement;
GO

-- Department Table
CREATE TABLE Department (
    DepartmentID INT IDENTITY(1,1) PRIMARY KEY,
    DepartmentName NVARCHAR(50) NOT NULL
);

-- Patient Table
CREATE TABLE Patient (
    PatientID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    DOB DATE NOT NULL,
    Gender CHAR(1) CHECK (Gender IN ('M', 'F', 'O')),
    Phone NVARCHAR(15),
    Address NVARCHAR(100)
);

-- Doctor Table
CREATE TABLE Doctor (
    DoctorID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Specialty NVARCHAR(50) NOT NULL,
    Phone NVARCHAR(15),
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

-- Appointment Table
CREATE TABLE Appointment (
    AppointmentID INT IDENTITY(1,1) PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    AppointmentDate DATETIME NOT NULL,
    Status NVARCHAR(20) CHECK (Status IN ('Scheduled', 'Completed', 'Cancelled')) DEFAULT 'Scheduled',
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

-- MedicalRecord Table
CREATE TABLE MedicalRecord (
    RecordID INT IDENTITY(1,1) PRIMARY KEY,
    PatientID INT,
    DoctorID INT,
    Diagnosis NVARCHAR(MAX) NOT NULL,
    Treatment NVARCHAR(MAX),
    RecordDate DATE NOT NULL,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (DoctorID) REFERENCES Doctor(DoctorID)
);

-- Bill Table
CREATE TABLE Bill (
    BillID INT IDENTITY(1,1) PRIMARY KEY,
    PatientID INT,
    Amount DECIMAL(10, 2) NOT NULL,
    BillDate DATE NOT NULL,
    Status NVARCHAR(20) CHECK (Status IN ('Paid', 'Pending')) DEFAULT 'Pending',
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID)
);

-- Staff Table
CREATE TABLE Staff (
    StaffID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(50) NOT NULL,
    LastName NVARCHAR(50) NOT NULL,
    Role NVARCHAR(50) NOT NULL,
    DepartmentID INT,
    FOREIGN KEY (DepartmentID) REFERENCES Department(DepartmentID)
);

-- Room Table
CREATE TABLE Room (
    RoomID INT IDENTITY(1,1) PRIMARY KEY,
    RoomNumber NVARCHAR(10) NOT NULL,
    RoomType NVARCHAR(20) CHECK (RoomType IN ('General', 'ICU', 'Private')) NOT NULL,
    MaxBeds INT NOT NULL CHECK (MaxBeds > 0),
    Status NVARCHAR(20) CHECK (Status IN ('Occupied', 'Available', 'Partially Occupied')) DEFAULT 'Available'
);

-- Bed Table
CREATE TABLE Bed (
    BedID INT IDENTITY(1,1) PRIMARY KEY,
    RoomID INT,
    BedNumber NVARCHAR(10) NOT NULL,
    Status NVARCHAR(20) CHECK (Status IN ('Occupied', 'Available')) DEFAULT 'Available',
    FOREIGN KEY (RoomID) REFERENCES Room(RoomID)
);

-- Admission Table
CREATE TABLE Admission (
    AdmissionID INT IDENTITY(1,1) PRIMARY KEY,
    PatientID INT,
    BedID INT,
    AdmissionDate DATE NOT NULL,
    DischargeDate DATE,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID),
    FOREIGN KEY (BedID) REFERENCES Bed(BedID)
);

-- AuditLog Table
CREATE TABLE AuditLog (
    LogID INT IDENTITY(1,1) PRIMARY KEY,
    LogMessage NVARCHAR(MAX),
    LogDate DATETIME
);

-- Stored Procedures
GO
CREATE PROCEDURE AddPatient
    @FirstName NVARCHAR(50),
    @LastName NVARCHAR(50),
    @DOB DATE,
    @Gender CHAR(1),
    @Phone NVARCHAR(15),
    @Address NVARCHAR(100)
AS
BEGIN
    INSERT INTO Patient (FirstName, LastName, DOB, Gender, Phone, Address)
    VALUES (@FirstName, @LastName, @DOB, @Gender, @Phone, @Address);
END;
GO

CREATE PROCEDURE ScheduleAppointment
    @PatientID INT,
    @DoctorID INT,
    @AppointmentDate DATETIME
AS
BEGIN
    INSERT INTO Appointment (PatientID, DoctorID, AppointmentDate, Status)
    VALUES (@PatientID, @DoctorID, @AppointmentDate, 'Scheduled');
END;
GO

CREATE PROCEDURE CancelAppointment
    @AppointmentID INT
AS
BEGIN
    UPDATE Appointment
    SET Status = 'Cancelled'
    WHERE AppointmentID = @AppointmentID;
END;
GO

CREATE PROCEDURE AddMedicalRecord
    @PatientID INT,
    @DoctorID INT,
    @Diagnosis NVARCHAR(MAX),
    @Treatment NVARCHAR(MAX),
    @RecordDate DATE
AS
BEGIN
    INSERT INTO MedicalRecord (PatientID, DoctorID, Diagnosis, Treatment, RecordDate)
    VALUES (@PatientID, @DoctorID, @Diagnosis, @Treatment, @RecordDate);
END;
GO

CREATE PROCEDURE GenerateBill
    @PatientID INT,
    @Amount DECIMAL(10, 2),
    @BillDate DATE
AS
BEGIN
    INSERT INTO Bill (PatientID, Amount, BillDate, Status)
    VALUES (@PatientID, @Amount, @BillDate, 'Pending');
END;
GO

CREATE PROCEDURE MarkBillPaid
    @BillID INT
AS
BEGIN
    UPDATE Bill
    SET Status = 'Paid'
    WHERE BillID = @BillID;
END;
GO

CREATE PROCEDURE AdmitPatient
    @PatientID INT,
    @BedID INT,
    @AdmissionDate DATE
AS
BEGIN
    INSERT INTO Admission (PatientID, BedID, AdmissionDate)
    VALUES (@PatientID, @BedID, @AdmissionDate);
    UPDATE Bed SET Status = 'Occupied' WHERE BedID = @BedID;
    UPDATE Room
    SET Status = CASE
        WHEN (SELECT COUNT(*) FROM Bed WHERE RoomID = Room.RoomID AND Status = 'Occupied') = MaxBeds THEN 'Occupied'
        WHEN (SELECT COUNT(*) FROM Bed WHERE RoomID = Room.RoomID AND Status = 'Occupied') > 0 THEN 'Partially Occupied'
        ELSE 'Available'
    END
    WHERE RoomID = (SELECT RoomID FROM Bed WHERE BedID = @BedID);
END;
GO

CREATE PROCEDURE DischargePatient
    @AdmissionID INT,
    @DischargeDate DATE
AS
BEGIN
    DECLARE @BedID INT;
    DECLARE @RoomID INT;
    SELECT @BedID = BedID, @RoomID = (SELECT RoomID FROM Bed WHERE BedID = Admission.BedID)
    FROM Admission WHERE AdmissionID = @AdmissionID;
    UPDATE Admission
    SET DischargeDate = @DischargeDate
    WHERE AdmissionID = @AdmissionID;
    UPDATE Bed SET Status = 'Available' WHERE BedID = @BedID;
    UPDATE Room
    SET Status = CASE
        WHEN (SELECT COUNT(*) FROM Bed WHERE RoomID = @RoomID AND Status = 'Occupied') = MaxBeds THEN 'Occupied'
        WHEN (SELECT COUNT(*) FROM Bed WHERE RoomID = @RoomID AND Status = 'Occupied') > 0 THEN 'Partially Occupied'
        ELSE 'Available'
    END
    WHERE RoomID = @RoomID;
END;
GO

CREATE PROCEDURE GetAvailableBeds
AS
BEGIN
    SELECT B.BedID, B.BedNumber, R.RoomNumber, R.RoomType
    FROM Bed B
    JOIN Room R ON B.RoomID = R.RoomID
    WHERE B.Status = 'Available';
END;
GO

CREATE PROCEDURE AddBed
    @RoomID INT,
    @BedNumber NVARCHAR(10)
AS
BEGIN
    DECLARE @bed_count INT;
    DECLARE @max_beds INT;
    SELECT @bed_count = COUNT(*), @max_beds = MaxBeds
    FROM Bed B
    JOIN Room R ON B.RoomID = R.RoomID
    WHERE B.RoomID = @RoomID
    GROUP BY MaxBeds;
    IF @bed_count >= @max_beds
        THROW 50001, 'Room has reached maximum bed capacity', 1;
    INSERT INTO Bed (RoomID, BedNumber, Status)
    VALUES (@RoomID, @BedNumber, 'Available');
END;
GO

-- Triggers
GO
CREATE TRIGGER PreventPastAppointments
ON Appointment
AFTER INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted WHERE AppointmentDate < GETDATE())
    BEGIN
        THROW 50002, 'Cannot schedule appointments in the past', 1;
        ROLLBACK;
    END
END;
GO

CREATE TRIGGER UpdateBedStatusOnAdmission
ON Admission
AFTER INSERT
AS
BEGIN
    DECLARE @RoomID INT;
    SELECT @RoomID = RoomID FROM Bed WHERE BedID = (SELECT BedID FROM inserted);
    UPDATE Bed SET Status = 'Occupied' WHERE BedID = (SELECT BedID FROM inserted);
    UPDATE Room
    SET Status = CASE
        WHEN (SELECT COUNT(*) FROM Bed WHERE RoomID = @RoomID AND Status = 'Occupied') = MaxBeds THEN 'Occupied'
        WHEN (SELECT COUNT(*) FROM Bed WHERE RoomID = @RoomID AND Status = 'Occupied') > 0 THEN 'Partially Occupied'
        ELSE 'Available'
    END
    WHERE RoomID = @RoomID;
END;
GO

CREATE TRIGGER PreventBedOverbooking
ON Admission
INSTEAD OF INSERT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM inserted i JOIN Bed b ON i.BedID = b.BedID WHERE b.Status = 'Occupied')
    BEGIN
        THROW 50003, 'Bed is already occupied', 1;
    END
    ELSE
    BEGIN
        INSERT INTO Admission (PatientID, BedID, AdmissionDate, DischargeDate)
        SELECT PatientID, BedID, AdmissionDate, DischargeDate
        FROM inserted;
    END
END;
GO

CREATE TRIGGER LogMedicalRecordCreation
ON MedicalRecord
AFTER INSERT
AS
BEGIN
    INSERT INTO AuditLog (LogMessage, LogDate)
    SELECT 'Medical Record created for PatientID ' + CAST(PatientID AS NVARCHAR(10)), GETDATE()
    FROM inserted;
END;
GO