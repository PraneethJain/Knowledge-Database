import asyncio
import aiomysql
import os


class DatabaseConnector:
    def __init__(
        self,
        user_name: str,
        database_name: str,
    ) -> None:
        self.database_name = database_name
        self.user_name = user_name

    async def _init(self):
        self._conn = await aiomysql.connect(
            host="127.0.0.1",
            port=3306,
            user=self.user_name,
            password=os.environ["MYSQLPASS"],
            db=self.database_name
        )
        self.cur = await self._conn.cursor()
        if (len(await self.get_table_names()) == 0):
            await self.create_and_populate()

    async def execute(self, query: str):
        await self.cur.execute(query)
        self.description = self.cur.description

    async def fetchall(self):
        rc = await self.cur.fetchall()
        await self._conn.commit()
        return rc
    
    async def create_and_populate(self):
        # TO DO

        pass
    
    async def get_table_names(self):
        await self.execute("SHOW TABLES")
        return [r[0] for r in list(await self.fetchall())]

    async def get_primary_key(self, table: str) -> list[str]:
        return [
            result[0]
            for result in filter(
                lambda result: result[3] == "PRI", await self.table_desc(table)
            )
        ]

    async def display_query(self, table: str) -> tuple[tuple, ...]:
        query_string = f"SELECT * FROM {table}"
        print(query_string)
        await self.execute(query_string)
        return await self.fetchall()

    async def insert_query(self, table: str, query_attrs: list[str | None]) -> None:
        query_string = f'INSERT INTO {table} VALUES ({', '.join(map(lambda attr: f"'{attr}'" if attr is not None else "NULL", query_attrs))})'
        print(query_string)
        await self.execute(query_string)
        return await self.fetchall()

    async def delete_query(self, table: str, query_attrs: list[str | None]):
        readcount = await self.get_read_count(table, query_attrs)
        if (readcount == 0):
            raise Exception("No tuple with the given attributes found!")
        keys_list = await self.get_primary_key(table)
        query_string = f'DELETE FROM {table} WHERE {" AND ".join([f"{key}='{attr}'" for key, attr in zip(keys_list, query_attrs)])}'
        print(query_string)
        await self.execute(query_string)
        print(self.description)
        rc = await self.fetchall()

    async def update_query(
        self, table: str, query_attrs: list[str | None], update_tuple: tuple[str, str | None]
    ):
        readcount = await self.get_read_count(table, query_attrs)
        if (readcount == 0):
            raise Exception("No tuple with the given attributes found!")
        keys_list = await self.get_primary_key(table)
        query_string = f'UPDATE {table} SET {update_tuple[0]}={f'"{update_tuple[1]}"' if update_tuple[1] is not None else "NULL"} WHERE {" AND ".join([f"{key}='{attr}'" for key, attr in zip(keys_list, query_attrs)])}'
        print(query_string)
        await self.execute(query_string)
        print(self.description)
        return await self.fetchall()

    async def table_desc(self, table: str) -> list[tuple]:
        query_string = f"DESC {table}"
        await self.execute(query_string)
        results = await self.fetchall()
        return results

    async def get_table_headers(self, table: str) -> list[str]:
        return [result[0] for result in await self.table_desc(table)]
    
    async def get_read_count(self, table: str, query_attrs: list[str | None]) -> int:
        keys_list = await self.get_primary_key(table)
        query_string = f'SELECT * FROM {table} WHERE {" AND ".join([f"{key}='{attr}'" for key, attr in zip(keys_list, query_attrs)])}'
        await self.execute(query_string)
        Results = list(await self.fetchall())
        return len(Results)


    async def last_year_awards(self) -> list[tuple]:
        await self.execute("select * from Award WHERE YEAR(Date)=YEAR(CURDATE())")
        Results = list(await self.fetchall())
        Results.insert(0, tuple(await self.get_table_headers("Award")))
        return Results

    async def get_prerequisites(self, topic_name: str) -> list[tuple]:
        await self.execute(f"SELECT e.Name FROM Subtopic AS e INNER JOIN Subtopic eh ON eh.Name = e.Prerequisite_of_Name WHERE eh.Name='{topic_name}'")
        Results = list(await self.fetchall())
        Results.insert(0, ("Name",))
        return Results

    async def get_citations(self):
        await self.execute("select SSN, Count(CitedByPubID) FROM Person INNER JOIN Publication AS P ON P.PubID = Published GROUP BY SSN")
        Results = list(await self.fetchall())
        Results.insert(0, ("SSN", "Count of Citations"))
        return Results

    async def get_university_by_pref(self, pref: str) -> list[tuple]:
        await self.execute(f"select * from University where Name like '{pref}%'")
        Results = list(await self.fetchall())
        Results.insert(0, tuple(await self.get_table_headers("University")))
        return Results

    async def get_awards_university_aos(self, university: str) -> list[tuple]:
        await self.execute(f"select Subtopic_Name, COUNT(Sponsor) FROM Teaches AS T INNER JOIN Award AS A ON A.P_SSN=T.P_SSN WHERE U_Name='{university}' GROUP BY U_Name, Subtopic_Name")
        Results = list(await self.fetchall())
        Results.insert(0, ("Subtopic_Name", "Number of Awards"))
        return Results

    async def get_city_university(self, city: str) -> list[tuple]:
        await self.execute(f"select * from University where Location_City='{city}'")
        Results = list(await self.fetchall())
        Results.insert(0, tuple(await self.get_table_headers("University")))
        return Results

    async def get_accreditations(self, uname: str) -> list[tuple]:
        await self.execute(f"select Accreditation from University_Accreditations WHERE Name='{uname}'")
        Results = list(await self.fetchall())
        Results.insert(0, ("Accreditations",))
        return Results

    async def close(self) -> None:
        await self.cur.close()
        await self._conn.commit()
        self._conn.close()


async def create_connector(user_name: str, database_name: str) -> DatabaseConnector:
    DBConnect = DatabaseConnector(user_name, database_name)
    await DBConnect._init()
    return DBConnect


async def test():
    conn = await create_connector("root", "dnaproject")
    # await conn.insert_query('Location', ['a', 'b'])
    # cur = await conn.get_primary_key('award')
    # cur = await conn.delete_query('subtopic', ['Number Theory'])
    # cur = await conn.insert_query(
    #     "award",
    #     [
    #         "123466789",
    #         "Outstanding Researcher Award",
    #         "5",
    #         "6",
    #         "2021",
    #         "10000",
    #         "Research",
    #     ],
    # )
    
    cur = await conn.update_query(
        "Location",
        [
            'a',
        ],
        ('Location_Country', 'Banana')
    )
    # cur = await conn.get_primary_key('Subtopic')
    # cur = await conn.get_awards_university_aos("bard college berlin")
    cur = await conn.display_query("Location")
    print(cur)

    await conn.close()


if __name__ == "__main__":
    asyncio.run(test())
