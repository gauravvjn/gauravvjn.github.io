---
layout: post
title: Machine Learning for beginners with Amazon SageMaker - Part 3
keywords: Python, Beginner, Machine Learning, Deep Learning, Artificial Intelligence, AWS, Amazon Web Services, SageMaker, Data Science, Notebook, Programming
excerpt: 3rd part of the previous post on Machine Learning for beginners with AWS SageMaker.
---

<img src="{{site.static_url}}/img/post/sagemaker.jpg" alt="Machine Learning with SageMaker" style="width:80%;height:60%"/>


#### _Note: This is [the 3rd part of "Machine Learning for beginners with Amazon SageMaker" series](/machine-learning-for-beginners-with-aws-sagemaker/)._


In the previous post, we learned how can we leverage the AWS SageMaker to train and test Machine Learning models. 
In this post, we'll try to improve the XGBoost model that we created in the last post by tuning the Hyperparameters. 
For beginners, it can be quite difficult to play with Hyperparameters without fully understanding them.
Again, Sagemaker comes with a handy utility that can tell us the best Hyperparameters configuration to obtain the best Model.

How does that work?

####  Model Hyperparameters Tuning

We use HyperparameterTuner class and provide the range of values for different Hyperparameters. Then, HyperparameterTuner
will run the model for all the values in the range and compare the performance of each run. In the end, it will return the
best model with the Hyperparameter that were used for that particular model.

You can get more details by looking at the below code.


```py
from sagemaker.tuner import IntegerParameter, ContinuousParameter, HyperparameterTuner


xgb_hyperparameter_tuner = HyperparameterTuner(
    estimator=xgb, # The estimator object to use as the basis for the training jobs.
    objective_metric_name='validation:rmse', # The metric Root Mean Square Error used to compare trained models.
    objective_type='Minimize', # We wish to minimize the Root Mean Square Error.
    max_jobs=20, # The total number of models to train
    max_parallel_jobs=3, # The number of models to train in parallel
    hyperparameter_ranges={
        'max_depth': IntegerParameter(1, 10),
        'eta': ContinuousParameter(0.05, 0.5),
        'min_child_weight': IntegerParameter(1, 10),
        'subsample': ContinuousParameter(0.5, 0.9),
        'gamma': ContinuousParameter(0, 10),
        'alpha': ContinuousParameter(0, 2)
    }
)   
``` 

Now, if you can recall from the [first post](/machine-learning-for-beginners-with-aws-sagemaker/), if we change the hyperparameters,
we need to train the model again. 

We have created a Hyperparameter Tuner object. We'll use this to train the model again by feeding the training and validation
dataset as we did in the [previous post](/machine-learning-for-beginners-with-aws-sagemaker-part-2/).


```py
 xgb_hyperparameter_tuner.fit({'train': s3_input_train, 'validation': s3_input_val})
```

We'll call the `wait()` method to print the logs of the training job 
```py
 xgb_hyperparameter_tuner.wait()
```

Once the job is done, we can get the best model by simply calling the `best_training_job()` method.

```py
 best_training_job = xgb_hyperparameter_tuner.best_training_job()
```

The value of `best_training_job` would be like 'sagemaker-xgboost-200307-1407-018-bd442cf0'.
We need to attach this job to the estimator and feed with testing data to see the performance.

```py
 xgb_attached = sagemaker.estimator.Estimator.attach(best_training_job)
 xgb_transformer = xgb_attached.transformer(instance_count=1, instance_type='ml.m4.xlarge')
 xgb_transformer.transform(test_location, content_type='text/csv', split_type='Line')
 xgb_transformer.wait()
```

Once this is done with transformation, it'll upload the result file on S3. We need to download that file
on the local instance(EC2). We can use some Notebook magic to do so(as we did in the previous post). 

```py
 !aws s3 cp --recursive $xgb_transformer.output_path $data_dir
```

Finally, Convert the downloaded data into a more readable and usable format. 
```py
 predictions = pd.read_csv(os.path.join(data_dir, 'test.csv.out'), header=None)
 pred_y = [round(num) for num in predictions.squeeze().values]
```

Check the accuracy of our model. 
```py
 accuracy_score(test_y, pred_y)
```
Awesome, We got an accuracy score of 0.8839 which is almost 10% more than the very first score(0.80) we got with GaussianNB.


#### Deploy the Model

Now the last thing we want to do is deploy our trained model so that it can be used by any user.

```py
 xgb_deployed_predictor = xgb_hyperparameter_tuner.deploy(initial_instance_count=1, instance_type='ml.m4.xlarge')
```

Or if you are not using Hyperparameter Tuner, you can simply use the `xgb` estimator object 
```py
 xgb_deployed_predictor = xgb.deploy(initial_instance_count=1, instance_type='ml.m4.xlarge')
```

When deploying a model you are asking SageMaker to launch a compute instance that will wait for data to be sent to it. 
This is important to know since the cost of a deployed endpoint depends on how long it has been running for.
We can get this endpoint by using `.endpoint` attribute.

```py
 xgb_deployed_predictor.endpoint
```

We need to tell the endpoint what format the data we are sending in
```py
 from sagemaker.predictor import csv_serializer

 xgb_deployed_predictor.content_type = 'text/csv'
 xgb_deployed_predictor.serializer = csv_serializer
```

We can use this endpoint to predict and check the performance of our model by feeding test data
```py
 Y_pred = xgb_deployed_predictor.predict(X_test.values).decode('utf-8')

 # predictions is currently a comma delimited string and so we would like to break it up as a numpy array.
 Y_pred = np.fromstring(Y_pred, sep=',')
```

WARNING: **if you are no longer using a deployed endpoint you should shut it down!**
you can do that by simply executing `delete_endpoint`.

```py
 xgb_deployed_predictor.delete_endpoint()
```

That's all for this series. I hope you learned something new.

Thank you for reading this :)

I kept it very simple and easy to understand. If you have any suggestions or questions, let me know in the comments.

PS: All the code can be found [here](https://github.com/gjain0/ML-ND-Capstone-Project/blob/master/Capstone%20Project.ipynb)
