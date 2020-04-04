from .worker import Worker
worker = Worker()

worker.open_files()
worker.map_data()
worker.write_output()
worker.close_files()
input("Press Enter to finish...")