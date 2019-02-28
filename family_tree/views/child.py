from flask import blueprints, current_app, jsonify, request
from graphlite import V
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from family_tree.database import Address, Person

blueprint = blueprints.Blueprint('child', __name__)


@blueprint.route('/children/<person_id>', methods=['GET'])
def get_person(person_id):
    db = current_app.config['db']
    child_ids = db.graph.find(V(person_id).begat())
    return jsonify(child_ids)


@blueprint.route('/child/add/<person_id>/<child_id>', methods=['POST'])
def add_person(person_id, child_id):
    db = current_app.config['db']
    with db.graph.transaction() as tr:
        tr.store(V(person_id).begat(child_id))
    return True
