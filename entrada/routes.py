from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint(
    'entrada_blueprint',
    __name__,
    url_prefix = '/entrada',
    template_folder = 'templates',
    static_folder = 'static'
    )

@blueprint.route('/<template>')
@login_required
def route_template(template):
    return render_template(template + '.html')