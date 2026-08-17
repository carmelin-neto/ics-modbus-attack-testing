# ICS Modbus Attack Testing — Probing Input Register Protections and ARP Spoofing on a Simulated PLC

## Objective
Test, rather than assume, whether two common attack techniques against 
industrial control traffic actually work in practice: (1) directly writing 
a fabricated value into a live sensor reading, and (2) intercepting 
PLC-to-device traffic via ARP spoofing. This project demonstrates hands-on 
attack testing against a simulated OT environment, building on the 
segmentation design from my [Purdue Model Mapping project](https://github.com/carmelin-neto/ot-purdue-model-mapping/blob/main/screenshots/purdue-model-oilgas..drawio.png) 
and the theoretical risks covered in my [Scanning Risk Writeup](https://github.com/carmelin-neto/ot-active-scanning-risk).

## Why This Project
It's one thing to explain why OT attacks are risky in theory — it's another 
to actually test whether a specific technique works against a real (if 
simulated) PLC, and to understand exactly why it succeeds or fails at the 
protocol level. This project shows I can move from concept to hands-on 
verification, and that I understand Modbus deeply enough to interpret 
results that weren't the ones I initially expected.

## Environment / Tools
- GRFICS v3 (Fortiphyd) — Docker-based industrial control system simulation
- Wireshark / tshark — packet capture and protocol analysis
- Python + pymodbus — scripted Modbus read/write testing
- arpspoof (dsniff) — ARP cache poisoning attempt
- Network segmentation: DMZ subnet (192.168.90.x) and ICS subnet 
  (192.168.95.x), consistent with the Purdue Model boundary from Project 1

## What I Did
1. Captured live Modbus traffic directly from the PLC container to identify 
   which of six field devices carried an actively-changing sensor value 
   (as opposed to static/idle registers).
2. Wrote a Python script using pymodbus to read the live sensor value, 
   attempt to overwrite it with a fabricated value, then read it again to 
   check whether the write took effect.
3. Set up a two-directional ARP spoofing attack from a device positioned on 
   the same network segment as the PLC, attempting to insert myself into 
   the traffic path between the PLC and the target sensor device.
4. Verified the spoofing attempt's actual effect by directly inspecting the 
   PLC's ARP cache, rather than assuming success from the tool running 
   without errors.

## Findings

I tested whether the live tank-level sensor value could be directly 
overwritten by sending a write command of `99` to the register. The write 
technically succeeded and returned a success status, but the actual sensor 
reading stubbornly remained at `302`, unaffected. This happens because 
Modbus separates "Input Registers" (the read-only space where the sensor 
value actually lives) from "Holding Registers" (the space a write command 
targets), even when both use the same numeric address. The write landed in 
a completely different memory zone than the one the sensor was actually 
reading from — confirming that the protocol-level separation genuinely 
holds, not just in theory.

I also attempted an ARP spoofing man-in-the-middle attack from a device 
positioned on the same network segment as the PLC, sending forged ARP 
replies to both the PLC and the target sensor device to try to intercept 
their traffic. The spoofing process ran continuously with no errors on my 
end, but checking the PLC's actual ARP table afterward showed no entry for 
the target device at all — not a poisoned one, just none. This failed 
because the PLC's underlying Linux system ignores unsolicited "gratuitous" 
ARP announcements by default, and only updates its ARP cache in response to 
a request it explicitly sent out itself.

## What I'd Do Differently in Production
Both results here are specific to this simulated environment's default 
configuration. A real assessment would need to test whether the target's 
ARP handling can be forced into accepting spoofed entries (e.g., by timing 
replies against genuine ARP requests rather than sending gratuitous ones), 
and would need to map which specific Modbus function codes and register 
types are writable on the actual devices in scope, rather than assuming 
uniform behavior across a fleet of PLCs.

## Screenshots

![Write test result](screenshots/write-test.png)
![ARP table - arp -n](screenshots/arp-n.png)
![ARP table - /proc/net/arp](screenshots/arp.png)


