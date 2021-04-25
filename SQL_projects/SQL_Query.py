queries = ["" for i in range(0, 15)]

### 0. Report the votes for the normal (i.e, not special) Senate Election in Maryland in 2018.
### Output column order: candidatename, partyname, candidatevotes
### Order by candidatename ascending
queries[0] = """
select candidatename, partyname, candidatevotes
from sen_state_returns
where year = 2018 and statecode = 'MD' and specialelections = False
order by candidatename asc;
"""

### 1. Write a query to find the maximum, minimum, and average population in 2010 across all states.
### The result will be a single row.
### Truncate the avg population to a whole number using trunc
### Output Columns: max_population, min_population, avg_population
queries[1] = """
select max(population_2010) as max_population, min(population_2010) as min_population, 
trunc(avg(population_2010)) as avg_population
from states
group by ();
"""

### 2. Write a query to find the candidate with the maximum votes in the 2008 MI Senate Election. 
### Output Column: candidatename
### Order by: candidatename
queries[2] = """
select candidatename
from sen_state_returns
where statecode = 'MI' and year = 2008 and 
candidatevotes = (select max(candidatevotes) from sen_state_returns where statecode = 'MI' and year = 2008)
order by candidatename asc;
"""

### 3. Write a query to find the number of candidates who are listed in the sen_state_returns table for each senate election held in 2018. 
### Note that there may be two elections in some states, and there should be two tuples in the output for that state.
### 'NA' or '' (empty) should be treated as candidates. 
### Output columns: statecode, specialelections, numcandidates
### Order by: statecode, specialelections
queries[3] = """
select statecode, specialelections, count(candidatename) as numcandidates
from sen_state_returns
group by statecode, specialelections, year
having year = 2018 
Order by statecode asc, specialelections asc ;
"""

### 4. Write a query to find, for the 2008 elections, the number of counties where Barack Obama received strictly more votes 
### than John McCain.
### This will require you to do a self-join, i.e., join pres_county_returns with itself.
### Output columns: num_counties
queries[4] = """
select count(w.countyname) as num_counties
from pres_county_returns w, pres_county_returns l
where l.candidatename = 'John McCain'
and w.candidatename = 'Barack Obama'
and l.statecode = w.statecode
and l.countyname = w.countyname
and l.year = 2008
and w.year=2008
and w.candidatevotes > l.candidatevotes
;
"""


### 5. Write a query to find the names of the states with at least 100 counties in the 'counties' table.
### Use HAVING clause for this purpose.
### Output columns: statename, num_counties
### Order by: statename
queries[5] = """
select states.name as statename ,count(counties.name) as num_counties
from counties, states 
where counties.statecode = states.statecode
group by statename
having count(counties.name) >= 100 
order by statename asc;
"""

### 6. Write a query to construct the following result:
###     (statecode, total_votes_2008, total_votes_2012)
### to count the total number of votes by state for Barack Obama in the two elections.
###
### Use the ability to "sum" an expression (e.g., the following query returns the number of counties in 'AR')
### select sum(case when statecode = 'AR' then 1 else 0 end) from counties;
###
### Order by: statecode
queries[6] = """
with election_08 (statecode, total_votes_2008) as
(select statecode, sum(candidatevotes) as total_votes_2008
from pres_county_returns
where candidatename = 'Barack Obama' 
and year = 2008
group by statecode),

election_12 (statecode, total_votes_2012) as
(select statecode, sum(candidatevotes) as total_votes_2012
from pres_county_returns
where candidatename = 'Barack Obama' 
and year = 2012
group by statecode)

select statecode, total_votes_2008, total_votes_2012
from election_08 natural join election_12;

"""

### 7. Write a query to find the disparity between the populations listed in 'states' table and those listed in 'counties' 
### table for 1950 and 2010.
### Result should be: 
###        (statename, disparity_1950, disparity_2010)
### So disparity_1950 = state population 1950 - sum of population_1950 for the counties in that state
### Use HAVING to only output those states where there is some disparity (i.e., where at least one of the two is non-zero)
### Order by statename
queries[7] = """
with countycount (statecode, nineties_cpop , twok_cpop) as
(select statecode,  sum(population_1950) as nineties_cpop, sum(population_2010) as twok_cpop
from counties
group by statecode)
select name as statename, population_1950 - nineties_cpop as disparity_1950, population_2010 - twok_cpop as disparity_2010
from states join countycount 
on states.statecode = countycount.statecode
where (population_1950 - nineties_cpop) <> 0 or (population_2010 - twok_cpop) <> 0
order by name asc;;
"""


