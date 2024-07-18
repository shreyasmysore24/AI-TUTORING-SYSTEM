import pickle
import pandas as pd
import sqlite3
import warnings
import numpy as np





def predict(one,two,three):
# Load the model from pickle file
 with open('model_pickle3', 'rb') as f:
    model = pickle.load(f)

# Connect to SQLite database (or create it if it doesn't exist)
 conn = sqlite3.connect('test_scores.db')
 cursor = conn.cursor()

 sc=cursor.execute("""SELECT maths
 FROM test_scores
 ORDER BY test_no DESC
 LIMIT 3;""")
 mli=[]
 for s in sc:
   mli.append(int(s[0])) 

 sc=cursor.execute("""SELECT science
 FROM test_scores
 ORDER BY test_no DESC
 LIMIT 3;""")
 sli=[]
 for s in sc:
   sli.append(int(s[0])) 

 sc=cursor.execute("""SELECT social
 FROM test_scores
 ORDER BY test_no DESC
 LIMIT 3;""")
 ssli=[]
 for s in sc:
   ssli.append(int(s[0]))



# Define new scores
 new_scores = {
    'maths': [one],
    'science': [two],
    'social': [three],
    'maths_lag_1': [mli[0]],
    'science_lag_1': [sli[0]],
    'social_lag_1': [ssli[0]],
    'maths_lag_2': [mli[1]],
    'science_lag_2': [sli[1]],
    'social_lag_2': [ssli[1]],
    'maths_lag_1': [mli[0]],
    'science_lag_1': [sli[0]],
    'social_lag_1': [ssli[0]],
     'maths_lag_3': [mli[2]],  
    'science_lag_3': [sli[2]],
    'social_lag_3': [ssli[2]]
}

# new_scores = {
#     'maths': [0],
#     'science': [0],
#     'social': [0],
#     'maths_lag_1': [1],  
#     'science_lag_1': [1],
#     'social_lag_1': [1],
#     'maths_lag_2': [1],
#     'science_lag_2': [1],
#     'social_lag_2': [1],
#     'maths_lag_3': [0],
#     'science_lag_3': [0],
#     'social_lag_3': [0]
# }

# Create DataFrame
 new_scores_df = pd.DataFrame(new_scores)

# Print to check DataFrame contents
 print("New scores DataFrame:")
 print(new_scores_df)

# Predict using the loaded model
 predicted_category = model.predict(new_scores_df)

 if predicted_category[0]==2:
    predicted_category='medium'
 elif predicted_category[0]==0:
    predicted_category='easy'
 else:
    predicted_category='hard'
# Print predicted category
 print(f'Predicted category: {predicted_category}')

 cursor.execute('''
    INSERT INTO test_scores (maths, science, social, category)
    VALUES (1, 0, 0, ?)
    ''', (predicted_category,))

 conn.commit()
 conn.close()





