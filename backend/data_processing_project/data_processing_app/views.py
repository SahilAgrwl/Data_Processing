# data_processing_app/views.py
from django.http import JsonResponse
from .models import ProcessedData
from .utils.infer_data_types import infer_and_convert_data_types

def process_data(request):
    if request.method == 'POST' and request.FILES.get('file'):
        file = request.FILES['file']
        result = infer_and_convert_data_types(file)

        if result['success']:
            processed_data = result['data']

            # Save the processed data to the database
            processed_data_instance = ProcessedData.objects.create(data=processed_data)

            # Get the processed data as a dictionary
            processed_data_dict = processed_data_instance.to_dict()

            return JsonResponse({'status': 'success', 'processed_data': processed_data_dict})
        else:
            return JsonResponse({'status': 'error', 'message': result['message']}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method or missing file.'}, status=400)
