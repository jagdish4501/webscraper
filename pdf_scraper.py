from selenium import webdriver
import requests
import queue
url = "https://arxiv.org/"


driver = webdriver.Chrome()
driver.get(url)
links = driver.execute_script("return document.getElementsByTagName('a');")


# Convert links array to a queue
links_queue = queue.Queue()
for link in links:
    links_queue.put(link.get_attribute('href'))

# Process links in a loop until queue is empty
while not links_queue.empty():
    href = links_queue.get()
    print(href, links_queue.qsize())
    try:
        response = requests.get(href)
        if response.headers.get('content-type') == 'application/pdf':
            # Generate a random filename using UUID
            filename = str(url.split("/")[-1]) + ".pdf"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print("PDF file saved:", filename)
        else:
            new_links = driver.execute_script(
                "return document.getElementsByTagName('a');")
            for link in new_links:
                links_queue.put(link.get_attribute('href'))
    except Exception as e:
        print("Error occurred while processing link:", e)

driver.quit()
