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

def getTop100Jobs(jobSet, userProfile, past_work_ex, city, state):
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
    return X




# Add City and State and Major too.
@api_view(['POST'])
def recommend(request):
    if request.method == 'POST':
        serializer = JobApplicantSerializer(data=request.data)
        # print('Valid',serializer.is_valid())
        if serializer.is_valid():
            # Convert input data to input format for model
            input_data = serializer.validated_data
            # Convert categorical values to numerical values
            input_data['currentlyEmployed'] = 1 if input_data['currentlyEmployed'] == 'Yes' else 0
            input_data['managedOthers'] = 1 if input_data['managedOthers'] == 'Yes' else 0
            degree_mapping = {
                'None': 0,
                'High School': 1,
                'Vocational': 2,
                'Associate\'s': 3,
                'Bachelor\'s': 4,
                'Master\'s': 5,
                'PhD': 6
            }
            degree = input_data['degree']
            input_data['degree'] = degree_mapping.get(input_data['degree'], 0)  

            input_data_list = [input_data[field] for field in ['degree', 'workHistoryCount', 
                                                               'yearsOfExp', 'currentlyEmployed',
                                                               'managedOthers', 'managedHowMany']]
            
            input_data_tf_idf_degree = degree + ' ' + input_data['major'] + ' ' + str(input_data['yearsOfExp'])
            input_data_transformed = tfidf_vectorizer.transform([input_data_tf_idf_degree])

            cosine_similarities = cosine_similarity(input_data_transformed, tfidf_matrix)
            top_similar_users_indices = cosine_similarities.flatten().argsort()[::-1][:10]
            most_similar_user = users.iloc[top_similar_users_indices]

            # Get the top 100 jobs that similar users have applied in
            top_jobs = getTopJobs(most_similar_user['UserID'].values)

            # Now, re-rank the above 100 jobs and recommend the Top 20
            top100Jobs = getTop100Jobs(top_jobs, input_data_list, input_data['workHistory'], input_data['city'], input_data['state'])

            prediction = model.predict(top100Jobs)

            top_jobs_list = list(top_jobs)
            job_predictions = {}

            # Iterate over each job ID in top_jobs and corresponding prediction value
            for i, job_id in enumerate(top_jobs_list):
                
                prediction_value = prediction[i][0]
               
                job_predictions[job_id] = prediction_value
            
            sorted_job_predictions = dict(sorted(job_predictions.items(), key=lambda item: item[1], reverse=True))

            recommended_jobs = []

            for job_id, prediction_value in sorted_job_predictions.items():
                if job_id in jobs['JobID'].values:

                    job_title = jobs[jobs['JobID'] == job_id]['Title'].values[0]
                    job_description = jobs[jobs['JobID'] == job_id]['DescCleaned'].values[0]
                  
                    recommended_jobs.append({'job_id': job_id, 'job_title':job_title, 'job_description': job_description})
                else:
                    print(f"Job ID {job_id} not found in the jobs dataset.")

                if (len(recommended_jobs) >= 20):
                    break

            return Response({'recommended_jobs': recommended_jobs}) 
        else:
            # If serializer is not valid, return the errors
            return Response(serializer.errors, status=400)
    else:
        # If the request method is not POST, return an error
        return Response({'error': 'Only POST requests are allowed'}, status=405)
