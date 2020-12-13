import json
import requests
import os
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

url = 'https://mirrors.tuna.tsinghua.edu.cn/jenkins/'
# Python 字典类型转换为 JSON 对象

def downloadPlugin(plugin):
	purl = '%splugins/%s/%s/%s.hpi' % (url, plugin['name'], plugin['version'], plugin['name'])
	down_res = requests.get(purl)
	path = 'plugins/%s/%s'%(plugin['name'],plugin['version'])
	try:
		os.makedirs(path)
	except Exception as e:
		pass
	with open('%s/%s.hpi'%(path,plugin['name']), "wb") as code:
		code.write(down_res.content)
with open('update-center.json','r',encoding='utf-8') as f:
	urls = []
	for line in f.readlines():
		data = json.loads(line)
		plugins = data['plugins']
		for i in plugins:
			#downloadPlugin(plugins[i])
			urls.append(plugins[i])
			depends = plugins[i]['dependencies']
			for j in range(len(depends)):
				# downloadPlugin(depends[j])
				urls.append(depends[j])
	executor = ThreadPoolExecutor(len(urls))
	future_tasks = [executor.submit(downloadPlugin, plugin) for plugin in urls]
	wait(future_tasks, return_when=ALL_COMPLETED)

