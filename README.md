# tic_tac_toe

## Set Up Your Environment
Install Python: Ensure Python 3.6 or later is installed on your system.

## Create a Virtual Environment:
## Open a terminal or command prompt and navigate to the directory where you want to create your project. Run the following commands:
python -m venv tenv
## Windows:
tenv\Scripts\activate
## macOS/Linux:
source tenv/bin/activate

## Install Dependencies by using the following commands:
pip install -r requirements.txt
## Start Server by using the following commands:
cd tictactoe

## create Tables 
python manage.py makemigrations / python manage.py makemigrations game



python manage.py migrate
## windows

python manage.py runserver
## macOS/Linux:
python3 manage.py runserver
