import pandas as pd
import os

# Products from Retailer A
retailer_a = {
    "product_id": ["A001", "A002", "A003", "A004", "A005",
                   "A006", "A007", "A008", "A009", "A010"],

    "product_name": [
        "Coca Cola Classic 1L",
        "Pepsi Cola 1L",
        "Dove Shampoo 650ml",
        "Pantene Shampoo 650ml",
        "Apple iPhone 15 128GB",
        "Samsung Galaxy S24 256GB",
        "Nike Air Max 270",
        "Maggi Noodles 70g",
        "Oreo Original Biscuits 120g",
        "Nivea Body Lotion 400ml"
    ],

    "brand": [
        "Coca Cola",
        "Pepsi",
        "Dove",
        "Pantene",
        "Apple",
        "Samsung",
        "Nike",
        "Maggi",
        "Oreo",
        "Nivea"
    ],

    "category": [
        "Soft Drinks",
        "Soft Drinks",
        "Shampoo",
        "Shampoo",
        "Smartphones",
        "Smartphones",
        "Footwear",
        "Food",
        "Food",
        "Personal Care"
    ],

    "size": [
        "1L", "1L", "650ml", "650ml", "128GB",
        "256GB", "US9", "70g", "120g", "400ml"
    ]
}

# Convert to DataFrame
df_a = pd.DataFrame(retailer_a)


# Products from Retailer B
retailer_b = {
    "product_id": ["B001", "B002", "B003", "B004", "B005",
                   "B006", "B007", "B008", "B009", "B010"],

    "product_name": [
        "Coca-Cola Classic 1000 ml",
        "Pepsi Cola 1 Litre",
        "Dove Hair Shampoo 650 ML",
        "Pantene Hair Shampoo 650 ML",
        "Apple iPhone 15 128 GB",
        "Samsung Galaxy S24 256 GB",
        "Nike Airmax 270",
        "Maggi Noodles 70 G",
        "Oreo Original 120g",
        "Nivea Body Lotion 400 ML"
    ],

    "brand": [
        "Coca-Cola",
        "Pepsi",
        "Dove",
        "Pantene",
        "Apple",
        "Samsung",
        "Nike",
        "Maggi",
        "Oreo",
        "Nivea"
    ],

    "category": [
        "Soft Drinks",
        "Soft Drinks",
        "Shampoo",
        "Shampoo",
        "Smartphones",
        "Smartphones",
        "Footwear",
        "Food",
        "Food",
        "Personal Care"
    ],

    "size": [
        "1000ml", "1L", "650ML", "650ML", "128GB",
        "256GB", "US9", "70G", "120g", "400ML"
    ]
}

df_b = pd.DataFrame(retailer_b)


# Create folder
os.makedirs("data/raw", exist_ok=True)


# Save files
df_a.to_csv("data/raw/retailer_A.csv", index=False)
df_b.to_csv("data/raw/retailer_B.csv", index=False)


print("Retailer A:")
print(df_a)

print("\nRetailer B:")
print(df_b)

print("\nFiles created successfully!")