#### Dataset and Schema

The dataset contains results of senate and presidential elections for a subset of the years. For the senate, it contains only the statewide results from 1976 to 2018, whereas for the presidential elections, it contains county-level data going back to 2000.

The schema of the tables should be self-explanatory.

The data was collected from https://electionlab.mit.edu/data.

Some things to remember:

The special senate elections are problematic. Typically senate elections take place every 6 years, with the two elections for a given state staggered. So generally speaking, any given year (say 2018), there would only be one senate election per state. However, because of special circumstances, there are sometimes 2 elections in a given year for the same state. These two can be disambiguated based on the specialelections boolean flag in the database.
In many cases (especially for complex queries or queries involving max or min), you will find it easier to create temporary tables using the with construct. This also allows you to break down the full query and makes it easier to debug.