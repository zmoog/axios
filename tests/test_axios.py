from unittest.mock import patch

from click.testing import CliRunner
import pytest

from axios.cli import cli


def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")

@pytest.mark.vcr(filter_query_parameters=["txtUser", "txtPassword"])
@pytest.mark.block_network
def test_login():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["login"])
        assert result.exit_code == 0
        assert "Logged in as BRANCA MAURIZIO (ISTITUTO COMPRENSIVO VEROLENGO)" in result.output

# @pytest.mark.vcr(filter_query_parameters=["txtUser", "txtPassword"])
# @pytest.mark.block_network
# def test_list_grades():
#     runner = CliRunner()
#     with runner.isolated_filesystem():
#         result = runner.invoke(cli, ["list-grades"])
#         assert result.exit_code == 0
#         assert "Logged in as BRANCA MAURIZIO (ISTITUTO COMPRENSIVO VEROLENGO)" in result.output
