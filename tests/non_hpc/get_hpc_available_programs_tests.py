__author__ = 'Pabitra'

from hydrogate import HydroDS

client = HydroDS(hpc='USU')
client.login(username="username for hydrogate",  password="password for hydrogate")

programs_at_usu_hpc = client.get_available_programs(hpc='USU')

print(programs_at_usu_hpc)

print ">>>>DONE ..."