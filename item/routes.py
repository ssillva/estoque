from flask import Blueprint, render_template, redirect, request, url_for

blueprint = Blueprint(
    'item_blueprint',
    __name__,
    url_prefix = '/item',
    template_folder = 'templates',
    static_folder = 'static'
    )

@blueprint.route('/index')
def index():
    all_data = Itens.query.all()
    return render_template("index.html", employees=all_data)

@blueprint.route('/<template>')
def route_template(template):
    return render_template(template + '.html')
