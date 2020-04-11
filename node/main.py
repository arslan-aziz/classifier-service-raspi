"""
The Pi sends a POST request encoding an acquired image to the image 
classifier service.
"""

import requests
import picamera
import time
import io
import base64

def capture_img():
	my_stream = io.BytesIO()
	with picamera.PiCamera() as camera:
		camera.resolution = (640,480)
		camera.start_preview()
		time.sleep(2)
		camera.capture(my_stream,'jpeg')
	return my_stream

def post_image(URL):
	# acquire image as byte file stream
	img = capture_img()
	img_encoded = str(base64.b64encode(img.getvalue()),encoding='utf-8') #encode bytes data
	response = requests.post(URL, data=img_encoded) #post string data
	return response


if __name__ == "__main__":
	URL ="http://192.168.1.12:80/upload_image" 
	while(True):
		response = post_image(URL)
		print(str(response.status_code)+" "+response.reason)
		time.sleep(2)

