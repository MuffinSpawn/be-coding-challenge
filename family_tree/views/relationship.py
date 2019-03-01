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
    select_sibling_ids = list(sibling_ids)
    select_sibling_ids.remove(int(person_id))
    return jsonify(select_sibling_ids)


@blueprint.route('/parents/<person_id>', methods=['GET'])
def get_parents(person_id):
    db = current_app.config['db']
    parent_ids = list(db.graph.find(V().begat(person_id)))
    return jsonify(parent_ids)


@blueprint.route('/grandparents/<person_id>', methods=['GET'])
def get_grandparents(person_id):
    db = current_app.config['db']
    parent_ids = list(db.graph.find(V().begat(person_id)))

    grandparent_ids = []
    for parent_id in parent_ids:
        grandparent_ids += list(db.graph.find(V().begat(parent_id)))
    return jsonify(grandparent_ids)


@blueprint.route('/cousins/<person_id>', methods=['GET'])
def get_cousins(person_id):
    db = current_app.config['db']
    parent_ids = list(db.graph.find(V().begat(person_id)))

    grandparent_ids = []
    for parent_id in parent_ids:
        grandparent_ids += list(db.graph.find(V().begat(parent_id)))

    auntuncle_ids = set([])
    for grandparent_id in grandparent_ids:
        partial_auntuncle_ids = list(db.graph.find(V(grandparent_id).begat(None)))
        for partial_auntuncle_id in partial_auntuncle_ids:
            auntuncle_ids.add(partial_auntuncle_id)
    select_auntuncle_ids = list(partial_auntuncle_id)
    for parent_id in parent_ids:
        select_auntuncle_ids.remove(int(parent_id))
    
    cousin_ids = set([])
    for auntuncle_id in select_auntuncle_ids:
        partial_cousin_ids = list(db.graph.find(V(auntuncle_id).begat(None)))
        for partial_cousin_id in partial_cousin_ids:
            cousin_ids.add(partial_cousin_id)
    return jsonify(cousin_ids)
