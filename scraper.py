import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import os

# Create a directory to store the output if not exists
if not os.path.exists('output'):
    os.makedirs('output')

def get_society_data(society_name):
    search_url = f"https://www.99acres.com/search.html?search_type=QS&text={society_name.replace(' ', '+')}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    
    try:
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            societies = soup.find_all('div', class_='srpTuple__tupleDetails')
            
            if societies:
                data_list = []
                for society in societies:
                    title = society.find('a', class_='srpTuple__propertyName').text.strip()
                    location = society.find('div', class_='srpTuple__propertyArea').text.strip()
                    price = society.find('div', class_='srpTuple__sp').text.strip()

                    data_list.append({
                        "Society Name": title,
                        "Location": location,
                        "Price": price
                    })
                
                return data_list
            else:
                print(f"No data found for {society_name}")
        else:
            print(f"Failed to fetch data from 99acres.com (Status Code: {response.status_code})")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    
    return []

def save_to_csv(data, filename):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")

if __name__ == "__main__":
    society_name = input("Enter the society name: ")
    data = get_society_data(society_name)
    if data:
        save_to_csv(data, f"output/{society_name.replace(' ', '_')}_data.csv")
