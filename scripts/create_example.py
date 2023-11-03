import json
import fire
from tri_seasonal_s1_sar_composites import stac, constants

def main(catalog_url: str):
    collection = stac.create_collection(catalog_url)
    item = stac.create_item(constants.EXAMPLE_PATH, catalog_url)
    
    with open('example_collection.json', 'w') as f:
        json.dump(collection.to_dict(), f)
    
    with open('example_item.json', 'w') as f:
        json.dump(item.to_dict(), f)
        
if __name__ == '__main__':
    fire.Fire(main)