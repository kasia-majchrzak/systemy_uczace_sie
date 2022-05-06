import math
from collections import deque
import numpy as np
import pandas as pd


class Node:

    def __init__(self):
        self.value = None
        self.next_node = None
        self.children = None


class ID3Service:

    def __init__(self, path, delimiter=',', header=None):
        self.node = None
        self._get_data_from_file(path, delimiter, header)

    def _get_data_from_file(self, path, delimiter=',', header=None):
        data_df = pd.read_csv(path, delimiter=delimiter, header=header)
        column_names = list()
        data = dict()
        catAttrName = ""

        dataSet = [[row[col] for col in data_df.columns] for row in data_df.to_dict('records')]
        for key in data_df.columns:
            attrName = f"Atrybut {key + 1}"
            if key == (len(data_df.columns) - 1):
                catAttrName = attrName

            column_names.append(attrName)
            data[attrName] = list()
            for row in dataSet:
                if row[key] not in data[attrName]:
                    data[attrName].append(row[key])

        data_df.columns = column_names
        lastNonCatAttr = len(column_names) - 1

        self.feature_names = list(data_df.keys())[:lastNonCatAttr]
        self.feature_values = np.array(data_df.drop(catAttrName, axis=1).copy())
        self.cat_data = np.array(data_df[catAttrName].copy())
        self.decision_attr_categories = list(set(self.cat_data))
        self.decision_attr_categories_count = [list(self.cat_data).count(x) for x in self.decision_attr_categories]
        self.entropy = self._get_entropy([x for x in range(len(self.cat_data))])

    def _get_entropy(self, cat_data_ids):
        labels = [self.cat_data[i] for i in cat_data_ids]
        label_count = [labels.count(x) for x in self.decision_attr_categories]
        entropy = sum([-count / len(cat_data_ids) * math.log(count / len(cat_data_ids), 2)
                       if count else 0 for count in label_count])
        return entropy

    def _get_information_gain(self, x_ids, feature_id):
        info_gain = self._get_entropy(x_ids)
        x_features = [self.feature_values[x][feature_id] for x in x_ids]
        feature_values = list(set(x_features))
        feature_values_count = [x_features.count(x) for x in feature_values]

        feature_values_id = [
            [x_ids[i] for i, x in enumerate(x_features) if x == y]
            for y in feature_values
        ]

        info_gain = info_gain - sum([val_counts / len(x_ids) * self._get_entropy(val_ids)
                                     for val_counts, val_ids in zip(feature_values_count, feature_values_id)])

        return info_gain

    def _get_feature_max_information_gain(self, x_ids, feature_ids):
        features_entropy = [self._get_information_gain(x_ids, feature_id) for feature_id in feature_ids]
        max_id = feature_ids[features_entropy.index(max(features_entropy))]

        return self.feature_names[max_id], max_id

    def buildDecisionTree(self):
        feature_values_ids = [x for x in range(len(self.feature_values))]
        feature_ids = [x for x in range(len(self.feature_names))]
        self.node = self.buildDecisionTreeRecursive(feature_values_ids, feature_ids, self.node)
        print('')

    def buildDecisionTreeRecursive(self, feature_values_ids, feature_ids, node):
        if node is None:
            node = Node()

        labels_in_features = [self.cat_data[x] for x in feature_values_ids]

        if len(set(labels_in_features)) == 1:
            node.value = self.cat_data[feature_values_ids[0]]
            return node

        if len(feature_ids) == 0:
            node.value = max(set(labels_in_features), key=labels_in_features.count)
            return node

        best_feature_name, best_feature_id = self._get_feature_max_information_gain(feature_values_ids, feature_ids)
        node.value = best_feature_name
        node.children = []

        feature_values = list(set([self.feature_values[x][best_feature_id] for x in feature_values_ids]))

        for value in feature_values:
            child = Node()
            child.value = value
            node.children.append(child)
            child_x_ids = [x for x in feature_values_ids if self.feature_values[x][best_feature_id] == value]
            if not child_x_ids:
                child.next_node = max(set(labels_in_features), key=labels_in_features.count)
                print('')
            else:
                if feature_ids and best_feature_id in feature_ids:
                    to_remove = feature_ids.index(best_feature_id)
                    feature_ids.pop(to_remove)

                child.next_node = self.buildDecisionTreeRecursive(child_x_ids, feature_ids[:], child.next_node)
        return node

    def printDecisionTree(self, main_node=None, level=0):
        tabulator = level * "\t"

        if main_node is None:
            main_node = self.node
            print(f'{tabulator} {main_node.value}')

        if not main_node:
            return
        nodes = deque()
        nodes.append(main_node)
        while len(nodes) > 0:
            node = nodes.popleft()
            if node.children:
                for child in node.children:
                    self.printDecisionTree(child, level + 1)
            elif node.next_node:
                if node.next_node.next_node is None and node.next_node.children is None:
                    print(f'{tabulator} {node.value} -> D: {node.next_node.value}')
                else:
                    print(f'{tabulator} {node.value} -> {node.next_node.value}')
                    self.printDecisionTree(node.next_node, level + 1)
