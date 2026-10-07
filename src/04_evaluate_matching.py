import pandas as pd


# -----------------------------------------
# 1. LOAD OUR MATCHING RESULTS
# -----------------------------------------

matches = pd.read_csv(
    "data/processed/product_matching_results.csv"
)


# -----------------------------------------
# 2. LOAD THE GROUND TRUTH
# -----------------------------------------

ground_truth = pd.read_csv(
    "data/raw/ground_truth.csv"
)


# -----------------------------------------
# 3. COMBINE THE TWO FILES
# -----------------------------------------

evaluation = pd.merge(
    matches,
    ground_truth,
    on=["retailer_a_id", "retailer_b_id"]
)


# -----------------------------------------
# 4. CREATE OUR PREDICTION
# -----------------------------------------

evaluation["predicted_match"] = 0

evaluation.loc[
    evaluation["decision"] == "Auto Match",
    "predicted_match"
] = 1


# -----------------------------------------
# 5. CALCULATE CORRECT PREDICTIONS
# -----------------------------------------

correct = (
    evaluation["predicted_match"]
    == evaluation["true_match"]
).sum()

total = len(evaluation)


# -----------------------------------------
# 6. ACCURACY
# -----------------------------------------

accuracy = (correct / total) * 100


# -----------------------------------------
# 7. PRECISION
# -----------------------------------------

true_positives = (
    (evaluation["predicted_match"] == 1)
    & (evaluation["true_match"] == 1)
).sum()

predicted_positives = (
    evaluation["predicted_match"] == 1
).sum()

if predicted_positives > 0:
    precision = (
        true_positives / predicted_positives
    ) * 100
else:
    precision = 0


# -----------------------------------------
# 8. RECALL
# -----------------------------------------

actual_positives = (
    evaluation["true_match"] == 1
).sum()

if actual_positives > 0:
    recall = (
        true_positives / actual_positives
    ) * 100
else:
    recall = 0


# -----------------------------------------
# 9. PRINT RESULTS
# -----------------------------------------

print("\nMATCHING EVALUATION")
print("--------------------------")

print("Evaluated pairs:", total)

print(
    "Correct predictions:",
    correct
)

print(
    "Accuracy:",
    round(accuracy, 2),
    "%"
)

print(
    "Precision:",
    round(precision, 2),
    "%"
)

print(
    "Recall:",
    round(recall, 2),
    "%"
)


# -----------------------------------------
# 10. SHOW DETAILED RESULTS
# -----------------------------------------

print("\nDetailed evaluation:")
print(
    evaluation[
        [
            "retailer_a_id",
            "retailer_b_id",
            "decision",
            "true_match"
        ]
    ]
)


# -----------------------------------------
# 11. SAVE EVALUATION
# -----------------------------------------

evaluation.to_csv(
    "data/processed/evaluation_results.csv",
    index=False
)

print("\nEvaluation completed successfully!")