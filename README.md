# MSApriori-Algorithm

This project contains the algorithm for generating frequent item-sets among multiple transactions in any shopping or retail store.
It is used for the purpose of association rule mining, with the intention that we can make some sense out of the data from the daily shopping transactions
made by millions of customers.

The algorithm considers a minimum support frequency for each item, so that all closely related items appear together rather than with other highly dissimilar items.

The algorithm first pre-processes the data given to it in the form of numbers - where numbers are represented as items in a store.

After that it takes into account the minimum support for each item.

From there on out, the MS Apriori Algorithm starts, and finally gives us the frequent item-sets printed out in a .txt folder.
