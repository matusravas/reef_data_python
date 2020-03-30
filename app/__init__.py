from app.worker import Worker

worker = Worker()

worker.map_data()
worker.write_output()
worker.close_files()

