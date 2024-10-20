# fileupload/views.py

import pandas as pd
from django.shortcuts import render
from .forms import UploadForm
from django.core.mail import send_mail

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            # Use pandas to read the uploaded file
            if file.name.endswith('.xlsx'):
                data = pd.read_excel(file)
            elif file.name.endswith('.csv'):
                data = pd.read_csv(file)
            else:
                data = None

            # Convert the DataFrame to HTML to display as a table
            if data is not None:
                table = data.to_html(index=False, classes='styled-table')  # Add the custom class
 # Convert DataFrame to HTML table

                # Send an email confirming file upload (optional)
                send_mail(
                    'Python Assignment - Sunitha Dhannani',  # Updated email subject
                    f'Excel file uploaded successfully.\nRows: {data.shape[0]}, Columns: {data.shape[1]}',
                    'dhannanisunitha6@gmail.com',  # Your email
                    ['tech@themedius.ai'],
                )

                return render(request, 'fileupload/success.html', {'table': table})

    else:
        form = UploadForm()

    return render(request, 'fileupload/upload.html', {'form': form})