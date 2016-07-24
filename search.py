import sys
import time
import getopt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException

def init_driver():
	driver = webdriver.Chrome()
	driver.wait = WebDriverWait(driver, 5)
	return driver

def googleit(driver, query):
	driver.get("https://www.google.com")
	try:
		box = driver.wait.until(EC.presence_of_element_located((By.NAME, "q")))
		button = driver.wait.until(EC.element_to_be_clickable((By.NAME, "btnK")))
		box.send_keys(query)
		try:
			button.click()
		except ElementNotVisibleException:
			button = driver.wait.until(EC.visibility_of_element_located((By.NAME, "btnG")))
			button.click()
	except TimeoutException:
		print("Can't reach server")

def bingit(driver, query):
	driver.get("https://www.bing.com")
	try:
		box = driver.wait.until(EC.presence_of_element_located((By.NAME, "q")))
		button = driver.wait.until(EC.element_to_be_clickable((By.NAME, "go")))
		box.send_keys(query)
		button.click()
	except TimeoutException:
		print("Can't reach server")

def ddgit(driver, query):
	driver.get("https://www.duckduckgo.com")
	try:
		box = driver.wait.until(EC.presence_of_element_located((By.NAME, "q")))
		button = driver.wait.until(EC.element_to_be_clickable((By.ID, "search_button_homepage")))
		box.send_keys(query)
		try:
			button.click()
		except ElementNotVisibleException:
			button = driver.wait.until(EC.visibility_of_element_located((By.ID, "search_button")))
			button.click()
	except TimeoutException:
		print("Can't reach server")

def lookup(driver, query, engine):
	if engine == "google":
		googleit(driver, query)
	elif engine == "bing":
		bingit(driver, query)
	elif engine == "duckduckgo":
		ddgit(driver, query)

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], 'he:', ['help', 'engine='])
	except getopt.GetoptError:
		print("[-h] [--help] for help.\n[-e] engine or [--engine] engine for custom search engine. Default is Google.")
	
	engine = 'google'
	for flag, arg in opts:
		if flag in ['-h', '--help']:
			print("[-h] [--help] for help.\n[-e] engine or [--engine] engine for custom search engine. Default is Google.")
		elif flag in ['-e', '--engine']:
			engine = arg

	# print(args)
	if args == []:
		print("No query specified.")
		sys.exit(2)
	else:
		query = "".join(args)

	supported_engines = ["google", "bing", "duckduckgo"]

	if(engine not in supported_engines):
		print(engine.upper(), "search engine not supported. Use Google, Bing or DuckDuckGo")
		print("[-h] [--help] for help.\n[-e] engine or [--engine] engine for custom search engine. Default is Google.")
		sys.exit(2)

	driver = init_driver()
	lookup(driver, query, engine.lower())
	time.sleep(5)
	driver.quit()

if __name__ == "__main__":
	main()