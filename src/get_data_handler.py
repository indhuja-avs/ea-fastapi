async def get_data_handler(uid, jobs):
    if uid in jobs:
        return jobs[uid].data
    else:
        return "Job not available"