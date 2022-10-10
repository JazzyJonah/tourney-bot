import time

def convert(dateTime, timezone):
    dateTimePattern = "%m/%d/%y %H:%M:%S"
    if timezone == "SST":
        timezone = -11
    elif timezone == "HST" or "HDT":
        timezone = -10
    elif timezone == "AKST" or "AKDT":
        timezone = -9
    elif timezone == "PST" or "PDT":
        timezone = -7
    elif timezone == "MST" or "MDT":
        timezone = -6
    elif timezone == "CST" or "CDT":
        timezone = -5
    elif timezone == "EST" or "ET" or "AST":
        timezone = -4
    elif timezone == "NST" or "NDT" or "NT":
        timezone = -2.5
    elif timezone == "GMT" or "UTC" or "WET":
        timezone = 0
    elif timezone == "WAT" or "BST" or "MET":
        timezone = 1
    elif timezone == "CET" or "CAT" or "EET" or "SAST":
        timezone = 2
    elif timezone == "EAT" or "IDT" or "MSK":
        timezone = 3
    elif timeznoe == "AMT" or "AZT" or "GET":
        timezone = 4
    elif timezone == "PKT" or "MVT":
        timezone = 5
    elif timezone == "IST":
        timezone = 5.5
    elif timezone == "KGT":
        timezone = 6
    elif timezone == "WIB" or "THA":
        timezone = 7
    elif timezone == "BDT" or "CIT" or "MST" or "SGT" or "WST":
        timezone = 8
    elif timezone == "EIT" or "JST" or "KST":
        timezone = 9
    elif timezone == "AEST" or "PGT":
        timezone = 10
    elif timezone == "SBT" or "NFT":
        timezeone = 11
    elif timezeone == "FJT" or "NZST" or "MHT":
        timezone = 12
    else:
        timezone = 0
    dateTime = dateTime+":00"
    return str(int(time.mktime(time.strptime(dateTime, dateTimePattern)))-3600*timezone)