import requests

def Price_Change_Gctest(skus=''):
    for i in skus.split(","):
        url = 'http://gctestprexg.admin.cnsuning.com/job/ppl/changePrice.htm?reqMsg={ "cmmdtyCode":"%s", "cityCode":"025"}'%i
        req = requests.get(url=url)
        print(req.text)

if __name__ == '__main__':
    sku='659882440,10629204011,10579253522,695595091,10579250789,10169254673,10019776076,120211971,622537390,945024821,945041770,775648208,620771420,10783358707,520500006,520500384,191811516,10108678292,131118421,131118414,10015301749,188540373,621358039,621358043,10578470715'
    Price_Change_Gctest(skus=sku)