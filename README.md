# growthcharts-API
an API to interpret anthropometric measurements from HAPI FHIR server producing growth charts images as FHIR observation instances.

first of all this is a beginner's work published to share the business knowledge and enhance the code via gurus input.

i'll upload a proper documentation later.

the basic concept is: a health app would request a certain patient to be assessed via WHO growth charts logic. growthcharts-API would query hapi-fhir server for patient's demographics and anthropometeric measurements (weight, height, body mass index, head circumference, arm circumference, triceps skinfold, subscapular skinfold) then run the logic on it producing image charts which sent to hapi-fhir server as observation object instances.

what is uploaded so far is the models, url, views, database and business logic (responder.py).

WHO data source : http://www.who.int/childgrowth/standards/en/

to be continued and supported with proper documentation file.
