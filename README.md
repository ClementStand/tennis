Hello world

# Data Preprocessing Steps Explained

This document explains the steps we took to prepare the tennis dataset for machine learning, following **best practices** to ensure a robust and reliable model.

## 1. Defining the Goal (Target Variable)
We want to predict **who wins** the match.
- We created a new target variable called `y`.
- **Logic**:
    - If **Player 1** is the Winner, `y = 1`.
    - If **Player 2** is the Winner, `y = 0`.
- This turns the problem into a "Binary Classification" task (predicting 1 or 0).

## 2. Choosing the Right Information (Feature Selection)
We carefully selected which columns (features) to use for prediction (`X`).
- **Kept**:
    - **Numerical**: `Rank`, `Points`, `Odds`, `Best of` (sets). These directly relate to player strength.
    - **Categorical**: `Series`, `Court`, `Surface`, `Round`. These describe the match conditions.
- **Dropped**:
    - `Winner` & `Score`: These are the *outcome*. Using them would be "cheating" (Data Leakage).
    - `Tournament`, `Player_1`, `Player_2`: These have too many unique values (high cardinality). Including them without special techniques would create thousands of unnecessary columns and confuse the model.

## 3. The Golden Rule: Split BEFORE You Touch (Train/Test Split)
**Crucial Step**: Before we did any cleaning or calculations, we split the data into two parts:
1.  **Training Set (80%)**: The data the model learns from.
2.  **Test Set (20%)**: The "exam" questions the model has never seen.

**Why?**
If we calculated averages (like median for missing values) using the *entire* dataset, information from the Test Set would "leak" into the Training Set. This is called **Data Leakage**, and it makes the model look better than it actually is. By splitting first, we ensure the Test Set remains completely pure and unseen.

## 4. Cleaning the Data (Imputation)
Real-world data often has missing values (marked as `-1`).
- **The Fix**: We used a `SimpleImputer`.
- **Important**: We calculated the median *only* from the **Training Set**. We then used that same number to fill gaps in both the Training and Test sets.

## 5. Leveling the Playing Field (Scaling)
The numerical data has very different ranges (Ranks 1-100 vs Points 0-16,000).
- **The Fix**: We used a `StandardScaler`.
- **Important**: We learned the mean and standard deviation *only* from the **Training Set**. We then applied this scaling to both sets. This simulates the real world where we don't know the distribution of future data.

## 6. Translating Words to Numbers (One-Hot Encoding)
Computers do not understand text like "Hard Court".
- **The Fix**: We used `OneHotEncoder`.
- It creates a new binary (0 or 1) column for every category (e.g., `Surface_Clay`, `Surface_Hard`).

## 7. The Assembly Line (Pipeline)
We wrapped all these steps into a **Pipeline**.
- **Flow**: `Raw Data` -> `Imputer` -> `Scaler` -> `Encoder` -> `Clean Data`.
- **Benefit**: The pipeline handles the complexity of "Fit on Train, Transform on Test" automatically, preventing mistakes and leakage.
