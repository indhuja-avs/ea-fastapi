import earthaccess as ea
from src.utils import *
import xarray as xr

def download_handler(new_job, short_name = None, date_range = None, concept_id = None, bounding_box = None):
    new_job.status = "in progress - querying data"
    results = callWithNonNoneArgs(ea.search_data,
    concept_id = concept_id,
    short_name=short_name,
    cloud_hosted=True,
    temporal=date_range,
    bounding_box=bounding_box,
    count = 1  #set count as 1 for testing purposes
    )
    i = 10
    new_job.progress = i
    new_job.status = "in progress - downloading files"
    result_files = []
    for result in results:
        i = i + 10
        result_file = ea.download(granules=result,local_path="/Users/Indhuja/Downloads/test/")
        result_files.append(result_file[0])
        new_job.progress = i
    new_job.files = result_files
    new_job.status = "in progress - parsing files"
    new_job.progress = 90
    fileset = ea.open(results)
    print(fileset)
    new_job.data = xr.open_mfdataset(fileset).to_dict(data=False)
    new_job.status = "complete"
    new_job.progress = 100
    