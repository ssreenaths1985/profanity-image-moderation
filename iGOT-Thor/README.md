# Thor-iGOT

An NSFW and India Map Detector serving responses over REST API developed using Keras (Tensorflow), Imageai and Flask in Python.

# User Guide

1. Clone Repo:
   git clone https://git.idc.tarento.com/nxt/thor/Thor-Profanity-Moderation.git
2. cd ~/Thor-Profanity-Moderation
3. Checkout to branch:
   git checkout Thor-iGOT
4. Pull the content of the branch:
   git pull origin Thor-iGOT
5. cd iGOT-Thor
7. Install pip requirements:
   pip3 install -r req.txt,
   pip3 install -r req2.txt
8. cd patch/
   if Linux: ./linux.sh
   if Windows: windows.bat
9. cd ..

10. Run app.py:
   python3 app.py




# Usage

Swagger link: http://localhost:5006/thor-igot

The curl command for for testing an image is given below:

Upload Image:
curl -X POST -F image=@path_to_image.jpeg 'http://localhost:5006/thor-igot/image/upload'



Sample Response:
{
 "code": 200,
 "payload": {
     "classification": "Not Offensive",
     "image_profanity": {
         "is_safe": true,
         "nsfw-nude": 0.06,
         "nsfw-risque": 0.0,
         "nsfw-sex": 0.0,
         "nsfw-violence": 0.0,
         "sfw": 0.94
     },
     "india_classification": [
         {
             "classification": {
                 "correct_percentage": 27,
                 "incorrect_percentage": 73
             },
             "percentage_probability": 99.94338154792786,
             "present": "true"
         }
     ],
     "text_profanity": {
         "overall_text_classification": {
             "classification": "Not Offensive",
             "probability": 0.9617760038023146,
             "text": " china ceded by pakistan china to gilgit siachen pakistan glacier ltien administered kashmir aksai chin chineser baltistan administered line of control osrinagar ladakh de administered indian kashmir jammu pakistan india c b b"
         },
         "possible_profanity": []
     }
 },
 "success": true
}
