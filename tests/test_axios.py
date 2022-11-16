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

@pytest.mark.vcr(filter_query_parameters=["txtUser", "txtPassword"])
@pytest.mark.block_network
def test_list_grades():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["list-grades"])
        assert result.exit_code == 0
        assert (
            result.output
            == """                                     Grades                                     
                                                                                
  Data         Materia     Tipo      Voto   Obiettivi   Commento     Docente    
 ────────────────────────────────────────────────────────────────────────────── 
  10/11/2022   ARTE E      Grafico   8                  Poster per   Pagliaru…  
               IMMAGINE                                 la pace      Veronica   
  09/11/2022   LINGUA      Scritto   8,5                Test units   Barbero    
               STRANIERA                                1 e 2        Daniela    
               INGLESE                                                          
  26/10/2022   ITALIANO    Orale     7.5                La           Rapalino   
                                                        leggenda     Lara       
  25/10/2022   SCIENZE     Scritto   7,75                            Micela     
                                                                     Silvia     
  24/10/2022   ITALIANO    Scritto   8.5                Prova di     Rapalino   
                                                        comprensi…   Lara       
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
                                                        qualità                 
                                                        del suono.              
  19/10/2022   SCIENZE     Pratico   7                  Valutazio…   Vogliotti  
               MOTORIE E                                test         Enzo       
               SPORTIVE                                 fisici                  
                                                        attitudin…              
  18/10/2022   LINGUA      Orale     8                  Interroga…   Giovanni…  
               STRANIERA                                u1 fino      Sonia      
               FRANCESE                                 alle                    
                                                        materie                 
                                                        scolastic…              
  17/10/2022   STORIA      Scritto   8.3                             Novelli    
                                                                     Cristina   
  26/09/2022   STORIA      Orale     8                               Novelli    
                                                                     Cristina   
                                                                                

"""
        )
