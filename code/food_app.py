from pathlib import Path
import datetime

import pandas as pd
import streamlit as st

import main
import predict


def get_user_input(df_train):
    # Order Information Section
    st.markdown("### 🛒 Order Related Information")
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("📅 Order Date", help="Select the date when order was placed")
    with col2:
        order_time = st.text_input("🕐 Order Time ", 
                                  placeholder="Enter time (e.g. 14:30)",
                                  help="Enter the time when order was placed")
    
    # Validate time format
    try:
        order_time = datetime.datetime.strptime(order_time, '%H:%M').time()
    except:
        if order_time:  # Only show error if user has entered something
            st.error("Please enter time in HH:MM format (e.g. 14:30)")
            return
        order_time = datetime.datetime.now().time()
    
    order_datetime = datetime.datetime.combine(date, order_time)
    
    col3, col4 = st.columns(2)
    with col3:
        pickup_time = st.text_input("🕑 Order Pickup Time ", 
                                  placeholder="Enter time (e.g. 14:45)",
                                  help="Enter the time when order was picked up")
        try:
            pickup_time = datetime.datetime.strptime(pickup_time, '%H:%M').time()
        except:
            if pickup_time:  # Only show error if user has entered something
                st.error("Please enter time in HH:MM format (e.g. 14:45)")
                return
            pickup_time = (datetime.datetime.now() + datetime.timedelta(minutes=15)).time()
    with col4:
        order_type = st.selectbox('🍕 Type of Order',
                                  df_train['Type_of_order'].unique())
    
    multiple_deliveries = st.selectbox('📦 Combined Deliveries',
                                       sorted(df_train['multiple_deliveries'].unique().astype('int')),
                                       help="Number of deliveries combined together")
    
    st.markdown("")
    
    # Location Information Section
    st.markdown("### 📍 Location Related Information")
    st.markdown("---")
    
    col5, col6 = st.columns(2)
    with col5:
        st.markdown("**🏪 Restaurant Location**")
        restaurant_latitude = st.text_input("Latitude", "14.829222", key="rest_lat")
        restaurant_longitude = st.text_input("Longitude", "67.920922", key="rest_long")
    
    with col6:
        st.markdown("**🏠 Delivery Location**")
        delivery_location_latitude = st.text_input("Latitude", "14.929222", key="del_lat")
        delivery_location_longitude = st.text_input("Longitude", "68.860922", key="del_long")
    
    st.markdown("")
    
    # Delivery Person Information Section
    st.markdown("### 🚴 Delivery Person Related Information")
    st.markdown("---")
    
    col7, col8 = st.columns(2)
    with col7:
        delivery_person_age = st.slider("👤 Age",
                                        int(df_train['Delivery_person_Age'].min()),
                                        int(df_train['Delivery_person_Age'].max()),
                                        int(df_train['Delivery_person_Age'].mean()))
    with col8:
        delivery_person_rating = st.slider("⭐ Rating",
                                           float(df_train['Delivery_person_Ratings'].min()),
                                           float(df_train['Delivery_person_Ratings'].max()),
                                           float(df_train['Delivery_person_Ratings'].mean()),
                                           format="%.1f")
    
    col9, col10 = st.columns(2)
    with col9:
        vehicle = st.selectbox('🛵 Vehicle Type',
                               df_train['Type_of_vehicle'].unique())
    with col10:
        vehicle_condition = st.selectbox('🔧 Vehicle Condition',
                                         sorted(df_train['Vehicle_condition'].unique()))
    
    st.markdown("")
    
    # City Information Section
    st.markdown("### 🏙️ City Related Information")
    st.markdown("---")
    
    col11, col12 = st.columns(2)
    with col11:
        city_code = st.selectbox('🏛️ City Name',
                                 df_train['City_code'].unique())
    with col12:
        city = st.selectbox('🌆 City Type',
                            df_train['City'].unique())
    
    st.markdown("")
    
    # Weather and Event Information Section
    st.markdown("### 🌤️ Weather Conditions & Event Information")
    st.markdown("---")
    
    col13, col14, col15 = st.columns(3)
    with col13:
        road_density = st.selectbox('🚦 Traffic Density',
                                    df_train['Road_traffic_density'].unique())
    with col14:
        weather_conditions = st.selectbox('☁️ Weather',
                                          df_train['Weather_conditions'].unique())
    with col15:
        festival = st.selectbox('🎉 Festival',
                                df_train['Festival'].unique())

    X = pd.DataFrame({
        'ID': '123456',
        'Delivery_person_ID': city_code + 'RES13DEL02',
        'Delivery_person_Age': delivery_person_age,
        'Delivery_person_Ratings': delivery_person_rating,
        'Restaurant_latitude': format(float(restaurant_latitude), ".6f"),
        'Restaurant_longitude': format(float(restaurant_longitude), ".6f"),
        'Delivery_location_latitude': format(float(delivery_location_latitude), ".6f"),
        'Delivery_location_longitude': format(float(delivery_location_longitude), ".6f"),
        'Order_Date': date.strftime('%d-%m-%Y'),
        'Time_Orderd': order_time.strftime('%H:%M:%S'),
        'Time_Order_picked': pickup_time.strftime('%H:%M:%S'),
        'Weatherconditions': 'conditions ' + weather_conditions,
        'Road_traffic_density': road_density,
        'Vehicle_condition': vehicle_condition,
        'Type_of_order': order_type,
        'Type_of_vehicle': vehicle,
        'multiple_deliveries': multiple_deliveries,
        'Festival': festival,
        'City': city
    }, index=[0])
    return X


