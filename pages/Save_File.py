import database
import random
import streamlit as st
import pandas as pd
#import Previous_Storage as ps
import Main_Detection as md
def print_res(keys,result):
    test_keys=keys
    res={}
    temp_array = []
    for names_index in range(len(test_keys)):
        for arrays in result:
            #print(arrays[names_index])
            temp_array.append(arrays[names_index])
    
        res[test_keys[names_index]] = temp_array
        temp_array=[]
        
    df = pd.DataFrame(res)   
    df.index = ["Quartile 1 Percentage","Quartile 2 Percentage","Quartile 3 Percentage","Quartile 4 Percentage"]
    x1=['Q1','Q2','Q3','Q4']
    st.table(df)
    print(res)

def CreateLineData(dataz):
    # opening the file in read mode
    my_file = open(dataz, "r")
  
    # reading the file
    data = my_file.read()
  
    # replacing end splitting the text 
    # when newline ('\n') is seen.
    data_into_list = data.split("\n")
    data_into_list.pop()
    my_file.close()

    return data_into_list

def extractDigits(lst):
    res = []
    for el in lst:
        sub = el.split(' ')
        res.append(sub)
      
    return res


try:
    'username' in st.session_state["username"]

    st.write("Do You Want To Save The Following Data?")
    temp=(CreateLineData("datatemp.txt"))

    tempData=extractDigits(temp)
    tempName=CreateLineData("name.txt")  
    print_res(tempName,tempData)

    title = st.text_input("Please enter the title to save the file")
    if title:
        if database.insert_data(str(random.randrange(1, 10**3)), st.session_state["username"],title,tempData,tempName):
            st.success("Saved")

except:
    st.error("Please Log In at main detection first")


