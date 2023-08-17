# gpsclock

A clock applet for HamPack (https://www.i8zse.it/en/hampack-e/).

Hampack is a Raspberry Pi4 setup made to use weak signal hamradio modes 'on the go', without any external service.
Weak Signal modes (as FT-8 or Js8Call) require an accurate time reference to work. In a standard setup, system tyme
is syncrhonized via NTP.
Since HamPack is intended to be used in places where the Internet is not available, it has a local NTP server configured
to get sync from a GPS receiver. However, GPS can get time to acquire a steady signal, so it is important to have a way to
simply know the 'quality' of time.

GpsClock interacts with gpsd (that handles GPS position data) and chrony (that gets the time from PPS data) and shows that
'quality', along with the position in Maidenhead grid locator (QRA) notation, that is the one we ham radio operator use to
identify our location.
