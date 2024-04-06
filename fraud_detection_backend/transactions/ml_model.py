import math
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from datetime import timedelta, datetime
from time import strftime, localtime

def predict_fraud():
    # Read the CSV file into a DataFrame
    df = pd.read_csv("data.csv")

    # Preprocessing steps
    df['international'] = df['international'].apply(lambda x: 1 if x else 0)
    datetime_list = df["dateTimeTransaction"].tolist()
    datetime_updated = []
    for epoch_time in datetime_list:
        datetime_updated.append(datetime.strptime(strftime('%Y-%m-%d', localtime(int(float(epoch_time)))), '%Y-%m-%d'))

    df["dateTimeTransaction"] = datetime_updated
    # df['dateTimeTransaction'] = pd.to_datetime(df['dateTimeTransaction'], unit='s').dt.strftime('%Y-%m-%d')

    # Define rules list to store detected rules
    rules = []

    conditions = [
        ((df['merchantCategoryCode'] >= 1) & (df['merchantCategoryCode'] <= 1499)),
        ((df['merchantCategoryCode'] > 1500) & (df['merchantCategoryCode'] <= 2999)),
        ((df['merchantCategoryCode'] > 3000) & (df['merchantCategoryCode'] <= 3299)),
        ((df['merchantCategoryCode'] > 3300) & (df['merchantCategoryCode'] <= 3499)),
        ((df['merchantCategoryCode'] > 3500) & (df['merchantCategoryCode'] <= 3999)),
        ((df['merchantCategoryCode'] > 4000) & (df['merchantCategoryCode'] <= 4799)),
        ((df['merchantCategoryCode'] >= 4800) & (df['merchantCategoryCode'] <= 4999)),
        ((df['merchantCategoryCode'] > 5000) & (df['merchantCategoryCode'] <= 5999)),
        ((df['merchantCategoryCode'] > 5600) & (df['merchantCategoryCode'] <= 5699)),
        ((df['merchantCategoryCode'] >= 5700) & (df['merchantCategoryCode'] <= 7299)),
        ((df['merchantCategoryCode'] > 7300) & (df['merchantCategoryCode'] <= 7999)),
        ((df['merchantCategoryCode'] > 8000) & (df['merchantCategoryCode'] <= 8999)),
        ((df['merchantCategoryCode'] > 9000) & (df['merchantCategoryCode'] <= 9999))
    ]

    values = [
        'Agriculture', 'Contracted Services', 'Airlines', 'Car Rental', 'Lodging', 'Transportation Services', 
        'Utility Services', 'Retail Outlet Services', 'Clothing Stores', 'Miscellaneous Stores', 
        'Business Services', 'Professional Services and Membership Organizations', 'Government Services'
    ]
    
    df['merchantCategory'] = np.select(conditions, values, default='Other')

    encoding_dict = {value: '{:0{width}b}'.format(index, width=len(values)) for index, value in enumerate(values)}
    df['merchantCategory_encoded'] = df['merchantCategory'].map(encoding_dict)

    df['dateTimeTransaction'] = pd.to_datetime(df['dateTimeTransaction'])
    dateTimeTransaction = df['dateTimeTransaction'].max()

    data_to_predict_on = df[df["dateTimeTransaction"]==dateTimeTransaction]
    df = df[df["dateTimeTransaction"]!=dateTimeTransaction]

    cardBalance = data_to_predict_on["cardBalance"]

    min_date_last_12hours = dateTimeTransaction - timedelta(hours=12)
    min_date_last_1day = dateTimeTransaction - timedelta(days=1)
    min_date_last_3day = dateTimeTransaction - timedelta(days=3)
    min_date_last_7day = dateTimeTransaction - timedelta(days=7)
    min_date_last_30day = dateTimeTransaction - timedelta(days=7)

    max_date = dateTimeTransaction

    filtered_df_last_12hour = df[(df['dateTimeTransaction'] >= min_date_last_12hours) & (df['dateTimeTransaction'] <= dateTimeTransaction)]
    filtered_df_last_1day = df[(df['dateTimeTransaction'] >= min_date_last_1day) & (df['dateTimeTransaction'] <= dateTimeTransaction)]
    filtered_df_last_3day = df[(df['dateTimeTransaction'] >= min_date_last_3day) & (df['dateTimeTransaction'] <= dateTimeTransaction)]
    filtered_df_last_7day = df[(df['dateTimeTransaction'] >= min_date_last_7day) & (df['dateTimeTransaction'] <= dateTimeTransaction)]
    filtered_df_last_30day = df[(df['dateTimeTransaction'] >= min_date_last_30day) & (df['dateTimeTransaction'] <= dateTimeTransaction)]

    last_12_transaction_amount = filtered_df_last_12hour['transactionAmount'].sum()
    last_12_location_list = list(zip(filtered_df_last_12hour['latitude'], filtered_df_last_12hour['longitude']))

    if (data_to_predict_on["cardBalance"] > 300000).any():
        if (last_12_transaction_amount / data_to_predict_on["cardBalance"].iloc[0]) >= 0.7:
            print("RULE-001")
            rules.append("RULE-001")

    def haversine(lat1, lon1, lat2, lon2):
        """
        Calculate the great circle distance between two points
        on the earth (specified in decimal degrees)
        """
        lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat/2)*2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)*2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = 6371 * c
        return distance

    def is_within_radius(new_lat, new_lon, existing_coords, radius):
        """
        Check if the new location is within the specified radius
        of any existing coordinates.
        """
        for existing_lat, existing_lon in existing_coords:
            distance = haversine(new_lat, new_lon, existing_lat, existing_lon)
            if distance <= radius:
                return True
        return False

    count = 0

    existing_coords = last_12_location_list

    def check_within_radius(existing_coords, radius):
        """
        Check if all pairs of existing coordinates are within the specified radius of each other.
        """
        for i, (lat1, lon1) in enumerate(existing_coords):
            for j, (lat2, lon2) in enumerate(existing_coords):
                if i != j:
                    distance = haversine(lat1, lon1, lat2, lon2)
                    if distance > radius:
                        count+=1

    radius = 200
    check_within_radius(existing_coords, radius)

    if(last_12_transaction_amount > 100000):
        if(count>=5):
            rules.append("RULE-002")

    data_to_predict_on_coherent_pattern = data_to_predict_on[["cardBalance", "cardAcceptorId", "cardAcceptorTerminalId", "transactionCurrencyCode", "transactionAmount", "international", "merchantCategory_encoded"]]

    if not filtered_df_last_12hour.empty:
        df = filtered_df_last_12hour[["cardBalance", "cardAcceptorId", "cardAcceptorTerminalId", "transactionCurrencyCode", "transactionAmount", "international", "merchantCategory_encoded"]]
        clf_last_12hour = IsolationForest(contamination=0.15, random_state=42)
        clf_last_12hour.fit(df)
        y_pred_12hour = clf_last_12hour.predict(data_to_predict_on_coherent_pattern)
        if y_pred_12hour[0] != 1:
            rules.append("RULE-003 last 12 hours")

    if not filtered_df_last_1day.empty:
        df = filtered_df_last_1day[["cardBalance", "cardAcceptorId", "cardAcceptorTerminalId", "transactionCurrencyCode", "transactionAmount", "international", "merchantCategory_encoded"]]
        clf_last_1day = IsolationForest(contamination=0.15, random_state=42)
        clf_last_1day.fit(df)
        y_pred_1day = clf_last_1day.predict(data_to_predict_on_coherent_pattern)
        if y_pred_1day[0] != 1:
            rules.append("RULE-003 last 1 day")

    if not filtered_df_last_7day.empty:
        df = filtered_df_last_7day[["cardBalance", "cardAcceptorId", "cardAcceptorTerminalId", "transactionCurrencyCode", "transactionAmount", "international", "merchantCategory_encoded"]]
        clf_last_7day = IsolationForest(contamination=0.15, random_state=42)
        clf_last_7day.fit(df)
        y_pred_7day = clf_last_7day.predict(data_to_predict_on_coherent_pattern)
        if y_pred_7day[0] != 1:
            rules.append("RULE-003 last 7 day")

    data_to_predict_on_mcc = data_to_predict_on[["merchantCategoryCode", "merchantCategory_encoded"]]

    if not filtered_df_last_3day.empty:
        df = filtered_df_last_3day[["merchantCategoryCode", "merchantCategory_encoded"]]
        clf_last_3day = IsolationForest(contamination=0.15, random_state=42)
        clf_last_3day.fit(df)
        y_pred_3day = clf_last_3day.predict(data_to_predict_on_mcc)
        if y_pred_3day[0] != 1:
            rules.append("RULE-004 last 3 day")

    if not filtered_df_last_7day.empty:
        df = filtered_df_last_7day[["merchantCategoryCode", "merchantCategory_encoded"]]
        clf_last_7day = IsolationForest(contamination=0.15, random_state=42)
        clf_last_7day.fit(df)
        y_pred_7day = clf_last_7day.predict(data_to_predict_on_mcc)
        if y_pred_7day[0] != 1:
            rules.append("RULE-004 last 7 day")

    if not filtered_df_last_30day.empty:
        df = filtered_df_last_30day[["merchantCategoryCode", "merchantCategory_encoded"]]
        clf_last_30day = IsolationForest(contamination=0.15, random_state=42)
        clf_last_30day.fit(df)
        y_pred_30day = clf_last_30day.predict(data_to_predict_on_mcc)
        if y_pred_30day[0] != 1:
            rules.append("RULE-004 last 30 day")
    return rules