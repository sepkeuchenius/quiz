import requests

for i in range(10):
    
    print(requests.get(f"https://www.bene-system.com/hp/pdfservice?pdf=XFPCRNX{some_number}NS{date}").text)