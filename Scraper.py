import requests
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt

# STEP 1: Fetch data
url = "http://books.toscrape.com/"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_ = "product_pod")

# STEP 2: Extract data
rating_map = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

data = []

for book in books:
    title = book.h3.a["title"]
    price = book.find("p", class_ ="price_color").text
    availability = book.find("p", class_="instock availability").text.strip()
    # Extract ratings
    rating_text = book.find("p", class_ = "star-rating")["class"][1]
    rating = rating_map[rating_text]
    
    data.append({
        "title": title,
        "price": price,
        "availability": availability,
        "rating": rating
    })
print(data[:5])

# STEP 3: Create DataFrame
df = pd.DataFrame(data)

# STEP 4: Data Cleaning
df["price"] = df["price"].str.replace("Â£", "").astype(float)  # remove Â£ and convert it into float
df["availability"] = df["availability"].str.replace("In stock", "Available") # replace "in stock" to "available"

# STEP 5: Save CSV
df.to_csv("books.csv", index=False)  

# STEP 6: Analysis
# Average of the prices
print("Average price:", df["price"].mean())
#Rating counts
print(df["rating"].value_counts())


#STEP 7: Visualization
# sort ratings properly
rating_counts = df["rating"].value_counts().sort_index()

plt.figure(figsize=(8,5))
rating_counts.plot(kind="bar")  
plt.title("Book Rating Distribution", fontsize=14)
plt.xlabel("Rating (1 to 5)", fontsize=12)
plt.ylabel("Number of Books", fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()

# Price vs Rating
df.groupby("rating")["price"].mean().plot(kind="bar")
plt.title("Average Price by Rating")
plt.xlabel("Rating (1 to 5)")   # 👈 x-axis name
plt.ylabel("Average Price")  
plt.show()

# Top expensive books
print(df.sort_values(by="price", ascending=False).head(5))


