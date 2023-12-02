from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Button, DataTable, ContentSwitcher, Footer, Input
from textual.containers import VerticalScroll, Horizontal, Vertical
from textual.screen import Screen

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
    def compose(self) -> ComposeResult:
        with Horizontal(id="table-switcher"):
            with VerticalScroll(id="table-buttons"):
                yield Button("Table1", id="table-1-button")
                yield Button("Table2", id="table-2-button")

            with ContentSwitcher(initial="table-1"):
                yield DataTable(id="table-1")
                yield DataTable(id="table-2")

            with Vertical(id="operation-buttons"):
                yield Button("Insert", id="insert-button")
                yield Button("Update", id="update-button")
                yield Button("Delete", id="delete-button")

        yield (Footer())

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id is None:
            return

        switcher = self.query_one(ContentSwitcher)
        attributes = ["lane", "swimmer", "country", "time"]
        primary_key_attributes = ["lane", "swimmer"]
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

    def on_mount(self) -> None:
        table1 = self.query_one("#table-1", DataTable)
        table1.add_columns(*ROWS[0])
        table1.add_rows(ROWS[1:5])

        table2 = self.query_one("#table-2", DataTable)
        table2.add_columns(*ROWS[0])
        table2.add_rows(ROWS[5:])


class KnowledgeDatabase(App[None]):
    CSS_PATH = "KnowledgeDatabase.tcss"
    SCREENS = {}
    BINDINGS = [Binding("q", "quit", "Quit")]
    TITLE = "Knowledge Database"

    def on_mount(self) -> None:
        self.push_screen(TableSwitcher())


if __name__ == "__main__":
    KnowledgeDatabase().run()