### 8. Use 'EXISTS' or 'NOT EXISTS' to find the states where no counties have population in 2010 above 500000 (500 thousand).
### Output columns: statename
### Order by statename
queries[8] = """
SELECT states.name as statename
FROM states 
WHERE NOT EXISTS
(SELECT * FROM counties  WHERE counties.statecode = states.statecode and counties.population_2010 > 500000)
order by statename asc ;;
"""

### 9. Write a query to find all counties (and their basic information) that have a unique name across all states. 
### Use scalar subqueries to simplify the query.
### Output columns: all attributes of counties (name, statecode, population_1950, population_2010)
### Order by name, statecode
queries[9] = """
select name, statecode, population_1950, population_2010
from counties temp
where 1 in (select count(statecode) from counties group by name having name= temp.name);;
"""

### 10. Use Set Intersection to find the counties that Barack Obama lost in 2008, but won in 2012.
### We have created a temporary table using WITH that you can use (or not).
###
### Output columns: countyname, statecode
### Order by countyname, statecode
queries[10] = """
with temp1 as (select countyname, statecode, year, max(candidatevotes) as maxvotes
        from pres_county_returns 
        group by countyname, statecode, year
        ),
     temp2 as (
             select p.countyname, p.statecode, p.year, p.candidatevotes = t.maxvotes as won
             from pres_county_returns p, temp1 t
             where p.countyname = t.countyname and p.statecode = t.statecode and p.year = t.year and p.candidatename = 'Barack Obama'
)
select countyname, statecode 
from temp2
where year=2008 and won = 'false'

intersect

select countyname, statecode 
from temp2
where year = 2012 and won = 'true'

Order by countyname asc, statecode asc;
"""


### 11. Find all presidential candidates listed in pres_county_returns who did NOT run for elections as a senator.
### HINT: Use "except" to simplify the query
###
### Every candidate should be reported only once. You will see incorrect answers in there because "names" don't match -- that's fine.
###
### Output columns: candidatename
### Order by: candidatename
queries[11] = """
SELECT candidatename
FROM pres_county_returns

EXCEPT

SELECT candidatename
FROM sen_state_returns;;
"""



### 12. Write a query listing the months and the number of states that were admitted to the union (admitted_to_union field) in that month.
### Use 'extract' for operating on dates, and the ability to create a small inline table in SQL. For example, try:
###         select * from (values(1, 'Jan'), (2, 'Feb')) as x;
###
### Output columns: month_no, monthname, num_states_admitted
### month should take values: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
### Order by: month_no
queries[12] = """
with months (month_no, monthname) as
(values(1, 'Jan'), (2, 'Feb'), (3, 'Mar'), (4, 'Apr'), (5, 'May'), (6, 'Jun'), (7, 'Jul'), (8, 'Aug'),
 (9, 'Sep'), (10, 'Oct'), (11, 'Nov'), (12, 'Dec'))

select month_no, monthname, count(name) as num_states_admitted
from months join states on (month_no = extract(month from admitted_to_union))
group by month_no, monthname
order by month_no asc;
"""


### 13. Create a view pres_state_votes with schema (year, statecode, candidatename, partyname, candidatevotes) where we maintain aggregated counts by statecode (i.e.,
### candidatevotes in this view would be the total votes for each state, including states with statecode 'NA').
queries[13] = """
create view pres_state_votes as
select year, statecode, candidatename, partyname, sum(candidatevotes) as candidatevotes
from pres_county_returns
group by year, statecode, candidatename, partyname 
;;
"""

### 14. Use a single ALTER TABLE statement to add (name, statecode) as primary key to counties, and to add CHECKs that neither of the two populations are less than zero.
### Name the two CHECK constraints nonzero2010 and nonzero1950.
queries[14] = """
alter table counties
add constraint nonzero2010 check (population_2010 >= 0),
add constraint nonzero1950 check (population_1950 >= 0),
add primary key (name, statecode)

"""