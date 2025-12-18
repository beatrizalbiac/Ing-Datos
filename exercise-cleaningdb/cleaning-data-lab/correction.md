# Exercise Correction: Data Cleaning Lab
**Student:** Beatriz Albiac  
**Exercise:** E-commerce Customer Orders Data Cleaning  
**Date:** December 12, 2025

---

## Overall Assessment

**Grade: 8.2/10** 

This is a well-structured data cleaning exercise with clear documentation, thoughtful approach to data quality issues, and comprehensive validation. The code demonstrates good understanding of pandas operations and data quality dimensions.

---

### 1. **Excellent Code Structure and Documentation** 
- Clear separation of steps with headers.
- Comprehensive comments explaining the logic.
- Well-documented cleaning rules.
- Good use of print statements for tracking progress.

### 2. **Data Quality Framework** 
- Implemented proper data quality dimensions (Accuracy, Completeness, Consistency, Validity, Uniqueness, Timeliness).
- Good before/after comparison with validation function.
- Appropriate use of `.copy()` to preserve raw data for comparison.

### 3. **Error Handling** 
- Good use of `on_bad_lines='warn'` for CSV parsing.
- Try-except block for data retrieval.
- Proper use of `errors="coerce"` in type conversions.

---

## Issues Found

### 1. **CRITICAL: Syntax Error** (Line 166) (-1 point)
**Severity:** Critical (prevents code execution)

```python
# WRONG (line 166)
age = pd.to_numeric(df["CustomerAge"], errors="coerce")s
                                                       ^ Extra 's'

# CORRECT
age = pd.to_numeric(df["CustomerAge"], errors="coerce")
```

**Impact:** This typo prevented the teacher requirements detection tool from parsing the file and would cause a runtime error.

---

### 2. **Code Quality Issues** (- 0.3 points)

#### a) Inconsistent Spacing (Line 33)
```python
# Current
df = pd.read_csv(io .StringIO(response.text),sep=',',on_bad_lines='warn')
                   ^ extra space

# Better
df = pd.read_csv(io.StringIO(response.text), sep=',', on_bad_lines='warn')
```

#### b) Incomplete Price Validation (Line 133)
```python
# price ¿drop nulls?
```
Price validation is mentioned in the rules but not implemented. Should add:
```python
df.loc[df["Price"] <= 0, "Price"] = np.nan
```


---

### 3. **Logic and Design Issues** (-0.5 points)

#### a) Country Validation in validation() Function
The consistency check includes lowercase versions that shouldn't exist after cleaning:
```python
consistency_mask = country.isin([
    "USA", "Canada", "UK",
    "usa", "us", "united states",  # These shouldn't exist after cleaning
    "united kingdom", "uk", "gb"    # These shouldn't exist after cleaning
])
```

**Better approach:**
```python
consistency_mask = country.isin(["USA", "Canada", "UK"])
```

#### b) Date Format Comment Inconsistency
- Comment says: "Standarize it to DD/MM/YYYY"
- Code implements: `YYYY/MM/DD` format
- The code is correct, but the comment is misleading


---

## Suggestions for Improvement

### 1. **Add Price Validation**
```python
# Add after line 133
df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
df.loc[df["Price"] <= 0, "Price"] = np.nan
df["Price"] = df["Price"].round(2)
```

### 2. **Handle Duplicates Properly**
Currently, duplicates are identified but not removed. Consider adding:
```python
# After line 70
df = df.drop_duplicates(subset=['OrderID'], keep='first')
print(f"✓ Removed {duplicates_count} duplicate OrderIDs")
```

### 3. **Improve Country Mapping with Error Handling**
```python
df["Country"] = df["Country"].map(countries)
# Add handling for unmapped countries
unmapped = df["Country"].isna().sum()
if unmapped > 0:
    print(f"[!] Warning: {unmapped} rows with unmapped countries")
```

### 4. **Add requirements.txt**
Create a proper requirements file:
```txt
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
```

### 5. **Better Output File Management**
```python
# Instead of hardcoded filename
output_file = 'cleaned_data.csv'
df.to_csv(output_file, index=False)
print(f"✓ Dataset saved to: {output_file}")
```


