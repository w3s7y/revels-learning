# revels-learning
The aim of this project is primarily for personal learning, but hosted open-source in the hope that others may find it useful. It is an attempt to create
 a dataset through data collection and ultimately build a machine learning model capable of classifying (predicting) the type of revel based on only
a few physical parameters (mass, height, width, etc).

This project is not by data scientists, but by a couple of infrastructure engineers
using this to learn.

## Data collection method
Our data was collected manually through physical measurement of 10 bags of revels chocolates (approximately 1.2KG). The general method was as follows.

1. Put a glass of water in the fridge, this is a cool project and the water needs to be just as cool!
1. Grab a bag
1. Record bag data into database (total mass, price, shop bought)
1. Write bag number on face of bag (bag_id) (if not already done)
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
* Water - For measuring specific gravity and therefore density
* Cotton Thread (for suspending sample in liquid)

### The Maths
Working out the density of a solid using archimedes principle requires using a
bit of maths, all we did was follow [this excellent educational lab sheet](https://www.unr.edu/Documents/science/physics/labs/151/09_Archimedes_Principle.pdf).

## Running the project
We aim to make this project trivial to run yourself, to this end we have
prepared a couple of docker images in addition to this project which should
make it easy for anyone to run this project.

### Install pre-requisite software
* Docker (I used 17.03) but anything after this will *probably* be fine

I would put git in this list, however it is not required but more a nice
to have as you can download the zip of this project directly from github.

### Get the project code
Either use git to clone this project (as mentioned above) or just download it
to a folder of your choosing and unzip it *into your home directory*. (To follow along at home, `cd` into the project
directory).

### Build the ML container
There is a Dockerfile in the repo which will build you a container to run the ML project in, you can build it by running:
```bash
docker build -t revels:latest .
```

### Start a postgres container
We will use the official postgres 9.6 image for this project.  Start one up by running:
```bash
docker run -d --name postgres -e POSTGRES_PASSWORD=somepassword postgres:9.6
```
Just choose a admin database password you like... you will need it later when starting the ML container. 

### Start the ML container
Now start up the ML container interactively 
```bash
docker run -it --name revels --link postgres -e REVELS_DB_ADMIN_PASS=somepassword revels
```

### Train the models
There is some more bootstrapping code that will train 6 common machine learning
algorithms (models) and save the model to the database in a table:

* Logistic Regression
* Linear Discrimination Analysis
* K Nearest Neighbour
* Descision Tree Classifier
* Gaussian Naive Bayes
* Support Vector Machines

Each of these models are classification algorithms (supervised learning) where
by we tell the algorithm the results while it's learning.  This is opposed to
clustering algorithms (unsupervised) where we don't give it any classification
and it trains to put observations into clusters (groups).

To train the models (and save the trained models to disk) simply execute:

```shell
python pyt/run.py train-models
```

This command will check to see if the database already exists and if not create it and load the data, then train the 6 
aforementioned models and persist them back in the database for later use along with some metadata for each model 
pertaining to their accuracy, f1 score etc. 

### Showing a summary
This step is not necessary, however can be nice to see a textual representation
of the data.

```shell
python pyt/run.py summary
```

This gives you a very basic statistical summary of the data set.

### Showing the results
To get a list of the results of model training, simply run:

```shell
python pyt/run.py results
```

This essentially just fetches the metadata from the database and prints it out. 

### Predicting a revel
This is the heart of the machine learning project, actually taking some 
measurments, querying a model to provide us with a prediction as to what kind 
of revel it is.  To do this simply take the measurements of your revel:

    <-  width ->
     ----------
    /          \
    \          /
     ----------

All dimesnsions are in mm, mass is in grams and density in g/cm3.

To get the models to predict on a revel, simply run

```shell
python pyt/run.py predict
```

This will then interactively ask for the data of the revel, and also ask which 
model you would like to test.  

It will then output the classification it believes the sample belongs to. 

## Project structure
The project files are split up into the following folders:

#### /psql
Contains the Postgresql schema creation file.

#### /pyt
Contains the main python machine learning and database IO modules.
This is where the bulk of the project code lives.

#### /unittests
Contains pytest modules for testing the code in pyt folder.

#### secrets_template.py
This file needs to be renamed to ```secrets.py``` in order for the pytest to
pick up the correct database connection details in order to test the db
connection code and also used by the machine learning code itself to pick up
the database connection details.

## Unit testing the project
Unit tests are written in pytest which making unit testing the project trivial.
Simply enter the root directory of the project and execute ```pytest -r p```
the ```-r p``` isn't even required, just gives info on each test executed.
*DO NOT RUN THE UNIT TESTS AGAINST A PRODUCTION DATABASE*
