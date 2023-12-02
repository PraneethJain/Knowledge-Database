CREATE TABLE `Area_of_Study` (
  `Name` varchar(32) PRIMARY KEY,
  `Description` varchar(1024),
  `Founding_Date` DATE NOT NULL
);

CREATE TABLE `Publication` (
  `PubID` integer PRIMARY KEY,
  `Title` varchar(64) NOT NULL,
  `Content` varchar(255) NOT NULL,
  `Date_of_Publishing` DATE NOT NULL,
  `Publishing_Journal_Name` varchar(32) NOT NULL,
  `CitedByPubID` integer
);

CREATE TABLE `Person` (
  `SSN` integer PRIMARY KEY,
  `Date_of_Birth` DATE NOT NULL,
  `Age` integer NOT NULL,
  `Nationality` varchar(32),
  `Super_SSN` integer,
  `Published` integer
);

CREATE TABLE `University` (
  `Name` varchar(64) PRIMARY KEY,
  `Location_City` varchar(32) NOT NULL,
  `Founding_Date` DATE NOT NULL
);

CREATE TABLE `Location` (
  `Location_City` varchar(32) PRIMARY KEY,
  `Location_Country` varchar(32) NOT NULL
);

CREATE TABLE `University_Acronyms` (
  `Name` varchar(64),
  `Acronym` varchar(32),
  PRIMARY KEY (`Name`, `Acronym`)
);

CREATE TABLE `University_Accreditations` (
  `Name` varchar(64),
  `Accreditation` varchar(32),
  PRIMARY KEY (`Name`, `Accreditation`)
);

CREATE TABLE `Book` (
  `BookID` integer PRIMARY KEY,
  `Book_Name` varchar(32) NOT NULL,
  `Publisher_Name` varchar(32) NOT NULL,
  `Edition_Number` integer
);

CREATE TABLE `Award` (
  `P_SSN` integer,
  `Name` varchar(32) NOT NULL,
  `Date` DATE NOT NULL,
  `Prize_Money` integer NOT NULL,
  `Sponsor` varchar(16),
  PRIMARY KEY (`P_SSN`, `Name`, `Date`)
);

CREATE TABLE `Event` (
  `U_Name` varchar(64) UNIQUE NOT NULL,
  `EventID` integer,
  `Date` DATE NOT NULL,
  `Venue_Building` varchar(32),
  `Venue_City` varchar(32),
  `Name` varchar(32),
  PRIMARY KEY (`EventID`)
);

CREATE TABLE `Subtopic` (
  `AoS_Name` varchar(32),
  `Name` varchar(32) PRIMARY KEY,
  `Description` varchar(1024),
  `Application` varchar(32),
  `Prerequisite_of_Name` varchar(32),
  `BookID` integer
);

CREATE TABLE `Researches` (
  `P_SSN` integer,
  `Subtopic_Name` varchar(32),
  `University_Name` varchar(64),
  PRIMARY KEY (`P_SSN`, `Subtopic_Name`, `University_Name`)
);

CREATE TABLE `Organizes` (
  `EventID` integer,
  `University_Name` varchar(64),
  `Subtopic_Name` varchar(32),
  PRIMARY KEY (`EventID`, `University_Name`, `Subtopic_Name`)
);

CREATE TABLE `Writes` (
  `P_SSN` integer,
  `BookID` integer,
  `Subtopic_Name` varchar(32),
  PRIMARY KEY (`P_SSN`, `BookID`, `Subtopic_Name`)
);

CREATE TABLE `Teaches` (
  `Subtopic_Name` varchar(32),
  `U_Name` varchar(64),
  `P_SSN` integer,
  `BookID` integer,
  PRIMARY KEY (`Subtopic_Name`, `U_Name`, `P_SSN`, `BookID`)
);

ALTER TABLE `University_Acronyms` ADD FOREIGN KEY (`Name`) REFERENCES `University` (`Name`);

ALTER TABLE `University_Accreditations` ADD FOREIGN KEY (`Name`) REFERENCES `University` (`Name`);

ALTER TABLE `University` ADD FOREIGN KEY (`Location_City`) REFERENCES `Location` (`Location_City`);

ALTER TABLE `Award` ADD FOREIGN KEY (`P_SSN`) REFERENCES `Person` (`SSN`);

ALTER TABLE `Event` ADD FOREIGN KEY (`U_Name`) REFERENCES `University` (`Name`);

ALTER TABLE `Subtopic` ADD FOREIGN KEY (`AoS_Name`) REFERENCES `Area_of_Study` (`Name`);

ALTER TABLE `Person` ADD FOREIGN KEY (`Super_SSN`) REFERENCES `Person` (`SSN`);

ALTER TABLE `Subtopic` ADD FOREIGN KEY (`Prerequisite_of_Name`) REFERENCES `Subtopic` (`Name`);

ALTER TABLE `Subtopic` ADD FOREIGN KEY (`BookID`) REFERENCES `Book` (`BookID`);

ALTER TABLE `Publication` ADD FOREIGN KEY (`CitedByPubID`) REFERENCES `Publication` (`PubID`);

ALTER TABLE `Person` ADD FOREIGN KEY (`Published`) REFERENCES `Publication` (`PubID`);

ALTER TABLE `Researches` ADD FOREIGN KEY (`P_SSN`) REFERENCES `Person` (`SSN`);

ALTER TABLE `Researches` ADD FOREIGN KEY (`Subtopic_Name`) REFERENCES `Subtopic` (`Name`);

ALTER TABLE `Researches` ADD FOREIGN KEY (`University_Name`) REFERENCES `University` (`Name`);

ALTER TABLE `Organizes` ADD FOREIGN KEY (`EventID`) REFERENCES `Event` (`EventID`);

ALTER TABLE `Organizes` ADD FOREIGN KEY (`University_Name`) REFERENCES `University` (`Name`);

ALTER TABLE `Organizes` ADD FOREIGN KEY (`Subtopic_Name`) REFERENCES `Subtopic` (`Name`);

ALTER TABLE `Writes` ADD FOREIGN KEY (`P_SSN`) REFERENCES `Person` (`SSN`);

ALTER TABLE `Writes` ADD FOREIGN KEY (`BookID`) REFERENCES `Book` (`BookID`);

ALTER TABLE `Writes` ADD FOREIGN KEY (`Subtopic_Name`) REFERENCES `Subtopic` (`Name`);

ALTER TABLE `Teaches` ADD FOREIGN KEY (`Subtopic_Name`) REFERENCES `Subtopic` (`Name`);

ALTER TABLE `Teaches` ADD FOREIGN KEY (`U_Name`) REFERENCES `University` (`Name`);

ALTER TABLE `Teaches` ADD FOREIGN KEY (`P_SSN`) REFERENCES `Person` (`SSN`);

ALTER TABLE `Teaches` ADD FOREIGN KEY (`BookID`) REFERENCES `Book` (`BookID`);
