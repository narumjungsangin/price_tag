import pandas as pd
from bs4 import BeautifulSoup

csv = pd.read_csv('list.csv', names=['color', 'size', 'name', 'price1', 'price2', 'explanation1', 'explanation2', 'explanation3'], encoding='CP949')
print(csv)

x = input("가격표 출력이 필요한 약 번호를 입력해주세요: ")

try:
    x = int(x)  # Convert input to an integer
    if x <= 0 or x > len(csv):
        print("번호표 안의 숫자를 입력해주세요")
    else:
        selected_row = csv.loc[x - 1]  # Subtract 1 to align with zero-based indexing

        # Extract values from the selected row
        color = selected_row['color']
        size = selected_row['size']
        name = selected_row['name']
        price1 = selected_row['price1']
        price2 = selected_row['price2']
        explanation1 = selected_row['explanation1']
        explanation2 = selected_row['explanation2']

        # Check if explanation3 exists in the DataFrame
        if 'explanation3' in csv.columns:
            explanation3 = selected_row['explanation3']
        else:
            explanation3 = 'N/A'

        print("Medicine Name:", name)
        print("Price:", price1, ",", price2)
        print("Explanation1:", explanation1)
        print("Explanation2:", explanation2)
        print("Explanation3:", explanation3)

        def sizehtml(size):
            html = ""  # Initialize html with an empty string
            if size == "대":
                with open('pricetag_design.html', 'r', encoding='utf-8') as file:
                    html = file.read()
            elif size == "중":
                with open('pricetag_design.html', 'r', encoding='utf-8') as file:
                    html = file.read()
            elif size == "소":
                with open('pricetag_design.html', 'r', encoding='utf-8') as file:
                    html = file.read()
            return html

        html = sizehtml(size)
        # Parse the HTML
        soup = BeautifulSoup(html, 'html.parser')

        # Find the <ul> element with class "explanation"
        ul = soup.find('ul', class_='explanation')

        h1 = soup.find('h1')
        h1.string = str(name)  # Convert name to a string before assigning
        # 설명 1
        li1 = ul.find('li')
        li1.string = str(price1)  # Convert price1 to a string before assigning

        # 설명 2
        li2 = li1.find_next('li')
        li2.string = str(explanation1)  # Convert explanation1 to a string before assigning

        # 설명 3
        li3 = li2.find_next('li')
        li3.string = str(explanation2)  # Convert explanation2 to a string before assigning

           # Write the modified HTML back to the file
        with open('pricetag_design.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

        print("HTML file modified successfully.")

except ValueError:
    print("유효한 번호를 입력해주세요")