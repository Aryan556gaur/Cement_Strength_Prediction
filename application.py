from flask import Flask, request, render_template, send_file
from src.exception import CustomException
from src.pipelines.TrainingPipeline import TrainingPipeline
from src.pipelines.PredictionPipeline import SinglePrediction, BatchPrediction
import sys

application = Flask(__name__)

app = application

@app.route("/")
def home():
    return render_template('index.html')


@app.route('/predict',methods=['GET','POST'])
def predict_datapoint():
    if request.method=='GET':
        return render_template('form.html')
    
    else:
        try:
            training_pipeline = TrainingPipeline()
            training_pipeline.run_training_pipeline()

            predict_pipeline = SinglePrediction(float(request.form.get('Cement')), float(request.form.get('Blast')),
                float(request.form.get('Fly')),float(request.form.get('Water')),float(request.form.get('Superplasticizer')),
                float(request.form.get('Coarse')),float(request.form.get('Fine')),float(request.form.get('Age')))
            
            df = predict_pipeline.get_data_as_dataframe()
            y = predict_pipeline.predict(df)

            return f"Your Concrete compressive strength is {y}MPa (megapascals)"
        
        except Exception as e:
            raise CustomException(e,sys)
    
    
@app.route('/predict_file',methods=['Get','Post'])
def predict_file():
    if request.method=='GET':
        return render_template('upload_file.html')
    
    else:
        try:
            training_pipeline = TrainingPipeline()
            training_pipeline.run_training_pipeline()

            predict_pipeline = BatchPrediction(request)
            input_file_path = predict_pipeline.save_file()
            predicted_file_path = predict_pipeline.predict_file(input_file_path)

            return send_file(path_or_file=predicted_file_path,download_name=predicted_file_path,as_attachment=True)
    
        except Exception as e:
            raise CustomException(e,sys)
        
if __name__=='__main__':
    app.run('0.0.0.0', debug=True)