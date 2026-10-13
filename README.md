# Statistical Explorer

A desktop app for exploring a student-grades dataset. It shows the data in a table, draws interactive charts, and calculates core descriptive statistics, each with its formula and a chart.

Built with Python, Tkinter, pandas, matplotlib and seaborn.

## Features

**Data**
- Data Table: browse the dataset (the first 200 rows are shown for speed).

**Graphs** (each has dropdown controls, a Reset button, and Save As PNG)
- Bar Plot: counts per category, or the average of a numeric column per group
- Scatter Plot: any two numeric columns, optionally colored by a category
- Histogram: any numeric column, adjustable bins, with a density curve
- Box Plot: any numeric column, optionally grouped by a category
- Pie Chart: share of each value in a chosen column

**Analysis** (each shows a results table and a chart)
- Range and Mid Range
- Mean
- Median
- Mode
- Variance and Standard Deviation

## Dataset

The app loads `mid term grades.csv` automatically on startup. It must be in the same folder as `app.py`. It has 500 student records with these columns:

| Column | Description |
|---|---|
| student_id | Student identifier |
| gender | Male / Female |
| age | Age in years |
| study_hours_per_week | Weekly study hours |
| attendance_rate | Attendance percentage |
| parent_education | Highest parent education level |
| internet_access | Yes / No |
| extracurricular | Yes / No |
| previous_score | Previous exam score |
| final_score | Final exam score |
| passed | Yes / No |

## Requirements

- Python 3.8 or newer
- Tkinter (included with the Windows and macOS installers from python.org; on Linux install it with `sudo apt install python3-tk`)
- pandas, numpy, matplotlib, seaborn (listed in `requirements.txt`)

## Installation

```bash
pip install -r requirements.txt
```

## Usage

Run the app from inside the project folder, so it can find the dataset:

```bash
python app.py
```

Use the sidebar on the left to switch between the table, graphs and analysis views.

## Generate the PDF report

```bash
python generate_report.py
```

This reads `mid term grades.csv` and writes `College_Analytics_Report.pdf`, a 7-page report with charts and short explanations.

## Project structure

```
app.py                  Main window, sidebar and view switching
generate_report.py      Builds the PDF report
parser.py               Markdown table parser (not used by the app)
requirements.txt        Python dependencies
mid term grades.csv     Dataset
views/
    data_table.py       Data table view
    graphs/             Bar, scatter, histogram, box and pie charts
    analysis/           Range, mean, median, mode, variance and std dev
```
