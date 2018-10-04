import os
import json
import numpy as np
import pandas as pd

dir_name = "data/"

time_columns = [ "participant_number" , "condition" , "menu_order" , "selection_time" , "correctly_predicted" , "error_in_trial" ] 
time_matrix = []
for i , fname in enumerate( os.listdir( dir_name ) ):
	if ".json" not in fname:
		continue

	data = json.load( open( dir_name + fname , "rb" ) )

	age = data[ "demographics" ][ "age" ]
	gender = data[ "demographics" ][ "gender" ]
	order = data[ "experiment_number" ]

	for trial in data[ "trials" ]:

		condition = trial[ "condition" ]
		time = trial[ "selection_time" ]
		predicted = trial[ "correctly_predicted" ]
		error = ( trial[ "errors" ][ "number_errors" ] > 0 )

		row = [ i , condition , order , time , predicted , error ]
		time_matrix.append( row )

time_df = pd.DataFrame( time_matrix , columns=time_columns )
time_df.to_csv( open( "data/time_data.csv" , "w" ) , index=False )

qualitative_columns = [ "participant_number" , "age" , "gender" , "menu_order" , "overall_preference" , "overall_easy" , 
						"control_satisfaction" , "control_difficulty" , "control_frustration" , "control_efficiency" , 
						"ephemeral_satisfaction" , "ephemeral_difficulty" , "ephemeral_frustration" , "ephemeral_efficiency" ] 

qualitative_matrix = []
for i , fname in enumerate( os.listdir( dir_name ) ):
	if ".json" not in fname:
		continue
	
	data = json.load( open( dir_name + fname , "rb" ) )

	age = data[ "demographics" ][ "age" ]
	gender = data[ "demographics" ][ "gender" ]
	order = data[ "experiment_number" ]

	overall_preference = data[ 'overall-comparisons' ][ 'prefer' ]
	overall_easy = data[ 'overall-comparisons' ][ 'prefer' ]

	control_satisfaction = 	data[ 'qualitative_information' ][ 'control' ][ 'satisfaction' ]
	control_difficulty = 	data[ 'qualitative_information' ][ 'control' ][ 'difficulty' ]
	control_frustration = 	data[ 'qualitative_information' ][ 'control' ][ 'frustration' ]
	control_efficiency = 	data[ 'qualitative_information' ][ 'control' ][ 'efficiency' ]

	ephemeral_satisfaction = 	data[ 'qualitative_information' ][ 'ephemeral' ][ 'satisfaction' ]
	ephemeral_difficulty = 	data[ 'qualitative_information' ][ 'ephemeral' ][ 'difficulty' ]
	ephemeral_frustration = 	data[ 'qualitative_information' ][ 'ephemeral' ][ 'frustration' ]
	ephemeral_efficiency = 	data[ 'qualitative_information' ][ 'ephemeral' ][ 'efficiency' ]

	row = [ i , age , gender , order , overall_preference , overall_easy , 
			control_satisfaction , control_difficulty , control_frustration , control_efficiency ,
			ephemeral_satisfaction , ephemeral_difficulty , ephemeral_frustration , ephemeral_efficiency ]

	qualitative_matrix.append( row )

qualitative_df = pd.DataFrame( qualitative_matrix , columns=qualitative_columns )
qualitative_df.to_csv( open( "data/qualitative_data.csv" , "w" ) , index=False )

