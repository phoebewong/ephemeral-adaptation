import json
import numpy as np

def generate_selection_indices( n_menus , n_menu_items , zipfian_dist ):
	##Generate the list of click locations
	##For each item in the zipfian dist, assign a menu item to it 
	##without replacement, then add it to the list the number of times 
	##specified by the distribution, once for each menu, then shuffle the 
	##resulting list and return it 
	selection_indices = []
	menu_indices = np.random.choice( n_menu_items , len( zipfian_dist ) ,  replace=False ) ##Sample w/out replacement the number of menu ids that we have counts for
	for i in range( n_menus ):
		for j in range( len( zipfian_dist ) ): ##For each number of counts in the zipfian dist
			for k in range( zipfian_dist[ j ] ): ##For the number specified by the zipfian dist, add one trial
				selection_indices.append( [ i , menu_indices[ j ] ] )
	selection_indices = np.array( selection_indices )
	np.random.shuffle( selection_indices ) ##Shuffle menu locations
	selection_indices = selection_indices.tolist()	
	return selection_indices

def generate_selections_and_predictions( n_menus , n_menu_items , zipfian_dist , n_recency_predictions , n_frequency_predictions , n_corrections ):
	##Generate menu items from Zipfian distribution in each menu and randomly shuffle them
	selection_indices = generate_selection_indices( n_menus , n_menu_items , zipfian_dist )
	
	##Hold onto data for recency and frequency computations
	recent_menu_items = [ [ i for i in range( n_recency_predictions ) ] for j in range( n_menus ) ] ##Lists to hold onto most recent items in each menu
	frequent_menu_items = np.zeros( ( n_menus , n_menu_items ) ) ##Lists to hold onto item frequencies for each menu

	incorrect_indices = [] ##Cache mistakes
	prediction_indices = [] ##Cache predictions
	for i , [ menu_idx , item_idx ] in enumerate( selection_indices ):
		
		##Grab the n_recency_predictions most recent items
		recency_items = [ [ menu_idx , recent_menu_items[ menu_idx ][ j ] ] for j in range( n_recency_predictions ) ]

		frequency_items = [] ##Add frequency items that aren't in recency list until you hit n_frequency_predictions
		for frequency_idx in np.argsort( frequent_menu_items[ menu_idx ] )[ ::-1 ]:
			if len( frequency_items ) >= n_frequency_predictions:
				break
			if frequency_idx not in recent_menu_items[ menu_idx ]:
				frequency_items.append( frequency_idx )

		##Grab the n_recency_predictions most recent items
		for j in range( n_frequency_predictions ):
			frequency_items[ j ] = [ menu_idx , frequency_items[ j ] ]

		predictions = recency_items + frequency_items
		prediction_indices.append( predictions )

		##If the item wasn't in the list, record it
		if [ menu_idx , item_idx ] not in predictions:
			incorrect_indices.append( i )
		
		##Update lists for next iteration
		recent_menu_items[ menu_idx ].append( item_idx )
		recent_menu_items[ menu_idx ] = recent_menu_items[ menu_idx ][ 1: ]
		frequent_menu_items[ menu_idx ][ item_idx ] += 1

	##Compute the accuracy
	accuracy = ( ( len( selection_indices ) - len( incorrect_indices ) ) + n_corrections ) / float( len( selection_indices ) )

	##Correct a random n_corrections of the wrong predictions
	incorrect_indices = np.array( incorrect_indices )
	np.random.shuffle( incorrect_indices )
	for correction_idx in incorrect_indices[ :n_corrections ]:
		prediction_indices[ correction_idx ][ np.random.choice( len( prediction_indices[ correction_idx ] ) ) ] = selection_indices[ correction_idx ]

	return selection_indices , prediction_indices , accuracy

def swap_menu_numbers( selection_indices , prediction_indices , correspondence_list ):
	##Permute the menu numbers in the selection and prediction indices according to the numbers in correspondence list
	for j in range( len( prediction_indices ) ):
		selection_indices[ j ][ 0 ] = correspondence_list[ selection_indices[ j ][ 0 ] ]
		for k in range( len( prediction_indices[ j ] ) ):
			prediction_indices[ j ][ k ][ 0 ] = correspondence_list[ prediction_indices[ j ][ k ][ 0 ] ]
	return selection_indices , prediction_indices

