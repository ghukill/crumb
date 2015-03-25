# helpers for crumb_http

def extractKV(request):
	if request.method == 'POST':
		try:
			k = request.form['key']
		except:
			k = False
		try:
			v = request.form['value']
		except:
			v = False
		


	if request.method == 'GET':
		try:
			k = request.args.get('key')
		except:
			k = False
		try:
			v = request.args.get('value')
		except:
			v = False
		


	return(k,v)

