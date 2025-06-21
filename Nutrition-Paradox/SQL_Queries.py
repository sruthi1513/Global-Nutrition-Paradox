#OBESITY TABLE
#---------------------
#Top 5 regions with the highest average obesity levels in the most recent year(2022)
query1 = """
SELECT Region, ROUND(AVG(Mean_Estimate),3) AS Average_Obesity 
FROM obesity
WHERE Year = 2022 AND Sex = 'Both' AND Region IS NOT NULL
GROUP BY Region
ORDER BY Average_Obesity DESC
LIMIT 5;
"""
# Top 5 countries with highest obesity estimates
query2="""
SELECT Country, MAX(Mean_Estimate) AS Max_Obesity 
FROM obesity
GROUP BY Country
ORDER BY Max_Obesity DESC
LIMIT 5;
"""
# Obesity trend in India over the years(Mean_estimate)
query3="""
SELECT Year, ROUND(AVG(Mean_Estimate),5) as Average_Mean_Estimate 
FROM obesity
WHERE Country = 'India'
GROUP BY Year
ORDER BY Year;
"""
# Average obesity by gender
query4="""
SELECT Sex, ROUND(AVG(Mean_Estimate),2) AS Average_Mean_Estimate
FROM obesity
GROUP BY Sex;
"""
# Country count by obesity level category and age group
query5="""
SELECT obesity_level, Age_Group, COUNT(Country) AS Country_Count
FROM obesity
WHERE obesity_Level IS NOT NULL
GROUP BY obesity_level, Age_Group
ORDER BY obesity_level, Age_Group;
"""
# Top 5 countries least reliable countries(with highest CI_Width) and Top 5 most consistent countries (smallest average CI_Width)
query6="""
(
SELECT Country, MIN(CI_Width) AS CI_Width, 'More Reliable/Consistent' AS Category
FROM obesity
GROUP BY Country
ORDER BY CI_Width ASC
LIMIT 5
)
UNION ALL
(
SELECT Country, MAX(CI_Width) AS CI_Width, 'Least Reliable' AS Category
FROM obesity
GROUP BY Country
ORDER BY CI_Width DESC
LIMIT 5
);
"""
# Average obesity by age group
query7="""
SELECT Age_Group, ROUND(AVG(Mean_Estimate),2) AS Average_Mean_Estimate 
FROM obesity
GROUP BY Age_Group;
"""
# Top 10 Countries with consistent low obesity (low average + low CI)over the years
query8="""
SELECT Country, ROUND(AVG(Mean_Estimate),2) AS AVG_Obesity, ROUND(AVG(CI_Width), 2) AS Avg_CI_Width
FROM obesity
GROUP BY Country
HAVING Avg_Obesity IS NOT NULL AND Avg_CI_Width IS NOT NULL
ORDER BY Avg_Obesity ASC, Avg_CI_Width ASC
LIMIT 10;
"""
# Countries where female obesity exceeds male by large margin (same year)
query9="""
SELECT 
	f.Country, 
    f.Year, 
    ROUND(AVG(f.Mean_Estimate - m.Mean_Estimate),2) AS Obesity_GAP, 
    ROUND(AVG(f.Mean_Estimate),2) AS Female_Obesity, 
    ROUND(AVG(m.Mean_Estimate),2) AS Male_Obesity
FROM obesity f
JOIN obesity m
ON f.Country = m.Country AND f.Year = m.Year AND f.Age_Group = m.Age_Group 
WHERE f.Sex = 'Female' AND m.Sex = 'Male' 
GROUP BY f.Country, f.Year
HAVING Obesity_Gap > 5
ORDER BY Obesity_Gap DESC;
"""
# Global average obesity percentage per year
query10="""
SELECT Year, ROUND(AVG(Mean_Estimate),2) AS Obesity_Percentage
FROM obesity
GROUP BY year
ORDER BY Year;
"""
#------------------------------------------------------------------------------------------------------------
# MALNUTRITION TABLE
#---------------------
# Avg. malnutrition by age group
query11="""
SELECT Age_Group, ROUND(AVG(Mean_Estimate),2) AS Avg_Malnutrition
FROM malnutrition
GROUP BY Age_Group;
"""
# Top 5 countries with highest malnutrition(mean_estimate)
query12="""
SELECT Country, ROUND(MAX(Mean_Estimate),2) AS Malnutrition
FROM malnutrition
GROUP BY Country
ORDER BY Malnutrition DESC
LIMIT 5;
"""
# Malnutrition trend in African region over the years
query13="""
SELECT Year, ROUND(AVG(Mean_Estimate),2) AS Malnutrition
FROM malnutrition
WHERE Region = 'Africa'
GROUP BY Year
ORDER BY Year;
"""
# Gender-based average malnutrition
query14="""
SELECT Sex, ROUND(AVG(Mean_Estimate),2) AS Avg_Malnutrition
FROM malnutrition
GROUP BY Sex;
"""
# Malnutrition level-wise (average CI_Width by age group)
query15="""
SELECT malnutrition_level, Age_Group, ROUND(AVG(CI_Width),2) AS Avg_CI_Width
FROM malnutrition
GROUP BY malnutrition_level, Age_Group
ORDER BY malnutrition_level;
"""
# Yearly malnutrition change in specific countries(India, Nigeria, Brazil)
query16="""
SELECT  Year, Country, ROUND(AVG(Mean_Estimate),2) AS Malnutrition
FROM malnutrition
WHERE Country IN ('India','Nigeria','Brazil')
GROUP BY Country,Year
ORDER BY Country,Year;
"""
# Regions with lowest malnutrition averages
query17="""
SELECT  Region, ROUND(MIN(Mean_Estimate),2) AS Avg_Malnutrition
FROM malnutrition
WHERE Region IS NOT NULL
GROUP BY Region
ORDER BY Avg_Malnutrition;
"""
# Countries with increasing malnutrition
query18="""
SELECT 
    Country,
    MIN(Year) AS Start_Year,
    MAX(Year) AS End_Year,
    ROUND(MIN(Avg_Malnutrition), 2) AS Start_Mean_Estimate,
    ROUND(MAX(Avg_Malnutrition), 2) AS End_Mean_Estimate,
    ROUND(MAX(Avg_Malnutrition) - MIN(Avg_Malnutrition), 2) AS Increase
FROM (
    SELECT Country, Year, AVG(Mean_Estimate) AS Avg_Malnutrition
    FROM malnutrition
    GROUP BY Country, Year
) AS yearly_avg
GROUP BY Country
HAVING Increase > 0
ORDER BY Increase DESC;
"""
# Min/Max malnutrition levels year-wise comparison
query19="""
SELECT Year, ROUND(MIN(Mean_Estimate),2) AS Min_Malnutrition,  ROUND(MAX(Mean_Estimate),2) AS Max_Malnutrition
FROM malnutrition
GROUP BY Year
ORDER BY Year;
"""
# High CI_Width flags for monitoring(CI_width > 5)
query20="""
SELECT Country, Year, Age_Group, Mean_Estimate, CI_Width
FROM malnutrition
WHERE CI_Width > 5
ORDER BY CI_Width DESC;
"""
#------------------------------------------------------------------------------------------------------------
# COMBINED
#---------------------
# Obesity vs malnutrition comparison by country(any 5 countries)
query21="""
SELECT o.Country, ROUND(AVG(o.Mean_Estimate),2) AS Avg_Obesity, ROUND(AVG(m.Mean_Estimate),2) AS Avg_Malnutrition
FROM obesity o
JOIN malnutrition m 
ON o.Country = m.Country AND o.Year = m.Year AND o.Age_Group = m.Age_Group and o.Sex = m.Sex
GROUP BY o.Country
ORDER BY m.Country;
"""
# Gender-based disparity in both obesity and malnutrition
query22="""
SELECT o.Sex, ROUND(AVG(o.Mean_Estimate),2) AS Avg_Obesity, ROUND(AVG(m.Mean_Estimate),2) AS Avg_Malnutrition, o.obesity_level, m.malnutrition_level
FROM obesity o
JOIN malnutrition m
ON o.Sex = m.Sex AND o.Country = m.Country AND o.Year = m.Year AND o.Age_Group = m.Age_Group
GROUP BY o.Sex, o.obesity_level, m.malnutrition_level;
"""
# Region-wise avg estimates side-by-side(Africa and America)
query23="""
SELECT
    o.Year,
    ROUND(AVG(CASE WHEN o.Region = 'Africa' THEN o.Mean_Estimate END), 2) AS Africa_Obesity,
    ROUND(AVG(CASE WHEN o.Region = 'Americas' THEN o.Mean_Estimate END), 2) AS Americas_Obesity,
    ROUND(AVG(CASE WHEN m.Region = 'Africa' THEN m.Mean_Estimate END), 2) AS Africa_Malnutrition,
    ROUND(AVG(CASE WHEN m.Region = 'Americas' THEN m.Mean_Estimate END), 2) AS Americas_Malnutrition
FROM obesity o
JOIN malnutrition m 
ON o.Country = m.Country AND o.Year = m.Year AND o.Sex = m.Sex AND o.Age_Group = m.Age_Group
WHERE o.Region IN ('Africa', 'Americas')
GROUP BY o.Year
ORDER BY o.Year;
"""
# Countries with obesity up & malnutrition down
query24="""
WITH obesity_avg AS (
    SELECT 
        Country, MIN(Year) AS Start_Year, MAX(Year) AS End_Year,
        ROUND(AVG(CASE WHEN Year = (SELECT MIN(Year) FROM obesity) THEN Mean_Estimate END), 2) AS Obesity_Start,
        ROUND(AVG(CASE WHEN Year = (SELECT MAX(Year) FROM obesity) THEN Mean_Estimate END), 2) AS Obesity_End
    FROM obesity
    GROUP BY Country
),
malnutrition_avg AS (
    SELECT 
        Country,
        ROUND(AVG(CASE WHEN Year = (SELECT MIN(Year) FROM malnutrition) THEN Mean_Estimate END), 2) AS Malnutrition_Start,
        ROUND(AVG(CASE WHEN Year = (SELECT MAX(Year) FROM malnutrition) THEN Mean_Estimate END), 2) AS Malnutrition_End
    FROM malnutrition
    GROUP BY Country
)
SELECT o.Country, o.Obesity_Start, o.Obesity_End, m.Malnutrition_Start, m.Malnutrition_End
FROM obesity_avg o
JOIN malnutrition_avg m ON o.Country = m.Country
WHERE o.Obesity_End > o.Obesity_Start AND m.Malnutrition_End < m.Malnutrition_Start
ORDER BY (o.Obesity_End - o.Obesity_Start) DESC;
"""
# Age-wise trend analysis
query25="""
SELECT o.Year, o.Age_Group, ROUND(AVG(o.Mean_Estimate), 2) AS Avg_Obesity, ROUND(AVG(m.Mean_Estimate), 2) AS Avg_Malnutrition
FROM obesity o
JOIN malnutrition m 
ON o.Country = m.Country AND o.Year = m.Year AND o.Sex = m.Sex AND o.Age_Group = m.Age_Group
GROUP BY o.Year, o.Age_Group
ORDER BY o.Year, o.Age_Group;
"""





