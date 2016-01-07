# Written by Mariah Krimchansky, Nicole Gonzalez, Shreyas Lakhtakia
# Last updated: 12/11/15, 11pm
# ELE/COS 381
# Final Project

import json
import sys
import matplotlib.pyplot as plt
from scipy import stats

# READ IN DATA -----------------------------------------------------------------

# some data doesnt list its price range, and so it was looked up by hand

PriceRange0 = ["McDonald's", "Subway", "Popeyes", "Pizza Hut", "Pizza Shack", "Arby's", \
               "KFC", "Au Bon Pain Co Inc", "Caribou Coffee", "GM Dog N' Burger Shoope", \
               "Latina Pizza", "Bellisario Pizza Shop", "Hunan Wok Chinese Restaurant", \
               "Salonika Imports", "Bobby's Lounge", "Wang's Kitchen", "Amazon Cafe", \
               "Rowdy BBQ", "Jim's Famous Sauce", "Pizzeria Primos", "Sam's Sun Sandwich",\
               "Skyvue", "Mama Pepino's", "Vocelli Pizza of Dormont", "Vocelli Pizza", \
               "The Potato Patch", "Riviera Pizza & Pasta", "Z-Best Barbeque", \
               "California Taco Shop", "Billu's Indian Grill", "Gavino's Pizzeria", \
               "The Warhol: Cafe", "Red Hot Pittsburgh","Soup Nancys","The Golden Palace Buffet", \
               "Angelina's Pizzeria", "Sandpresso", "Edgar's Authentic Mexican","Suzy's Sandwiches & Deli", \
               "Craftwork Kitchen", "Jean's Southern Cuisine", "51 Wings and Things", "Juice Up 412", \
               "Binali Pizza", "AVA Cafe + Lounge", "Everest Ethnic Restaurant", "Diyor Cafe and Lounge", \
               "Philly PittStop", "Pizza Care"]

PriceRange1 = ["Lotus Garden", "The Green Mango", "Vocelli Pizza", "Hot Metal Diner", \
               "Steel City Diner", "Geno's Restaurant", "Liberty Avenue Deli", \
                "Lone Star Steakhouse", "Bai Ling Chinese Restaurant", "Boonda's", \
                "Suds & Subs", "George Aiken", "Finn McCools", "The Jaggerbush", \
                "Cuzamil", "Maldini's Taste of Italy", "Mulligan's Sports Bar and Grill",\
                "Island Cafe", "Baba D's","The Salad Cafe", "Molly Brannigans", "The Green Mango Thai Cafe",\
                "E. M. Pizzeria", "Sal's New York Pizzeria", "Angelias Italian Grille", "La Hacienda",\
                "Pittza Rella", "Damon's Grill & Sports Bar", "Senor Frogs", "Mullen's", \
                "Cent Anni's", "Melange Bistro Bar", "Pittsburgh Pizza Grill", "Roxanne's Take-Out  & Catering", \
                "Chen's Wok","Pizza Milano", "Bellamonte Pizza", "The Smokehouse Bar & Grill", "1905 Eatery", \
                "Disilva's Pizzeria", "Johnny Rockets"]

PriceRange2 = ["Michael's Restaurant & Lounge", "The Rivers Casino", "Pittsburgh Restaurant Week", \
               "Club Colony", "Carnegie Delicatessen and Catering"]
data = []
with open('yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_business.json') as f:
    for line in f:
        tmpdata = (json.loads(line))
        #make sure business is a restaurant
        if ("Food" in tmpdata["categories"] or "Restaurants" in tmpdata["categories"]):
            #make sure business is in pittsburgh
            #right now changed to pennsylvania for more data..
            if " NC " in tmpdata["full_address"]:
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
# create a hashtable to store how many of each restaurant (price wise) in each zip code
zipTotPriRest = {}
# create a hashtable to store total score (price wise) (will late make average)
zipAvePriRest = {}
totKeyEr = 0
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
                
                #add the restaurant price by pulling out the dollar signs
                try:
                    price = int(restaurant["attributes"]["Price Range"]) - 1
                except KeyError:
                    if restaurant['name'] in PriceRange0:
                        price = 0
                    elif restaurant['name'] in PriceRange1:
                        price = 1
                    elif restaurant['name'] in PriceRange2:
                        price = 2
                zipTotPriRest[str(zipCode)][price] += 1
                zipAvePriRest[str(zipCode)][price] += restaurant["stars"]
            else:
                zipTotalRest[str(zipCode)] = 1
                zipAveRest[str(zipCode)] = restaurant["stars"]
                zipTotalRevs[str(zipCode)] = restaurant["review_count"]
                
                #add the restaurant price by pulling out the dollar signs
                try:
                    price = int(restaurant["attributes"]["Price Range"]) - 1
                except KeyError:
                    print restaurant['name']
                    if restaurant['name'] in PriceRange0:
                        price = 0
                    elif restaurant['name'] in PriceRange1:
                        price = 1
                    elif restaurant['name'] in PriceRange2:
                        price = 2
                zipTotPriRest[str(zipCode)] = [0,0,0]
                zipTotPriRest[str(zipCode)][price] += 1
                zipAvePriRest[str(zipCode)] = [0.,0.,0.]
                zipAvePriRest[str(zipCode)][price] += restaurant["stars"]
        except ValueError: #throw out data without a zipcode
            pass        
    except IndexError:
        pass
