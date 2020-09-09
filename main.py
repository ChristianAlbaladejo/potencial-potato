import pyodbc
import socket

import requests as req
from flask_caching import Cache
from flask import Flask, json, request, render_template, jsonify
from flask_cors import CORS, cross_origin
from decouple import config

colours = {"aliceblue": "#f0f8ff", "Blanca": "#faebd7", "aqua": "#00ffff", "aquamarine": "#7fffd4", "azure": "#f0ffff",
           "beige": "#f5f5dc", "bisque": "#ffe4c4", "black": "#000000", "blanchedalmond": "#ffebcd", "blue": "#0000ff",
           "blueviolet": "#8a2be2", "brown": "#a52a2a", "burlywood": "#deb887",
           "cadetblue": "#5f9ea0", "chartreuse": "#7fff00", "chocolate": "#d2691e", "coral": "#ff7f50",
           "cornflowerblue": "#6495ed", "cornsilk": "#fff8dc", "crimson": "#dc143c", "cyan": "#00ffff",
           "darkblue": "#00008b", "darkcyan": "#008b8b", "darkgoldenrod": "#b8860b", "darkgray": "#a9a9a9",
           "darkgreen": "#006400", "darkkhaki": "#bdb76b", "darkmagenta": "#8b008b", "darkolivegreen": "#556b2f",
           "darkorange": "#ff8c00", "darkorchid": "#9932cc", "darkred": "#8b0000", "darksalmon": "#e9967a",
           "darkseagreen": "#8fbc8f", "darkslateblue": "#483d8b", "darkslategray": "#2f4f4f",
           "darkturquoise": "#00ced1",
           "darkviolet": "#9400d3", "deeppink": "#ff1493", "deepskyblue": "#00bfff", "dimgray": "#696969",
           "dodgerblue": "#1e90ff",
           "firebrick": "#b22222", "floralwhite": "#fffaf0", "forestgreen": "#228b22", "fuchsia": "#ff00ff",
           "gainsboro": "#dcdcdc", "ghostwhite": "#f8f8ff", "gold": "#ffd700", "goldenrod": "#daa520",
           "gray": "#808080", "green": "#008000", "greenyellow": "#adff2f",
           "honeydew": "#f0fff0", "hotpink": "#ff69b4",
           "indianred ": "#cd5c5c", "indigo": "#4b0082", "ivory": "#fffff0", "khaki": "#f0e68c",
           "lavender": "#e6e6fa", "lavenderblush": "#fff0f5", "lawngreen": "#7cfc00", "lemonchiffon": "#fffacd",
           "lightblue": "#add8e6", "lightcoral": "#f08080", "lightcyan": "#e0ffff", "lightgoldenrodyellow": "#fafad2",
           "lightgrey": "#d3d3d3", "lightgreen": "#90ee90", "lightpink": "#ffb6c1", "lightsalmon": "#ffa07a",
           "lightseagreen": "#20b2aa", "lightskyblue": "#87cefa", "lightslategray": "#778899",
           "lightsteelblue": "#b0c4de",
           "lightyellow": "#ffffe0", "lime": "#00ff00", "limegreen": "#32cd32", "linen": "#faf0e6",
           "magenta": "#ff00ff", "maroon": "#800000", "mediumaquamarine": "#66cdaa", "mediumblue": "#0000cd",
           "mediumorchid": "#ba55d3", "mediumpurple": "#9370d8", "mediumseagreen": "#3cb371",
           "mediumslateblue": "#7b68ee",
           "mediumspringgreen": "#00fa9a", "mediumturquoise": "#48d1cc", "mediumvioletred": "#c71585",
           "midnightblue": "#191970", "mintcream": "#f5fffa", "mistyrose": "#ffe4e1", "moccasin": "#ffe4b5",
           "navajowhite": "#ffdead", "navy": "#000080",
           "oldlace": "#fdf5e6", "olive": "#808000", "olivedrab": "#6b8e23", "orange": "#ffa500",
           "orangered": "#ff4500", "orchid": "#da70d6",
           "palegoldenrod": "#eee8aa", "palegreen": "#98fb98", "paleturquoise": "#afeeee", "palevioletred": "#d87093",
           "papayawhip": "#ffefd5", "peachpuff": "#ffdab9", "peru": "#cd853f", "pink": "#ffc0cb", "plum": "#dda0dd",
           "powderblue": "#b0e0e6", "purple": "#800080",
           "rebeccapurple": "#663399", "red": "#ff0000", "rosybrown": "#bc8f8f", "royalblue": "#4169e1",
           "saddlebrown": "#8b4513", "salmon": "#fa8072", "sandybrown": "#f4a460", "seagreen": "#2e8b57",
           "seashell": "#fff5ee", "sienna": "#a0522d", "silver": "#c0c0c0", "skyblue": "#87ceeb",
           "slateblue": "#6a5acd", "slategray": "#708090", "snow": "#fffafa", "springgreen": "#00ff7f",
           "steelblue": "#4682b4",
           "tan": "#d2b48c", "teal": "#008080", "thistle": "#d8bfd8", "tomato": "#ff6347", "turquoise": "#40e0d0",
           "violet": "#ee82ee",
           "wheat": "#f5deb3", "white": "#ffffff", "whitesmoke": "#f5f5f5",
           "yellow": "#ffff00", "yellowgreen": "#9acd32"};

