'''*****************************************************************************
FILE: saveSymbols.py
Author: asad70
-------------------------------------------------------------------
****************************************************************************'''
import requests
from requests import get
from bs4 import BeautifulSoup

def saveSym(exchange, outputFile):
	exchanges = {
	"nasdaq": "https://www.advfn.com/nasdaq/nasdaq.asp?companies={letter}",	
	"nyse": "https://www.advfn.com/nyse/newyorkstockexchange.asp?companies={letter}",
	"amex": "https://www.advfn.com/amex/americanstockexchange.asp?companies={letter}"}

	url = exchanges[exchange.lower()]
	file = open(outputFile, 'w', encoding="utf-8")
	
	# advfn web structures each symbol by letter
	letters = "ABCDEFGHIJKLMNOPQUSTUVWXYZ+"
	for letter in letters:
		request_data = requests.get(url.format(letter = letter))
		request_html = request_data.text
		soup = BeautifulSoup(request_html, 'html.parser')
		content = soup.find_all("table", {"class", "market tab1"})
		rows = content[0].find_all("tr")
		for i in range(2, len(rows)):
			td = rows[i].find_all("td")
			symbol = td[1].getText()
			name = td[0].getText()
			if len(symbol) != 0:
				file.write(f"{name}, {symbol}")
				file.write("\n")
		print(f"Finished letter {letter} for {exchange}")
	file.close()
	print(f"Finished extracting data for {exchange}. Data saved in {outputFile}")
	

saveSym("nasdaq", "nasdaqsym.txt")
saveSym("amex", "amexsym.txt")
saveSym("nyse", "nysesym.txt")