from django.shortcuts import render
import pandas as pd

resultsdict = []

csvreader = pd.read_csv('/workspaces/kool/kool/firsttest.csv', 
                        encoding='UTF-8',
                        header=None)

# iterating through csv file using pandas
for expert, trustworthiness in zip(csvreader[0], csvreader[1]):
    resultsdict.append([expert, trustworthiness])


def results(request, id):
    return render(request, 'result_page.html', {'results': resultsdict})
