import json
from flask import Flask
from flask import request, jsonify, session, redirect
import scrapy
import math
from scrapy.selector import Selector
from flask_cors import CORS
from flask_pymongo import PyMongo
import requests
import bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from bson import json_util


# import requests


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['MONGO_DBNAME'] = 'fkexample'
app.config['MONGO_URI'] = 'mongodb+srv://jatin:jatin123@cluster0.1zrdh.mongodb.net/pricedropdb?retryWrites=true&w=majority'
app.secret_key = "super secret key"
app.config['JWT_SECRET_KEY'] = 'jatinjwt-secret-key'
jwt = JWTManager(app)
CORS(app)
mongo = PyMongo(app)

@app.route("/", methods=['GET','POST'])
def homee():
    # print('11111111111111')
    if request.method == 'GET':
        # print('ssss')
        # neww = request.form.get()
        # neww = request.get_json()
        # print(neww)
        return "Successfull Home"

@app.route("/example", methods=['GET','POST'])
def example():
    # print('11111111111111')
    if request.method == 'POST':
        # print('ssss')
        # neww = request.form.get()
        neww = request.get_json()
        # print(neww)
        return neww


@app.route("/111", methods=['GET','POST'])
def exa1():
    # print('0000000000000')
    if request.method == 'POST':

        try:
            # print('zzzzzzz')
            # neww = request.form.get()
            neww = request.get_json()
            # print(neww)

            values = neww['url']
            # print(values)

            x = requests.get(values)

            # print(x.text)

            details = []

            resp = Selector(text=x.text)

            products = resp.css("li.item")

            # print(products)

            for pro in products:

                title = pro.css('div.title > b > a::text').get()

                if not title:
                    # print("Skippppping Product.....NOT FOUND")
                    continue

                
                titleee = title.replace("\n                ", "").replace("\n            ","")



                # plattform = product.css("div.btn-wrap > a.shop-now::text").get()
                # plattformmmmm = plattform.replace("Buy on ","")

                plattform = pro.css("div.btn-wrap > a").attrib['title']
                plattformmmmm = plattform.replace("View ","").replace(" Price History Chart","")



                ffinalprice = pro.css("span.final::text").get()
                if ffinalprice:
                    finalpriceint = int(ffinalprice.replace("\u20b9", "").replace(",", ""))
                elif not ffinalprice:
                    finalpriceint = 0

                

                hhighestprice = pro.css("div.price-overview > div.item:nth-child(2)::text").get()
                if hhighestprice:
                    highestpriceint = int(hhighestprice.replace("\u20b9", "").replace(",", ""))
                elif not hhighestprice:
                    highestpriceint = 0




                llowestprice = pro.css("div.price-overview > div.item:nth-child(1)::text").get()
                if llowestprice:
                    lowestpriceint = int(llowestprice.replace("\u20b9", "").replace(",", ""))
                elif not llowestprice:
                    lowestpriceint = 0




                ddiscountprice = pro.css("span.price-old::text").get()
                if ddiscountprice:
                    dicsountpriceint = int(ddiscountprice.replace("\u20b9", "").replace(",", ""))
                elif not ddiscountprice:
                    dicsountpriceint = finalpriceint




                ppercentage = pro.css("span.percent::text").get()
                if ppercentage:
                    percentageint = int(ppercentage.replace("% Off", ""))
                elif not ppercentage:
                    percentageint = 0




                pproducturl = pro.css("div.btn-wrap > a").attrib['href']
                if pproducturl:
                    producturlshort = pproducturl.replace("/","").replace(".html","")
                elif not pproducturl:
                    producturlshort = ""

                # count = 0

                # title = pro.css('div.title > b > a::text').get()
                
                # # print(pro.css("a.market_listing_row_link").attrib["href"])
                # links = pro.css("a.market_listing_row_link").attrib["href"]

                # # imageurl = pro.css(f"div.market_listing_row").get()
                # imageurl = pro.css(f"div.market_listing_row > img").attrib["src"]

                # # imageurl = pro.css("img#result_0_image").attrib["src"]

                # name = pro.css("span.market_listing_item_name::text").get()
                # quantity = pro.css("span.market_listing_num_listings_qty::text").get()
                # # price = pro.css("span.sale_price::text").get().replace("$", "").replace(" USD", "").replace(",","")
                # pricefirst = pro.css("span.normal_price::text").getall()

                # price = pricefirst[2].replace("$", "").replace(" USD", "").replace(",","")
                # intprice = float(price)
                data = {
                    "producttitle": titleee,
                    "finalprice": finalpriceint,
                    "discountprice": dicsountpriceint,
                    "percent": percentageint,
                    "features": pro.css("div.highlights > ul > li::text").getall(),
                    "producturl": producturlshort,
                    "imageurl": pro.css("div.col-left > a > img").attrib['data-src'],
                    "lowestprice": lowestpriceint,
                    "highestprice": highestpriceint
                }

                details.append(data)

            return jsonify(details)

           
        except:
            return jsonify({"errormessage": "too many request at same time"} )
        


