from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import time, localtime, strftime, sleep
import random
import os
import json

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

option = Options()
option.add_argument('user-agent=' + user_agent)
# option.add_argument('headless')    # 브라우저를 띄우지 않고 진행
option.add_argument('--blink-settings=imagesEnabled=false')    # 이미지 로딩 X.
option.add_argument('--mute-audio')    # 음소거 설정
option.add_argument('incognito')    # 시크릿 모드 설정
driver = webdriver.Chrome(options=option)
# driver.implicitly_wait(5)    # 사이트 접속 불가 시 최대 대기시간
dir_path = os.path.dirname(os.path.realpath(__file__))

URL = ""    ####

# 결과 폴더 없을시 결과 폴더 생성
if os.path.exists(f"{dir_path}/결과") == True:
    pass
else:
    os.makedirs(f"{dir_path}/결과")

driver.get(URL)

tm = time()
local_tm = localtime(tm)
str_tm = strftime('%m월%d일_%H시%M분', local_tm)

####   로그인   ####
login_select = driver.find_element(By.XPATH, "/html/body/div[1]/table/tbody/tr/td[4]/table/tbody/tr[1]/td[1]/a/img")
login_select.click()

input_ID = driver.find_element(By.XPATH, "//*[@id='id']")
input_ID.send_keys("")    # 아이디 입력

sleep(0.5)    # 아이디 입력 후 대기시간

input_PW = driver.find_element(By.XPATH, "//*[@id='passwd']")
input_PW.send_keys("")    # 비밀번호 입력

sleep(0.5)    # 비밀번호 입력 후 대기시간

input_PW.send_keys(Keys.ENTER)    # 엔터 입력

####   메뉴이동   ####
menu_click = driver.find_element(By.XPATH, "/html/body/div[3]/ul/li[1]/a/img")
menu_click.click()

sleep(random.uniform(1.5, 2))    # 이동 후 대기시간

site_click = driver.find_element(By.XPATH, "//*[@id='img_r32']/a")
site_click.click()

sleep(random.uniform(1.5, 2))    # 이동 후 대기시간

####   크롤링 시작   ####
sel_cate1_dropbox = Select(driver.find_element(By.ID, "sel_cate1"))    # 대분류 목록 불러오기

sel_cate1_num = 1
sel_cate1_num_list = []
sel_cate1_dropbox_list = []

for sel_cate1_list in sel_cate1_dropbox.options:
    sel_cate1_num_list.append(f"{sel_cate1_num} : {sel_cate1_list.text}")
    sel_cate1_dropbox_list.append(sel_cate1_list.text)
    sel_cate1_num += 1
sel_cate1_num_lists = '\n'.join(sel_cate1_num_list)
print("크롤링 시작 대분류를 선택하십시오")
print(sel_cate1_num_lists)
sel_cate1_start = input("번호 선택 : ")
print(f"\n{sel_cate1_dropbox_list[int(sel_cate1_start) - 1]} 부터 크롤링 시작 하겠습니다.")

select_result_count = int(input("\n-------------------------\n상위 몇위 까지 추출 하시겠습니까?\n ※  0 선택 시 전체 추출\n\n순위선택: "))
if select_result_count == 0:
    select_result_count = 999999

