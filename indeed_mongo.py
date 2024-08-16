import pymongo
from datetime import datetime

class Indeed_Mongo:

    def __init__(self):
        self.create_connections()
        self.create_unique_index()

    def create_connections(self):
        self.mongo_url = 'mongodb://localhost:27017/'
        self.client = pymongo.MongoClient(self.mongo_url)
        self.db = self.client['indeed']
        self.collection = self.db['jobs']

    def insert_data(self,data):
        data['created_at'] = datetime.now()
        insert_result = self.collection.insert_one(data)
        return insert_result.inserted_id

    def create_unique_index(self):
        self.collection.create_index([('job_id', pymongo.ASCENDING)], unique=True)

    def check_job_exists(self,job_id):
        return self.collection.count_documents({'job_id' : job_id}) > 0

    # All the job post will be delete above 14 days
    def clear_all_jobs_14_or_above(self):
        all_jobs = self.collection.find()
        today_date = datetime.today().date()
        for all_job in all_jobs:
            if all_job['job_posted']:
                difference = (today_date - datetime.strptime(all_job['job_posted'] , '%d/%m/%Y').date()).days
                try:
                    if int(difference) > 14:
                        self.collection.delete_one({'job_id': all_job['job_id']})
                except:
                    pass
            else:
                self.collection.delete_one({'job_id': all_job['job_id']})


if __name__ == '__main__':
    mg = Indeed_Mongo()
    mg.clear_all_jobs_14_or_above()

