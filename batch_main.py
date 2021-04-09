from population_batch import PopulationBatch

my_directory = 'data/Replication_Timing_200ms_GFP_400ms_RFP_04072021'
my_glob_pattern = '*Trans.tif'
my_fluor_list = ['GFP', 'RFP']

my_batch = PopulationBatch(my_directory, my_glob_pattern, my_fluor_list)