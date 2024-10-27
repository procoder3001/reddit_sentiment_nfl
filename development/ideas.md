was able to get transformers pipeline working in vertex ai notebook
- apparently can schedule vertex ai notebooks, but can we turn them off

a more general solution, building vertex ai pipelines
- https://cloud.google.com/vertex-ai/docs/pipelines/notebooks


N1 Predefined Instance Core running in Americas costs like 6 cents in a day

After having everything set up (loading data and predicting on data), compute_engine/Storage PD Capacity seems to be the most expensive service

To cut down on storage PD Capacity cost, I deleted 2 vm's created when I made notebooks with Vertex AI workbench. These vm's had persistent disks attached to them.

use cloud scheduler, cloud function, pub sub to access data, used as input to app

uses vertex pipeline to do model inference, code as a pipeline,py file and deploy and schedule
- so will only need 1 component for using the hugging face package

# Update schedule
- Cloud scheduler updates data daily at 5:00 AM:
- cloud function is run by cloud scheduler
    - https://towardsdatascience.com/how-to-schedule-a-python-script-on-google-cloud-721e331a9590

cloud scheduler uses pub/sub as target type, uses pub.sub topic reddit-nfl-comments

Similarly, use cloud scheduler to schedule vertex ai pipeline
- Vertex pipeline kicks off daily at 6:00 AM
- https://cloud.google.com/vertex-ai/docs/pipelines/schedule-cloud-scheduler
    - http trigger type
    - gsutil URI: gs://gcf-sources-134756275535-us-central1/scheduled_pipelines/intro_pipeline_2.json
    - cloud function url: $CLOUD_FUNCTION_URL


# Notes
with function based components, hard to know what versions of pacakges to use, 
how do i know when i specify base image like us-docker.pkg.dev/vertex-ai/training/pytorch-xla.1-11:latest

# deploy 

docker build --no-cache --platform linux/amd64 -t IMAGE_NAME:v1.0.0 .  

docker tag $IMAGE_NAME:$IMAGE_TAG $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$IMAGE_TAG

docker push $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:$IMAGE_TAG