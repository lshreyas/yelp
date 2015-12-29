# Written by Mariah Krimchansky, Nicole Gonzalez, Shreyas Lakhtakia
# Last updated: 12/11/15, 11pm
# ELE/COS 381
# Final Project

import json
import sys
import matplotlib.pyplot as plt

# READ IN DATA -----------------------------------------------------------------

data = []
with open('yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json') as f:
    for line in f:
        tmpdata = (json.loads(line))
        #make sure business is a restaurant
        if "Restaurants" in tmpdata["categories"]:
            #make sure business is in pittsburgh
            #right now changed to pennsylvania for more data..
            if " PA " in tmpdata["full_address"]:
                #if both conditions were met, can add to data
                data.append(tmpdata)
    print("done reading in data...")

# SORT REVIEW DATA BY ZIP CODE  ------------------------------------------------

# create a hashtable to store the total number of restaraunts in each zip code
zipTotalRest = {}
# create a hashtable that, for now, just has the total score (will later make average)
zipAveRest = {}
# create a hashtable to store the total number of reviews in each zip code
zipTotalRevs = {}
    
for restaurant in data:
    address = restaurant["full_address"]
    #get the zip code from the address
    #not all addresses seem to have a zip code, so putting a
    #try- catch to prevent index out of bound
    try:
        zipCode = address.split(", ")[1].split(' ')[1]
        
        #check if has zipcode
        try: 
            int(zipCode)
            # by doing str(zipCode), the keys get stored as strings, but we need them to be ints, for uniformity in all our hashtables
            
            if zipCode in zipTotalRest.keys():
                zipTotalRest[str(zipCode)] += 1
                zipAveRest[str(zipCode)] += restaurant["stars"]
                zipTotalRevs[str(zipCode)] += restaurant["review_count"]
            else:
                zipTotalRest[str(zipCode)] = 1
                zipAveRest[str(zipCode)] = restaurant["stars"]
                zipTotalRevs[str(zipCode)] = restaurant["review_count"]
        
        except ValueError: #throw out data without a zipcode
            pass        
    except IndexError:
        pass

# READ IN AVERAGE/MEDIAN INCOME FOR ZIPCODES -----------------------------------

zipMedInc = {}
zipAveInc = {}
zipDifInc = {}
zipPopDen = {}

f = open('zip_income')
#read 7 lines plus one space per zipcode
while True:
    brackets = [0] * 6
    total = f.readline()
    if total == "":
        break #this means the end of file was reached
    else:
        inc_zipcode = int(total.split('\t')[0].replace("'", ''))                                        
    for i in range(0,6):
        line = f.readline().split('\t')
        brackets[i] = int((line[2].strip('\n').replace("'", '')))
    #discard next line - it is blank
    f.readline()

    #if the zip code is relevant, calculate mean add it to the hashtable
    # 0 = 0 to 25000, 1 = 25000 to 50000, ...
    # for dif, the number represents the difference between the two income ranges
    # (if 25 and 75 percentile were in same bracket, dif = 0)
    if str(inc_zipcode) in zipTotalRest.keys():
        
        #put in population density
        zipPopDen[inc_zipcode] = sum(brackets)
        
        #variables to calcuate mean, median, difference in data
        median_index = float(sum(brackets))/2
        perc25_index = float(sum(brackets))/4
        perc75_index = median_index + perc25_index
        val_25 = 0
        val_75 = 0
        count_index = 0
        #find median
        for i in range(0,6):
            count_index = count_index + brackets[i]
            if count_index > median_index:
                #this is the median bracket!
                zipMedInc[inc_zipcode] = i
                break
        #do the same for 25, 75 percentile
        count_index = 0
        for i in range(0,6):
            count_index = count_index + brackets[i]
            if count_index > perc25_index:
                #25th percentile
                val_25 = i
                break
        count_index = 0
        for i in range(0,6):
            count_index = count_index + brackets[i]
            if count_index > perc75_index:
                #75th percentile
                val_75 = i
                break
        zipDifInc[inc_zipcode] = val_75 - val_25
        #find 'rough' average
        weight = 0
        for i in range(0,6):
            weight = weight + (12500 + 25000 * i) * brackets[i]
        zipAveInc[inc_zipcode] = weight/sum(brackets)

print "Median income by zipcode:"
print zipMedInc
print

print "Diff income by zipcode:"
print zipDifInc
print

print "Average income by zipcode:"
print zipAveInc
print

print "Population Density by zipcode:"
print zipPopDen
print

# CALCULATE MEAN/BAYESIAN RESTAURANT SCORE BY ZIP CODE -------------------------

zipBayRest = {}
R = 0
N = 0

for key in zipAveRest:
    #calculate mean restaurant score by zip code
    #do we also want to do a weighted average???
    zipAveRest[key] = zipAveRest[key]/zipTotalRest[key]
    R += zipAveRest[key]*zipTotalRevs[key]
    N += zipTotalRevs[key]
R = R/N
    
for key in zipAveRest:    
    #calculate bayesian restaurant score by zip code
    #do we want to do the bayesian restaurant specificly??? - will be more complex
    r = zipAveRest[key]
    n = zipTotalRevs[key]
    zipBayRest[key] = ((N*R + r*n)/(N + n))

print "Average of restaurant score by zipcode:"
print zipAveRest
print
print "Bayesian average of restaurant score by zipcode:"
print zipBayRest
print
print "Restaurant density by zipcode:"
print zipTotalRest
print
print len(zipMedInc)
print len(zipAveRest)

# POPULATION DENSITY BY ZIP CODE -----------------------------------------------


# AVERAGE RESTAURANT PRICE BY ZIP CODE  ----------------------------------------
#this will be best shown with a map I think, so using Google Earth API


# PLOT ALL COMBINATIONS OF VARIABLES BY ZIP CODE -------------------------------

#the variables to be plotted are: zipMedInc, zipDifInc, zipAveInc, zipPopDen, zipAveRest, zipBayRest, zipTotalRest
zipMedIncList = []
zipDifIncList = []
zipAveIncList = []
zipPopDenList = []
zipAveRestList = []
zipBayRestList = []
zipTotalRestList = []

for key in zipAveInc:
	# for each zip code in this hashtable (zipAveInc), store values corresponding to this zip code in lists
	# ONLY if data for that ZIP code is also available in the hash tables storing Yelp data

	if str(key) in zipAveRest: #this hash table has zip codes stored as strings!
		zipMedIncList.append(zipMedInc[key])
		zipDifIncList.append(zipDifInc[key])
		zipAveIncList.append(zipAveInc[key])
		zipPopDenList.append(zipPopDen[key])
		zipAveRestList.append(zipAveRest[str(key)])
		zipBayRestList.append(zipBayRest[str(key)])
		zipTotalRestList.append(zipTotalRest[str(key)])

# plotting average restaurant rating against average income
fig1 = plt.figure(1)
plt.plot(zipAveIncList, zipAveRestList, 'ro')
plt.xlabel('Average Income, by ZIP')
plt.ylabel('Average Restaurant Rating, by ZIP')
plt.show()

# plot average restaurant Bayesian rating vs average rating
fig2 = plt.figure(2)
plt.plot(zipAveRestList, zipBayRestList, 'bo')
plt.ylabel('Average Bayesian Rating, by ZIP')
plt.xlabel('Average Restaurant Rating, by ZIP')
plt.show()

# plot Bayesian average restaurant rating against average income
fig3 = plt.figure(3)
plt.plot(zipAveIncList, zipBayRestList, 'go')
plt.xlabel('Average Income, by ZIP')
plt.ylabel('Average Bayesian Rating, by ZIP')
plt.show()

