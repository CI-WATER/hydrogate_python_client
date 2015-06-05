__author__ = 'Pabitra'
from hydrogate import HydroDS

client = HydroDS()
client.authenticate_user(username="hydrogate username",  password="hydrogate password", hpc='USU')

print ">>>.DONE..."