from flask import Blueprint
from coderg.extensions import db
from coderg.models import Role

onetime = Blueprint('onetime', __name__)


@onetime.route('/aqdasadmin')
def aqdasadmin():
    db.session.add(Role(title='ADMIN', username='aqdas'))
