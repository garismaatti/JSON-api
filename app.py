#!/usr/bin/env python2
# -*- coding: utf8 -*-
#
# 2017-04-24 by Ari Salopää
#
# Versio 1
# TASK 1, 2 and 3 done
'''
CHALLENGE 1.

Your task is to implement backend application library to product catalog and shopping basket​ of a web shop.

Product catalog contains at least
 - names,
 - amounts for sale (i.e. stock) and
 - prices of available products.
 - ...?

Shopping basket contains products from catalog and to­be­purchased amounts.
Don’t forget to keep the product catalog up to date: products and stocks are updated based on the reservations in the basket.


We need the following functions:
1. Adding/removing/editing products in product catalog
2. Adding/removing/editing products in shopping basket
3. Querying products from product catalog with basic pagination (e.g. 100 products /
query), sorted by given sorting key (name or price).

4. Querying products from product catalog, grouped by price ranges
(with a single functioncall, fully customizable via input data, example of range set: cheaper than 5 €, 5-­10€, more expensive than 10€).
5. Searching product from catalog by matching the beginning of product name, filtering the results within given price range (min, max), and sorting by given key (name or price).

We appreciate good programming practices (e.g. tests) and readibility of your solution. ​
Please mark clearly task number in your code in the following format: TASK­1, TASK­2 etc.

You can employ any programming language and use freely any open source software libraries.
To store data, you can use suitable database engine.
'''

from flask import Flask, jsonify, abort, request, make_response, url_for
#from flask_httpauth import HTTPBasicAuth
import time

app = Flask(__name__, static_url_path = "")
#auth = HTTPBasicAuth()


# TODO make a proper SQL database
catalog = [
    {
        'id': 1,
        'name': 'Apples',
        'amount': 100,
        'unit': 'kpl',
        'price': 10.25,
        'currency': '€',
        'add_time': time.strftime("%G-%m-%dT%TZ"),
        'add_person': 'test',
        'mod_time': time.strftime("%G-%m-%dT%TZ"),
        'mod_person': 'test'
    },
    {
        'id': 2,
        'name': 'Carrots',
        'amount': 120,
        'unit': 'kpl',
        'price': 9.98,
        'currency': u'€',
        'add_time': time.strftime("%G-%m-%dT%TZ"),
        'add_person': 'test',
        'mod_time': time.strftime("%G-%m-%dT%TZ"),
        'mod_person': 'test'
    }
]

basket = [
    {
        'user_id': 'cookie',
        'product_id': 1,
        'amount': 120,
        'add_time': time.strftime("%G-%m-%dT%TZ"),
        'mod_time': time.strftime("%G-%m-%dT%TZ")
    }
]


# handle error - 400 bad request
@app.errorhandler(400)
def not_found(error):
    if error.description['message']:
        return make_response(jsonify( { 'error': 'Bad request, ' +str(error.description['message']) } ), 400)
    return make_response(jsonify( { 'error': 'Bad request' } ), 400)

# handle error - 404 not found
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

# handle error - 409 Conflict
@app.errorhandler(409)
def not_found(error):
    return make_response(jsonify( { 'error': 'Conflict, already exist!' } ), 404)


# modify items returned throu api
def make_public_item(item):
    new_item = {}
    for field in item:
        if field == 'id':
            new_item[field] = item[field]
            new_item['uri'] = url_for('get_item', item_id = item['id'], _external = False)
        elif field == 'add_time':
            pass
        elif field == 'add_person':
            pass
        elif field == 'mod_time':
            pass
        elif field == 'mod_person':
            pass
        else:
            new_item[field] = item[field]
    return new_item




### TASK 1

# GET catalog
@app.route('/api/v1.0/catalog', methods = ['GET'])
#@auth.login_required
def get_catalog():
    ### TASK 3
    fullCatalog = map(make_public_item, catalog)
    try:
        limit = int( request.args.get('limit', '0') )  #limit result
    except:
        abort(400, {'message': 'invalid limit!'})
    sortby = request.args.get('sortby', 'name') #sorting by 'name' or 'price'
    #sort list
    sortedlist = sorted(fullCatalog, key=lambda k: k[sortby])
    #limit rows amount
    if limit > 0:
        fullCatalog = []
        for j in range(limit):
            fullCatalog.append(sortedlist[j])
            print j
    else:
        fullCatalog = sortedlist
    return jsonify( { 'catalog': fullCatalog } )


# GET catalog item
@app.route('/api/v1.0/catalog/<int:item_id>', methods = ['GET'])
#@auth.login_required
def get_item(item_id):
    item = filter(lambda t: t['id'] == item_id, catalog)
    if len(item) == 0:
        abort(404)
    return jsonify( { 'item': make_public_item(item[0]) } )


# NEW catalog item
@app.route('/api/v1.0/catalog', methods = ['POST'])
#@auth.login_required
def create_item():
    if not request.json \
    or not 'name' in request.json \
    or not 'price' in request.json \
    or not 'amount' in request.json:
        abort(400)
    item = {
        'id': catalog[-1]['id'] + 1,
        'name': request.json['name'],
        'amount': request.json['amount'],
        'unit': request.json.get('unit', 'kpl'),
        'price': request.json['name'],
        'currency': request.json.get('currency', '€'),
        'add_time': time.strftime("%G-%m-%dT%TZ"),
        'add_person': 'api',
        'mod_time': time.strftime("%G-%m-%dT%TZ"),
        'mod_person': 'api'
    }
    catalog.append(item)
    return jsonify( { 'item': make_public_item(item) } ), 201


