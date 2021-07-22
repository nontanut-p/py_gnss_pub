import pynmea2

#
msg = pynmea2.parse("$GNRMC,143909.00,A,5107.0020216,N,11402.3294835,W,0.036,348.3,210307,0.0,E,A*31")

print(msg.track)

