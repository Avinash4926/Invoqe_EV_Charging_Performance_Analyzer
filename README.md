
# ⚡ EVCharge Analytics — Electric Vehicle Charging EDA

### Invoqe Data Analytics Internship | Task 2

EVCharge Analytics is an exploratory data analysis project focused on electric vehicle charging transactions. The project uses charging-session data to investigate charging activity, session duration, demand patterns, charger usage, and location-based trends.

The project demonstrates practical skills in **data cleaning, data preprocessing, exploratory data analysis, statistical analysis, and data visualization** using Python.

---

## 🎯 Project Objectives

- Understand the structure and quality of EV charging transaction data.
- Identify and handle missing values, duplicate records, and invalid entries.
- Analyze charging-session duration and demand.
- Explore charging activity by day, hour, location, and charger type.
- Investigate relationships between numerical variables.
- Create visualizations to communicate meaningful patterns.
- Summarize findings from the analyzed dataset.

---

## 📊 Dataset

**Dataset:** EV Charging Transactions  
**Source:** [IEEE PES Data Sharing — EV Charging Transactions](https://ieee-pes-data-sharing.org/datasets/detail/c903145b-3ba7-4fd3-ac1b-7727abf79e73)

The dataset contains EV charging-session records with fields such as:

| Column | Description |
|---|---|
| `UserID` | Identifier for the user |
| `ChargerID` | Identifier for the charger |
| `ChargerCompany` | Charger company identifier |
| `Location` | Charging location category |
| `ChargerType` | Charger type identifier |
| `StartDay` | Charging start date |
| `StartTime` | Charging start time |
| `EndDay` | Charging end date |
| `EndTime` | Charging end time |
| `StartDatetime` | Combined charging start timestamp |
| `EndDatetime` | Combined charging end timestamp |
| `Duration` | Charging session duration in minutes |
| `Demand` | Recorded charging demand value |

> Refer to the original dataset documentation for the meaning and units of encoded fields such as `ChargerType` and `Demand`.

---

## 🛠️ Technologies Used

- **Python** — Programming language
- **Pandas** — Data manipulation and cleaning
- **NumPy** — Numerical operations
- **Matplotlib** — Data visualization
- **Seaborn** — Statistical visualization
- **Jupyter Notebook** — Interactive analysis and documentation

---

## 📁 Project Structure

```text
Invoqe_EVCharge_Analytics/
│
├── EVCharge_EDA.ipynb
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── ev_charging_raw.csv
│   └── ev_charging_cleaned.csv
│
└── visualizations/
    ├── charging_sessions_by_day.png
    ├── charging_sessions_by_hour.png
    ├── energy_distribution.png
    ├── charging_duration_distribution.png
    ├── sessions_by_location.png
    ├── demand_by_charger_type.png
    └── correlation_heatmap.png
```

---

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/Avinash4926/Invoqe_EVCharge_Analytics.git
cd Invoqe_EVCharge_Analytics
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Launch Jupyter Notebook

```bash
python -m notebook
```

Open `EVCharge_EDA.ipynb` and execute the cells in order.

---

## 🔄 Project Workflow

1. **Data Collection**  
   Download the EV charging transaction dataset from the provided source.

2. **Data Loading**  
   Load the CSV file into a Pandas DataFrame.

3. **Data Inspection**  
   Examine column names, data types, dataset dimensions, and descriptive statistics.

4. **Data Cleaning**  
   Check missing values, remove duplicate records, convert data types, and filter invalid records.

5. **Feature Engineering**  
   Extract time-based features such as start hour, day of week, month, and time period.

6. **Exploratory Data Analysis**  
   Analyze charging sessions, demand, duration, location, charger type, and numerical relationships.

7. **Data Visualization**  
   Generate charts to communicate the observed patterns.

8. **Insights and Reporting**  
   Summarize the findings based on the actual analysis results.

---

## 📈 Analysis and Visualizations

The notebook explores the following questions:

- How does charging activity vary by day of the week?
- Which hours have the most charging sessions?
- How is charging demand distributed?
- What is the distribution of charging-session duration?
- Which locations have the most recorded sessions?
- How does demand vary across charger types?
- What relationships exist between duration, demand, and time-based variables?

### Generated Visualizations

- Charging Sessions by Day of Week
- Charging Sessions by Start Hour
- Distribution of EV Charging Demand
- Distribution of Charging Session Duration
- Top Locations by Charging Sessions
- Demand Distribution by Charger Type
- Correlation Heatmap

---

## 🧹 Data Cleaning

The notebook performs the following data preparation steps:

- Checks missing values and their percentages.
- Identifies duplicate records.
- Converts timestamp columns to datetime format.
- Converts numerical columns to suitable numeric types.
- Removes exact duplicate records.
- Removes records with missing essential values.
- Filters invalid duration and demand values.
- Creates time-based features for further analysis.
- Saves the cleaned dataset as a CSV file.

---

## 📂 Project Outputs

| Output | Description |
|---|---|
| `EVCharge_EDA.ipynb` | Complete analysis notebook |
| `ev_charging_raw.csv` | Original downloaded dataset |
| `ev_charging_cleaned.csv` | Cleaned dataset |
| `visualizations/` | Generated charts |
| `requirements.txt` | Python dependencies |
| `README.md` | Project documentation |

---

## 🔍 Key Findings

Add your verified findings after running the notebook.

Examples of findings to report:

- Total number of charging sessions analyzed
- Number of unique users, chargers, and locations
- Average and median session duration
- Average and median demand
- Most active day of the week
- Most active charging hour
- Location with the highest session count
- Observed relationships between duration and demand

> **Important:** Report only the numerical results and patterns calculated from your dataset.

---

## 📌 Skills Demonstrated

- Data loading and inspection
- Data cleaning and validation
- Datetime preprocessing
- Feature engineering
- Exploratory data analysis
- Statistical summaries
- Data visualization
- Jupyter Notebook documentation
- Git and GitHub version control

---

## ⚠️ Disclaimer

This project is developed for educational and internship purposes as part of the **Invoqe Data Analytics Internship — Task 2**. Dataset ownership, licensing, and usage conditions remain with the original dataset provider.

---

## 👨‍💻 Author

**Avinash**  
B.Tech — Artificial Intelligence and Machine Learning

Developed as part of the **Invoqe Data Analytics Internship**.

---

## ⭐ Acknowledgment

Thanks to **Invoqe** for providing the opportunity to apply practical data analytics skills through an internship project.
