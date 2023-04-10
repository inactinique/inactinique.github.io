import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import json


#ser = Service("chromedriver.exe")
ser = Service("chromedriver")

options = Options()
options.add_experimental_option("detach", True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(service=ser, options=options)

SEARCH_REQUEST=input("Enter the search request: ")
Counterr=int(input("Enter the results amount needed(minimum=50, put -1 if you want ALL results): "))   #Amonut of results needed

if(Counterr!=-1 and Counterr<50):
    Counterr=50
    print("The number you entered is less than 50, setting it to 50 automatically")

def loadNew(curs):
    errorr=False
    browser.get("https://lexica.art/api/trpc/prompts.infinitePrompts?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22text%22%3A%22"+SEARCH_REQUEST+"%22%2C%22searchMode%22%3A%22images%22%2C%22source%22%3A%22search%22%2C%22cursor%22%3A"+str(curs)+"%7D%7D%7D")
    p = browser.page_source
    try:
        heading = browser.find_element(By.TAG_NAME, "pre").text
    except:
        errorr=True
    if(errorr==False):
        with open('temp.json', 'wb') as f:
            heading=heading.encode('utf8')
            f.write(heading)
        f = open('temp.json', encoding="utf8")
        data = json.load(f)
        if "error" in data[0]:
            print("Website returned error, trying again in 100ms. Cursor: "+str(curs))
            time.sleep(0.1)
            loadNew(curs)
        else:
            j=0
            for i in data[0]['result']['data']['json']['prompts']:
                data=i['prompt']+"\n"
                with open(str(SEARCH_REQUEST+'.txt'), 'ab') as m:
                    data=data.encode('utf8')
                    m.write(data)
                if(curs+j>=Counterr-1):
                    print("Successfully added between "+str(curs)+" and "+str(Counterr))
                    print("FINISH, check "+str(SEARCH_REQUEST)+".txt in current directory")
                    with open('temp.json', 'wb') as f:
                        clearr=" "
                        clearr=clearr.encode('utf8')
                        f.write(clearr)
                    browser.quit()
                    exit()
                j=j+1
            print("Successfully added between "+str(curs)+" and "+str(curs+50))
            time.sleep(0.1)
    else:
        print("Unknown error, trying again in 100ms")
        time.sleep(0.1)
        loadNew(curs)

def getMaxResults():
    numm=0
    nums=['0','1','2','3','4','5','6','7','8','9']
    print("Counter equals -1, detecting the maximum possible amount...")
    browser.get("https://lexica.art/?q="+str(SEARCH_REQUEST))
    p = browser.page_source
    try:
        cellValue = browser.find_element(By.CSS_SELECTOR, "div.text-center:nth-child(7)").text
        for i in range(0,len(cellValue),1):
            if cellValue[i] in nums:
                numm=numm*10+int(cellValue[i])
        global Counterr
        Counterr = numm
        print("Maximum amount detected: "+str(Counterr))
    except:
        print("Error when looking for the maximum result amount; Trying again in 250ms")
        time.sleep(0.25)
        getMaxResults()
    
    

#MAIN
if(Counterr==-1):
    getMaxResults()
print("Starting with parameters: Request="+str(SEARCH_REQUEST)+"; ResultAmount="+str(Counterr))

with open(str(SEARCH_REQUEST+'.txt'), 'w') as g:
    g.write('#####FIRST LINE#####'+"\n")
browser.get("https://lexica.art/api/trpc/prompts.infinitePrompts?batch=1&input=%7B%220%22%3A%7B%22json%22%3A%7B%22text%22%3A%22"+SEARCH_REQUEST+"%22%2C%22searchMode%22%3A%22images%22%2C%22source%22%3A%22search%22%2C%22cursor%22%3Anull%7D%2C%22meta%22%3A%7B%22values%22%3A%7B%22cursor%22%3A%5B%22undefined%22%5D%7D%7D%7D%7D")
p = browser.page_source
heading = browser.find_element(By.TAG_NAME, "pre").text
with open('temp.json', 'wb') as f:
    heading=heading.encode('utf8')
    f.write(heading)
f = open('temp.json', encoding="utf8")
data = json.load(f)
if "error" in data[0]:
        print("Website returned error, restart the app please")
        exit()
        
cursor=data[0]['result']['data']['json']['nextCursor']
for i in data[0]['result']['data']['json']['prompts']:
    data=i['prompt']+"\n"
    with open(str(SEARCH_REQUEST+'.txt'), 'ab') as m:
        data=data.encode('utf8')
        m.write(data)

print("Successfully added first 50 lines of prompts")
while(cursor<Counterr):
    loadNew(cursor)
    cursor=cursor+50
with open('temp.json', 'wb') as f:
    clearr=" "
    clearr=clearr.encode('utf8')
    f.write(clearr)
browser.quit()
print("FINISH, check "+str(SEARCH_REQUEST)+".txt in current directory")