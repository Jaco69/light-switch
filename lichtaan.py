#
# schakelt automatisch het licht aan als het nacht wordt
#
import ephem
import time
import pifacedigitalio as p

slaap = 0   # slapen om 0 uur na middernacht
wakker = 7  # wakker om 7 uur na middernacht
wacht = 4   # wacht 4 uur na slaap om DST te berekenen
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
else:
  # het is al donker
  avond = ephem.now()

while (True):
  if (time.localtime().tm_isdst == 1):
    slaapuit =  ephem.Date(slaap * ephem.hour + 0.5 + int(ochtend) + time.altzone * ephem.second)
  else:
    slaapuit =  ephem.Date(slaap * ephem.hour + 0.5 + int(ochtend) + time.timezone * ephem.second)
  # het is avond, doe het licht aan
  p.digital_write(1, 1) #licht aan
  time.sleep((slaapuit - avond) * 24 * 3600)
  # we zijn naar bed, doe het licht uit
  p.digital_write(0, 0) #licht uit
  time.sleep(wacht * 3600) # wacht x uur voor eventuele zomer/winter tijd verandering
  if (time.localtime().tm_isdst == 1):
    wakkeraan = ephem.Date(wakker * ephem.hour + 0.5 + int(ochtend) + time.altzone * ephem.second)
  else:
    wakkeraan = ephem.Date(wakker * ephem.hour + 0.5 + int(ochtend) + time.timezone * ephem.second)
  time.sleep(((wakkeraan - slaapuit) * 24 - wacht)* 3600) # wacht de rest van de tijd tot we wakker zijn
  # we zijn wakker, is het nog donker doe dan het licht aan
  if (ochtend > wakkeraan):
    p.digital_write(0, 1) #licht aan
    time.sleep((ochtend - wakkeraan) * 24 * 3600)
    p.digital_write(0, 0) #licht uit
    print("Ochtend licht uit", ephem.localtime(ephem.now()))
  # bereken tijden voor nieuwe nacht
  time.sleep(3600)
  zon.compute()
  avond = huis.next_setting(zon, use_center=True)
  ochtend = huis.next_rising(zon, use_center=True)
  time.sleep((avond - ephem.now()) * 24 * 3600)
