import io
from typing import List

import click
from rich import box
from rich.console import Console
from rich.table import Table

from .models import Grade


class GradesListResult:
    
    def __init__(self, grades: List[Grade]) -> None:
        self.grades = grades

    def __str__(self) -> str:
        table = Table(title="Grades", box=box.SIMPLE)
        table.add_column("Data")
        table.add_column("Materia")
        table.add_column("Tipo")
        table.add_column("Voto")
        table.add_column("Commento")
        table.add_column("Docente")

        for g in self.grades:
            table.add_row(
                str(g.date),
                str(g.subject),
                str(g.kind),
                str(g.value),
                str(g.comment),
                str(g.teacher),
            )

        # we capture the output into this variable
        output = io.StringIO()

        # turn table into a string using the Console
        console = Console(file=output)
        console.print(table)

        return output.getvalue()


    def json(self) -> str:
        pass

    def ndjson(self) -> str:
        pass
