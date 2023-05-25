import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from numerize import numerize

# atur nama aplikasi/title halaman
st.set_page_config(page_title="Latihan Streamlit", 
                   layout="wide")

# formatting style
m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: #0099ff;
    color:#ffffff;
}
div.stButton > button:hover {
    background-color: #00ff00;
    color:#ff0000;
    }
</style>""", unsafe_allow_html=True)

"# Superstore Dashboard"
df = pd.read_csv("superstore.csv")
# st.write(df)

df.info()
# Tipe data dari atribut ship_date dan order_data harusnya datetime
df['ship_date'] = pd.to_datetime(df['ship_date'])
df['order_date'] = pd.to_datetime(df['order_date'])
# tipe data postalcode harusnya object/string, bukan int. karena ia tidak diioperasikan scr matematis
df['postal_code'] = df['postal_code'].apply(lambda x: str(x))

# 1. Periksa tahun terakhir dari data
df['order_year'] = df['order_date'].dt.year
MAX_YEAR = df['order_year'].max()

# 2. Hitung sales, banyaknya order, banyaknya konsumen, profit %
# gunakan pivot table untuk ngebreakdown multivariabel
mx_data = pd.pivot_table(
    data=df,
    index="order_year",
    aggfunc={
        'sales':np.sum,
        'profit':np.sum,
        'order_id':pd.Series.nunique,
        'customer_id':pd.Series.nunique
    }
).reset_index()

mx_data['profit_ratio'] = (mx_data['profit'] * 100.0) / mx_data['sales']

col1, col2, col3, col4 = st.columns(4)

# menampilkan metris
data = mx_data[mx_data['order_year']==MAX_YEAR]
with col1:
    st.metric(label="Sales",
            value=numerize.numerize(mx_data['sales'][3]),
            delta=((mx_data['sales'][3]-mx_data['sales'][2])/mx_data['sales'][2])*100
            )
    
with col2:
    st.metric(label="Order",
            value=mx_data['order_id'][3],
            delta=((mx_data['order_id'][3]-mx_data['order_id'][2])/mx_data['order_id'][2])*100
            )
    
with col3:
    st.metric(label="Customer",
            value=mx_data['customer_id'][3],
            delta=((mx_data['customer_id'][3]-mx_data['customer_id'][2])/mx_data['customer_id'][2])*100
            )
    
with col4:
    st.metric(label="Profit",
            value=f"{mx_data['profit_ratio'][3]:.2f}%",
            delta=((mx_data['order_id'][3]-mx_data['order_id'][2])/mx_data['order_id'][2])*100
            )

# Membuat Chart
"# Sales Chart"

# altair membuat objek berupa chart dengan data di dalam parameter
sales_line = alt.Chart(df[df['order_year']==MAX_YEAR]).mark_line()
# encode chart, ngedefinisiin sumbu x dan y
freqOption = st.selectbox(
    "Pilih Frekuensi",
    ["Harian", "Bulanan"]
)

timeUnit = {
    "Harian" : "yearmonthdate",
    "Bulanan": "yearmonth"
}

sales_line = alt.Chart(df[df['order_year']==MAX_YEAR]).mark_line().encode(
                                                            alt.X('order_date', title="Order Date", timeUnit=timeUnit[freqOption]),
                                                            alt.Y('sales', title="Sales", aggregate='sum')
                                                            )

st.altair_chart(sales_line, use_container_width=True)

# Membuat Sales per Region
"# Sales per Region"
aggOption = st.selectbox(
    "Pilih Agregat",
    ['average', 'count', 'distinct', 'max', 'mean', 'median', 'min', 'missing', 'product', 'q1', 'q3', 'ci0', 'ci1', 'stderr', 'stdev', 'stdevp', 'sum', 'valid', 'values', 'variance', 'variancep']
)

reg1, reg2, reg3, reg4 = st.columns(4)

with reg1:
    "## West"
    sales_cat1 = alt.Chart(df[(df['order_year']==MAX_YEAR)&(df['region']=="West")]).mark_bar().encode(
                                                            alt.X('category', title="Category", axis=alt.Axis(labelAngle=0)),
                                                            alt.Y('sales', title="Sales", aggregate=aggOption)
                                                            )

    st.altair_chart(sales_cat1, use_container_width=True)

with reg2:
    "## East"
    sales_cat2 = alt.Chart(df[(df['order_year']==MAX_YEAR)&(df['region']=="East")]).mark_bar().encode(
                                                            alt.X('category', title="Category", axis=alt.Axis(labelAngle=0)),
                                                            alt.Y('sales', title="Sales", aggregate=aggOption)
                                                            )

    st.altair_chart(sales_cat2, use_container_width=True)

with reg3:
    "## South"
    sales_cat3 = alt.Chart(df[(df['order_year']==MAX_YEAR)&(df['region']=="South")]).mark_bar().encode(
                                                            alt.X('category', title="Category", axis=alt.Axis(labelAngle=0)),
                                                            alt.Y('sales', title="Sales", aggregate=aggOption)
                                                            )

    st.altair_chart(sales_cat3, use_container_width=True)

with reg4:
    "## Central"
    sales_cat4 = alt.Chart(df[(df['order_year']==MAX_YEAR)&(df['region']=="Central")]).mark_bar().encode(
                                                            alt.X('category', title="Category", axis=alt.Axis(labelAngle=0)),
                                                            alt.Y('sales', title="Sales", aggregate=aggOption)
                                                            )

    st.altair_chart(sales_cat4, use_container_width=True)
# menampilkan tabel
st.dataframe(df)
st.dataframe(mx_data)