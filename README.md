# Retail Product Matching & Data Quality Operations

**Domain:** Retail Data Operations · Product Master Data Management  
**Tools:** Python · SQL / MySQL · Power BI · Power Query · DAX · GitHub  
**Type:** End-to-end data pipeline — cleaning, matching, evaluation, RCA, dashboarding

---

## Why I Built This Project

Anyone who has worked with product data from multiple sources knows the problem immediately.

The same product arrives with different names, different units, different punctuation — from two different retailers, two different ERP systems, or two different suppliers. Matching them manually is slow, error-prone, and does not scale. Matching them blindly with a simple name comparison misses too many real matches and creates too many false ones.

This project was built to answer a question that sits at the core of retail data operations, pricing analysis, and category reporting:

> **How do you reliably identify that two differently-described product records are actually the same product — and what do you do when you are not sure?**

The answer this project builds is a transparent, scored, explainable matching workflow with three decision lanes: auto-match, human review, and reject. It is the kind of system a data operations team would actually use in production — not because it is perfect, but because it is honest about what it does not know.

---

## The Business Problem

When product data is received from multiple retail sources, the same item frequently appears in different formats:

| Retailer A | Retailer B |
|---|---|
| `Coca Cola Classic 1L` | `Coca-Cola Classic 1000 ml` |
| `Pepsi Cola 1L` | `Pepsi Cola 1 Litre` |
| `Dove Shampoo 650ml` | `Dove Hair Shampoo 650 ML` |

These are the same products. But differences in punctuation, spacing, unit formatting, hyphenation, and naming conventions make direct text matching fail.

When product matching goes wrong, the downstream effects compound quickly:

- Product catalogs show duplicate or split entries
- Pricing analysis compares the wrong products
- Category reports double-count or miss products entirely
- Retailer data integration breaks
- Market measurement becomes unreliable

This project addresses the root of that problem — not just by matching products, but by building a workflow that is transparent about its confidence, routes uncertain cases to human review, and investigates its own failures through Root Cause Analysis.

---

## Dataset

Two synthetic retailer product datasets were created to simulate real data-quality challenges.

| Dataset | Records |
|---|---|
| Retailer A | 10 |
| Retailer B | 10 |
| **Total pairs evaluated** | **100** |

The dataset intentionally introduces the most common real-world data quality issues:

- Spacing and hyphenation differences (`Coca Cola` vs `Coca-Cola`)
- Unit formatting variations (`1L` vs `1000 ml` vs `1 Litre`)
- Naming abbreviations (`Shampoo` vs `Hair Shampoo`)
- Brand value inconsistency

> **Note:** This dataset is fully synthetic. All metrics reported reflect evaluation results on this dataset and should not be interpreted as production system performance.

---

## Project Workflow

```
Raw Retail Data (Retailer A + Retailer B)
            ↓
    Data Cleaning & Standardization
            ↓
    Product Pair Generation (10 × 10 = 100 pairs)
            ↓
    Attribute-Based Matching Score
            ↓
    Confidence Classification
       ┌────┴────────┬──────────────┐
   Auto Match   Human Review    Reject
       └────┬────────┘
            ↓
    Ground Truth Evaluation
            ↓
    RCA — False Negative Investigation
            ↓
    SQL Operational Analysis
            ↓
    Power BI Dashboard
```

---

## How the Matching Works

Every product from Retailer A was compared against every product from Retailer B. For each pair, a composite match score was calculated across four weighted attributes:

| Attribute | Weight | Why this weight |
|---|---|---|
| Product Name Similarity | 35 | The strongest signal — fuzzy text match using RapidFuzz |
| Brand | 25 | Brand must agree for a valid match |
| Category | 20 | Category mismatch is a strong rejection signal |
| Product Size | 20 | Size must be comparable — units normalised before comparison |
| **Total** | **100** | |

Product name similarity was calculated using **fuzzy string matching** (RapidFuzz library) rather than exact text comparison. This captures partial matches and handles minor formatting differences.

### Matching Decision Rules

| Score Range | Decision | Meaning |
|---|---|---|
| ≥ 80 | **Auto Match** | High confidence — process automatically |
| 60 – 79 | **Human Review** | Uncertain — route to analyst queue |
| < 60 | **Reject** | Low confidence — not a match |

The human review lane is the most important design decision in this project. Forcing uncertain records into an automatic accept or reject decision creates silent errors. Routing them to a review queue makes the uncertainty visible and actionable.

---

## Key Results

| Metric | Result |
|---|---|
| Total Product Pairs Evaluated | 100 |
| Auto Matches | 9 |
| Human Review | 3 |
| Rejected | 88 |
| Auto-Match Rate | 9.0% |
| **Accuracy** | **99.0%** |
| **Precision** | **100.0%** |
| **Recall** | **90.0%** |

### What these numbers mean in plain language

**99% Accuracy** — 99 out of 100 product pairs were classified correctly. One true match was routed to human review instead of being auto-matched.

**100% Precision** — Every record the system auto-matched was a genuine match. Zero false positives. The system never said two products were the same when they were not.

**90% Recall** — The system found 9 out of 10 true matches automatically. The 10th was caught by the human review queue rather than being missed entirely.

**The 3 Human Review records** — These demonstrate the workflow doing exactly what it is designed to do: separating uncertain decisions from confident ones and making the uncertainty explicit rather than hiding it inside an automatic result.

