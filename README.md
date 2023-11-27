
# UW-Madison Duo Key Generator

UW Madison requires students to autenticate every login to canvas using duo security. However they provide a website to generate temperary autenticatation keys by answering a few security questions.

This aplication automates the process fo getting a temp key so students do not need a second device to login in.


## Set Up
This project requires python and selenium to be installed. Clone the repo and edit the loginInfo.py file with your login information.

run main.py and a key will by copied to your clipboard. If not all required sequrity questions are in loginInfo.py the program will error and inform you of the needed question answers