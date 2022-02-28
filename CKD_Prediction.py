import streamlit as st
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
# import plotly_express as px
import streamlit.components.v1 as components

import shap
import pickle
import joblib
import time

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="Dialysis Risk Prediction for Chronic Kidney Disease Patients",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 加载模型和解释数据
m2 = pickle.load(open('etc_2c.pkl', 'rb'))
e2 = pickle.load(open('explainer_2c.pkl','rb'))

m3 = pickle.load(open('etc_3c.pkl', 'rb'))
e3 = pickle.load(open('explainer_3c.pkl', 'rb'))

m4 = pickle.load(open('etc_4c.pkl', 'rb'))
e4 = pickle.load(open('explainer_4c.pkl', 'rb'))

# m2 = joblib.load('etc_2c.jl')
# e2 = joblib.load('explainer_2c.jl')

# m3 = joblib.load('etc_3c.jl')
# e3 = joblib.load('explainer_3c.jl')

# m4 = joblib.load('etc_4c.jl')
# e4 = joblib.load('explainer_4c.jl')

st.title('Dialysis Risk Prediction for Chronic Kidney Disease Patients')
st.subheader('This model is trying to answer:')
st.subheader('For CKD patient in stage G4 or at the end of stage 3(G3b)，how soon he/she needs to take dialysis')

st.sidebar.header("Patient data")
with st.sidebar:
    age = st.slider(label="年龄(Age)", min_value=30, max_value=90, step=1)
    male = st.sidebar.radio("性别(Gender)", options=['Male', 'Female'], index=0)
    anemic = st.checkbox("贫血(Anemic)", 0)
    cadiopathic = st.checkbox("心脏病(Cadiopathic)", 0)
    diabetic = st.checkbox("糖尿病(Diabetic)", 0)
    Hypertension_episodes = st.checkbox("高血压(Hypertension Episodes)", 0)
    ast = st.slider(label="谷草转氨酶(AST)", min_value=6.0, max_value=1300.0, step=0.1)
    chlorine = st.slider(label='氯(Chlorine)', min_value=83.0, max_value=120.0, step=0.1)
    potassium = st.slider(label="钾", min_value=2.00, max_value=8.00, step=0.01)
    creatinine = st.slider(label='肌酸酐(Creatinine)', min_value=1.60, max_value=7.80, step=0.01)
    creatinine_delta = st.slider(label='肌酸酐变化值(Creatinine delta)', min_value=-5.00, max_value=8.00, step=0.01)
    erythrocytes = st.slider(label="红细胞(Erythrocytes)", min_value=1.80, max_value=6.00, step=0.01)
    erythrocytes_delta = st.slider(label="红细胞变化值(Erythrocytes delta)", min_value=-2.00, max_value=1.30, step=0.01)
    GFR_delta_last_4_months = st.slider(label="过去四个月GFR的变化值(GFR delta last 4 months)", min_value=-16.00,
                                        max_value=36.00, step=0.01)
    GFR_delta_last_year = st.slider(label="过去一年GFR的变化值(GFR delta last year)", min_value=-19.00,
                                    max_value=50.00, step=0.01)
    GFR_standard_deviation_last_4_month = st.slider(label="过去一年GFR的标准差(GFR standard deviation last 4 month)",
                                                    min_value=0.00,
                                                    max_value=16.00, step=0.01)
    GFR_standard_deviation_last_year = st.slider(label="过去一年GFR的标准差(GFR standard deviation last year)", min_value=0.00,
                                                 max_value=16.00, step=0.01)
    last_GFR = st.slider(label="最近的GFR(last GFR)", min_value=15.00,max_value=35.00)
    hematocrit = st.slider(label="红细胞压积(Hematorit)", min_value=15.0, max_value=40.0, step=0.1)
    hemoglobin = st.slider(label="血红蛋白(Hemoglobin)", min_value=0.1, max_value=16.0, step=0.1)
    mean_corpuscular_hemoglobin = st.slider(label='平均红细胞血红蛋白(MCH)', min_value=20.0, max_value=39.0, step=0.1)
    mean_corpuscular_volume = st.slider(label='平均红细胞容积(MCV)', min_value=67.0, max_value=112.0, step=0.1)
    sodium = st.slider(label='钠离子(Sodium)', min_value=120, max_value=160, step=1)
