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

info = {
    'merchandise_subtotal':'0',
    'shipping_subtotal':'0',
    'shipping_subtotal_before_discount':'0',
    'total_payable':'0',
    'coin_offset':'0',
    'coin_used':'0',
    'channel_id':'0',
    'BASIC_SHIPPING_FEE':'0',
    'ITEM_TOTAL':'0',
    'SHIPPING_DISCOUNT_BY_SHOPEE':'0',
    'SHOPEE_OR_SELLER_SHIPPING_DISCOUNT':'0',
    'order_total':'0',
    'order_total_without_shipping':'0',
    'shipping_fee':'0',
    'shopee_shipping_discount_id':'0',
    'voucher_wallet_checking_channel_ids':'0',
    'addressid':'0',
    'catids':'0',
    'image':'0',
    'name':'0',
    'price':'0',
    'order_total':'0',
    'order_total_without_shipping':'0',
    'is_official_shop':'0',
    'shop_name':'0',
    'timestamp':'0'
}


def getCheckout():
    printMsg("Ambil info checkoutnya dulu ya say..")

    #Set API item checkout
    api = 'https://shopee.co.id/api/v2/checkout/get'
    headers = { 
        'origin': 'https://shopee.co.id',
        'content-type': 'application/json',
        'referer': 'https://shopee.co.id/cart/',
        'x-csrftoken': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'cookie': cookie
    }
    data = '{"shoporders":[{"shop":{"shopid":' + product['shopId'] + '},"items":[{"itemid":' + product['itemId'] + ',"modelid":' + product['modelId'] + ',"add_on_deal_id":null,"is_add_on_sub_item":null,"item_group_id":null,"quantity":1}],"logistics":{"recommended_channelids":null},"buyer_address_data":{},"selected_preferred_delivery_time_slot_id":null}],"selected_payment_channel_data":{},"promotion_data":{"use_coins":false,"free_shipping_voucher_info":{"free_shipping_voucher_id":0,"disabled_reason":"","description":""},"platform_vouchers":[],"shop_vouchers":[],"check_shop_voucher_entrances":true,"auto_apply_shop_voucher":false},"device_info":{"device_id":"","device_fingerprint":"","tongdun_blackbox":"","buyer_payment_info":{}},"tax_info":{"tax_id":""}}'
    payload = json.loads(data)
    logger.info(data)

    #Get response
    response = requests.post(api, headers=headers, json=payload).json()
    logger.info(response)

    info['merchandise_subtotal'] = str(response['checkout_price_data']['merchandise_subtotal'])
    info['shipping_subtotal'] = str(response['checkout_price_data']['shipping_subtotal'])
    info['shipping_subtotal_before_discount'] = str(response['checkout_price_data']['shipping_subtotal_before_discount'])
    info['total_payable'] = str(response['checkout_price_data']['total_payable'])

    info['coin_offset'] = str(response['promotion_data']['coin_info']['coin_offset'])
    info['coin_used'] = str(response['promotion_data']['coin_info']['coin_used'])

    info['channel_id'] = str(response['selected_payment_channel_data']['channel_id'])

    info['BASIC_SHIPPING_FEE'] = str(response['shoporders'][0]['amount_detail']['BASIC_SHIPPING_FEE'])
    info['ITEM_TOTAL'] = str(response['shoporders'][0]['amount_detail']['ITEM_TOTAL'])
    info['SHIPPING_DISCOUNT_BY_SHOPEE'] = str(response['shoporders'][0]['amount_detail']['SHIPPING_DISCOUNT_BY_SHOPEE'])
    info['SHOPEE_OR_SELLER_SHIPPING_DISCOUNT'] = str(response['shoporders'][0]['amount_detail']['SHOPEE_OR_SELLER_SHIPPING_DISCOUNT'])

    info['order_total'] = str(response['shoporders'][0]['order_total'])
    info['order_total_without_shipping'] = str(response['shoporders'][0]['order_total_without_shipping'])
    info['shipping_fee'] = str(response['shoporders'][0]['shipping_fee'])

    info['shopee_shipping_discount_id'] = str(response['shipping_orders'][0]['shopee_shipping_discount_id'])

    info['voucher_wallet_checking_channel_ids'] = str(response['shoporders'][0]['logistics']['voucher_wallet_checking_channel_ids'])

    info['addressid'] = str(response['shoporders'][0]['buyer_address_data']['addressid'])

    info['catids'] = str(response['shoporders'][0]['items'][0]['categories'][0]['catids'])
    info['image'] = str(response['shoporders'][0]['items'][0]['image'])
    info['name'] = response['shoporders'][0]['items'][0]['name']
    info['price'] = str(response['shoporders'][0]['items'][0]['price'])

    info['order_total'] = str(response['shoporders'][0]['order_total'])
    info['order_total_without_shipping'] = str(response['shoporders'][0]['order_total_without_shipping'])

    info['is_official_shop'] = str(response['shoporders'][0]['shop']['is_official_shop'])
    info['shop_name'] = response['shoporders'][0]['shop']['shop_name']

    info['timestamp'] = str(response['timestamp'])

    return True

