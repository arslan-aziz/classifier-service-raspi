"""
The Pi sends a POST request encoding an acquired image to the image 
classifier service.
"""

import requests
import time
import io

if __name__ == "__main__":
	URL ="http://192.168.1.12:80/pitest"
	i=0 
	while(True):
		#response = post_image(URL)
		data = "count "+str(i)
		response = requests.post(URL,data=data.encode('utf-8'))
		print(str(response.status_code)+" "+response.reason)
		time.sleep(2)
		i+=1

