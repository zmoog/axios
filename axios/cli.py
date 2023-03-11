import datetime
import io

import click
from rich import box
from rich.console import Console
from rich.table import Table

from .models import Credentials
from .navigator import Navigator

today = datetime.date.today()


@click.group()
@click.option("--username", "-u", required=True, envvar="AXIOS_USERNAME")
@click.option("--password", "-p", required=True, envvar="AXIOS_PASSWORD")
@click.option(
    "--customer-id", "-id", required=True, envvar="AXIOS_CUSTOMER_ID"
)
@click.option("--student-id", required=True, envvar="AXIOS_STUDENT_ID")
@click.option(
    "--year",
    required=True,
    default=today.year if 9 <= today.month <= 12 else today.year - 1,
    envvar="AXIOS_STUDENT_YEAR",
)
@click.option(
    "--period",
    required=True,
    default="FT01" if today.month <= 12 else "FT02",
    envvar="AXIOS_STUDENT_PERIOD",
)
@click.option(
    "-v",
    "--verbose",
    is_flag=True,
    help="Enables verbose mode",
    default=False,
    envvar="AXIOS_VERBOSE",
)
@click.version_option()
@click.pass_context
def cli(
    ctx: click.Context,
    username: str,
    password: str,
    customer_id: str,
    student_id: str,
    year: int,
    period: str,
    verbose: bool,
):
    """Command line utility to access https://family.axioscloud.it"""
    ctx.ensure_object(dict)
    ctx.obj["username"] = username
    ctx.obj["password"] = password
    ctx.obj["customer_id"] = customer_id
    ctx.obj["student_id"] = student_id
    ctx.obj["year"] = year
    ctx.obj["period"] = period
    ctx.obj["verbose"] = verbose


@cli.command(name="login")
@click.pass_context
def login(ctx: click.Context):
    nav = Navigator(
        Credentials(
            username=ctx.obj["username"],
            password=ctx.obj["password"],
            customer_id=ctx.obj["customer_id"],
        ),
        student_id=ctx.obj["student_id"],
    )

    profile = nav.login()

    click.echo(
        f"Logged in as {profile.name} ({profile.customer_title} {profile.customer_name})"
    )


@cli.group()
def grades():
    pass


@grades.command(name="list")
@click.pass_context
def list_grades(ctx: click.Context):
    nav = Navigator(
        Credentials(
            username=ctx.obj["username"],
            password=ctx.obj["password"],
            customer_id=ctx.obj["customer_id"],
        ),
        student_id=ctx.obj["student_id"],
    )

    nav.login()
    nav.select_year(ctx.obj["year"])
    nav.select_period(ctx.obj["period"])

    _grades = nav.list_grades()

    table = Table(title="Grades", box=box.SIMPLE)
    table.add_column("Data")
    table.add_column("Materia")
    table.add_column("Tipo")
    table.add_column("Voto")
    # table.add_column("Obiettivi")
    table.add_column("Commento")
    table.add_column("Docente")

    for v in _grades:
        table.add_row(
            str(v.date),
            str(v.subject),
            str(v.kind),
            str(v.value),
            # str(v.target),
            str(v.comment),
            str(v.teacher),
        )

    # we capture the output into this variable
    output = io.StringIO()

    # turn table into a string using the Console
    console = Console(file=output)
    console.print(table)

    click.echo(output.getvalue())
