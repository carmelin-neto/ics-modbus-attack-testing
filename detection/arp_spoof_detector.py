## Detection Engineering Addition

To go beyond attack testing, I wrote a small Python detection script 
(`detection/arp_spoof_detector.py`, using Scapy) that flags the exact 
signature of the ARP spoofing attack I ran above: a single MAC address 
claiming ownership of more than one IP address in a capture window.

I validated it two ways:

1. **Against the attack traffic** — the script correctly flagged the MAC 
   address used in the spoofing attempt, showing it had claimed to own 
   both the PLC's IP and the target device's IP simultaneously:

   ![ARP spoof detected](screenshots/detector-alert.png)

2. **Against clean, legitimate traffic** (my original PLC capture with no 
   attack activity) — the script correctly reported no spoofing signature, 
   confirming it doesn't false-positive on normal network behavior:

   ![No false positive on clean traffic](screenshots/detector-clean.png)

This closes the loop between offense and defense: I didn't just run an 
attack and observe the result — I built and validated a way to detect it.
