from flask import Flask, render_template
import random
app = Flask(__name__)

# list of cat images
images = [
"https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/dog-puppy-on-garden-royalty-free-image-1586966191.jpg",
"https://cdn.vox-cdn.com/thumbor/BxuxxhuJ3sdJjC8bWFl9ODJHKDk=/0x0:4608x3456/1400x1400/filters:focal(0x0:4608x3456):format(jpeg)/cdn.vox-cdn.com/uploads/chorus_image/image/46064224/8409370600_b4610104d6_o.0.0.jpg",
"https://komonews.com/resources/media2/16x9/full/1015/center/80/f05ff5c9-11fe-4998-af57-5ced74c072bf-large16x9_dog4.jpg",
"https://www.science.org/do/10.1126/science.aba2340/abs/dogs_1280p_0.jpg",
"https://upload.wikimedia.org/wikipedia/commons/5/58/Shiba_inu_taiki.jpg",
"https://img5.goodfon.ru/wallpaper/nbig/0/f7/sobaka-lezhit-akita-inu-akita-ryzhaia.jpg",
"https://korm.com.ua/images/companies/1/blog/korm.com.ua_pictures_05_12_18/4.jpg?1544090764933"]

@app.route('/')
def index():
    url = random.choice(images)
    return render_template('index.html', url=url)
    
if __name__ == "__main__":
    app.run(host="0.0.0.0")
