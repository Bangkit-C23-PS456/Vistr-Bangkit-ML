from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import numpy as np
import pandas as pd

# Load the saved model
model_bal = load_model("model/temp_balikpapan.h5")
model_ber = load_model("model/temp_berau.h5")
model_bon = load_model("model/temp_bontang.h5")
model_kut = load_model("model/temp_kutai.h5")
model_pen = load_model("model/temp_penajam.h5")
model_sam = load_model("model/temp_samarinda.h5")

model_weather_bal = load_model("model/weather_balikpapan.h5")
model_weather_ber = load_model("model/weather_berau.h5")
model_weather_bon = load_model("model/weather_bontang.h5")
model_weather_kut = load_model("model/weather_kutai.h5")
model_weather_pen = load_model("model/weather_penajam.h5")
model_weather_sam = load_model("model/weather_samarinda.h5")

df_bal = pd.read_csv('data/balikpapan_weather.csv')
df_ber = pd.read_csv('data/berau_weather.csv')
df_bon = pd.read_csv('data/bontang_weather.csv')
df_kut = pd.read_csv('data/kutai_weather.csv')
df_pen = pd.read_csv('data/penajam_weather.csv')
df_sam = pd.read_csv('data/samarinda_weather.csv')


def predict_temperature(date, city):

    if city == 'Balikpapan':
      model = model_bal
      df = df_bal
    if city == 'Berau':
      model = model_ber
      df = df_ber
    if city == 'Bontang':
      model = model_bon
      df = df_bon
    if city == 'Kutai Kertanegara':
      model = model_kut
      df = df_kut
    if city == 'Penajam':
      model = model_pen
      df = df_pen
    if city == 'Samarinda':
      model = model_sam
      df = df_sam
      
    
    year, month, day = map(int, date.split('-'))

    # Tanggal yang akan diprediksi suhunya
    input_date = datetime(year, month, day)

    # Tentukan tanggal referensi
    reference_date = datetime(2015, 1, 1)

    # Hitung perbedaan hari antara tanggal input dan tanggal referensi
    delta_days = (input_date - reference_date).days

    data = df[['Date', 'Temp']]
    data = data.set_index('Date')
    # minmax scaler
    scaler = MinMaxScaler(feature_range = (0, 1))
    data = scaler.fit_transform(data)

    # Ubah perbedaan hari menjadi representasi numerik
    input_date_representation = scaler.transform([[delta_days]])[0]

    time_step = 100  # Set the appropriate value based on your problem and data characteristics

    # Buat input data untuk prediksi
    input_data = []
    for i in range(len(data) - time_step + 1, len(data)):
        input_data.append(data[i, 0])
    input_data.append(input_date_representation[0])

    # Konversi input data menjadi array NumPy
    input_data = np.array(input_data)

    # Reshape input data menjadi bentuk yang dapat diterima oleh model
    input_data = np.reshape(input_data, (1, time_step, 1))

    # Lakukan prediksi suhu
    predicted_temperature = model.predict(input_data)

    # Reshape predicted_temperature to have the expected dimensions
    predicted_temperature = np.reshape(predicted_temperature, (1, 1))

    # Apply inverse_transform to convert the predicted_temperature to the original scale
    predicted_temperature = scaler.inverse_transform(predicted_temperature)[0][0]

    return {
        'temp': predicted_temperature,
        'city': city,
        'date': date
    }
    
def predict_weather(date, city):

    if city == 'Balikpapan':
      model = model_weather_bal
      df = df_bal
    elif city == 'Berau':
      model = model_weather_ber
      df = df_ber
    elif city == 'Bontang':
      model = model_weather_bon
      df = df_bon
    elif city == 'Kutai Kertanegara':
      model = model_weather_kut
      df = df_kut
    elif city == 'Penajam':
      model = model_weather_pen
      df = df_pen
    elif city == 'Samarinda':
      model = model_weather_sam
      df = df_sam
    else:
      return {
          'message':'City not found'
      }
    
    # Extract the features and target variable
    data = df[['Date', 'Weather']]  # Select 'Date' and 'Weather' columns
    data = data.set_index('Date')

    # Create numerical labels for the categorical variable 'Weather'
    labels = data['Weather'].unique()

    year, month, day = map(int, date.split('-'))

    # Tanggal yang akan diprediksi suhunya
    input_date = datetime(year, month, day)

    # Tentukan tanggal referensi
    reference_date = datetime(2015, 1, 1)

    # Get the number of days since the reference date
    delta_days = (input_date - reference_date).days

    # Create a sequence of four consecutive delta days
    input_sequence = np.repeat(delta_days, 4)

    # Reshape the input data into the shape expected by the model
    input_data = input_sequence.reshape((1, 4, 1))

    # Predict the weather
    predicted_weather = model.predict(input_data)[0]

    # Get the index of the weather with the highest probability
    predicted_weather_index = np.argmax(predicted_weather)

    # Get the label of the weather corresponding to the index
    predicted_weather_label = labels[predicted_weather_index]

    return {
        'weather': predicted_weather_label,
        'city': city,
        'date': date
    }