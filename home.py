import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from queries import *
import time

st.set_page_config(page_title="Dashboard",page_icon="📊",layout="wide")
st.subheader("MENTAL HEALTH ANALYSING DASHBOARD🧠📈")

#fetch data
result=fetch_all_data()
df=pd.DataFrame(result,columns=["Sno","Age","Gender","Occupation","Days_Indoors","Growing_Stress","Quarantine_Frustrations","Changes_Habits","Mental_Health_History","Weight_Change","Mood_Swings","Coping_Struggles","Work_Interest","Social_Weakness",])
#sidebar

st.sidebar.image("data\logo__.png",caption="Mental Health Analysis",width=300)
with st.sidebar:
    selected=option_menu(
    menu_title="Main Menu",
    options=["Home","Charts","Progress","TabularView"],
    icons=["house","bi bi-bar-chart","eye","bi bi-table"],
    menu_icon=["cast"],
    default_index=0
    )
st.sidebar.subheader("Please filter")
Gender=st.sidebar.multiselect(
"Select Gender",
options=df["Gender"].unique(),
default=df["Gender"].unique()
)

Age=st.sidebar.multiselect(
    "Select Age_group",
    options=df["Age"].unique(),
    default=df["Age"].unique()
)
df_selection=df.query(
    "Gender==@Gender & Age==@Age"
)
Count_of_people=df_selection["Sno"].count()
Social_Weakness=(df_selection["Social_Weakness"]=="Yes").sum()
Mood_swings=(df_selection["Mood_Swings"]=="High").sum()
Weight_change=(df_selection["Weight_Change"]=="Yes").sum()
Mental_Health_History=(df_selection["Mental_Health_History"]=="Yes").sum()
Gender_Category=len(df_selection["Gender"].unique())
Occupation=df_selection["Occupation"].mode().iloc[0]
Quarantine_affected=(df_selection["Quarantine_Frustrations"]=="Yes").sum()
no_work_interest=(df_selection["Work_Interest"]=="No").sum()
Changes_Habits=(df_selection["Changes_Habits"]=="Yes").sum()
struggles=(df_selection["Coping_Struggles"]=="Yes").sum()

#home_table
def home():

    #compute top analytics
    total1,total2,total3,total4=st.columns(4,gap="large")
    with total1:
        st.info("Total Count of People: ",icon="👥")
        st.metric(label="Total Count",value=Count_of_people)
    with total2:
        st.info("Gender Answered:",icon="👫")
        st.metric(label="Gender",value=Gender_Category)
    with total3:
        st.info("Mostly Affected Occupation:",icon="👜")
        st.metric(label="Occupation",value=str(Occupation))
    with total4:
        st.info("Affected by Quarantine:",icon="😷")
        st.metric(label="Count",value=Quarantine_affected)
    st.markdown("""---""")

    total5,total6,total7,total8=st.columns(4,gap="large")
    with total5:
        st.info("Had Social Weakness: ",icon="🤕")
        st.metric(label="Social Weakness",value=Social_Weakness)
    with total6:
        st.info("Had Mood Swings:",icon="🤯")
        st.metric(label="Mood Swings",value=Mood_swings)
    with total7:
        st.info("Had Weight Change:",icon="🎰")
        st.metric(label="Occupation",value=Weight_change)
    with total8:
        st.info("Previously Affected :",icon="😒")
        st.metric(label="Mental health Affected",value=Mental_Health_History)
    st.markdown("""---""")

#graphs
        
def graphs():
    #simple bar graph 
    Affected_by_occupation=(
    df_selection[df_selection["Growing_Stress"]=="Yes"]["Occupation"].unique()
    )
    Days=df_selection["Days_Indoors"].unique()  
    fig_occupation=px.bar(
        Affected_by_occupation,
        x=Days,
        y=Affected_by_occupation,
        title="<b> Analysis of Growing stress by Occupation with Age</b>",
        color_discrete_sequence=["#86A789"]*len(Affected_by_occupation),
    )
    fig_occupation.update_layout(
        plot_bgcolor="#E1F0DA",
        xaxis=(dict(showgrid=False))
    )
    fig_occupation.update_xaxes(title="Occupation")
    fig_occupation.update_yaxes(title="Growing Stress with respect to Age")
    
    #simple line graph 
    Affected_by_age=df_selection[df_selection["Growing_Stress"]=="Yes"].groupby(by=["Age"]).count()
    fig_age=px.line(
        Affected_by_age,
        x=Affected_by_age.index,
        y="Sno",
        orientation="h",
        title="<b> Analysis of Growing stress by Age</b>",
        color_discrete_sequence=["#86A789"]*len(Affected_by_age),
        #template="plotly_white",
    )
    fig_age.update_layout(
        plot_bgcolor="#E1F0DA",
        xaxis=(dict(showgrid=False))        
    )
    left,right=st.columns([2,2])
    left.plotly_chart(fig_age,use_container_width=True,use_container_height=True)
    right.plotly_chart(fig_occupation,use_container_width=True,use_container_height=True)
    
    #simple scatter plot
    Affected_by_days=(df_selection["Days_Indoors"]).unique()
    Occu=df_selection["Occupation"].unique()
    fig_weight = px.scatter(
        Affected_by_days,
        x=Occu,
        y=Affected_by_days,
        title="<b>Analysis of Weight change with Occupation</b>",
        color_discrete_sequence=["#86A789"]*len(Affected_by_days),
        )
    fig_weight.update_layout(
        plot_bgcolor="#E1F0DA",
        xaxis=(dict(showgrid=False))
    )
    fig_weight.update_xaxes(title="Days_Indoors")
    fig_weight.update_yaxes(title="Weight Change with respect to Occupation")