# MOD catalog item
@app.route('/api/v1.0/catalog/<int:item_id>', methods = ['PUT'])
#@auth.login_required
def update_item(item_id):
    item = filter(lambda t: t['id'] == item_id, catalog)
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' in request.json and type(request.json['name']) != unicode:
        abort(400)
    if 'unit' in request.json and type(request.json['unit']) != unicode:
        abort(400)
    if 'currency' in request.json and type(request.json['currency']) != unicode:
        abort(400)
    if 'mod_person' in request.json and type(request.json['mod_person']) != unicode:
        abort(400)
    if 'amount' in request.json and type(request.json['amount']) is not int:
        abort(400)
    if 'price' in request.json and type(request.json['price']) is not float:
        abort(400)
    item[0]['name'] = request.json.get('name', item[0]['name'])
    item[0]['amount'] = request.json.get('amount', item[0]['amount'])
    item[0]['unit'] = request.json.get('unit', item[0]['unit'])
    item[0]['price'] = request.json.get('price', item[0]['price'])
    item[0]['currency'] = request.json.get('currency', item[0]['currency'])
    item[0]['mod_time'] = time.strftime("%G-%m-%dT%TZ")
    item[0]['mod_person'] = request.json.get('mod_person', 'api')
    return jsonify( { 'item': make_public_item(item[0]) } )


# DEL catalog item
@app.route('/api/v1.0/catalog/<int:item_id>', methods = ['DELETE'])
#@auth.login_required
def delete_item(item_id):
    item = filter(lambda t: t['id'] == item_id, catalog)
    if len(item) == 0:
        abort(404)
    catalog.remove(item[0])
    return jsonify( { 'result': True } )





### TASK 2

# modify items returned throu api
def make_public_basket_item(item):
    new_item = {}
    for field in item:
        if field == 'user_id':
            new_item[field] = item[field]
            new_item['uri'] = url_for('get_basket_item', user_id = item[field], item_id = item['product_id'], _external = False)
        elif field == 'add_time':
            pass
        elif field == 'mod_time':
            pass
        else:
            new_item[field] = item[field]
    return new_item

# GET basket items for user
@app.route('/api/v1.0/basket/<user_id>', methods = ['GET'])
#@auth.login_required
def get_basket_items(user_id):
    items = filter(lambda t: t['user_id'] == user_id, basket)
    if len(items) == 0:
        return jsonify( { 'items': {} } )
    return jsonify( { 'items': map(make_public_basket_item, items) } )


# GET basket item for user
@app.route('/api/v1.0/basket/<user_id>/<int:item_id>', methods = ['GET'])
#@auth.login_required
def get_basket_item(user_id, item_id):
    items = filter(lambda t: t['user_id'] == user_id, basket)
    item = filter(lambda t: t['product_id'] == item_id, items)
    if len(item) == 0:
        abort(404)
    return jsonify( { 'items': map(make_public_basket_item, item) } )


# NEW basket item
@app.route('/api/v1.0/basket', methods = ['POST'])
#@auth.login_required
def create_basket_item():
    if not request.json \
    or not 'user_id' in request.json \
    or not 'product_id' in request.json \
    or not 'amount' in request.json:
        abort(400)
    #if product_id does not exist
    ex_item = filter(lambda t: t['id'] == request.json['product_id'], catalog)
    if len(ex_item) == 0:
        abort(400, {'message': 'product_id does not exist!'})
    #if product_id already in list, (do not allow dublicates)
    user_items = filter(lambda t: t['user_id'] == request.json['user_id'], basket)
    ex_item = filter(lambda t: t['product_id'] == request.json['product_id'], user_items)
    if len(ex_item) > 0:
        abort(400, {'message': 'product_id already listed!'})
    item = {
        'user_id': request.json['user_id'],
        'product_id': request.json['product_id'],
        'amount': request.json['amount'],
        'add_time': time.strftime("%G-%m-%dT%TZ"),
        'mod_time': time.strftime("%G-%m-%dT%TZ")
    }
    basket.append(item)
    return jsonify( { 'item': make_public_basket_item(item) } ), 201


# DEL basket item for user
@app.route('/api/v1.0/basket/<user_id>/<int:item_id>', methods = ['DELETE'])
#@auth.login_required
def delete_basket_item(user_id, item_id):
    items = filter(lambda t: t['user_id'] == user_id, basket)
    if len(items) == 0:
        abort(404)
    for i in items:
        if ( i.get('product_id') == item_id):
            basket.remove(i)
    return jsonify( { 'result': True } )


# MOD basket item
@app.route('/api/v1.0/basket/<user_id>/<int:item_id>', methods = ['PUT'])
#@auth.login_required
def update_basket_item(user_id, item_id):
    items = filter(lambda t: t['user_id'] == user_id, basket)
    item = filter(lambda t: t['product_id'] == item_id, items)
    if len(item) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'amount' in request.json and type(request.json['amount']) is not int:
        abort(400)
    item[0]['amount'] = request.json.get('amount', item[0]['amount'])
    item[0]['mod_time'] = time.strftime("%G-%m-%dT%TZ")
    return jsonify( { 'item': make_public_basket_item(item[0]) } )






if __name__ == '__main__':
    app.run(debug = True)
