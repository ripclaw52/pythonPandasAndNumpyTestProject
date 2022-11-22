import googlemaps

API_KEY= 'AIzaSyAF0yyNAP6SC5THWffeBciCEWz0gXXQ8Ao'

map_client = googlemaps.Client(API_KEY)

addy='470 Macewan Rd SW, Edmonton, Alberta'
addy2='3216 26 Street, Edmonton, Alberta'

addy3='2710 33 Avenue, Edmonton, Alberta'

addy4 = '2420 108 Street, Edmonton, Alberta'

addy5 = '3268 28 Avenue NW, Edmonton, Alberta'

response = map_client.geocode(addy5)
print(response)