"""
ics_calendar_convert.py

This program converts a set of .ics file to a flat file with some fields of interest, eliminates most of the junk, 
and chronologically sorts the file. I then copy/paste the text output into an .odt document in OpenOffice (just 
opening the file seems to go into a spreadsheet at the moment) then select a two-column format, and go through 
and make manual adjustments as needed. There are some odd middle-of-word line breaks that need to be removed; not clear why.
 
TO RUN PROGRAM:

python3 ics_calendar_convert.py

INPUT FILE: Hard coded list ICS_FILES of file names; also first convert to Unix file format if needed

OUTPUT FILES:

cal.scr.txt -- unsorted version with original records; mostly debugging
cal.fmt.txt -- unsorted version that prints any lines that have escaped the filtering

PROGRAMMING NOTES:

1. The repeating events RRULE is not implemented.

2. Process for getting Google to export calendars has changed over time, is just Google this to figure out the current method. 

3. Google currently doesn't export the TZ information, so everything is converted from UTD to EST (or whatever time zone you want using the constant UTD_OFFSET

SYSTEM REQUIREMENTS
This program has been successfully run under Mac OS 10.11; it is standard Python3 so it 
should also run in Unix or Windows. 

PROVENANCE:
Programmer: Philip A. Schrodt
            Parus Analytics LLC
            Charlottesville, VA

Copyright (c) 2020  Philip A. Schrodt.  All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted under the terms of the GNU General Public License:
http://www.opensource.org/licenses/gpl-license.html

Report bugs to: schrodt735@gmail.com

REVISION HISTORY:
11-Jan-11:  Initial version in perl
   Jan-20:  Finally transitioned to Python, mostly with new code

----------------------------------------------------------------------------------
"""

UTD_OFFSET = 500  # standard time offset from UTD: HHMM
DST_START = "20190310" # start and end of daylight savings time
DST_END = "20191103"

TARGET_YEAR = "2018"

ICS_FILES = ["Personal_louffmcalh372ispd47bsp6lko@group.calendar.google.com.ics", "schrodt735@gmail.com.ics"]

def fmt_date(thedate):
    return thedate[:4] + "." + thedate[4:6] + "." + thedate[6:]
    
def get_span():
    global therec
    if thedate >= DST_START and thedate <= DST_END:
        offset = UTD_OFFSET - 100
    else:
        offset = UTD_OFFSET
    atime = int(therec['start'][9:13]) - offset
    if atime <= 0:
        atime += 2400
        therec['start'] = str(int(therec['start'][:8]) -1 ) + therec['start'][8:]
    therec['timespan'] = str(atime).zfill(4)
    if "end" in therec:
        atime = int(therec['end'][9:13]) - offset
        if atime < 0:
            atime += 2400
        therec['timespan'] += " - " + str(atime).zfill(4)

    therec['date'] = therec['start'][:8]
    
     
daterec = {}

fout = open("cal.scr.txt","w")  # debugging and could be removed
MAX_KA = 64000  # DEBUG: set to a small number to avoid processing entire file
for filename in ICS_FILES:
    print("Processing", filename)
    with open(filename, "r") as fin:
        ka = 0
        line = fin.readline()
        while line:
            if line[:-1] == "BEGIN:VEVENT":
                therec = {}
                line = fin.readline()
                while line[:-1] != "END:VEVENT":
                    part = line[:-1].partition(":")
                    pt2 = part[2].replace("\\,", ",")
                    if line.startswith("DTSTART"):
                        if pt2.startswith(TARGET_YEAR):
                            therec["start"] = pt2
                            ka += 1
                            if ka > MAX_KA: break
                    elif line.startswith("DTEND"):
                            therec["end"] = pt2
                    elif line.startswith("LOCATION"):
                            if len(pt2) > 2 :
                                therec["loc"] = pt2
                    elif line.startswith("SUMMARY"):
                            therec["text"] = pt2
                    elif line.startswith("DESCRIPTION"):
                        if len(pt2) > 2:
                            strg = pt2
                            line = fin.readline()
                            while line[0] == " ":
                                strg += line[1:-1] 
                                line = fin.readline()                                                
                            if "-::~:~::" in strg:
                                therec["desc"] = strg[:strg.index("-::~:~::")] 
                            else:
                                therec["desc"] = strg 
                            therec["desc"] = therec["desc"].replace("\\,", ",")                                             
                    line = fin.readline()
                if "start" in therec:
                    thedate = therec['start'][:8]
                    if len(therec['start']) > 8:
                        get_span()
                        thedate = therec['start'][:8]
                    else:
                        therec['timespan'] = "++"
                    if thedate in daterec:
                        if therec['timespan'] in daterec[thedate]:
                            daterec[thedate][therec['timespan']].append(therec)
                        else:
                            daterec[thedate][therec['timespan']] = [therec]
                    else:                
                        daterec[thedate] = {therec['timespan']:[therec]}
                
                    fout.write(str(therec) + "\n")
            if ka > MAX_KA: break
            line = fin.readline()

fout.close()        
"""
fout = open("cal.debug.txt","w")
#print(daterec)
for date, dayrec in sorted(daterec.items()):
    fout.write(date + "\n" + str(dayrec) + "")
fout.close()
exit()
"""
fout = open("cal.fmt.txt","w")
#print(daterec)
for date, dayrec in sorted(daterec.items()):
    showday = True
    print("\n" + fmt_date(date))
    for timespan, rec in sorted(dayrec.items()):
        if timespan == "++":
            print(rec)
            for li in rec:
                fout.write("\n==== " + fmt_date(date))
                if 'end' in li and int(li['end']) -1  != int(date):
        #            print("==>", dayrec["++"][0]['end'])
                    fout.write(" - " + fmt_date(str(int(li['end']) -1)))
                fout.write(" ====\n")
                fout.write(li.get('text',"---") + "\n")
        else:
            if showday:
                fout.write("\n" + fmt_date(date) + "\n") 
                showday = False   
#            print("====", dayrec["++"][0].get('text',"---"), "====")
    #            print(rec)
            for li in rec:
                if 'text' in li:
                    print(timespan, li['text'])
                    fout.write(timespan + ": "  + li['text'] + "\n")
                    if 'loc' in li:
                        print(li['loc'])
                        fout.write("             " + li['loc'] + "\n")
                    if 'desc' in li and len(li['desc']) > 2:
                        print(li['desc'])
                        fout.write("             " + li['desc'] + "\n")
            
fout.close()
print("Finished")