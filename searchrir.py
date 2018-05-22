import urllib2
import argparse
import string
import json

def makequery (querystring):
    header = {'Accept': 'application/json'}
    req = urllib2.Request(querystring, None, header)
    response = urllib2.urlopen(req)
    answer = response.read()
    return answer
	
def parse_afrinic(json, irrjson, data):
    for item in json:
        # print ''.join(["Total record sets found: ", str(len(json))])
        for entry in item:
            # print ''.join(["Total data elements found: ", str(len(item))])
            # Extract data labels from key field
            # Add data of interest to data dictionary
            if str(entry['key']).lower()=='country':
                data['country'] = entry['value']            
            if str(entry['key']).lower()=='city':
                data['city'] = entry['value']
    counter = 0
    for item in irrjson:
        for entry in item:
            if str(entry['key']).lower()=='descr':
                keyname = ''.join(['descr',str(counter)])
                data[keyname] = entry['value']
            if str(entry['key']).lower()=='route':
                keyname = ''.join(['route',str(counter)])
                data[keyname] = entry['value']
            counter+=1    
    return

def parse_apnic(json, irrjson, data):
    for item in json:
        # print ''.join(["Total record sets found: ", str(len(json))])
        for entry in item:
            # print ''.join(["Total data elements found: ", str(len(item))])
            # Extract data labels from key field
            # Add data of interest to data dictionary
            if str(entry['key']).lower()=='descr':
                data['descr'] = entry['value']
            if str(entry['key']).lower()=='country':
                data['country'] = entry['value']            
            if str(entry['key']).lower()=='city':
                data['city'] = entry['value']
    counter = 0
    for item in irrjson:
        for entry in item:
            if str(entry['key']).lower()=='route':
                keyname = ''.join(['route',str(counter)])
                data[keyname] = entry['value']
                counter+=1
    return

def parse_arin(json, irrjson, data):
    for item in json:
        # print ''.join(["Total record sets found: ", str(len(json))])
        for entry in item:
            # print ''.join(["Total data elements found: ", str(len(item))])
            # Extract data labels from key field
            # Add data of interest to data dictionary
            if str(entry['key']).lower()=='orgname':
                data['orgname'] = entry['value']
            if str(entry['key']).lower()=='country':
                data['country'] = entry['value']            
            if str(entry['key']).lower()=='city':
                data['city'] = entry['value']
    counter = 0
    for item in irrjson:
        for entry in item:
            if str(entry['key']).lower()=='route':
                keyname = ''.join(['route',str(counter)])
                data[keyname] = entry['value']
                counter+=1

def parse_lacnic(json, data):
    for item in json:
        # print ''.join(["Total record sets found: ", str(len(json))])
        for entry in item:
            # print ''.join(["Total data elements found: ", str(len(item))])
            # Extract data labels from key field
            # Add data of interest to data dictionary
            if str(entry['key']).lower()=='owner':
                data['owner'] = entry['value']
            if str(entry['key']).lower()=='country':
                data['country'] = entry['value']            
            if str(entry['key']).lower()=='city':
                data['city'] = entry['value']
    return

def parse_ripe(json, irrjson, data):
    for item in json:
        # print ''.join(["Total record sets found: ", str(len(json))])
        for entry in item:
            # print ''.join(["Total data elements found: ", str(len(item))])
            # Extract data labels from key field
            # Add data of interest to data dictionary
            if str(entry['key']).lower()=='country':
                data['country'] = entry['value']            
            if str(entry['key']).lower()=='city':
                data['city'] = entry['value']
    counter = 0
    for item in irrjson:
        for entry in item:
            if str(entry['key']).lower()=='descr':
                keyname = ''.join(['descr',str(counter)])
                data[keyname] = entry['value']
            if str(entry['key']).lower()=='route':
                keyname = ''.join(['route',str(counter)])
                data[keyname] = entry['value']
            counter+=1
    return

def print_results(data):
    for key in data:
        print ''.join(['[**] ',str(key), ' : ', str(data[key])])
        
def searching(ipaddr): 
    print ''.join(["[*] ","Querying RIPEstat for ", ipaddr])   
    querystring = ''.join(['http://stat.ripe.net/data/whois/data.json?resource=',ipaddr])
    answer = makequery(querystring)
    response = json.loads(answer)
    # print response
    rir = response["data"]["authorities"][0]
    datadict = {'rir':rir}
    # Based on RIR, invoke correct parser
    records = response["data"]["records"]
    records2 = response["data"]["irr_records"]
    if rir == 'arin':
        parse_arin(records, records2, datadict)
    elif rir == 'ripe':
        parse_ripe(records, records2, datadict)
    elif rir == 'apnic':
        parse_apnic(records, records2, datadict)
    elif rir == 'afrinic':
        parse_afrinic(records, records2, datadict)
    elif rir == 'lacnic':
        parse_lacnic(records, records2, datadict)
    else:
        print 'Error'
                
    print_results(datadict)
    return 
    
def main():
    parser = argparse.ArgumentParser(description='Search IP Address.')
    parser.add_argument('address',type = str, nargs =1)
    args = parser.parse_args()
    searching(args.address[0])

if __name__== "__main__":
    main()
