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
* Docker (we used 17.03.00-ea) but anything after this will *probably* be fine
* Docker-compose (1.12.0) or the latest stable version.

I would put git in this list, however it is not required but more a nice
to have as you can download the zip of this project directly from github.

### Get the project code
Either use git to clone this project (as mentioned above) or just download it
to a folder of your choosing and unzip it *into your home directory*. (For the purposes of this readme,
we shall assume you have unzipped it to `/home/user/revels-learning`).

### Start the environment
In the root of the folder there is a ```docker-compose.yaml``` this will create
a docker network and 2 containers in that network.  A single Postgresql database
instance and also a python data science container.

```shell
cd ${HOME}/revels-learning
docker-compose up -d
```
This docker compose command will create a docker network (so the images can talk
to each other) and start the containers.

### Get a shell on the python container
Next up, simply run `docker exec` to connect to the running python container

```shell
docker exec -it revelslearning_python_1 bash
```

### Use the scripts to load the data into the database.
As the containers are started empty, we need to load the data from a pg_dump file
into your database, this is done by running the bootstrap script with the
`do-initial-dataload` argument from within the python container:

```shell
python pyt/bootstrap.py do-initial-dataload
```  

This script will create a database user called `scienceuser` with a password of
`sicenceuser` and also execute the sql scripts `psql/create_db.sql` and
`psql/dbdump.sql`.  This will put the database into a usable state for the
remainder of the project.

### Train the models
There is some more bootstrapping code that will train 6 common machine learning
algorithms (models):

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
python pyt/bootstrap.py do-train-model
```

This will load the data out of the database into a pandas data frame,

### Showing a summary
This step is not necessary, however can be nice to see a textual representation
of the data.

```shell
python pyt/bootstrap.py do-show-summary
```

### Showing the results
To get a list of the results of model training, simply run:

```shell
python pyt/bootstrap.py do-show-results
```

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
python pyt/bootstrap.py do-predict-revel
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

## Execution environment
I have created a docker image which has all of the necessary modules and
programs installed to run this project.  This can be found on [docker hub](https://hub.docker.com/w3s7y/scientific-python)
You may also pull it directly into your local repo with
```docker pull benwest/scientific-python```

## Unit testing the project
Unit tests are written in pytest which making unit testing the project trivial.
Simply enter the root directory of the project and execute ```pytest -r p```
the ```-r p``` isn't even required, just gives info on each test executed.
*DO NOT RUN THE UNIT TESTS AGAINST A PRODUCTION DATABASE*
