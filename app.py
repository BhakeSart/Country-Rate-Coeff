import streamlit as st
import pandas as pd

df=pd.read_excel("dataset-v1.xlsx",sheet_name="Sheet4")

st.header('Country Rate Co-efficient Calculator', divider='blue')
country = st.selectbox("Select Country",df["Country"].unique())
year_logic=df.loc[df["Country"]==country,"Year"].values[0].max()
custom_value = st.number_input("Insert Custom Value")

denom=df.loc[(df["Country"]== country) & (df["Year"]==year_logic),"Hourly Wage"].values[0]
wage=round(denom,2)
st.metric(label="Hourly wage of the selected country", value=wage)

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = True

if st.session_state.clicked:
    
    df["Coefficient"]=df["Hourly Wage"]/denom
    df["Output"]=df["Coefficient"]*custom_value
    latest_year=df.groupby("Country")["Year"].idxmax()
    final_df=df.loc[latest_year]
    st.write(final_df)

st.write(" ")
button=st.button("Calculate",on_click=click_button)


st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")

st.subheader("Country Comparator",divider="blue")
comp_country_select = st.multiselect("Select a Country to compare",df["Country"].unique())
comp_latest_year=df.groupby("Country")["Year"].idxmax()
comp_final_df=df.loc[comp_latest_year]
round_op=round(custom_value,1)
base_comp=pd.DataFrame({"Base Country":[country],
                        "Output":[round_op]})
st.write(base_comp)
comp_df=comp_final_df[comp_final_df["Country"].isin(comp_country_select)]

comp_df_op=pd.DataFrame({"Country":comp_df["Country"],
                         "Output":comp_df["Output"]})
st.write(comp_df_op)

st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.write(" ")
st.subheader("Plotting Countries",divider="blue")
latest_year=df.groupby("Country")["Year"].idxmax()
final_df=df.loc[latest_year]
country_select = st.multiselect("Select a Country to plot",final_df["Country"].unique()) 
countries={'Countries': country_select}
final_country=pd.DataFrame(countries)

st.write('You selected:', country_select)
metric_columns=["Monthly Wage","Hourly Wage","Coefficient","Output"]
df_metric=final_df[metric_columns]

metrics_selector=st.selectbox("Select a metric to plot",df_metric.columns)
st.write("You Selected:",metrics_selector)

filtered_df=final_df[final_df["Country"].isin(country_select)]
st.write(filtered_df)



plot=sns.barplot(filtered_df, x="Country",y=metrics_selector,hue="Country")
st.pyplot(plot.get_figure())
