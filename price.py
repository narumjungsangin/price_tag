import requests
import pandas as pd
from tkinter import filedialog
import xml.etree.ElementTree as ET
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from textwrap import wrap

file_path = filedialog.askopenfilename(title="Select an Excel file", filetypes=[("Excel files", "*.xls;*.xlsx")])

if file_path:
    df = pd.read_excel(file_path, header=None)
    
    data_a = df.loc[3:, 0]
    print(data_a)
    data_j = df.loc[3:, 9]
    print(data_j)
else:
    print("No file selected")

url = 'http://apis.data.go.kr/1471000/DrbEasyDrugInfoService/getDrbEasyDrugList'
params = {
    'serviceKey': '9FryoQCr7vKxyF1C7hDwfThWnPTAeXsK9xIyJ0GrF0%2BqmUA7RHpa7Xz8dgeFd2fq2b9YbuahROnLdLNfhDpWfg%3D%3D',
    'efcyQesitm': '',
    'type': 'xml'
}

data_list = []

for item_name, item_j in zip(data_a, data_j):
    params['itemName'] = item_name
    response = requests.get(url, params=params)
    
    # XML 응답을 파싱하여 efcyQesitm 값을 추출합니다
    root = ET.fromstring(response.content)
    efcyQesitm_elements = root.findall('.//efcyQesitm')
    
    if efcyQesitm_elements:
        description = efcyQesitm_elements[0].text  # 설명을 저장합니다
    else:
        description = "약품설명을 수기로 입력해주세요."  # 설명이 없는 경우 메시지를 저장합니다

    # 데이터 리스트에 약품 정보를 추가합니다
    data_list.append([item_name, item_j, description])
    print(f'약품명: {item_name} \n 가격: {item_j} \n 약품설명: {description}\n\n')

# 데이터 리스트 확인
for data in data_list:
    print(data)

pdfmetrics.registerFont(TTFont('NanumGothic', 'NanumGothic.ttf'))

# PDF 생성
c = canvas.Canvas("가격표.pdf", pagesize=A4)

width, height = A4

for i, (item_name, item_j, description) in enumerate(data_list):
    x = 50 + (i % 2) * 250  # 각 가격표의 x 좌표
    y = height - 50 - (i // 2) * 150  # 각 가격표의 y 좌표


    wrapped_description = wrap(description, 30)
    description_lines = wrapped_description[:3]  
    if len(wrapped_description) > 3:
        description_lines[-1] += '...'
    

    card_width = 230
    card_height = 120
    title_width = c.stringWidth(item_name, 'NanumGothic', 16)
    x_centered = x + (card_width - title_width) / 2
    c.roundRect(x, y - card_height, card_width, card_height, 10, stroke=1, fill=0)
    
    c.setFont("NanumGothic", 16)
    c.drawString(x_centered, y - 17, f"{item_name}")
    
    c.setFont("NanumGothic", 9)
    
    wrapped_description = wrap(description, 30)
    description_lines = wrapped_description[:4]  
    if len(wrapped_description) > 3:
        description_lines[-1] += '...'
    y_text_start = y - 40
    line_height = 14 
    for j, line in enumerate(description_lines):
        c.drawString(x + 10, y_text_start - (j * line_height), line)

    
    title_width = c.stringWidth(str(item_j), 'NanumGothic', 16)
    x_centered = x + (card_width - title_width) / 2
    c.setFont("NanumGothic", 16)
    c.drawString(x_centered, y - 110, f"{item_j}")

    
    if (i + 1) % 8 == 0:
        c.showPage()
c.save()
