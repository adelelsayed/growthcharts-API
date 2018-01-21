

import datetime as dat
import agecalc
import requests as re
import base64

from dateutil import relativedelta

import matplotlib.pyplot as pt
pt.switch_backend('Qt4Agg')

import scipy.stats as sp
import numpy as np

from gcharter.models import *


wtCharts = ['weight for age 0 to 5 years boys','weight for age 0 to 5 years girls','weight for age 5 to 10 years boys','weight for age 5 to 10 years girls']
htCharts =['height for age 5 to 19 years boys','height for age 5 to 19 years girls','length-height for age 0 to 5 years boys',
           'length-height for age 0 to 5 years girls']
bmiCharts=['body mass index for age 0 to 5 years boys','body mass index for age 0 to 5 years girls','body mass index for age 5 to 19 years boys',
           'body mass index for age 5 to 19 years girls']
hcCharts =['head circumference for age 0 to 5 years boys','head circumference for age 0 to 5 years girls']
acCharts=['arm circumference for age up to 5 years boys','arm circumference for age up to 5 years girls']
ssCharts=['subscapular skinfold for age up to 5 years boys','subscapular skinfold for age up to 5 years girls']
tsCharts=['triceps skinfold for age up to 5 years boys','triceps skinfold for age up to 5 years girls']

bundle = '''{
  "resourceType":"Bundle" ,
  "type":"transaction",
  "entry": [{"request": {
                        "method":"POST",
                        "url": "Observation"},
						
						"resource":{
						"resourceType":"Observation",
						"status":"final",
						"valueCodeableConcept":{
						"code": {
						"coding": {
                "system": "gcharts" ,
                "code":  %d ,
                "display": "%s"}}},
				"subject":{
          "reference": "Patient/%d"
        },"valueString":"%s" }}]}'''

headers = {"content-type":"application/fhir+json;charset=utf-8"}


