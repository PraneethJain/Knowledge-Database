--location table
INSERT INTO `Location` (`Location_City`, `Location_Country`) VALUES
('New York', 'USA'),
('London', 'UK'),
('Toronto', 'Canada'),
('Sydney', 'Australia'),
('Berlin', 'Germany');
-- university table
INSERT INTO `University` (`Name`, `Location_City`, `Founding_Date`) VALUES
('New york university', 'New York', '1950-05-02'),
('cambridge university', 'London', '1925-09-10'),
('mcgill university', 'Toronto', '1960-03-08'),
('University of sydney', 'Sydney', '1975-07-12'),
('bard college berlin', 'Berlin', '1900-11-04');
-- Populate Area_of_Study table
INSERT INTO `Area_of_Study` (`Name`, `Description`, `Founding_Date`) VALUES
('Computer Science', 'Study of computers and computational systems', '1990-01-01'),
('Physics', 'Study of matter, energy, and the fundamental forces of nature', '1920-05-15'),
('Biology', 'Study of living organisms and their interactions', '1955-09-30'),
('Mathematics', 'Study of numbers, quantities, and shapes', '1800-03-12'),
('History', 'Study of past events and their significance', '1900-11-20');
-- publication
INSERT INTO `Publication` (`PubID`, `Title`, `Content`, `Date_of_Publishing`, `Publishing_Journal_Name`, `CitedByPubID`) VALUES
(1, 'Introduction to Computer Science', 'A comprehensive guide to computer science basics', '2022-04-10', 'Computer Journal', NULL),
(2, 'Fundamentals of Physics', 'Exploring the principles of physics', '2021-07-05', 'Physics Today', NULL),
(3, 'The Biology Book', 'An overview of key concepts in biology', '2023-02-18', 'Nature Biology', NULL),
(4, 'Mathematical Foundations', 'Understanding core mathematical principles', '2019-11-30', 'Mathematics Review', NULL),
(5, 'History Revisited', 'Exploring historical events and their impact', '2020-08-22', 'Historical Review', NULL);
--person table
INSERT INTO `Person` (`SSN`, `Date_of_Birth`, `Age`, `Nationality`, `Super_SSN`, `Published`) VALUES
(123456789, '1985-06-15', 37, 'American', NULL, 1),
(234567890, '1990-02-28', 32, 'British', 123456789, 2),
(345678901, '1980-09-10', 42, 'Canadian', 123456789, 3),
(456789012, '1995-12-03', 28, 'Australian', NULL, 4),
(567890123, '1975-04-20', 47, 'German', NULL, 5);
--university acronyms
INSERT INTO `University_Acronyms` (`Name`, `Acronym`) VALUES
('New york university', 'NYU'),
('cambridge university', 'CU'),
('mcgill university', 'MU'),
('University of sydney', 'UOS'),
('bard college berlin', 'BCB');
-- University_Accreditations
INSERT INTO `University_Accreditations` (`Name`, `Accreditation`) VALUES
('New york university', 'ABET'),
('cambridge university', 'HEA'),
('mcgill university', 'AACSB'),
('University of sydney', 'EQUIS'),
('bard college berlin', 'WASC');
-- Populate Book table
INSERT INTO `Book` (`BookID`, `Book_Name`, `Publisher_Name`, `Edition_Number`) VALUES
(101, 'Computer Algorithms', 'Tech Books', 3),
(102, 'Physics in Action', 'Science Press', 2),
(103, 'Bioinformatics Basics', 'BioTech Publishing', 1),
(104, 'Advanced Mathematics', 'Math Publishers', 4),
(105, 'World History Chronicles', 'Historical Publications', 2);
-- Populate Award table
INSERT INTO `Award` (`P_SSN`, `Name`, `Date`, `Prize_Money`, `Sponsor`) VALUES
(123456789, 'Outstanding Researcher Award', '2021-06-05', 10000, 'Research'),
(234567890, 'Best Paper Award', '2022-10-12', 5000, 'Tech'),
(345678901, 'Innovation Excellence Prize', '2023-04-03', 15000, 'Innovate'),
(456789012, 'Young Scientist Award', '2020-09-08', 8000, 'Science'),
(567890123, 'Historical Achievement Award', '2019-07-11', 12000, 'History');
-- Populate Event table
INSERT INTO `Event` (`U_Name`, `EventID`, `Date`, `Venue_Building`, `Venue_City`, `Name`) VALUES
('New york university', 1, '2022-03-15', 'Conference Hall', 'New York', 'Tech Symposium'),
('cambridge university', 2, '2023-05-20', 'Lecture Theater', 'London', 'Physics Conference'),
('mcgill university', 3, '2021-09-10', 'Auditorium', 'Toronto', 'Biotechnology Expo'),
('University of sydney', 4, '2020-12-05', 'Seminar Room', 'Sydney', 'Mathematics Workshop'),
('bard college berlin', 5, '2019-06-08', 'History Museum', 'Berlin', 'Historical Symposium');
-- Populate Subtopic table
INSERT INTO `Subtopic` (`AoS_Name`, `Name`, `Description`, `Application`, `Prerequisite_of_Name`, `BookID`) VALUES
('Computer Science', 'Algorithm Design', 'Designing efficient algorithms for problem-solving', 'Software Development', NULL, 101),
('Physics', 'Quantum Mechanics', 'Study of the behavior of matter and energy at the quantum level', 'Quantum Computing', NULL, 102),
('Biology', 'Genetic Engineering', 'Manipulating genes to achieve desired traits', 'Biomedical Research', NULL, 103),
('Mathematics', 'Number Theory', 'Study of properties and relationships of numbers', 'Cryptography', NULL, 104),
('History', 'Ancient Civilizations', 'Exploring the cultures and societies of ancient times', 'Historical Research', NULL, 105),
('Mathematics', 'Linear Algebra', 'Studying vector spaces and linear transformations', 'Engineering', 'Quantum Mechanics', NULL),
('Mathematics', 'Calculus 2', 'Studying multivariate functions and their properties', 'Engineering', 'Quantum Mechanics', NULL),
('Mathematics', 'Calculus 1', 'Studying univariate functions and their properties', 'Engineering', 'Calculus 2', NULL);

