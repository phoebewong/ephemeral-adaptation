import json
import numpy as np

def generate_selection_indices( n_menu_items , zipfian_dist ):
	##Generate the list of click locations
	selection_indices = []
	menu_indices = np.random.choice( n_menu_items , len( zipfian_dist ) ,  replace=False ) ##Sample w/out replacement the number of menu ids that we have counts for
	for j in range( len( zipfian_dist ) ): ##For each number of counts in the zipfian dist
		for k in range( zipfian_dist[ j ] ): ##For the number specified by the zipfian dist, add one trial
			selection_indices.append( menu_indices[ j ] )
	selection_indices = np.array( selection_indices )
	np.random.shuffle( selection_indices ) ##Shuffle menu locations
	selection_indices = selection_indices.tolist()	
	return selection_indices

def generate_prediction_indices( selection_indices , n_corrections ):
	prediction_indices = []
	##Algorithm from: A Comparison of Static, Adaptive, and Adaptable Menus
	recency_list = np.zeros( len( selection_indices ) )
	frequency_list = np.zeros( len( selection_indices ) )
	recency_predictions = [ 0 ]
	frequency_predictions = [ 1 , 2 ]
	incorrect_predictions = [] ##Keep track of whcih ones you may want to correct
	for j , idx in enumerate( selection_indices ):
		prediction_indices.append( frequency_predictions + recency_predictions )

		recency_list += 1 ##Add 1 to all recency counters
		frequency_list[ idx ] += 1 ##Add 1 to frequency counter of current
		recency_list[ idx ] = 0

		if idx not in recency_predictions and idx not in frequency_predictions: ##If the current isn't already in the partition, figure out what to do but otherwise, don't do anything
			least_recent_id = recency_predictions[ 0 ] ##Only 1 recency item
			least_frequent_id = frequency_predictions[ np.argmin( frequency_list[ frequency_predictions ] ) ]

			if frequency_list[ least_recent_id ] < frequency_list[ least_frequent_id ]:
				recency_predictions[ 0 ] = idx
			else:
				frequency_predictions[ list( frequency_predictions ).index( least_frequent_id ) ] = recency_predictions[ 0]
				recency_predictions[ 0 ] = idx
			incorrect_predictions.append( j )

	##Randomly correct a few predictions to increase accuracy for high accuracy condition (these all are)
	correct_indices = np.random.choice( incorrect_predictions , n_corrections , replace=False )
	for idx in correct_indices:
		replace_idx = np.random.choice( len( prediction_indices[ idx ] ) )
		prediction_indices[ idx ][ replace_idx ] = selection_indices[ idx ]

	###Compute accuracy
	correct_predictions = 0
	for j in range( len( selection_indices ) ):
		if selection_indices[ j ] in prediction_indices[ j ]:
			correct_predictions += 1
	accuracy = correct_predictions / float( len( selection_indices ) )

	return prediction_indices , accuracy

def generate_selection_and_prediction_locations( selection_indices , prediction_indices ):
	selection_locations = []
	predicted_locations = []
	for j in range( len( selection_indices ) ):
		menu_indices = np.random.choice( 3 , 3 , replace=False )
		for k in menu_indices:
			selection_locations.append( [ k , selection_indices[ j ] ] )
			predicted_locations.append( [] )
			for l in range( len( prediction_indices[ j ] ) ):
				predicted_locations[ -1 ].append( [ k , prediction_indices[ j ][ l ] ] )

	return selection_locations , predicted_locations

def swap_menu_numbers_in_selection_and_prediction_locations( selection_indices , prediction_indices , c ):
	if c > 0:
		assert c == 1 , "Only set up for 2 conditions"
		correspondence_list = [ [ 1 , 2 , 0 ] , [ 2 , 0 , 1 ] ][ np.random.choice( 2 ) ] ##Maps menus in condition 1 to menus in condition 2
	else:
		correspondence_list = [ 0 , 1 , 2 ]
	for j in range( len( predicted_locations ) ):
		selection_locations[ j ][ 0 ] = correspondence_list[ selection_locations[ j ][ 0 ] ]
		for k in range( len( predicted_locations[ j ] ) ):
			predicted_locations[ j ][ k ][ 0 ] = correspondence_list[ predicted_locations[ j ][ k ][ 0 ] ]

	return selection_locations , predicted_locations

