#importing required modules
#sklearn and xgboost has to be installed but not imported
import streamlit as st
import pandas as pd
import numpy as np
import pickle

#header texts
st.markdown("<h1 style='text-align: center; color: #F1698B;'>AB InBev Maverick 2.0</h1>", unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; color: #F1698B;'>Team: Swift Snipers</h1>", unsafe_allow_html=True)

#instructions
st.header("Instructions:")
st.write("1. Input all the data.")
st.write("2. Click on 'Get Discount'.")
st.write("3. Wait a few seconds to get results.")

#input area
with st.form(key='my_form'):
    poc_id = st.text_input(label='Enter POC ID',key="1")
    city_tier = st.selectbox('City Tier',[0,1,2],key="2")
    
    #dividing the rest of the inputs into 2 columns to save space
    left_col1, right_col1 = st.beta_columns(2)
    with left_col1:
        poc_image = st.radio("POC Image",('Mainstream', 'Premium'),key="5")
        total_volume_2018 = st.number_input(label='Total Volume 2018',key="3")
        product_volume_2019 = st.number_input(label='Product Volume 2019',key="4")
        segment = st.selectbox('Segment',['Entertainment Led', 'Drink Led',
        'Institutional', 'Food Led', 'Wholesaler', 'Not applicable'],key="8")
        brand = st.selectbox('Brand',['JUPILER', 'PIEDBOEUF', 'DIEKIRCH', 'BELLE VUE', 'HOEGAARDEN', 'LEFFE', 'TRIPEL KARMELIET', 'GOOSE ISLAND', 'STELLA ARTOIS', 'CORONA', 'VIEUX TEMPS', 'SCOTCH CTS', 'PURE BLONDE', 'CUBANISTO', 'GINETTE', 'KWAK', 'BASS', 'KRUGER', "BECK'S", 'HORSE ALE',
        'GINDER-ALE', 'DEUS', 'SAFIR', 'BIRRA DEL BORGO'],key="10")
        pack_type = st.selectbox("Pack Type",['BOTTLE', 'BULK', 'KEG', 'CAN', 'PERFECTDRAFT'],key="15")
        
    with right_col1:
        returnability = st.radio("Returnability",('Returnable', 'Non-Returnable'),key="12")
        total_volume_2019 = st.number_input(label='Total Volume 2019',key="6")
        gross_turnover_2019 = st.number_input(label='Gross Turnover 2019',key="7")
        sub_segment = st.selectbox('Sub Segment',['Events', 'Party Place', 'Institutional', 'Bar', 'Restaurant', 'Sports Venue', 'Recreational', 'Beer bar', 'Hybrid', 'Quick Dining', 'Music Venue', 'Cocktail Bar', 'Wholesaler',
        'Local Bar', 'Sub Agent', 'Not applicable'],key="9")
        sub_brand = st.selectbox('Sub Brand',['JUPILER PILS', 'PIEDBOEUF TRIPLE', 'JUPILER 0,0', 'PIEDBOEUF BLONDE', 'PIEDBOEUF FONCEE', 'DIEKIRCH PILS', 'BELLE VUE EXTRA KRIEK', 'HOEGAARDEN ROSEE', 'HOEGAARDEN WHITE', 'FLAVOURED ALCOHOLIC', 'LEFFE BLONDE', 'TRIPEL KARMELIET', 'GOOSE ISLAND IPA', 'HOEGAARDEN ROSE 0,0', 'LEFFE BRUNE', 'LEFFE SANS ALCOOL/ALCOHOLVRIJ', 'STELLA ARTOIS REGULAR', 'BELLE VUE KRIEK CLASSIQUE', 'CORONA EXTRA', 'JUPILER BLUE', 'VIEUX TEMPS REGULAR', 'SCOTCH CTS', 'BELLE VUE GUEUZE', 'HOEG RADLER LEMON 0,0', 'PURE BLONDE REGULAR', 'CUBANISTO RUM', 'GINETTE LAGER', 'GINETTE FRUIT', 'GINETTE TRIPEL', 'KWAK', 'HOEGAARDEN JULIUS', 'LEFFE', 'LEFFE ROYALE', 'LEFFE RUBY', 'LEFFE TRIPLE', 'HOEGAARDEN BEATRIX', 'HOEGAARDEN YELLOW', 'BASS PALE ALE', 'KRUGER EXPORT', 'HOEGAARDEN 0,0', 'LEFFE RITUEL 9', 'HOEGAARDEN GRAND CRU', 'LEFFE ROYALE CASCADE IPA', 'GINETTE BLONDE', 'HOEGAARDEN FORBIDDEN FRUIT', ' HOEGAARDEN RADLER AGRUM 0,0', "BECK'S REGULAR", 'HORSE ALE', 'LEFFE RADIEUSE', 'GINETTE BLANCHE', 'DIEKIRCH XMAS BEER', 'GINDER-ALE', 'LEFF NECT', 'DIEKIRCH GRAND CRU', 'DEUS', 'SAFIR REGULAR', 'LEFFE MIXED', 'CUBANISTO PHENOMENAL', " GOOSE ISLAND HONKER'S ALE", 'LEFFE ROYALE IPA', 'BIRRA DEL BORGO CASTAGNALE', 'GOOS 312',
        'GOOSE ISLAND MIDWAY IPA', 'DIEKIRCH BRUIN', 'LEFFE ROYALE MAPUCHE'],key="11")
        tax = st.number_input(label='Tax',key="13")
    
    
    province = st.selectbox('Province',['Brussels Capital Region', 'Liège', 'Antwerp', 'Namur', 'Limburg', 'Hainaut', 'East Flanders', 'Flemish Brabant', 'West Flanders',
    'Luxembourg', 'Walloon Brabant'],key="14")

    submit_button = st.form_submit_button(label='Get Discount')

#st.form_submit_button returns True upon form submit
if submit_button:
    city_tier_dict = {
        0:1,
        1:2,
        2:4
    }
    #adding initial inputs
    inputs = [
        total_volume_2019, city_tier_dict.get(city_tier), 
        product_volume_2019, gross_turnover_2019-tax
    ]
    inputs.append(1) if poc_image == 'Premium' else inputs.append(0) #adding premium
    
    #adding segments
    segment_dict = {
        'Entertainment Led': 0, 
        'Food Led': 0,
        'Institutional': 0, 
        'Not applicable': 0,
        'Wholesaler': 0
    }
    if(segment!='Drink Led'):
        for key in segment_dict.keys():
            if(key==segment):
                segment_dict[key]=1
    inputs.extend(segment_dict.values())
    
    #adding pack types
    pack_type_dict = {
        'BULK': 0,
        'CAN': 0,
        'KEG': 0,
        'PERFECTDRAFT': 0,
    }
    if(pack_type!='BOTTLE'):
        for key in pack_type_dict.keys():
            if(key==pack_type):
                pack_type_dict[key]=1
    inputs.extend(pack_type_dict.values())


    inputs.append(1) if returnability == 'Returnable' else inputs.append(0) #adding returnable

    #adding sub segments
    sub_segment_dict = {
        'Bar': 0,
        'Hybrid': 0,
        'Beer bar': 0,
        'Restaurant': 0,
        'Institutional': 0,
        'Sports Venue': 0
    }

    for key in sub_segment_dict.keys():
        if(key==sub_segment):
            sub_segment_dict[key]=1
    inputs.extend(sub_segment_dict.values())

    #adding brands
    brand_dict = {
        'LEFFE': 0,
        'JUPILER': 0,
        'HOEGAARDEN': 0,
        'TRIPEL KARMELIET': 0,
        'BELLE VUE': 0,
        'STELLA ARTOIS': 0,
    }

    for key in brand_dict.keys():
        if(key==brand):
            brand_dict[key]=1
    inputs.extend(brand_dict.values())

    #adding sub_brands
    sub_brand_dict = {
        'JUPILER PILS': 0,
        'LEFFE BLONDE': 0,
        'HOEGAARDEN WHITE': 0,
        'JUPILER 0,0': 0,
        'LEFFE BRUNE': 0,
        'TRIPEL KARMELIET': 0,
        'STELLA ARTOIS REGULAR': 0,
        'HOEGAARDEN ROSEE': 0,
    }

    for key in sub_brand_dict.keys():
        if(key==sub_brand):
            sub_brand_dict[key]=1
    inputs.extend(sub_brand_dict.values())

    #adding provinces
    province_dict = {
        'West Flanders': 0,
        'Brussels Capital Region': 0,
        'Liège': 0,
        'Flemish Brabant': 0,
        'East Flanders': 0,
        'Hainaut': 0,
        'Antwerp': 0,
        'Limburg': 0,
        'Namur': 0
    }

    for key in province_dict.keys():
        if(key==province):
            province_dict[key]=1
    inputs.extend(province_dict.values())
    inputs.append(total_volume_2019-total_volume_2018) #adding YoY growth amount
    
    #loading the 4 models
    with open('./pickle_files/hypertuned_rf_regressor_total_discount.pickle','rb') as modelFile:
        tdr_model = pickle.load(modelFile) #total discount regression model
    with open('./pickle_files/hypertuned_rf_regressor_on_invoice_discount.pickle','rb') as modelFile:
        odr_model = pickle.load(modelFile) #on invoice discount regression model
    with open('./pickle_files/hypertuned_xgb_classify_total_discount.pickle','rb') as modelFile:
        tdc_model = pickle.load(modelFile) #total discount classification model
    with open('./pickle_files/hypertuned_xgb_classify_on_invoice_discount.pickle','rb') as modelFile:
        odc_model = pickle.load(modelFile) #on invoice discount classification model

    cols = tdc_model.get_booster().feature_names #getting column names
    inputs_df = pd.DataFrame([inputs],columns=cols) #creating a dataframe of the inputs

    #predicting the discounts using the models
    tdr_prediction = tdr_model.predict(inputs_df)
    odr_prediction = odr_model.predict(inputs_df)
    tdc_prediction = tdc_model.predict(inputs_df)
    odc_prediction = odc_model.predict(inputs_df)

    #printing the output
    st.title("Results:") 
    if(tdc_prediction): #total discount is non-zero
        st.write("- POC ID: ", poc_id," should be getting a total discount of: ", round(tdr_prediction[0],2),".")
        st.write("- They should be getting an on-invoice discount of: ", round(odr_prediction[0],2),".")
        st.write("- And an off-invoice discount of", round(tdr_prediction[0]-odr_prediction[0],2),".")

        st.subheader("Further Info")
        st.write("- Total Discount Percentage is: ",round((tdr_prediction[0]/(gross_turnover_2019-tax))*100,2), "%")
        if(total_volume_2018!=0):
            st.write("- The YoY growth is: ",(((total_volume_2019-total_volume_2018)/(total_volume_2018))*100), "%")
    else: #total discount is zero
        st.write("- POC ID: ", poc_id," should be getting no discount.")



