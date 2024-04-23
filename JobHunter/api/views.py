from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
import joblib
from tensorflow.keras.models import load_model
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import os
from .serializers import JobApplicantSerializer
import pandas as pd

# Get the path to the pickled model file
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'keras_model.h5')

tfidf_vectorizer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'tfidf_vectorizer.pkl')
tfidf_matrix_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'tfidf_matrix.pkl')
jobdesc_tfidf_matrix_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'job_description_tfidf_matrix.pkl')

users_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'modified_users.csv')
apps_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'application_record.csv')
jobs_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'jobs.csv')

job_vectorizer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'job_description_tfidf.pkl')
work_history_vectorizer_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'work_history_tfidf.pkl')


# Load the pickled model
model = load_model(model_path)
tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)
job_vectorizer = joblib.load(job_vectorizer_path)
work_history_vectorizer = joblib.load(work_history_vectorizer_path)

tfidf_matrix = joblib.load(tfidf_matrix_path)
jobdesc_tfidf_matrix = joblib.load(jobdesc_tfidf_matrix_path)


users = pd.read_csv(users_path)
apps = pd.read_csv(apps_path)
jobs = pd.read_csv(jobs_path)


def getTopJobs(userIds):
    jobsSet = set()
    for user in userIds:
        jobsAppliedTo = apps[apps['UserID']==user]
        jobsAppliedTo = jobsAppliedTo['JobID'].values

        for job in jobsAppliedTo:
            jobsSet.add(job)
            if (len(jobsSet) > 100):
                break
        if (len(jobsSet) > 100):
                break
    
    return jobsSet

def getTop20Jobs(jobSet, userProfile, past_work_ex, city, state):
    # Firstly, we create the user_profile to training_data form
    user_feature = np.array(userProfile)
    work_ex_transform = work_history_vectorizer.transform([past_work_ex])
    user_feature = np.concatenate((user_feature, work_ex_transform.toarray()[0]))

    X = np.zeros((1,158))

    # Then, we add the job_transform_tfidf to the user
    for jobId in jobSet:
        jobInfo = jobs[jobs['JobID'] == jobId]
        jobDesc = jobInfo.Title + jobInfo.DescCleaned + jobInfo.ReqCleaned
    
        # print(jobInfo.index.values)
        idx = jobInfo.index.values[0]
        feature = np.concatenate((user_feature, jobdesc_tfidf_matrix[idx, :].toarray()[0]))

        if jobInfo['City'].values[0] == city:
            feature = np.append(feature, [1])
        else:
            feature = np.append(feature, [0])

        if jobInfo['State'].values[0] == state:
            feature = np.append(feature, [1])
        else:
            feature = np.append(feature, [0])

        feature = feature.reshape(1,158)
        X = np.concatenate((X, feature), axis=0)

    # Finally, we rank all of them based on the probabilities of model prediction
    




# Add City and State and Major too.
@api_view(['POST'])
def recommend(request):
    if request.method == 'POST':
        # Deserialize the input data from the request
        serializer = JobApplicantSerializer(data=request.data)
        if serializer.is_valid():
            # Convert input data to input format for model
            input_data = serializer.validated_data
            # Convert categorical values to numerical values
            input_data['currently_employed'] = 1 if input_data['currently_employed'] == 'Yes' else 0
            input_data['managed_others'] = 1 if input_data['managed_others'] == 'Yes' else 0
            degree_type_mapping = {
                'None': 0,
                'High School': 1,
                'Vocational': 2,
                'Associate\'s': 3,
                'Bachelor\'s': 4,
                'Master\'s': 5,
                'PhD': 6
            }
            input_data_degree_notencoded = input_data['degree_type']
            input_data['degree_type'] = degree_type_mapping.get(input_data['degree_type'], 0)  

            input_data_list = [input_data[field] for field in ['degree_type', 'work_history_count', 
                                                               'total_years_experience', 'currently_employed',
                                                               'managed_others', 'managed_how_many']]
            
            input_data_as_numpy_array = np.asarray(input_data_list)
            input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
            input_data_tf_idf_degree = input_data_degree_notencoded + ' ' + input_data['major'] + ' ' + str(input_data['total_years_experience'])
            input_data_transformed = tfidf_vectorizer.transform([input_data_tf_idf_degree])

            # print("Shape of transformed data is: ", input_data_transformed.shape)
            # print("Shape of matrix data is: ", tfidf_matrix.shape)


            cosine_similarities = cosine_similarity(input_data_transformed, tfidf_matrix)
            top_similar_users_indices = cosine_similarities.flatten().argsort()[::-1][:10]
            most_similar_user = users.iloc[top_similar_users_indices]

            # print("Most similar user:")
            # print(most_similar_user['UserID'].values)

            # Get the top 100 jobs that similar users have applied in
            top_jobs = getTopJobs(most_similar_user['UserID'].values)
            # print(len(top_jobs))

            # Now, re-rank the above 100 jobs and recommend the Top 20
            top20Jobs = getTop20Jobs(top_jobs, input_data_list, input_data['past_work_ex'], input_data['city'], input_data['state'])








            return Response({'predicted_cost'}) 
        else:
            # If serializer is not valid, return the errors
            return Response(serializer.errors, status=400)
    else:
        # If the request method is not POST, return an error
        return Response({'error': 'Only POST requests are allowed'}, status=405)
