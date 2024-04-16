import obspython as OBS
from datetime import datetime
import time

# variables for OBS properties later
source_name = ''
# clock_24_hour = False
current_time = ''

def script_description():
    return """Clock
    Displays a clock in a text source."""

def script_properties():
    props = OBS.obs_properties_create()
    # text source select/refresh
    list_property = OBS.obs_properties_add_list(props, "source_name", 'Source: ', OBS.OBS_COMBO_TYPE_LIST, OBS.OBS_COMBO_FORMAT_STRING)
    
    OBS.obs_properties_add_button(props, "button", "Refresh list of sources: ",
                                  lambda props,prop: True if populate_list_property_with_source_names(list_property) else True)
    populate_list_property_with_source_names(list_property)

    OBS.obs_properties_add_bool(props, "clock_24_hour", '24 Hour Clock: ')

    return props

def script_update(settings):
    global source_name
    source_name = OBS.obs_data_get_string(settings, 'source_name')
    # clock_24_hour = OBS.obs_data_get_bool(settings, 'clock_24_hour')

def script_load(settings):
    global source_name
#    global clock_24_hour
    global current_time

# fills the given list property with the names of all text sources plus an empty one:
def populate_list_property_with_source_names(list_property):
    sources = OBS.obs_enum_sources()
    OBS.obs_property_list_clear(list_property)
    OBS.obs_property_list_add_string(list_property, "", "")
    for source in sources:
        source_id = OBS.obs_source_get_id(source)
        if source_id == 'text_gdiplus_v2':
            name = OBS.obs_source_get_name(source)
            OBS.obs_property_list_add_string(list_property, name, name)
    OBS.source_list_release(sources)

def set_time():
    global current_time

    now = datetime.now
    current_time = now.strftime("%H:%M:%S")
    update_source_text()
    time.sleep(0.25)

def update_source_text():
    global source_name, current_time
    src = OBS.obs_get_source_by_name(source_name)
    textset = OBS.obs_data_create()
    OBS.obs_data_set_string(textset, 'text', current_time)
    OBS.obs_source_update(src, textset)
    OBS.obs_data_release(textset)
    OBS.obs_source_release(src)
