import pandas as pd


# -----------------------------------------
# CREATE ALL POSSIBLE PRODUCT PAIRS
# -----------------------------------------

results = []

for a in range(1, 11):

    for b in range(1, 11):

        retailer_a_id = f"A{a:03d}"
        retailer_b_id = f"B{b:03d}"

        # Same number means same product
        if a == b:
            true_match = 1
        else:
            true_match = 0

        results.append({
            "retailer_a_id": retailer_a_id,
            "retailer_b_id": retailer_b_id,
            "true_match": true_match
        })


# -----------------------------------------
# CONVERT TO DATAFRAME
# -----------------------------------------

ground_truth = pd.DataFrame(results)


# -----------------------------------------
# SAVE FILE
# -----------------------------------------

ground_truth.to_csv(
    "data/raw/ground_truth.csv",
    index=False
)


# -----------------------------------------
# SHOW RESULTS
# -----------------------------------------

print("Ground truth created successfully!")

print("\nTotal pairs:", len(ground_truth))

print("\nTrue matches:")
print(
    ground_truth["true_match"].value_counts()
)

print("\nFirst 10 rows:")
print(
    ground_truth.head(10)
)