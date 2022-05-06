from services.ID3 import ID3Service

service = ID3Service("D:\\Informatyka II st\\II\\Systemy uczące się\\car.data", ",", None)
service.buildDecisionTree()
service.printDecisionTree()
