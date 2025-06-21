import streamlit as st
import pandas as pd
import plotly.express as px
from SqlExecution import *
import plotly.graph_objects as go

st.set_page_config(page_title="Global Nutrition Paradox Dashboard", layout="wide")
st.title("🌍Global Nutrition Paradox Dashboard")
st.markdown("Explore key insights on obesity and malnutrition trends across countries, age groups, and genders.")

tab1, tab2, tab3 = st.tabs(["Obesity Insights | ", "Malnutrition Insights | ", "Combined Obesity & Malnutrition Analysis | "])

# ============ OBESITY ============
with tab1:
    st.header("🍔 Obesity Analysis")

    with st.expander("Top 5 Regions with Highest Obesity (2022)"):
        df1 = pd.DataFrame(fetch_query1())
        st.dataframe(df1)
        st.bar_chart(df1.set_index("Region"))

    with st.expander("Top 5 Countries with Highest Obesity"):
        df2 = pd.DataFrame(fetch_query2())
        st.dataframe(df2)
        st.bar_chart(df2.set_index("Country"))

    with st.expander("Obesity Trend in India Over the Years"):
        df3 = pd.DataFrame(fetch_query3())
        fig = px.line(df3, x="Year", y="Average_Mean_Estimate", title="India's Obesity Trend")
        st.plotly_chart(fig)

    with st.expander("Average Obesity by Gender"):
        df4 = pd.DataFrame(fetch_query4())
        st.dataframe(df4)
        st.bar_chart(df4.set_index("Sex"))

    with st.expander("Country Count by Obesity Level and Age Group"):
        df5 = pd.DataFrame(fetch_query5())
        st.dataframe(df5)

    with st.expander("Most & Least Reliable Countries by CI Width"):
        df6 = pd.DataFrame(fetch_query6())
        st.dataframe(df6)

    with st.expander("Average Obesity by Age Group"):
        df7 = pd.DataFrame(fetch_query7())
        st.dataframe(df7)
        st.bar_chart(df7.set_index("Age_Group"))

    with st.expander("Top 10 Countries with Consistently Low Obesity"):
        df8 = pd.DataFrame(fetch_query8())
        st.dataframe(df8)

    with st.expander("Countries Where Female Obesity > Male by Large Margin"):
        df9 = pd.DataFrame(fetch_query9())
        st.dataframe(df9)

    with st.expander("Global Average Obesity Percentage Over Time"):
        df10 = pd.DataFrame(fetch_query10())
        st.dataframe(df10)
        fig = px.line(df10, x="Year", y="Obesity_Percentage", title="Global Obesity Over Years")
        st.plotly_chart(fig)

# ============ MALNUTRITION ============
with tab2:
    st.header("🥦 Malnutrition Analysis")

    with st.expander("Avg. Malnutrition by Age Group"):
        df11 = pd.DataFrame(fetch_query11())
        st.dataframe(df11)
        st.bar_chart(df11.set_index("Age_Group"))

    with st.expander("Top 5 Countries with Highest Malnutrition"):
        df12 = pd.DataFrame(fetch_query12())
        st.dataframe(df12)

    with st.expander("Malnutrition Trend in Africa"):
        df13 = pd.DataFrame(fetch_query13())
        st.dataframe(df13)
        fig = px.line(df13, x="Year", y="Malnutrition", title="Africa Malnutrition Trend")
        st.plotly_chart(fig)

    with st.expander("Gender-wise Malnutrition"):
        df14 = pd.DataFrame(fetch_query14())
        st.dataframe(df14)
        st.bar_chart(df14.set_index("Sex"))

    with st.expander("Malnutrition Level-wise CI Width by Age Group"):
        df15 = pd.DataFrame(fetch_query15())
        st.dataframe(df15)

    with st.expander("Yearly Malnutrition Trends in India, Nigeria, Brazil"):
        df16 = pd.DataFrame(fetch_query16())
        fig = px.line(df16, x="Year", y="Malnutrition", color="Country", title="Malnutrition Trend")
        st.plotly_chart(fig)

    with st.expander("Regions with Lowest Malnutrition Averages"):
        df17 = pd.DataFrame(fetch_query17())
        st.dataframe(df17)

    with st.expander("Countries with Increasing Malnutrition"):
        df18 = pd.DataFrame(fetch_query18())
        st.dataframe(df18)

    with st.expander("Year-wise Min and Max Malnutrition"):
        df19 = pd.DataFrame(fetch_query19())
        st.dataframe(df19)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df19['Year'],
            y=df19['Min_Malnutrition'],
            name='Min Malnutrition',
            marker_color='indianred'))
        fig.add_trace(go.Scatter(
            x=df19['Year'],
            y=df19['Max_Malnutrition'],
            name='Max Malnutrition',
            marker_color='skyblue')) 
        fig.update_layout(
            title='Min & Max Malnutrition by year',
            barmode='group',
            xaxis_title='Year',
            yaxis_title='Malnutrition',
            height=600)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("High CI_Width Flags (CI > 5)"):
        df20 = pd.DataFrame(fetch_query20())
        st.dataframe(df20)

# ============ COMBINED ============
with tab3:
    st.header("🔀 Combined Obesity & Malnutrition")

    with st.expander("Obesity vs Malnutrition by Country"):
        df21 = pd.DataFrame(fetch_query21())
        st.dataframe(df21)
        fig = px.scatter(df21, x="Avg_Obesity", y="Avg_Malnutrition", color="Country")
        st.plotly_chart(fig)

    with st.expander("Gender Disparity in Both"):
        df22 = pd.DataFrame(fetch_query22())
        st.dataframe(df22)

    with st.expander("Region-wise Comparison (Africa vs Americas)"):
        df23 = pd.DataFrame(fetch_query23())
        st.dataframe(df23)
        st.line_chart(df23.set_index("Year"))

    with st.expander("Obesity Up, Malnutrition Down"):
        df24 = pd.DataFrame(fetch_query24())
        st.dataframe(df24)
        fig = go.Figure()
        # Obesity: start and end
        fig.add_trace(go.Scatter(
            x=df24['Country'],
            y=df24['Obesity_Start'],
            name='Obesity Start',
            marker_color='indianred'))
        fig.add_trace(go.Scatter(
            x=df24['Country'],
            y=df24['Obesity_End'],
            name='Obesity End',
            marker_color='darkred')) 
        # Malnutrition: start and end
        fig.add_trace(go.Scatter(
            x=df24['Country'],
            y=df24['Malnutrition_Start'],
            name='Malnutrition Start',
            marker_color='skyblue'))
        fig.add_trace(go.Scatter(
            x=df24['Country'],
            y=df24['Malnutrition_End'],
            name='Malnutrition End',
            marker_color='steelblue'))
        fig.update_layout(
            title='Obesity & Malnutrition Change by Country',
            barmode='group',
            xaxis_title='Country',
            yaxis_title='Percentage',
            height=600)
        st.plotly_chart(fig, use_container_width=True)

    with st.expander("Age-wise Trends (Both Conditions)"):
        df25 = pd.DataFrame(fetch_query25())
        st.dataframe(df25)
        fig = px.line(df25, x="Year", y="Avg_Obesity", color="Age_Group", title="Obesity by Age")
        st.plotly_chart(fig)
        fig2 = px.line(df25, x="Year", y="Avg_Malnutrition", color="Age_Group", title="Malnutrition by Age")
        st.plotly_chart(fig2)

    