if __name__ == "__main__":
    st.set_page_config(
        page_title="Food Delivery Time Prediction", 
        page_icon="🍔", 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Custom CSS for beautiful styling with modern professional colors
    st.markdown("""
        <style>
        .main {
            background:#8ABEB9
        }
        .stApp {
            background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
        }
        h1 {
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            padding: 25px;
            background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            font-weight: 700;
            letter-spacing: 1px;
            margin-bottom: 30px;
            border: 2px solid #81c784;
        }
        h3 {
            color: white;
            font-weight: 700;
            padding: 10px;
            background: #000000;
            border-radius: 8px;
        }
        .stTextInput>div>div>input {
            background-color: #EFECE3;
            color: #1a1a1a;
        }
        .stSelectbox>div>div>div {
            background-color: #EFECE3;
            color: #1a1a1a;
        }
        .stSlider>div>div {
            background-color: #EFECE3;
            border-radius: 10px;
            padding: 10px;
        }
        label {
            color: white !important;
            font-weight: 600 !important;
            background: rgba(27, 94, 32, 0.8);
            padding: 4px 8px;
            border-radius: 4px;
        }
        p {
            color: white !important;
            background: rgba(27, 94, 32, 0.8);
            padding: 4px 8px;
            border-radius: 4px;
        }
        .stButton>button {
            width: 100%;
            background: linear-gradient(135deg, #388e3c 0%, #2e7d32 100%);
            color: white;
            font-size: 22px;
            font-weight: bold;
            padding: 18px;
            border-radius: 12px;
            border: none;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%);
            box-shadow: 0 6px 8px rgba(0, 0, 0, 0.4);
        }
        .result-card {
            background: rgba(46, 125, 50, 0.9);
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            margin: 15px 0;
            border-left: 5px solid #81c784;
            color: white;
        }
        .metric-card {
            background: rgba(46, 125, 50, 0.9);
            padding: 20px;
            border-radius: 10px;
            color: white;
            text-align: center;
            margin: 10px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        .success-box {
            background: rgba(46, 125, 50, 0.95);
            padding: 25px;
            border-radius: 10px;
            color: white;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            margin: 20px 0;
        }
        div[data-testid="stMarkdownContainer"] > p {
            background: transparent;
            color: white !important;
        }
        .stMarkdown a {
            color: #81c784 !important;
        }
        div.stMetric {
            background: rgba(46, 125, 50, 0.9);
            padding: 15px;
            border-radius: 10px;
            color: white;
        }
        div.stMetric label {
            color: #a5d6a7 !important;
        }
        .metric-value {
            color: white !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Read in training data
    df_train = pd.read_csv(str(Path(__file__).parents[1] / 'data/train.csv'))
    main.cleaning_steps(df_train)

    # Beautiful header
    st.markdown("<h1>🍔 Food Delivery Time Prediction 🚀</h1>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    # Get user input from main screen
    input_df = get_user_input(df_train)
    
    st.markdown("<br>", unsafe_allow_html=True)

    # Beautiful button with spacing
    col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
    with col_btn2:
        calculate_button = st.button("🚀 Calculate Delivery Time", type="primary")

    if calculate_button:
        order_date = input_df['Order_Date'][0]
        order_time = input_df['Time_Orderd'][0]
        order_date_time = datetime.datetime.strptime(f'{order_date} {order_time}', '%d-%m-%Y %H:%M:%S')
        order_pickup_time = input_df['Time_Order_picked'][0]
        order_pickup_date_time = datetime.datetime.strptime(f'{order_date} {order_pickup_time}', '%d-%m-%Y %H:%M:%S')

        total_delivery_minutes = round(predict.predict(input_df)[0], 2)
        minutes = int(total_delivery_minutes)
        seconds = int((total_delivery_minutes - minutes) * 60)
        X = order_pickup_date_time + datetime.timedelta(minutes=minutes, seconds=seconds)

        # Beautiful success message
        st.markdown("""
            <div class="success-box">
                <h2>✅ Prediction Complete!</h2>
                <p style="font-size: 18px;">Your delivery time has been calculated successfully</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Results in beautiful cards
        col_result1, col_result2 = st.columns(2)
        
        with col_result1:
            st.markdown("""
                <div class="result-card">
                    <h3>📋 Order Details</h3>
                    <hr>
                </div>
            """, unsafe_allow_html=True)
            st.markdown(f"**🕐 Order Placed:** `{order_date_time.strftime('%d %B %Y, %I:%M %p')}`")
            st.markdown(f"**📦 Order Picked Up:** `{order_pickup_date_time.strftime('%d %B %Y, %I:%M %p')}`")
        
        with col_result2:
            st.markdown("""
                <div class="result-card">
                    <h3>⏱️ Delivery Prediction</h3>
                    <hr>
                </div>
            """, unsafe_allow_html=True)
            formatted_X = "{:.2f}".format(total_delivery_minutes)
            st.markdown(f"**⏰ Total Delivery Time:** `{formatted_X} minutes`")
            st.markdown(f"**🎯 Estimated Arrival:** `{X.strftime('%d %B %Y, %I:%M %p')}`")
        
        # Big metric display
        st.markdown("<br>", unsafe_allow_html=True)
        col_metric1, col_metric2, col_metric3 = st.columns(3)
        
        with col_metric1:
            st.metric(label="⏱️ Delivery Time", value=f"{formatted_X} min", delta="Predicted")
        
        with col_metric2:
            delivery_speed = "🚀 Fast" if total_delivery_minutes < 30 else "🚗 Normal" if total_delivery_minutes <= 45 else "🐢 Slow"
            st.metric(label="📊 Delivery Speed", value=delivery_speed)
        
        with col_metric3:
            st.metric(label="🎯 Arrival Time", value=X.strftime('%I:%M %p'))