-- researches table
INSERT INTO `Researches` (`P_SSN`, `Subtopic_Name`, `University_Name`)
VALUES
(123456789, 'Algorithm Design', 'New york university'),
(234567890, 'Quantum Mechanics', 'cambridge university'),
(345678901, 'Genetic Engineering', 'mcgill university'),
(456789012, 'Number Theory', 'University of sydney'),
(567890123, 'Ancient Civilizations', 'bard college berlin');

-- Populate Organizes table
INSERT INTO `Organizes` (`EventID`, `University_Name`, `Subtopic_Name`)
VALUES
(1, 'New york university', 'Algorithm Design'),
(2, 'cambridge university', 'Quantum Mechanics'),
(3, 'mcgill university', 'Genetic Engineering'),
(4, 'University of sydney', 'Number Theory'),
(5, 'bard college berlin', 'Ancient Civilizations');

-- Populate Writes table
INSERT INTO `Writes` (`P_SSN`, `BookID`, `Subtopic_Name`)
VALUES
(123456789, 101, 'Algorithm Design'),
(234567890, 102, 'Quantum Mechanics'),
(345678901, 103, 'Genetic Engineering'),
(456789012, 104, 'Number Theory'),
(567890123, 105, 'Ancient Civilizations');

-- Populate Teaches table
INSERT INTO `Teaches` (`Subtopic_Name`, `U_Name`, `P_SSN`, `BookID`)
VALUES
('Algorithm Design', 'New york university', 123456789, 101),
('Quantum Mechanics', 'cambridge university', 234567890, 102),
('Genetic Engineering', 'mcgill university', 345678901, 103),
('Number Theory', 'University of sydney', 456789012, 104),
('Ancient Civilizations', 'bard college berlin', 567890123, 105);