import requests

BASE_URL = "https://www.everlane.com/api/v3/collections/mens-"

pages = [
    "sweaters",
    "sweatshirts"
    "outerwear",
    "jeans",
    "bottoms",
    "tees",
    "shirt-shop"
    ]

driver = webdriver.Chrome()

def getAndPrintHTML(url):
    try:
        response = requests.get(url)

        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print('HTTP error occurred: {}'.format(http_err))  # Python 3.6
    except Exception as err:
        print('Other error occurred: {}'.format(err))  # Python 3.6
    else:
        print('Success!')
        data = response.json()
        
        #print(response.text)

#getAndPrintHTML(BASE_URL + pages[0])
