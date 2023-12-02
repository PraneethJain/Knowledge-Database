from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, DataTable, ContentSwitcher, Footer, Input, Static
from textual.containers import VerticalScroll, Horizontal, Vertical
from textual.screen import Screen

from db import create_connector, DatabaseConnector


class ErrorScreen(Screen):
    BINDINGS = [("escape,space,q,question_mark", "pop_screen", "Close")]

    def __init__(
        self,
        exception: Exception,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.exception = exception

    def compose(self) -> ComposeResult:
        yield Static(f"{self.exception}")


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
                try:
                    match self.operation:
                        case "insert":
                            await database.insert_query(
                                self.table_name,
                                [wid.value for wid in self.input_widgets],
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
                                self.table_name,
                                [wid.value for wid in self.input_widgets],
                            )
                    self.app.pop_screen()
                    await self.update_table(self.table_name)
                except Exception as e:
                    self.app.push_screen(ErrorScreen(e))
            case "cancel":
                self.app.pop_screen()

    async def update_table(self, table_name: str) -> None:
        table = self.app.query_one(f"#{table_name}", DataTable)
        table.clear()
        try:
            rows = await database.display_query(table_name)
            table.add_rows(rows)
        except Exception as e:
            self.app.push_screen(ErrorScreen(e))

        self.refresh()

    def compose(self) -> ComposeResult:
        yield from self.input_widgets
        yield Button("Submit", id="submit")
        yield Button("Cancel", id="cancel")


class AdvancedQuery(Screen):
    BINDINGS = [("escape,space,q,question_mark", "pop_screen", "Close")]

    def __init__(
        self,
        input_attr: str,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
    ) -> None:
        super().__init__(name, id, classes)
        self.input_attr = input_attr
        self.mapping_with_input = {
            "topic_name": database.get_prerequisites,
            "pref": database.get_university_by_pref,
            "university": database.get_awards_university_aos,
        }

        self.mapping_without_input = {
            "last_year_awards": database.last_year_awards,
            "get_citations": database.get_citations,
        }
        if self.input_attr in self.mapping_with_input:
            self.input_widget = Input(placeholder=self.input_attr, id="qinput")
            self.func = self.mapping_with_input[self.input_attr]

        self.datatable = DataTable(
            zebra_stripes=True,
            header_height=2,
            cursor_type="none",
        )

        if self.input_attr in self.mapping_without_input:
            self.call_later(self.fill_table)

    async def fill_table(self) -> None:
        results = await self.mapping_without_input[self.input_attr]()
        self.datatable.add_columns(*results[0])
        self.datatable.add_rows(results[1:])

    def compose(self) -> ComposeResult:
        if self.input_attr in self.mapping_with_input:
            yield self.input_widget
        yield self.datatable

    @on(Input.Submitted, "#qinput")
    async def input_submitted(self, event: Input.Submitted):
        results = await self.func(self.input_widget.value)
        if len(self.datatable.columns) == 0:
            self.datatable.add_columns(*results[0])
        self.datatable.clear()
        self.datatable.add_rows(results[1:])
        self.refresh()


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
                yield Static("Tables")

                for table_name in self.table_names:
                    yield Button(table_name, id=f"{table_name}-button")

                yield Static("Advanced Queries")

                yield Button("Last Year Awards", id="last-year-awards-button")
                yield Button("Get Prerequisites", id="get-prerequisites-button")
                yield Button("Get Citations", id="get-citations-button")
                yield Button("Get University", id="get-university-button")
                yield Button("Get Awards University", id="get-awards-university-button")

            with ContentSwitcher(initial=self.table_names[0]):
                for table_name in self.table_names:
                    yield DataTable(
                        id=table_name,
                        zebra_stripes=True,
                        header_height=2,
                        cursor_type="none",
                    )

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
        try:
            attributes = await database.get_table_headers(table_name)
            primary_key_attributes = await database.get_primary_key(table_name)
        except Exception as e:
            self.app.push_screen(ErrorScreen(e))
            return

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
            case "last-year-awards-button":
                self.app.push_screen(AdvancedQuery("last_year_awards"))
            case "get-prerequisites-button":
                self.app.push_screen(AdvancedQuery("topic_name"))
            case "get-citations-button":
                self.app.push_screen(AdvancedQuery("get_citations"))
            case "get-university-button":
                self.app.push_screen(AdvancedQuery("pref"))
            case "get-awards-university-button":
                self.app.push_screen(AdvancedQuery("university"))
            case _:
                switcher.current = event.button.id[:-7]

    async def on_mount(self) -> None:
        for table_name in self.table_names:
            table = self.query_one(f"#{table_name}", DataTable)

            try:
                headers = await database.get_table_headers(table_name)
            except Exception as e:
                self.app.push_screen(ErrorScreen(e))
                return
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
