Simple API



## CHALLENGE

Task was to implement backend application library to product catalog and shopping basket​ of a web shop.

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
To store data, use suitable database engine.



## Running

made to run linux machines with >python2.7 installed


## Install dependences
```
pip install flask
```

## Run api
```
./app.py
```


## Testing with curl

``` bash


# GET catalog
curl "http://localhost:5000/api/v1.0/catalog"

# GET catalog item
curl "http://localhost:5000/api/v1.0/catalog/1"
curl "http://localhost:5000/api/v1.0/catalog/2"

#DELETE item from catalog
curl -X DELETE http://localhost:5000/api/v1.0/catalog/2

#POST new item to catalog
curl -H "Content-Type: application/json" -X POST "http://localhost:5000/api/v1.0/catalog" -d '{"name":"cookies", "price":5.3, "amount":22}'




#POST new item to basket
curl -H "Content-Type: application/json" -X POST -d '{"user_id":"cookie", "product_id":2, "amount":22}' "http://localhost:5000/api/v1.0/basket"

#DELETE item 2 from basket
curl -X DELETE "http://localhost:5000/api/v1.0/basket/cookie/2"

#GET user 'cookie' items
curl "http://localhost:5000/api/v1.0/basket/cookie"

#GET user 'cookie' item 1
curl "http://localhost:5000/api/v1.0/basket/cookie/1"

#DELETE user 'cookie' item 1
curl -X DELETE "http://localhost:5000/api/v1.0/basket/cookie/1"

#PUT new amount to user 'cookie' item 1
curl -H "Content-Type: application/json" -X PUT -d '{"amount":22}' "http://localhost:5000/api/v1.0/basket/cookie/1"




#GET catalog and limit to 1
curl "http://localhost:5000/api/v1.0/catalog?limit=1"

#GET catalog and limit to 1 and sort by price
curl "http://localhost:5000/api/v1.0/catalog?limit=1&sortby=price"


```


--

--

--

--

--

--

## Why this and that

### why python?
Well as it's was suposed to be JSON api I decided it would be easier to do with nodejs or python, as I'm familiar with both languages and JSON is well supported in them both.
In the end I decided to go with a python, as I'm done more testing with python.


### Why dict database?
Not fully reading/undertanding "customer requirements" enough and dict was just easier/faster to start. (missed word "engine" after database...) 

After reaching deadline, I can only blame myself for not choosing SQLITE or some other SQL database from the start, well maybe on version 2.

### why flask?
No particular reason just looked for something simple and fast, flask just looked simpliest from found 3.




## Conlusion

It's a failure because of miss-reading customer requirements about database, leading to do work that need to be re-writed and some can't be done until it's done.
But to be my first api it at least it works for point I did it, maybe with little more time and more planning it could have been completed.

What works: 
 - See section [testing with curl](https://github.com/garismaatti/JSON-api#testing-with-curl)
 - TASK1 - Adding/removing/editing products in product catalog
 - TASK2 - Adding/removing/editing products in shopping basket
 - TASK3 - Querying products from product catalog with row limit and sort by name or price
 - constrain not to add to basked if all is already recerved
 - trying to add basket more then catalog has, will just add what there is left to add


What doesn't:
 - proper SQL-database
 - TASK4. Querying products from product catalog, grouped
 - TASK5. Searching product from catalog
 - Multifile tructure
 - A lot of test and testing missing
 - test are failing
 - shopping basket reservations are never automaticly canceled
 - missing encryption (may be done with nginx)
 - missing authentication
 - non-exist database missing salt/encryption



