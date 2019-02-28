from flask import blueprints, current_app, jsonify, request
import logging

logger = logging.getLogger('__name__')
logger.setLevel(logging.DEBUG)

from family_tree.database import Address, Person

blueprint = blueprints.Blueprint('person', __name__)


@blueprint.route('/person', methods=['GET'])
def get_person():
    return jsonify(True)


@blueprint.route('/person/add', methods=['POST'])
def add_person():
    record = request.get_json()
    address = record['address']
    logger.debug('Request Data: {}'.format(record))

    address = Address(**address)
    record.pop('address')
    person = Person(**record)

    db = current_app.config['db']
    db.session.add(address)
    id = db.session.add(person)
    logger.debug('ID: {}'.format(id))
    db.session.commit()
    # flask.flash('Restaurant {} added.'.format(restaurant.name))

    return jsonify(id=person.id)
