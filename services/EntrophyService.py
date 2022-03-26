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
        result = list()
        if trainingSet is None or trainingSet.count() == 0:
            tree_node = TreeNodeDTO()
            tree_node.level = 0
            tree_node.item = "Failure"
            result.append(tree_node)
            return result

        uniqueTrainingValues = set(trainingSet)

        if uniqueTrainingValues.__sizeof__() == 1:
            tree_node = TreeNodeDTO()
            tree_node.level = 0
            tree_node.item = trainingSet[0]
            result.append(tree_node)
            return result

        if nonCatAttributes is None or nonCatAttributes.count() == 0:
            tree_node = TreeNodeDTO()
            tree_node.level = 0
            tree_node.item = max(set(trainingSet), key=trainingSet.count)
            result.append(tree_node)
            return result



        return result
