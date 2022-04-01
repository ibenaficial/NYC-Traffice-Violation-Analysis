# NYC Traffic Violation Analysis
Bena Huang
<br>10/27/21
## Building and Running Docker Image
Before doing anything, you must first create an EC2 server on Amazon. Once the server has been
created, we can go into the file browser to create the “project01” folder and our necessary files:
Dockerfile, requirements.txt, and main.py.
<br>To build a docker image, we change our directory to our “project01” folder using the “cd” command in
our terminal instance. Then run the following:
### Docker build -t bigdata1:1.0 project01/
To run the docker image, we use the following command in our terminal instance:
docker run \
#### -v $PWD:/app \
#### -e DATASET_ID="nc67-uf89" \
#### -e APP_TOKEN="q04ia5gRnoMvCEigomLaSj3yc" \
#### -e INDEX_NAME="violations" \
#### -e ES_HOST="https://search-sta9760f2021benaiwyjfy4gdryoipo46uyctn3voa.us-east-2.es.amazonaws.com" \
#### -e ES_USERNAME="bena" \
#### -e ES_PASSWORD="Sta9760f2021bena@" \
#### project01:1.0 --page_size=3 –num_pages=2
<br><br>**DATASET_ID** – The dataset that we are using is from NYC Open Data. It is the Open Parking and Camera
Violations dataset.
<br><br>**APP_TOKEN** – The app token is used to access the dataset using the Socrata API. This app token is
unique to each user.
<br><br>**INDEX_NAME** – This is the name we give our index. To create a new index, we simply name it a different
name.
<br><br>**ES_HOST** – This is the Amazon Elasticsearch url where our data will be loaded to
<br><br>**ES_USERNAME** – The username login for our Elasticsearch instance
<br><br>**ES_PASSWORD** – The password login for our Elasticsearch instance
<br><br>**--page_size –num_pages** – These are commands that are used after we import the argparse library. “—
page_size” states how many lines of data we want to load, and “—num_pages” specifies how many calls
to the API. For example, “—page_size=3 –num_page=2” will result in 6 lines of rows being loaded: 2 calls
for 3 lines each.

This way of running the docker image also requires us to import the “os” library. In our “main.py” file,
we will have to specify the following:
#### DATASET_ID = os.environ["DATASET_ID"]
#### APP_TOKEN = os.environ["APP_TOKEN"]
#### INDEX_NAME = os.environ["INDEX_NAME"]
#### ES_HOST = os.environ["ES_HOST"]
#### ES_USERNAME = os.environ["ES_USERNAME"]
#### ES_PASSWORD = os.environ["ES_PASSWORD"]

In the scenario where we create a new index or a new Elasticsearch instance, we can easily plug in the
new values into our docker run command instead of having to edit our original code.
## Specifications within “main.py” code

In order to properly index data in our Elasticsearch index, we have to correctly map all fields in our code
into a usable format. For example, in the original dataset, the “issue_date” field is a text type. But in
order to be able to properly use this data in Elasticsearch, this needs to be changed to a date type. Other
fields of interest that I used were “fine_amount”, “penalty_amount”, “precinct”, “county”,
“issuing_agency” to name a few. Fields with numbers were mapped as integer types, and “precinct”,
“county”, and “issuing_agency” were mapped as keyword types. In the original dataset, these fields
were text types, but I soon realized when making my visuals that Kibana does not recognize text type
strings as aggregable fields. Therefore, I couldn’t use it in my visualizations. By changing the field type to
keyword, we’re able to aggregate and create visuals utilizing these fields.

![image](https://user-images.githubusercontent.com/102686618/161180796-19a1aa3a-2c18-46a7-8f40-9d5152dd409b.png)

However, to actual load data into our Elasticsearch instance, we also need to create a “client.get” script.
This allows us to pull in only the fields that we need. To keep our data valid and to avoid any missing
fields in data rows, I made an if statement for each field that I was indexing. If a certain row of data was
missing a certain field, then instead of skipping that row, it would fill in that field with “MISSING”.

To also ensure that we’re not loading the same data rows over and over again into Elasticsearch, we also
need to keep our data in order. By using the “summons_number”, we order our dataset by the
summons number.

![image](https://user-images.githubusercontent.com/102686618/161180831-d4ce85b8-ac1b-4133-92da-12861813ddb8.png)

## Visualizations in Kibana

In Kibana, we’re able to use the data that we loaded to create graph visuals showing the spread of data.
Some of the graphs I decided to create looked at which county had the greatest number of tickets
issued, and which issuing agency issued the greatest number of tickets. We can see that the county with
the greatest number of tickets issued was NY (aka Manhattan), followed by Kings (Brooklyn), Queens,
Bronx, and Staten Island. The issuing agency that issued the greatest number of tickets was the Police
Department, followed by Department of Sanitation, Traffic, and Con Rail. Neither analysis were
surprising to me, as it’s well known that Manhattan is the busiest borough with the most cars, and the
Police Department is responsible for issuing most of the tickets.

A fifth visual I created was a data table, showcasing the number of rows that was loaded into
Elasticsearch. By using the _id field, we can see that a total of 103,189 rows were loaded.
