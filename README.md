# football_scrapper_whoscored
Scraper4.py is a file which scrapes the data from whoscored.com using selenium and data stored in json format
All the generated data from the scraper has been stored inside the MongoDB so that queries can easily fetch the data from MongoDB.
For starting with MongoDB, mongodb server has to be downloaded and start the server and connect with mongodb compass
https://www.mongodb.com/download-center/community
After installing mongodb community edition, mongodb server has to started . for that goto run type mongod.exe and then start it. if it automatically switches off the windows then goto your user folder and create a folder name "DB" and another folder inside DB :
then start it again. server will not shut down. 
After starting the server, compass has to be downloaded from below link 
https://www.mongodb.com/products/compass?lang=de-de
and connect with mongoDB server, MongoDB default server is 
  host = '127.0.0.1'
    port = 27017
and this way your scraped data will be  uploaded into Mongo compass.

