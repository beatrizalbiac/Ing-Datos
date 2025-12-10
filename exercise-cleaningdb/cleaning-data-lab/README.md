# **Exercise 3 - Data Cleaning Exercise**
*By Beatriz Albiac*


### 1. Check the file data to fast check. Read it with Pandas
- **How many rows do we have?**
  189 rows
- **Is there any sensible information?**
  Yes, the name, email, phone number and age
- **What kind of problems can we have regarding the nature of this data?**
  Inconsistent formats, invalid values, missing data etc.

### 2. Clean it
**Define the rules we need to clean the data**
- CustomerName: Standarize the font (capitals and lowercase letters) -> So the first letter of the name and lastname is capitalized, and the rest is in lowercase
- Email: Standarize the font -> so everything's on lowecase
- Phone: Erase everything that isn't a number
- Country: Standarize it so the same country is refered to with the same format and wording
- OrderDate: Standarize it to DD/MM/YYYY so every date has the same format
- Quantity: Has to be greater than 0
- Price: Has to be greater than 0
- CustomerAge: Has to be a number between 1 and 100
- OrderStatus: It's already clean and standarized)

*NULLS:*
- Drop rows with null Quantity or Price
- Drop rows with BOTH null Email and Phone