def generate_word_list( word_categories , n_menus , n_menu_items ):
	##Sample the words in each block
	##Sample all categories at once so you know there are no duplicates
	sampled_categories = np.random.choice( word_categories.keys() , int( ( n_menus * n_menu_items ) / 4. ) ,  replace=False ) 
	##Index into which menu and list of menus of words
	menu_number = -1
	##Go through and fill out the words in each menu
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

def generate_selection_and_predictions_with_accuracy( min_accuracy , max_accuracy , n_menus , n_menu_items , zipfian_dist , 
														n_recency_predictions , n_frequency_predictions , n_corrections ):	
	##Sample experiments until you get one with the right accuracy
	accuracy = 0.
	while accuracy < min_accuracy or accuracy > max_accuracy:
		selections , predictions , accuracy = generate_selections_and_predictions( n_menus , n_menu_items , zipfian_dist , 
														n_recency_predictions , n_frequency_predictions , n_corrections )
	return selections , predictions

if __name__ == "__main__":

	##Parameters of the experiment
	zipfian_dist = [ 15 , 8 , 5 , 4 , 3 , 3 , 2 , 2 ]
	word_categories = json.load( open( "categories.json" , "rb" ) )
	n_participants = 15
	n_blocks = 2
	n_menus = 3
	n_menu_items = 16
	n_recency_predictions = 1
	n_frequency_predictions = 2
	n_corrections = 18
	n_practice_questions = 8

	##Keep sampling tasks until you get one with an accuracy in this range
	min_accuracy = 0.78
	max_accuracy = 0.81

	correspondence_list = [ 1 , 2 , 0 ] ##How to map menus to new menus in expt 2

	###Generate Practice Experiment Block with specified accuracy
	practice_control_selections , practice_control_predictions = generate_selection_and_predictions_with_accuracy( min_accuracy , max_accuracy , 
																	n_menus , n_menu_items , zipfian_dist , n_recency_predictions , 
																	n_frequency_predictions , n_corrections )
	##Truncate to first n_practice questions
	practice_control_selections = practice_control_selections[ :n_practice_questions ]
	practice_control_predictions = practice_control_predictions[ :n_practice_questions ]

	##Swap menu numbers for ephemeral condition
	practice_ephemeral_selections , practice_ephemeral_predictions = swap_menu_numbers( practice_control_selections , 
																			practice_control_predictions , correspondence_list )
	
	##Fill in random words in each block
	practice_blocks = {
		"ephemeral" : [ {
			"selection_locations": practice_ephemeral_selections ,
			"predicted_locations": practice_ephemeral_predictions ,
			"words": generate_word_list( word_categories , n_menus , n_menu_items )
		} ] ,
		"control" : [ {
			"selection_locations": practice_control_selections ,
			"predicted_locations": practice_control_predictions ,
			"words": generate_word_list( word_categories , n_menus , n_menu_items )
		} ]
	}

	###Generate Experiment Block with specified accuracy
	control_selections , control_predictions = generate_selection_and_predictions_with_accuracy( min_accuracy , max_accuracy , 
																n_menus , n_menu_items , zipfian_dist , n_recency_predictions , 
																n_frequency_predictions , n_corrections )

	##Swap menu numbers for ephemeral condition
	ephemeral_selections , ephemeral_predictions = swap_menu_numbers( control_selections , control_predictions , correspondence_list )

	##Fill in random words in each condition and block
	experiment_blocks = {
		"ephemeral" : [ {
			"selection_locations": ephemeral_selections ,
			"predicted_locations": ephemeral_predictions ,
			"words": generate_word_list( word_categories , n_menus , n_menu_items )
		} for i in range( 2 ) ] ,
		"control" : [ {
			"selection_locations": control_selections ,
			"predicted_locations": control_predictions ,
			"words": generate_word_list( word_categories , n_menus , n_menu_items )
		} for i in range( 2 ) ]
	}

	##Make an experiment for each ordering of conditions
	experiment_1_data = {
		"condition_order": [ "control" , "ephemeral" ] ,
		"experiment_blocks": experiment_blocks ,
		"practice_blocks": practice_blocks ,
	}
	experiment_2_data = {
		"condition_order": [ "ephemeral" , "control" ] ,
		"experiment_blocks": experiment_blocks ,
		"practice_blocks": practice_blocks ,
	}
	participant_experiment_data = [ experiment_1_data , experiment_2_data ]

	##Dump the experiment specs to a json file
	json.dump( participant_experiment_data , open( "experiment_data.json" , "wb" ) )

