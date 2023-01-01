from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys as keys
import os
import pandas as pd
import numpy as np

import time
from datetime import datetime, timedelta

today=datetime.strftime(datetime.now(), '%d-%m-%Y')

currpath=os.getcwd()
f= open(currpath + "\SERA_FOE"+today+".txt","a+")
odpath=currpath.replace("phyton\db_python\SERA Module","")
print(odpath)

TODB=pd.read_csv(odpath+ '00FlightPlan Runway Analysis\Output Files\PerformanceTODB.csv', header=0, names=("Airport", "Runway", "MTOW"))
LDDB=pd.read_csv(odpath+ '00FlightPlan Runway Analysis\Output Files\PerformanceLDDB.csv', header=0, names=("Airport", "Runway", "LNDW"))

driver= webdriver.Chrome()


driver.get("https://sera.com.au/")

driver.find_element(By.XPATH, "/html/body/form/div/section/div[2]/div[2]/div/div/input[1]").send_keys("xxxx")
driver.find_element(By.XPATH,"/html/body/form/div/section/div[2]/div[2]/div/div/input[2]").send_keys("xxxx")
driver.find_element(By.XPATH,"/html/body/form/div/section/div[2]/div[2]/div/div/input[3]").send_keys("xxxx")
time.sleep(1)
driver.find_element(By.XPATH,'/html/body/form/div/section/div[2]/div[2]/div/div/input[4]').click()
#alert_obj = driver.switch_to.alert
#alert_obj.accept()

wait=WebDriverWait(driver,20)


wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="navigation"]/li[21]/a'))
elem0=driver.find_element(By.XPATH,'//*[@id="navigation"]/li[21]/a')
driver.execute_script("arguments[0].click();", elem0)


wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/a'))
elem1=driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/a')
driver.execute_script("arguments[0].click();", elem1)

wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/ul/li/a'))

elem2=driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/ul/li/a')
driver.execute_script("arguments[0].click();", elem2)



