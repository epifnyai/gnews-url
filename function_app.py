import azure.functions as func  
import json  
import logging  
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.by import By  
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC  

import time
  
app = func.FunctionApp()  
  
@app.route(route="GetOriginalURL", auth_level=func.AuthLevel.ANONYMOUS)  
def GetOriginalURL(req: func.HttpRequest) -> func.HttpResponse:  
    logging.info('Python HTTP trigger function processed a request.')  
  
    # Get the 'url' parameter from the query string or request body  
    url = req.params.get('url')  
    if not url:  
        try:  
            req_body = req.get_json()  
        except ValueError:  
            pass  
        else:  
            url = req_body.get('url')  
  
    if not url:  
        return func.HttpResponse(  
            "Please pass a 'url' in the query string or in the request body.",  
            status_code=400  
        )  
  
    def get_final_url(url):  
        # Set up options for headless mode  
        chrome_options = Options()  
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--no-sandbox")  
        chrome_options.add_argument("--disable-dev-shm-usage")  
        chrome_options.add_argument("--disable-gpu")  
        chrome_options.add_argument("--disable-software-rasterizer")  
        chrome_options.add_argument("--disable-extensions")  
        chrome_options.add_argument("--disable-popup-blocking")  
        chrome_options.add_argument("--disable-images")  
        chrome_options.add_argument("--blink-settings=imagesEnabled=false")  
        chrome_options.add_argument("--disable-javascript")  
        chrome_options.add_argument("--disable-plugins")  
        chrome_options.add_argument("--disable-infobars")  
        chrome_options.add_argument("--disable-notifications")  
        chrome_options.add_argument("--disable-background-networking")  
        chrome_options.add_argument("--disable-background-timer-throttling")  
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")  
        chrome_options.add_argument("--disable-breakpad")  
        chrome_options.add_argument("--disable-client-side-phishing-detection")  
        chrome_options.add_argument("--disable-default-apps")  
        chrome_options.add_argument("--disable-hang-monitor")  
        chrome_options.add_argument("--disable-prompt-on-repost")  
        chrome_options.add_argument("--disable-renderer-backgrounding")  
        chrome_options.add_argument("--disable-sync")  
        chrome_options.add_argument("--disable-translate")  
        chrome_options.add_argument("--disable-voice-input")  
        chrome_options.add_argument("--disable-wake-on-wifi")  
        chrome_options.add_argument("--disable-web-security")  
        chrome_options.add_argument("--disable-webrtc-hw-encoding")  
        chrome_options.add_argument("--disable-webrtc-hw-decoding")  
        chrome_options.add_argument("--headless")  
        chrome_options.add_argument("--mute-audio")  
        chrome_options.add_argument("--no-first-run")  
        chrome_options.add_argument("--no-default-browser-check")  
        chrome_options.add_argument("--password-store=basic")  
        chrome_options.add_argument("--use-mock-keychain")  
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")  
  
        driver = webdriver.Chrome(options=chrome_options)  
        # driver.set_page_load_timeout(10)  
  
        try:  
            # Open the URL  
            driver.get(url)  
  
            time.sleep(2)
  
            # Get the final URL  
            final_url = driver.current_url  
  
            return final_url  
        finally:  
            driver.quit()  
  
    final_url = get_final_url(url)  
  
    if final_url:  
        return func.HttpResponse(  
            json.dumps({"original_url": final_url}, ensure_ascii=False, indent=2),  
            mimetype="application/json",  
            status_code=200  
        )  
    else:  
        return func.HttpResponse(  
            "Failed to retrieve the original article URL.",  
            status_code=500  
        )  
        
        