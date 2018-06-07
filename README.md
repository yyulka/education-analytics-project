
# Short Description

The project explores relationship between students' online behavior and their
success in an online course in Open University (UK).
The goal of the project is identifying student characteristics and behavior
patterns that are linked to high risk of failing the class. The analysis can
serve as a first step in developing "early warning" indicators that instructors
can use to help students achieve their academic goals.

# Long Description

This project belongs to the field of learning analytics. Learning analytics
involves using data to inform decisions on the part of instructors or school
administration with the goal of improving student learning outcomes.
According to research, early intervention has been effective in increasing
student academic success. Data can be used to develop so-called "early warning"
indicators that help identify students who may need extra attention to complete
the course.  Instructors can use this information to develop strategies that
would help students progress to a passing grade.

In this project I used data from an online course to identify student
characteristics and behavior patterns that are linked to high risk of failing
the class. I looked into the relationship between student demographic
characteristics as well as the way students interact with the course website
(e.g. the number of times a student logs into the system, the number of
resources the student accesses) and their academic success in the course.

## Data

The data comes from Open University which is a public distance learning and
research university in the UK. The dataset contains student-level demographic
and website usage data from an online course in Open University. The dataset
size is ~5500 student records.   

The course duration is 9 months and the data comes from four sections: Fall and
Spring semesters in 2013 and 2014.

## Modeling

Dependent variable:
* student failing the course (y/n). Based on the dataset, about 30% of students
failed the course.

Independent variables (features) fall into three categories:
*	Demographic characteristics: age, gender, education, region characteristics,
disability status, studied credits
*	Website Activity: number of clicks, variety of resources accessed regularly
*	Assessments: assessment scores, late submission

For the modeling part, I experimented with a number of models (random forest,
KNN, logistic regression) and their parameters. I ended up using logistic regression for
predictions since it had comparable performance but better interpretability.

## Metrics

For model evaluation metrics I looked at precision, recall and F1 (composite
metrics). Recall may be more important in this situation as we want to make sure
we correctly identify those who are at high risk of not passing the course, even
if it means more false positives. One way I used to increase recall was
adjusting the threshold (e.g. using .3 threshold instead of .5). This increases
recall at the expense of precision.

## Analysis and Results

For my analysis I used five checkpoints, which I chose based on the assessment
periods.  

![F1 Score](F1Score.png)

Information from each additional period improved predictions. If we look at the
score from logistic regression (I'm using F1 here but precision and recall tell
the same story) we can see that prediction score increases. This is not
surprising. The more interesting thing is the shape of this curve. We can see
that the curve increases pretty fast at the first two periods and then flattens
out. It indicates that even relatively early on in the course the model has a
fairly good predictive power.

Including additional periods doesn't increase predictive power as much (the
curve flattens out, there are some diminishing returns here). But even later
into the course the intervention can still be meaningful. With a 9-month
course there is still a lot a student can do to turn things around, even with
a couple of months left.

### Logistic regression results (at Checkpoint 2)

Demographics: students that come from regions with good socioeconomic
characteristics are less likely to fail the class, students who tried to take
the class (and failed) are more likely to fail again. Certain age groups
(33-35 years) perform better than others.

Website activity: students who are engaged and perform well on the assignments
are less likely to fail, those who submit the assignments late are more likely
to fail.

Using data from other courses may provide additional insights, but even based
on this dataset it looks like there is a lot of information, even early on in
the course, that can be used to identify students who are at risk of not passing
the course. This information can justify and guide instructor's actions that can
help students progress to a passing grade and achieve their academic goals.

# Data Source

Open University Learning Analytics dataset
https://analyse.kmi.open.ac.uk/open_dataset#about
