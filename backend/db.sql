CREATE TABLE ReliefCamp (
    camp_id INT PRIMARY KEY,
    camp_name VARCHAR(100) NOT NULL,
    location VARCHAR(255) NOT NULL,
    capacity INT NOT NULL,
    contact_person VARCHAR(100)
);

INSERT INTO ReliefCamp VALUES
(1, 'Delhi Flood Relief Camp', 'New Delhi', 500, 'Rajesh Verma'),
(2, 'Mumbai Cyclone Shelter', 'Mumbai', 350, 'Pooja Sharma'),
(3, 'Kolkata Flood Relief', 'Kolkata', 400, 'Anil Mehta'),
(4, 'Chennai Tsunami Shelter', 'Chennai', 300, 'Suresh Kumar'),
(5, 'Assam Flood Relief', 'Guwahati', 450, 'Neha Das'),
(6, 'Bihar Flood Camp', 'Patna', 600, 'Arun Mishra'),
(7, 'Uttarakhand Earthquake Relief', 'Dehradun', 200, 'Vikram Joshi'),
(8, 'Rajasthan Drought Relief', 'Jaipur', 350, 'Priya Singh'),
(9, 'Odisha Cyclone Shelter', 'Bhubaneswar', 400, 'Ravi Nair'),
(10, 'Kerala Monsoon Relief', 'Thiruvananthapuram', 500, 'Asha Menon');


CREATE TABLE VictimSurvivor (
    victim_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    contact_no VARCHAR(15),
    address VARCHAR(255),
    camp_id INT,
    FOREIGN KEY (camp_id) REFERENCES ReliefCamp(camp_id)
);

INSERT INTO VictimSurvivor VALUES
(1, 'Amit', 'Sharma', '1990-03-15', '9876543210', 'Delhi', 1),
(2, 'Priya', 'Singh', '1985-07-10', '9988776655', 'Mumbai', 2),
(3, 'Ravi', 'Kumar', '1992-06-21', '9123456789', 'Kolkata', 3),
(4, 'Sunita', 'Das', '1988-12-11', '9212345678', 'Chennai', 4),
(5, 'Rajesh', 'Yadav', '1995-02-28', '9198765432', 'Guwahati', 5),
(6, 'Neha', 'Mishra', '1987-05-19', '9876123450', 'Patna', 6),
(7, 'Manoj', 'Verma', '1991-08-14', '9898989898', 'Dehradun', 7),
(8, 'Meena', 'Nair', '1993-09-25', '9009009009', 'Jaipur', 8),
(9, 'Vikash', 'Patil', '1989-01-30', '9192929292', 'Bhubaneswar', 9),
(10, 'Deepa', 'Menon', '1996-04-17', '9080706050', 'Thiruvananthapuram', 10);


CREATE TABLE Inventory (
    item_id INT PRIMARY KEY,
    item_name VARCHAR(255),
    camp_id INT,
    quantity INT NOT NULL,
    date_received DATE NOT NULL,
    FOREIGN KEY (camp_id) REFERENCES ReliefCamp(camp_id)
);

INSERT INTO Inventory (item_id, item_name, camp_id, quantity, date_received) VALUES
(201, 'Rice Bags', 1, 500, '2024-02-01'),
(202, 'Medicines', 2, 200, '2024-02-02'),
(203, 'Water Bottles', 3, 1000, '2024-02-03'),
(204, 'Blankets', 1, 300, '2024-02-04'),
(205, 'Dry Food Packets', 4, 600, '2024-02-05'),
(206, 'First Aid Kits', 5, 150, '2024-02-06'),
(207, 'Baby Food', 2, 120, '2024-02-07'),
(208, 'Cooked Meals', 6, 800, '2024-02-08'),
(209, 'Sanitary Kits', 7, 250, '2024-02-09'),
(210, 'Blood Units', 3, 90, '2024-02-10');


CREATE TABLE Donor (
    donor_id INT PRIMARY KEY,
    donor_name VARCHAR(255),
    item_id INT,
    quantity INT,
    date_donated DATE,
    FOREIGN KEY (item_id) REFERENCES Inventory(item_id)
);

INSERT INTO Donor VALUES
(101, 'Tata Trusts', 201, 200, '2024-02-01'),
(102, 'Reliance Foundation', 202, 150, '2024-02-02'),
(103, 'Akshaya Patra Foundation', 203, 500, '2024-02-03'),
(104, 'Goonj NGO', 204, 250, '2024-02-04'),
(105, 'HDFC Bank CSR', 205, 400, '2024-02-05'),
(106, 'Red Cross India', 206, 100, '2024-02-06'),
(107, 'Amazon India Relief', 207, 80, '2024-02-07'),
(108, 'ISCKON Food Relief', 208, 600, '2024-02-08'),
(109, 'P&G Hygiene Initiative', 209, 180, '2024-02-09'),
(110, 'Apollo Blood Bank', 210, 50, '2024-02-10');


CREATE TABLE Donation (
    donation_id INT PRIMARY KEY,
    donor_id INT,
    item_id INT,
    quantity INT,
    date_donated DATE,
    FOREIGN KEY (donor_id) REFERENCES Donor(donor_id),
    FOREIGN KEY (item_id) REFERENCES Inventory(item_id)
);