api = Flask(__name__)
cache = Cache(api, config={"CACHE_TYPE": "simple", "CACHE_DEFAULT_TIMEOUT": "10"})
cors = CORS(api)
api.config['CORS_HEADERS'] = 'Content-Type'
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=' + config('SERVER_NAME') + ';'
                                                          'username=' + config('SERVER_USERNAME') + ';'
                                                                                                    'password=' + config(
    'SERVER_PASS') + ';'
                     'Database=' + config('SERVER_DATABASE') + ';'
                                                               'Trusted_Connection=yes;')
cache.init_app(api)


@api.route('/', methods=['GET'])
def get_warehouse():
    api.logger.info(f'Entramos al path {request.path}')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM igtposretail.dbo.Warehouse')
    data = cursor.fetchall()
    tables = []
    column_names = [column[0] for column in cursor.description]
    for row in data:
        tables.append(dict(zip(column_names, row)))
    return json.dumps(tables)


@api.route('/api/show/<name>')
def test_api(name):
    values = {'name': name}
    return jsonify(values)


@api.route('/api/getShopifyProducts', methods=['GET'])
def getShopifyProducts():
    r = req.get(
        url=config('API_URL') + '/admin/api/2020-07/products.json')
    data = r.json()
    for i in data['products']:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM igtposretail.dbo.Product WHERE igtposretail.dbo.Product.Name = '" + i['title'] + "'")
        cursor_data = cursor.fetchall()
        if not cursor_data:
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(Id) + 1 FROM igtposretail.dbo.SizeGroup")
            cursor_data = cursor.fetchall()
            tables = []
            column_names = [column[0] for column in cursor.description]
            for row in cursor_data:
                tables.append(dict(zip(column_names, row)))
            sizeGroupId = str(tables[0][''])
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(Id) + 1 FROM igtposretail.dbo.Size")
            cursor_data = cursor.fetchall()
            tables = []
            column_names = [column[0] for column in cursor.description]
            for row in cursor_data:
                tables.append(dict(zip(column_names, row)))
            sizeId = str(tables[0][''])
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(Id) + 1 FROM igtposretail.dbo.Color")
            cursor_data = cursor.fetchall()
            tables = []
            column_names = [column[0] for column in cursor.description]
            for row in cursor_data:
                tables.append(dict(zip(column_names, row)))
            colorId = str(tables[0][''])
            cursor = conn.cursor()
            cursor.execute("SELECT MAX(Id) + 1 FROM igtposretail.dbo.ColorGroup")
            cursor_data = cursor.fetchall()
            tables = []
            column_names = [column[0] for column in cursor.description]
            for row in cursor_data:
                tables.append(dict(zip(column_names, row)))
            colorGroupId = str(tables[0][''])
            sizes = ''
            colors = ""
            for x in i["variants"]:
                if not x['option1'] is None:
                    sizes += x['option1'] + " "
                if not x['option2'] is None:
                    colors += x['option2'] + " "
            sizescut = sizes.split()
            sizes = ' '.join(sorted(set(sizescut), key=sizescut.index))
            sizesName = sizes
            words = colors.split()
            colors = ' '.join(sorted(set(words), key=words.index))
            colorName = colors
            colors = colors.split()
            sizes = sizes.split()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM igtposretail.dbo.SizeGroup WHERE igtposretail.dbo.SizeGroup.Name = '" + sizesName + "'")
            cursor_data = cursor.fetchall()
            if not cursor_data:
                if not x['option1'] is None:
                    lines = ""
                    for idx, y in enumerate(sizes):
                        id = int(sizeId) + idx
                        lines += "<Size Id ='" + str(id) + "' Name='" + y + "'/>"
                    xml = """<?xml version='1.0' encoding='utf-8'?>
                    <Export>
                    <SizeGroups>
                        <SizeGroup Id='""" + sizeGroupId + """' Name='""" + sizesName + """'>
                            <Sizes>
                               """ + lines + """
                            </Sizes>
                        </SizeGroup>
                    </SizeGroups>
                    </Export>"""
                    headers = {
                        "Content-Type": "application/xml; charset=utf-8",
                        "Accept": "application/xml",
                        "Api-Token": config('AGORA_API_TOKEN')
                    }
                    r = req.post('http://localhost:9984/api/import/', data=xml, headers=headers)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM igtposretail.dbo.ColorGroup WHERE igtposretail.dbo.ColorGroup.Name = '" + colorName + "'")
            cursor_data = cursor.fetchall()
            if not cursor_data:
                if not x['option2'] is None:
                    lines = ""
                    for idx, y in enumerate(colors):
                        id = int(colorId) + idx
                        if y in colours:
                            lines += "<Color Id ='" + str(id) + "' Name='" + y + "' Value='" + colours[y] + "'/>"
                        else:
                            lines += "<Color Id ='" + str(id) + "' Name='" + y + "' Value='#000000'/>"
                    xml = """<?xml version='1.0' encoding='utf-8'?>
                                <Export>
                                    <ColorGroups>
                                        <ColorGroup Id='""" + colorGroupId + """' Name='""" + colorName + """'>
                                            <Colors>
                                               """ + lines + """
                                            </Colors>
                                        </ColorGroup>
                                    </ColorGroups>
                                    </Export>"""
                    headers = {
                        "Content-Type": "application/xml; charset=utf-8",
                        "Accept": "application/xml",
                        "Api-Token": config('AGORA_API_TOKEN')
                    }
                    r = req.post('http://localhost:9984/api/import/', data=xml, headers=headers)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM igtposretail.dbo.Family WHERE igtposretail.dbo.Family.Name = '" + i[
                'product_type'] + "'")
            cursor_data = cursor.fetchall()
            if not cursor_data:
                cursor = conn.cursor()
                cursor.execute("SELECT MAX(Id) + 1 FROM igtposretail.dbo.Family")
                cursor_data = cursor.fetchall()
                tables = []
                column_names = [column[0] for column in cursor.description]
                for row in cursor_data:
                    tables.append(dict(zip(column_names, row)))
                familyId = str(tables[0][''])
                xml = """<?xml version='1.0' encoding='utf-8'?>
                            <Export>
                                <Families>
                                    <Family Id='""" + familyId + """' Name='""" + i['product_type'] + """' 
                                    Color="#BACDE2" Order="1"/> </Families> </Export> """
                headers = {
                    "Content-Type": "application/xml; charset=utf-8",
                    "Accept": "application/xml",
                    "Api-Token": config('AGORA_API_TOKEN')
                }
                r = req.post('http://localhost:9984/api/import/', data=xml, headers=headers)

            cursor = conn.cursor()
            cursor.execute("SELECT MAX(Id) + 1 FROM igtposretail.dbo.Product")
            cursor_data = cursor.fetchall()
            tables = []
            column_names = [column[0] for column in cursor.description]
            for row in cursor_data:
                tables.append(dict(zip(column_names, row)))
            productId = str(tables[0][''])

            cursor = conn.cursor()
            cursor.execute("SELECT Id FROM igtposretail.dbo.Family where Name='" + i['product_type'] + "'")
            cursor_data = cursor.fetchall()
            tables = []
            column_names = [column[0] for column in cursor.description]
            for row in cursor_data:
                tables.append(dict(zip(column_names, row)))
            familyId = str(tables[0]['Id'])
            barcodes = ""
            prices = ""
            for row in i['variants']:
                prices += row['price'] + ' '
                if not row['barcode'] == "":
                    barcodes += "<Barcode Value='" + row['barcode'] + "'/>"
            prices = prices.split()
            prices = ' '.join(sorted(set(prices), key=prices.index))
            prices = prices.split()
            pricelist = ''
            for r in prices:
                pricelist += "<Price PriceListId='1' Price='" + r + "'/>"
            if sizesName != "Única":
                if sizesName:
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id FROM igtposretail.dbo.SizeGroup where Name='" + sizesName + "'")
                    cursor_data = cursor.fetchall()
                    tables = []
                    column_names = [column[0] for column in cursor.description]
                    for row in cursor_data:
                        tables.append(dict(zip(column_names, row)))
                    sizeGroupId = str(tables[0]['Id'])
            else:
                sizeGroupId = 1
            if colorName:
                cursor = conn.cursor()
                cursor.execute("SELECT Id FROM igtposretail.dbo.ColorGroup where Name='" + colorName + "'")
                cursor_data = cursor.fetchall()
                tables = []
                column_names = [column[0] for column in cursor.description]
                for row in cursor_data:
                    tables.append(dict(zip(column_names, row)))
                colorGroupId = str(tables[0]['Id'])
            # fetch Storage Options
            storageOptions = ""
            for x in i["variants"]:
                if x['option1'] is None or x['option1'] == "Default Title":
                    sizeGroupId = ""
                if x['option2'] is None:
                    colorGroupId = ""
                if sizeGroupId != "":
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id FROM igtposretail.dbo.Size where Name='" + str(x['option1']) + "' and "
                                                                                                             "SizeGroupId='" + str(
                        sizeGroupId) + "'")
                    cursor_data = cursor.fetchall()
                    tables = []
                    column_names = [column[0] for column in cursor.description]
                    for row in cursor_data:
                        tables.append(dict(zip(column_names, row)))
                        sizeId = str(tables[0]['Id'])
                if colorGroupId != "":
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id FROM igtposretail.dbo.Color where Name='" + str(x[
                                                                                                  'option2']) + "' and ColorGroupId='" + str(
                        colorGroupId) + "'")
                    cursor_data = cursor.fetchall()
                    tables = []
                    column_names = [column[0] for column in cursor.description]
                    for row in cursor_data:
                        tables.append(dict(zip(column_names, row)))
                        colorId = str(tables[0]['Id'])
                if x['option1'] == "Default Title" and x['option2'] is not None:
                    sizeGroupId = 1
                if sizeGroupId == 1:
                    sizeId = 1
                if colorGroupId or sizeGroupId != "":
                    storageOptions += "<StorageOption WarehouseId='1' ColorId='" + str(colorId) + "' SizeId='" + str(
                        sizeId) + "' Location='' MinStock='0' MaxStock='" + str(
                        x['inventory_quantity']) + "'/>"
                else:
                    storageOptions += "<StorageOption WarehouseId='1' Location='' MinStock='1' MaxStock='" + str(
                        x['inventory_quantity']) + "'/>"
            xml = """<?xml version="1.0" encoding="utf-8" standalone="yes"?>
            <Export>
                <Products>
                    <Product Id='""" + productId + """' Name='""" + i['handle'] + """' FamilyId='""" + familyId + """' VatId='4'
            ButtonText='""" + i['body_html'] + """' Color='#FFFFFF'
            Order="1" SizeGroupId='""" + str(sizeGroupId) + """' 
            UseAsDirectSale="true"
            PrintWhenPriceIsZero="false"
            ColorGroupId='""" + str(colorGroupId) + """'  IsSoldByWeight="false">
                        <Barcodes>
                            """ + barcodes + """
                        </Barcodes>
                        <StorageOptions>
                            """ + storageOptions + """
                        </StorageOptions>
                        <Prices>
                            """ + pricelist + """
                        </Prices>
                    </Product>
                </Products>
            </Export>"""
            print(xml)
            headers = {
                "Content-Type": "application/xml; charset=utf-8",
                "Accept": "application/xml",
                "Api-Token": config('AGORA_API_TOKEN')
            }
            r = req.post('http://localhost:9984/api/import/', data=xml, headers=headers)
            print(r.text)

            for x in i["variants"]:
                print('a')
                if sizeGroupId != "" and colorGroupId != "":
                    cursor = conn.cursor()
                    cursor.execute("SELECT Id FROM igtposretail.dbo.Size where Name='" + str(x['option1']) + "' and "
                                                                                                             "SizeGroupId='" + str(
                        sizeGroupId) + "'")
                    cursor_data = cursor.fetchall()
                    tables = []
                    column_names = [column[0] for column in cursor.description]
                    for row in cursor_data:
                        tables.append(dict(zip(column_names, row)))
                        sizeId = str(tables[0]['Id'])

                    cursor = conn.cursor()
                    cursor.execute("SELECT Id FROM igtposretail.dbo.Color where Name='" + str(x[
                                                                                                  'option2']) + "' and ColorGroupId='" + str(
                        colorGroupId) + "'")
                    cursor_data = cursor.fetchall()
                    tables = []
                    column_names = [column[0] for column in cursor.description]
                    for row in cursor_data:
                        tables.append(dict(zip(column_names, row)))
                        colorId = str(tables[0]['Id'])
                    cursor = conn.cursor()
                    cursor.execute("UPDATE [igtposretail].[dbo].[StorageOptions] set Shopify_Id = '" + str(x[
                                                                                                               'inventory_item_id']) + "' where ProductId = " + productId + " and SizeId = " + sizeId + " and ColorId = " + colorId + ";")
                    conn.commit()
                    print(cursor)
                else:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE [igtposretail].[dbo].[StorageOptions] set Shopify_Id = '" + str(x[
                                                                                                               'inventory_item_id']) + "' where ProductId = " + productId + " and SizeId IS NULL and ColorId IS NULL;")
                    conn.commit()
                    print(cursor)

    return str(data)


