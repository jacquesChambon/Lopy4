from machine import Timer
from machine import WDT

class Clock:
  def __init__(self, led, period=5, max_count=10):
    self._max_count=max_count
    self.__alarm = Timer.Alarm(self._seconds_handler, period, periodic=True)
    self._led=led
    self._count=0
    self._wdt=WDT(timeout=period*2*1000)  # enable WDT with a timeout of 2*period seconds
  def _seconds_handler(self, alarm):
    self._count += 1
    print("Timer Alarm called : %s" % str(self._count))
    self._led(1)
    self._wdt.feed()
    if self._count == self._max_count:
       print("Alarm canceled afetr %s calls" % str(self._max_count))
       alarm.cancel() # stop counting
