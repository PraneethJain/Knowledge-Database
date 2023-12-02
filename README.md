# Knowledge-Database
A database to store information about knowledge.

# Team Info
- **Number**: 29
- **Name**: long long int
- Members: [Moida Praneeth Jain](https://github.com/PraneethJain)(2022101093), [Mohammed Faisal](https://github.com/JerseysGet)(2022101101), [Harshvardhan Rana](https://github.com/harshvardhanrana)(2022101095), [Divyansh Jain](https://github.com/divyansh1702)(2022101125)

# List of Tables
- Area_of_Study: A broad field of study.
- Subtopic: A specific field of study.
- Award: Contains relevant information about awards.
- Book: Contains book publisher and edition.
- Event: Contains relevant event details.
- Location: City to country mappings.
- Organizes: University organizing an event on a subtopic.
- Person: Contains relevant person information.
- Publication: Papers published by a person on a topic and their citations.
- Researches: Person researching subtopic at a university.
- Teaches: Person teaching a subtopic at a university using a book.
- University: Contains relevant university details.
- University_Accreditations: Contains the list of accreditations of a university.
- University_Acronyms: Contains the list of acronyms of a university.
- Writes: Person writes a book on a subtopic.

# List of Commands
## Generic Commands
These apply to all the tables individually
- Insert
- Update
- Delete

## Advanced Queries
These are queried upon multiple tables and model our functional requirements.
- **Last Year Awards**: Get information of all the awards awarded within the past year.
- **Get Prerequisites**: Get the list of immediate prerequisites of any given subtopic.
- **Get Citations**: Get the count of citations of every person.
- **Get University**: Searches for a university given any prefix of the university name.
- **Get Awards University**: Get the awards won by the researches of any given univeristy.
