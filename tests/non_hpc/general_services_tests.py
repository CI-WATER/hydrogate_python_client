__author__ = 'Pabitra'
from hydrogate import HydroDS

client = HydroDS()

# test printing service log history all, first in first print
client.show_service_request_history()

# print only the first 2 items
client.show_service_request_history(count=2)

# print all items (last in print first)
client.show_service_request_history(order='last')

# print only the last 3 items
client.show_service_request_history(order='last', count=3)

print ">>> DONE ...."