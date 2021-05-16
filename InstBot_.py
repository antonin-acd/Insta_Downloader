import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
import os
import peusdo




def get_driver():
    options_ = webdriver.ChromeOptions()
    options_.add_argument('headless')
    options_.add_argument("--log-level=3")
    options_.add_argument("--window-size=1920, 1080")
    options_.add_argument("--start-maximized")
    options_.add_argument('--no-sandbox')
    options_.add_argument("--disable-gpu")
    options_.add_experimental_option("excludeSwitches", ["enable-automation"])
    options_.add_experimental_option('useAutomationExtension', False)
    
    driver = webdriver.Chrome(options=options_)
    driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
    return driver


def isprivate(driver):
    try:
        driver.find_element_by_xpath('//h2[@class="rkEop"]')
        return True
    except:
        return False


def wait_my_dear(driver,path):
    for i in range(250):
        try:
            driver.find_element_by_xpath(path)
            return True
        except:
            time.sleep(0.5)
            continue

def element_here(driver,path):
    try:
        driver.find_element_by_xpath(path)
        return True
    except:
        return False

def connedted_page(driver , login , password):
    time.sleep(1)
    driver.find_element_by_name("username").send_keys(login)
    time.sleep(0.5)
    driver.find_element_by_xpath('//input[@aria-label="Mot de passe"]').send_keys(password)
    time.sleep(0.5)
    driver.find_elements_by_tag_name("button")[1].click()
    
    time.sleep(10)
    
    driver.find_elements_by_tag_name("button")[1].click()
    
    time.sleep(10)
    try:
        driver.find_elements_by_tag_name("button")[-1].click()
    except:
        pass
    return driver


def go_to_connect(driver, login , password):
    page = BeautifulSoup(driver.page_source , features="lxml")
    link = page.find("a",{"class":"huQXy"})
    link = "https://www.instagram.com" + link
    driver.get(link)
    driver = connedted_page(driver , login , password)
    
    return driver


def dl_from_link(link,Tfilepath_):
    requete = requests.get(link, stream=True)
    with open(Tfilepath_ , "wb") as f:
        f.write(requete.content)
        f.close()



def multiple_picture(driver,filepath,name,ind=0):
    visited_list = []
    while True:
        page = BeautifulSoup(driver.page_source,features="lxml")
        img_link = page.find("ul",{"class":"vi798"})

        links = img_link.find_all("li",{"class":"Ckrof"})
        try:
            links = [x.find("img")["src"] for x in links]

            for i in links:
                if i not in visited_list:
                    visited_list.append(i)
            
            if element_here(driver,'//button[@class="  _6CZji   "]'):
                driver.find_element_by_xpath('//button[@class="  _6CZji   "]').click()
            else:
                break
        except:
            break

    if visited_list != []:
        for i in range(len(visited_list)):
            filepath_ = filepath + name + "_" + str(ind) + "_" + str(i) + ".jpg"
            dl_from_link(visited_list[i],filepath_)



#FOR IMAGE DOWNLOAD
def download_img(user_link , img_number , user_name="" , user_pawword="" , path=None):
    name = user_link.split("/")[-2]

    if path != None:
        filepath = path + name + "/"   #"C:/Users/Antonin Achard/Desktop/InstaDownloader/"+name+"/"
        if os.path.exists(filepath) != True:
            os.mkdir(filepath)
    else:
        return ""
    #options_ = webdriver.ChromeOptions()
    #options_.add_argument("headless")

    #driver = webdriver.Chrome(options=options_)
    driver = get_driver()
    driver.get(user_link)
    try:
        driver.find_element_by_xpath('//button[@class="aOOlW  bIiDR  "]').click()
    except:
        pass
    time.sleep(2)
    
    if driver.current_url == "https://www.instagram.com/accounts/login/":
        driver = connedted_page(driver , user_name , user_pawword)
        driver.get(user_link)
    print("I'm On the requested page")
    page = BeautifulSoup(driver.page_source , features="lxml")
    link = page.find_all("div",{"class":"Nnq7C weEfm"})
    link2 = []
    for i in link:
        link2.extend(i.find_all("a"))

    print("Start Donwload processus")
    
    if isinstance(img_number,tuple):
        for i in range(img_number[0] , img_number[1]): #for i in range(1,15)
            print("Current Download: photo {}".format(i),end="\r")

            link = link2[i] #lien balise publication 
            link = link["href"] #id publication
            link = "https://www.instagram.com/" + link #lien complet publication
            driver.get(link)
            
            page = BeautifulSoup(driver.page_source,features="lxml") 
            
            

            if element_here(driver,'//span[@aria-label="Lire"]') == True: #Si c'est une vidéo il passe
                linky1 = page.find("video",{"class":"tWeCl"})["poster"]
                filepath_ = filepath + name + "_" + str(i) + "_(Picture_Base_On_Video)" + ".jpg"
                dl_from_link(linky1,filepath_)
                continue
            
            tester = page.find("ul",{"class":"vi798"}) 
            if tester != None: #Si plusieurs photo existe (qu'on peut voir plusieurs photo en une)
                multiple_picture(driver,filepath,name,ind=i) #il appelle multiple_picture qui se charge de les télécharger
            
            else: #sinon il télécharge la photo unique
                filepath_ = filepath + name + "_" + str(i) + ".jpg" 
                linky = page.find("img",{"class":"FFVAD"})["src"]


                while os.path.exists(filepath_) == False:
                    try:
                        dl_from_link(linky,filepath_)
                    except:
                        continue

    else:
        link = link2[img_number]
        link = link["href"]
        link = "https://www.instagram.com/" + link
        driver.get(link)
        time.sleep(2)
        page = BeautifulSoup(driver.page_source , features="lxml")
        

        if element_here(driver,'//span[@aria-label="Lire"]') == True: #Si c'est une vidéo il passe
            linky1 = page.find("video",{"class":"tWeCl"})["poster"]
            filepath_ = filepath + name + "_" + str(i) + "_(Picture_Base_On_Video)" + ".jpg"
            dl_from_link(linky1,filepath_)
            
            
        else:
            imgs_link = page.find("ul",{"class":"vi798"})
            if imgs_link != None:
                multiple_picture(driver,filepath,name)


            else:
                img_link = page.find("img",{"class":"FFVAD"})["src"]
                filepath_ = filepath + name + "_" + str(0) + ".jpg"
                dl_from_link(img_link,filepath_)

    print("The download processus is over")
    driver.close()






download_img("page_link",(0,6),"user_name","user_password",path="path/to/folder")