@app.route("/222", methods=['GET','POST'])
def exa():
    # print('11111111111111')
    if request.method == 'POST':
        try:

            # print('ssss')
            # neww = request.form.get()
            neww = request.get_json()
            # print(neww)

            values = neww['url']

            # print(values)


            x = requests.get(values)

            # print(x.content)

            resp = Selector(text=x.content)

            platform = resp.css("span.buy-button > a::text").get()
            productlink = resp.css("span.buy-button > a").attrib["href"]

            # example = resp.css('div.cmo-mod.cmo-product-price-overview > div.bd > div.section > div.item > div.label.lowest + div::text').get()
            # example = resp.css('div.cmo-mod.cmo-product-price-overview > div.bd > div.section > div.item > div.label.highest + div::text').get()
            # print(example)

            lowestprice = resp.css('div.cmo-mod.cmo-product-price-overview > div.bd > div.section > div.item > div.label.lowest + div::text').get()

            if lowestprice:
                lowestpriceint = int(lowestprice.replace("\u20b9", "").replace(",", ""))
            elif not lowestprice:
                lowestpriceint = 0

            hhighestprice = resp.css("div.cmo-mod.cmo-product-price-overview > div.bd > div.section > div.item > div.label.highest + div::text").get()
            if hhighestprice:
                highestpriceint = int(hhighestprice.replace("\u20b9", "").replace(",", ""))
            elif not hhighestprice:
                highestpriceint = 0

            currentprice = resp.css("div.cmo-mod.cmo-product-price-overview > div.bd > div.section > div.item > div.label + div::text").get()
            if currentprice:
                currentpriceint = int(currentprice.replace("\u20b9", "").replace(",", ""))
            elif not currentprice:
                currentpriceint = 0

            features = resp.css("div.cmo-mod.cmo-product-highlights > div.bd > ul > li::text").getall()

            imageurl = resp.css("div.bd > div.cmo-mp-image-frm > img").attrib["src"]

            producttitle = resp.css("div.hd > h1::text").get()

            percent = resp.css('span.discount-percent.js-product-discount-percentage::text').get()

            discountprice = resp.css("span.price-old::text").get()

            data = {
                "platform": platform,
                "productlink": productlink,
                "lowestprice": lowestpriceint,
                "highestprice": highestpriceint,
                "features": features,
                "imageurl": imageurl,
                "product": producttitle,
                "price": currentpriceint,
                "percent": percent,
                "discountprice": discountprice,

            }




            

            
            return jsonify(data)

        except:
            return jsonify({"errormessage": "too many request at same time"} )


