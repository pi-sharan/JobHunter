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
users_path= os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'modified_users.csv')

# Load the pickled model
model = load_model(model_path)
tfidf_vectorizer = joblib.load(tfidf_vectorizer_path)
users = pd.read_csv(users_path)
tfidf_matrix = joblib.load(tfidf_matrix_path)

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
            # users['DegreeType'] = users['DegreeType'] + ' ' + users['Major'] + ' ' + users['TotalYearsExperience']      

            input_data_list = [input_data[field] for field in ['degree_type', 'work_history_count', 
                                                               'total_years_experience', 'currently_employed',
                                                               'managed_others', 'managed_how_many']]
            # input_data_list.extend(input_data['workexp'])
            input_data_as_numpy_array = np.asarray(input_data_list)
            input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
            # Print the input data to the console
            # print("Input Data:", input_data_reshaped)
            input_data_tf_idf_degree = input_data_degree_notencoded + ' ' + input_data['major'] + ' ' + str(input_data['total_years_experience'])
            print("The input data"+input_data_tf_idf_degree)
            input_data_transformed = tfidf_vectorizer.transform([input_data_tf_idf_degree])

            cosine_similarities = cosine_similarity(input_data_transformed, tfidf_matrix)
            top_similar_users_indices = cosine_similarities.flatten().argsort()[::-1][:10]
            most_similar_user = users.iloc[top_similar_users_indices]

            print("Most similar user:")
            print(most_similar_user)

            # need to uncomment after forming the X_test
            # Make a prediction using the model
            # prediction = model.predict(input_data_reshaped)

            # Return the prediction as a JSON response
            return Response({'predicted_cost'}) 
        else:
            # If serializer is not valid, return the errors
            return Response(serializer.errors, status=400)
    else:
        # If the request method is not POST, return an error
        return Response({'error': 'Only POST requests are allowed'}, status=405)
