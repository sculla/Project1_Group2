# Project1_Group2
Metis MTA 

## Making a Feature Branch for your contribution:
When making a branch for your part of the project, please use the feature/<your branch name> to denote your part of the project. After the successful completion of the feature, we will merge it to the develop branch.  
With this, we are able to easily each work off of a single branch, develop, and have our features able to be pushed back to that branch for the full integration. 

Please let me know if you're having any issues with this, I've included a link here to review as well [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow) 

--@sculla

## MVP - Stations that will get money/productive canviser  
"Send your staff with these daytime hours of 6am - 8pm to these 10 stations for the best turn out"  
* busiest stations  
* sustained flow  

### Pivot List: Sub Regions for Tech centers / Universities  
* diversity of buroughs  
* tech hubs?  
## Please check issue list

Feature ideas:
* adding a geo heat map  
** pulling second DB that maps the names of the stations to an address  
* turnstile graphs for the traffic by hour?  
** not just the most popular 
* remove tourism hubs  


Column math to do:
*first check if counts are increasing per station or per station AND per line, becuase of the cumulative count issue 
using whichever makes sense:

how to check: normalize the counts (counts[i]-=counts[0] for each station (or station and line, depeding on the system) and graph the normalized counts vs entry number for that particular station with an overlay for all stations >> this graph will allow us check for whether the data increases consistantly across the board or if there are strange jumps. 

We should also do this for date time, to see if stations have any strange missing chunks of time!!

##we can use these normalized counts to make the first bar graph that we talked out. since the normalized_count[lastindex] = rides in a week, a sorted bar-graph of these last entries (normalized) will give us our top stations for the week


if the counts go up without any weird flucuations  >> then we can proceed to calculate our riders added per time chunk (rides(by station) = count[i] - count [i-1] for the group) and for our time normalized rate (station rate (by station) = (count[i] - count [i-1]) / ( time [i] - time [i-1])     >> this is going to cause an issue for the FIRST INDEX. since it does not have a previous entry, I'm okay with setting them to zero, but lets all agree on that.

we can use these values to make two other important graphs: these graphs are going to show us WHEN stations are getting the most riders. we only need to run these for the *best* stations based on the last bar graph. codily, we can prob just make a list of stations from the greatest values.
1. count at time, vs time for stations of interest (scatter plots, should be diff plot per station we plot)
2. rate at time vs time, overlay between stations should be fine because it is defacto noramlized for binning here(I would fit with a spline for each station.)

after these, we can think about next steps. . . 




