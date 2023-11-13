from flask import Blueprint, render_template, redirect, request, url_for
blueprint = Blueprint(
    'base_blueprint',
    __name__,
    url_prefix = '',
    template_folder = 'templates',
    static_folder = 'static'
    )

#from database import db
#from .models import User

@blueprint.route('/')
def route_default():
    return redirect(url_for('item_blueprint.item'))

@blueprint.route('/<template>')
def route_template(template):
    return render_template(template + '.html')