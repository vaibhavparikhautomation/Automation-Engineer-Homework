from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

#All Xpaths used in Script
inputadSeachXpath = "//input[@id='adsearch-input']"
dropdownListsearchAutoXpath = "//*[@id='adsearch-dropdown' and @class ='adsearch__dropdown search-bar-dropdown visible']/div//following-sibling::div[@class='search-bar-dropdown-row']"
elementparentLoadMoreXpath = "//*[@id='er-app']/div/div[5]/a//parent::div"
buttonloadMoreXpath = "//*[@id='er-app']/div/div[5]/a"
imageContainerXpath = "//*[@id='er-app']/div/div[4]/div[1]/div[2]"
creativeCountText = "//*[@id='er-app']/div/div[2]/div/div[2]/span"
linkRandomBrandXpath = "//*[@id='main-nav']/div[1]/div[1]/a[2]"
hoverImageXpath = "//*[@id='er-app']/div/div[4]/div[1]/div[2]/div[1]/div/img"
InputPopUpShare = "//*[@class ='popup']/div[2]/div[1]/input"
btnCopyLinkXpath = "//*[@class ='popup']/div[2]/div[2]/button"
closePopupWindowXpath  = "//*[@class ='popup']/div[1]/span/img"

#Input Strings used in scrpt
RandomBrandText="Random Brand"
ShareLinkText = "Share"

#Functions Defination
def wait_for_element_to_load(elementxpath,timeout):
    try:
        element_present = EC.presence_of_element_located((By.XPATH, elementxpath))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
           print("Timed out waiting for element to load")

def search_auto_dropdown_text(inputadSeachXpath,dropdownListsearchAutoXpath,Searchstring):
    #Verify if search bar exist or not.
     if check_exists_by_xpath(inputadSeachXpath)!="False": 
        #Enter Search Term in "Moat Ad Search" input box
        driver.find_element_by_xpath(inputadSeachXpath).send_keys(searchautodropdownText)
        # Wait for search bar autocomplete drop down texts to appear.
        wait_for_element_to_load(dropdownListsearchAutoXpath,5)
        elementList = driver.find_elements_by_xpath(dropdownListsearchAutoXpath)
        print("For specified string total number of Texts Displayed under search bar autocomplete drop down is: " + str(len(elementList)))
        print("When user enter '"+searchautodropdownText+"' texts result displayed for autocomplete drop down are:")
        #Iterate through list to display all the text for input search
        for x in range(1,len(elementList)+1):
          get_text_displayed = driver.find_element_by_xpath("//*[@id='adsearch-dropdown']/div/div["+str(x)+"]/a/div/span/div/span").text
          print(get_text_displayed)
          #Clear the text searched to continue with next test case.
          driver.find_element_by_xpath(inputadSeachXpath).clear()
        print("Testcase 1 Passed")  
     else:
        print("Testcase 1 Failed")

def verify_creatives_count(inputadSeachXpath,dropdownListsearchAutoXpath,elementparentLoadMoreXpath,buttonloadMoreXpath,imageContainerXpath,creativeCountText,searchText):
        #Enter Search Term in "Moat Ad Search" input box
        driver.find_element_by_xpath(inputadSeachXpath).send_keys(searchText)
        time.sleep(3)
        elementList = driver.find_elements_by_xpath(dropdownListsearchAutoXpath)
        #Calculate the lenght of the drop down list to iterate 
        print "Length of the auto drop down search result is: "+ str(len(elementList))
        #Search for the term in auto drop down list
        for x in range(1,len(elementList)+1):
            get_text_displayed = driver.find_element_by_xpath("//*[@id='adsearch-dropdown']/div/div["+str(x)+"]/a/div/span/div/span").text
            print(get_text_displayed)
            if get_text_displayed==searchText:
               #Click on searched element when found
               driver.find_element_by_xpath("//*[@id='adsearch-dropdown']/div/div["+str(x)+"]/a/div/span/div/span").click()
               break
            else:
               print("No such elements exists")
        time.sleep(3)    
        #Click on "Load More" button until all images are loaded before creatives counting
        while True:
            parentLoadMore = driver.find_element_by_xpath(elementparentLoadMoreXpath)
            if 'not-visible' in parentLoadMore.get_attribute('class'):
                break;
            driver.find_element_by_xpath(buttonloadMoreXpath).click()
            time.sleep(8)
                        
        #verify number of images
        #select the specific value from autocomplete dropdown text
        ParentCreatives = driver.find_element_by_xpath(imageContainerXpath)
        Creatives = ParentCreatives.find_elements_by_tag_name('img')
        print 'len(Creatives): ' + str(len(Creatives))
        actualCreativeCount = str(len(Creatives))
        elm = driver.find_element_by_xpath(creativeCountText)
        print elm.text
        expectedCreativeCount = elm.text.split(" ", 1)[0]
        print expectedCreativeCount
        if actualCreativeCount==expectedCreativeCount:
           print("Expected Creative Counts for '"+searchText+"' is "+expectedCreativeCount+" & it matches with actual creative count that is : "+actualCreativeCount)
           print("Testcase 2 Passed for search term '"+searchText+"'")
        else:
           print("Expected Creative Counts for '"+searchText+"' is "+expectedCreativeCount+" & it does not matches with actual creative count that is : "+actualCreativeCount)
           print("Testcase 2 Passed for search term '"+searchText+"'")
           
