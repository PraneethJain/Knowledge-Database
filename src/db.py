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
            await create_and_populate(self)

    async def execute(self, query: str):
        await self.cur.execute(query)
        self.description = self.cur.description

    async def fetchall(self):
        return await self.cur.fetchall()
    
    async def create_and_populate(self):
        self.execute("")
    
    async def get_table_names(self):
        await self.execute("SHOW TABLES")
        return [r[0] for r in list(await self.fetchall())]

    async def get_primary_key(self, table: str) -> list[str]:
        try:
            return [
                result[0]
                for result in filter(
                    lambda result: result[3] == "PRI", await self.table_desc(table)
                )
            ]
        except Exception as E:
            print(E)

    async def display_query(self, table: str) -> tuple[tuple, ...]:
        query_string = f"SELECT * FROM {table}"
        print(query_string)
        try:
            await self.execute(query_string)
            return await self.fetchall()
        except Exception as E:
            print(E)

    async def insert_query(self, table: str, query_attrs: list[str | None]) -> None:
        query_string = f'INSERT INTO {table} VALUES ({', '.join(map(lambda attr: f"'{attr}'" if attr is not None else "NULL", query_attrs))})'
        print(query_string)
        try:
            await self.execute(query_string)
            return await self.fetchall()
        except Exception as E:
            print(E)

    async def delete_query(self, table: str, query_attrs: list[str | None]):
        keys_list = await self.get_primary_key(table)
        query_string = f'DELETE FROM {table} WHERE {" AND ".join([f"{key}='{attr}'" for key, attr in zip(keys_list, query_attrs)])}'
        print(query_string)
        try:
            await self.execute(query_string)
            print(self.description)
            return await self.fetchall()
        except Exception as E:
            print(E)

    async def update_query(
        self, table: str, query_attrs: list[str | None], update_tuple: (str, str | None)
    ):
        keys_list = await self.get_primary_key(table)
        query_string = f'UPDATE {table} SET {update_tuple[0]}={f'"{update_tuple[1]}"' if update_tuple[1] is not None else "NULL"} WHERE {" AND ".join([f"{key}='{attr}'" for key, attr in zip(keys_list, query_attrs)])}'
        print(query_string)
        try:
            await self.execute(query_string)
            print(self.description)
            return await self.fetchall()
        except Exception as E:
            print(E)

    async def table_desc(self, table: str) -> list[list[str]]:
        query_string = f"DESC {table}"
        try:
            await self.execute(query_string)
            results = await self.fetchall()
            return results
        except Exception as E:
            print(E)

    async def get_table_headers(self, table: str) -> list[str]:
        try:
            return [result[0] for result in await self.table_desc(table)]
        except Exception as E:
            print(E)

    async def last_year_awards(self) -> tuple[tuple, ...]:
        try:
            await self.execute("select * from Award WHERE YEAR(Date)=YEAR(CURDATE())")
            Results = list(await self.fetchall())
            Results.insert(0, tuple(await self.get_table_headers("Award")))
            return Results
        except Exception as E:
            print(E)

    async def get_prerequisites(self, topic_name: str) -> tuple[(str)]:
        try:
            await self.execute(f"SELECT e.Name FROM Subtopic AS e INNER JOIN Subtopic eh ON eh.Name = e.Prerequisite_of_Name WHERE eh.Name='{topic_name}'")
            Results = list(await self.fetchall())
            Results.insert(0, ("Name",))
            return Results
        except Exception as E:
            print(E)

    async def get_citations(self):
        try:
            await self.execute("select SSN, Count(CitedByPubID) FROM Person INNER JOIN Publication AS P ON P.PubID = Published GROUP BY SSN")
            Results = list(await self.fetchall())
            Results.insert(0, ("SSN", "Count of Citations"))
            return Results
        except Exception as E:
            print(E)

    async def get_university_by_pref(self, pref: str):
        try:
            await self.execute(f"select * from University where Name like '{pref}%'")
            Results = list(await self.fetchall())
            Results.insert(0, tuple(await self.get_table_headers("University")))
            return Results
        except Exception as E:
            print(E)

    async def get_awards_university_aos(self, university: str, aos: str):
        try:
            await self.execute(f"select U_Name, COUNT(Sponsor) FROM Teaches AS T INNER JOIN Award AS A ON A.P_SSN=T.P_SSN WHERE U_Name='{university}' AND Subtopic_Name='{aos}' GROUP BY U_Name")
            Results = list(await self.fetchall())
            Results.insert(0, ("U_Name", "Number of Awards"))
            return Results
        except Exception as E:
            print(E)

    async def close(self):
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
    
    # cur = await conn.update_query(
    #     "Location",
    #     [
    #         'a',
    #     ],
    #     ('Location_Country', 'Banana')
    # )
    # cur = await conn.get_primary_key('Subtopic')
    cur = await conn.get_awards_university_aos("bard college berlin", "Number Theory")
    print(cur)

    await conn.close()


if __name__ == "__main__":
    asyncio.run(test())
