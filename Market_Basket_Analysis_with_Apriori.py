import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)      

df = pd.read_excel("/kaggle/input/market-basket-analysis/Assignment-1_Data.xlsx")


# We are trying to understand the data.

def check_df(dataframe, head=5):
    print("################### Shape ####################")
    print(dataframe.shape)
    print("#################### Info #####################")
    print(dataframe.info())
    print("################### Nunique ###################")
    print(dataframe.nunique())
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("################## Quantiles #################")
    print(dataframe.describe([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
    print("#################### Head ####################")
    print(dataframe.head(head))

check_df(df)


# Data Preparation

# We set a small threshold value to account for the presence of outliers in the data.
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return low_limit, up_limit

# We are writing a function to equalize the outlier values in the data to threshold values.
def replace_with_thresholds(dataframe, variable):
    low_limit, up_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit

# We are removing the negative and outlier values from the quantity and price variables.
def retail_data_prep(dataframe):
    dataframe = dataframe[dataframe["Quantity"] > 0]
    dataframe = dataframe[dataframe["Price"] > 0]
    replace_with_thresholds(dataframe, "Quantity")
    replace_with_thresholds(dataframe, "Price")
    return dataframe

df = retail_data_prep(df)

df.describe().T


# We are selecting only the data for France in order to narrow down the data since it is large.
df_fr = df[df['Country'] == "France"]

# We are creating a table based on the sum of Quantity for the breakdown of BillNo and Itemname.
df_fr.groupby(['BillNo', 'Itemname']).agg({"Quantity": "sum"}).unstack().fillna(0).iloc[0:5, 0:5]

# We are converting the table to a completely Boolean type.
fr_inv_pro_df=df_fr.groupby(['BillNo', 'Itemname']). \
                agg({"Quantity": "sum"}). \
                unstack(). \
                fillna(0). \
                applymap(lambda x: 1 if x > 0 else 0)


# We are using the Apriori method to find the support values of the products.
frequent_itemsets = apriori(fr_inv_pro_df.astype("bool"),   
                            min_support=0.01,
                            use_colnames=True)

frequent_itemsets.sort_values("support", ascending=False).head()


# With this method, we can obtain the support, confidence, and lift values of the products with the support values that we input.
rules = association_rules(frequent_itemsets,       
                          metric="support",        
                          min_threshold=0.01)


# By setting a threshold value for the metrics obtained, we can see the product associations in Apriori algorithm.
rules[(rules["support"]>0.05) & (rules["confidence"]>0.1) & (rules["lift"]>5)]. \
sort_values("confidence", ascending=False).head(10)


# Thus, we can see the products that are closely related to each other.


# Providing product recommendations to users at the shopping cart stage.

def arl_recommender(rules_df, product_name, rec_count=1):
    sorted_rules = rules_df.sort_values("lift", ascending=False)
    recommendation_list = []
    for i, product in enumerate(sorted_rules["antecedents"]):
        for j in list(product):
            if j == product_name:
                recommendation_list.append(list(sorted_rules.iloc[i]["consequents"])[0])

    return recommendation_list[0:rec_count]

# When we sort the items in the cart by Lift,
# we can select the desired product and see the desired number of other products that are most closely related to it.


# For example; 'PLASTERS IN TIN CIRCUS PARADE'
arl_recommender(rules, ('Quantity', 'PLASTERS IN TIN CIRCUS PARADE'), 3) 


