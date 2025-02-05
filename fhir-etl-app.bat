@echo off
echo [%date% %time%] Starting fhir-etl Docker App
docker run --rm -it fhir-etl 
echo [%date% %time%] Docker fhir-etl App Finished
pause