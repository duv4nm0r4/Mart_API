# Mart_API
Service using Python, MongoDB, Flask and Docker. The service receive through a POST request some parameters and return a valid response. 
Dockerized. 
Save the results in a database (MongoDB).  
GUI for the service (Flask).

Execution port: 5000
GUI URL: http://localhost:5000/

Behaviour:
• Receive a list of words in a post request in JSON format to the URL localhost:5000/api/insert_one
• From the list, extracts the longest word and returns its length, the letters used in the word and count of each letter. 
  Returns the number of characters in upper and lower case and the Caesar word encryption.
  If the longest word is an url extract the domain and defang the original url.
  If the “MART” String appears in one of the words of the input list, show it.
• The results are stored in a database. 
  You can query all data stored by localhost:5000/api/db
  You can query a specific data stored by localhost:5000/api/db/<id_to_query>
  You can delate a specific data stored by localhost:5000/api/db/delete/<id_to_delete>
  
