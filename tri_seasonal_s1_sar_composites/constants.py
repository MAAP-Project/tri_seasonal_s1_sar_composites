EXAMPLE_PATH = 's3://maap-ops-workspace/montesano/dps_output/do_gee_download_by_subtile/EXPORT_GEE_v2/SAR_S1_2018/2023/10/13/22/06/55/952988/s1_vv_vh_gamma_2018_pwr_tile103-subtile000127/s1_vv_vh_gamma_2018_pwr_tile103.VH_median_summer-subtile000127.tif'
PATTERN = 's1_vv_vh_gamma_2018_pwr_tile{tile}.{band}_median_{season}-subtile{subtile}.tif'
PATTERN_REGEX = r"s1_vv_vh_gamma_2018_pwr_tile(?P<tile>\d+)\.(?P<band>V[HV])_median_(?P<season>\w+)-subtile(?P<subtile>\d+)\.tif"
DATE_RANGES = {
    'frozen':["2018-01-01T00:00:00Z","2018-03-03T00:00:00Z"],
    'summer':["2018-06-15T00:00:00Z","2018-08-31T00:00:00Z"],
    'shoulder':["2018-09-15T00:00:00Z","2018-10-31T00:00:00Z"]

}



ID_PATTERN="{parent_folder}_{season}"


ROOT_LINK = "https://stac.maap-project.org"
COLLECTION_ID='tri_seasonal_s1_sar_composites'
COLLECTION_TITLE='Tri seasonal S1 SAR composites'
COLLECTION_DESCRIPTION='tri-seasonal composite built yearly from dual-polarimetric data. For each of the 3 seasons we consider, we use bands VV and VH, for a total of 6 bands for each year.'
COLLECTION_LINK = f"{ROOT_LINK}/collections/{COLLECTION_ID}"
COLLECTION_ITEMS_LINK = f'{COLLECTION_LINK}/items'
COLLECTION_LICENSE = 'not-provided'


ITEM_SELF_LINK = f"{COLLECTION_ITEMS_LINK}/"

BANDS = ['VV','VH']

SEASONS = ['frozen','summer','shoulder']