from selenium import selenium
import time
from selenium import webdriver
from DBConnection import MysqlConnecttion

class sele:

    def __init__(self):
        self.verificationErrors = []
        self.selenium = selenium("localhost", 4444, "*chrome", "http://www.linkedin.com")
        self.selenium.start()
        self.driver = webdriver.Firefox()
 
    def __del__(self):
        self.selenium.stop()

    def start(self):
                sel = self.selenium
                sel.open("http://www.linkedin.com")
                time.sleep(2.5)
                sel.type("session_key", 'coleknowlden@frontier.com')
                time.sleep(3.0)
                sel.type("session_password", 'CoMaKn1387')
                time.sleep(1.0)
                sel.click('signin')
                time.sleep(3.0)
    def start2(self):
                driv = self.driver
                driv.get("http://www.linkedin.com")
                time.sleep(2.5)
                sk = driv.find_element_by_name("session_key")
                sk.send_keys('coleknowlden@frontier.com')
                time.sleep(3.0)
                sp = driv.find_element_by_name("session_password")
                sp.send_keys('CoMaKn1387')
                sign = driv.find_element_by_name("signin")
                time.sleep(1.0)
                sign.click()
                time.sleep(3.0)
    def startgoogle(self):
            driver = webdriver.Firefox()
            sel = self.selenium
            time.sleep(3.0)
            sel.open("http://www.google.com")
            local_sql = MysqlConnecttion("local")
            query = r"select author from authors"
            rows = local_sql.excute_with_result(query)
            for row in rows:
                time.sleep(3.0)
                sel.open("http://www.google.com")
                time.sleep(3.0)
                str1 = str(row[0]) + ' gartner analyst profile'
                sel.type("q", str1)
                time.sleep(3.0)
                sel.click('btnI')
                time.sleep(3.0)
                driver.get(sel.get_location())
                i= 0
                try:
                    yes = 0
                    x = driver.find_elements_by_class_name('anText')
                    for y in x:
                        if y.text == 'Roles and Responsibilities':
                            str1 = x[i+1].text
                            str1 = str(str1.replace("'",""))
                            query = r"UPDATE authors set gartner_roles = '%s' WHERE author = '%s'"%(str1, row[0])
                            local_sql.excute(query)
                        if y.text == 'Previous Experience':
                            str1 = x[i+1].text
                            str1 = str(str1.replace("'",""))
                            query = r"UPDATE authors set gartner_previous_experiance = '%s' WHERE author = '%s'"%(str1, row[0])
                            local_sql.excute(query)
                        if y.text == 'Professional Background':
                            str1 = ''
                            k = i
                            j = 0
                            while j == 0:
                                try:
                                    if x[k+1].text == "Education":
                                        j = 1
                                    else:
                                        str1 = str1 + x[k+1].text + '; '
                                    k = k+1
                                except:
                                    j = 1
                                    pass
                            str1 = str(str1.replace("'",""))
                            query = r"UPDATE authors set gartner_professional_bg = '%s' WHERE author = '%s'"%(str1, row[0])
                            local_sql.excute(query)
                        if y.text == 'Education':
                            str1 = ''
                            k = i
                            j = 0
                            while j == 0:
                                try:
                                    if x[k+1].text == "LATEST RESEARCH":
                                        j = 1
                                    else:
                                        str1 = str1 + x[k+1].text + '; '
                                    k = k+1
                                except:
                                    j = 1
                                    pass
                            str1 = str(str1.replace("'",""))
                            query = r"UPDATE authors set gartner_education = '%s' WHERE author = '%s'"%(str1, row[0])
                            local_sql.excute(query)
                        if y.text == 'Areas of Coverage':
                            yes = 1
                        i = i+1
                    x = driver.find_elements_by_class_name('hdrName')
                    for y in x:
                        str1 = y.text
                        str1 = str(str1.replace("'",""))
                        query = r"UPDATE authors set gartner_name = '%s' WHERE author = '%s'"%(str1, row[0])
                        local_sql.excute(query)
                    if yes == 1:
                        x = driver.find_elements_by_class_name('resourceThinBlueLink')
                        str1 = ''
                        for y in x:
                            if y.text == 'View Latest Research':
                                str1 = str(str1.replace("'",""))
                                query = r"UPDATE authors set gartner_areas_of_coverage = '%s' WHERE author = '%s'"%(str1, row[0])
                                local_sql.excute(query)
                                break
                            else:
                                str1 = str1  + y.text + '; '
                except:
                    print "what"
                    continue
                    pass
                
    def after_login(self):
        sel = self.selenium
        # check login succeed before going on
        local_sql = MysqlConnecttion("local")
        query = r"select author from authors where profilelink is null"
        rows = local_sql.excute_with_result(query)
        for row in rows:
            time.sleep(10.0)
            str1 = str(row[0]) + ' gartner'
            sel.type("keywords", str1)
            time.sleep(1.0)
            sel.click('search')
            time.sleep(3.0)
            try:
                x = "http://www.linkedin.com" + sel.get_attribute('//li[@data-li-position="0"]/a/@href')
            except:
                try:
                    x = "http://www.linkedin.com" + sel.get_attribute('//li[@data-li-position="1"]/a/@href')
                except:
                    query = r"UPDATE authors set profilelink = 'NONE' WHERE author = '%s'"%(row[0])
                    local_sql.excute(query)
                    continue
                    pass
                query = r"UPDATE authors set profilelink = '%s' WHERE author = '%s'"%(x, row[0])
                local_sql.excute(query)
                continue
                pass
            query = r"UPDATE authors set profilelink = '%s' WHERE author = '%s'"%(x, row[0])
            local_sql.excute(query)

    def after_login2(self):
        driv = self.driver
        # check login succeed before going on
        local_sql = MysqlConnecttion("local")
        query = r"select profilelink from authors where profilelink != 'NONE' and linkedin_name is NULL"
        rows = local_sql.excute_with_result(query)
        for row in rows:
            driv.get(row[0])
            time.sleep(5.0)
            try:
                x = driv.find_element_by_id('name')
                query = r"UPDATE authors set linkedin_name = '%s' WHERE profilelink = '%s'"%(x.text, row[0])
                local_sql.excute(query)
            except:
                pass
            try:
                x = driv.find_element_by_id('summary-item-view')
                str1 = x.text
                str2 = str1.replace("'","")
                query = r"UPDATE authors set linkedin_summary = '%s' WHERE profilelink = '%s'"%(str2, row[0])
                local_sql.excute(query)
            except:
                pass
            try:
                x = driv.find_element_by_id('background-experience')
                str1 = x.text
                str2 = str1.replace("'","")
                query = r"UPDATE authors set linkedin_experience = '%s' WHERE profilelink = '%s'"%(str2, row[0])
                local_sql.excute(query)
            except:
                print "what"
                pass
            try:
                x = driv.find_elements_by_class_name('endorse-item-name-text')
                str1 = ''
                for y in x:
                    str1 = str1 + y.text + '; '
                str1 = str(str1.replace("'",""))
                query = r"UPDATE authors set linkedin_skills = '%s' WHERE profilelink = '%s'"%(str1, row[0])
                local_sql.excute(query)
            except:
                pass
            try:
                x = driv.find_element_by_id('background-education')
                str1 = x.text
                str2 = str1.replace("'","")
                query = r"UPDATE authors set linkedin_education= '%s' WHERE profilelink = '%s'"%(str2, row[0])
                local_sql.excute(query)
            except:
                pass
           
            



s = sele()
s.startgoogle()
