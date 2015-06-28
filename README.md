# CBIR Search Engine
Python content base image reterival search engine

# Requirements
 - opencv 3.0.0
 - python dependencies in requirements.txt
# Run as script
## SIFT feature
Search by SIFT feature using bag-of-words model
```
python sift_feature/index.py --vocabulary sift_feature/vocabulary.npy --index sift_feature/index.csv
python sift_feature/search.py --vocabulary sift_feature/vocabulary.npy --index sift_feature/index.csv --query dataset/snoopy_image_0010.jpg
```

## Color feature
Search by color distribution
```
python color_feature/index.py --index color_feature/index.csv
python color_feature/search.py --index color_feature/index.csv --query dataset/snoopy_image_0010.jpg
```

# Run in server
```
python manage.py syncdb
python manage.py runserver
```
