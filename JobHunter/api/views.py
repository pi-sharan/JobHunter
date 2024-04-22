from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import numpy as np
from tensorflow.keras.models import load_model
import os
from .serializers import JobApplicantSerializer

# Get the path to the pickled model file
model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Model', 'keras_model.h5')

# Load the pickled model
model = load_model(model_path)

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
            input_data['degree_type'] = degree_type_mapping.get(input_data['degree_type'], 0)

            input_data_list = [input_data[field] for field in ['degree_type', 'work_history_count', 
                                                               'total_years_experience', 'currently_employed',
                                                               'managed_others', 'managed_how_many']]
            input_data_list.extend(input_data['workexp'])
            input_data_as_numpy_array = np.asarray(input_data_list)
            input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
            # Print the input data to the console
            print("Input Data:", input_data_reshaped)

            # Make a prediction using the model
            prediction = model.predict(input_data_reshaped)

            # Return the prediction as a JSON response
            return Response({'predicted_cost': prediction[0]})
        else:
            # If serializer is not valid, return the errors
            return Response(serializer.errors, status=400)
    else:
        # If the request method is not POST, return an error
        return Response({'error': 'Only POST requests are allowed'}, status=405)
