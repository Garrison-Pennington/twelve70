import requests, json

BASE_URL = "https://www.everlane.com/api/v3/collections/mens-"
STORE_BASE_URL = "https://www.everlane.com/products/{}?collection=mens-{}"

PAGES = [
    "sweaters",
    "sweatshirts",
    "outerwear",
    "jeans",
    "bottoms",
    "tees",
    "shirt-shop"
    ]

# p = JSON.products[i]
# ProductList def:
#  {
#   name=p.display_name: {
#       store_url:  https://www.everlane.com/products/mens-(PRODUCT NAME)?collection=mens-(COLLECTION),
#       img_url: https://res.cloudinary.com/everlane/image/upload/f_auto,q_auto/v1/i/(IMAGE ID).jpg,
#       alt_img_url: https://res.cloudinary.com/everlane/image/upload/f_auto,q_auto/v1/i/(IMAGE ID).jpg,
#       colors: {
#           p.color.name: {
#               url: https://www.everlane.com/products/mens-(PRODUCT NAME)?collection=mens-(COLLECTION),
#               primary_img_url: https://res.cloudinary.com/everlane/image/upload/f_auto,q_auto/v1/i/(IMAGE ID).jpg,
#               alt_img_url: https://res.cloudinary.com/everlane/image/upload/f_auto,q_auto/v1/i/(IMAGE ID).jpg,
#               available_sizes: ["S","M","L", etc. ]
#           }
#       }
#   }
#   price: p.price
#  }

# String ---> JSON
# GET collection data from everlane as JSON
def getCollectionData(collection):
    try:
        response = requests.get(BASE_URL + collection)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print('HTTP error occurred: {}'.format(http_err))  # Python 3.5
    except Exception as err:
        print('Other error occurred: {}'.format(err))  # Python 3.5
    else:
        print('Success!')
        # Get JSON
        data = response.json()
        return data

# JSON String ---> ProductList (see lines 16-33)
# Parse collection data in ProductList obj
def parseCollectionData(data, collection):
    # Find Products in JSON
    all_products = data['products']
    # Empty dict to put parsed data in
    products = {}
    # Loop over products
    for p in all_products:
        # Get image and store urls for product
        urls = parseUrls(p, collection)
        name = p['display_name']
        color = p['color']['name']
        # Has the same product been found in a different color already?
        if name in products:
            # Add images and page url to colors property
            products[name]['colors'][color] = urls
        else:
            # Create new product entry
            prodObj = {
                'price': p['price'],
                'url': urls['url'],
                'primary_img_url': urls['primary_img_url'],
                'alt_img_url': urls['alt_img_url'],
                'colors': {color:urls}
            }
            products[name] = prodObj
    return products

# JSON String ---> JSON
# Parse specific product urls
def parseUrls(productData,collection):
    primary_img = ''
    alt_img = ''
    for img in productData['albums']['square']:
        if img['tag'] == 'primary':
            primary_img = img['src']
        elif img['tag'] == 'alt':
            alt_img = img['src']

    obj = {
        'primary_img_url': primary_img,
        'url': STORE_BASE_URL.format(productData['permalink'],collection),
        'alt_img_url': alt_img
    }

    return obj

# ProductList String ---> null
# Dump contents of productList to a file name [collection].json
def outputProductList(productList, collection):
    with open('products/' + collection + '.json', 'w') as json_file:
        json.dump(productList,json_file)

# String ---> .json file
# Create a ProductList from everlane Collection and dump file to products folder
def scrapeCollection(collection):
    data = getCollectionData(collection)
    prodList = parseCollectionData(data,collection)
    outputProductList(prodList,collection)

# Scrape all collections in PAGES array
def scrapeEverlane():
    for collection in PAGES:
        scrapeCollection(collection)

scrapeEverlane()
