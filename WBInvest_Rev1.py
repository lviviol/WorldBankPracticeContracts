# World Bank Data includes all contract awards financed by The World Bank under Investment Project Financing (IPF) operations. 
# Source: https://financesone.worldbank.org/contract-awards-in-investment-project-financing/DS00005
# Downloaded data on 11 Jan 2025
# Simulation --> Get data --> Input into Database --> Extract needed data from DB --> Analyse

import sqlite3
import csv
import pandas as pd
import os
import matplotlib.pyplot as plt


# For code creation purpose only, delete old files created
os.remove('WBInvest.db')
os.remove('WBProjects_Analyze.csv') #Analyze selected column
os.remove('WBPractise.csv')         #Analyze selected details
os.remove('WBProjects.png')         #Plot
os.remove('WBPractice.png')         #Bar Chart



#Create & Connect to database
conn = sqlite3.connect('WBInvest.db')

#Load WBInvest.csv into WBInvest.db
def load_csv_to_db():
    df = pd.read_csv('/Users/infinity/Documents/Coder/Coding/SQL/RawData/WBInvest.csv')

    #Data Cleanup with strip() is used to remove extra white spaces
    df.columns = df.columns.str.strip()

    # convert the date column into a datetime object
    df['Contract Signing Date'] = pd.to_datetime(df['Contract Signing Date'])

    # extract the day, month, and year components
    df['Contract Sign Year'] = df['Contract Signing Date'].dt.year
    #df['Month'] = df['Contract Signing Date'].dt.month
    #df['Day'] = df['Contract Signing Date'].dt.day

    # show the modified data frame
    print(df)

    #df['Contract Signing Date'] = df['Contract Signing Year'].dt.strftime('%Y')

    #Storing dataframe/datafile into TABLE WBProjects
    #'Fail' is database name already exist
    #'Replace' & 'Append' is also available
    df.to_sql('WBProjects', conn, if_exists='fail')
    conn.commit()
load_csv_to_db()


#Check if data is imported into database
def check_csv_loading():
    conn = sqlite3.connect('WBInvest.db')
    c = conn.cursor()
    c.execute("SELECT * FROM WBProjects")
    print(c.fetchone())
    conn.commit
check_csv_loading()


#Query db to get column names of WBProjects Table
def sql_header():
    conn = sqlite3.connect('WBInvest.db')
    c = conn.cursor()
    c.execute("PRAGMA table_info(WBProjects)")
    columns = c.fetchall()
    for column in columns:
        print(column[1])
    
    conn.commit()
    conn.close()
sql_header()

#Select Specific Columns from Database
def select_columns():
    conn=sqlite3.connect('WBInvest.db')
    c=conn.cursor()
    c.execute('SELECT "Fiscal Year", "Contract Sign Year", Region, "Project Global Practice","Supplier Contract Amount (USD)" FROM WBProjects')
    rows = c.fetchall()
    #for row in rows:
            #print(row)
    conn.commit()
    conn.close()
select_columns()


#Calculate by Contract Sign Year, Region & Total Contract Amount
#Copy to new table WBProjects_Analyze
def calculate_new_table():
    conn=sqlite3.connect('WBInvest.db')
    c=conn.cursor()
    c.execute('''
            CREATE TABLE WBProjects_Analyze AS
            SELECT "Fiscal Year", "Contract Sign Year", Region, "Project Global Practice", ROUND(SUM("Supplier Contract Amount (USD)"), 0) AS Total_Value
            FROM WBProjects
            GROUP BY "Contract Sign Year", Region
    ''')
    rows = c.fetchall()   
    conn.commit()
    conn.close()
calculate_new_table()

def check_new_table():
    conn=sqlite3.connect('WBInvest.db')
    c=conn.cursor()
    c.execute("SELECT * FROM WBProjects_Analyze LIMIT 5")
    rows = c.fetchall()
    for row in rows:
        print(row)
    conn.commit()
check_new_table()


#Export SQLIte Table Data to csv
def export_analyze_csv():
    conn = sqlite3.connect('WBInvest.db')
    c=conn.cursor()
    analyze_data = "SELECT * FROM WBProjects_Analyze"
    c.execute(analyze_data)
    output = c.fetchall()
    for row in output:
        df = pd.read_sql_query(analyze_data,conn)
        df.to_csv('WBProjects_Analyze.csv', index = False)
    conn.commit()
export_analyze_csv()


#Plot Bubble Plot