print "KeyError = " + str(totKeyEr)
# READ IN AVERAGE/MEDIAN INCOME FOR ZIPCODES -----------------------------------

zipMedInc = {}
zipAveInc = {}
zipDifInc = {}
zipPopDen = {}

f = open('zip_income_NC')
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
    for i in range(0,3):
        if zipTotPriRest[key][i] != 0:
            zipAvePriRest[key][i] = zipAvePriRest[key][i]/zipTotPriRest[key][i]
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
print "Restaraunt Price Range density by zipcode"
print zipTotPriRest
print
print "Average Price range for restaurant score by zipcode"
print zipAvePriRest
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

#restaurant variables split by how expensive the restaurant is
#average restaurant ratings, divided by their expensiveness
zipLoAveRest = []
zipMedAveRest = []
zipHiAveRest = []
zipLoNoZero = []
zipMedNoZero = []
zipHiNoZero = []

#restaurant density, divided by their expensiveness
zipLoDenRest = []
zipMedDenRest = []
zipHiDenRest = []

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
        
        if zipAvePriRest[str(key)][0] != 0:
            zipLoAveRest.append(zipAvePriRest[str(key)][0])
            zipLoNoZero.append(zipAveInc[key])
        if zipAvePriRest[str(key)][1] != 0:
            zipMedAveRest.append(zipAvePriRest[str(key)][1])
            zipMedNoZero.append(zipAveInc[key])
        if zipAvePriRest[str(key)][2] != 0:
            zipHiAveRest.append(zipAvePriRest[str(key)][2])
            zipHiNoZero.append(zipAveInc[key])
        
        zipLoDenRest.append(zipTotPriRest[str(key)][0])
        zipMedDenRest.append(zipTotPriRest[str(key)][1])
        zipHiDenRest.append(zipTotPriRest[str(key)][2])

# plotting average restaurant rating against average income
fig1 = plt.figure(1)

slope, interc, r_value, p_value, std_err = stats.linregress(zipAveIncList,zipAveRestList)
plt.plot(zipAveIncList, zipAveRestList, 'ro')
lineval= [slope * min(zipAveIncList) + interc, slope * max(zipAveIncList) + interc]
plt.plot([min(zipAveIncList), max(zipAveIncList)], lineval)
plt.text(70000,3.8,"r_value = " + str(round(r_value,3)))
plt.title('NC Average Income vs. Average Restaurant Rating')
plt.xlabel('Average Income, by ZIP')
plt.ylabel('Average Restaurant Rating, by ZIP')
plt.show()

# plot average restaurant Bayesian rating vs average rating
fig2 = plt.figure(2)

slope, interc, r_value, p_value, std_err = stats.linregress(zipAveRestList,zipBayRestList)
plt.plot(zipAveRestList, zipBayRestList, 'ro')
lineval= [slope * min(zipAveRestList) + interc, slope * max(zipAveRestList) + interc]
plt.plot([min(zipAveRestList), max(zipAveRestList)], lineval)
plt.text(3.3,3.560,"r_value = " + str(round(r_value,3)))
plt.xlabel('Average Bayesian Rating, by ZIP')
plt.ylabel('Average Restaurant Rating, by ZIP')
plt.show()

# plot Bayesian average restaurant rating against average income
fig3 = plt.figure(3)

slope, interc, r_value, p_value, std_err = stats.linregress(zipAveIncList,zipBayRestList)
plt.plot(zipAveIncList, zipBayRestList, 'go')
lineval= [slope * min(zipAveIncList) + interc, slope * max(zipAveIncList) + interc]
plt.plot([min(zipAveIncList), max(zipAveIncList)], lineval)
plt.text(80000,3.560,"r_value = " + str(round(r_value,3)))
plt.xlabel('Average Income, by ZIP')
plt.ylabel('Average Bayesian Rating, by ZIP')

