import requests

BASE_URL = "https://www.everlane.com/api/v3/collections/mens-"
STORE_BASE_URL = "https://www.everlane.com/products/{}?collection=mens-{}"

pages = [
    "sweaters",
    "sweatshirts"
    "outerwear",
    "jeans",
    "bottoms",
    "tees",
    "shirt-shop"
    ]

# p = JSON.products[i]
# products def:
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

def scrapeEverlane(collection):
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
        data = response.json()
        all_products = data['products']
        products = {}
        for p in all_products:

            primary_img = ''
            alt_img = ''
            for img in p['albums']['square']:
                if img['tag'] == 'primary':
                    primary_img = img['src']
                elif img['tag'] == 'alt':
                    alt_img = img['src']
            
            obj = {
                'primary_img_url': primary_img,
                'url': STORE_BASE_URL.format(p['permalink'],collection),
                'alt_img_url': alt_img
            }

            if p['display_name'] in products:
                products[p['display_name']]['colors'][p['color']['name']] = obj
            else:
                prodObj = {
                    'price': p['price'],
                    'url': STORE_BASE_URL.format(p['permalink'],collection),
                    'primary_img_url': primary_img,
                    'alt_img_url': alt_img,
                    'colors': {p['color']['name']:obj}
                }
                products[p['display_name']] = prodObj
        return products

        #print(response.text)

print(scrapeEverlane(pages[0]))
