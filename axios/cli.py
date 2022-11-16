import io

import click
from rich import box
from rich.console import Console
from rich.table import Table

from .models import Credentials
from .navigator import Navigator


@click.group()
@click.version_option()
def cli():
    "Command line utility to access https://family.axioscloud.it"


@cli.command(name="login")
@click.option("--username", "-u", required=True, envvar="AXIOS_USERNAME")
@click.option("--password", "-p", required=True, envvar="AXIOS_PASSWORD")
@click.option(
    "--customer-id", "-id", required=True, envvar="AXIOS_CUSTOMER_ID"
)
def login(username: str, password: str, customer_id: str):
    nav = Navigator(
        Credentials(
            username=username, password=password, customer_id=customer_id
        )
    )

    profile = nav.login()

    click.echo(
        f"Logged in as {profile.name} ({profile.customer_title} {profile.customer_name})"
    )


@cli.command(name="list-grades")
@click.option("--username", "-u", required=True, envvar="AXIOS_USERNAME")
@click.option("--password", "-p", required=True, envvar="AXIOS_PASSWORD")
@click.option(
    "--customer-id", "-id", required=True, envvar="AXIOS_CUSTOMER_ID"
)
def list_grades(username: str, password: str, customer_id: str):
    nav = Navigator(
        Credentials(
            username=username,
            password=password,
            customer_id=customer_id,
        )
    )

    nav.login()
    grades = nav.list_grades()

    table = Table(title="Grades", box=box.SIMPLE)
    table.add_column("Data")
    table.add_column("Materia")
    table.add_column("Tipo")
    table.add_column("Voto")
    table.add_column("Obiettivi")
    table.add_column("Commento")
    table.add_column("Docente")

    for v in grades:
        table.add_row(
            str(v.date),
            str(v.subject),
            str(v.kind),
            str(v.value),
            str(v.target),
            str(v.comment),
            str(v.teacher),
        )

    # turn table into a string using the Console
    console = Console(file=io.StringIO())
    console.print(table)

    click.echo(console.file.getvalue())
