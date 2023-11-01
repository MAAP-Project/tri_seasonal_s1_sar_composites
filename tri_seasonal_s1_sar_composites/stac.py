import rio_stac
import datetime
import pystac
from tri_seasonal_s1_sar_composites import constants as c
from tri_seasonal_s1_sar_composites import utils

def create_collection(catalog_url: str) -> pystac.Collection :
    """ create collection """
    spatial_extent = pystac.collection.SpatialExtent([[-180, -90, 180, 90]])
    temporal_extent = pystac.collection.TemporalExtent(intervals=[[datetime.datetime(2018,1,1), datetime.datetime(2018, 12, 31)]])
    
    item_assets = {
        k : pystac.extensions.item_assets.AssetDefinition.create(title=k, description=k,media_type='image/tiff; application=geotiff; profile=cloud-optimized',roles=['data']) for k in c.BANDS
    }
    
    collection = pystac.Collection(
        id=c.COLLECTION_ID,
        description=c.COLLECTION_DESCRIPTION,
        extent=pystac.collection.Extent(spatial_extent, temporal_extent),
        title=c.COLLECTION_TITLE,
        stac_extensions=['https://stac-extensions.github.io/item-assets/v1.0.0/schema.json'],
        href=c.COLLECTION_LINK_PATTERN.format(root=catalog_url, collection=c.COLLECTION_ID),
        license=c.COLLECTION_LICENSE,
        extra_fields={'item_assets':item_assets}
    )
    
    ext = pystac.extensions.item_assets.ItemAssetsExtension(collection)
    ext.item_assets = item_assets
    
    # commenting this out because it seems to be added automatically by our ingestor 
    # ext.collection.add_link(pystac.Link(pystac.RelType.ITEMS, COLLECTION_ITEMS_LINK, media_type=pystac.MediaType.GEOJSON))

    ext.collection.add_link(pystac.Link(pystac.RelType.PARENT, catalog_url, media_type=pystac.MediaType.JSON))

    
    return ext.collection


def create_item(file_path: str, catalog_url: str) -> pystac.Item:
    """
    create a STAC item for the tile, subtile and season corresponding to `file_path`
    the STAC item spatial extent corresponds to the tile, subtile associated with `file_path`, and the
    temporal extent corresponds to the date ranges associated with the season of `file_path`
    """
    file_paths = {band: utils.get_path_and_season(file_path, band)[1] for band in c.BANDS}
    season = utils.get_path_and_season(file_path, 'VV')[0] # any of the two works 
    parent_folder = f"{file_paths['VV'].split('/')[-2]}" # any of the two works except if anything changes in the DPS output structure
    
    common_kwargs = dict(
        with_eo=True,
        with_raster=True,
        with_proj=True,
        asset_roles=['data'],
        collection=c.COLLECTION_LINK,
        asset_media_type="image/tiff; application=geotiff; profile=cloud-optimized",
        properties={'start_datetime':c.DATE_RANGES[season][0], 'end_datetime':c.DATE_RANGES[season][1]},
        id=c.ID_PATTERN.format(parent_folder=parent_folder, season=season)
    )
    
    items = { band: 
        rio_stac.stac.create_stac_item(
        source=file_paths[band],
        asset_name=band,
        **common_kwargs
    ) for band in c.BANDS
    }
    
    
    item = items['VV'] # any of the two, then add the asset for the other
    
    item.add_asset('VH',items['VH'].assets['VH'])
    item.add_link(pystac.Link(pystac.RelType.ROOT, catalog_url, media_type=pystac.MediaType.JSON))
    item.add_link(pystac.Link(pystac.RelType.PARENT, c.COLLECTION_LINK_PATTERN.format(root=catalog_url, collection=c.COLLECTION_ID), media_type=pystac.MediaType.JSON))
    item.add_link(pystac.Link(pystac.RelType.SELF, f"{c.COLLECTION_ITEMS_LINK_PATTERN.format(collection_link=c.COLLECTION_LINK_PATTERN.format(root=catalog_url, collection=c.COLLECTION_ID))}/{item.id}", media_type=pystac.MediaType.GEOJSON))
    
    return item