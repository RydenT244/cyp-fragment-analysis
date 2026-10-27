# CYP-Relevant Chemical Fragment Feature Analysis

## 1. Research Objective

This project investigates whether explicitly encoding CYP-relevant chemical groups improves predictions of cytochrome P450 (CYP) inhibition beyond standard molecular fingerprints. It also identifies which fragment indicators provide the most additional predictive value for **CYP1A2, CYP2C9, CYP2D6, and CYP3A4**.

## 2. Data and Feature Preparation

The original fragment-map dataset contains **39,505 molecules** represented by SMILES strings and molecular fragment memberships derived from SMARTS patterns. Twelve CYP-relevant groups were encoded as binary indicators (present = 1; absent = 0). These features were matched to OpenADMET direct-inhibition pIC50 measurements.

**Available measurements after matching**

| CYP isoform | Molecules with pIC50 measurements |
|:------------|---------------------------------:|
| CYP1A2      | 1,412 |
| CYP2C9      | 1,285 |
| CYP2D6      | 1,490 |
| CYP3A4      | 2,334 |

The available labeled compounds differ across isoforms. Missing inhibition measurements were not treated as zero.

## 3. Exploratory Feature Analysis

### Fragment prevalence and co-occurrence

The most prevalent groups across the full molecular collection were aryl halide (30.80%), pyridine (28.46%), and basic aliphatic amine (23.45%). Other examples include imidazole (11.79%), 1,2,4-triazole (4.30%), and steroid core (1.38%).

Pairwise Jaccard similarities were generally low, indicating limited overlap between most fragment memberships. Neither prevalence nor co-occurrence alone establishes predictive value.

### Scored versus blind molecules

The fragment map contains **4,901 scored molecules** and **748 blind molecules**. Some fragments have noticeably different prevalence between these groups.

| Chemical group         | Blind − scored prevalence (percentage points) |
|:-----------------------|----------------------------------------------:|
| Aryl halide            | +8.84 |
| Imidazole              | +8.30 |
| Pyridine               | +5.27 |
| 1,2,4-Triazole         | −4.17 |
| Basic aliphatic amine  | −7.10 |

These differences suggest some shift in chemical composition between scored and blind collections, potentially relevant to model generalization. They do not show which fragments improve inhibition prediction.

## 4. Fragment Associations with Inhibition

Mean pIC50 measurements were compared for molecules **with** and **without** each fragment. The difference was defined as:

`mean pIC50 (with fragment) − mean pIC50 (without fragment)`

Notable descriptive results included:

- **Carboxylic acid:** Lower mean pIC50 across all four isoforms; the largest observed difference was for CYP3A4 (−1.669).
- **Basic aliphatic amine:** Higher mean pIC50 for CYP2D6 (+0.551), but lower means for CYP1A2, CYP2C9, and CYP3A4.
- **Imidazole:** Positive mean differences for several isoforms.
- **Aryl halide:** Positive mean differences for CYP1A2, CYP2C9, and CYP3A4.

These are associations, not causal effects or direct estimates of predictive contribution. Some fragment–isoform combinations had few labeled observations.

## 5. Predictive Feature Evaluation

### Models and experimental design

- **Ridge regression:** Regularization tuned using training-only cross-validation.
- **Random Forest regression:** Fixed hyperparameter configuration in the reported comparison.
- **Baseline features:** 2,048-bit Morgan fingerprints.
- **Augmented features:** Fingerprints plus 12 binary CYP fragment indicators.
- **Metrics:** RMSE (lower is better) and R² (higher is better).
- **Validation:** Random splits and repeated scaffold-grouped train/test splits; scaffold groups were kept separate within each split.

### Ridge: repeated scaffold-split results

Mean held-out RMSE across **20 scaffold-based splits**:

| CYP isoform | Fingerprints only | Fingerprints + 12 fragments | RMSE reduction |
|:------------|------------------:|----------------------------:|---------------:|
| CYP1A2      | 0.9116 | 0.9081 | 0.0035 |
| CYP2C9      | 0.6990 | 0.6894 | 0.0096 |
| CYP2D6      | 0.8640 | 0.8504 | 0.0136 |
| **CYP3A4**  | **0.8457** | **0.8136** | **0.0321** |

Adding the twelve indicators reduced mean RMSE for every isoform in this Ridge experiment; CYP3A4 showed the largest average reduction.

