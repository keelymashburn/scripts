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
    
def searching(ipaddr): 
    print ("Querying RIRs for " + ipaddr)   
    querystring = ''.join(['http://stat.ripe.net/data/whois/data.json?resource=',ipaddr])
    answer = makequery(querystring)
    fred = json.loads(answer)
    rir = fred["data"]["authorities"][0]
    print ''.join(["Authoritative RIR:  ", rir])
    # Based on RIR, invoke correct parser
    # Make these into their own functions later
    if rir == 'arin':
        # these are the keys i want: orgname, city, country
        gary = fred["data"]["records"]
        for item in gary:
            for entry in item:
                if entry["key"]=="Country":
                    print "Country = " + entry["value"]
                if entry["key"]=="City":
                    print "City = " + entry["value"]
    elif rir == 'ripe':
        return
    elif rir == 'apnic':
        return
    elif rir == 'afrinic':
        return
    elif rir == 'lacnic':
        return
    else:
        print 'Sum Ting Wong'
    
           

   


                
    #CompanyName = gary["value"]
    #print "Company Name = " + CompanyName
    
    #gary = fred["data"]["records"][0]["country"] # key is country, need value
    #CountryName = gary["value"]
    #print "Country = " + CountryName
    
    #CustomerURL = fred["data"]["records"][0]["country"]
    #print "Customer URL = " + CustomerURL
    #answer2 = makequery(CustomerURL)
    #gary = json.loads(answer2)
    #Country = fred["objects"]["object"][0] 
    #print Country
    return 

def main():
    parser = argparse.ArgumentParser(description='Search IP Address.')
    parser.add_argument('address',type = str, nargs =1)
    args = parser.parse_args()
    searching(args.address[0])

if __name__== "__main__":
    main()
