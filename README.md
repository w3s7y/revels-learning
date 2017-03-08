# revels-learning
The aim of this project is primarily for personal learning, but hosted open-source in the hope that others may find it useful. It is an attempt to create
 a raw dataset through data collection and ultimately build a machine learning model capable of classifying (predicting) the type of revel based on only
a few physical parameters (mass, height, width, etc).  

## Data collection method
Our data was collected manually through physical measaurement of 10 bags of revels chocolates (approx 1.2KG). The general method was as follows. 

1. Grab a bag
1. Record bag data into database (total mass, price, shop bought)
1. Write bag number on face of bag (bag_id)
1. Open the bag & for each revel in the bag
  1. Measure its mass (in grams)
  1. Measure its density (in g/cm3)
  1. As step two requires it to get wet, dry it off.
  1. Measure its height
  1. Measure its width
  1. Measure its depth
  1. eat the sample to confirm it's type
  1. Record data into database along with it's bag number
  1. Repeat above steps for every sample in the bag
1. Repeat for all ten bags.

### Equipment used for data collection
* Accurate Scales (0.01g resolution)
* Vernier Calipers (0.02mm resolution)
* Distilled Water - For measuring specific gravity and therefore density
* Cotton Thread (for suspending sample in liquid)
* One penny piece (used as a sinker for samples that floated (the malteasers))

### The Maths
Working out the density of a solid using archimedes principle requires using a 
bit of maths, all we did was follow [this excellent educational lab sheet](https://www.unr.edu/Documents/science/physics/labs/151/09_Archimedes_Principle.pdf).

## Database schema
The database has 4 tables, shops, bags, types and finally data.  
With the following data types and relations:

### Shops
This table provides us with the ability to trace where specific samples 
originated from (i.e. the shop where they were bought).

Column Name | Type | Foreign Key
------------|------|------------
id | serial | none
shop_name | text | none
address_1 | text | none
address_2 | text | none
address_3 | text | none
postcode | text | none

### Bags
This table provides us with information specific to each bag, 
specifically it's total weight and price.

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
The project was initally completed using cloud computing (Amazon Web Services) 
resources, it is the aim of the project however to provide some docker images 
to allow the casual user to clone and run this project themselves on any 
machine that has docker installed. 
