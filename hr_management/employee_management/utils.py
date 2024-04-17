from django.utils.text import slugify

def document_upload_to(instance, file_name):
  """
  Generates a unique upload path for documents based on employee ID and file name.

  Args:
      instance (Document): The Document object being saved.

  Returns:
      str: The upload path for the file.
  """
  # Ensure employee object is available
  if not instance.employee:
      raise ValueError("Employee object is not set for the Document instance.")

  # Create a slugified version of the file name (optional for better URL compatibility)
  file_name = slugify(instance.file.name)

  # Construct the upload path using employee ID and slugified file name
  return f'documents/{instance.employee.id}/{file_name}'
