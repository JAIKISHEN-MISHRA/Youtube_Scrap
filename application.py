from selenium import webdriver
from selenium.webdriver.common.by import By
from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import pymongo

app = Flask(__name__)

@app.route("/", methods=['GET'])
@cross_origin()
def home_page():
    return render_template("index.html")

@app.route("/YouTube", methods=['POST', 'GET'])
@cross_origin()
def result():
    if request.method == 'POST':
        try:
            url = "https://www.youtube.com/@PW-Foundation/videos"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            }
            driver = webdriver.Chrome()
            driver.get(url)
            videos = driver.find_elements(By.CLASS_NAME, 'style-scope ytd-rich-grid-media')
            filename = "Youtube.csv"
            fw = open(filename, "w")
            headers = "Video Link, Thumbnail_Link, Video_Title, Video_Views, Video_Time \n"
            YouTube_Data = []  # Corrected the variable name
            for i in videos[:5]:
                try:
                    vid_link = i.find_element(By.XPATH, './/*[@id="video-title-link"]').get_attribute("href")
                except:
                    vid_link = "No Link"
                try:
                    vid_thumbnail = i.find_element(By.XPATH, './/*[@id="thumbnail"]').get_attribute("href")
                except:
                    vid_thumbnail = "No link"
                try:
                    vid_title = i.find_element(By.XPATH, './/*[@id="video-title"]').text
                except:
                    vid_title = "No title"
                try:
                    vid_views = i.find_element(By.XPATH, './/*[@id="metadata-line"]/span[1]').text
                except:
                    vid_views = "No views"
                try:
                    vid_time = i.find_element(By.XPATH, './/*[@id="metadata-line"]/span[2]').text
                except:
                    vid_time = "No time"
                myDict = {
                    "Video_link": vid_link,
                    "Thumbnail_Link": vid_thumbnail,
                    "Video_Title": vid_title,
                    "Video_view": vid_views,
                    "Video_Time": vid_time
                }
                YouTube_Data.append(myDict)  # Corrected the variable name

            # MongoDB connection and data insertion
            client = pymongo.MongoClient("mongodb+srv://Jaimishra20031:Jai31072003@jaicluster.xau2qru.mongodb.net/")  # Replace with your connection string
            db = client['Youtube_Scrap']
            Youtube_col = db['Youtube_Col']
            Youtube_col.insert_many(YouTube_Data)  # Corrected the variable name

            # Extracting and returning the selected data based on button value
            if request.form["button"] == "Video_Link":
                ans = [i["Video_link"] for i in YouTube_Data]
                return render_template('Result.html', ans=ans, title="Video_Link")
            elif request.form["button"] == "Thumbnail_Link":
                ans = [i["Thumbnail_Link"] for i in YouTube_Data]
                return render_template('Result.html', ans=ans, title="Thumbnail_Link")
            elif request.form["button"] == "Video_Title":
                ans = [i["Video_Title"] for i in YouTube_Data]
                return render_template('Result.html', ans=ans, title="Video_Title")
            elif request.form["button"] == "Video_Views":
                ans = [i["Video_view"] for i in YouTube_Data]
                return render_template('Result.html', ans=ans, title="Video_Views")
            elif request.form["button"] == "Video_Time":
                ans = [i["Video_Time"] for i in YouTube_Data]
                return render_template('Result.html', ans=ans, title="Video_Time")

        except Exception as e:
            print("The exception is:", e)
            return 'something is wrong'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
