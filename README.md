### A PCGC LAB QC script

#### General idea
- For each loinc-code
    - find the unit (R) with most observation count
    - generate a boxplot for R
    - remove the unit if its observation count is less than 1% of R's count
    - remove the unit if its median is not within R's IQR or R's median is not within the IQR of that unit.

#### Requirement
- Pandas
