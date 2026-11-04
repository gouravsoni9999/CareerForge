from pathlib import Path
from django.core.exceptions import ValidationError

MAX_RESUME_SIZE = 5*1024*1024 # 5 MB

def validate_resume_file(file):
    extension = Path(file.name).suffix.lower()

    if extension != ".pdf":
        raise ValidationError("Only PDF resumes are allowed.")

    if file.size > MAX_RESUME_SIZE:
        raise ValidationError("Resume size must not exceed 5 MB.")

    # check the pdf file signature
    file.seek(0)
    file_signature = file.read(5)
    file.seek(0)

    if file_signature != b"%PDF-":
        raise ValidationError("The uploaded file is not a valid PDF.")