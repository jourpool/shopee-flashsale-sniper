import requests, re, json, time, logging, sys, schedule, argparse
from itertools import count
from datetime import date, timedelta
from hashlib import md5

#Global Variable
origin = 'https://shopee.co.id'
userAgent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
refererCart = 'https://shopee.co.id/cart/'

#Set Logger
logger = logging.getLogger('Sniper')
fh = logging.FileHandler('process.log', 'w', 'utf-8')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
#logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

#Get Product Information
def getInfo(itemId, shopId, price, modelId, promotionId):
    print("\nInitializing Attack..")

    global product
    product = {}
    product['itemId'] = itemId
    product['shopId'] = shopId
    product['price'] = price
    product['modelId'] = modelId
    product['promotionId'] = promotionId
    
    return True

#Get Product Information without data provided
def getInfoWithoutData():
    print("\nInitializing Attack..")

    global product
    product = {}

    #Get itemId and shopeId from url
    if '/product/' in url:
        param = re.search('/product/(.*)[?]', url).group(1).split('/')
        product['itemId'] = param[1]
        product['shopId'] = param[0]
    else:
        param = url.split('.')
        product['itemId'] = param[-1]
        product['shopId'] = param[-2]

    #Set API url for product information
    url_api = 'https://shopee.co.id/api/v2/item/get?itemid=' + product['itemId'] + '&shopid=' + product['shopId']
    headers = { 
        'Referer': url,
        'user-agent': userAgent
    }

    #Get product information
    response = requests.get(url_api, headers=headers).json()
    logger.info(response)

    #Set Product Information
    try:
        product['modelId'] = str(response['item']['models'][0]['modelid'])
        product['price'] = str(response['item']['flash_sale']['price'])
        product['promotionId'] = str(response['item']['flash_sale']['promotionid'])
        print("\nTarget Acquired: " + response['item']['name'])
    except:
        pass
    
    return True

#Add Product to Cart
def addToCart():
    print("\nProcessing Items..")

    #Set Current Time
    product['timestamp'] = int(time.time())

    #Set API for adding to cart
    api = 'https://shopee.co.id/api/v2/cart/add_to_cart'
    headers = { 
        'referer': url,
        'cookie': cookie,
        'x-csrftoken': token,
        'user-agent': userAgent
    }
    data = '{"quantity":1,"checkout":true,"update_checkout_only":false,"donot_add_quantity":false,"source":"{\\"refer_urls\\":[]}","client_source":1,"shopid":' + product['shopId'] + ',"itemid":' + product['itemId'] + ',"modelid":' + product['modelId'] + '}'
    payload = json.loads(data)
    logger.info(data)

    #Get response
    response = requests.post(api, headers=headers, json=payload).json()
    logger.info(response)
    print(response)

    return True

#Checkout Item
def checkout():
    print("\nPushing All Items..")

    #Set API item checkout
    api = 'https://shopee.co.id/api/v4/cart/checkout'
    headers = { 
        'origin': origin,
        'cookie': cookie,
        'x-csrftoken': token,
        'referer': refererCart,
        'user-agent': userAgent,
        'content-type': 'application/json'
    }
    data = '{"selected_shop_order_ids":[{"shopid":' + product['shopId'] + ',"item_briefs":[{"itemid":' + product['itemId'] + ',"modelid":' + product['modelId'] + ',"item_group_id":null,"applied_promotion_id":' + product['promotionId'] + ',"offerid":null,"price":' + product['price'] + ',"quantity":1,"is_add_on_sub_item":null,"add_on_deal_id":null,"status":1,"cart_item_change_time":' + str(product['timestamp']) + '}],"shop_vouchers":[]}],"platform_vouchers":[]}'
    payload = json.loads(data)
    logger.info(data)

    #Get response
    response = requests.post(api, headers=headers, json=payload).json()
    logger.info(response)
    print(response)

    return response

