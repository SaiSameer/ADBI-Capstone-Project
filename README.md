# Business Recommendations using Prediction of Review Rating

# Download and install any missing packages that are used.

1. Download the yelp academic dataset and copy the json files to a folder named dataset placed in the same directory as preprocess.py
2. Run the preprocess.py file to read the business json data, filter it based on category and city to 'Restaurants' and 'Pittsburgh' respectively. This filtered dataset is written as a new file named review_pittsburgh_restaurant.json which will be used for our project
3. Run the symmetrickl.py to find the optimal number of topics for LDA from the plot between the Symmetric KL Divergence and No of topics
4. Run training.py in Topic_Modelling to train the LDA model and populate the optimal number of topics we found in the previous step though Symmetric KL Divergence
5. Run display.py to display the results based on business ID of interest.
