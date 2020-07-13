from bs4 import BeautifulSoup as bs
import requests
import argparse

USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
# US english
LANGUAGE = "en-US,en;q=0.5"

def get_weather_data(url):
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html = session.get(url)
    # create a new soup
    soup = bs(html.text, "html.parser")
    
    #store all results on this dictionary
    result = {}
    # extract region
    result['region'] = soup.find("div", attrs={"id": "wob_loc"}).text
    # extract temperature now
    result['temp_now'] = soup.find("span", attrs={"id": "wob_tm"}).text
    # get the day and hour now
    result['dayhour'] = soup.find("div", attrs={"id": "wob_dts"}).text
    # get the actual weather
    result['weather_now'] = soup.find("span", attrs={"id": "wob_dc"}).text
    # get the precipitation
    result['precipitation'] = soup.find("span", attrs={"id": "wob_pp"}).text
    # get the % of humidity
    result['humidity'] = soup.find("span", attrs={"id": "wob_hm"}).text
    # extract the wind
    result['wind'] = soup.find("span", attrs={"id": "wob_ws"}).text

    print("Nama Kota : " + result['region'])
    print("Temperature "+ result['temp_now']+" Celcius")
    print("Waktu : " + result['dayhour'])
    print("Cuaca saat ini : " + result['weather_now'])
    print("Pengedapan : " + result['precipitation'])
    print("Kelembaban : " + result['humidity'])
    print("Kekuatan Angin : " + result['wind'])
    option = input("Info mengenai cuaca dalam seminggu (Y/n) : ")
    print("")
    
    if option == 'Y' or option == 'Yes' or option == 'yes':
        # get next few days' weather
        next_days = []
        days = soup.find("div", attrs={"id": "wob_dp"})
        for day in days.findAll("div", attrs={"class": "wob_df"}):
            # extract the name of the day
            day_name = day.find("div", attrs={"class": "vk_lgy"}).attrs['aria-label']
            # get weather status for that day
            weather = day.find("img").attrs["alt"]
            temp = day.findAll("span", {"class": "wob_t"})
            # maximum temparature in Celsius, use temp[1].text if you want fahrenheit
            max_temp = temp[0].text
            # minimum temparature in Celsius, use temp[3].text if you want fahrenheit
            # min_temp = temp[2].text
            # next_days.append({"name": day_name, "weather": weather, "max_temp": max_temp, "min_temp": min_temp})
            
            print("Nama Hari : " + day_name)
            print("Cuaca : " + weather)
            print("Temperature : " + max_temp + " Celcius\n")


if __name__ == "__main__":
    URL1 = "https://www.google.com/search?q=cuaca+"
    nama_kota=["Jakarta", "Bogor", "Depok", "Tangerang", "Bekasi"]
    parser = argparse.ArgumentParser("Python program to check current weather in few days on the current city")
    for kota in nama_kota:
        URL = URL1+kota
        data = get_weather_data(URL)
    
    