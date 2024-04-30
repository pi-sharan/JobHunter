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