INSERT INTO Donation VALUES
(301, 101, 201, 200, '2024-02-01'),
(302, 102, 202, 150, '2024-02-02'),
(303, 103, 203, 500, '2024-02-03'),
(304, 104, 204, 250, '2024-02-04'),
(305, 105, 205, 400, '2024-02-05'),
(306, 106, 206, 100, '2024-02-06'),
(307, 107, 207, 80, '2024-02-07'),
(308, 108, 208, 600, '2024-02-08'),
(309, 109, 209, 180, '2024-02-09'),
(310, 110, 210, 50, '2024-02-10');


CREATE TABLE Supply (
    supply_id INT PRIMARY KEY,
    item_id INT,
    camp_id INT,
    quantity INT,
    date_received DATE,
    FOREIGN KEY (item_id) REFERENCES Inventory(item_id),
    FOREIGN KEY (camp_id) REFERENCES ReliefCamp(camp_id)
);

INSERT INTO Supply VALUES
(401, 201, 1, 200, '2024-02-02'),
(402, 202, 2, 150, '2024-02-03'),
(403, 203, 3, 500, '2024-02-04'),
(404, 204, 1, 250, '2024-02-05'),
(405, 205, 4, 400, '2024-02-06'),
(406, 206, 5, 100, '2024-02-07'),
(407, 207, 2, 80, '2024-02-08'),
(408, 208, 6, 600, '2024-02-09'),
(409, 209, 7, 180, '2024-02-10'),
(410, 210, 3, 50, '2024-02-11');


CREATE TABLE Volunteer (
    volunteer_id INT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    contact_number VARCHAR(15),
    skills VARCHAR(255)
);

INSERT INTO Volunteer VALUES
(401, 'Amit', 'Sharma', '9876543210', 'Medical Assistance'),
(402, 'Pooja', 'Devi', '9765432190', 'Logistics'),
(403, 'Ramesh', 'Kumar', '9988776655', 'Food Distribution'),
(404, 'Neha', 'Verma', '9898989898', 'Rescue Operations'),
(405, 'Vikas', 'Singh', '9123456789', 'Shelter Management'),
(406, 'Priya', 'Joshi', '9009009009', 'First Aid'),
(407, 'Manish', 'Das', '9198765432', 'Water Supply Distribution'),
(408, 'Anjali', 'Reddy', '9080706050', 'Child Care'),
(409, 'Karthik', 'Nair', '9876123450', 'Counseling'),
(410, 'Deepika', 'Menon', '9192929292', 'Sanitation Support');


CREATE TABLE VolunteerAssignment (
    assignment_id INT PRIMARY KEY,
    volunteer_id INT,
    camp_id INT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (volunteer_id) REFERENCES Volunteer(volunteer_id),
    FOREIGN KEY (camp_id) REFERENCES ReliefCamp(camp_id)
);

INSERT INTO VolunteerAssignment VALUES
(101, 401, 1, '2025-02-01', '2025-02-10'),
(102, 402, 2, '2025-02-02', '2025-02-12'),
(103, 403, 3, '2025-02-03', '2025-02-15'),
(104, 404, 4, '2025-02-04', '2025-02-14'),
(105, 405, 5, '2025-02-05', '2025-02-20'),
(106, 406, 6, '2025-02-06', '2025-02-25'),
(107, 407, 7, '2025-02-07', '2025-02-18'),
(108, 408, 8, '2025-02-08', '2025-02-22'),
(109, 409, 9, '2025-02-09', '2025-02-28'),
(110, 410, 10, '2025-02-10', '2025-02-27');


CREATE TABLE MissingPersonReport (
    report_id INT PRIMARY KEY,
    reporter_name VARCHAR(255),
    missing_person_name VARCHAR(255),
    last_seen_location VARCHAR(255),
    date_reported DATE,
    contact VARCHAR(15),
    camp_id INT,
    victim_id INT,
    FOREIGN KEY (camp_id) REFERENCES ReliefCamp(camp_id),
    FOREIGN KEY (victim_id) REFERENCES VictimSurvivor(victim_id)
);


INSERT INTO MissingPersonReport VALUES
(1, 'Amit Sharma', 'Rohit Sharma', 'New Delhi', '2025-02-01', '9876543210', 1, 1),
(2, 'Priya Singh', 'Neha Singh', 'Mumbai', '2025-02-02', '9988776655', 2, 2),
(3, 'Ravi Kumar', 'Suresh Kumar', 'Kolkata', '2025-02-03', '9123456789', 3, 3),
(4, 'Sunita Das', 'Anjali Das', 'Chennai', '2025-02-04', '9212345678', 4, 4),
(5, 'Rajesh Yadav', 'Ankit Yadav', 'Guwahati', '2025-02-05', '9198765432', 5, 5),
(6, 'Neha Mishra', 'Arjun Mishra', 'Patna', '2025-02-06', '9876123450', 6, 6),
(7, 'Manoj Verma', 'Kiran Verma', 'Dehradun', '2025-02-07', '9898989898', 7, 7),
(8, 'Meena Nair', 'Suraj Nair', 'Jaipur', '2025-02-08', '9009009009', 8, 8),
(9, 'Vikash Patil', 'Rahul Patil', 'Bhubaneswar', '2025-02-09', '9192929292', 9, 9),
(10, 'Deepa Menon', 'Kavita Menon', 'Thiruvananthapuram', '2025-02-10', '9080706050', 10, 10);




