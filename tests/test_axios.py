import pytest
from click.testing import CliRunner

from axios.cli import cli

env = {
    "AXIOS_USERNAME": "user1234",
    "AXIOS_PASSWORD": "user1234",
    "AXIOS_CUSTOMER_ID": "91014810013",
    "AXIOS_STUDENT_ID": "00001234",
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
        with open("/tmp/sample.txt", "w") as f:
            f.write(result.output)
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
                                                                                
  Data         Materia         Tipo      Voto   Commento         Docente        
 ────────────────────────────────────────────────────────────────────────────── 
  31/01/2023   ARTE E          Grafico   10     Pittura          Pagliarulo     
               IMMAGINE                         rupestre         Veronica       
  27/01/2023   SCIENZE         Pratico   8      IMPEGNO E        Vogliotti      
               MOTORIE E                        PARTECIPAZIONE   Enzo           
               SPORTIVE                                                         
  27/01/2023   SCIENZE         Pratico   7      VALUTAZIONE      Vogliotti      
               MOTORIE E                        TEST FISICI      Enzo           
               SPORTIVE                         ATTITUDINALI                    
  26/01/2023   MUSICA          Pratico   7.5    Verifica di      Cataldo        
                                                carattere        Francesco      
                                                pratico.                        
  25/01/2023   STORIA          Orale     9                       Novelli        
                                                                 Cristina       
  25/01/2023   TECNOLOGIA e    Scritto   8                       Pavarin Maria  
               INFORMATICA                                       Luisa          
  24/01/2023   SCIENZE         Scritto   9      Verifica         Micela Silvia  
                                                scritta                         
                                                sull'organizz…                  
                                                dei viventi                     
  23/01/2023   RELIGIONE       Orale     7                       Avanzato       
                                                                 Paola Carla    
  20/01/2023   ITALIANO        Orale     7.5    Presentazione    Rapalino Lara  
                                                libro                           
  19/01/2023   EDUCAZIONE      Scritto   8,5    Verifica di      Micela Silvia  
               CIVICA                           educazione                      
                                                civica di                       
                                                italiano sulla                  
                                                comprensione                    
                                                del testo                       
  19/01/2023   ITALIANO        Scritto   8.5    Verifica di      Rapalino Lara  
                                                Educazione                      
                                                Civica (il                      
                                                voto fa media                   
                                                con le altre                    
                                                valutazioni di                  
                                                Ed. Civica, ma                  
                                                non con quelle                  
                                                di Italiano):                   
                                                il rapporto                     
                                                tra uomini e                    
                                                animali                         
                                                (comprensione                   
                                                del testo)                      
  18/01/2023   LINGUA          Scritto   9,75   Verifica units   Barbero        
               STRANIERA                        3-4              Daniela        
               INGLESE                                                          
  17/01/2023   ITALIANO        Scritto   9+     Grammatica:      Rapalino Lara  
                                                l'articolo                      
  16/01/2023   STORIA          Scritto   7.7                     Novelli        
                                                                 Cristina       
  13/01/2023   MATEMATICA      Scritto   8,75   Verifica         Micela Silvia  
                                                scritta sui                     
                                                numeri                          
                                                naturali e                      
                                                decimali                        
  12/01/2023   ARTE E          Grafico   8      Paesaggio        Pagliarulo     
               IMMAGINE                                          Veronica       
  12/01/2023   ARTE E          Grafico   9      Colori caldi e   Pagliarulo     
               IMMAGINE                         freddi           Veronica       
  11/01/2023   STORIA          Scritto   7.3                     Novelli        
                                                                 Cristina       
  10/01/2023   EDUCAZIONE      Scritto   7,5    Verifica         Micela Silvia  
               CIVICA                           scritta di                      
                                                educazione                      
                                                civica -                        
                                                Tecnologia                      
  23/12/2022   LINGUA          Scritto   8      Da risentire     Giovannini     
               STRANIERA                        sul verbo        Sonia          
               FRANCESE                         essere.                         
  23/12/2022   ITALIANO        Scritto   6.5    Tema in classe   Rapalino Lara  
  22/12/2022   LINGUA          Orale     8,5    Interrogazione   Barbero        
               STRANIERA                                         Daniela        
               INGLESE                                                          
  21/12/2022   SCIENZE         Scritto   8      Verifica         Micela Silvia  
                                                scritta sugli                   
                                                stati di                        
                                                aggregazione e                  
                                                i passaggi di                   
                                                stato                           
  19/12/2022   ITALIANO        Scritto   8-     La favola:       Rapalino Lara  
                                                comprensione                    
                                                del testo e                     
                                                verifica delle                  
                                                conoscenze                      
  15/12/2022   SCIENZE         Pratico   8      Verifica         Vogliotti      
               MOTORIE E                        intermedia       Enzo           
               SPORTIVE                         test di                         
                                                resistenza:                     
                                                Cooper (6                       
                                                minuti)                         
  13/12/2022   TECNOLOGIA e    Grafico   7                       Pavarin Maria  
               INFORMATICA                                       Luisa          
  12/12/2022   GEOGRAFIA       Scritto   6.7                     Novelli        
                                                                 Cristina       
  06/12/2022   TECNOLOGIA e    Scritto   7.5                     Pavarin Maria  
               INFORMATICA                                       Luisa          
  05/12/2022   RELIGIONE       Orale     8.5    VALUTAZIONE      Avanzato       
                                                PARTECIPAZIONE   Paola Carla    
  02/12/2022   MATEMATICA      Scritto   7,75   Verifica sugli   Micela Silvia  
                                                insiemi                         
  01/12/2022   ARTE E          Grafico   10     Tav.3 figura e   Pagliarulo     
               IMMAGINE                         sfondo           Veronica       
  01/12/2022   ARTE E          Grafico   7/8    Tav.1 Punto e    Pagliarulo     
               IMMAGINE                         linea            Veronica       
  30/11/2022   MUSICA          Orale     7      Verifica di      Cataldo        
                                                carattere        Francesco      
                                                teorico.                        
                                                Interrogazione                  
                                                su tutto il                     
                                                programma                       
                                                svolto finora.                  
  24/11/2022   ITALIANO        Scritto   8.5    Fonologia e      Rapalino Lara  
                                                ortografia                      
  23/11/2022   TECNOLOGIA e    Grafico   6.5                     Pavarin Maria  
               INFORMATICA                                       Luisa          
  23/11/2022   MUSICA          Orale     7,5    Verifica di      Cataldo        
                                                carattere        Francesco      
                                                teorico.                        
                                                Interrogazione                  
                                                su tutto il                     
                                                programma                       
                                                svolto finora.                  
  18/11/2022   MATEMATICA      Grafico   8,5    Verifica sulle   Micela Silvia  
                                                equivalenze e                   
                                                le operazioni                   
                                                con le misure                   
                                                del tempo                       
  16/11/2022   TECNOLOGIA e    Grafico   7                       Pavarin Maria  
               INFORMATICA                                       Luisa          
  10/11/2022   ARTE E          Grafico   8      Poster per la    Pagliarulo     
               IMMAGINE                         pace             Veronica       
  09/11/2022   LINGUA          Scritto   8,5    Test units 1 e   Barbero        
               STRANIERA                        2                Daniela        
               INGLESE                                                          
  08/11/2022   LINGUA          Scritto   8      Verifica unità   Giovannini     
               STRANIERA                        1                Sonia          
               FRANCESE                                                         
  28/10/2022   MATEMATICA      Scritto   8,5    Verifica di      Micela Silvia  
                                                aritmetica                      
                                                sulle                           
                                                rappresentazi…                  
                                                grafiche                        
  26/10/2022   ITALIANO        Orale     7.5    La leggenda      Rapalino Lara  
  25/10/2022   SCIENZE         Scritto   7,75                    Micela Silvia  
  24/10/2022   ITALIANO        Scritto   8.5    Prova di         Rapalino Lara  
                                                comprensione                    
                                                del testo                       
  20/10/2022   LINGUA          Scritto   9,5    Verifica unit    Barbero        
               STRANIERA                        1                Daniela        
               INGLESE                                                          
  20/10/2022   MUSICA          Pratico   6,5    Verifica di      Cataldo        
                                                carattere        Francesco      
                                                pratico.                        
                                                Conoscenza                      
                                                delle prime 5                   
                                                note,                           
                                                posizioni                       
                                                delle dita                      
                                                sullo                           
                                                strumento,                      
                                                qualità del                     
                                                suono.                          
  19/10/2022   SCIENZE         Pratico   7      Valutazione      Vogliotti      
               MOTORIE E                        test fisici      Enzo           
               SPORTIVE                         attitudinali                    
  18/10/2022   LINGUA          Orale     8      Interrogazione   Giovannini     
               STRANIERA                        u1 fino alle     Sonia          
               FRANCESE                         materie                         
                                                scolastiche                     
  17/10/2022   STORIA          Scritto   8.3                     Novelli        
                                                                 Cristina       
  26/09/2022   STORIA          Orale     8                       Novelli        
                                                                 Cristina       
                                                                                

"""
        )


@pytest.mark.vcr(filter_query_parameters=["txtUser", "txtPassword"])
@pytest.mark.block_network
def test_grades_list_json():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli, ["--output-format", "json", "grades", "list"], env=env
        )
        with open("/tmp/sample.txt", "w") as f:
            f.write(result.output)

        expected = '[{"date": "2023-03-20T00:00:00", "subject": "STORIA", "kind": "Orale", "value": "10", "teacher": "Novelli Cristina", "comment": ""}, {"date": "2023-03-17T00:00:00", "subject": "ITALIANO", "kind": "Orale", "value": "8", "teacher": "Rapalino Lara", "comment": "Presentazione orale del libro letto"}, {"date": "2023-03-16T00:00:00", "subject": "LINGUA STRANIERA INGLESE", "kind": "Scritto", "value": "8,25", "teacher": "Barbero Daniela", "comment": "Verifica units 5-6"}, {"date": "2023-03-15T00:00:00", "subject": "TECNOLOGIA e INFORMATICA", "kind": "Grafico", "value": "8", "teacher": "Pavarin Maria Luisa", "comment": ""}, {"date": "2023-03-08T00:00:00", "subject": "ITALIANO", "kind": "Scritto", "value": "8.5", "teacher": "Rapalino Lara", "comment": "Epica: epica omerica e Iliade"}, {"date": "2023-03-08T00:00:00", "subject": "TECNOLOGIA e INFORMATICA", "kind": "Grafico", "value": "8.5", "teacher": "Pavarin Maria Luisa", "comment": ""}, {"date": "2023-03-06T00:00:00", "subject": "ITALIANO", "kind": "Orale", "value": "8", "teacher": "Rapalino Lara", "comment": "La fiaba"}, {"date": "2023-03-02T00:00:00", "subject": "SCIENZE", "kind": "Scritto", "value": "8,75", "teacher": "Micela Silvia", "comment": ""}, {"date": "2023-02-22T00:00:00", "subject": "GEOGRAFIA", "kind": "Orale", "value": "7.75", "teacher": "Gardello Martina", "comment": ""}, {"date": "2023-02-17T00:00:00", "subject": "MATEMATICA", "kind": "Scritto", "value": "9", "teacher": "Micela Silvia", "comment": "Verifica scritta di aritmetica sulle quattro operazioni e le loro propriet\\u00e0."}, {"date": "2023-02-16T00:00:00", "subject": "MUSICA", "kind": "Scritto", "value": "6", "teacher": "Cataldo Francesco", "comment": "Verifica scritta di carattere teorico."}, {"date": "2023-02-16T00:00:00", "subject": "ARTE E IMMAGINE", "kind": "Grafico", "value": "9", "teacher": "Pagliarulo Veronica", "comment": "Arte egizia"}, {"date": "2023-02-15T00:00:00", "subject": "TECNOLOGIA e INFORMATICA", "kind": "Scritto", "value": "8.75", "teacher": "Pavarin Maria Luisa", "comment": ""}, {"date": "2023-02-07T00:00:00", "subject": "LINGUA STRANIERA FRANCESE", "kind": "Scritto", "value": "8", "teacher": "Giovannini Sonia", "comment": "Verifica Unit\\u00e9 3"}]\n'

        assert result.exit_code == 0, result.output
        assert result.output == expected


@pytest.mark.vcr(filter_query_parameters=["txtUser", "txtPassword"])
@pytest.mark.block_network
def test_grades_list_ndjson():
    runner = CliRunner()
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli, ["--output-format", "ndjson", "grades", "list"], env=env
        )
        with open("/tmp/sample.txt", "w") as f:
            f.write(result.output)

        expected = """{"date": "2023-03-23T00:00:00", "subject": "ARTE E IMMAGINE", "kind": "Grafico", "value": "9", "teacher": "Pagliarulo Veronica", "comment": "Concorso LAV"}
{"date": "2023-03-20T00:00:00", "subject": "STORIA", "kind": "Orale", "value": "10", "teacher": "Novelli Cristina", "comment": ""}
{"date": "2023-03-17T00:00:00", "subject": "ITALIANO", "kind": "Orale", "value": "8", "teacher": "Rapalino Lara", "comment": "Presentazione orale del libro letto"}
{"date": "2023-03-16T00:00:00", "subject": "LINGUA STRANIERA INGLESE", "kind": "Scritto", "value": "8,25", "teacher": "Barbero Daniela", "comment": "Verifica units 5-6"}
{"date": "2023-03-15T00:00:00", "subject": "TECNOLOGIA e INFORMATICA", "kind": "Grafico", "value": "8", "teacher": "Pavarin Maria Luisa", "comment": ""}
{"date": "2023-03-08T00:00:00", "subject": "ITALIANO", "kind": "Scritto", "value": "8.5", "teacher": "Rapalino Lara", "comment": "Epica: epica omerica e Iliade"}
{"date": "2023-03-08T00:00:00", "subject": "TECNOLOGIA e INFORMATICA", "kind": "Grafico", "value": "8.5", "teacher": "Pavarin Maria Luisa", "comment": ""}
{"date": "2023-03-06T00:00:00", "subject": "ITALIANO", "kind": "Orale", "value": "8", "teacher": "Rapalino Lara", "comment": "La fiaba"}
{"date": "2023-03-02T00:00:00", "subject": "SCIENZE", "kind": "Scritto", "value": "8,75", "teacher": "Micela Silvia", "comment": ""}
{"date": "2023-02-22T00:00:00", "subject": "GEOGRAFIA", "kind": "Orale", "value": "7.75", "teacher": "Gardello Martina", "comment": ""}
{"date": "2023-02-17T00:00:00", "subject": "MATEMATICA", "kind": "Scritto", "value": "9", "teacher": "Micela Silvia", "comment": "Verifica scritta di aritmetica sulle quattro operazioni e le loro propriet\\u00e0."}
{"date": "2023-02-16T00:00:00", "subject": "MUSICA", "kind": "Scritto", "value": "6", "teacher": "Cataldo Francesco", "comment": "Verifica scritta di carattere teorico."}
{"date": "2023-02-16T00:00:00", "subject": "ARTE E IMMAGINE", "kind": "Grafico", "value": "9", "teacher": "Pagliarulo Veronica", "comment": "Arte egizia"}
{"date": "2023-02-15T00:00:00", "subject": "TECNOLOGIA e INFORMATICA", "kind": "Scritto", "value": "8.75", "teacher": "Pavarin Maria Luisa", "comment": ""}
{"date": "2023-02-07T00:00:00", "subject": "LINGUA STRANIERA FRANCESE", "kind": "Scritto", "value": "8", "teacher": "Giovannini Sonia", "comment": "Verifica Unit\\u00e9 3"}
"""

        assert result.exit_code == 0, result.output
        assert result.output == expected
