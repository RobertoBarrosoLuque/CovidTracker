import api_req
import geopandas
import geoviews as gv
gv.extension('bokeh')

shape_folder = 'C:/Users/robal/Dropbox/U Chicago/CovidProject/ShapeFiles/'
us_states = geopandas.read_file(shape_folder + "tl_2017_us_state.shp")
us_states = us_states[us_states["DIVISION"] != '0']
us_states.set_value(us_states.NAME=="Alaska","geometry", us_states[us_states.NAME=="Alaska"].scale(xfact=.5, yfact=.5) )
#positive = total cummulative official cases 
daily_cases = api_req.get_daily_cases()
cumsum_cases_2day = daily_cases[daily_cases["dateChecked"] == max(daily_cases.dateChecked)]

doctors_df = api_req.get_num_doctors()

cumsum_states = us_states[["STUSPS", "NAME", "geometry"]].merge(cumsum_cases_2day[["state","positive"]], left_on='STUSPS', right_on='state')

cumsum_states = cumsum_states.merge(doctors_df, left_on="NAME", right_on="State")[["State", "geometry","positive", "doc_per_thousand"]]

gv.Polygons(cumsum_states, vdims=['positive',"doc_per_thousand",'State']).opts(colorbar=True, cmap='PiYG',width=400, height=200,xlim=(-130, -65), ylim=(20,70), tools=['hover'])