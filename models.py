# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Percentiles(models.Model):

    identifier = models.AutoField(primary_key = True)
    chartName = models.CharField(max_length = 264)
    xValueType = models.CharField(choices = (('age','age'),('height','height')), max_length = 10)
    xValue = models.IntegerField()
    xUnit = models.CharField(choices = (('days','days'),('months','months'),('cm','cm')), max_length = 10)
    genderValue = models.CharField(choices = (('male','male'),('female','female')),max_length = 10)
    valueL = models.FloatField()
    valueM = models.FloatField()
    valueS = models.FloatField()
    valueP01 = models.FloatField()
    valueP1 = models.FloatField()
    valueP3 = models.FloatField()
    valueP5 = models.FloatField()
    valueP10 = models.FloatField()
    valueP15 = models.FloatField()
    valueP25 = models.FloatField()
    valueP50 = models.FloatField()
    valueP75 = models.FloatField()
    valueP85 = models.FloatField()
    valueP90 = models.FloatField()
    valueP95 = models.FloatField()
    valueP97 = models.FloatField()
    valueP99 = models.FloatField()
    valueP999 = models.FloatField()
    valueSD4neg = models.FloatField()
    valueSD3neg = models.FloatField()
    valueSD2neg = models.FloatField()
    valueSD1neg = models.FloatField()
    valueSD0 = models.FloatField()
    valueSD1 = models.FloatField()
    valueSD2 = models.FloatField()
    valueSD3 = models.FloatField()
    valueSD4 = models.FloatField()

    def __str__(self):
        return '{} {} {} {} {}'.format(self.chartName,self.xValueType,self.xValue,self.xUnit,self.genderValue)
'''
class Zscores(models.Model):

    identifier = models.AutoField(primary_key = True)
    chartName = models.CharField(max_length = 264)
    ageValue = models.IntegerField()
    genderValue = models.CharField(choices = (('male','male'),('female','female')),max_length = 10)
    ageUnit = models.CharField(choices = (('d','days'),('m','months')), max_length = 10)
    valueSD4neg = models.FloatField()
    valueSD3neg = models.FloatField()
    valueSD2neg = models.FloatField()
    valueSD1neg = models.FloatField()
    valueSD0 = models.FloatField()
    valueSD1 = models.FloatField()
    valueSD2 = models.FloatField()
    valueSD3 = models.FloatField()
    valueSD4 = models.FloatField()

    def __str__(self):
        return '{} {} {} {}'.format(self.chartName,self.ageValue,self.ageUnit,self.genderValue)
''' 

    