---

## Root Cause Analysis — The One Missed Match

The evaluation identified one false negative. The matching process routed a genuine product pair to Human Review instead of Auto Match.

**Affected pair:**

| Field | Retailer A | Retailer B |
|---|---|---|
| Product Name | Coca Cola Classic 1L | Coca-Cola Classic 1000 ml |
| Brand | `coca cola` | `coca-cola` |
| Category | Beverages | Beverages |
| Size | 1000 ml | 1000 ml |

**What matched correctly:**
- Category — full score
- Size — full score (after unit normalisation)
- Product name similarity — high score

**What failed:**
- Brand comparison — zero score because `coca cola` ≠ `coca-cola`

**Root cause:** The brand field was compared after basic text cleaning but before hyphen removal. The hyphen in `coca-cola` caused an exact-match failure, reducing the total score below the 80-point auto-match threshold.

**Corrective action:** Normalize brand values before comparison — remove hyphens, extra spaces, and punctuation as part of the standardization step. This would have resolved the mismatch before scoring began.

**Operational impact of catching this:** The record was not lost. It appeared in the Human Review queue and would have been correctly matched by an analyst. The RCA shows where the automated logic can be strengthened to reduce manual queue volume.

---

## SQL Analysis

Matching results were loaded into MySQL for operational analysis. SQL was used to answer the questions a data operations team would ask about system performance:

- How many records were auto-matched, reviewed, and rejected?
- What is the precision and recall across decision categories?
- Which records are false negatives and why?
- What is the average match score by decision band?
- Which score ranges produce the most exceptions?

Example business question addressed in SQL:

> *Which product matches were missed by the automated matching process, and what was the root cause?*

This moves the analysis beyond a single accuracy metric and into identifying specific, fixable data-quality issues.

---

## Power BI Dashboard

The Power BI dashboard provides an operational monitoring view for a data operations stakeholder.

### KPIs tracked

- Total Product Pairs Processed
- Auto-Match Rate
- Human Review Queue Size
- Rejected Records
- Accuracy / Precision / Recall
- Average Match Score

### Dashboard views

- **Matching Decision Distribution** — How records split across Auto Match, Human Review, and Reject
- **Matching Quality Breakdown** — True positives, false positives, false negatives, true negatives
- **Match Confidence Distribution** — Score distribution across all 100 pairs
- **Operational Insights** — Exception patterns and RCA findings

The dashboard allows any stakeholder to answer in under 30 seconds: how many records were processed, how many can be automated, how many need review, and where the matching process is failing.

---

## Tools and Libraries

| Tool | Used For |
|---|---|
| Python (pandas, NumPy) | Dataset creation, data cleaning, standardization |
| RapidFuzz | Fuzzy string matching for product name similarity |
| scikit-learn | Evaluation metrics — accuracy, precision, recall |
| matplotlib | Exploratory visualisation |
| SQL / MySQL | Operational analysis, KPI calculation, RCA queries |
| Power BI | Executive dashboard, KPI monitoring |
| Power Query | Dataset preparation, score band classification |
| DAX | Calculated KPI measures in Power BI |
| GitHub | Version control, documentation, portfolio |

---

## Repository Structure

```
retail-product-matching/
├── README.md
├── data/
│   ├── retailer_a.csv
│   ├── retailer_b.csv
│   └── ground_truth.csv
├── python/
│   ├── 01_data_creation.py
│   ├── 02_cleaning_standardization.py
│   ├── 03_matching_scoring.py
│   └── 04_evaluation.py
├── sql/
│   ├── matching_decision_summary.sql
│   ├── precision_recall_analysis.sql
│   ├── false_negative_identification.sql
│   └── rca_classification.sql
└── powerbi/
    └── product_matching_dashboard.pbix
```

---

## Business Recommendations

Based on the analysis findings:

**1. Strengthen attribute normalisation before matching**
Brand names, units, punctuation, and spacing should all be standardised before any comparison is performed. The false negative in this project was caused by a normalisation gap, not a matching logic failure.

**2. Always maintain a human review queue**
Do not force uncertain records into a binary accept/reject decision. A review queue makes uncertainty visible, measurable, and improvable.

**3. Monitor precision and recall separately**
A high accuracy score can hide a problematic precision-recall balance. In data operations, false positives (wrong matches accepted) are usually more damaging than false negatives (real matches missed) — the human review queue catches the latter.

**4. Use RCA for recurring exceptions**
When the same type of formatting issue causes repeated failures, that is a signal to update the standardization step — not to increase the match threshold.

**5. Track matching quality over time**
As new product data arrives, monitoring the auto-match rate, human review queue size, and false negative rate over time shows whether data quality is improving or degrading.

---

## What This Project Demonstrates

- End-to-end data pipeline thinking — from raw inconsistent data to a monitored operational workflow
- Explainable scoring design — every match decision can be traced back to individual attribute scores
- Honest handling of uncertainty — uncertain records are surfaced, not hidden
- SQL for operational analytics — moving beyond model metrics into actionable business questions
- Root cause analysis methodology — identifying not just that something failed but why and how to fix it
- Dashboard design for a non-technical stakeholder — KPIs and views that answer real operational questions

---

*Dataset is synthetic. Metrics reflect evaluation results on this specific dataset.*
