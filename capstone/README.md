# Home Credit Default Risk Prediction

## Overview

This project develops a machine learning model to predict loan default risk using the Home Credit dataset. The workflow includes exploratory data analysis, feature engineering, customer segmentation, model training, explainability, monitoring, and deployment through a Scikit-learn Pipeline.

## Project Structure

```text
notebooks/
├── 01_eda.ipynb
├── 02_data_preparation.ipynb
├── 03_feature_engineering.ipynb
├── 04_modeling.ipynb
├── 05_explainability.ipynb
└── 06_scikit_learn_pipelines.ipynb

models/
├── best_model.pkl
└── credit_scoring_pipeline.pkl

reports/
└── model_documentation.md
```

## Best Model

The final selected model is a tuned Gradient Boosting Classifier.

### Hyperparameters

```python
GradientBoostingClassifier(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    random_state=42
)
```

### Evaluation Metrics

- AUROC: 0.7633
- Gini: 0.5265
- KS: 0.3893

## Technologies

- Python
- Pandas
- NumPy
- Scikit-learn
- SHAP
- Matplotlib
- Git

## Run Order

1. 01_eda.ipynb
2. 02_data_preparation.ipynb
3. 03_feature_engineering.ipynb
4. 04_modeling.ipynb
5. 05_explainability.ipynb
6. 06_scikit_learn_pipelines.ipynb

## Example Usage

Load the saved pipeline:

```python
import joblib
import pandas as pd

pipeline = joblib.load("../models/credit_scoring_pipeline.pkl")
sample = pd.read_csv("../data/application_train.csv").drop(columns="TARGET").head(5)

predictions = pipeline.predict(sample)
probabilities = pipeline.predict_proba(sample)[:, 1]

print(predictions)
print(probabilities)
```