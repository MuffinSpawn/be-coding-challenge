import collections
from flask import blueprints, current_app, jsonify, request
from graphlite import V
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from family_tree.database import Address, Person

blueprint = blueprints.Blueprint('child', __name__)


@blueprint.route('/child/add/<person_id>/<child_id>', methods=['POST'])
def add_child(person_id, child_id):
    db = current_app.config['db']
    with db.graph.transaction() as tr:
        tr.store(V(person_id).begat(child_id))
    return jsonify(True)


@blueprint.route('/children/<person_id>', methods=['GET'])
def get_children(person_id):
    db = current_app.config['db']
    child_ids = list(db.graph.find(V(person_id).begat(None)))
    return jsonify(child_ids)


@blueprint.route('/siblings/<person_id>', methods=['GET'])
def get_siblings(person_id):
    db = current_app.config['db']
    parent_ids = list(db.graph.find(V().begat(person_id)))
    sibling_ids = set([])
    for parent_id in parent_ids:
        partial_sibling_ids = list(db.graph.find(V(parent_id).begat(None)))
        for partial_sibling_id in partial_sibling_ids:
            sibling_ids.add(partial_sibling_id)
    return jsonify(list(sibling_ids))


@blueprint.route('/parents/<person_id>', methods=['GET'])
def get_parents(person_id):
    return jsonify(True)


@blueprint.route('/grandparents/<person_id>', methods=['GET'])
def get_grandparents(person_id):
    return jsonify(True)


@blueprint.route('/cousins/<person_id>', methods=['GET'])
def get_cousins(person_id):
    return jsonify(True)
