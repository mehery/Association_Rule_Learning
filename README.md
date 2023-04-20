# Association_Rule_Learning

### Association Rule Learning

Association Rule Learning is also known as basket analysis.

Product recommendations can be made based on the rules learned through association analysis.

It is a rule-based machine learning technique used to discover patterns in data.

### Apriori Algorithm

It is a method of basket analysis that is used to discover associations among products.

The Apriori algorithm has three metrics that allow us to observe the patterns and structures of relationships within the dataset.

These three metrics are:

Support(X,Y) = Freq(X,Y) / N >>> The probability of X and Y occurring together.

Confidence(X,Y) = Freq(X,Y) / Freq(X) >>> The probability of Y being purchased when X is purchased.

Lift = Support(X,Y) / Support(X) * Support(Y) >>> The probability of Y being purchased when X is purchased increases by the lift value.

Dataset Details

BillNo: 6-digit number assigned to each transaction. Nominal.

Itemname: Product name. Nominal.

Quantity: The quantities of each product per transaction. Numeric.

Date: The day and time when each transaction was generated. Numeric.

Price: Product price. Numeric.

CustomerID: 5-digit number assigned to each customer. Nominal.

Country: Name of the country where each customer resides. Nominal.