@app.route("/333", methods=['GET','POST'])
def exasearch():
    # print('11111111111111')
    if request.method == 'POST':
        try:

            # print('ssss')
            # neww = request.form.get()
            neww = request.get_json()
            # print(neww)

            values = neww['url']

            # print(values)


            x = requests.get(values)

            # print(x.content)

            details = []

            resp = Selector(text=x.content)


            products = resp.css("li.item > div.unit")

            # print(products)

            count = 0

            for pro in products:

                

                count = count + 1

                # print(count)

                # print(0)

                title = pro.css('div.title > h2 > a::text').get()

                # print(title)

                if(title is None):
                    continue

                titleee = title.replace("\n                ", "").replace("\n            ","")

                finalprice = pro.css('div.price > div.final::text').get()
                discountprice = pro.css('div.discount > span.price-old::text').get()
                percentage = pro.css('div.discount > span.percent::text').get()
                link = pro.css('div.btn-wrap > a').attrib["href"]
                if link:
                    producturlshort = link.replace("/","").replace(".html","")
                elif not link:
                    producturlshort = ""

                try:

                    imageurl = pro.css('div.img-wrap > a > img').attrib["data-src"]

                except:
                    imageurl = pro.css('div.img-wrap > a > img').attrib["src"]


                

                
                # print('jjjjjjjjjjjjjjjjjjjjj')
                # print(imageurl)

                # if imageurl is None:
                #     imageurl = pro.css('div.img-wrap > a > img').attrib["src"]


                data = {
                    "producttitle": titleee,
                    "finalprice": finalprice,
                    "discountprice": discountprice,
                    "percent": percentage,
                    # "features": features,
                    "producturl": producturlshort,
                    "imageurl": imageurl,
                    # "lowestprice": lowestpriceint,
                    # "highestprice": highestpriceint
                }

                details.append(data)

            # platform = resp.css("span.buy-button > a::text").get()
            # productlink = resp.css("span.buy-button > a").attrib["href"]

            # data = {
            #     "platform": platform,
            #     "productlink": productlink
            # }




            

            
            return jsonify(details)
        except:
            return jsonify({"errormessage": "too many request at same time"} )
        

@app.route("/444", methods=['GET','POST'])
def login():

    neww = request.get_json()

    users = mongo.db.users
    login_user = users.find_one({'email': neww['email']})

    if login_user:
        if bcrypt.hashpw(neww['password'].encode('utf-8'), login_user['password']) == login_user['password']:
            session['email'] = neww['email']
            # return redirect(url_for)
            # print(login_user['_id'])
            userid = login_user['_id']
            access_token = create_access_token(identity=str(userid))
            # print(access_token)
            return jsonify({'success': 'Successfully Login', 'token': access_token, 'email': login_user['email']})
        else:
            return jsonify({'error': 'Invalid Password'})
    else:
        return jsonify({'error': 'Invalid Email'})

@app.route("/555", methods=['GET','POST'])
def register():

    if request.method == 'POST':
        neww = request.get_json()
        users = mongo.db.users
        existing_user = users.find_one({'email': neww['email']})

        # print('111111111111')
        # print(neww['username'])

        if existing_user is None:
            # print('222222222222')

            hashpass = bcrypt.hashpw(neww['password'].encode('utf-8'), bcrypt.gensalt())
            users.insert_one({'name': neww['username'], 'email': neww['email'], 'password': hashpass})
            session['email'] = neww['email']
            return jsonify({'success': 'Successfully Register'})
        return jsonify({'error': 'Already Register By this Email'})
    

@app.route("/666", methods=['GET','POST'])
def watchlist():

    if request.method == 'POST':
        neww = request.get_json()
        # print(neww)
        users = mongo.db.users
        # existing_user = users.find_one({'name': request.form['username']})
        existing_user = users.find_one({'email': neww['email']})

        # print('111111111111')
        # print(neww['username'])

        product = neww['product']
        price = neww['price']
        highestprice = neww['highestprice']
        lowestprice = neww['lowestprice']
        percent = neww['percent']
        discountprice = neww['discountprice']
        imageurl = neww['imageurl']
        producturl = neww['producturl']

        tractpro = {
            "product": product,
            'price': price,
            'highestprice': highestprice,
            'lowestprice': lowestprice,
            'percent': percent,
            'discountprice': discountprice,
            'imageurl': imageurl,
            'producturl': producturl
        }

        if existing_user:
            # print('222222222222')

            data =  users.find_one_and_update({'email': neww['email']}, {'$push': {'trackedproducts': tractpro}}, upsert = True, new = True)
            
            # print(data)
            # session['email'] = request.form['username']
            return jsonify({'success': 'Successfully Added to Tracked Products','data': json.loads(json_util.dumps(data))})
        else:
            return 'Invalid User'
        

