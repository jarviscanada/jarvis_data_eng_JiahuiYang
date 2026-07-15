# Model Validation Summary

## Model Purpose

The model estimates the probability that a credit applicant will default on a loan. It is intended to support credit-risk assessment and help identify applications that may require additional review.

## Methodology

The best model uses a Gradient Boosting classifier with 300 estimators, a learning rate of 0.05, a maximum tree depth of 4, and a fixed random state of 42.

The input data comes from the Home Credit application dataset. Numeric variables are filled using median imputation and standardized. Categorical variables are filled using the most frequent category and one-hot encoded.

Key variables include applicant income, credit amount, age, employment history, external credit scores, and engineered ratios such as credit-to-income.

## Performance

Best Model performance metrics:

- AUROC: 0.7633
- Gini: 0.5265
- KS: 0.3893
- Cross-validation mean AUROC: 0.7635
- Cross-validation AUROC standard deviation: 0.0047
- Logistic Regression baseline AUROC: 0.7539

The best model performed better than the Logistic Regression baseline and showed stable performance across validation folds.

## Explainability

SHAP analysis was used to explain global and individual predictions. The top features included:

1. EXT_SOURCE_MEAN
2. CREDIT_TERM
3. CODE_GENDER_M_True
4. AMT_GOODS_PRICE
5. NAME_EDUCATION_TYPE
6. DAYS_EMPLOYED
7. EXT_SOURCE_1_MISSING
8. AMT_ANNUITY
9. NAME_FAMILY_STATUS_Married_True
10. IEXT_SOURCE_3

## Limitations

The model was trained on historical Home Credit data and may not fully represent current economic conditions.

Performance may decrease during severe recessions or when borrower behavior changes.

Some variables contain missing or anomalous values.

The dataset may not represent all demographic or applicant groups equally.

Potential fairness and bias risks require separate testing before deployment.

## Monitoring Plan

The following metrics should be tracked:

- AUROC
- Gini
- KS
- AUPRC
- Default rate
- Approval rate
- Missing-value rates
- Feature distributions
- PSI for key features
- Prediction score distribution

PSI thresholds:

- PSI below 0.10: stable
- PSI from 0.10 to 0.25: moderate shift and closer monitoring
- PSI above 0.25: significant shift requiring model review

A PSI above 0.25 in important variables, or a meaningful decline in AUROC, should trigger investigation and possible retraining.

## Reproducibility

- Random state: 42
- Data SHA-256: ad552d8b86289bb9522767b76f3b7ad5f9c8adf05ed3a661730389c61fec5871
- Model SHA-256: 8774a828cf82aac48c3bb155983087b5f285a3642446ee70d0a82bdf904b989a
- Model file: `models/credit_scoring_pipeline.pkl`