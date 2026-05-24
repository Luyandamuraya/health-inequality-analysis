 # Health Inequality Analysis in England

## 📌 Project Overview

This project explores health inequality across local authorities in England using open-source public datasets.  

Health inequality refers to the avoidable and unfair differences in health outcomes, access to healthcare, and wider determinants of health between different groups or areas.

The aim of this project was to investigate how demographic, socioeconomic, clinical, environmental, and healthcare access factors vary across different local authorities, and how these differences may contribute to unequal health outcomes.

This project brought together multiple datasets across themes including:

- Demographics
- Socioeconomic indicators
- Health outcomes
- Primary care access
- Clinical prevalence indicators
- Environmental indicators
- Vaccination coverage

The project was also an opportunity to work with real-world public health data, geographical lookups, data cleaning, weighted calculations, and exploratory analysis.

---

## 🎯 Project Objectives

The main objectives of this project was to:

- Explore how health outcomes differ across local authorities 
- Compare health inequality indicators across demographic and socioeconomic groups
- Understand the relationship between deprivation, access to healthcare, and health outcomes
- Practise combining multiple public datasets using geographical codes

---

## 🧠 Why This Project Matters

Health inequality is shaped by more than healthcare alone. Factors such as income, employment, education, deprivation, transport access, ethnicity, housing, and environment can all influence health outcomes.

Having previously worked in the pharmaceutical and healthcare analytics space, I was interested in exploring how publicly available data can be used to better understand differences in health outcomes across England.

This project helped me think about how data can be used to identify patterns, highlight disparities, and support more informed decision-making in healthcare and public policy.

---

## 📊 Data Sources

All datasets used in this project are open-source/publicly available.

The project includes data relating to:

- Local authority demographics
- Life expectancy
- Deprivation indices
- GP access and travel times
- Hospital access and travel times
- Disease prevalence indicators
- Vaccination coverage
- Environmental indicators
- Population and ethnicity breakdowns

Geographical lookup files were also used to join datasets across different UK geographical structures, such as local authorities, Integrated Care Boards, and other regional classifications.

---

## 🛠️ Tools and Technologies

- Python
- Pandas
- Jupyter Notebook
- Excel
- GitHub
- Public health datasets
- UK geographical lookup files

---

## 🔍 Key Skills Demonstrated

This project allowed me to practise and demonstrate:

- Data cleaning and preprocessing
- Working with multiple datasets
- Joining data using geographical codes
- Understanding UK geographical structures
- Handling inconsistent data formats
- Exploratory data analysis
- Weighted calculations
- Public health data interpretation

---

## 🌟 Key Learning Highlights

Some of the main things I learned during this project include:

### Understanding geographical structures

A major part of the project involved understanding how different UK geographical structures relate to each other. For example, some datasets were available at local authority level, while others used Integrated Care Board or regional boundaries.

This meant I had to use lookup tables to correctly join datasets and ensure the analysis was geographically consistent.

### Working with real-world health data

This project gave me experience working with different types of health-related data, including GP-collected data, clinical prevalence data, vaccination coverage, and access indicators.

It also helped me understand that public datasets vary significantly in quality, granularity, and ease of use.

### Refining the project scope

One of the biggest learning points was seeing the difference between the data I initially wanted to use and the data that was actually available at the correct level of detail.

This helped me think more carefully about feasibility, data availability, and project design.

### Using weighted calculations

I also explored why simple averages are not always appropriate when comparing health indicators.

For example, when calculating life expectancy, an unweighted average assumes male and female populations are equal. However, female populations are often slightly higher overall, and in older age groups, females can significantly outnumber males.

Using weighted calculations helped create more accurate comparisons across local authorities.

---

## 📈 Methodology

The project followed these broad steps:

1. Identified relevant public datasets relating to health inequality
2. Reviewed data availability and geographical granularity
3. Cleaned and standardised datasets
4. Used geographical codes and lookup files to join datasets
5. Created derived indicators where needed
6. Applied weighted calculations for selected measures
7. Compared indicators across local authorities
8. Explored patterns between deprivation, access, demographics, and health outcomes

---

## 📁 Repository Structure

```text
health-inequality-analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── health_inequality_analysis.ipynb
│
├── outputs/
│   ├── charts/
│   └── tables/
│
├── README.md
└── requirements.txt
