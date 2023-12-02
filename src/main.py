from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, DataTable, ContentSwitcher, Footer, Input
from textual.containers import VerticalScroll, Horizontal, Vertical
from textual.screen import Screen

from db import create_connector, DatabaseConnector


class InputEntry(Screen):
    def __init__(
        self,
        fields: list[str],
        operation: str,
        table_name: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.input_widgets = [Input(placeholder=field) for field in fields]
        self.operation = operation
        self.table_name = table_name

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id is None:
            return

        print(event.button.id)
        match event.button.id:
            case "submit":
                match self.operation:
                    case "insert":
                        await database.insert_query(
                            self.table_name, [wid.value for wid in self.input_widgets]
                        )
                        print(
                            self.table_name, [wid.value for wid in self.input_widgets]
                        )
                    case "update":
                        await database.update_query(
                            self.table_name,
                            [wid.value for wid in self.input_widgets[:-2]],
                            (
                                self.input_widgets[-2].value,
                                self.input_widgets[-1].value,
                            ),
                        )
                    case "delete":
                        await database.delete_query(
                            self.table_name, [wid.value for wid in self.input_widgets]
                        )
                self.app.pop_screen()
            case "cancel":
                self.app.pop_screen()

        await self.update_table(self.table_name)

    async def update_table(self, table_name: str) -> None:
        table = self.app.query_one(f"#{table_name}", DataTable)
        table.clear()
        rows = await database.display_query(table_name)
        table.add_rows(rows)
        self.refresh()

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
                self.app.push_screen(InputEntry(attributes, "insert", table_name))
            case "update-button":
                self.app.push_screen(
                    InputEntry(
                        primary_key_attributes + ["Attribute Name", "Attribute Value"],
                        "update",
                        table_name,
                    )
                )
            case "delete-button":
                self.app.push_screen(
                    InputEntry(primary_key_attributes, "delete", table_name)
                )
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

    async def action_quit(self) -> None:
        await database.close()
        return await super().action_quit()


if __name__ == "__main__":
    database: DatabaseConnector
    KnowledgeDatabase().run()