def pay():
    printMsg("Saatnya kita bayar..")

    #Set API payment
    api = 'https://shopee.co.id/api/v2/checkout/place_order'
    headers = {
        'origin': 'https://shopee.co.id',
        'content-type': 'application/json',
        'referer': 'https://shopee.co.id/checkout/',
        'x-csrftoken': token,
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
        'cookie': cookie
    }

    data = '{"status":200,"headers":{},"cart_type":0,"shipping_orders":[{"cod_fee":0,"tax_payable":0,"order_total":' + info['order_total'] + ',"shipping_id":1,"buyer_ic_number":"","fulfillment_info":{"fulfillment_flag":64,"fulfillment_source":"","managed_by_sbs":false,"order_fulfillment_type":2,"warehouse_address_id":0},"shopee_shipping_discount_id":' + info['shopee_shipping_discount_id'] + ',"selected_logistic_channelid_with_warning":null,"selected_logistic_channelid":' + info['shopee_shipping_discount_id'] + ',"voucher_wallet_checking_channel_ids":' + info['voucher_wallet_checking_channel_ids'] + ',"shipping_group_icon":"","buyer_remark":null,"buyer_address_data":{"tax_address":"","error_status":"","address_type":0,"addressid":' + info['addressid'] + '},"shipping_fee_discount":0,"shipping_group_description":"","shoporder_indexes":[0],"order_total_without_shipping":' + info['order_total_without_shipping'] + ',"shipping_fee":' + info['shipping_fee'] + ',"selected_preferred_delivery_time_option_id":0,"amount_detail":{"BASIC_SHIPPING_FEE":' + info['BASIC_SHIPPING_FEE'] + ',"SELLER_ESTIMATED_INSURANCE_FEE":0,"SHOPEE_OR_SELLER_SHIPPING_DISCOUNT":' + info['SHOPEE_OR_SELLER_SHIPPING_DISCOUNT'] + ',"VOUCHER_DISCOUNT":0,"SHIPPING_DISCOUNT_BY_SELLER":0,"SELLER_ESTIMATED_BASIC_SHIPPING_FEE":0,"SHIPPING_DISCOUNT_BY_SHOPEE":' + info['SHIPPING_DISCOUNT_BY_SHOPEE'] + ',"INSURANCE_FEE":0,"ITEM_TOTAL":' + info['ITEM_TOTAL'] + ',"shop_promo_only":true,"COD_FEE":0,"TAX_FEE":0,"SELLER_ONLY_SHIPPING_DISCOUNT":0}}],"disabled_checkout_info":{"auto_popup":false,"description":"","error_infos":[]},"timestamp":' + info['timestamp'] + ',"checkout_price_data":{"shipping_subtotal":' + info['shipping_subtotal'] + ',"shipping_discount_subtotal":0,"shipping_subtotal_before_discount":1000000000,"bundle_deals_discount":null,"group_buy_discount":0,"merchandise_subtotal":' + info['merchandise_subtotal'] + ',"tax_payable":0,"buyer_txn_fee":0,"credit_card_promotion":null,"promocode_applied":null,"shopee_coins_redeemed":null,"total_payable":' + info['total_payable'] + '},"client_id":0,"promotion_data":{"promotion_msg":"","price_discount":0,"can_use_coins":true,"voucher_info":{"coin_earned":0,"promotionid":0,"discount_percentage":0,"discount_value":0,"voucher_code":null,"reward_type":0,"coin_percentage":0,"used_price":0},"coin_info":{"coin_offset":' + info['coin_offset'] + ',"coin_earn":0,"coin_earn_by_voucher":0,"coin_used":' + info['coin_used'] + '},"free_shipping_voucher_info":{"free_shipping_voucher_id":0,"disabled_reason":null,"free_shipping_voucher_code":""},"applied_voucher_code":null,"shop_voucher_entrances":[{"status":false,"shopid":' + product['shopId'] + '}],"card_promotion_enabled":false,"invalid_message":null,"card_promotion_id":null,"voucher_code":null,"use_coins":false},"dropshipping_info":{"phone_number":"","enabled":false,"name":""},"selected_payment_channel_data":{"channel_id":' + info['channel_id'] + ',"channel_item_option_info":{"option_info":""},"version":2},"shoporders":[{"shop":{"remark_type":0,"support_ereceipt":false,"images":"","is_official_shop":false,"cb_option":false,"shopid":' + product['shopId'] + ',"shop_name":"' + info['shop_name'] + '"},"buyer_remark":null,"shipping_fee":' + info['shipping_fee'] + ',"order_total":' + info['order_total'] + ',"shipping_id":1,"buyer_ic_number":"","items":[{"itemid":' + product['itemId'] + ',"is_add_on_sub_item":false,"image":"a8444ef6b589470728baa94d2a2b6385","shopid":' + product['shopId'] + ',"opc_extra_data":{"slash_price_activity_id":0},"promotion_id":' + product['promotionId'] + ',"add_on_deal_id":0,"modelid":' + product['modelId'] + ',"offerid":0,"source":"","checkout":true,"item_group_id":0,"service_by_shopee_flag":false,"none_shippable_full_reason":"","price":' + info['price'] + ',"is_flash_sale":true,"categories":[{"catids":[134,17977,17984]}],"shippable":true,"name":"Netline Kabel Printer USB - 1,5 Meter","none_shippable_reason":"","is_pre_order":false,"stock":0,"model_name":"","quantity":1}],"selected_logistic_channelid":80014,"cod_fee":0,"tax_payable":0,"buyer_address_data":{"tax_address":"","error_status":"","address_type":0,"addressid":' + info['addressid'] + '},"shipping_fee_discount":0,"order_total_without_shipping":999900000,"selected_preferred_delivery_time_option_id":0,"amount_detail":{"BASIC_SHIPPING_FEE":1000000000,"COD_FEE":0,"SHOPEE_OR_SELLER_SHIPPING_DISCOUNT":-1000000000,"VOUCHER_DISCOUNT":0,"SHIPPING_DISCOUNT_BY_SELLER":0,"SELLER_ESTIMATED_INSURANCE_FEE":0,"SELLER_ESTIMATED_BASIC_SHIPPING_FEE":0,"SHIPPING_DISCOUNT_BY_SHOPEE":1000000000,"INSURANCE_FEE":0,"ITEM_TOTAL":999900000,"shop_promo_only":true,"TAX_FEE":0,"SELLER_ONLY_SHIPPING_DISCOUNT":0},"ext_ad_info_mappings":[]}],"can_checkout":true,"order_update_info":{},"buyer_txn_fee_info":{"error":"invalid_rule_id"}}'

    payload = json.loads(data)
    #logger.info(data)

    #Get response
    response = requests.post(api, headers=headers, json=payload).json()
    logger.info(response)

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
                if getCheckout():
                    pay()

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