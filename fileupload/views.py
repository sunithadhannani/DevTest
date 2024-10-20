import pandas as pd
from django.shortcuts import render
from .forms import UploadForm
from django.core.mail import send_mail

def upload_file(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            try:
                # Use pandas to read the uploaded file
                if file.name.endswith('.xlsx'):
                    data = pd.read_excel(file)
                elif file.name.endswith('.csv'):
                    data = pd.read_csv(file)
                else:
                    data = None
                    return render(request, 'fileupload/error.html', {'error': 'Unsupported file format. Please upload .xlsx or .csv file.'})
                
                # Convert the DataFrame to HTML to display as a table
                if data is not None:
                    table = data.to_html(index=False)  # Convert DataFrame to HTML table

                    # Send email with a basic summary report
                    row_count, col_count = data.shape
                    email_subject = 'Python Assignment - SunithaDhannai'
                    email_body = f'Excel file uploaded successfully.\nRows: {row_count}, Columns: {col_count}.'
                    
                    send_mail(
                        email_subject,
                        email_body,
                        'dhannanisunitha6@gmail.com',  # Replace with your email
                        ['tech@themedius.ai'],
                    )

                    # Render the table in the success page
                    return render(request, 'fileupload/success.html', {'table': table})
            except Exception as e:
                # Handle any file processing errors
                return render(request, 'fileupload/error.html', {'error': f'Error processing file: {str(e)}'})
    
    else:
        form = UploadForm()

    return render(request, 'fileupload/upload.html', {'form': form})