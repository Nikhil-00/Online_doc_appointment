import mysql.connector
from tabulate import tabulate
import streamlit as st 
from streamlit_option_menu import option_menu
from PIL import Image
import time as t
import pandas as pd

# Database connection
mydb = mysql.connector.connect(host="localhost", user="root", password="pandey",database = "doctor_appointment")
mycursor = mydb.cursor()

# Creating the necessary databases and tables if they do not exist
mycursor.execute("CREATE DATABASE IF NOT EXISTS doctor_appointment")
mycursor.execute("USE doctor_appointment")
mycursor.execute("CREATE TABLE IF NOT EXISTS user(user_name VARCHAR(50) PRIMARY KEY, password VARCHAR(30))")
mycursor.execute("CREATE TABLE IF NOT EXISTS doctor(doctor_name VARCHAR(20) PRIMARY KEY, password VARCHAR(20))")
mycursor.execute("CREATE TABLE IF NOT EXISTS doctor_details(doctor_name VARCHAR(20), dept_id VARCHAR(5) PRIMARY KEY, doctor_department VARCHAR(20), doctor_phone VARCHAR(11), doctor_available VARCHAR(20))")
mycursor.execute("CREATE TABLE IF NOT EXISTS appointment(patient_phno VARCHAR(11) PRIMARY KEY, patient_name VARCHAR(20), department_name VARCHAR(25), date_of_appointment Varchar(10))")

# Medanta
st.title("WELCOME TO :red[MEDANTA]")
st.image("hospital.png")
st.logo("hospital.png")

#
# ADD APPOINTMENTS
def add_appointment():
    patient_phno = st.text_input("Enter Phone number")
    patient_name = st.text_input("Enter patient name")
    dept_name = st.selectbox("Pick department name ",["None","Cardiology","Dental","Orthology"])
    mycursor.execute("select doctor_name,doctor_department,doctor_available from doctor_details")
    data=mycursor.fetchall()
    st.subheader("Available Dates")
    df=pd.DataFrame(data,columns=mycursor.column_names)
    st.dataframe(df)
    date_of_appointment = st.date_input("Appointment Date",format="YYYY-MM-DD")
    tap2 = st.button("Add Details")
    if(tap2):
        mycursor.execute("select patient_phno from appointment where patient_phno='"+patient_phno+"'")
        pot3 = mycursor.fetchone()
        if(pot3 is not None):
            st.error("Phone number already exits ")
        else:
            mycursor.execute("insert into appointment values('"+patient_phno+"','"+patient_name+"','"+dept_name+"','"+str(date_of_appointment)+"')")
            mydb.commit()
            st.balloons()
            st.success("Details added successfully")
#Delete Appointments
def delete_appointment():
    patient_phno = st.text_input("Enter Phone number")
    dele=st.button("Delete")
    if(dele):
        mycursor.execute("select patient_phno from appointment where patient_phno = '"+patient_phno+"'")
        pot = mycursor.fetchone()
        if pot is None:
            st.error("Invalid Phone_number")
        else:
            mycursor.execute("Delete from appointment where patient_phno='"+patient_phno+"'")
            mydb.commit()
            st.balloons()
            st.success("Appointment Successfully Deleted")

# Search Appointments
def search_appointment():
    search = option_menu(
        menu_title=None,
        options=["Previous Treatment","Appointments Details"],
        orientation="horizontal",
    )
    if search=="Appointments Details":
        patient_phno = st.text_input("Enter Phone number")
        ser=st.button("Search")
        if(ser):
            mycursor.execute("select * from appointment where patient_phno = '"+patient_phno+"'")
            data = mycursor.fetchone()
            if data is not None  :
                st.subheader("Your Appointment")
                mycursor.execute("select * from appointment where patient_phno = '"+patient_phno+"'")
                data1=mycursor.fetchall()
                df=pd.DataFrame(data1,columns=mycursor.column_names)
                st.dataframe(df)
                st.balloons()
            elif data is None :
                st.error("Invalid Phone Number")
    if search == "Previous Treatment":
        patient_phno_ = st.text_input("Enter Phone number")
        ser1=st.button("Search")
        if(ser1):
            mycursor.execute("select * from treatement where patient_phno = '"+patient_phno_+"'")
            data2 = mycursor.fetchone()
            if data2 is not None  :
                st.subheader("Previous Treatment")
                print("hello")
                mycursor.execute("select * from treatement where patient_phno = '"+patient_phno_+"'")
                print("helloooooo")
                data3=mycursor.fetchall()
                df3=pd.DataFrame(data3,columns=mycursor.column_names)
                st.dataframe(df3)
                st.balloons()
            elif data2 is None :
                st.error("Invalid Phone Number")
