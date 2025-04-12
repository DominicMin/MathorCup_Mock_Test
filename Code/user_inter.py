import matplotlib.pyplot as plt
import pandas as pd
from prophet_prediction import predictions  

def display_menu(options, title = "Select"):
    print(title)
    for idx, option in enumerate(options, 1):
        print(f"{idx}. {option}")
    print("0. Back")
    return input("[INPUT]Enter option number (or 'q' to quit): ")

def plot_forecast(route, year_key):
    entry = predictions[route][year_key]
    if not entry:
        print("[ERROR]No valid prediction data available for this selection")
        return
    
    model = entry["model"]
    forecast = entry["forecast"]

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

def route_selection():
    routes = list(predictions.keys())
    while True:
        choice = display_menu(routes, "Available Routes")
        
        if choice.lower() == 'q':
            return False
        if choice == '0':
            return True
        
        try:
            idx = int(choice) - 1
            selected_route = routes[idx]
            year_selection(selected_route)
        except (ValueError, IndexError):
            print("[ERROR]Invalid input, please try again")

def year_selection(route):
    years = list(predictions[route].keys())
    while True:
        choice = display_menu(years, f"Select Data Year - {route}")
        
        if choice.lower() == 'q':
            return False
        if choice == '0':
            return True
        
        try:
            idx = int(choice) - 1
            selected_year = years[idx]
            plot_forecast(route, selected_year)
        except (ValueError, IndexError):
            print("[ERROR]Invalid input, please try again")

def main():
    while True:
        choice = input("\nMain Menu:\n1. View Forecast Charts\n2. Exit\n> ")
        
        if choice == '1':
            if not route_selection():
                break
        elif choice == '2' or choice.lower() == 'q':
            break
        else:
            print("[ERROR]Invalid selection, please try again")
    
    print("\n[INFO]System end.")

if __name__ == "__main__":
    main()