@api.route('/api/updateStock', methods=['GET'])
def updateStock():
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT SUM(QuantityInSaleUnit) as Total, StorageOptions.shopify_Id from [igtposretail].["
                   "dbo].[Movement] INNER JOIN [igtposretail].[dbo].[StorageOptions] ON "
                   "Movement.ProductId=StorageOptions.ProductId and Movement.ColorId=StorageOptions.ColorId and "
                   "Movement.SizeId=StorageOptions.SizeId GROUP BY Movement.ProductId, Movement.SizeId, "
                   "Movement.ColorId, StorageOptions.shopify_Id")
    cursor_data = cursor.fetchall()
    tables = []
    column_names = [column[0] for column in cursor.description]
    for row in cursor_data:
        tables.append(dict(zip(column_names, row)))

    for x in tables:
        a = int(x['Total'])
        r = req.get(
            url=config('API_URL') + '/admin/api/2019-04/inventory_levels.json?inventory_item_ids=' + x['shopify_Id'])
        data = r.json()
        body = {
            "location_id": data['inventory_levels'][0]['location_id'],
            "inventory_item_id": x['shopify_Id'],
            "available_adjustment": a
        }
        r = req.post(
            url=config('API_URL') + '/admin/api/2020-07/inventory_levels/adjust.json', data=body)
        print(r.text)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Movement;")
        conn.commit()

    return 'tables'


ip = socket.gethostbyname(socket.gethostname())


@api.errorhandler(404)
def page_not_found(error):
    return render_template('error404.html', error=error), 404


if __name__ == '__main__':
    api.run(host=ip)
