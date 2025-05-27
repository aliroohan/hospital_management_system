INSERT INTO Department (DepartmentName) VALUES ('Cardiology'), ('Neurology');
INSERT INTO Patient (FirstName, LastName, DOB, Gender, Phone, Address)
VALUES ('John', 'Doe', '1990-05-15', 'M', '1234567890', '123 Main St'),
       ('Jane', 'Smith', '1985-03-22', 'F', '0987654321', '456 Oak Ave');
INSERT INTO Doctor (FirstName, LastName, Specialty, Phone, DepartmentID)
VALUES ('Alice', 'Brown', 'Cardiologist', '1112223333', 1),
       ('Bob', 'Wilson', 'Neurologist', '4445556666', 2);
INSERT INTO Room (RoomNumber, RoomType, MaxBeds) VALUES ('101', 'General', 4), ('201', 'ICU', 2);
INSERT INTO Bed (RoomID, BedNumber) VALUES (1, 'B1'), (1, 'B2'), (2, 'B1');