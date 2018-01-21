# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

import requests as re
import json

from gcharter.models import *
from . import serializers,responder

import matplotlib.pyplot as pt
pt.switch_backend('Qt4Agg')
# Create your views here.




class TheView(viewsets.ViewSet):
    

    '''from the request url take the patient id and the readings count
    construct a request url(s) for hapi server
    process the data you get from hapi then pass it to Responder class
    return from Responder a dictionary with the p values, z scores and charts urls
    to the application requesting
    and also send a create request to hapi as an observation object'''

    

    def view(self,request,patient,readCount):

        self.patient = int(self.kwargs['patient'])
        self.readCount = int(self.kwargs['readCount'])
        
        '''demographics'''
        demosObj = re.get('https://fhirtest.uhn.ca/baseDstu3/Patient?_id={}'.format(self.patient))
        demosJson = json.loads(demosObj.text)
        dob = demosJson['entry'][0]['resource']['birthDate']
        gender = demosJson['entry'][0]['resource']['gender']



        '''weight'''
        weightObj = re.get('https://fhirtest.uhn.ca/baseDstu3/Observation?code=3141-9&_count={}&patient={}&_format=json&_pretty=true'.format(self.readCount,self.patient))

        weightJson = json.loads(weightObj.text)

        weightMs = {}

        if 'entry' in weightJson:

            for i in weightJson['entry']:

                weightMs.update({i['resource']['valueQuantity']['value']:i['resource']['valueQuantity']['unit']})
        else:
            weightMs.update({None:None})

        '''height'''
        heightObj = re.get('https://fhirtest.uhn.ca/baseDstu3/Observation?code=20570-8&_count={}&patient={}&_format=json&_pretty=true'.format(self.readCount,self.patient))

        heightJson = json.loads(heightObj.text)

        heightMs = {}

        if 'entry' in heightJson:

            for i in heightJson['entry']:

                heightMs.update({i['resource']['valueQuantity']['value']:i['resource']['valueQuantity']['unit']})
        else:
            heightMs.update({None:None})
        

        '''body mass index'''
        bmiObj = re.get('https://fhirtest.uhn.ca/baseDstu3/Observation?code=39156-5&_count={}&patient={}&_format=json&_pretty=true'.format(self.readCount,self.patient))

        bmiJson = json.loads(bmiObj.text)

        bmiMs = {}

        if 'entry' in bmiJson:

            for i in bmiJson['entry']:

                bmiMs.update({i['resource']['valueQuantity']['value']:i['resource']['valueQuantity']['unit']})
        else:
            bmiMs.update({None:None})

        '''head circumference'''
        hcObj = re.get('https://fhirtest.uhn.ca/baseDstu3/Observation?code=8287-5&_count={}&patient={}&_format=json&_pretty=true'.format(self.readCount,self.patient))

        hcJson = json.loads(hcObj.text)

        hcMs = {}

        if 'entry' in hcJson:

            for i in hcJson['entry']:

                hcMs.update({i['resource']['valueQuantity']['value']:i['resource']['valueQuantity']['unit']})

        else:
            hcMs.update({None:None})
            
        '''triceps skinfold 8354-3'''
        tsObj = re.get('https://fhirtest.uhn.ca/baseDstu3/Observation?code=8354-3&_count={}&patient={}&_format=json&_pretty=true'.format(self.readCount,self.patient))

        tsJson = json.loads(tsObj.text)

        tsMs = {}

        if 'entry' in tsJson:

            for i in tsJson['entry']:

                tsMs.update({i['resource']['valueQuantity']['value']:i['resource']['valueQuantity']['unit']})

        else:
            tsMs.update({None:None})
        '''arm circumference 56072-2'''

        acObj = re.get('https://fhirtest.uhn.ca/baseDstu3/Observation?code=56072-2&_count={}&patient={}&_format=json&_pretty=true'.format(self.readCount,self.patient))

        acJson = json.loads(acObj.text)

        acMs = {}

        if 'entry' in acJson:

            for i in acJson['entry']:

                acMs.update({i['resource']['valueQuantity']['value']:i['resource']['valueQuantity']['unit']})

        else:
            acMs.update({None:None})

        '''subscapular skinfold -> yet to get the loinc code , if any'''
        ssMs={None:None}

            

        observs = {'wt':weightMs,'ht':heightMs,'bmi':bmiMs,'hc':hcMs,'ac':acMs,'ts':tsMs,'ss':ssMs}

        respons = {}
        
        runRes = responder.Responder(self.patient,gender,dob,observs,respons)
        runRes.chartQual()
        runRes.plotter()


        return HttpResponse("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\"><html><head></head><body>%s</body></html>"%runRes.respons)
