import requests
import pandas as pd
from requests.structures import CaseInsensitiveDict
csvFile="9200_9300.csv"
url_download = "https://cae-largefile-prod.cisco.com/Web-Ui"
srId = "690867692"
fileName = "mgdc-11-c01-as01--tech-sup.txt"
params={'srId':'690867692', 'fileName':'mgdc-11-c01-as01--tech-sup.txt'}
cookie1="guestCntry=US; guestLang=en_US; CCW_SERVER_HOST_NAME=ccw-pblu-ext-alln-6d76b656f9-pwjh5; _abck=12DDA6C7696C53E1C8EF8E68F3BE1671~0~YAAQdK1NaBm3bhV6AQAA6JrsHQa6YN3So7QMa9T5dN7GTIwvSgIFafS2CfMOZXT0rVohvcddUDSjN4cbYlNIviLo12c4vdbJIhMrxvYLZLo3T2AiNEGWyWjq0OEVAiUZ9Kk6+MrJ6NRXrlOzbH+hiFtRPXoeJZdmjLQPFvV2/Zzxu4n5lnlknb4ZcrAeImYrY9lEKT8nx2NVWSR8MJd5FfbMQZuVIQuqedn/NmkTcLeUL1dE/ZlGN6nCfKXh0FiLkxCfl2Vhh59xHBigC/w8seUqZN2AlOx2vX7bLF6cnC30EXKZeRrzZS7nLuwMrZtp5ni6qsw774uxG7jviZ1lWQmx0j4kN5f6HWtHUsN9AeMPAkBgDJ+miGXZAagrLj/kUdGQ183mNmZOi7cyJJLyPJEQ2OFwFXc=~-1~-1~-1; GUTCID=testseg2%3D18618614; _ga=GA1.2.853405633.1621489846; _fbp=fb.1.1626929835682.160880593; aam_uuid=02597018745041892621905212819764514450; WRUID=3409635330900644; ELOQUA=GUID=808912E38C8B49D7A8529937DA10EDCC; OptanonAlertBoxClosed=2021-08-05T17:20:57.097Z; iv=0d4f3f2f-f60e-46c5-a4c4-a290c54542e9; _mkto_trk=id:564-WHV-323&token:_mch-cisco.com-1629971704443-48215; _biz_uid=3355a79b9d8a489facdfe3659ce39e62; _cs_c=0; CP_GUTC=72.163.4.165.1632462482925086; _cs_id=22c82df8-34bd-a876-e13a-13218deaf9ec.1610338898.77.1632808240.1632808240.1589297132.1644502898666; __CT_Data=gpv=21&ckp=tld&dm=cisco.com&apv_14_www47=21&cpv_14_www47=21&rpv_14_www47=21; anchorvalue=; AMCVS_B8D07FF4520E94C10A490D4C%40AdobeOrg=1; cdcUniqueKey=84g8f1i03c5g7; _gcl_au=1.1.794244459.1636899968; check=true; AMCVS_97EC4C5658ACABA20A495D1E%40AdobeOrg=1; AMCV_97EC4C5658ACABA20A495D1E%40AdobeOrg=-330454231%7CMCIDTS%7C18954%7CMCMID%7C02255049754187805901930687550505984114%7CMCAAMLH-1638164753%7C12%7CMCAAMB-1638164753%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1637567153s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C3.1.2; OptanonConsent=isIABGlobal=false&datestamp=Tue+Nov+23+2021+10%3A55%3A29+GMT%2B0530+(India+Standard+Time)&version=6.21.0&hosts=&consentId=fcac3113-e81e-446d-9d35-87ca02a9e079&interactionCount=2&landingPath=NotLandingPage&groups=1%3A1%2C2%3A1%2C3%3A1%2C4%3A1&AwaitingReconsent=false&geolocation=IN%3BKA&isGpcEnabled=0; _biz_nA=35; _biz_flagsA=%7B%22Version%22%3A1%2C%22Ecid%22%3A%22-1624845529%7C1042081706%22%2C%22ViewThrough%22%3A%221%22%2C%22XDomain%22%3A%221%22%7D; _biz_pendingA=%5B%5D; _uetvid=8d03c550676c11eb9cd91beca7d07a67; ADRUM=s=1637646899353&r=https%3A%2F%2Fcdetsng.cisco.com%2Fsummary%2F%3Fhash%3D366227692; bdb_cookie=9e595846-ad32-4322-8333-1767f4ea3e87; loginPageReferrer=https%3A//csone.my.salesforce.com/; loginPageRef=https%3A//csone.my.salesforce.com/; wasOnLoginPage=false; cdcSsoTimer=LoggedIn; authorization=LoggedIn; AMCV_B8D07FF4520E94C10A490D4C%40AdobeOrg=281789898%7CMCIDTS%7C18957%7CMCMID%7C07282432605775044631436987955566450451%7CMCAAMLH-1638423307%7C12%7CMCAAMB-1638423307%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1637825707s%7CNONE%7CMCAID%7CNONE%7CvVersion%7C4.1.0%7CMCCIDH%7C-1432046144; s_cc=true; s_ppvl=onesearch.cisco.com%2Fsearchpage%2Fv1%2C25%2C25%2C722%2C1536%2C722%2C1536%2C864%2C1.25%2CP; s_ppv=onesearch.cisco.com%2Fsearchpage%2Fv1%2C25%2C25%2C722%2C1536%2C722%2C1536%2C864%2C1.25%2CP; utag_main=v_id:0179832c4312001d36e848586e9c03073004d06b00978$_sn:212$_ss:0$_st:1637820311183$vapi_domain:cisco.com$_se:16$ses_id:1637818035361%3Bexp-session$_pn:2%3Bexp-session$ctm_ss:true%3Bexp-session; s_sq=%5B%5BB%5D%5D; s_ptc=3826%5E%5E0%5E%5E0%5E%5E0%5E%5E2461%5E%5E38%5E%5E4417%5E%5E7%5E%5E10729; wamsessiontracker=T1RLAQJ7PACxcomEVrJfYnL-pw3cn56duxAwb4KEgG92yM1MYzHL9PQ7AACAvq1_VB2aY49Jlf5HxvTDlmB4IRAte1jwoYQQ9Nf53D_5mM01KWse9ZvX4Uzd4jykiB8hcBhlft3klZhMmnJuIpWf0WN1tgY16k09j0T3PNiV8INRQZ5jp8PzL24j0Sn1jqI1KwgfJpGQthv0pExZT7ZX2luCN5ZP3HwpV0ct-IY*; discovery=T1RLAQIoR2DOajK8vobwqT3sqX0xgAQUsxDkk9RTsEB4iEuR9V1OwYRiAACQkr_wcvK4XpjPQjotjlPFqR3LSsTRYw3b7ixMHFtwvLYL-IMdv5hYfrpsgs8L8AO3nh-HcqsVEKHuVUhPS3l9gLY-WeGgYOQUCdHnfhVH38PwuZ8cowVihiVnt4N_8H4A5XSTmoD0IuuGOWQ0Ljn1ZRMxnPqjA8aHnNA0ETdIKMJY4oZWNhQ5JkIW1qMNVgKd"
headers = CaseInsensitiveDict()
headers["X-Custom-Header"] = "value"
headers["Content-Type"] = "application/json"
headers["Cookie"] = cookie1
#resp = requests.get(url, params=params,  headers=headers)
#print(resp.status_code)

