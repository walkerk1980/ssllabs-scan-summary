#!/usr/bin/env python3
import os
import json
import sys

assessment_filename = sys.argv[1]

assessment = ''
with open(assessment_filename, 'r') as file:
  assessment = json.loads(file.read())
  for host in assessment:
    print()
    #print(host.keys())
    print(host.get('host'))
    if host.get('status') == 'ERROR':
      print(host.get('statusMessage'))
    else:
      print(' Endpoints: ')
      for endpoint in host.get('endpoints'):
        #print(endpoint.keys())
        if endpoint.get('statusMessage') == 'Ready':
          keylist = ['ipAddress', 'grade', 'details']
          if endpoint.get('grade') not in ['A', 'A+', 'A-']:
            keylist = list(endpoint.keys())
        else:
          keylist = ['ipAddress', 'statusMessage']
        for key in keylist:
          if key != 'details':
            print('  {0}: {1}'.format(key, endpoint.get(key)))
          else:
            #for key in ['suites', 'protocols']:
              #print('   {0}'.format(key))
              #print('   {0}: {1}'.format(key, endpoint.get('details').get(key)))
            if [(x) for x in endpoint.get('details').get('protocols') if x.get('version') < '1.2']:
              print(' WARNING: TLS VERSION less than 1.2 supported!')
            if [(x) for x in endpoint.get('details').get('protocols') if x.get('name') != 'TLS']:
              print(' WARNING: SSL PROTOCOL supported!')
            good_suites = [
              'TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256',
              'TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384'
            ]
            protocols = [(protocols) for protocols in endpoint.get('details').get('suites')]
            suite_lists = [(suite.get('list')) for suite in protocols][0]
            #print(suite_lists)
            if [(suite) for suite in suite_lists if 'CBC' in suite.get('name')]:
                print(' WARNING: CBC CIPHERS supported!')
            if [(suite) for suite in suite_lists if suite.get('name') not in good_suites]:
                print(' WARNING: WEAK CIPHERS supported!')
      #for cert in host.get('certs'):
        #print(cert.keys())
    print(' More details at: https://www.ssllabs.com/ssltest/analyze.html?d={0}&hideResults=on'.format(host.get('host')))
