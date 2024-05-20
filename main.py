import requests
from bs4 import BeautifulSoup as BS

def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return 'oshibka'


def get_links(html):
    soup = BS(html, 'html.parser')
    links = []

    container = soup.find('div', class_='container body-container')
    if container:
        posts = container.find_all('div', class_='category-block-content-item')
        for post in posts:
            link = post.find('a').get('href')
            full_link = 'https://www.house.kg' + link 
            links.append(full_link)

    return links




def get_posts(links):
    titles = []
    descriptions = []
    for link in links:
        html = get_html(link)
        soup = BS(html, 'html.parser')
        title_tag = soup.find('h1')
        descrip_tag = soup.find('p')

        title = title_tag.text.strip()
        description = descrip_tag.text.strip()
        
        titles.append(title)
        descriptions.append(description)
    
    return titles, descriptions

    


def save_in_txt(titles, descriptions, filename='output.txt'):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write('Title\t and Description\n')
        for i in range(len(titles)):
            file.write(f'{titles[i]}\t\n{descriptions[i]}\n\n\nNew post\nTitle\n\n')
    print(f'Data saved in file {filename}')




def main():
    URL = 'https://www.house.kg/'
    html = get_html(URL)
    links = get_links(html)

    if links:
        titles, descriptions = get_posts(links)

        if titles and descriptions:
            save_in_txt(titles, descriptions)
        else:
            print("No data to save.")
    else:
        print("No links found.")

if __name__ == '__main__':
    main()