plt.show()

# plot total restaurants against average income
fig4 = plt.figure(4)

slope, interc, r_value, p_value, std_err = stats.linregress(zipAveIncList,zipTotalRestList)
plt.plot(zipAveIncList, zipTotalRestList, 'go')
lineval= [slope * min(zipAveIncList) + interc, slope * max(zipAveIncList) + interc]
plt.plot([min(zipAveIncList), max(zipAveIncList)], lineval)
plt.text(70000,200,"r_value = " + str(round(r_value,3)))
plt.xlabel('Average Income, by ZIP')
plt.ylabel('Number of Restaurants, by ZIP')
plt.title('NC Average Income vs. Number of Restaurants')
plt.show()

# plot average score, price wise
fig5 = plt.figure(5)
slope1, interc1, r_value1, p_value1, std_err1 = stats.linregress(zipLoNoZero,zipLoAveRest)
slope2, interc2, r_value2, p_value2, std_err2 = stats.linregress(zipMedNoZero,zipMedAveRest)
slope3, interc3, r_value3, p_value3, std_err3 = stats.linregress(zipHiNoZero,zipHiAveRest)
plt.plot(zipLoNoZero, zipLoAveRest, 'go', color='blue', label='Low Price Range')
plt.plot(zipMedNoZero, zipMedAveRest, 'go', color='green', label='Med Price Range')
plt.plot(zipHiNoZero, zipHiAveRest, 'go', color='red', label='High Price Range')
lineval1= [slope1 * min(zipAveIncList) + interc1, slope1 * max(zipAveIncList) + interc1]
lineval2= [slope2 * min(zipAveIncList) + interc2, slope2 * max(zipAveIncList) + interc2]
lineval3= [slope3 * min(zipAveIncList) + interc3, slope3 * max(zipAveIncList) + interc3]
plt.plot([min(zipAveIncList), max(zipAveIncList)], lineval1,color='blue')
plt.plot([min(zipAveIncList), max(zipAveIncList)], lineval2,color='green')
plt.plot([min(zipAveIncList), max(zipAveIncList)], lineval3,color='red')
plt.xlabel('Average Income, by ZIP')
plt.ylabel('Average Score, by ZIP')
plt.title('NC Average Restaurant Score by their Price Ranges')
plt.text(60000,2.75,'Low r_value='+str(round(r_value1,3))+"\n"+\
         'Med r_value='+str(round(r_value2,3))+"\n"+\
        'High r_value='+str(round(r_value3,3)))
legend = plt.legend(loc='upper left', shadow=True)
for label in legend.get_texts():
    label.set_fontsize('small')
plt.show()

# plot density, price wise


fig6 = plt.figure(6)
slope1, interc1, r_value1, p_value1, std_err1 = stats.linregress(zipAveIncList,zipLoDenRest)
slope2, interc2, r_value2, p_value2, std_err2 = stats.linregress(zipAveIncList,zipMedDenRest)
slope3, interc3, r_value3, p_value3, std_err3 = stats.linregress(zipAveIncList,zipHiDenRest)
plt.plot(zipAveIncList, zipLoDenRest, 'go', color='blue',label='Low Price Range')
plt.plot(zipAveIncList, zipMedDenRest, 'go', color='green',label='Med Price Range')
plt.plot(zipAveIncList, zipHiDenRest, 'go', color='red',label='High Price Range')
lineval1= [slope1 * min(zipAveIncList) + interc1, slope1 * max(zipAveIncList) + interc1]
lineval2= [slope2 * min(zipAveIncList) + interc2, slope2 * max(zipAveIncList) + interc2]
lineval3= [slope3 * min(zipAveIncList) + interc3, slope3 * max(zipAveIncList) + interc3]
plt.plot([min(zipAveIncList), max(zipAveIncList)], lineval1,color='blue')
plt.plot([min(zipAveIncList), max(zipAveIncList)], lineval2,color='green')
plt.plot([min(zipAveIncList), max(zipAveIncList)], lineval3,color='red')
plt.xlabel('Average Income, by ZIP')
plt.ylabel('Number of Restaurants, by ZIP')
plt.title('NC Number of Restaurants by their Price Ranges')
plt.text(65000,90,'Low r_value='+str(round(r_value1,3))+"\n"+\
         'Med r_value='+str(round(r_value2,3))+"\n"+\
        'High r_value='+str(round(r_value3,3)))
legend = plt.legend(loc='upper left', shadow=True)
for label in legend.get_texts():
    label.set_fontsize('small')
plt.show()