def download_file(url,fileName,params,headers):
    local_filename = url.split('/')[-1]
    # NOTE the stream=True parameter below
    with requests.get(url, params=params,  headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(fileName, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                #if chunk:
                f.write(chunk)
    print(fileName)
    return local_filename

def getCookie():
    loginUrl = "https://scripts.cisco.com/api/v2/auth/login"
    API_KEY = "YmphdHRpOjEwSmFuMTk4MDgxIQ=="
    r = requests.get(loginUrl, headers={'Authorization': 'Basic %s' %  API_KEY})
    #print(r.status_code)
    #print(r.headers["Set-Cookie"])
    return(r.headers["Set-Cookie"])

def downloadAttachment(sr,cookie,downloadFile):
    return()

def getAttachmentList(sr,cookie,headers,url_download):
    url = "https://scripts.cisco.com/api/v2/attachments/"+str(sr)
    r = requests.get(url, headers={'Cookie': '%s' % cookie})
    shTechCount = 0
    #print(r.status_code)
    if r.status_code == 200:
        json=r.json()
        lJson = len(json)
        #print(type(json))
        for i in range(lJson):
            for key in json[i]:
                if key == "fileName":
                    #print(key)
                    if "tech" in json[i][key] or "run" in json[i][key]:
	                print(json[i][key])
                        downloadFile=json[i][key]
                        shTechCount = shTechCount + 1
                        print(shTechCount)
                        print("xxxxxx")
                        strSR=str(sr)
                        params={'srId':strSR, 'fileName':downloadFile}
                        download_file(url_download,downloadFile,params,headers)
        #print(json)
        #print(type(r.text))

# get SR's from csv file
df = pd.read_csv(csvFile, usecols = ['SR Number'])

cookie = getCookie()
for ind in df.index:
     print(df['SR Number'][ind])
     sr = df['SR Number'][ind]
     getAttachmentList(sr,cookie,headers,url_download)


# from 1 sr get all attachments
# get company name from SR
# get company type. i.e finance, NGE, etc.
# find out the attachment name of show tech

# download attachment file
#download_file(url,fileName,params,headers)
