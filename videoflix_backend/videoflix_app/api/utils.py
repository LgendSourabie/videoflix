from django.http import Http404 
import os
import glob

def get_or_404(model,pk):
    """Get model object or return 404 Not Found"""

    try:
        pk = int(pk)
        instance = model.objects.get(pk=pk)
        return instance
    except ValueError:
        raise ValueError("The ID must be an integer")
    except model.DoesNotExist:
        raise Http404("Model does not exist")
      

def delete_files_starting_with(source, file_postfix="_thumb"):
    # Construct the pattern to match files starting with the given prefix
    file_name, _ = os.path.splitext(source)
    file_name = os.path.basename(file_name)
    file_postfix = f"{file_name}" + f"{file_postfix}"

    pattern = os.path.join("media/videos/", f"{file_postfix}*")
    
    files_to_delete = glob.glob(pattern)
    if files_to_delete:
        for file in files_to_delete:
            try:
                os.remove(file)
            except Exception as e:
                print(f"Error deleting {file}: {e}")


def seconds_to_time(seconds):
    """Convert time in string"""

    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = seconds % 60

    if hours > 0:
        return f"{hours:02}:{minutes:02}:{remaining_seconds:02}"
    else:
        return f"{minutes:02}:{remaining_seconds:02}"
