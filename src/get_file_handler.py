async def get_file_handler(uid, jobs):
    if uid in jobs:
        return jobs[uid].files
    else:
        return "Job not available"