import pandas as pd  # pip install pandas

# ตั้งค่า Pandas ให้แสดงทุกคอลัมน์
# pd.set_option('display.max_columns', None)

df = pd.read_excel(
    io='.\HRLOS_Summary.xlsx',
    engine='openpyxl',
    sheet_name='SC1_jtl',
    skiprows=0,
    usecols='A:M',
    nrows=1000,
)
print(df.columns)  # แสดงชื่อคอลัมน์ทั้งหมด
print(df.dtypes)  # แสดงประเภทข้อมูลของแต่ละคอลัมน์
print(df.head())
print(df.tail())
