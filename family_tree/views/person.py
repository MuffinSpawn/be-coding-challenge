from flask import blueprints, current_app, jsonify, request
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

from family_tree.database import Address, Person

blueprint = blueprints.Blueprint('person', __name__)


@blueprint.route('/person/<person_id>', methods=['GET'])
def get_person(person_id):
    db = current_app.config['db']
    person = db.session.query(Person).filter_by(id=person_id).one()
    record = person.json
    address_id = record.pop('address_id')
    address = db.session.query(Address).filter_by(id=address_id).one()
    record['address'] = address.json

    return jsonify(record)


@blueprint.route('/person/add', methods=['POST'])
def add_person():
    record = request.get_json()
    address = record['address']

    db = current_app.config['db']

    address = Address(**address)
    db.session.add(address)
    db.session.flush()

    record['address_id'] = address.id
    record.pop('address')
    person = Person(**record)

    db.session.add(person)
    db.session.commit()

    return jsonify(id=person.id)
