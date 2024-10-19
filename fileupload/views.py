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
            data = pd.read_excel(file) if file.name.endswith('.xlsx') else pd.read_csv(file)

            # Generate summary report
            summary = data.describe().to_string()

            # Send email with the summary report as body text
            send_mail(
                'Python Assignment - SunithaDhannani',
                summary,
                'from@example.com',
                ['tech@themedius.ai'],
            )

            return render(request, 'fileupload/success.html', {'summary': summary})

    else:
        form = UploadForm()

    return render(request, 'fileupload/upload.html', {'form': form})
