# An implementation of ephemeral adaptation, as presented by Findlater et al.

## TODO

### Expt Generation TODO

1. Update prediction algorithm to have 3 items highlighted instead of 4
2. Change menu indices in different conditions!!
3. Generate some plots of prediction errors
4. Predict over menu items?
5. Look at youtube video again!!

Explanation of Experiment Generation:
1. Randomly choose (without replacement) a menu item corresponding to each count in the Zipfian distribution.  (E.g. 15 count -- item 3, 8 count -- item 7 etc.)
2. Randomize the order of these selections (E.g. 3 count item, 8 count item, 3 count item, 15 count item etc.)
3. Generate the prediction sequence using the algorithm in "A Comparison of Static, Adaptive, and Adaptable Menus" that holds on to a few recent and a few
