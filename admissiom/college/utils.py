import os

def get_upload_path(instance, filename):
    return os.path.join("documents", instance.applicant.user.username, filename)
