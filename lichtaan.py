#!/usr/bin/env python3
#
# schakelt automatisch het licht aan als het nacht wordt
#
import ephem
import time
import pifacedigitalio as p

slaap = 0   # slapen om 0 uur na middernacht
wakker = 7  # wakker om 7 uur na middernacht
wacht = 4   # wacht 4 uur na slaap om DST te berekenen

def sleep(tijd):
  print ("begin slaap voor", tijd / ephem.second, "seconden om", ephem.localtime(ephem.now()))
  time.sleep(tijd / ephem.second)
  print ("stop slaap om", ephem.localtime(ephem.now()))

p.init()
huis = ephem.Observer()
huis.lat = "52.1856"
huis.lon = "4.44541"
huis.elev = 1
huis.horizon = '-2.0' # -6=civil twilight, -12=nautical, -18=astronomical
zon = ephem.Sun()
ochtend = huis.next_rising(zon, use_center=True)
avond = huis.next_setting(zon, use_center=True)
if ((avond - ephem.now()) < (ochtend-ephem.now())):
  # het is nu dag wacht tot de avond
  sleep(avond - ephem.now())
else:
  # het is al donker
  avond = ephem.now()

while (True):
  if (time.localtime().tm_isdst == 1):
    slaapuit =  ephem.Date(slaap * ephem.hour + 0.5 + int(ochtend) + time.altzone  * ephem.second)
  else:
    slaapuit =  ephem.Date(slaap * ephem.hour + 0.5 + int(ochtend) + time.timezone * ephem.second)
  if (slaapuit > avond):
    # het is avond, doe het licht aan
    p.digital_write(1, 1) #licht aan
  sleep(slaapuit - ephem.now())
  # we zijn naar bed, doe het licht uit
  p.digital_write(0, 0) #licht uit
  sleep(wacht * ephem.hour) # wacht x uur voor eventuele zomer/winter tijd verandering
  if (time.localtime().tm_isdst == 1):
    wakkeraan = ephem.Date(wakker * ephem.hour + 0.5 + int(ochtend) + time.altzone * ephem.second)
  else:
    wakkeraan = ephem.Date(wakker * ephem.hour + 0.5 + int(ochtend) + time.timezone * ephem.second)
  sleep(wakkeraan - slaapuit - wacht * ephem.hour) # wacht de rest van de tijd tot we wakker zijn
  # we zijn wakker, is het nog donker doe dan het licht aan
  if (ochtend > wakkeraan):
    p.digital_write(0, 1) #licht aan
    sleep(ochtend - wakkeraan)
    p.digital_write(0, 0) #licht uit
  # bereken tijden voor nieuwe nacht
  huis.date = ochtend + 1 * ephem.hour
  print ("nu", ephem.localtime(ephem.now()), " avond", ephem.localtime(avond), " ochtend", ephem.localtime(ochtend))
  avond = huis.next_setting(zon, use_center=True)
  ochtend = huis.next_rising(zon, use_center=True)
  print ("Volgende                       avond", ephem.localtime(avond), " ochtend", ephem.localtime(ochtend))
  sleep(avond - ephem.now())
