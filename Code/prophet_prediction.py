import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from data_proc import new

'''
This program uses the Prophet algorithm (which forecasts time-dependent sequences) to predict the freight volume of a specific route in 2023.

Algorithm principle:
    y(t) = g(t) + s(t) + h(t) + epsilon(t)

y(t): outcome
g(t): growth trend
s(t): seasonality trend
h(t): holidays effects
epsilon(t): errors

Noted that the data from 2021 was significantly affected by the pandemic, making it less representative and resulting in larger error terms.
Using data from 2021 and combined data of 2021 and 2022 for prediction can easily lead to unrealistic results, 
as the model may learn incorrect patterns.
It is better to use the prediction results based on 2022 data alone.
'''

#remove outliers
def outlier_filter(df):
    q1 = df['y'].quantile(0.25)
    q3 = df['y'].quantile(0.75)
    IQR = q3 - q1
    lower_bound = q1 - 1.5 * IQR
    upper_bound = q3 + 1.5 * IQR
    return df[(df['y'] >= lower_bound) & (df['y'] <= upper_bound)]

#generate legal data format for prediction
def data_selection(sfrom, sto, year):
    #Select and format data for specific route and year
    specific_routes = new[
        (new["site_from"] == sfrom) & 
        (new["site_to"] == sto) & 
        (new["date_code"] // 1000 == year)
    ]
    
    #process data format
    specific_routes = specific_routes.drop(["site_from", "site_to"], axis = 1)
    specific_routes["date_code"] = pd.to_datetime(
        specific_routes["date_code"].astype(str), 
        format = '%Y%j'
    )
    specific_routes.rename(
        columns = {"date_code": "ds", "shipment_volume": "y"}, 
        inplace = True
    )

    return specific_routes

#initialization
predictions = {
    "DC14-DC10": {2021: {}, 2022: {}, "Both Years": {}},       
    "DC20-DC35": {2021: {}, 2022: {}, "Both Years": {}},
    "DC25-DC62": {2021: {}, 2022: {}, "Both Years": {}},
}

#train model and make predictions
for route in predictions:
    sites = route.split('-')
    sfrom, sto = sites[0], sites[1]
    
    for year_key in predictions[route]:
        if year_key != "Both Years":
            data = data_selection(sfrom, sto, year_key)
        else:
            df1 = data_selection(sfrom, sto, 2021)
            df2 = data_selection(sfrom, sto, 2022)
            data = pd.concat([df1, df2], ignore_index = True)
        
        #remove outlier
        data = outlier_filter(data)
        
        #model construction
        model = Prophet(
            growth = "flat",
            seasonality_mode = "multiplicative",
            changepoint_prior_scale = 0.001, 
            seasonality_prior_scale = 15, 
            yearly_seasonality = 12, 
            holidays_prior_scale = 10,              
        )
        
        #traditional holidays and custom holidays
        model.add_country_holidays(country_name = "CN")
        promotion_dates = [
            "2021-06-18", "2021-11-11", "2021-12-12",
            "2022-06-18", "2022-11-11", "2022-12-12",
            "2023-06-18", "2023-11-11", "2023-12-12",
        ]
        custom_holidays = pd.DataFrame({
            "holiday": 'promotion',
            "ds": pd.to_datetime(promotion_dates),
            "lower_window": -5,
            "upper_window": 10
        })
        model.holidays = pd.concat([model.holidays, custom_holidays])
        
        #set seasonality
        model.add_seasonality(
            name = "quarter",
            period = 91.25,
            fourier_order = 10,
            prior_scale = 15
        )
        model.fit(data)
        
        #predictions generation
        future = model.make_future_dataframe(periods = 365)
        forecast = model.predict(future)
        forecast[['yhat', 'yhat_lower', 'yhat_upper']] = forecast[['yhat', 'yhat_lower', 'yhat_upper']].clip(lower = 0)

        #store results
        predictions[route][year_key] = {
            "model": model,
            "forecast": forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(365)
        }

'''
Chart explanation:
Black dots: Observed values (actual values)
Light blue shaded area: Uncertainly interval
Dark blue line: Predicted/Forecast values (median value of uncertainly interval)
'''

if __name__ == "__main__":
    #result visualization
    for route in predictions:
        for year_key in predictions[route]:
            #escape empty records
            if not predictions[route][year_key]:
                continue
                
            #get results
            model = predictions[route][year_key]["model"]
            forecast = predictions[route][year_key]["forecast"]
            
            #generate graphs
            fig = model.plot(forecast)
            
            current_ax = plt.gca()

            forecast_start = forecast['ds'].max() - pd.DateOffset(days = 365)
            current_ax.axvline(x = forecast_start, color = 'purple', 
                                linestyle = '--', alpha = 0.7, label = 'Forecast Start')
            
            plt.title(f"{route} Volume Prediction ({year_key} Basis)")
            plt.xlabel("Date")
            plt.ylabel("Shipment Volume")
            plt.legend()
            plt.show()