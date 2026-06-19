from pyspark.ml import PipelineModel

MODEL_PATH = "./models/flight_delay_model"

def load_model():
    return PipelineModel.load(MODEL_PATH)