# revels-learning
The aim of this project is primarily for personal learning, but hosted open-source in the hope that others may find it useful. It is an attempt to create
 an original data set through data collection and build a machine learning model capable of classifying (predicting) the type of revel based on only
a few physical parameters (mass, height, width, etc).

This project is not by data scientists, but by an interested infrastructure engineer using this to learn.  
As such the project also serves as a good introduction to running docker containers, building your own containers etc.

## Data collection method
Our data was collected manually through physical measurement of 10 bags of revels chocolates (approximately 1.2KG). The general method was as follows.

* Put a glass of water in the fridge, this is a cool project and the water needs to be just as cool!
* Grab a bag
* Record bag data into database (total mass, price, shop bought)
* Write bag number on face of bag (bag_id) (if not already done)
* Open the bag & for each revel in the bag
    * Measure its mass (in grams)
    * Measure its density (in g/cm3)
    * As step two requires it to get wet, dry it off.
    * Measure its height
    * Measure its width
    * Measure its depth
    * eat the sample to confirm it's type
    * Record data into database along with it's bag number
    * Repeat above steps for every sample in the bag
* Repeat for all ten bags.

### Equipment used for data collection
* Accurate Scales (0.01g resolution)
* Vernier Calipers (0.02mm resolution)
* Water - For measuring specific gravity and therefore density
* Cotton Thread (for suspending sample in liquid)
* Plastic drinking cups, straws, tape etc. (for making density measurement rig)

### The Maths
Working out the density of a solid using archimedes principle requires using a
bit of maths, all we did was follow [this lab sheet](https://www.unr.edu/Documents/science/physics/labs/151/09_Archimedes_Principle.pdf).

## Running the project
I aim to make this project trivial to run yourself, to this end I have decided to run it all in docker, this means you
only have to download and install one piece of software (Docker) and will be able to run this project and many others!

### Install pre-requisite software
* [Docker](https://store.docker.com/search?type=edition&offering=community)

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
This tells docker to build in the context of the current directory `.` and create an image with a tag of `revels` and
version of `latest`. 

Once complete you can confirm you have built the container by running `docker images` and you should see a `revels` repository
at tag `lastest`.

### Start a database container
We will use the official postgres 9.6 image as the database backend for this project.  Start the DB container by running:
```bash
docker run -d --name revels-db -e POSTGRES_PASSWORD=somepassword postgres:9.6
```
Just choose a admin database password you like... you will need it later when starting the ML container. 

### Start the revels-ml container
Now start up the ML container you built earlier by running: 
```bash
docker run -it --name revels-ml --link revels-db -e REVELS_DB_ADMIN_PASS=somepassword -v ${PWD}:/project revels
```
As we ran this with "The interactive flags (-it)" set, this will start the container and attach our terminal to the IO
streams of the container (giving us a shell on the container).  

From within the container you can now use the ML code to train models and predict revels!

### Train the models
There is some more bootstrapping code that will train 5 common machine learning
algorithms (models) and save the model to the database in a table:

* Logistic Regression
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
python3 revels/run.py train [validation-split]
```

This command will check to see if the database already exists and if not create it and load the data, then train the 5 
aforementioned models and persist them back in the database for later use along with some metadata for each model 
pertaining to their accuracy, f1 score etc. 

Validation-split is the amount of data to keep back for validation steps (0.2 = 20% of data kept for validation)

### Train the models (without persisting to DB)
Sometimes, you may just want to get the scores for a particular set of training parameters without saving the mdoels to
the DB.  In that instance, just run the `validate` argument (same parameters as `train` argument).
```shell
python3 revels/run.py validate [validation-split]

```

### Cross validation scoring for models
```shell
python3 revels/run.py x-val-score [validation-split] [k-fold] [random-seed]
```

### Showing a summary
This step is not necessary, however can be nice to see a textual representation of some basic stats for each type of 
revel in the current data set.

```shell
python3 revels/run.py summary
```
This gives you things like the mix/max/average of each variable grouped by type.

### Showing the results
To get a list of the results of model training, simply run:

```shell
python3 revels/run.py results [number]
```

This essentially just fetches top `number` models (sorted by accuracy) from the database and reports on the algorithm used. 

### Predicting a revel
This is the heart of the machine learning project, actually taking some 
measurements, querying a model to provide us with a prediction as to what kind 
of revel it is.  To do this simply take the measurements of your revel:

    <-  width ->
     ----------
    /          \
    \          /
     ----------

All dimesnsions are in mm, mass is in grams and density in g/cm3.  When we did this we simply lay the revel longest side
"across" (left-right) on the desk and then that was "width", depth was front-back and height was how high it stood off the 
desk. 

To get the models to predict on a revel, simply run:

```shell
python3 pyt/run.py predict
```

This will then interactively ask for the data of the revel, and also ask which 
model you would like to test.  

It will then output the classification it believes the sample belongs to, along with it's certainty (as %).

