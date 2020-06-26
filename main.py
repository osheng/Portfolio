from portfolio import Portfolio

"""
TODO I'd like to forget about modeling whole portfolios for now. Instead,
the first goal will be to create an asset (which takes in a csv name or df
with price history)
and creates an object with the asset history, and then create methods for
basic manipulations.
* find the earliest and latest dates
* find the price on specific dates
* get day to day rates of Return
* find max and min daily rates of return
* find the n days with the highest (or lowest RoR)
* drop the max and min daily rates (not necessary)
* compute mean and median daily rates (including or exlcuding extremes)
* compute rate of return over a set period (like earliest date to latest)
* etc

The motivation here is that when different companies post rates of return
it's not clear to me that they are all being calculated in the same way. So,
I would like to be able to calculate everything from scratch to see rates of
return are calculated given a set of dataself.

My second motivation is to be able to test hypotheses out there like the
following:
* market timing is difficult to the point of not being worth attempting.
    (split an asset into as many consecutive year-long segments as possible)
    and compare the rates of return on those segments
* how much of a year's rate of return is determined by the ten best days
    in the year (or ten worst days)
* if you remove the ten best days in a year for multiple years, how much
    does that affect performance? What about the ten worst days?

"""
def model(p: Portfolio):
    pass
