# revels-learning
The aim of this project is primarily for personal learning, but hosted open-source in the hope that others may find it useful. It is an attempt to create
 a raw dataset through data collection and ultimately build a machine learning model capable of classifying (predicting) the type of revel based on only
a few physical parameters (mass, height, width, etc).  

## Data collection method
Data was collected manually through physical measaurement of 10 bags of revels chocolates (1.2KG). This can then be randomly split into training and vali
dation data.  Before new data can be collected and used to test the machine learning model. 

## Database schema
The database has 4 tables, shops, bags, types and finally data.  With the following data types and relations:

### Shops
This table provides us with the ability to trace where specific samples originated from (i.e. the shop where they were bought).

Column Name | Type | Foreign Key
------------|------|------------
id | serial | none
shop_name | text | none
address_1 | text | none
address_2 | text | none
address_3 | text | none
postcode | text | none

### Bags
This table provides us with information specific to each bag, specifically it's total weight and price.

Column Name | Type | Foreign Key
------------|------|------------
id | serial | none
shop_bought | integer | shops(id)
price | real | none

### Types
Provide the textual prepresentation of the Revel type.

Column Name | Type | Foreign Key
------------|------|------------
id | serial | none
type_name | text | none

### Data
The main data table, with all data specific to each sample. 

Column Name | Type | Foreign Key
------------|------|------------
id | serial | none
bag_id | integer | bags(id)
revel_type | integer | types(id)
mass | real | none
density | real | none
height | real | none
width | real | none 
depth | real | none


## Running the project
The project was initally completed using cloud computing (Amazon Web Services) resources, it is the aim of the project however to provide some docker images to allow the casual user to clone and run this project themselves on any machine that has docker installed. 