#     specific_gravity_standard_deviation = st.text_input(label='比重标准偏差(SGSTDV)',value='0.0000045')
    specific_gravity_standard_deviation = st.number_input(label='比重标准偏差(SGSTDV)',min_value=0.000000,step=0.000001,max_value=0.0005,value=0.0000045,format="%.6f")
    urate = st.slider(label='尿酸(Urate)', min_value=3.00, max_value=9.00, step=0.01)
    urea = st.slider(label='尿素(Urea)', min_value=50.00, max_value=200.00, step=0.01)
    urea_delta = st.slider(label='尿素变化值(Urea delta)', min_value=-60.00, max_value=60.00, step=0.01)
    features = {"age": age,
                "anemic": anemic,
                "aspartate aminotransferase": ast,
                "cardiopathic": cadiopathic,
                "chlorine": chlorine,
                "creatinine": creatinine,
                "creatinine delta": creatinine_delta,
                "diabetic": diabetic,
                "erythrocytes": erythrocytes,
                "erythrocytes delta": erythrocytes_delta,
                "GFR delta last 4 months": GFR_delta_last_4_months,
                "GFR delta last year": GFR_delta_last_year,
                "GFR standard deviation last 4 months": GFR_standard_deviation_last_4_month,
                "GFR standard deviation last year": GFR_standard_deviation_last_year,
                "hematocrit": hematocrit,
                "hemoglobin": hemoglobin,
                "hypertension episodes": Hypertension_episodes,
                "last GFR": last_GFR,
                "male": male,
                "mean corpuscular hemoglobin": mean_corpuscular_hemoglobin,
                "mean corpuscular volume": mean_corpuscular_volume,
                "potassium": potassium,
                "sodium": sodium,
                "specific gravity standard deviation": specific_gravity_standard_deviation,
                "urate": urate,
                "urea": urea,
                "urea delta": urea_delta
                }
    df = pd.DataFrame([features])
    df['anemic'] = df['anemic'].apply(lambda x: 1 if x == True else 0)
    df['cardiopathic'] = df['cardiopathic'].apply(lambda x: 1 if x == True else 0)
    df['diabetic'] = df['diabetic'].apply(lambda x: 1 if x == True else 0)
    df['hypertension episodes'] = df['hypertension episodes'].apply(lambda x: 1 if x == True else 0)
    df['male']= df['male'].apply(lambda x: 1 if x == '男' else 0)

my_bar = st.progress(0)
st.write(df)

placeholder = st.empty()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Binary model"):
        with placeholder.container():
            df.to_csv('df1.csv',index=0)
            pred = m2.predict_proba(df)
            my_bar.progress(20)
            col11,col22,col33,col44 = st.columns((3,1,1,3))
            with col22:
                st.metric('<12 months', " %d%%"%(pred[0][0]*100), delta=None, delta_color='normal')
            with col33:
                st.metric('>=12 months', " %d%%" % (pred[0][1] * 100), delta=None, delta_color='normal')
            my_bar.progress(40)
            df2=pd.read_csv('./df1.csv')
            shaps_values=e2(df2)
            st.subheader("Feature impact")
            my_bar.progress(70)
            st.pyplot(shap.plots.force(shaps_values[0],matplotlib=True,plot_cmap='BrBG',contribution_threshold=0.05))
            my_bar.progress(100)

with col2:
    if st.button("Three-class model"):
        with placeholder.container():
            df.to_csv('df1.csv',index=0)
            pred = m3.predict_proba(df)
            my_bar.progress(20)
            col11,col22,col33,col44,col55 = st.columns((3,2,2,2,3))
            with col22:
                st.metric('<6 month', " %d%%"%(pred[0][0]*100), delta=None, delta_color='normal')
            with col33:
                st.metric('Btw 6-18 months', " %d%%" % (pred[0][1] * 100), delta=None, delta_color='normal')
            with col44:
                st.metric('>18 months', " %d%%" % (pred[0][2] * 100), delta=None, delta_color='normal')
            my_bar.progress(40)
            df2=pd.read_csv('./df1.csv')
            shaps_values=e3(df2)
            st.subheader("Feature impact")
            my_bar.progress(70)
            st.pyplot(shap.plots.force(shaps_values[0],matplotlib=True,contribution_threshold=0.05))
            my_bar.progress(100)

with col3:
    if st.button("Four-class model"):
        with placeholder.container():
            df.to_csv('df1.csv',index=0)
            pred = m4.predict_proba(df)
            my_bar.progress(20)
            col11,col22,col33,col44 = st.columns((2,2,2,2))
            with col11:
                st.metric('<6 months', " %d%%"%(pred[0][0]*100), delta=None, delta_color='normal')
            with col22:
                st.metric('Btw 6-14 months', " %d%%" % (pred[0][1] * 100), delta=None, delta_color='normal')
            with col33:
                st.metric('Btw 14-24 months', " %d%%" % (pred[0][2] * 100), delta=None, delta_color='normal')
            with col44:
                st.metric('>24 months', " %d%%" % (pred[0][3] * 100), delta=None, delta_color='normal')
            my_bar.progress(40)
            df2=pd.read_csv('./df1.csv')
            shaps_values=e4(df2)
            st.subheader("Feature impact")
            my_bar.progress(70)
            st.pyplot(shap.plots.force(shaps_values[0],matplotlib=True,contribution_threshold=0.05))
            my_bar.progress(100)
