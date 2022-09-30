# JotForm Demo
### Resources
Docker Image: https://hub.docker.com/repository/docker/adamosmi/jotform_demo

Github Repo: https://github.com/adamosmi/jotform_demo

JotForm API Documentation: https://api.jotform.com/docs/

## How to run JotForm Demo data pull
1. Pull docker image (or build it yourself from Dockerfile)
    ```
    docker pull adamosmi/jotform_demo
    ```

2. Get your Jotform API key
    * Log into your account and click "Create New Key": https://www.jotform.com/myaccount/api
        - Read-Only is fine

3. Create folder on your local computer to store output data from demo

4. Run docker image with API key as an env variable and path to storage folder created in previous step (be sure to remove curly brackets in code below)
    ```
    docker run -v {insert_local_file_path_here}:/job_data -e JOTFORM_API_KEY={insert_your_api_key_here} adamosmi/jotform_demo
    ```
5. Output should give you all submissions from all forms associated with the account

## How to make updates to code
The python script responsible for running the pull and transformations can be found here:
https://github.com/adamosmi/jotform_demo/blob/master/src/job.py