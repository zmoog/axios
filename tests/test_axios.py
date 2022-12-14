from unittest.mock import patch

import pytest
from click.testing import CliRunner

from axios.cli import cli


env = {
    "AXIOS_USERNAME": "username",
    "AXIOS_PASSWORD": "password",
    "AXIOS_CUSTOMER_ID": "91014810013",
}

def test_version():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["--version"], env=env)
        assert result.exit_code == 0
        assert result.output.startswith("cli, version ")
    assert result.exit_code == 0, result.output
    assert result.output.startswith("cli, version ")


@pytest.mark.vcr(filter_query_parameters=["txtUser", "txtPassword"])
@pytest.mark.block_network
def test_login():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["login"], env=env)
        assert result.exit_code == 0, result.output
        assert (
            "Logged in as BRANCA MAURIZIO (ISTITUTO COMPRENSIVO VEROLENGO)"
            in result.output
        )


@pytest.mark.vcr(filter_query_parameters=["txtUser", "txtPassword"])
@pytest.mark.block_network
def test_list_grades():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["grades", "list"], env=env)
        assert result.exit_code == 0, result.output
        assert (
            # Click's CliRunner uses a terminal width of 80 characters, so
            # Rich will wrap the output to fit the terminal width.
            #
            # Don't go crazy with the indentation, just save the output in a
            # file with something like:
            #
            # with open("sample.txt", "w") as f:
            #     f.write(result.output)
            #
            # And then copy the output from the file in the assert.
            result.output
            == """                                     Grades                                     
                                                                                
  Data         Materia     Tipo      Voto   Obiettivi   Commento     Docente    
 ?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????? 
  10/11/2022   ARTE E      Grafico   8                  Poster per   Pagliaru???  
               IMMAGINE                                 la pace      Veronica   
  09/11/2022   LINGUA      Scritto   8,5                Test units   Barbero    
               STRANIERA                                1 e 2        Daniela    
               INGLESE                                                          
  26/10/2022   ITALIANO    Orale     7.5                La           Rapalino   
                                                        leggenda     Lara       
  25/10/2022   SCIENZE     Scritto   7,75                            Micela     
                                                                     Silvia     
  24/10/2022   ITALIANO    Scritto   8.5                Prova di     Rapalino   
                                                        comprensi???   Lara       
                                                        del testo               
  20/10/2022   LINGUA      Scritto   9,5                Verifica     Barbero    
               STRANIERA                                unit 1       Daniela    
               INGLESE                                                          
  20/10/2022   MUSICA      Pratico   6,5                Verifica     Cataldo    
                                                        di           Francesco  
                                                        carattere               
                                                        pratico.                
                                                        Conoscenza              
                                                        delle                   
                                                        prime 5                 
                                                        note,                   
                                                        posizioni               
                                                        delle dita              
                                                        sullo                   
                                                        strumento,              
                                                        qualit??                 
                                                        del suono.              
  19/10/2022   SCIENZE     Pratico   7                  Valutazio???   Vogliotti  
               MOTORIE E                                test         Enzo       
               SPORTIVE                                 fisici                  
                                                        attitudin???              
  18/10/2022   LINGUA      Orale     8                  Interroga???   Giovanni???  
               STRANIERA                                u1 fino      Sonia      
               FRANCESE                                 alle                    
                                                        materie                 
                                                        scolastic???              
  17/10/2022   STORIA      Scritto   8.3                             Novelli    
                                                                     Cristina   
  26/09/2022   STORIA      Orale     8                               Novelli    
                                                                     Cristina   
                                                                                

"""
        )
