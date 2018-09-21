import json

n_participants = 20

participant_experiment_data = []

for i in range( n_participants ):

	condition_order = [ "control" , "ephemeral" ]
	selection_locations = [ [ 0 , 0 ] ] * 126
	predicted_locations = [ [ [ 0 , 0 ] , [ 0 , 1 ] , [ 0 , 2 ] ] ] * 126

	word_list = []
	for j in range( 3 ):
		word_list.append( [] )
		for k in range( 16 ):
			word_list[ j ].append( "Word " + str( k ) )

	block_list = {}
	for condition in condition_order:
		block_list[ condition ] = []
		for j in range( 2 ):
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
