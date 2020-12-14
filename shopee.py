import requests, re, json, time, logging, sys, schedule
from itertools import count

#Global Variable
itemId = '0'
shopId = '0'
promotionId = '0'
modelId = '0'
price = '0'
timestamp = 0

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
def getInfo(url):
    printMsg("Ngambil informasi produk...")

    global itemId
    global shopId
    global promotionId
    global modelId
    global price

    #Get itemId and shopeId from url
    if '/product/' in url:
        param = re.search('/product/(.*)[?]', url).group(1).split('/')
        itemId = param[1]
        shopId = param[0]
    else:
        param = url.split('.')
        itemId = param[-1]
        shopId = param[-2]

    #Set API url for product information
    url_api = 'https://shopee.co.id/api/v2/item/get?itemid=' + itemId + '&shopid=' + shopId
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
        modelId = str(response['item']['models'][0]['modelid'])
        price = str(response['item']['flash_sale']['price'])
        promotionId = str(response['item']['flash_sale']['promotionid'])
    except:
        pass
    
    return True

#Add Product to Cart
def addToCart():
    printMsg("Nambahin ke keranjang dulu cuy..")

    #Set Current Time
    global timestamp
    timestamp = int(time.time())

    #Set API for adding to cart
    api = 'https://shopee.co.id/api/v2/cart/add_to_cart'
    headers = { 
        'x-csrftoken': 'VJfuneWDQRzrU3QFgUvijbErFRHku6M9',
        'referer': 'https://shopee.co.id/Chuba-Cassava-Chips-Rasa-Sambal-Balado-Ijo-60-gr-Triple-Pack-i.40079377.5145838119',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'cookie': 'SPC_IA=-1; SPC_F=9awTBIZES0uYFNkfmvsUzgJJbUrlfY2W; REC_T_ID=5591070a-76c9-11e9-b8e7-f898efc7166d; G_ENABLED_IDPS=google; SPC_CLIENTID=9awTBIZES0uYFNkfusezgxuaruhgvumz; SC_DFP=Eva3li3Ef1YLX6wg8YhiUf1nznTpZMDK; SPC_SI=mall.Se8WgeNKzPFRrNhjMfE9yHWtBonTXmwO; csrftoken=VJfuneWDQRzrU3QFgUvijbErFRHku6M9; welcomePkgShown=true; SPC_U=144737012; SPC_EC=IrO9Qek/PCPHL7nGlM/1379L2KjaGM4mAQQVwB8dJ+vf94HTT+A9lTnfZtR6GRpdg2bQBbXGdEPy3noZnRSl/3TgRDu3pQdbIMqOKqYv4aPV5AS2h5wxa2lnIPcY+doc5em+Makb9zxy9DUOViCICWhiQZmpC/7BKKNFl4iCvHY=; _gcl_au=1.1.402160856.1607854379; _fbp=fb.2.1607854379239.154716612; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.3.1156611057.1607854380; _dc_gtm_UA-61904553-8=1; REC_B_MD_7=1607854780_0.30.0.37; REC_MD_36=1607855363; _ga_SW6D8G0HXK=GS1.1.1607854379.1.1.1607854766.0; _ga=GA1.3.1413019161.1607854379; SPC_R_T_ID="Y0P4aw4QiEazQGfc0cKYIQq7IUN5pGToE2aHHpRoTUw361H/aPWAvEU/sse8u6LnF3NpDjk8eqds2TP6Sl7BgprjAB2trjyNqI4nwzWr6NQ="; SPC_T_IV="X674sZB3zttsyi2/d9JyPQ=="; SPC_R_T_IV="X674sZB3zttsyi2/d9JyPQ=="; SPC_T_ID="Y0P4aw4QiEazQGfc0cKYIQq7IUN5pGToE2aHHpRoTUw361H/aPWAvEU/sse8u6LnF3NpDjk8eqds2TP6Sl7BgprjAB2trjyNqI4nwzWr6NQ="'
    }
    data = '{"quantity":1,"checkout":true,"update_checkout_only":false,"donot_add_quantity":false,"source":"{\\"refer_urls\\":[]}","client_source":1,"shopid":' + shopId + ',"itemid":' + itemId + ',"modelid":' + modelId + '}'
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
        'x-csrftoken': 'VJfuneWDQRzrU3QFgUvijbErFRHku6M9',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'cookie': 'SPC_IA=-1; SPC_F=9awTBIZES0uYFNkfmvsUzgJJbUrlfY2W; REC_T_ID=5591070a-76c9-11e9-b8e7-f898efc7166d; G_ENABLED_IDPS=google; SPC_CLIENTID=9awTBIZES0uYFNkfusezgxuaruhgvumz; SC_DFP=Eva3li3Ef1YLX6wg8YhiUf1nznTpZMDK; SPC_SI=mall.Se8WgeNKzPFRrNhjMfE9yHWtBonTXmwO; csrftoken=VJfuneWDQRzrU3QFgUvijbErFRHku6M9; welcomePkgShown=true; SPC_U=144737012; SPC_EC=IrO9Qek/PCPHL7nGlM/1379L2KjaGM4mAQQVwB8dJ+vf94HTT+A9lTnfZtR6GRpdg2bQBbXGdEPy3noZnRSl/3TgRDu3pQdbIMqOKqYv4aPV5AS2h5wxa2lnIPcY+doc5em+Makb9zxy9DUOViCICWhiQZmpC/7BKKNFl4iCvHY=; _gcl_au=1.1.402160856.1607854379; _fbp=fb.2.1607854379239.154716612; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.3.1156611057.1607854380; REC_MD_36=1607857040; _ga_SW6D8G0HXK=GS1.1.1607854379.1.1.1607856529.0; _ga=GA1.3.1413019161.1607854379; _dc_gtm_UA-61904553-8=1; SPC_R_T_ID="Dd6RBmufYffms0sEM4kp76EQGOzuzqupUWcwF4q/898ivx1MOm9SGnXjWprSI5P4jJdhSc770NZqgfM3CwgnKkJIt2km2rhIg3aT4q4FtyM="; SPC_T_ID="Dd6RBmufYffms0sEM4kp76EQGOzuzqupUWcwF4q/898ivx1MOm9SGnXjWprSI5P4jJdhSc770NZqgfM3CwgnKkJIt2km2rhIg3aT4q4FtyM="; SPC_R_T_IV="mLutxccyjIgxgzyfDe50cA=="; SPC_T_IV="mLutxccyjIgxgzyfDe50cA=="; REC_B_MD_7=1607856549_0.30.0.40'
    }
    data = '{"selected_shop_order_ids":[{"shopid":' + shopId + ',"item_briefs":[{"itemid":' + itemId + ',"modelid":' + modelId + ',"item_group_id":null,"applied_promotion_id":' + promotionId + ',"offerid":null,"price":' + price + ',"quantity":1,"is_add_on_sub_item":null,"add_on_deal_id":null,"status":1,"cart_item_change_time":' + str(timestamp) + '}],"shop_vouchers":[]}],"platform_vouchers":[]}'
    payload = json.loads(data)
    logger.info(data)

    #Get response
    response = requests.post(api, headers=headers, json=payload).json()
    logger.info(response)

    return response

#Run scheduler
def runScheduler(hour):
    #Set Scheduler
    schedule.every().day.at(hour).do(lambda: run(sys.argv[1]))

    animation = "|/-\\"

    for i in count(0):
        schedule.run_pending()
        time.sleep(1)
        sys.stdout.write("\r## Nungguin jam flash sale.. Sabar ya.. " + animation[i % len(animation)] + " ##")
        sys.stdout.flush()

#Run the program
def run(url):
    if getInfo(url):
        if addToCart():
            if checkout():
                printMsg("Anjay! checkout berhasil coy")

#Check if argument exist
if len(sys.argv) > 1:
    if len(sys.argv) > 2:
        runScheduler(sys.argv[2])
    else:
        run(sys.argv[1])
else:
    printMsg("Link produk sama waktunya mana bege??")
    sys.exit()

