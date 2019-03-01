from flask import blueprints, current_app, jsonify, request
from graphlite import V
import logging
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from family_tree.database import Address, Person

blueprint = blueprints.Blueprint('person', __name__)


@blueprint.route('/person/<person_id>', methods=['GET'])
def get_person(person_id):
    db = current_app.config['db']
    try:
        person = db.session.query(Person).filter_by(id=person_id).one()
        record = person.json
        address_id = record.pop('address_id')
        address = db.session.query(Address).filter_by(id=address_id).one()
        record['address'] = address.json
    except NoResultFound:
        return jsonify(False), 404

    return jsonify(record)


@blueprint.route('/person/add', methods=['POST'])
def add_person():
    record = request.get_json()
    address = record['address']

    db = current_app.config['db']

    # For now just add a new address for each person.
    # Ideally we would check if the address exists and reuse it.
    address = Address(**address)
    db.session.add(address)
    db.session.flush()

    record['address_id'] = address.id
    record.pop('address')
    person = Person(**record)

    db.session.add(person)
    db.session.commit()

    return jsonify(id=person.id), 201


@blueprint.route('/person/update/<person_id>', methods=['POST'])
def update_person(person_id):
    update_record = request.get_json()

    db = current_app.config['db']
    person = db.session.query(Person).filter_by(id=person_id).one()

    try:
        update_address = update_record.pop('address')

        address = db.session.query(Address).filter_by(id=person.address_id).one()
        address.update(**update_address)
        db.session.add(address)
    except KeyError:
        pass
    person.update(**update_record)
    db.session.add(person)

    db.session.commit()

    return jsonify(True)


@blueprint.route('/person/remove/<person_id>', methods=['POST'])
def remove_person(person_id):
    db = current_app.config['db']
    person = db.session.query(Person).filter_by(id=person_id).one()
    db.session.delete(person)

    # remove parent and child edges associated with this person
    parent_ids = list(db.graph.find(V().begat(person_id)))
    child_ids = list(db.graph.find(V(person_id).begat(None)))
    with db.graph.transaction() as tr:
        tr.delete_many(V(person_id).begat(id) for id in child_ids)
        tr.delete_many(V(id).begat(person_id) for id in parent_ids)

    return jsonify(True)
