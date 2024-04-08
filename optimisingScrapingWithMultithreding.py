from selenium import webdriver
import requests
import threading
import sys

url = "https://arxiv.org/list/astro-ph/new?skip=0&show=2000"

def fn(url):
    if url is not None:
        if 'pdf' in url:
            return True
        else:
            return False
    

def save_pdf(url):
    try:
        response = requests.get(url)
        if response.headers.get('content-type') == 'application/pdf':
            # Generate a random filename using UUID
            filename = str(url.split("/")[-1]) + ".pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print("PDF file saved:", filename)
    except : 
        print("error occured in save file function")




driver = webdriver.Chrome()
driver.get(url)
links = driver.execute_script("return document.getElementsByTagName('a');")
print("size of link", len(links))

# Function to process links in a separate thread
def process_links(links, stop_event):
    for link in links:
        if stop_event.is_set():
            return
        href = link.get_attribute('href')
        if fn(href):
            save_pdf(href)

# Split the links into chunks for each thread
chunk_size = 5  # Adjust as needed
link_chunks = [links[i:i+chunk_size] for i in range(0, len(links), chunk_size)]

# Create and start threads for each link chunk
threads = []
stop_event = threading.Event()

for chunk in link_chunks:
    thread = threading.Thread(target=process_links, args=(chunk, stop_event))
    thread.start()
    threads.append(thread)

try:
    # Wait for all threads to finish
    for thread in threads:
        thread.join()
except KeyboardInterrupt:
    print("Ctrl+C detected, exiting...")
    stop_event.set()  # Set the flag to signal threads to exit gracefully
    sys.exit(0)  # Exit peacefully after setting the flag

driver.quit()