#Auto Re-Size Plots to Fit Screen
import csv
import pandas as pd
from matplotlib import rcParams
from matplotlib.ticker import MultipleLocator
rcParams.update({'figure.autolayout': True})

# Load the data
df = pd.read_csv('WBProjects_Analyze.csv')

# Create a bubble plot
def Bubble_Plot():
    plt.figure(figsize=(10, 6))

    scatter = plt.scatter(
        x=df['Contract Sign Year'],
        y=df['Region'],
        s=df['Total_Value'] / 1000000,  # Adjust size for better visualization
        c=df['Region'].astype('category').cat.codes,  # Color by region
        cmap='viridis',  # Color map
        alpha=0.6,
        edgecolors='w',
        linewidth=0.5
    )

    # Add labels and title
    plt.xlabel('Contract Sign Year')
    plt.ylabel('Region', wrap=True)
    plt.title('World Bank Projects Contract Value (US$ mil)')
    plt.colorbar(scatter, label='Region Color Variance')


    # Annotate bubbles in the year 2024 with "Total Value"
    for i, row in df[df['Contract Sign Year'] == 2024].iterrows():
        plt.annotate(
            f"{row['Total_Value'] / 1000000:.0f}",
            (row['Contract Sign Year'], row['Region']),
            textcoords="offset points",
            xytext=(0,5),
            ha='center'
        )

    #handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6, num=1, func=lambda s: s * 1000000)
    #size_legend = plt.legend(handles, labels, loc="upper left", title="Total Value (in millions)")
    #size_legend = plt.legend(handles, labels, loc="upper left", title="Total Value (in millions)", bbox_to_anchor=(0, 0.8))
    #plt.gca().add_artist(size_legend)

    # Show plot
    plt.savefig('WBProjects.png')
    plt.show()
    plt.close()

Bubble_Plot()

if __name__ == '__Bubble_Plot__': #Makes sure the program runs when the file is executed
    Bubble_Plot()


import sqlite3
import csv
from collections import Counter

# Word count for Region & Practise only
def word_count2():
    conn = sqlite3.connect('WBInvest.db')
    c = conn.cursor()
    
    # Select the relevant columns
    c.execute('''
        SELECT "Region", "Project Global Practice"
        FROM WBProjects_Analyze
    ''')
    rows = c.fetchall()
    
    # Initialize a dictionary to store the word counts
    word_counts = {}
    
    for row in rows:
        region, practices = row
        if practices:
            practice_list = practices.split(';')
            for practice in practice_list:
                key = (region)
                if key not in word_counts:
                    word_counts[key] = Counter()
                word_counts[key][practice.strip()] += 1

# Write the word counts to a CSV file
    with open('WBPractise.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Region', 'Practice', 'Count'])  # Header

        # Print the word counts
        for key, counter in word_counts.items():
            region = key
            print(f'Region: {region}')
            for practice, count in counter.items():
                writer.writerow([region,practice,count])
                #print(f'  {practice}: {count}')
        conn.commit()
        conn.close()        
word_count2()


import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('WBPractise.csv')

def plot_practice_barchart():
    # Get unique Zones and Shades dynamically
    regions = df['Region'].unique()
    practices = df['Practice'].unique()

    # Initialize the plot
    plt.figure(figsize=(12, 8))
    sns.set(style="whitegrid")

    # Create a color palette with unique colors for each practice
    unique_practices = df['Practice'].unique()
    palette = sns.color_palette("husl", len(unique_practices))
    color_dict = dict(zip(unique_practices, palette))

    # Plot each Zone dynamically
    for region in regions:
        region_data = df[df['Region'] == region]
        plt.bar(
            #[f"{practices}-{region}" for practices in region_data['Practice']], #Creates double x-axis
            region_data['Practice'], #Creates stake columns
            region_data['Count'], 
            label=f"Region {region}"
        )

    # Customize the chart
    plt.title("Count by Region and Practice (Dynamic Handling)", fontsize=16)
    #plt.xlabel("Region and Practice", fontsize=12)
    plt.xlabel("Practice", fontsize=12)
    plt.ylabel("Count", fontsize=12)
    plt.xticks(rotation=45, ha='right', fontsize=10)
    plt.legend(title="Region")
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    #plt.gca().set_xticklabels([])  # Remove x-axis labels
    plt.tight_layout()

    # Show the plot
    plt.savefig('WBPractice.png')
    plt.show()
    plt.close()

plot_practice_barchart()
