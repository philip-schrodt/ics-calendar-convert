# ics-calendar-convert
This program converts a set of .ics file to a flat file with some fields of interest, eliminates most of the junk, and chronologically sorts the file. I then copy/paste the text output into an .odt document in OpenOffice (just opening the file seems to go into a spreadsheet at the moment) then select a two-column format, and go through and make manual adjustments as needed. There are some odd middle-of-word line breaks that need 
to be removed; not clear why.
 
TO RUN PROGRAM:
---------------

python3 ics_calendar_convert.py

INPUT FILE:
-----------
Hard coded list ICS_FILES of file names; also first convert to Unix file format if necessary (used to be; doesn't seem to be now)

OUTPUT FILES:
-------------

cal.scr.txt -- unsorted version with original dict records; mostly used for debugging

cal.fmt.txt -- formatted output

PROGRAMMING NOTES:
-----------------

1. The repeating events RRULE is not implemented.

2. Process for getting Google to export calendars has changed over time, is just Google this to figure out the current method. 
Google currently doesn't export the TZ information, so everything is converted from UTD to EST (or whatever time zone you want using the constant UTD_OFFSET

PROVENANCE:
-----------
Programmer: Philip A. Schrodt, Parus Analytics LLC, Charlottesville, Virginia, USA

Copyright (c) 2020  Philip A. Schrodt.  All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted under the terms of the GNU General Public License:
http://www.opensource.org/licenses/gpl-license.html

Report bugs to: parus735@gmail.com

Sample Output
-------------
```
2019.01.12
1000 - 1030: Did offsite TimeMach back of iMac
1830 - 2100: IMCC [1900]            

2019.01.13
1000 - 1030: Post OMS to Slack 
1900 - 2030: Wine tasting Market St Wine Market             

==== 2018.01.14 - 2018.01.18 ====
Berlin PreView workshop

2019.01.14
1400 - 1700: AA3111: CHO[1510] -> ORD[1610]
             Locator: XZYZWI
2130 - 0000: AA6169: ORD[2035]->LHR[1015]

==== 2018.01.15 ====
Estimated tax due

2019.01.15
2400 - 0530: AA6169: ORD[2035]->LHR[1015]
0745 - 0945: AA6596: LHR[1245] -> TXL[1540]

2019.01.19
1300 - 1345: Lunch: Michouacan             
1800 - 2100: Dinner: Bill and Melissa             

==== 2019.01.20 ====
Penguin Awareness Day

2019.01.20
0200 - 0230: BCBS Teleconf [0230]             
1900 - 2100: KM group          

2019.01.22
1100 - 1330: Lunch at Monticello: Grigg Building             
1630 - 1730: Haircut: Laura            
1830 - 2100: IMCC [1900]             

2019.01.23
0800 - 1000: IMCC ExComm meeting             
1500 - 1545: Send Berlin slides

2019.01.24
1900 - 2100: Dinner: Fig: Bill and Hillary
             Fig, 1331 W Main St, Charlottesville, VA 

2019.01.25
1400 - 1500: Susan: Tea Bazaar 
```
