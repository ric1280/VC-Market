## VC-Market 

Requirements:
  -python 2.7
  -mysql server
  -R 3.5.2
  -rpython
  -Rserve

1. Install python 2.7 https://www.python.org/download/releases/2.7/
2. Install mysql (only server is required) https://cybersaf-my.sharepoint.com/:u:/g/personal/ricardo_maia_cybersafe_pt/EWXk38na2f1Ohqi5U0LDbVoBaahTGTliZV0OXM05wwheEw?e=uv9GTe
  - Add a user with admin priviledges and with the following credentials: username:user, password:1234
3. Install mysql connector-c-6.0.2 https://cybersaf-my.sharepoint.com/personal/ricardo_maia_cybersafe_pt/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fricardo_maia_cybersafe_pt%2FDocuments%2FPrograms%2Fmysql-connector-c-6%2E0%2E2-win32%2Emsi&parent=%2Fpersonal%2Fricardo_maia_cybersafe_pt%2FDocuments%2FPrograms&CID=d2b8fc63-719d-4277-94c4-3a176db84cc8
4. Install mysql Python exe https://cybersaf-my.sharepoint.com/:u:/g/personal/ricardo_maia_cybersafe_pt/EZJeaHzPto5IuJuiwU89n1sBTjkVoKcyMLewY5wwWeyACA?e=gH88lU
5. Install R 3.5.2
6. Install rpython available here https://cybersaf-my.sharepoint.com/:f:/g/personal/ricardo_maia_cybersafe_pt/EmY5TBppyH1JplGpzG-pyYwBGXjjNhp5Jn3VWJAJDW2wjg?e=DxwQd3
  - Install RTools for windows to install a R package from file and not from Cran repository
7. Install Rserve windows exe and R Cran Package

#### Run the Market ####

1. Start R Serve:
  - On cmd:
    >R
    >library(Rserve)
    >Rserve()
    
2. Run MarketServer.py under VC-Market/Market
3. Start volunteers: 
    - Run startVolunteer.R under VC-Market/Client (On Rstudio or cmd with Rscript command)
4. Load client R packages:
    - Open a R session on Rstudio or cmd with command R
    - > source("vc_compute.R")
    - > single_remote_execution() 
    - > choose a job to send to the market, for instance prime_factorization.R
    

# PredictorSystem
As organizations realize how data analysis helps them to harness their data and use it to identify new opportunities, the popularity of specialized programming languages like R rises. R is an open source programming language and an environment for statistical computing and graphics, whose increasing notoriety has attracted lots of new users, including everyday users that cannot take the most of the R’s capabilities due to a lack of computing resources. For these reasons, a Volunteer Computing (VC) platform for R software is currently being developed to allow public participants to, voluntarily, share their devices’ idle processing power in exchange for computing credits. These credits can then be used to request for computing power within the platform. In this work we propose a decision system for the mentioned platform that, through estimations, selects the most suitable execution site for a given R script. In order to generate such estimations we follow a history based approach, where we use previous function calls observations to create regression models. The results from this proposed system were validated using the R-Benchmark 25 script, which is globally used in the R community as an utility to measure the R’s performance under different machines.


## Important Files

: .R :

- rExecutor.R
- realArgumentMiner.R
- callTreeAnalysis.R
- predictorFunct.R
- mutualMinerFunctions.R
- drawTree.R
- historyReader.R

: .py :

- saveModule.py
- connectionModule.py
- dummyVolunteers.py
- dummyMarket.py
- offPredictor.py

Francisco Banha's Files
-
- client.R
-

## Important Installations

- Python 2.7
- R 3.4.0
- install Iperf3 on the machine
- install: `sudo apt-get install python-dev`
- install the necessary R packages
- Use `sudo apt-get install r-cran-car` in case `car` package is not installing
- install so that the banner can be printed`sudo apt-get install xclip || echo "alias clipboard='xclip -sel clip'" >> ~/.bashrc`


## Important Notes
- Código do Francisco Banha (sandbox) não está integrado. Precisa de uma versão modificada do próprio R.
- A parte de gravar o ambiente de execução para depois fornecer ao incubator, não está a funcionar. Mas não é essencial visto que o que se quer é a integração com o interpretador do R (ver issue #6)
- The price (a.k.a credits per time unit) is not being considered in the decision
- The R files have to be run from the indicated folder (ver issue #1)

## Main Commands

- Run `offPredictor.py`, `dummyVolunteers.py` and `dummyMarket.py`

In order to **_run the example file_**:

```
(...)/PredictorSystem_public/CodeAnalysisRW/Demos$  Rscript testScript.R

```

## Other Commands


In order to **_populate_** a certain **package** with CRAN example file:
```
(...)/PredictorSystem_public/CodeAnalysisRW$  Rscript populateFunction.R stats

```

In order to **_populate_** a certain **function** with CRAN example file:
```
(...)/PredictorSystem_public/CodeAnalysisRW$  Rscript populateFunction.R stats lm

```

In order to **_display the records_** a certain **function** has in the system:

```
(...)/PredictorSystem_public/CodeAnalysisRW$  Rscript historyReader.R stats lm

```

In order to **_display the records_** a certain **package** has in the system:

```
(...)/PredictorSystem_public/CodeAnalysisRW$  Rscript historyReader.R TOTAL stats

```


# VC-Market




