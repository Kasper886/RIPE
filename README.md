# RIPE
I needed to write the script which will get info about RIPE members (RIPE provides IP to ISP, HSP and so on in Europe). 
Also I used TOR client sockets to bypass IP blocking from multiple requests.
First of all the script receives the list of RIPE mambers then parces info from json file and make reqiest to the RIPE Data Base to receive members contacts.

To prevent duplicates I added one more script that deletes duplicates.