def getCheckout():
    print("\nGathering All Information..")

    #Set API item checkout
    api = 'https://shopee.co.id/api/v2/checkout/get'
    headers = { 
        'origin': origin,
        'cookie': cookie,
        'x-csrftoken': token,
        'referer': refererCart,
        'user-agent': userAgent,
        'content-type': 'application/json',
    }
    data = '{"shoporders":[{"shop":{"shopid":' + product['shopId'] + '},"items":[{"itemid":' + product['itemId'] + ',"modelid":' + product['modelId'] + ',"add_on_deal_id":null,"is_add_on_sub_item":null,"item_group_id":null,"quantity":1}],"logistics":{"recommended_channelids":null},"buyer_address_data":{},"selected_preferred_delivery_time_slot_id":null}],"selected_payment_channel_data":{},"promotion_data":{"use_coins":false,"free_shipping_voucher_info":{"free_shipping_voucher_id":0,"disabled_reason":"","description":""},"platform_vouchers":[],"shop_vouchers":[],"check_shop_voucher_entrances":true,"auto_apply_shop_voucher":false},"device_info":{"device_id":"","device_fingerprint":"","tongdun_blackbox":"","buyer_payment_info":{}},"tax_info":{"tax_id":""}}'
    payload = json.loads(data)
    logger.info(data)

    #Get response
    response = requests.post(api, headers=headers, json=payload).json()
    logger.info(response)

    #Set gathered checkout information
    global checkoutData
    checkoutData = json.loads(json.dumps(response))

    return True

def pay():
    print("\nSending The Attack..")

    #Set API payment
    api = 'https://shopee.co.id/api/v2/checkout/place_order'
    headers = {
        'origin': origin,
        'cookie': cookie,
        'x-csrftoken': token,
        'user-agent': userAgent,
        'content-type': 'application/json',
        'referer': 'https://shopee.co.id/checkout/'
    }

    data = checkoutData

    try: 
        data['shoporders'][0]['buyer_ic_number'] = ''
    except:
        pass
    try:
        data['shipping_orders'][0]['buyer_ic_number'] = ''
    except:
        pass
    try:
        data['shoporders'][0]['ext_ad_info_mappings'] = []
    except:
        pass

    data['status'] = 200
    data['headers'] = {}

    payload = json.loads(json.dumps(data))

    #Get response
    response = requests.post(api, headers=headers, json=payload).json()
    logger.info(response)
    print(response)

    return True

#Basic Authentication
def auth(pwd):
    day1 = date.today()
    day2 = day1 + timedelta(days=1)

    key = str(day1.day).encode('utf-8')
    key2 = str(day2.day).encode('utf-8') 

    encrypted = md5(key).hexdigest()[:4]
    encrypted2 = md5(key2).hexdigest()[:4]

    if pwd == encrypted or pwd == encrypted2:
        return True

    return False

#Run the program with scheduler
def runScheduler(hour):
    #Set Scheduler
    schedule.every().day.at(hour).do(lambda: run())

    animation = "|/-\\"
    print("\n")

    for i in count(0):
        schedule.run_pending()
        time.sleep(1)
        sys.stdout.write("\rWaiting For The Scheduler to Execute The Attack (" + hour + ")" + animation[i % len(animation)])
        sys.stdout.flush()

#Run the program
def run():
        if not (args.itemid or args.shopid or args.price or args.modelid or args.promotionid):
            getInfoWithoutData()
        else:
            getInfo(args.itemid, args.shopid, args.price, args.modelid, args.promotionid)
        addToCart()
        checkout()
        getCheckout()
        pay()
        print("\nEnd of attack!")

#Set arguments parser
parser = argparse.ArgumentParser(description='Shopee Flashsale Sniper')

parser.add_argument('-pwd', required=True, type=str, help='Password to execute')
parser.add_argument('-url', required=True, type=str, help='Flashsale Product URL')
parser.add_argument('-cookie', required=True, type=str, help='User Session Cookie')
parser.add_argument('-token', required=True, type=str, help='User Token')
parser.add_argument('--time', type=str, help='Time of Attack. Format=HH:MM. Example=23:30')

parser.add_argument('--itemid', type=str, help='itemId of the product.')
parser.add_argument('--shopid', type=str, help='shopId of the product.')
parser.add_argument('--price', type=str, help='Discounted price of the product.')
parser.add_argument('--modelid', type=str, help='modelId of the product variant.')
parser.add_argument('--promotionid', type=str, help='promotionId of the flash sale.')

args = parser.parse_args()

#Check if argument exist
if not (args.url or args.cookie or args.token):
    parser.print_help()
    sys.exit()

#Set arguments
url = args.url
token = args.token
cookie = args.cookie

#Execute
if auth(args.pwd):
    if args.time is not None:
        runScheduler(args.time)
    else: 
        run()
else:
    print("\nIncorrect Password")