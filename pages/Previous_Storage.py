import database
import random
import streamlit as st
import pandas as pd

def print_res_table(keys,result):
    test_keys=keys
    res={}
    temp_array = []
    for names_index in range(len(test_keys)):
        for arrays in result:
            #print(arrays[names_index])
            temp_array.append(round(int(float(arrays[names_index]))))
    
        res[test_keys[names_index]] = temp_array
        temp_array=[]
    
    
    df = pd.DataFrame(res)
    df.index = ["Quartile 1 Percentage","Quartile 2 Percentage","Quartile 3 Percentage","Quartile 4 Percentage"]
    st.table(df)
    st.line_chart(df)







#Try to catch if user is not login yet but try access data
try:
    'username' in st.session_state["username"]
    username = st.session_state["username"]
    name = st.session_state["name"]
    st.write(name,"'s Data")
    breh = random.randrange(1, 10**3)
    bruh=database.fetch_users(username)
    if username:
        for breh in bruh:
            st.write(breh["title"])
            print_res_table(breh["characters"],breh["quartile"])

except:
    st.error("Please Log In at main detection first")



