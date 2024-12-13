# Use the Azure Functions Python base image  
FROM mcr.microsoft.com/azure-functions/python:4-python3.11-appservice  
  
# Enable Azure Functions logging  
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \  
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true  
  
# Install manually all the missing libraries  
RUN apt-get update && \  
    apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils wget && \  
    rm -rf /var/lib/apt/lists/*  
  
# Install Chrome  
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \  
    dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install && \  
    rm google-chrome-stable_current_amd64.deb  
  
# Copy requirements.txt and install Python dependencies  
COPY requirements.txt /  
RUN pip install --no-cache-dir -r /requirements.txt  
  
# Copy the rest of the application code  
COPY . /home/site/wwwroot  
  
# Command to start the Azure Functions runtime  
CMD ["python", "-m", "azure_functions_worker"]  