for j in range(12, 13):
    if j>=11:
        for i in range(0, 50):
            clkpages='//*[@id="grid_mt"]/div[5]/div/div[1]/a[' + str(11)+']'
            
            
            wait.until(lambda driver: driver.find_element(By.XPATH,clkpages))
            elem8=driver.find_element(By.XPATH,clkpages)
            driver.execute_script("arguments[0].click();", elem8)
            
            wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="grid_mt"]/div[5]/div/div[2]/strong[1]'), "11"))
       
        
            clkpages='//*[@id="grid_mt"]/div[5]/div/div[1]/a[' + str(j-9)+']'
            clkitems='//*[@id="grid_mt_r' + str(i) +'_grid_mt_c0"]/div/a'
            codeitems='//*[@id="grid_mt_r' + str(i) +'_grid_mt_c3"]/div'
           
            try:

           
                wait.until(lambda driver: driver.find_element(By.XPATH,clkpages))
                elem8=driver.find_element(By.XPATH,clkpages)
                driver.execute_script("arguments[0].click();", elem8)
                
                wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="grid_mt"]/div[5]/div/div[2]/strong[1]'), str(j)))
                           
                wait.until(lambda driver: driver.find_element(By.XPATH,codeitems))
                icaoname=driver.find_element(By.XPATH,codeitems).text

                elem3=driver.find_element(By.XPATH,clkitems)
                driver.execute_script("arguments[0].click();", elem3)
                
                TOW="-"
                LDW="-"
                for kk in range(len(TODB.index)):           
                    if TODB.iat[kk, 0].strip()==icaoname:
                        TOW=TODB.iat[kk,2]
                               
                for ll in range(len(LDDB.index)):
                    if LDDB.iat[ll, 0].strip()==icaoname:
                        LDW=LDDB.iat[ll,2]
                if TOW=="-":
                    f.write(icaoname + "Has no data in the PerfDB")

                param= icaoname+ " "+ str(TOW) + " " + str(LDW)
                engcom=("Review date:"  + str(today) + "\n" 
                "Takeoff & Landing Analysis \n" 
                "Config: 30C, 5 flap, 26 K Thrust Rating, Bleed-off, DRY runway, 0 wind and Standard QNH \n" \
                "Airport TOW LDW \n" + \
                        param)
                
                wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="aerodromes"]/table[1]/tbody/tr[8]/td'))
                 
                    
                driver.switch_to.frame(driver.find_element(By.ID, "engComment_ifr"))
                
                elem=driver.find_element(By.XPATH,"/html/body")
                elem.clear()
                elem.send_keys(engcom)
                time.sleep(1)
                driver.switch_to.default_content()

             
                wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="saveBtn"]'))
                elem4=driver.find_element(By.XPATH,'//*[@id="saveBtn"]')
                driver.execute_script("arguments[0].click();", elem4)
            except:
                f.write("timeoutexception")
           
                f.write(icaoname + "couldnt be updated")
                
            finally:
                
                wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="navigation"]/li[21]/a'))
                elem5=driver.find_element(By.XPATH,'//*[@id="navigation"]/li[21]/a')
                driver.execute_script("arguments[0].click();", elem5)
                
                wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/a'))
                elem6=driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/a')
                driver.execute_script("arguments[0].click();", elem6)

                wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/ul/li/a'))
                elem7=driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/ul/li/a')
                driver.execute_script("arguments[0].click();", elem7)
        
        
    else:
        for i in range(0, 50):
            clkpages='//*[@id="grid_mt"]/div[5]/div/div[1]/a[' + str(j)+']'
            clkitems='//*[@id="grid_mt_r' + str(i) +'_grid_mt_c0"]/div/a'
            codeitems='//*[@id="grid_mt_r' + str(i) +'_grid_mt_c3"]/div'
           
            try:
    
           
                wait.until(lambda driver: driver.find_element(By.XPATH,clkpages))
                elem8=driver.find_element(By.XPATH,clkpages)
                driver.execute_script("arguments[0].click();", elem8)
                
                wait.until(EC.text_to_be_present_in_element((By.XPATH, '//*[@id="grid_mt"]/div[5]/div/div[2]/strong[1]'), str(j)))
                           
                wait.until(lambda driver: driver.find_element(By.XPATH,codeitems))
                icaoname=driver.find_element(By.XPATH,codeitems).text
    
                elem3=driver.find_element(By.XPATH,clkitems)
                driver.execute_script("arguments[0].click();", elem3)
                
                TOW="-"
                LDW="-"
                for kk in range(len(TODB.index)):           
                    if TODB.iat[kk, 0].strip()==icaoname:
                        TOW=TODB.iat[kk,2]
                               
                for ll in range(len(LDDB.index)):
                    if LDDB.iat[ll, 0].strip()==icaoname:
                        LDW=LDDB.iat[ll,2]
                if TOW=="-":
                    f.write(icaoname + "Has no data in the PerfDB")
    
                param= icaoname+ " "+ str(TOW) + " " + str(LDW)
                engcom=("Review date:"  + str(today) + "\n" 
                "Takeoff & Landing Analysis \n" 
                "Config: 30C, 5 flap, 26 K Thrust Rating, Bleed-off, DRY runway, 0 wind and Standard QNH \n" \
                "Airport TOW LDW \n" + \
                        param)
                
                wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="aerodromes"]/table[1]/tbody/tr[8]/td'))
                 
                    
                driver.switch_to.frame(driver.find_element(By.ID, "engComment_ifr"))
                
                elem=driver.find_element(By.XPATH,"/html/body")
                elem.clear()
                elem.send_keys(engcom)
                time.sleep(1)
                driver.switch_to.default_content()
    
             
                wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="saveBtn"]'))
                elem4=driver.find_element(By.XPATH,'//*[@id="saveBtn"]')
                driver.execute_script("arguments[0].click();", elem4)
            except:
                f.write("timeoutexception")
           
                f.write(icaoname + "couldnt be updated")
                
            finally:
                
                wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="navigation"]/li[21]/a'))
                elem5=driver.find_element(By.XPATH,'//*[@id="navigation"]/li[21]/a')
                driver.execute_script("arguments[0].click();", elem5)
                
                wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/a'))
                elem6=driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/a')
                driver.execute_script("arguments[0].click();", elem6)
    
                wait.until(lambda driver: driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/ul/li/a'))
                elem7=driver.find_element(By.XPATH,'//*[@id="toggleButtons"]/li[4]/ul/li/a')
                driver.execute_script("arguments[0].click();", elem7)

f.close



