from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, DataTable, ContentSwitcher, Footer, Input
from textual.containers import VerticalScroll, Horizontal, Vertical
from textual.screen import Screen

from db import create_connector, DatabaseConnector

ROWS = [
    ("lane", "swimmer", "country", "time"),
    (4, "Joseph Schooling", "Singapore", 50.39),
    (2, "Michael Phelps", "United States", 51.14),
    (5, "Chad le Clos", "South Africa", 51.14),
    (6, "László Cseh", "Hungary", 51.14),
    (3, "Li Zhuhao", "China", 51.26),
    (8, "Mehdy Metella", "France", 51.58),
    (7, "Tom Shields", "United States", 51.73),
    (1, "Aleksandr Sadovnikov", "Russia", 51.84),
    (10, "Darren Burns", "Scotland", 51.84),
]


class InputEntry(Screen):
    def __init__(
        self,
        fields: list[str],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.input_widgets = [Input(placeholder=field) for field in fields]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id is None:
            return

        match event.button.id:
            case "submit":
                # show status message and then close
                self.app.pop_screen()
            case "cancel":
                self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield from self.input_widgets
        yield Button("Submit", id="submit")
        yield Button("Cancel", id="cancel")


class TableSwitcher(Screen):
    def __init__(
        self,
        table_names: list[str],
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.table_names = table_names

    def compose(self) -> ComposeResult:
        with Horizontal(id="table-switcher"):
            with VerticalScroll(id="table-buttons"):
                for table_name in self.table_names:
                    yield Button(table_name, id=f"{table_name}-button")

            with ContentSwitcher(initial=self.table_names[0]):
                for table_name in self.table_names:
                    yield DataTable(id=table_name)

            with Vertical(id="operation-buttons"):
                yield Button("Insert", id="insert-button")
                yield Button("Update", id="update-button")
                yield Button("Delete", id="delete-button")

        yield (Footer())

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id is None:
            return

        switcher = self.query_one(ContentSwitcher)
        if switcher.current is None:
            return

        table_name = switcher.current
        attributes = await database.get_table_headers(table_name)
        primary_key_attributes = await database.get_primary_key(table_name)
        match event.button.id:
            case "insert-button":
                self.app.push_screen(InputEntry(attributes))
            case "update-button":
                self.app.push_screen(
                    InputEntry(
                        primary_key_attributes + ["Attribute Name", "Attribute Value"]
                    )
                )
            case "delete-button":
                self.app.push_screen(InputEntry(primary_key_attributes))
            case _:
                switcher.current = event.button.id[:-7]

    async def on_mount(self) -> None:
        for table_name in self.table_names:
            table = self.query_one(f"#{table_name}", DataTable)

            headers = await database.get_table_headers(table_name)
            table.add_columns(*headers)

            rows = await database.display_query(table_name)
            table.add_rows(rows)


class KnowledgeDatabase(App[None]):
    CSS_PATH = "KnowledgeDatabase.tcss"
    SCREENS = {}
    BINDINGS = [Binding("q", "quit", "Quit")]
    TITLE = "Knowledge Database"

    async def on_mount(self) -> None:
        global database
        database = await create_connector("praneeth", "dnaproject")
        table_names = await database.get_table_names()
        self.push_screen(TableSwitcher(table_names))


if __name__ == "__main__":
    database: DatabaseConnector
    KnowledgeDatabase().run()