#simple pie chart
    color_list=["#163020","#304D30","#337357","#99BC85"]
    Affected_by_quarantine=(df_selection[df_selection["Quarantine_Frustrations"]=="Yes"]["Occupation"]).value_counts()
    Occupation=df_selection["Occupation"].unique()
    fig_quarantine = px.pie(
        Affected_by_quarantine,
        names=Occupation,
        values=(Affected_by_quarantine)*len(Occupation),
        color_discrete_sequence=color_list,
        title="Analysis of Quarantine Affected change with Occupation")
    left1,right1=st.columns([2,2])
    left1.plotly_chart(fig_weight,use_container_width=True,use_container_height=True)
    right1.plotly_chart(fig_quarantine,use_container_width=True,use_container_height=True)


def table():
        with st.expander("Tabular"):
            showData=st.multiselect("Table View:",df_selection.columns)
            st.write(df_selection[showData])


def progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff99, #FFFF00)}<\style>""",unsafe_allow_html=True)
    target=824
    current=Count_of_people
    percent=round((current/target*100))
    mybar=st.progress(0)
    st.write("you have ", percent,"%", "of", (format(target, 'd')))
    for percent_complete in range(percent):
        time.sleep(0.01)
        mybar.progress(percent_complete+1, text="Count of people")

    st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #D2E3C8, #86A789)}<\style>""",unsafe_allow_html=True)
    target=Count_of_people
    current=Quarantine_affected
    percent=round((current/target*100))
    mybar=st.progress(0)
    st.write("you have ", percent,"%", "of", (format(target, 'd')))
    for percent_complete in range(percent):
        time.sleep(0.01)
        mybar.progress(percent_complete+1, text="Affected by Quarantine")

    st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff99, #FFFF00)}<\style>""",unsafe_allow_html=True)
    target=Count_of_people
    current=no_work_interest
    percent=round((current/target*100))
    mybar=st.progress(0)
    st.write("you have ", percent,"%", "of", (format(target, 'd')))
    for percent_complete in range(percent):
        time.sleep(0.01)
        mybar.progress(percent_complete+1, text="Had No Work interest")

    st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff99, #FFFF00)}<\style>""",unsafe_allow_html=True)
    target=Count_of_people
    current=struggles
    percent=round((current/target*100))
    mybar=st.progress(0)
    st.write("you have ", percent,"%", "of", (format(target, 'd')))
    for percent_complete in range(percent):
        time.sleep(0.01)
        mybar.progress(percent_complete+1, text="Coping Struggles")

    st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff99, #FFFF00)}<\style>""",unsafe_allow_html=True)
    target=Count_of_people
    current=Changes_Habits
    percent=round((current/target*100))
    mybar=st.progress(0)
    st.write("you have ", percent,"%", "of", (format(target, 'd')))
    for percent_complete in range(percent):
        time.sleep(0.01)
        mybar.progress(percent_complete+1, text="Changes Habits")        

    st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff99, #FFFF00)}<\style>""",unsafe_allow_html=True)
    target=Count_of_people
    current=Weight_change
    percent=round((current/target*100))
    mybar=st.progress(0)
    st.write("you have ", percent,"%", "of", (format(target, 'd')))
    for percent_complete in range(percent):
        time.sleep(0.01)
        mybar.progress(percent_complete+1, text="Gone through Weight change")

    st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff99, #FFFF00)}<\style>""",unsafe_allow_html=True)
    target=Count_of_people
    current=Social_Weakness
    percent=round((current/target*100))
    mybar=st.progress(0)
    st.write("you have ", percent,"%", "of", (format(target, 'd')))
    for percent_complete in range(percent):
        time.sleep(0.01)
        mybar.progress(percent_complete+1, text="Faced Social Weakness")

    st.markdown("""<style>.stProgress > div > div > div > div {background-image: linear-gradient(to right, #99ff99, #FFFF00)}<\style>""",unsafe_allow_html=True)
    target=Count_of_people
    current=Mood_swings
    percent=round((current/target*100))
    mybar=st.progress(0)
    st.write("you have ", percent,"%", "of", (format(target, 'd')))
    for percent_complete in range(percent):
        time.sleep(0.01)
        mybar.progress(percent_complete+1, text="Gone through Mood Swings")

  
#switcher

if selected=="Home":
    st.header(f"Page: {selected}")
    home()
if selected=="Charts":
    st.header(f"Page: {selected}")
    graphs()
if selected=="Progress":
    st.header(f"Page: {selected}")
    progressbar()
if selected=="TabularView":
    st.header(f"Page: {selected}")
    table()




