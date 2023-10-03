import requests,bs4,os
import re
url =input( 'https://www.aiguoman.com\n')
os.makedirs('images',exist_ok=True)
num = 0
chapter = 1
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.40'
}
while url != "https://www.aiguoman.com/":
	#下载页面
	print(f' Get page {url}')
	try:
		res = requests.get(url,headers=headers)
	except requests.RequestException as e:
		print(f'Error: {e}')
		input('Press Enter to exit...')
		exit()
	#打印状态码
	if res.status_code == 200:
		print(f"Http:{res.status_code} Success\n")
	try:
		res.raise_for_status()
	except:
		print(f'Http Error:{res.status_code}')
		input('Press Enter to exit...')
		exit()
	#删除可能含日文字符的标题
	rest=res.text
	new_rest=re.sub(r'<title>.*</title>','',rest)
	#漫画分类储存
	if num ==0:
		string = re.compile(r'(?<=<title>).*?(?=</title>)')
		i = string.search(rest)
		os.makedirs(f"images/{i.group()}",exist_ok=True)
	os.makedirs(f"images/{i.group()}/chapter：{str(chapter)}",exist_ok=True)
		
	soup = bs4.BeautifulSoup(new_rest,'html.parser')
	#选择器
	comicElems = soup.find_all('img')
	for comicElem in comicElems:
		comicUrl = comicElem.get('src')
		print(f' Downloading img {comicUrl}\n')			
		try:
			res = requests.get(comicUrl)
			res.raise_for_status()
		except:
			print(f'Http Error:{res.status_code}\npass\n')
			pass
		#保存图像
		imageFile = open(os.path.join(f"images/{i.group()}/chapter：{str(chapter)}",os.path.basename(f"{str(num)}.jpg")),'wb')
		num +=1
		for chunk in res.iter_content(1000000):
			imageFile.write(chunk)
		imageFile.close()

	print("Could not find imgs in this page\n")
	print("Trying to get next chapter\n")
	#获取下一章节的url
	try:
		prevLink = soup.select('.next-title')[0]
		chapter +=1
	except:
		break
	url = f"https://www.aiguoman.com/{prevLink.get('href')}"

input("All the task has been completed")

	 