@app.route("/777", methods=['GET','POST'])
def trackedproducts():

    if request.method == 'POST':
        neww = request.get_json()
        # print(neww)
        users = mongo.db.users
        trackedpro = users.find_one({"email": neww['email']}, {'trackedproducts', 'email'})

        if trackedpro is not None:
            # print(trackedpro)
            return jsonify({'data': json.loads(json_util.dumps(trackedpro))})
            
        
        else:
            return jsonify({'error': 'noooo'})
        

@app.route("/888", methods=['GET','POST'])
def checktrackedproducts():

    if request.method == 'POST':
        neww = request.get_json()
        # print(neww)
        users = mongo.db.users
        trackedpro = users.find_one({"email": neww['email']}, {'trackedproducts', 'email'})

        # print(trackedpro['trackedproducts'])
        # print(neww['product'])

        for i in trackedpro['trackedproducts']:
            # print(i['product'])

            if(i['product'] == neww['product']):
                return jsonify({'Found': 'True'})
        return jsonify({'NOTFound': 'True'})
        # check = users.find_one({"email": neww['email'], trackedproducts: { $in: [friend] }});
        # for match in users.find({ "email": neww['email']},{ "trackedproducts": "red" }):
        #     print(match)

        # if trackedpro is not None:
        #     # print(trackedpro)
        #     return jsonify({'data': json.loads(json_util.dumps(trackedpro))})
            
        return 'kkkk'
        # else:
        #     return jsonify({'error': 'noooo'})
            

@app.route("/999", methods=['GET','POST'])
def deletetrackedproducts():

    if request.method == 'POST':
        neww = request.get_json()
        # print(neww)
        users = mongo.db.users

        data = users.find_one_and_update({ 'email' : neww['email'] },{ "$pull" : { "trackedproducts" : { "product" : neww['product']}}} )

        # return 'Done'

        # print(data)

        if data is not None:

            return jsonify({'success': 'Successfully Removed From Tracked Products','data': json.loads(json_util.dumps(data))})
        
        else:
            return jsonify({'error': 'No Product Found'})


@app.route("/100", methods=['GET','POST'])
def addfcmtoken():

    if request.method == 'POST':
        neww = request.get_json()
        print(neww['email'])
        print(neww['fcmtoken'])
        # print(neww['email'])
        if neww['email'] == "":
            # print("NO Email")

            tokencollection = mongo.db.fcmtoken

            data = tokencollection.find_one({'token': neww['fcmtoken']})

            # print(data)
            # print('1111111111111')

            document = {
                "token": neww['fcmtoken']
            }

            if data is None:
                # print('trigger')
                tokencollection.insert_one(document)
                return jsonify({'success': 'Token Added to FCMTOKEN Collection'})
            else:
                return jsonify({'success': "Token Already Exists in FCMTOKEN Collection"})

        users = mongo.db.users
        data =  users.update_one({'email': neww['email']}, {'$addToSet': {'fcmtoken': neww['fcmtoken']}})
        # print(data.raw_result['updatedExisting'])

        if data.raw_result['updatedExisting'] is True:
            return jsonify({'success': 'Successfully Added FCM Token to user {}'.format(neww['email'])})

        else:

            # print('No email Found Saving Token to FCMTOKEN Collection')

            tokencollection = mongo.db.fcmtoken

            data = tokencollection.find_one({'token': neww['fcmtoken']})

            # print(data)

            document = {
                "token": neww['fcmtoken']
            }

            if data is None:
                tokencollection.insert_one(document)
                return jsonify({'success': "Token Added to FCMTOKEN Collection"})
            else:
                return jsonify({'success': "Token Already Exists in FCMTOKEN Collection"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
