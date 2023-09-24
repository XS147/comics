import requests,bs4,os
url = 'https://www.aiguoman.com/chapter/199421-38150.html'
os.makedirs('bing',exist_ok=True)
headers = {
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.40'
}
while url != "https://www.aiguoman.com/":
	#下载页面
	print(f' Downloading page {url}')
	res =requests.get(url,headers=headers)
	print(res.text)
	#打印状态码
	if res.status_code == 200:
		print(f"Http:{res.status_code} Success\n")
	try:
		res.raise_for_status()
	except:
		print(f'Http Error:{res.status_code}')
		input()
		pass
	soup = bs4.BeautifulSoup(res.text,'html.parser')
	#选择器
	comicElems = soup.find_all(f'.main-item img')
	if comicElems==[]:
		print("Could not find imgs in this page\n")
		print("Trying to get next chapter\n")
		#获取下一章节的url
		prevLink = soup.select('.next-title')[0]
		if prevLink == []:
			break
		else:
			url = f"https://www.aiguoman.com/{prevLink.get('href')}"
			break
	else:
		comicUrl = comicElems[0].get('src')
		print(f' Downloading img {comicUrl}\n')			
		try:
			res = requests.get(comicUrl)
			res.raise_for_status()
		except:
			print(f'Http Error:{res.status_code}\npass\n')
			pass
		#保存图像
		imageFile = open(os.path.join('images',os.path.basename(comicUrl)),'wb')
		for chunk in res.iter_content(1000000):
			imageFile.write(chunk)
		imageFile.close()
input("All the task has been completed")

	#获取下一章节的url
	#prevLink = soup.select('body > div.main.main-scroll_mode.J_scroll_mode.J_block > ul > li:nth-child(39) > a')[0]
	#url = f"https:{prevLink.get('href')}"

	 

