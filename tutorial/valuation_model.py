import spider_launch
import csv
import sys

#Choose CIKs or exit 
choice = 0
ciksToAnalyze =[]

while choice != 'y':
    choice = input("To use existing files, press 'e'\nTo download new data, press 'n'\nPress 'y' to exit:\n")
    if choice == 'e':
        try:
            ciksToAnalyze = list(map(str, input("Enter existing CIKs separated by comma: ").split(sep=',')))
            choice = 'y'
            print("You chose: ", ciksToAnalyze) #check the input
        except:
            print("Attention! Enter more than one CIK!")
    if choice == 'n':
        spider_launch.runQuotesSpider()
        ciksToAnalyze = spider_launch.myCIKs
        print("You chose:")
        print(ciksToAnalyze) #check the input
        choice = 'y'
    else:
        sys.exit()

#Get the time frame of required data
start_year = 0
end_year = 0
range_years = 0

while start_year != 'y':
    start_year = input("Enter start year or press 'y' to exit: ")
    if start_year != 'y':
        end_year = input("Enter end year or press 'y' to exit: ")
        if end_year != 'y':
            range_years=range(int(start_year)+1,int(end_year)+2,1)
            start_year = 'y'
            end_year = 'y'


#Load data
stockData = []
for cik in ciksToAnalyze:
    for year in range_years:
        filename=cik+'_'+str(year)+'0101.csv'
        try:
            with open(filename,newline='') as csvfile:
                print("opened file:  %s" % filename)
                caption_lines = csv.DictReader(csvfile)
                for row in caption_lines:
                    line = [row['account'], row['balance']]
                    stockData.append(line)
        except:
            print("File does not exist")

#Calculate ROE
#a) find average net income and shareholder equity over the given years
sumNIL = 0.0
countNIL = 0
sumSHE = 0.0
countSHE = 0
for i in range(len(stockData)):
    if 'us-gaap:netincome' in stockData[i][0] : 
        sumNIL = sumNIL + float(stockData[i][1])
        countNIL=countNIL+1
    if 'us-gaap:stockholdersequity' in stockData[i][0] : 
        sumSHE = sumSHE+float(stockData[i][1])
        countSHE = countSHE+1
        
print("average Net IncomeLoss: %f" % (sumNIL/countNIL))
print("average Sareholder Equity: %f" % (sumSHE/countSHE))

#b) Calculate average ROE as average NetIncomeLoss / average Shareholder Equity
averageROE=((sumNIL/countNIL)/(sumSHE/countSHE))
print("average Net IncomeLoss / average SHE: %f" % averageROE)


