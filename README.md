# Ed-Fi Data Loader


```bash

python src/app.py;
curl http://localhost:8080;
curl -i -H "Content-Type: application/json" -X POST \
    -d '{"bucketName": "k12-analytics-engineering", "filePath":"/AssessmentResults.csv", "templateName": "NWEA MAP Growth Assessment Results", "schoolYear": "2021"}' \
    http://localhost:8080;

```
