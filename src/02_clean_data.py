import pandas as pd


# -----------------------------------------
# 1. LOAD THE TWO RETAILER FILES
# -----------------------------------------

df_a = pd.read_csv("data/raw/retailer_A.csv")
df_b = pd.read_csv("data/raw/retailer_B.csv")


# -----------------------------------------
# 2. CLEAN PRODUCT NAME
# -----------------------------------------

def clean_product_name(name):

    name = str(name)

    # Convert to lowercase
    name = name.lower()

    # Replace hyphen with space
    name = name.replace("-", " ")

    # Remove extra spaces
    name = " ".join(name.split())

    return name


df_a["clean_name"] = df_a["product_name"].apply(clean_product_name)
df_b["clean_name"] = df_b["product_name"].apply(clean_product_name)


# -----------------------------------------
# 3. CLEAN BRAND
# -----------------------------------------

df_a["clean_brand"] = df_a["brand"].str.lower()
df_b["clean_brand"] = df_b["brand"].str.lower()


# -----------------------------------------
# 4. CLEAN CATEGORY
# -----------------------------------------

df_a["clean_category"] = df_a["category"].str.lower()
df_b["clean_category"] = df_b["category"].str.lower()


# -----------------------------------------
# 5. CLEAN SIZE
# -----------------------------------------

df_a["clean_size"] = df_a["size"].str.lower()
df_b["clean_size"] = df_b["size"].str.lower()


# -----------------------------------------
# 6. STANDARDIZE SIZE
# -----------------------------------------

def clean_size(size):

    size = str(size).lower().strip()

    if "litre" in size:
        number = size.replace("litre", "").strip()
        return float(number) * 1000

    if "ml" in size:
        number = size.replace("ml", "").strip()
        return float(number)

    if "gb" in size:
        number = size.replace("gb", "").strip()
        return float(number)

    if "g" in size:
        number = size.replace("g", "").strip()
        return float(number)

    if size.endswith("l"):
        number = size.replace("l", "").strip()
        return float(number) * 1000

    return size

df_a["standard_size"] = df_a["size"].apply(clean_size)
df_b["standard_size"] = df_b["size"].apply(clean_size)


# -----------------------------------------
# 7. CHECK MISSING VALUES
# -----------------------------------------

print("\nRetailer A missing values:")
print(df_a.isnull().sum())

print("\nRetailer B missing values:")
print(df_b.isnull().sum())


# -----------------------------------------
# 8. CHECK DUPLICATES
# -----------------------------------------

print("\nRetailer A duplicate IDs:")
print(df_a["product_id"].duplicated().sum())

print("\nRetailer B duplicate IDs:")
print(df_b["product_id"].duplicated().sum())


# -----------------------------------------
# 9. CHECK STANDARDIZED SIZES
# -----------------------------------------

print("\nRetailer A sizes:")
print(
    df_a[
        ["product_name", "size", "standard_size"]
    ]
)

print("\nRetailer B sizes:")
print(
    df_b[
        ["product_name", "size", "standard_size"]
    ]
)


# -----------------------------------------
# 10. SAVE CLEANED DATA
# -----------------------------------------

df_a.to_csv(
    "data/processed/retailer_A_clean.csv",
    index=False
)

df_b.to_csv(
    "data/processed/retailer_B_clean.csv",
    index=False
)


print("\nCleaning and standardization completed successfully!")