# Treatment 
def doc_treatment():
    doc_dept_id = st.text_input("Enter deptartment Id")
    patient_phno = st.text_input("Enter Patient Phone Number")  
    if "Login" not in st.session_state:
        st.session_state.Login = False
    if "Treatment" not in st.session_state:
        st.session_state.Treatment = False
    if st.button("Login"):
        st.session_state.Login = True
        mycursor.execute("select patient_phno from appointment where patient_phno='"+patient_phno+"' and department_name = (Select dept_name from department where dept_id='"+doc_dept_id+"')")
        check1 = mycursor.fetchone()
        if(check1 is None):
            st.error("Invalid Department Id")
        else:
            st.success("Login")  
    if st.session_state.Login :
        if st.button("Treatment"):
            st.session_state.Treatment = True
    if st.session_state.Treatment:
        mycursor.execute("select patient_phno from appointment where patient_phno='"+patient_phno+"' and department_name = (Select dept_name from department where dept_id='"+doc_dept_id+"')")
        check = mycursor.fetchone()
        if check is None:
            st.error("Invalid Phone Number")
        else:
            st.subheader("Previous History")
            mycursor.execute("select * from treatement where patient_phno = '"+patient_phno+"'")
            data2 = mycursor.fetchall()
            df2=pd.DataFrame(data2,columns=mycursor.column_names)
            st.dataframe(df2)
            st.subheader("Appoinment details")
            mycursor.execute("select * from appointment where patient_phno = '"+patient_phno+"'")
            data1=mycursor.fetchall()
            df1=pd.DataFrame(data1,columns=mycursor.column_names)
            st.dataframe(df1)
            mycursor.execute("select date_of_appointment from appointment where patient_phno = '"+patient_phno+"'")
            date_appo = mycursor.fetchone()
            treat=option_menu(
                menu_title=None,
                options=["Reappointment","Treated"],
                orientation="horizontal",
            )
            if(treat=="Treated"):
                patient_treat = st.text_input("Treatment")
                if st.button("ADD Treatment"):
                    mycursor.execute("insert into treatement values('"+patient_phno+"','"+str(date_appo[0])+"','"+patient_treat+"')")
                    mydb.commit()
                    st.balloons()
                    st.success("Data Successfully Stored")
                    mycursor.execute("insert into record select * from appointment where patient_phno='"+patient_phno+"'")
                    mydb.commit()
                    mycursor.execute("delete from appointment where patient_phno='"+patient_phno+"'")
                    mydb.commit()
            if(treat=="Reappointment"):
                patient_treat = st.text_input("Treatment")
                re_app= st.date_input("Reappointment Date")
                mycursor.execute("insert into treatement values('"+patient_phno+"','"+str(date_appo[0])+"','"+patient_treat+"')")
                mycursor.execute("insert into record select * from appointment where patient_phno='"+patient_phno+"'")
                mycursor.execute("delete from appointment where patient_phno='"+patient_phno+"'")
                mydb.commit()
                mycursor.execute("insert into appointment select * from appointment where patient_phno='"+patient_phno+"'")
                mycursor.execute("update appointment set date_of_appointment ='"+str(re_app[0])+"' where patient_phno='"+patient_phno+"'")
                mydb.commit()
                st.balloons()
                st.success("Data Successfully Stored")
                mycursor.execute("delete from appointment where patient_phno='"+patient_phno+"'")
                mydb.commit()
                
                
                
            
                

# Main menu    
selected = option_menu(
    menu_title="Main menu",
    options=["Home","Patient","Doctor","Authority"],
    orientation="horizontal",
)
if (selected == 'Home'):
    st.title("HOME")
    st.image("Medanta.jpeg")
    st.subheader("About Us")
    st.write("Medanta Medanta one of the country’s largest multi-speciality tertiary care provider is founded by Dr. Naresh Trehan, a world-renowned cardiovascular and cardiothoracic surgeon, with the mission to deliver advanced but affordable medical services to patients. For four years in a row, Medanta Gurugram ranked the best private hospital in India in 2020, 2021, 2022 and 2023. It also featured in the list of top 250 global hospitals in 2023 by Newsweek.")
elif (selected=="Patient"):
    appointments = option_menu(
        menu_title=None,
        options=["ADD","DELETE","SEARCH"],
        orientation="horizontal",
    )
    if(appointments=="ADD"):
        add_appointment()
    elif(appointments=="DELETE"):
        delete_appointment()
    elif(appointments=="SEARCH"):
        search_appointment()
elif(selected=="Doctor"):
    doc = option_menu(
        menu_title=None,
        options=["Appointments","Treatment"],
        orientation="horizontal"
    )
    if(doc=="Appointments"):
        dept_id = st.text_input("Enter deptartment Id")
        date_of_appointment = st.date_input("Enter Appointment Date")
        click=st.button("Search")
        if(click):
            mycursor.execute("Select dept_name from department where dept_id='"+dept_id+"'")
            data=mycursor.fetchone()
            if(data is not None):
                mycursor.execute("select * from appointment where date_of_appointment = '"+str(date_of_appointment)+"' and department_name = (Select dept_name from department where dept_id='"+dept_id+"') ")
                data1 = mycursor.fetchall()
                df=pd.DataFrame(data1,columns=mycursor.column_names)     
                st.dataframe(df)     
            else:
                st.error("Invalid Department_id")      
    elif(doc=="Treatment"):
        doc_treatment()