class Responder:

    

    def __init__(self,ide,gen,dob,obs,respons):

        self.ide = ide
        self.gen = gen
        self.dob = dob
        self.obs = obs
        self.respons = respons
        

        

    def chartQual(self):

        global dateOB,numDays, numMonths
        dateOB = dat.datetime.strptime(self.dob,'%Y-%m-%d')
        numDays = (dat.datetime.now() - dateOB).days
        numMonths = agecalc.age_months(dateOB.day,dateOB.month,dateOB.year)
      
        if numDays/365 <= 5:
            chartsQualified = [ charOb['chartName'] for charOb in Percentiles.objects.filter(xValueType='age',
                                                    xValue = numDays,
                                                    xUnit = 'days'
                                                    , genderValue = self.gen
                                                    ).values()]
            if numDays/365 <= 2 and self.obs['wt'].keys()!= [None] and self.obs['ht'].keys()!= [None]:

                if self.gen == 'male':
                    chartsQualified.append('weight for length 0 to 2 years boys')
                elif self.gen == 'female':
                    chartsQualified.append('weight for length 0 to 2 years girls')
            elif numDays/365 > 2 and self.obs['wt'].keys()!= [None] and self.obs['ht'].keys()!= [None]:

                if self.gen == 'male':
                    chartsQualified.append('weight for height 2 to 5 years boys')
                elif self.gen == 'female':
                    chartsQualified.append('weight for height 2 to 5 years girls')



        elif numDays/365 >= 5 and numDays/365 <= 19:
            chartsQualified = [charOb['chartName'] for charOb in Percentiles.objects.filter(xValueType='age',
                                                    xValue = numMonths,
                                                    xUnit = 'months'
                                                    , genderValue = self.gen
                                                    ).values()]

        '''clear the charts that request had no measurements for'''
        if self.obs['wt'].keys()== [None]:
            chartsQualified= [x for x in chartsQualified if x not in wtCharts]

        if self.obs['ht'].keys()== [None]:
            chartsQualified= [x for x in chartsQualified if x not in htCharts]

        if self.obs['bmi'].keys()== [None]:
            chartsQualified= [x for x in chartsQualified if x not in bmiCharts]

        if self.obs['hc'].keys()== [None]:
            chartsQualified= [x for x in chartsQualified if x not in hcCharts]

        if self.obs['ac'].keys()== [None]:
            chartsQualified= [x for x in chartsQualified if x not in acCharts]

        if self.obs['ts'].keys()== [None]:
            chartsQualified= [x for x in chartsQualified if x not in tsCharts]

        '''subscapular skinfold yet to be completed when i get loinc code for it'''
        chartsQualified= [x for x in chartsQualified if x not in ssCharts]
        
        
        self.chartsQualified =chartsQualified

        return self.chartsQualified

    
    def plotter(self):


        
        qual  = {'days':numDays,'months':numMonths}
        if self.obs['ht'].keys() != [None]:qual.update({ 'cm': (sum(self.obs['ht'].keys())/float(len(self.obs['ht'].keys())))})


        

        for i in self.chartsQualified:

            deter = Percentiles.objects.values_list('xUnit',flat = True).filter(chartName = i)[0]


            x_axis = Percentiles.objects.values_list('xValue',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))

            P01 = Percentiles.objects.values_list('valueP01',flat = True).filter(chartName = i , xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P1 =  Percentiles.objects.values_list('valueP1',flat = True).filter(chartName = i , xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P3 =  Percentiles.objects.values_list('valueP3',flat = True).filter(chartName = i , xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P5 =  Percentiles.objects.values_list('valueP5',flat = True).filter(chartName = i , xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P10 =  Percentiles.objects.values_list('valueP10',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P15 =  Percentiles.objects.values_list('valueP15',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P25 =  Percentiles.objects.values_list('valueP25',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P50 =  Percentiles.objects.values_list('valueP50',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P75 =  Percentiles.objects.values_list('valueP75',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P85 =  Percentiles.objects.values_list('valueP85',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P90 =  Percentiles.objects.values_list('valueP90',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P95 =  Percentiles.objects.values_list('valueP95',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P97 =  Percentiles.objects.values_list('valueP97',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P99 =  Percentiles.objects.values_list('valueP99',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            P999 =  Percentiles.objects.values_list('valueP999',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            SD4neg=  Percentiles.objects.values_list('valueSD4neg',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            SD3neg=  Percentiles.objects.values_list('valueSD3neg',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            SD2neg=  Percentiles.objects.values_list('valueSD2neg',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            SD1neg=  Percentiles.objects.values_list('valueSD1neg',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            SD0=  Percentiles.objects.values_list('valueSD0',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            SD1=  Percentiles.objects.values_list('valueSD1',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            SD2=  Percentiles.objects.values_list('valueSD2',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            SD3=  Percentiles.objects.values_list('valueSD3',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))
            SD4=  Percentiles.objects.values_list('valueSD4',flat = True).filter(chartName = i, xValue__gt=(qual[deter]-(qual[deter]*0.5)), xValue__lt=(qual[deter]+(qual[deter]*0.5)))

            fig = pt.figure()
            ax = pt.subplot2grid((1,1),(0,0))

            

            ax.plot(x_axis,P01)
            ax.plot(x_axis,P1)
            ax.plot(x_axis,P3)
            ax.plot(x_axis,P5)
            ax.plot(x_axis,P10)
            ax.plot(x_axis,P15)
            ax.plot(x_axis,P25)
            ax.plot(x_axis,P50)
            ax.plot(x_axis,P75)
            ax.plot(x_axis,P85)
            ax.plot(x_axis,P90)
            ax.plot(x_axis,P95)
            ax.plot(x_axis,P97)
            ax.plot(x_axis,P99)
            ax.plot(x_axis,P999)

            if 'weight for age' in i:
                
                if numDays/364 <= 5 and self.obs['wt'].keys()!= [None]:
                    wtZscores = [((((val)/(Percentiles.objects.values_list('valueM',flat = True).filter(chartName = i,xValue =numDays))[0])**
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0]))-1)
                                 /(((Percentiles.objects.values_list('valueS',flat = True).filter(chartName = i,xValue =numDays))[0])*
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0])) for val in self.obs['wt'].keys()]
                    wtPs = [sp.norm.cdf(z) for z in wtZscores]
                    
                    pt.plot(([numDays]*len(self.obs['wt'].keys())),(self.obs['wt'].keys()),'o')
                    
                elif numDays/365 >= 5 and numDays/365 <= 10 and self.obs['wt'].keys()!= [None]:
                    wtZscores = [((((val)/(Percentiles.objects.values_list('valueM',flat = True).filter(chartName = i,xValue =numMonths))[0])**
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numMonths))[0]))-1)
                                 /(((Percentiles.objects.values_list('valueS',flat = True).filter(chartName = i,xValue =numMonths))[0])*
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numMonths))[0])) for val in self.obs['wt'].keys()]
                    wtPs = [sp.norm.cdf(z) for z in wtZscores]

                    pt.plot(([numMonths]*len((self.obs['wt'].keys()))),(self.obs['wt'].keys()),'o')
            
                
            elif 'body mass index' in i:
                
                if numDays/364 <= 5 and self.obs['bmi'].keys()!= [None]:
                    bmiZscores = [((((val)/(Percentiles.objects.values_list('valueM',flat = True).filter(chartName = i,xValue =numDays))[0])**
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0]))-1)
                                 /(((Percentiles.objects.values_list('valueS',flat = True).filter(chartName = i,xValue =numDays))[0])*
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0])) for val in self.obs['bmi'].keys()]
                    bmiPs = [sp.norm.cdf(z) for z in bmiZscores]

                    pt.plot(([numDays]*len(self.obs['bmi'].keys())),(self.obs['bmi'].keys()),'o')
                    
                elif numDays/365 >= 5 and numDays/365 <= 19 and self.obs['bmi'].keys()!= [None]:
                    bmiZscores = [((((val)/(Percentiles.objects.values_list('valueM',flat = True).filter(chartName = i,xValue =numMonths))[0])**
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numMonths))[0]))-1)
                                 /(((Percentiles.objects.values_list('valueS',flat = True).filter(chartName = i,xValue =numMonths))[0])*
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numMonths))[0])) for val in self.obs['bmi'].keys()]
                    bmiPs = [sp.norm.cdf(z) for z in bmiZscores]

                    pt.plot(([numMonths]*len(self.obs['bmi'].keys())),(self.obs['bmi'].keys()),'o')

                
            elif 'height for age' or 'length-height for age' in i:
                
                if numDays/364 <= 5 and self.obs['ht'].keys() != [None]:
                    htZscores = [((((val)/(Percentiles.objects.values_list('valueM',flat = True).filter(chartName = i,xValue =numDays))[0])**
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0]))-1)
                                 /(((Percentiles.objects.values_list('valueS',flat = True).filter(chartName = i,xValue =numDays))[0])*
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0])) for val in self.obs['ht'].keys()]
                    htPs = [sp.norm.cdf(z) for z in htZscores]

                    pt.plot(([numDays]*len(self.obs['ht'].keys())),(self.obs['ht'].keys()),'o')
                    
                elif numDays/365 >= 5 and numDays/365 <= 19 and self.obs['ht'].keys()!= [None]:
                    htZscores = [((((val)/(Percentiles.objects.values_list('valueM',flat = True).filter(chartName = i,xValue =numMonths))[0])**
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numMonths))[0]))-1)
                                 /(((Percentiles.objects.values_list('valueS',flat = True).filter(chartName = i,xValue =numMonths))[0])*
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numMonths))[0])) for val in self.obs['ht'].keys()]
                    htPs = [sp.norm.cdf(z) for z in htZscores]

                    pt.plot(([numMonths]*len(self.obs['ht'].keys())),(self.obs['ht'].keys()),'o')
                
            elif 'head circumference' in i:
                
                if numDays/364 <= 5 and self.obs['hc'].keys()!= [None]:
                    hcZscores = [((((val)/(Percentiles.objects.values_list('valueM',flat = True).filter(chartName = i,xValue =numDays))[0])**
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0]))-1)
                                 /(((Percentiles.objects.values_list('valueS',flat = True).filter(chartName = i,xValue =numDays))[0])*
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0])) for val in self.obs['hc'].keys()]
                    hcPs = [sp.norm.cdf(z) for z in hcZscores]

                    pt.plot(([numDays]*len(self.obs['hc'].keys())),(self.obs['hc'].keys()),'o') 

            elif 'triceps skinfold' in i:
                
                if numDays/364 <= 5 and self.obs['ts'].keys()!= [None]:
                    tsZscores = [((((val)/(Percentiles.objects.values_list('valueM',flat = True).filter(chartName = i,xValue =numDays))[0])**
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0]))-1)
                                 /(((Percentiles.objects.values_list('valueS',flat = True).filter(chartName = i,xValue =numDays))[0])*
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0])) for val in self.obs['ts'].keys()]
                    tsPs = [sp.norm.cdf(z) for z in tsZscores]

                    pt.plot(([numDays]*len(self.obs['ts'].keys())),(self.obs['ts'].keys()),'o')

            elif 'arm circumference' in i:
                
                if numDays/364 <= 5 and self.obs['ac'].keys()!= [None]:
                    acZscores = [((((val)/(Percentiles.objects.values_list('valueM',flat = True).filter(chartName = i,xValue =numDays))[0])**
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0]))-1)
                                 /(((Percentiles.objects.values_list('valueS',flat = True).filter(chartName = i,xValue =numDays))[0])*
                                   ((Percentiles.objects.values_list('valueL',flat = True).filter(chartName = i,xValue =numDays))[0])) for val in self.obs['ac'].keys()]
                    acPs = [sp.norm.cdf(z) for z in acZscores]

                    pt.plot(([numDays]*len(self.obs['ac'].keys())),(self.obs['ac'].keys()),'o')
            '''subscapular skinfold'''
                    

            pt.xlabel('{} in {}'.format((Percentiles.objects.values_list('xValueType',flat = True).filter(chartName = i)[0]).encode('ascii'),
                                            (Percentiles.objects.values_list('xUnit',flat = True).filter(chartName = i)[0]).encode('ascii')))
            pt.title('{} Percentiles'.format(i))
            
            pt.savefig('D:\\weekly\\{} Percentiles for {}'.format(i,self.ide))

            chartPerImg = base64.b64encode(open("D:/weekly/{} Percentiles for {}.png".format(i,self.ide),"rb").read())

            
            post1=re.post('https://fhirtest.uhn.ca/baseDstu3/',headers=headers,data=bundle%(1,str(i),int(self.ide),chartPerImg))

            fig1 = pt.figure()
            ax1 = pt.subplot2grid((1,1),(0,0))

            ax1.plot(x_axis,SD4neg)
            ax1.plot(x_axis,SD3neg)
            ax1.plot(x_axis,SD2neg)
            ax1.plot(x_axis,SD1neg)
            ax1.plot(x_axis,SD0)
            ax1.plot(x_axis,SD1)
            ax1.plot(x_axis,SD2)
            ax1.plot(x_axis,SD3)
            ax1.plot(x_axis,SD4)

            if 'weight for age' in i and self.obs['wt'].keys()!= [None]:
                if numDays/364 <= 5 :
                    pt.plot(([numDays]*len(self.obs['wt'].keys())),(self.obs['wt'].keys()),'o')
                elif numDays/365 >= 5 and numDays/365 <= 19:
                    pt.plot(([numMonths]*len(self.obs['wt'].keys())),(self.obs['wt'].keys()),'o')
                    
            elif 'body mass index' in i and self.obs['bmi'].keys()!= [None]:
                if numDays/364 <= 5:
                    pt.plot(([numDays]*len(self.obs['bmi'].keys())),(self.obs['bmi'].keys()),'o')
                elif numDays/365 >= 5 and numDays/365 <= 19:
                    pt.plot(([numMonths]*len(self.obs['bmi'].keys())),(self.obs['bmi'].keys()),'o')
                
            elif 'height for age' or 'length-height for age' in i and self.obs['ht'].keys()!= [None]:
                if numDays/364 <= 5:
                    pt.plot(([numDays]*len(self.obs['ht'].keys())),(self.obs['ht'].keys()),'o')
                elif numDays/365 >= 5 and numDays/365 <= 19:
                    pt.plot(([numMonths]*len(self.obs['ht'].keys())),(self.obs['ht'].keys()),'o')
                
            elif 'head circumference' in i and self.obs['hc'].keys()!= [None]:
                pt.plot(([numDays]*len(self.obs['hc'].keys())),(self.obs['hc'].keys()),'o')

            elif 'arm circumference' in i and self.obs['ac'].keys()!= [None]:
                pt.plot(([numDays]*len(self.obs['ac'].keys())),(self.obs['ac'].keys()),'o')

            elif 'triceps skinfold' in i and self.obs['ts'].keys()!= [None]:
                pt.plot(([numDays]*len(self.obs['ts'].keys())),(self.obs['ts'].keys()),'o')

            '''subscapular skinfold'''




            pt.xlabel('{} in {}'.format((Percentiles.objects.values_list('xValueType',flat = True).filter(chartName = i)[0]).encode('ascii'),
                                            (Percentiles.objects.values_list('xUnit',flat = True).filter(chartName = i)[0]).encode('ascii')))
            pt.title('{} Z scores'.format(i))
            
            pt.savefig('D:\\weekly\\{} Zscores for {}'.format(i,self.ide))

            chartZImg = base64.b64encode(open('D:\\weekly\\{} Zscores for {}.png'.format(i,self.ide),"rb").read())

            
            post2=re.post('https://fhirtest.uhn.ca/baseDstu3/',headers=headers,data=bundle%(1,str(i),int(self.ide),chartZImg))


            self.respons.update({post1:post1.text})
            self.respons.update({post2:post2.text})
       

        return self.respons
