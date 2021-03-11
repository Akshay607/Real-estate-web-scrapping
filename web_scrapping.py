import requests
from bs4 import BeautifulSoup
import pandas

r=requests.get("http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s=0.html",
headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})
c=r.content
soup=BeautifulSoup(c,"html.parser")

pg=soup.find_all("a",{"class":"Page"})[-1].text

baseurl="http://www.pyclass.com/real-estate/rock-springs-wy/LCWYROCKSPRINGS/t=0&s="
l=[]
for page in range(0,int(pg)*10,10):
    r = requests.get(baseurl+str(page)+".html",
    headers={'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'})

    c=r.content

    soup=BeautifulSoup(c,"html.parser")
    all =soup.find_all("div",{"class":"propertyRow"})
    all1=all[0].find("h4",{"class":"propPrice"}).text.replace(" ","").replace("\n","")
    
    for item in all:
        d={}
        d["Price"]=item.find("h4",{"class","propPrice"}).text.replace("\n","").replace(" ","")
        d["Address"]=item.find_all("span",{"class","propAddressCollapse"})[0].text
        d["Locality"]=item.find_all("span",{"class","propAddressCollapse"})[1].text
        try:
            d["Beds"]=item.find("span",{"class":"infoBed"}).find("b").text
        except:
            d["Beds"]=None
        try:
            d["Area"]=item.find("span",{"class","infoSqFt"}).find("b").text
        except:
            d["Area"]=None

        try:
            d["Full_bath"]=item.find("span",{"class":"infoValueFullBath"}).find("b").text
        except:
            d["Full_bath"]=None

        try:
            d["Half_bath"]=item.find("span",{"class":"infoValueHalfBath"}).find("b").text
        except:
            d["Half_bath"]=None

        for col_grp in item.find_all("div",{"class":"columnGroup"}):
            for feature_grp, feature_name in zip(col_grp.find_all("span",{"class","featureGroup"}),col_grp.find_all("span",{"class","featureName"})):
                if "Lot Size" in feature_grp.text:
                    d["Lot_size"]=feature_name.text
        l.append(d)
    df=pandas.DataFrame(l)
df.to_csv("Output.csv")