for sel_cate1_select_list in sel_cate1_dropbox_list[int(sel_cate1_start) - 1 : ]:    # 대분류 수 만큼 반복
    excel_num = 1
    sel_cate1_dic = {}
    sel_cate1_dropbox.select_by_visible_text(sel_cate1_select_list)    # 대분류 선택
    sleep(random.uniform(2.8, 3.3))    # 대분류 선택 후 대기 시간
    sel_cate2_dropbox = Select(driver.find_element(By.ID, "sel_cate2"))    # 중분류 목록 불러오기
    for sel_cate2_select_list in sel_cate2_dropbox.options:    # 중분류 수 만큼 반복
        sel_cate2_dic = {}
        if sel_cate2_select_list.text == "중분류 선택":
            pass
        else:
            excel_B_start = excel_num + 1
            sel_cate2_dropbox.select_by_visible_text(sel_cate2_select_list.text)    # 중분류 선택
            sleep(random.uniform(2.8, 3.3))    # 중분류 선택 후 대기시간
            sel_cate3_dropbox = Select(driver.find_element(By.ID, "sel_cate3"))    # 소분류 목록 불러오기
            for sel_cate3_select_list in sel_cate3_dropbox.options:    # 소분류 수 만큼 반복
                sel_cate3_num = 0
                next_page = 0
                over_num = 1
                sel_cate3_list = []
                if len(sel_cate3_list) >= select_result_count:    # 선택한 상위 추출 수 도달시 다음 중분류로 이동
                    break
                if sel_cate3_select_list.text == "소분류 선택":
                    pass
                else:
                    excel_C_start = excel_num + 1
                    try:
                        page_now = driver.find_element(By.XPATH, "//*[@id='oPage']/tbody/tr/td[2]/font/b")    # 현재 페이지 가져오기
                        if page_now.text != "1":
                            page_click = driver.find_element(By.XPATH, "//*[@id='oPage']/tbody/tr/td[2]/a[1]")    # 1페이지로 이동(분류 이동 시 이전 페이지 번호를 가져오는 과정 대비)
                            page_click.click()
                            sleep(random.uniform(0.3, 1))    # 페이지 이동 후 대기시간
                        else:
                            pass
                    except:
                        pass
                    page_result = driver.find_element(By.XPATH, "//*[@id='oPage']/tbody/tr/td[3]")    # 페이지 수 가져오기
                    page_count = page_result.text.split(' ')
                    sel_cate3_dropbox.select_by_visible_text(sel_cate3_select_list.text)    # 소분류 선택
                    sleep(random.uniform(2.8, 3.3))    # 소분류 선택 후 대기시간
                    for page_select in range(int(page_count[1])):    # 페이지 수 만큼 반복
                        page_num = page_select + 1
                        if len(sel_cate3_list) >= select_result_count:    # 선택한 상위 추출 수 도달시 다음 중분류로 이동
                            break
                        for xpath_num in range(3, 23):    # data 수집 시작
                            if len(sel_cate3_list) >= select_result_count:    # 선택한 상위 추출 수 도달시 다음 중분류로 이동
                                break
                            try:
                                table_result = driver.find_element(By.XPATH, f"//*[@id='oTable']/tbody/tr[{xpath_num}]/td[2]/a")
                                table_result_url = table_result.get_attribute("href").split("url=")
                                one_day_peaple_visit = driver.find_element(By.XPATH, f"//*[@id='oTable']/tbody/tr[{xpath_num}]/td[9]")
                                one_day_page_view = driver.find_element(By.XPATH, f"//*[@id='oTable']/tbody/tr[{xpath_num}]/td[10]")
                                one_day_session_visit = driver.find_element(By.XPATH, f"//*[@id='oTable']/tbody/tr[{xpath_num}]/td[11]")
                                sel_cate3_num += 1
                                try:
                                    peaple_text = one_day_peaple_visit.text.replace(',', '')
                                    peaple_text = int(peaple_text)
                                except:
                                    peaple_text = one_day_peaple_visit.text.split(' ')[0]
                                    peaple_text = int(peaple_text) - 1
                                sel_cate3_list.append({"num" : sel_cate3_num, "site" : table_result.text, "URL" : table_result_url[1], "peaple" : peaple_text, "page" : one_day_page_view.text, "session" : one_day_session_visit.text})
                                print(f"num : {sel_cate3_num}, site : {table_result.text}, URL : {table_result_url[1]}, peaple : {peaple_text}, page : {one_day_page_view.text}, session : {one_day_session_visit.text}")
                            except:
                                try:
                                    sel_cate3_list.append({"num" : sel_cate3_num, "site" : table_result.text, "URL" : table_result_url[1], "peaple" : "", "page" : "", "session" : ""})
                                    print(f"num : {sel_cate3_num}, site : {table_result.text}, URL : {table_result_url[1]} , peaple : , page : , session : ")
                                except:
                                    break
                        try:
                            ####   페이지 이동    ####
                            if page_num % 10 == 0:
                                if page_num == 10:
                                    sleep(random.uniform(0.5, 1))    # 페이지 선택 후 대기시간
                                    page_click = driver.find_element(By.XPATH, "//*[@id='oPage']/tbody/tr/td[2]/a[10]/img")
                                    page_click.click()
                                else:
                                    sleep(random.uniform(0.5, 1))    # 페이지 선택 후 대기시간
                                    page_click = driver.find_element(By.XPATH, "//*[@id='oPage']/tbody/tr/td[2]/a[12]/img")
                                    page_click.click()
                                next_page += 1
                            elif page_num > 10:
                                sleep(random.uniform(0.5, 1))    # 페이지 선택 후 대기시간
                                page_click = driver.find_element(By.XPATH, f"//*[@id='oPage']/tbody/tr/td[2]/a[{page_num - next_page * 10 + 2}]")
                                page_click.click()
                            else:
                                sleep(random.uniform(0.5, 1))    # 페이지 선택 후 대기시간
                                page_click = driver.find_element(By.XPATH, f"//*[@id='oPage']/tbody/tr/td[2]/a[{page_num}]")
                                page_click.click()
                        except Exception as e:
                            break

    ####   딕셔너리 형태로 저장 ####                        
                    sel_cate2_dic[sel_cate3_select_list.text] = sel_cate3_list
            sel_cate1_dic[sel_cate2_select_list.text] = sel_cate2_dic

    ####   중간 저장(대분류 기준)   ####
    sel_cate1_name = sel_cate1_select_list
    sel_cate1_path = f"{dir_path}/결과/{sel_cate1_name.replace('/', '')} {str_tm}.json"
    with open(sel_cate1_path, 'w', encoding="UTF-8-sig") as writefile:
        json.dump({sel_cate1_select_list : sel_cate1_dic}, writefile, indent=4, ensure_ascii=False)

driver.close()