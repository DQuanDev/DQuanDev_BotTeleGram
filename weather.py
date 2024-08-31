import telebot
import requests

API_TOKEN = '7381890411:AAEsOjqGXsz3IcAz5cK18vsjKluGgnTB04g'
WEATHER_API_URL = "https://nguyenmanh.name.vn/api/weather"
API_KEY = "w9U34lRM"

bot = telebot.TeleBot(API_TOKEN)

def fetch_weather_data(location):
    """Fetch weather data from the API."""
    try:
        response = requests.get(f"{WEATHER_API_URL}?city={location}&apikey={API_KEY}")
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.RequestException as e:
        return {"error": str(e)}

def format_weather_message(weather_data):
    """Format weather data into a message with icons at the beginning."""
    if 'error' in weather_data:
        return f"🌦️ Không thể lấy thông tin thời tiết: {weather_data['error']}"

    if weather_data.get('status') != 200:
        return "🌦️ Không thể lấy thông tin thời tiết. Vui lòng thử lại sau."

    weather_info = weather_data['result']
    city = weather_info['name']
    temp = weather_info['main']['temp']
    description = weather_info['weather'][0]['description']
    humidity = weather_info['main']['humidity']
    wind_speed = weather_info['wind']['speed']

    return f"""
*🌍 Thời tiết tại: {city}*
*🌡️ Nhiệt độ*: {temp}°C
*☁️ Mô tả*: {description}
*💧 Độ ẩm*: {humidity}%
*🌬️ Tốc độ gió*: {wind_speed} m/s
"""

@bot.message_handler(commands=['weather'])
def send_weather(message):
    """Handle the /weather command."""
    try:
        location = message.text.split('/weather ', 1)[1].strip()
        if not location:
            raise IndexError
        weather_data = fetch_weather_data(location)
        weather_message = format_weather_message(weather_data)
        bot.reply_to(message, weather_message, parse_mode='Markdown')
    except IndexError:
        bot.reply_to(message, "⚠️ Vui lòng cung cấp vị trí. Ví dụ: /weather Hanoi")
    except Exception as e:
        bot.reply_to(message, f"❗ Có lỗi xảy ra: {str(e)}")

if __name__ == '__main__':
    bot.polling(none_stop=True)

from replit import db
