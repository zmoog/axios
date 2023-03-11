# axios

Python library and CLI to access the school electronic register from Axios

[![PyPI](https://img.shields.io/pypi/v/axios.svg)](https://pypi.org/project/axios/)
[![Changelog](https://img.shields.io/github/v/release/zmoog/axios?include_prereleases&label=changelog)](https://github.com/zmoog/axios/releases)
[![Tests](https://github.com/zmoog/axios/workflows/Test/badge.svg)](https://github.com/zmoog/axios/actions?query=workflow%3ATest)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/zmoog/axios/blob/master/LICENSE)

Command line utility to access https://family.axioscloud.it

## Installation

Install this tool using `pip`:

    pip install axios

## Usage

First, set the environment variables:

    export AXIOS_CUSTOMER_ID="12345678909"
    export AXIOS_USERNAME="1234"
    export AXIOS_PASSWORD="a-secret-i-will-not-share"
    export AXIOS_STUDENT_ID="4567"

To list latest grades, run:

    $ axios grades list
                                                                                            Grades

      Data         Materia                      Tipo      Voto   Obiettivi   Commento                                                                                Docente
     ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
      06/12/2022   TECNOLOGIA e INFORMATICA     Scritto   7.5                                                                                                        Pavarin Maria Luisa
      02/12/2022   MATEMATICA                   Scritto   7,75               Verifica sugli insiemi                                                                  Micela Silvia
      01/12/2022   ARTE E IMMAGINE              Grafico   10                 Tav.3 figura e sfondo                                                                   Pagliarulo Veronica
      01/12/2022   ARTE E IMMAGINE              Grafico   7/8                Tav.1 Punto e linea                                                                     Pagliarulo Veronica
      30/11/2022   MUSICA                       Orale     7                  Verifica di carattere teorico. Interrogazione su tutto il programma svolto finora.      Cataldo Francesco
      24/11/2022   ITALIANO                     Scritto   8.5                Fonologia e ortografia                                                                  Rapalino Lara
      23/11/2022   TECNOLOGIA e INFORMATICA     Grafico   6.5                                                                                                        Pavarin Maria Luisa
      23/11/2022   MUSICA                       Orale     7,5                Verifica di carattere teorico. Interrogazione su tutto il programma svolto finora.      Cataldo Francesco
      18/11/2022   MATEMATICA                   Grafico   8,5                Verifica sulle equivalenze e le operazioni con le misure del tempo                      Micela Silvia
      16/11/2022   TECNOLOGIA e INFORMATICA     Grafico   7                                                                                                          Pavarin Maria Luisa
      10/11/2022   ARTE E IMMAGINE              Grafico   8                  Poster per la pace                                                                      Pagliarulo Veronica
      09/11/2022   LINGUA STRANIERA INGLESE     Scritto   8,5                Test units 1 e 2                                                                        Barbero Daniela

Defaults to current year and period.

To select a different year or period, run:

    # allowed values: FT01 and FT02
    axios --period FT02 grades list 

    # the year classes started
    axios --year 2021 grades list 
    
    # you can combine them, of course
    axios --year 2021 --period FT01

For help, run:

    axios --help

You can also use:

    python -m axios --help

## Development

To contribute to this tool, first checkout the code. Then create a new virtual environment:

    cd axios
    python -m venv venv
    source venv/bin/activate

Now install the dependencies and test dependencies:

    pip install -e '.[test]'

To run the tests:

    pytest