def check_random_brand(RandomBrandText,linkRandomBrandXpath):
    #Click on 'Random Brand' Link
    driver.find_element_by_link_text(RandomBrandText).click()
    wait_for_element_to_load(linkRandomBrandXpath,3)
    #Capture the Title of the current Page
    time.sleep(2)
    get_title= driver.title
    return get_title

def check_exists_by_xpath(xpath):
    try:
        #Verify whether element with input xpath exist or not
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

#create webdriver object  
driver = webdriver.Chrome()  

#maximize the window size  
driver.maximize_window()  

#navigate to the url  
driver.get('https://moat.com/')

#wait for the page to load successfully
wait_for_element_to_load(inputadSeachXpath,15)

#Enter string to be searched 
Searchstring = ["Satu"]

#Verify the search bar autocomplete drop down texts
for searchautodropdownText in Searchstring:
    search_auto_dropdown_text(inputadSeachXpath,dropdownListsearchAutoXpath,Searchstring)
 
     
#Enter string to be searched
keywordToSearch = ["Saturn","Krux","Saturday's Market"]

#Verify the creatives count on the search results page is correct for above 3 search texts
for searchText in keywordToSearch:
    verify_creatives_count(inputadSeachXpath,dropdownListsearchAutoXpath,elementparentLoadMoreXpath,buttonloadMoreXpath,imageContainerXpath,creativeCountText,searchText)
    driver.back()
    wait_for_element_to_load(inputadSeachXpath,5)

#Navigate forward to the existing browser window 
driver.forward()

#Capture title of the page when user clicked 'Random Brand' link for first time.
get_title_on_first_click = check_random_brand(RandomBrandText,linkRandomBrandXpath)

#Navigate backward to the existing browser window
driver.back()

#Capture title of the page when user clicked 'Random Brand' link for second time.
get_title_on_second_click = check_random_brand(RandomBrandText,linkRandomBrandXpath)
print("When user click on 'Random Brand' Link for first time value equals : "+get_title_on_first_click)
print("When user click on 'Random Brand' Link for second time value equals :"+get_title_on_second_click)

#Comparing values captured above
if get_title_on_first_click!=get_title_on_second_click:
   print("'Random Brand link' on the search results page is random")
   print "Testcase 3 Passed"
else:
   print("'Random Brand link' on the search results page is not random")
   print "Testcase 3 Failed"
 
#Wait for image to be displayed
wait_for_element_to_load(hoverImageXpath,5)

#hover over image
but_loc = driver.find_element_by_xpath(hoverImageXpath)
ActionChains(driver).move_to_element(but_loc).perform()

#Verify if Share ad Feature Link exist or not
if check_exists_by_xpath(ShareLinkText)!="False":
   #Click on Share Link
   driver.find_element_by_link_text(ShareLinkText).click()
   time.sleep(3)
   InputPopUpExist = check_exists_by_xpath(InputPopUpShare)
   if InputPopUpExist!="False":
      copyLink = driver.find_element_by_xpath(InputPopUpShare).get_attribute("value")
      print "Url is : "+copyLink
      print "Share ad feature link exists when hovering over an add & user is able to click it"
      print "Testcase 4 Passed"
   else:
      print "Share ad feature does not exist"
       
   #Click on Copy Link
   driver.find_element_by_xpath(btnCopyLinkXpath).click()

   #Close the Popup window
   driver.find_element_by_xpath(closePopupWindowXpath).click()
   
else:
   print "Share ad feature link does not exists when hovering over an add"
   print "Testcase 4 Failed"


#quit driver instance
#driver.quit()   
