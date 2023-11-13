# -*- coding: utf-8 -*-
# config import
from config import app_config, app_active
from flask import Flask, request, redirect, render_template, Response, json, abort
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module
# config import
from config import app_config, app_active

config = app_config[app_active]

def create_app(config_name):
    app = Flask(__name__, template_folder='templates')


    app.secret_key = config.SECRET
    app.config.from_object(app_config[app_active])
    app.config.from_pyfile('config.py')

    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(config.APP)
    db.init_app(app)

    #Blueprint
    for module_name in ('entrada', 'equipamento', 'item', 'saida', 'user', 'base'):
        module = import_module('{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

    return app