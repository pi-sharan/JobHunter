# JobHunter
Since the dataset consisted of more than 1 million jobs and user information. Due to memory restrictions and ease of convenience, we have considered the users who have applied in the duration of window 6. Since the dataset only contains information about the users and the jobs they have applied. For our recommendation system, we have considered negative sampling. It means that equal to the number of jobs users have applied, we will consider the jobs the users have not applied in our training data. So that we get a balanced dataset suitable for classification.
Here we are performing the following tasks
1]  Our primary objective is to develop a binary classification model capable of predicting whether a user will apply for a job or not, based on their respective profiles.
2] Using user-user similarity we will retrieve the 100 jobs by fetching the jobs applied by the similar users of the current user 
3] Given the top 100 jobs, we will estimate the ranking of these jobs, so that we can recommend the user to the job that holds the top rank

Classification Results:
| **Models**           | **Accuracy** | **Precision** | **Recall** | **F1**|
|------------------|----------|-----------|--------|-------|
| Linear Regression| 0.5150   | 0.515     | 0.5157 | 0.5153|
| Random Forest    | 0.635    | 0.634     | 0.639  | 0.636 |
| Xgboost          | 0.5776   | 0.5778    | 0.5786 | 0.5780|
| Adaboost         | 0.535    | 0.534     | 0.541  | 0.538 |
| Neural Network   | 0.830    | 0.852     | 0.849  | 0.858 |
| Text CNN         | 0.818   | 0.842     | 0.851  | 0.8437|
| CNN LSTM         | 0.845    | 0.831     | 0.832  | 0.879 |
| Word2Vec Neural Network | 0.850 | 0.937 | 0.751 | 0.834 |

# Locally Deploying Website
You can run our website frontend and backend using the following steps:

## Front-end UI:

Install npm if not already installed.

Go to the Frontend UI / job-hunter folder. 

1. Run ```npm install```
2. Run ```npm start```

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

## Backend (Django):

Install Django if not already installed.

Go the JobHunter Folder.

Run ```python manage.py runserver```

This would open both Front-end and Backend on localhost.

## Usage:

1. Go to [http://localhost:3000](http://localhost:3000) on your browser. It will show the following form - 


<img src="https://github.com/pi-sharan/JobHunter/assets/57253436/b659474f-eb38-4b9a-967a-75967cb145af" height="600">

2. After filling in the required details press submit. It would lead you to the recommended jobs website.

   <img src="https://github.com/pi-sharan/JobHunter/assets/57253436/20dd63d1-4003-45a2-b45d-90b58191fb4f" height="500">


# Recommendation Algorithm:

## Bayesian Personalized Ranking Approach:

Initially we tried the BPR based recommendation, where we converted the User-Job applications to a binary 0/1 interaction matrix, based on if the user has applied to the job or not. Then, we tried User-User and Item-Item Collaborative Filtering, Matrix Factorization and Neural Collaborative Filtering methods. However, these did not give good results. Possibly due to the compressing of interaction to 0/1 hard labels. 

![MF](https://github.com/pi-sharan/JobHunter/assets/57253436/473cda15-24a0-41b7-b1e8-ea53923fff36)

## Final Approach:

![finalmodel](https://github.com/pi-sharan/JobHunter/assets/57253436/bb55704e-8e94-463c-9361-dea9e85624af)

Find more details about it at - [https://sites.google.com/view/jobhunteasy/home]




