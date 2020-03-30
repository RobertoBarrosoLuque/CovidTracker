import api_req
import geopandas
import geoviews as gv
gv.extension('bokeh')

shape_folder = 'C:/Users/robal/Dropbox/U Chicago/CovidProject/ShapeFiles/'
us_states = geopandas.read_file(shape_folder + "tl_2017_us_state.shp")
us_states = us_states[us_states["DIVISION"] != '0']
us_states[us_states.NAME=="Alaska"].scale(xfact=.5, yfact=.5)

#positive = total cummulative official cases 
daily_cases = api_req.get_daily_cases()
cumsum_cases_2day = daily_cases[daily_cases["dateChecked"] == max(daily_cases.dateChecked)]

cumsum_states = us_states[["STUSPS", "NAME", "geometry"]].merge(cumsum_cases_2day[["state","positive"]], left_on='STUSPS', right_on='state')

gv.Polygons(cumsum_states, vdims=['positive','NAME']).opts(colorbar=True, cmap='PiYG',width=800, height=400, tools=['hover'], infer_projection=True)