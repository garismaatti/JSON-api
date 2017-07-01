#!/usr/bin/env python2
# -*- coding: utf8 -*-

from flask import Flask, jsonify, abort, request, make_response, url_for
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if username == 'miguel':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 403)
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog

@app.errorhandler(400)
def not_found(error):
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

catalog = [
    {
        'id': 1,
        'name': 'Apples',
        'amount': 100,
        'price': 10.25
    },
    {
        'id': 2,
        'name': 'Carrots',
        'amount': 120,
        'price': 9.98
    }
]

def make_public_item(item):
    new_item = {}
    for field in item:
        if field == 'id':
            new_item[field] = item[field]
            new_item['uri'] = url_for('get_item', item_id = item['id'], _external = False)
        else:
            new_item[field] = item[field]
    return new_item

@app.route('/api/v1.0/catalog', methods = ['GET'])
@auth.login_required
def get_catalog():
    return jsonify( { 'catalog': map(make_public_item, catalog) } )

@app.route('/api/v1.0/catalog/<int:item_id>', methods = ['GET'])
@auth.login_required
def get_item(item_id):
    item = filter(lambda t: t['id'] == item_id, catalog)
    if len(item) == 0:
        abort(404)
    return jsonify( { 'item': make_public_item(item[0]) } )

@app.route('/api/v1.0/catalog', methods = ['POST'])
@auth.login_required
def create_item():
    if not request.json or not 'name' in request.json:
        abort(400)
    item = {
        'id': catalog[-1]['id'] + 1,
        'name': request.json['name'],
        'description': request.json.get('description', ""),
        'done': False
    }
    catalog.append(item)
    return jsonify( { 'item': make_public_item(item) } ), 201

@app.route('/api/v1.0/catalog/<int:item_id>', methods = ['PUT'])
@auth.login_required
def update_item(item_id):
    item = filter(lambda t: t['id'] == item_id, catalog)
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    item[0]['title'] = request.json.get('title', item[0]['title'])
    item[0]['description'] = request.json.get('description', item[0]['description'])
    item[0]['done'] = request.json.get('done', item[0]['done'])
    return jsonify( { 'item': make_public_item(item[0]) } )

@app.route('/api/v1.0/catalog/<int:item_id>', methods = ['DELETE'])
@auth.login_required
def delete_item(item_id):
    item = filter(lambda t: t['id'] == item_id, catalog)
    if len(item) == 0:
        abort(404)
    catalog.remove(item[0])
    return jsonify( { 'result': True } )

if __name__ == '__main__':
    app.run(debug = True)
