from modules.TreeNode import TreeNodeDTO
import pandas as pd


class EntrophyService:

    def loadDataFromFile(self, filepath):
        nonCatAttributes = list()
        file_content = pd.read_csv(filepath, delimiter=',', header=None)

        trainingSet = [[row[col] for col in file_content.columns] for row in file_content.to_dict('records')]
        for key in file_content.columns:
            nonCatAttributes.append(set())
            for row in trainingSet:
                nonCatAttributes[key].add(row[key])

        print(nonCatAttributes)
        print(trainingSet)


    def ID3(catAttribute, nonCatAttributes=[], trainingSet=[]) -> list:
        attributesInfos = dict()
        for idx, attrValuesList in enumerate(nonCatAttributes):
            info = 0
            gain = 0
            valuesCount = len(trainingSet)
            attributeDict = dict()
            for attrVal in attrValuesList:
              attrValCount = 0
              for row in trainingSet:
                attrValCount += row.count(attrVal)

              info += (attrValCount/valuesCount)*math.log(attrValCount/valuesCount, 2)
              attributeDict[attrVal] = (attrValCount/valuesCount)

            info = -1 * info

            for attrVal in attrValuesList:
              attributeDict[attrVal] = (attributeDict[attrVal]*info)

            for attrVal in attrValuesList:
              attributeDict[attrVal] = (attributeDict[attrVal]*info)

            gain = 1 - info

            attributesInfos[f'a{idx}'] = { 'idx': idx, 'info': info, 'gain': gain, 'info(ai, T)': attributeDict }
            print(attributesInfos[f'a{idx}'])

