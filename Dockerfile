FROM mcr.microsoft.com/azure-functions/python:4-python3.10
 
ENV AzureWebJobsScriptRoot=/ \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# Install azure-cli
RUN pip3 install azure-cli

# Install azure-functions-core-tools
# ref: https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local
RUN apt-get update && \
  apt-get install -y curl gpg && \
  apt install -y lsb-release && \
  curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg && \
  mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg && \
  echo "" \
  apt-get update && \
  apt-get install -y azure-functions-core-tools-4

# Install essential packages
RUN apt-get update \
    && apt-get install -y \
    build-essential \
    cmake \
    git \
    wget \
    unzip \
    unixodbc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install a specific version of Chrome - v114.0.5735.198-1 in this case.
RUN CHROME_VERSION=114.0.5735.198-1 && \
    wget --no-check-certificate xxxx && \
    dpkg -i google-chrome-stable_${CHROME_VERSION}_amd64.deb; apt update; apt install -y -f; apt install -y xvfb;

# Install specific versions of the Chrome driver corresponding to the chrome version installed above
RUN BROWSER_MAJOR=$(google-chrome --version | sed 's/Google Chrome \([0-9]*\).*/\1/g') && \
    wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${BROWSER_MAJOR} -O chrome_version && \
    wget https://chromedriver.storage.googleapis.com/`cat chrome_version`/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/ && \
    DRIVER_MAJOR=$(chromedriver --version | sed 's/ChromeDriver \([0-9]*\).*/\1/g') && \
    echo "chrome version: $BROWSER_MAJOR" && \
    echo "chromedriver version: $DRIVER_MAJOR" && \
    if [ $BROWSER_MAJOR != $DRIVER_MAJOR ]; then echo "VERSION MISMATCH"; exit 1; fi

ENV PATH="/usr/local/bin/chromedriver:${PATH}"
 
COPY requirements.txt /
RUN pip install -r /requirements.txt
 
COPY . .

EXPOSE xxxx

CMD func host start --port xxxx
