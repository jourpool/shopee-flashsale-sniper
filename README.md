# Shopee Flashsale Sniper
Order a Shopee Flashsale product in an instant.

## Arguments

### Required Arguments
```-url```
URL of the Flashsale Product

```-cookie```
User session Cookie

### Optional Arguments

```-time```
Scheduler in HH:MM format

## Examples

Basic usage: 

    shopee.py -url https://shopee.co.id/Japan-Hobby-Tools-Easy-Wrapper-Protective-Small-Blue-i.57237654.7210875698 -cookie 'SPC_IA=-1; SPC_F=9awTBIZES0uYFNkfmvsUzgJJbUrlfY2W; REC_T_ID=5591070a-76c9-11e9-b8e7-f898efc7166d; G_ENABLED_IDPS=google; SPC_CLIENTID=9awTBIZES0uYFNkfusezgxuaruhgvumz; SC_DFP=Eva3li3Ef1YLX6wg8YhiUf1nznTpZMDK; SPC_SI=mall.Se8WgeNKzPFRrNhjMfE9yHWtBonTXmwO; csrftoken=VJfuneWDQRzrU3QFgUvijbErFRHku6M9; welcomePkgShown=true; SPC_U=144737012; SPC_EC=IrO9Qek\/PCPHL7nGlM\/1379L2KjaGM4mAQQVwB8dJ+vf94HTT+A9lTnfZtR6GRpdg2bQBbXGdEPy3noZnRSl\/3TgRDu3pQdbIMqOKqYv4aPV5AS2h5wxa2lnIPcY+doc5em+Makb9zxy9DUOViCICWhiQZmpC\/7BKKNFl4iCvHY=; _gcl_au=1.1.402160856.1607854379; _fbp=fb.2.1607854379239.154716612; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.3.1156611057.1607854380; _dc_gtm_UA-61904553-8=1; REC_B_MD_7=1607854780_0.30.0.37; REC_MD_36=1607855363; _ga_SW6D8G0HXK=GS1.1.1607854379.1.1.1607854766.0; _ga=GA1.3.1413019161.1607854379; SPC_R_T_ID=\"Y0P4aw4QiEazQGfc0cKYIQq7IUN5pGToE2aHHpRoTUw361H\/aPWAvEU\/sse8u6LnF3NpDjk8eqds2TP6Sl7BgprjAB2trjyNqI4nwzWr6NQ=\"; SPC_T_IV=\"X674sZB3zttsyi2\/d9JyPQ==\"; SPC_R_T_IV=\"X674sZB3zttsyi2\/d9JyPQ==\"; SPC_T_ID=\"Y0P4aw4QiEazQGfc0cKYIQq7IUN5pGToE2aHHpRoTUw361H\/aPWAvEU\/sse8u6LnF3NpDjk8eqds2TP6Sl7BgprjAB2trjyNqI4nwzWr6NQ=\"'

With scheduler: 

    shopee.py -url https://shopee.co.id/Japan-Hobby-Tools-Easy-Wrapper-Protective-Small-Blue-i.57237654.7210875698 -cookie 'SPC_IA=-1; SPC_F=9awTBIZES0uYFNkfmvsUzgJJbUrlfY2W; REC_T_ID=5591070a-76c9-11e9-b8e7-f898efc7166d; G_ENABLED_IDPS=google; SPC_CLIENTID=9awTBIZES0uYFNkfusezgxuaruhgvumz; SC_DFP=Eva3li3Ef1YLX6wg8YhiUf1nznTpZMDK; SPC_SI=mall.Se8WgeNKzPFRrNhjMfE9yHWtBonTXmwO; csrftoken=VJfuneWDQRzrU3QFgUvijbErFRHku6M9; welcomePkgShown=true; SPC_U=144737012; SPC_EC=IrO9Qek\/PCPHL7nGlM\/1379L2KjaGM4mAQQVwB8dJ+vf94HTT+A9lTnfZtR6GRpdg2bQBbXGdEPy3noZnRSl\/3TgRDu3pQdbIMqOKqYv4aPV5AS2h5wxa2lnIPcY+doc5em+Makb9zxy9DUOViCICWhiQZmpC\/7BKKNFl4iCvHY=; _gcl_au=1.1.402160856.1607854379; _fbp=fb.2.1607854379239.154716612; AMP_TOKEN=%24NOT_FOUND; _gid=GA1.3.1156611057.1607854380; _dc_gtm_UA-61904553-8=1; REC_B_MD_7=1607854780_0.30.0.37; REC_MD_36=1607855363; _ga_SW6D8G0HXK=GS1.1.1607854379.1.1.1607854766.0; _ga=GA1.3.1413019161.1607854379; SPC_R_T_ID=\"Y0P4aw4QiEazQGfc0cKYIQq7IUN5pGToE2aHHpRoTUw361H\/aPWAvEU\/sse8u6LnF3NpDjk8eqds2TP6Sl7BgprjAB2trjyNqI4nwzWr6NQ=\"; SPC_T_IV=\"X674sZB3zttsyi2\/d9JyPQ==\"; SPC_R_T_IV=\"X674sZB3zttsyi2\/d9JyPQ==\"; SPC_T_ID=\"Y0P4aw4QiEazQGfc0cKYIQq7IUN5pGToE2aHHpRoTUw361H\/aPWAvEU\/sse8u6LnF3NpDjk8eqds2TP6Sl7BgprjAB2trjyNqI4nwzWr6NQ=\"' -time 23:30
