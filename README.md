# AntennaOptimization

This problem came about after the hurricane that hit Puerto Rico and took out almost all of the island. First responders were sent down to Puerto Rico but did not have great communication opportunities because all of the cell towers were down.

Wanted to find the best way to cover the island with service for radio communication, but rather than doing the obvious maximum coverage problem, we had a twist.

We knew that there was going to be more people needing help than others, and we had a good idea of where this was going to occur, but we could not be sure until boots were on the ground and saw the demand across the island. Because of this, we decided we wanted to do a min max regret problem.

This min max regret problem breaks down like this: if we think there will be an arbitrary demand of 10 in Northern Puerto Rico and 1 every where else, we will put an antenna in the middle of the Northern part in order to cover that demand. But if we get to the island and realize that there is only 5 demand in the Northern part and there is 5 demand in the east, then we have an antenna improperly placed to cover the most people; we would be regretting where we placed that antenna. This is the min min regret; we are trying to minimize our maximum regret of placing an antenna somewhere in a place that turns out to have low demand.

The code was done in Spyder using pyomo.
