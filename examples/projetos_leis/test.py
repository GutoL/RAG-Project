
import sys
sys.path.append('../../')
# from indexer.indexer import DocumentsHandler
# from utils.database_manager import DataBaseManager
# from generator.generator import QueryHandler

from codes.utils.database_manager import DataBaseManager

config_file = 'config.json'

database_manager = DataBaseManager(config_file)

existing_items = database_manager.get_existing_data()

for item in existing_items:
    # print(item)
    print(existing_items[item])
    print('---------------------')

prompt = 'Qual é o principal tópico das emendas parlamentares?'

db = database_manager.get_db_connection()        

results = db.similarity_search(prompt, k=10)

for r in results:
    print(r)

print(prompt)