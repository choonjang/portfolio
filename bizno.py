import requests
import os

def get_company_info(api_key, query):
    url =f"https://bizno.net/api/fapi?key={api_key}&q={query}&type=json"
    response = requests.get(url)
    print(response.text)
    
def process_companies(api_key, input_file, output_file):
    with open(input_file,'r',encoding='utf-8') as f:
        companies = f.read().splitlines()
    
    with open(output_file,'w',encoding='utf-8') as f:
        for company in companies:
            info = get_company_info(api_key, company)
            print(info)
            if info['resultCode'] in error_code_dic.keys():
                print(error_code_dic[info['resultCode']])
                break
            print(f"{company} -> 작업 시작")
            for item in info['items']:
                if item == None:
                    break
                try:
                    f.write(f'------------------------------------------------\n')
                    f.write(f"회사명: {item['company']}\n")
                    f.write(f"사업자등록번호: {item['bno']}\n")
                    f.write(f"법인등록번호: {item['cno']}\n")
                    f.write(f"사업자상태(명칭): {item['bstt']}\n")
                    f.write(f"과세유형(명칭): {item['taxtype']}\n")
                    f.write(f'------------------------------------------------\n')
                except Exception:
                    f.write(f'------------------------------------------------\n')
                    f.write(f"상호명 : {company} -> 검색할 수 없습니다.\n")
                    f.write(f'------------------------------------------------\n')
            print(f"{company} -> 작업 종료")
    print("최종 처리완료")

dir_path = os.path.dirname(os.path.realpath(__file__))

api_key = ""    ####
input_file = f"{dir_path}/companies.txt"
output_file = f"{dir_path}/company_info.txt"

error_code_dic = {
    -1 : "등록되지 않은 사용자",
    -2 : "파라미터 오류",
    -3 : "1일 200건 초과",
    -9 : "기타에러"
    }

process_companies(api_key,input_file,output_file)