import json
import numpy as np

zipfian_dist = [ 15 , 8 , 5 , 4 , 3 , 3 , 2 , 2 ]
word_categories = json.load( open( "categories.json" , "rb" ) )

n_participants = 20
n_blocks = 2
n_menus = 3
n_menu_items = 16
n_predictions = 4

participant_experiment_data = []
for i in range( n_participants ):

	##Half of the experiments are control then ephemeral, and the rest are the reverse
	if i <= n_participants / 2.:
		condition_order = [ "control" , "ephemeral" ]
	else:
		condition_order = [ "ephemeral" , "control" ]

	#selection_locations = [ [ 0 , 0 ] ] * 126
	##Generate the list of click locations
	selection_indices = []
	menu_indices = np.random.choice( n_menu_items , len( zipfian_dist ) ,  replace=False ) ##Sample w/out replacement the number of menu ids that we have counts for
	for j in range( len( zipfian_dist ) ): ##For each number of counts in the zipfian dist
		for k in range( zipfian_dist[ j ] ): ##For the number specified by the zipfian dist, add one trial
			selection_indices.append( menu_indices[ j ] )
	selection_indices = np.array( selection_indices )
	np.random.shuffle( selection_indices ) ##Shuffle menu locations
	selection_indices = selection_indices.tolist()	
	
	prediction_indices = []
	##Algorithm from: A Comparison of Static, Adaptive, and Adaptable Menus
	recency_list = np.zeros( len( selection_indices ) )
	frequency_list = np.zeros( len( selection_indices ) )
	frequency_predictions = np.random.choice( n_menu_items , n_predictions ).tolist() ##Start with some random predictions
	recency_predictions = frequency_predictions[ 2: ]
	frequency_predictions = frequency_predictions[ :2 ]
	incorrect_predictions = []
	for j , idx in enumerate( selection_indices ):
		prediction_indices.append( frequency_predictions + recency_predictions )
		frequency_list[ idx ] += 1 ##Add 1 to frequency counter of current
		recency_list[ idx ] = 0
		recency_list += 1 ##Add 1 to all recency counters
		if idx not in recency_predictions and idx not in frequency_predictions: ##If the current isn't already in the partition, figure out what to do but otherwise, don't do anything
			incorrect_predictions.append( j )
			least_recent_id = recency_predictions[ np.argmax( recency_list[ recency_predictions ] ) ]
			least_frequent_id = frequency_predictions[ np.argmin( frequency_list[ frequency_predictions ] ) ]
			if frequency_list[ least_recent_id ] < frequency_list[ least_frequent_id ]:
				recency_predictions[ list( recency_predictions ).index( least_recent_id ) ] = idx
			else:
				frequency_predictions[ list( frequency_predictions ).index( least_frequent_id ) ] = least_recent_id
				recency_predictions[ list( recency_predictions ).index( least_recent_id ) ] = idx

	correct_indices = np.random.choice( incorrect_predictions , 18 )
	for idx in correct_indices:
		replace_idx = np.random.choice( 4 )
		prediction_indices[ idx ][ replace_idx ] = selection_indices[ idx ]

	#correct_predictions = 0
	#for j in range( len( selection_indices ) ):
	#	if selection_indices[ j ] in prediction_indices[ j ]:
	#		correct_predictions += 1
	#print( "Accuracy: " + str( correct_predictions / float( len( selection_indices ) ) ) )

	selection_locations = []
	predicted_locations = []
	for j in range( len( selection_indices ) ):
		menu_indices = np.random.choice( 3 , 3 , replace=False )
		for k in menu_indices:
			selection_locations.append( [ k , selection_indices[ j ] ] )
			predicted_locations.append( [] )
			for l in range( len( prediction_indices[ j ] ) ):
				predicted_locations[ -1 ].append( [ k , prediction_indices[ j ][ l ] ] )

	correct_predictions = 0
	for j in range( len( selection_locations ) ):
		if selection_locations[ j ] in predicted_locations[ j ]:
			correct_predictions += 1
	print( "Accuracy: " + str( correct_predictions / float( len( selection_locations ) ) ) )

	block_list = {}
	for condition in condition_order:
		block_list[ condition ] = []
		for j in range( n_blocks ):	
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

			##Make a block dictionary, so far it just has the words in it
			##Add it to the block list for the current condition
			block = {}
			block[ "words" ] = word_list
			block_list[ condition ].append( block )

	experiment_data = {
		"condition_order": condition_order ,
		"selection_locations": selection_locations ,
		"predicted_locations": predicted_locations ,
		"experiment_blocks": block_list ,
	}

	participant_experiment_data.append( experiment_data )

json.dump( participant_experiment_data , open( "experiment_data.json" , "wb" ) )



