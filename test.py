from DataProcessing.DataProcessor import DataProcessor

dataProcessor = DataProcessor(5)
X, Y = dataProcessor.dataProcessing("xss-train.txt", "labeled_data.csv")