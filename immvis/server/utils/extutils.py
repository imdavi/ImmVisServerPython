_FILE_EXTENSION_CSV = ".csv"
_FILE_EXTENSION_JSON = ".json"
_FILE_EXTENSION_XLS = ".xls"
_FILE_EXTENSION_XLSX = ".xlsx"
_FILE_EXTENSION_PNG = ".png"
_FILE_EXTENSION_JPG = ".jpg"
_FILE_EXTENSION_JPEG = ".jpeg"
_FILE_EXTENSION_TIFF = ".tiff"
_FILE_EXTENSION_TIF = ".tif"

def _has_extension(file_path, extension):
    lowercase_file_path = file_path.lower()
    return lowercase_file_path.endswith(extension)

def is_excel(file_path):
    return _has_extension(file_path, _FILE_EXTENSION_XLS) or _has_extension(file_path, _FILE_EXTENSION_XLSX)

def is_csv(file_path):
    return _has_extension(file_path, _FILE_EXTENSION_CSV)

def is_json(file_path):
    return _has_extension(file_path, _FILE_EXTENSION_JSON)

def is_image(file_path):
    return (_has_extension(file_path, _FILE_EXTENSION_JPG) or 
    _has_extension(file_path, _FILE_EXTENSION_JPEG) or 
    _has_extension(file_path, _FILE_EXTENSION_PNG) or 
    _has_extension(file_path, _FILE_EXTENSION_TIF) or 
    _has_extension(file_path, _FILE_EXTENSION_TIFF))
