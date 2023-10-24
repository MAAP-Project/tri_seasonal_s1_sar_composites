from tri_seasonal_s1_sar_composites import constants as c
import re
from typing import Tuple

def get_path_and_season(file_path, band, pattern_regex=c.PATTERN_REGEX, pattern=c.PATTERN) -> Tuple[str, str]:
    """
    using an example of full path to a DPS output tiff file in S3, and as input
    the band, returns the full path for the file corresponding
    to that band, plus the season. 
    """
    parts = file_path.split('/')
    filename = parts[-1]
    fparts = re.match(pattern_regex, filename).groupdict()
    return fparts['season'], f"{'/'.join(parts[:-1])}/{pattern.format(band=band, season=fparts['season'], tile=fparts['tile'], subtile=fparts['subtile'])}"
