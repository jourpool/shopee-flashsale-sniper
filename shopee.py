import requests, re, json, time, logging, sys, schedule, argparse
from itertools import count

#Global Variable
product = {
    'itemId':'0',
    'shopId':'0',
    'promotionId':'0',
    'modelId':'0',
    'price':'0',
    'timestamp':0
}

#Set Logger
logger = logging.getLogger('factory')
fh = logging.FileHandler('process.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(levelname)s: %(funcName)s:%(lineno)d %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(logging.StreamHandler())
logger.setLevel(logging.DEBUG)

#Print Message to Console
def printMsg(msg):
    message = "\n####################################\n" + msg + "\n####################################\n"
    return print(message)

#Get Product Information
def getInfo():
    printMsg("Ngambil informasi produk...")

    #Get itemId and shopeId from url
    if '/product/' in url:
        param = re.search('/product/(.*)[?]', url).group(1).split('/')
        product['itemId'] = param[1]
        product['shopId'] = param[0]
    else:
        param = url.split('.')
        product['itemId'] = param[-1]
        product['shopId'] = param[-2]

    test = product.items()

    #Set API url for product information
    url_api = 'https://shopee.co.id/api/v2/item/get?itemid=' + product['itemId'] + '&shopid=' + product['shopId']
    headers = { 
        'Host': 'shopee.co.id',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'Referer': url
    }

    #Get product information
    response = requests.get(url_api, headers=headers).json()
    logger.info(response)

    #Set Product Information
    try:
        product['modelId'] = str(response['item']['models'][0]['modelid'])
        product['price'] = str(response['item']['flash_sale']['price'])
        product['promotionId'] = str(response['item']['flash_sale']['promotionid'])
        printMsg(response['item']['name'])
    except:
        pass
    
    return True

#Add Product to Cart
def addToCart():
    printMsg("Nambahin ke keranjang dulu cuy..")

    #Set Current Time
    product['timestamp'] = int(time.time())

    #Set API for adding to cart
    api = 'https://shopee.co.id/api/v2/cart/add_to_cart'
    headers = { 
        'x-csrftoken': token,
        'referer': url,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'cookie': cookie
    }
    data = '{"quantity":1,"checkout":true,"update_checkout_only":false,"donot_add_quantity":false,"source":"{\\"refer_urls\\":[]}","client_source":1,"shopid":' + product['shopId'] + ',"itemid":' + product['itemId'] + ',"modelid":' + product['modelId'] + '}'
    payload = json.loads(data)
    logger.info(data)

    #Get response
    response = requests.post(api, headers=headers, json=payload).json()
    logger.info(response)

    return True

#Checkout Item
def checkout():
    printMsg("Kuy checkout barangnya..")

    #Set API item checkout
    api = 'https://shopee.co.id/api/v4/cart/checkout'
    headers = { 
        'origin': 'https://shopee.co.id',
        'content-type': 'application/json',
        'referer': 'https://shopee.co.id/cart/',
        'x-csrftoken': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'cookie': cookie
    }
    data = '{"selected_shop_order_ids":[{"shopid":' + product['shopId'] + ',"item_briefs":[{"itemid":' + product['itemId'] + ',"modelid":' + product['modelId'] + ',"item_group_id":null,"applied_promotion_id":' + product['promotionId'] + ',"offerid":null,"price":' + product['price'] + ',"quantity":1,"is_add_on_sub_item":null,"add_on_deal_id":null,"status":1,"cart_item_change_time":' + str(product['timestamp']) + '}],"shop_vouchers":[]}],"platform_vouchers":[]}'
    payload = json.loads(data)
    logger.info(data)

    #Get response
    response = requests.post(api, headers=headers, json=payload).json()
    logger.info(response)

    return response

#Run the program with scheduler
def runScheduler(hour):
    #Set Scheduler
    schedule.every().day.at(hour).do(lambda: run())

    animation = "|/-\\"

    for i in count(0):
        schedule.run_pending()
        time.sleep(1)
        sys.stdout.write("\r## Nungguin jam flash sale.. Sabar yach.. " + animation[i % len(animation)] + " ##")
        sys.stdout.flush()

#Run the program
def run():
    if getInfo():
        if addToCart():
            if checkout():
                printMsg("Anjay! checkout berhasil coy")

#Set arguments parser
parser = argparse.ArgumentParser(description='Shopee Flashsale Sniper')

parser.add_argument('-url', required=True, type=str, help='URL produk flashsale nya bre')
parser.add_argument('-cookie', required=True, type=str, help='Cookie session nya anjir')
parser.add_argument('-token', required=True, type=str, help='Token nya janglup')
parser.add_argument('--time', type=str, help='Jam piro kalo mau otomatis. Format=JAM:MENIT. Contoh=23:30')

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
if args.time is not None:
    runScheduler(args.time)
else: 
    run()