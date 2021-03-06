import selection_script as select
import matplotlib.pyplot as plt

def get_population_function(population_feature, elevation_raster, 
                            spatial_relationships, population_field, start, 
                            stop, interval):
	results list = []
        for level in range(start, stop, interval):
                val = select.sum_below_elevation(population_Feature, 
                                                 elevation_raster,
                                                 spatial_relationships,
                                                 population_field)
		results.append((level, val))
	return results

def graph_population_function(pair_list, name):
	sea_levels = [pair[0] for pair in pair_list]
	populations = [pair[1] for pair in pair_list]
        	

def selection_comparison_graph(population_features, elevation_raster, selection_list):
	for method in selection_list:
		results = get_population_function(population_features, elevation_raster, method[1])
		graph_population_function(results, method[0], axis)

def selection_bargraph(population_features, elevation_raster, selection_list, sea_level):
	results = []
	for method in selection_list:
		results.append(get_affected(#.....
	#make bar graph
