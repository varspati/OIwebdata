import streamlit as st
import os
import pandas as pd
from PIL import Image
import sys
import database as db
import streamlit_authenticator as stauth
from streamlit_login_auth_ui.widgets import __login__

# cd Option_Chain_scripts
# streamlit run UI_streamlit.py
st.set_page_config(page_title="Option Chain Dashboard", page_icon=':bar_chart:', layout='wide')

__login__obj = __login__(auth_token = "pk_prod_63Z972DXZB4CGJKS8NTD61Q7F5T4", 
                    company_name = "Divine Academy",
                    width = 200, height = 250, 
                    logout_button_name = 'Logout', hide_menu_bool = False, 
                    hide_footer_bool = False, 
                    lottie_url = 'https://assets2.lottiefiles.com/packages/lf20_jcikwtux.json')

LOGGED_IN = __login__obj.build_login_ui()

if LOGGED_IN == True:
    directory_of_python_script = os.path.dirname(os.path.abspath(__file__))
    all_files = os.listdir(directory_of_python_script)    
    csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
    csv_files_name = [os.path.splitext(each)[0] for each in csv_files]
    # print(csv_files_name)

    image_path = os.path.join(directory_of_python_script, "nse logo.png")
    image =  Image.open(image_path)
    st.image(image)

    st.title('Option Chain Live Data Dashboard')

    Expiry_Date = []
    scripts = st.selectbox('Select Scripts', options=['select']+csv_files_name)
    if scripts != 'select':
        df = pd.read_csv(os.path.join(directory_of_python_script, f"{scripts}.csv"), on_bad_lines='skip')
        df.columns = ['Index','TimeStamp', 'Symbol', 'UNDERLYING', 'CALL_P_CHNG', 'CALL_CHNG', 'CALL_IV', 'CALL_OI', 'CALL_CHNG_OI', 'STRIKE_PRICE', 'EXPIRY_DATE', 'PUT_P_CHNG', 'PUT_CHNG', 'PUT_IV', 'PUT_OI', 'PUT_CHNG_OI', 'PCR', 'PCR_avrg', 'resistance', 'support']
        df = df.drop('Index', axis=1)
        df["TimeStamp"] = pd.to_datetime(df["TimeStamp"])
        df['TimeStamp'] = df['TimeStamp'].dt.strftime('%H:%M')
        Expiry_Date.extend(df.iloc[:, 9].tolist())
        Expiry_Date = list(set(Expiry_Date))
        Expiry_Date = st.selectbox('Select Expiry Date', options=Expiry_Date)
        Range = list(set())
    if st.button('Submit'):
        temp_df = df.loc[(df['Symbol'] == scripts) & (df['EXPIRY_DATE'] == Expiry_Date), ['TimeStamp', 'CALL_CHNG_OI', 'PUT_OI', 'PUT_CHNG_OI', 'PCR', 'PCR_avrg', 'resistance', 'support']] 
        st.dataframe(temp_df)

 