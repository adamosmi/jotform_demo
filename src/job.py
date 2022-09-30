"""
Documentation on api available here: https://api.jotform.com/docs/

Script intended to generate sample csv of all responses on all forms submitted which can then be uploaded to sql.
"""

import os
import requests
import json
from pprint import pprint
import pandas as pd
from datetime import datetime

api_key = os.getenv('JOTFORM_API_KEY') # env var name set in Dockerfile and fed in at runtime
datetime_string = datetime.now().strftime('%m_%d_%Y')
output_path = f'/job_data/output_{datetime_string}.csv'  # /job_data is defined as output path in entyrpoint.sh and used in docker call as mount point

# get all user submissions
print('retrieving submission data from jotform api...')
user_submissions_req = requests.get(f'https://api.jotform.com/user/submissions?apiKey={api_key}', verify=False)
user_submissions_res = json.loads(user_submissions_req.text)
# pprint(user_submissions_res)

# build output
print('processing submission data...')
output_list = []
for submission in user_submissions_res.get('content', []): # get information on each submission to be included with answer data
    # pprint(submission) # pprint makes debugging easier, gives you clean view of json
    # print(submission.keys()) # lets you better understand the info
    submission_id = submission.get('id')
    submission_created_date = submission.get('created_at')
    submission_updated_date = submission.get('updated_at')
    for question_key, question_value in submission.get('answers', {}).items(): # get response values
        # print(question_value)
        question_name = question_value.get('name')
        question_order = question_value.get('order')
        question_text = question_value.get('text')
        response_value = question_value.get('answer')

        # build final output {'column_name': populated value}
        # for simplicity, all fields in output formatted as a string, would want to update in production
        output = {
            'submission_id': submission_id,
            'submission_created_date': submission_created_date,
            'submission_updated_date': submission_updated_date,
            'question_name': question_name,
            'question_order': question_order,
            'question_text': question_text,
            'response_value': str(response_value) # can be a dictionary, further processing required
        }
        output_list.append(output)

print('building output file...')
output_df = pd.DataFrame(output_list)
output_df = output_df.sort_values(by=['submission_id', 'submission_created_date', 'question_order'], ascending=True)
output_df.to_csv(output_path, index=False, mode='w')

print(f'output of size {str(output_df.shape)} saved to: {output_path}')
print('DONE.')

# NOTE: some response values can be dictionaries, breaking these up into seperate line rows is important
# >>> output_df.iloc[2]
# submission_id                                 5403091265344111259
# submission_created_date                       2022-09-29 21:05:26
# submission_updated_date                       2022-09-29 21:07:46
# question_name                                         yourFucking
# question_order                                                  2
# question_text                                   YOUR FUCKING Name
# response_value             {'first': 'Lucas', 'last': 'Amoudruz'}
# Name: 2, dtype: object
    # submission_names.append(submission.get('name'))
# print(submission_names)

# >>> output_df.iloc[4]
# submission_id                              5403091265344111259
# submission_created_date                    2022-09-29 21:05:26
# submission_updated_date                    2022-09-29 21:07:46
# question_name                                    phoneNumber12
# question_order                                               4
# question_text                  YOUR MOTHERFUCKING Phone Number
# response_value             {'area': '857', 'phone': '2666578'}
# Name: 4, dtype: object

# >>> pprint(output_df.iloc[86])
# submission_id                                            5403043255678481649
# submission_created_date                                  2022-09-29 19:45:25
# submission_updated_date                                                 None
# question_name                                                     chooseYour
# question_order                                                             7
# question_text                                          Choose your package: 
# response_value             {'paymentArray': '{"total":"0.00","paypalcompl...{'paymentArray': '{"total":"0.00","paypalcompleteData":{"submission_id":"5403043255678481649","merchantId":null,"amount":null,"transactionId":null,"currency":null,"paymentType":null,"sandbox":null,"sandboxMode":null,"isCharged":true}}'}
# Name: 86, dtype: object