def generate_word_list( word_categories , n_menus , n_menu_items ):
	##Sample the words in each block
	##Sample all categories at once so you know there are no duplicates
	sampled_categories = np.random.choice( word_categories.keys() , int( ( n_menus * n_menu_items ) / 4. ) ,  replace=False ) 
	##Index into which menu and list of menus of words
	menu_number = -1
	word_list = []
	for k , category in enumerate( sampled_categories ):
		##If you reach the end of the menu, move to the next
		if k % 4 == 0:
			if menu_number >= 0:
				assert len( word_list[ menu_number ] ) == n_menu_items , "A menu with an odd number of items!"
				menu_number += 1
			word_list.append( [] )

		##For every word in the category, add it to the menu
		for word in word_categories[ category ]:
			word_list[ menu_number ].append( word )

	return word_list


if __name__ == "__main__":

	##Parameters of the experiment
	zipfian_dist = [ 15 , 8 , 5 , 4 , 3 , 3 , 2 , 2 ]
	word_categories = json.load( open( "categories.json" , "rb" ) )
	n_participants = 15
	n_blocks = 2
	n_menus = 3
	n_menu_items = 16
	n_predictions = 3
	n_corrections = 11
	n_practice_questions = 8

	###Generate Practice Experiment Block
	selection_indices = generate_selection_indices( n_menu_items , zipfian_dist )
	prediction_indices , accuracy = generate_prediction_indices( selection_indices , n_corrections )
	selection_locations , predicted_locations = generate_selection_and_prediction_locations( selection_indices , prediction_indices )
	practice_block = {}
	practice_block[ "selection_locations" ] = selection_locations[ :n_practice_questions ]
	practice_block[ "predicted_locations" ] = predicted_locations
	practice_block[ "words" ] = generate_word_list( word_categories , n_menus , n_menu_items )

	##Generate an experiment setup for each participant
	accuracies = []
	participant_experiment_data = []
	for i in range( n_participants ):
		##Half of the experiments are control then ephemeral, and the rest are the reverse
		if i <= n_participants / 2.:
			condition_order = [ "control" , "ephemeral" ]
		else:
			condition_order = [ "ephemeral" , "control" ]

		selection_indices = generate_selection_indices( n_menu_items , zipfian_dist )
		prediction_indices , accuracy = generate_prediction_indices( selection_indices , n_corrections )
		accuracies.append( accuracy )
		selection_locations , predicted_locations = generate_selection_and_prediction_locations( selection_indices , prediction_indices )

		block_list = {}
		for c , condition in enumerate( condition_order ):
			selection_locations , predicted_locations = swap_menu_numbers_in_selection_and_prediction_locations( selection_indices , prediction_indices , c )
			block_list[ condition ] = []
			for j in range( n_blocks ):	
				block = {}
				block[ "selection_locations" ] = selection_locations
				block[ "predicted_locations" ] = predicted_locations
				block[ "words" ] = generate_word_list( word_categories , n_menus , n_menu_items )
				block_list[ condition ].append( block )

		experiment_data = {
			"condition_order": condition_order ,
			"experiment_blocks": block_list ,
			"practice_block": practice_block ,
		}
		participant_experiment_data.append( experiment_data )

	print( "Mean Accuracy: " + str( np.mean( accuracies ) ) )

	##Shuffle the generated experiments so e.g. the first 10 aren't all the same
	participant_experiment_data = np.array( participant_experiment_data )
	np.random.shuffle( participant_experiment_data )
	participant_experiment_data = list( participant_experiment_data )

	json.dump( participant_experiment_data , open( "experiment_data.json" , "wb" ) )

	
