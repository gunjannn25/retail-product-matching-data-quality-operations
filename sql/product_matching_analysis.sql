-- Product Matching Analysis
-- Retail Product Matching, Data Coding & Quality Operations
-- MySQL

-- 1. Matching decision summary
SELECT
    decision,
    COUNT(*) AS pair_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM evaluation_results), 1) AS share_pct
FROM evaluation_results
GROUP BY decision
ORDER BY pair_count DESC;

-- 2. Main KPIs
SELECT
    COUNT(*) AS total_pairs,
    SUM(CASE WHEN decision = 'Auto Match' THEN 1 ELSE 0 END) AS auto_matches,
    SUM(CASE WHEN decision = 'Human Review' THEN 1 ELSE 0 END) AS human_review,
    SUM(CASE WHEN decision = 'Reject' THEN 1 ELSE 0 END) AS rejected_pairs,
    ROUND(100.0 * SUM(CASE WHEN decision = 'Auto Match' THEN 1 ELSE 0 END) / COUNT(*), 1) AS auto_match_rate
FROM evaluation_results;

-- 3. Accuracy, precision and recall
SELECT
    ROUND(100.0 * SUM(CASE WHEN true_match = predicted_match THEN 1 ELSE 0 END) / COUNT(*), 1) AS accuracy_pct,
    ROUND(100.0 * SUM(CASE WHEN true_match = 1 AND predicted_match = 1 THEN 1 ELSE 0 END)
          / NULLIF(SUM(CASE WHEN predicted_match = 1 THEN 1 ELSE 0 END), 0), 1) AS precision_pct,
    ROUND(100.0 * SUM(CASE WHEN true_match = 1 AND predicted_match = 1 THEN 1 ELSE 0 END)
          / NULLIF(SUM(CASE WHEN true_match = 1 THEN 1 ELSE 0 END), 0), 1) AS recall_pct
FROM evaluation_results;

-- 4. Match quality breakdown
SELECT
    CASE
        WHEN true_match = 1 AND predicted_match = 1 THEN 'True Positive'
        WHEN true_match = 0 AND predicted_match = 1 THEN 'False Positive'
        WHEN true_match = 1 AND predicted_match = 0 THEN 'False Negative'
        ELSE 'True Negative'
    END AS match_status,
    COUNT(*) AS pair_count
FROM evaluation_results
GROUP BY match_status
ORDER BY pair_count DESC;

-- 5. Score analysis by decision
SELECT
    decision,
    COUNT(*) AS pair_count,
    ROUND(AVG(total_score), 2) AS avg_match_score,
    ROUND(MIN(total_score), 2) AS min_score,
    ROUND(MAX(total_score), 2) AS max_score
FROM evaluation_results
GROUP BY decision
ORDER BY avg_match_score DESC;

-- 6. False negatives / records needing attention
SELECT
    retailer_a_id,
    retailer_a_name,
    retailer_b_id,
    retailer_b_name,
    brand_score,
    category_score,
    size_score,
    name_similarity,
    total_score,
    decision
FROM evaluation_results
WHERE true_match = 1
  AND predicted_match = 0;

-- 7. RCA flag for missed matches
SELECT
    retailer_a_id,
    retailer_a_name,
    retailer_b_id,
    retailer_b_name,
    brand_score,
    category_score,
    size_score,
    name_similarity,
    total_score,
    decision,
    CASE
        WHEN brand_score = 0 AND category_score > 0
             AND size_score > 0 AND name_similarity >= 80
            THEN 'Likely brand normalization issue'
        WHEN name_similarity < 60 THEN 'Low product-name similarity'
        WHEN category_score = 0 THEN 'Category mismatch'
        WHEN size_score = 0 THEN 'Size mismatch'
        ELSE 'Needs manual review'
    END AS rca_flag
FROM evaluation_results
WHERE true_match = 1
  AND predicted_match = 0;

-- 8. RCA detail for the identified A001/B001 pair.
-- The cleaned brand values are 'coca cola' and 'coca-cola'.
-- The current matching rule uses exact equality, so the hyphen
-- causes the brand comparison to fail.
SELECT
    a.product_id AS retailer_a_id,
    a.clean_brand AS retailer_a_clean_brand,
    b.product_id AS retailer_b_id,
    b.clean_brand AS retailer_b_clean_brand,
    REPLACE(a.clean_brand, '-', '') AS normalized_brand_a,
    REPLACE(b.clean_brand, '-', '') AS normalized_brand_b,
    CASE
        WHEN REPLACE(a.clean_brand, '-', '') =
             REPLACE(b.clean_brand, '-', '')
        THEN 'Brand match after normalization'
        ELSE 'Brand still different'
    END AS normalization_check
FROM retailer_a_clean a
JOIN retailer_b_clean b
  ON a.product_id = 'A001'
 AND b.product_id = 'B001';

-- RCA SUMMARY
-- Issue: one true match was not auto-accepted.
-- Root cause: 'coca cola' vs 'coca-cola' failed the exact brand comparison.
-- Supporting evidence: category_score = 20, size_score = 20,
-- name_similarity = 84.44, but brand_score = 0.
-- Corrective action: normalize punctuation/hyphens in brand fields
-- before applying the exact brand comparison.
-- Impact: the valid pair went to human review, contributing to 90% recall.
-- Note: this is a 100-pair synthetic evaluation, not production performance.
