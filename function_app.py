import azure.functions as func  
import json  
import logging  
from googlenewsdecoder import new_decoderv1  
  
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
        interval_time = 0  # default interval is None, if not specified  
        try:  
            decoded_url = new_decoderv1(url, interval=interval_time)  
            if decoded_url.get("status"):  
                return decoded_url["decoded_url"]  
            else:  
                logging.error("Error: " + decoded_url["message"])  
                return None  
        except Exception as e:  
            logging.error(f"Error occurred: {e}")  
            return None  
  
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