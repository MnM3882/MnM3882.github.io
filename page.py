import sys
import os
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import mpld3
from flask import Flask, Response, render_template

app = Flask(__name__)

def scope():
	i = 0
	t = np.linspace(0, 0.5, 501)
	x = np.zeros(501)
	y = np.zeros(501)

	fig = plt.figure()
	ax = fig.add_subplot(1,1,1)
	ax.axis([0, 0.5, -100, 100])
	ax.set_title('Probando')
	lines1, = ax.plot(t, x, c='b')
	lines2, = ax.plot(t, y, c='r')
	
	plt.ion()

	fig.canvas.draw()

	while True:
		x = np.delete(x,0)
		x = np.append(x,np.random.randn())

		y = np.delete(y,0)
		y = np.append(y,-np.random.randn())

		if i == 0:

			lines1.set_ydata(np.cumsum(x))
			lines2.set_ydata(np.cumsum(y))
			fig.canvas.draw()

			fig.savefig('test.png')
			yield (b'--frame\r\n'+b'Content-Type: image/png\r\n\r\n' + open('test.png','rb').read() + b'\r\n')

			tt = False

		i = (i+1)%50
	
	
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
	return Response(scope(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)
