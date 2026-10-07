import pandas as pd
from rapidfuzz import fuzz


# -----------------------------------------
# 1. LOAD CLEANED DATA
# -----------------------------------------

df_a = pd.read_csv("data/processed/retailer_A_clean.csv")
df_b = pd.read_csv("data/processed/retailer_B_clean.csv")


# -----------------------------------------
# 2. CREATE EMPTY LIST FOR RESULTS
# -----------------------------------------

results = []


# -----------------------------------------
# 3. COMPARE EVERY PRODUCT
# -----------------------------------------

for i in range(len(df_a)):

    product_a = df_a.iloc[i]

    for j in range(len(df_b)):

        product_b = df_b.iloc[j]

        # Brand comparison
        if product_a["clean_brand"] == product_b["clean_brand"]:
            brand_score = 25
        else:
            brand_score = 0

        # Category comparison
        if product_a["clean_category"] == product_b["clean_category"]:
            category_score = 20
        else:
            category_score = 0

        # Size comparison
        if product_a["standard_size"] == product_b["standard_size"]:
            size_score = 20
        else:
            size_score = 0

        # Product name similarity
        name_similarity = fuzz.token_sort_ratio(
            product_a["clean_name"],
            product_b["clean_name"]
        )

        # Convert similarity into points out of 35
        name_score = (name_similarity / 100) * 35

        # Total score
        total_score = (
            brand_score
            + category_score
            + size_score
            + name_score
        )

        # ---------------------------------
        # 4. DECISION
        # ---------------------------------

        if total_score >= 80:
            decision = "Auto Match"

        elif total_score >= 60:
            decision = "Human Review"

        else:
            decision = "Reject"

        # ---------------------------------
        # 5. SAVE RESULT
        # ---------------------------------

        results.append({
            "retailer_a_id": product_a["product_id"],
            "retailer_a_name": product_a["product_name"],
            "retailer_b_id": product_b["product_id"],
            "retailer_b_name": product_b["product_name"],
            "brand_score": brand_score,
            "category_score": category_score,
            "size_score": size_score,
            "name_similarity": round(name_similarity, 2),
            "total_score": round(total_score, 2),
            "decision": decision
        })


# -----------------------------------------
# 6. CONVERT RESULTS TO DATAFRAME
# -----------------------------------------

matches = pd.DataFrame(results)


# -----------------------------------------
# 7. SORT BY HIGHEST SCORE
# -----------------------------------------

matches = matches.sort_values(
    "total_score",
    ascending=False
)


# -----------------------------------------
# 8. SHOW TOP MATCHES
# -----------------------------------------

print("\nTop product matches:")
print(
    matches[
        [
            "retailer_a_id",
            "retailer_a_name",
            "retailer_b_id",
            "retailer_b_name",
            "total_score",
            "decision"
        ]
    ].head(20)
)


# -----------------------------------------
# 9. SHOW DECISION COUNTS
# -----------------------------------------

print("\nDecision summary:")
print(
    matches["decision"].value_counts()
)


# -----------------------------------------
# 10. SAVE RESULTS
# -----------------------------------------

matches.to_csv(
    "data/processed/product_matching_results.csv",
    index=False
)

print("\nProduct matching completed successfully!")