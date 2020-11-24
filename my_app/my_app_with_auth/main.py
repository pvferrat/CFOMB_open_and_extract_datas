# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user
import csv
from cfonb import StatementReader
import os
from flask import *  
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

main = Blueprint('main', __name__)


## function allowing extraction
def script(file='4.dat'): 
    
    statement_file = open(file)
    reader = StatementReader() #reader of library

    try: # for classics files  with carriage return
        result =reader.parse(statement_file)
        print('on est dans le try')
    except: # for files without carriage return
        statement_file = open(file).readlines()
        statement_file = statement_file[0] # firt because just a long string
        tmp = '\r\n'.join(statement_file[i:i+120] for i in range(0, len(statement_file), 120)) # add a carriage return every 120 characters
        print('on est dans le except')
        with open('tmp.txt', 'w+') as fh:
            fh.write(tmp)   
            statement_file = open('tmp.txt')
            result =reader.parse(statement_file)
            os.remove("tmp.txt") #remove temp file

    liste_sortie = []        
    for j in list(range(0,len(result))):

        ligne1 = f'Compte numéro : {result[j].header["bank_code"]} {result[j].header["desk_code"]} {result[j].header["account_nb"]}'
        liste_sortie.append(ligne1)
        ligne2 = f'Solde début ({result[j].header["prev_date"]}) : {result[j].header["prev_amount"]}'
        liste_sortie.append(ligne2)
        ligne3 = f'Solde fin ({result[j].footer["next_date"]}) : {result[j].footer["next_amount"]}'
        liste_sortie.append(ligne3)
        ligne4 = ' '
        liste_sortie.append(ligne4)
    return liste_sortie


@main.route('/')
def index():
    return render_template('login.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)