## 6. Individual Fragment Ablation

For each candidate feature, a model was retrained **without that fragment**. The contribution was measured as:

`RMSE without fragment − RMSE with all fragments`

**Positive values** mean the fragment helped prediction under the tested model and splits.

Leading fragment–isoform combinations across **20 scaffold-based splits**:

| CYP isoform | Fragment | Ridge RMSE increase | Random Forest RMSE increase | RF positive splits |
|:------------|:---------|--------------------:|----------------------------:|-------------------:|
| **CYP3A4** | **Carboxylic acid** | **+0.0248** | **+0.0255** | **20/20** |
| CYP2D6 | Basic aliphatic amine | +0.0142 | +0.0179 | 19/20 |
| CYP2C9 | Carboxylic acid | +0.0049 | +0.0115 | 18/20 |

The same leading pairs had positive contributions in both Ridge and Random Forest. Most other individual fragment indicators contributed relatively little beyond fingerprints in these experiments.

Imidazole, for example, showed inhibition associations but little consistent incremental contribution in ablation. Its chemical relevance does not guarantee additional predictive value when fingerprints already encode related substructure information.

## 7. Reduced Feature Set Evaluation

A final Random Forest experiment compared fingerprints alone, fingerprints plus a small isoform-specific set of fragments, and fingerprints plus all twelve indicators, across **20 scaffold-based splits**.

**Reduced sets:**

- CYP1A2: carboxylic acid + basic aliphatic amine
- CYP2C9: carboxylic acid
- CYP2D6: basic aliphatic amine
- CYP3A4: carboxylic acid

**Mean scaffold-test RMSE (lower is better)**

| CYP isoform | Fingerprints only | Reduced set | All 12 fragments |
|:------------|------------------:|------------:|-----------------:|
| CYP1A2      | 0.9305 | 0.9255 | **0.9242** |
| CYP2C9      | 0.7316 | 0.7208 | **0.7143** |
| CYP2D6      | 0.8673 | 0.8495 | **0.8494** |
| CYP3A4      | 0.9240 | 0.8980 | **0.8916** |

The reduced feature sets retained approximately **79% (CYP1A2), 62% (CYP2C9), 99% (CYP2D6), and 81% (CYP3A4)** of the mean RMSE improvement achieved with all 12 fragment indicators (rounded values). These percentages compare improvements over the fingerprint-only baseline, not absolute prediction accuracy.

For **CYP2D6**, adding only basic aliphatic amine performed nearly identically to including all twelve fragment indicators. For **CYP3A4**, carboxylic acid accounted for most of the improvement, while the full set still performed better on average.

## 8. Limitations

- **Missing labels:** Each isoform had a different labeled subset.
- **Potential redundancy:** Morgan fingerprints already encode substructures associated with explicit fragment indicators.
- **Model dependence:** Ridge was tuned while the reported Random Forest used fixed hyperparameters; conclusions may change with other models or settings.
- **Repeated-split dependence:** Repeated scaffold splits reuse molecules and are not independent external validations.
- **Exploratory feature selection:** The reduced sets were chosen based on earlier results from this molecular dataset, so their performance is not an unbiased independent test of the selection process.
- **Assay details:** Numeric pIC50 checks were conducted, but censoring, assay uncertainty, and measurement limits were not fully evaluated.

## 9. Conclusion

Explicit CYP-relevant chemical-group indicators improved mean inhibition prediction performance beyond Morgan fingerprints under the evaluated Ridge and Random Forest configurations.

- **CYP3A4:** Carboxylic acid was the strongest individual additional feature, with consistent positive contributions in repeated scaffold-based ablation under both models.
- **CYP2D6:** Basic aliphatic amine was particularly useful; the reduced model containing this single additional fragment performed almost identically to the full twelve-fragment model.
- **CYP2C9:** Carboxylic acid contributed, although other fragments collectively offered further improvement.
- **CYP1A2:** Fragment indicators produced relatively small performance gains overall.

**Bottom line:** A compact set of chemically interpretable fragments captured much of the benefit of explicitly encoding CYP-relevant groups. The full 12-fragment set achieved the lowest mean Random Forest RMSE for every isoform in the reported reduced-feature comparison. These conclusions are exploratory and specific to the data and model configurations evaluated.
