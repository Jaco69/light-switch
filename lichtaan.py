#
# schakeld automatisch het licht aan als het nacht wordt
#
import ephem
import time
import pifacedigitalio as p

p.init()
huis = ephem.Observer()
huis.lat = "52.1856"
huis.lon = "4.44541"
huis.elev = 1
huis.horizon = '-2.0' # -6=civil twilight, -12=nautical, -18=astronomical
zon = ephem.Sun()
zon.compute()
ochtend = huis.next_rising(zon, use_center=True)
avond = huis.next_setting(zon, use_center=True)
if ((avond - ephem.now()) < (ochtend-ephem.now())):
  # het is nu dag wacht tot de avond
  time.sleep((avond - ephem.now()) * 24 * 3600)

while (True):
  slaapuit =  0 * ephem.hour + int(ochtend) + time.altzone * ephem.minute # licht uit om 00:00 uur 's nachts
  # het is avond, doe het licht aan
  p.digital_write(0, 1) #licht aan
  time.sleep((slaapuit - avond) * 24 * 3600)
  # we zijn naar bed, doe het licht uit
  p.digital_write(0, 0) #licht uit
  time.sleep(4 * 3600) # wacht 4 uur voor eventuele zomer/winter tijd verandering
  wakkeraan = 7 * ephem.hour + int(ochtend) + time.altzone * ephem.minute # de tijd dat we opstaan
  time.sleep((wakkeraan - slaapuit) * 24 * 3600 - 4 * 3600) # wacht de rest van de tijd tot we wakker zijn
  # we zijn wakker, is het nog donker doe dan het licht aan
  if (ochtend > wakkeraan):
    p.digital_write(0, 1) #licht aan
    time.sleep((ochtend - wakkeraan) * 24 * 3600)
    p.digital_write(0, 0) #licht uit
  # bereken tijden voor nieuwe nacht
  sleep(3600)
  zon.compute()
  avond = huis.next_setting(zon, use_center=True)
  ochtend = huis.next_rising(zon, use_center=True)
  time.sleep((avond - ephem.now()) * 24 * 3600)


