# Anomaly Detection of CodeUp Traffic

## Project Description: 
We are data anaylists looking at `curriculum data` from the codeup's curriculum access logs. We have to provide feedback for our boss by Friday afternoon regarding some question they provided.


#### The Request from our boss is as Follows: 
"I have some questions for you that I need to be answered before the board meeting Friday afternoon. I need to be able to speak to the following questions. I also need a single slide that I can incorporate into my existing presentation (Google Slides) that summarizes the most important points. My questions are listed below; however, if you discover anything else important that I didn’t think to ask, please include that as well.""

## Initial Questions: 
Answer 3 of the 7 folowing questions: 
1. Which lesson appears to attract the most traffic consistently across cohorts (per program)?
2. Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
3. Are there students who, when active, hardly access the curriculum? If so, what information do you have about these students?
4. Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?
5. At some point in 2019, the ability for students and alumni to access both curriculums (web dev to ds, ds to web dev) should have been shut off. Do you see any evidence of that happening? Did it happen before?
6. What topics are grads continuing to reference after graduation and into their jobs (for each program)?
7. Which lessons are least accessed? <br>
8. Anything else I should be aware of?

# Goal: 
- To explore these questions: 
    - 1: Which lesson appears to attract the most traffic consistently across cohorts (per program)?
    - 2: Is there a cohort that referred to a lesson significantly more than other cohorts seemed to gloss over?
    - 4: Is there any suspicious activity, such as users/machines/etc accessing the curriculum who shouldn’t be? Does it appear that any web-scraping is happening? Are there any suspicious IP addresses?
    - 8: Anything else I should be aware of?
- To Achive this:
    - Explore the dataset and find important information that could assist in answering the previous questions. 
    - Visually explore the data to find anomaly or suspicious activiyt. 
    - Find anthing else out about the information that could assist our boss.
    
# Project planning: 
1. Acquire the data from the codeup SQL server: 
    - Connect the two databases: cohorts and logs
    - Create a csv file for easier acsess
2. Prepare the data:
    - Look at the data in detail: describe, info, any nulls
    - Figure out if nulls could be a potential anomaly
3. Explore the data: 
    - Explore the data with the initial question in mind. 
    - Be able to provide answers to three of the questions in time for the meeting on friday
    - Give reasoning behind the results for each question.

# Steps to Reproduce: 
1. Downloading the repository: 
    - You can download the respository and clone it to your device. 
    - You must have SQL credentials for the codeup sql server to gain access to the data. 
    - Run the Final Notebook, while also looking at how the wrangle file functions assist the notebook. 
2. Coppying the notebook to you own jupyter lab:
    - You can simply copy and past the code if you do not want clone the entire repository. Make sure you understand the code and what it does before implementing on your own. 


# Data Dictionary: 
| **Variable** | **Explanation** | 
|--------------|-----------------|
| Name | This is the name of the cohort |
| Start_date | When the cohort started |
| End_date | When the cohort ended | 
| Program_id | Which program the user is in (1,2,3,4)|
| Date | The day the user accesed the path |
| Time | The time the user accessed the path |
| Path | The URl Path  |
| User_id | The users unique identification number |
| Cohort_id | The id number of the cohort |
| ip | Internet adress fpr the path |


# Takeaways: 
1. Question One: 
    - The most common lesson across data science cohorts is classification/overview. While for web development it is the javascript-i lesson.
2. Question two: 
    - For the lesson that has a large differnce in traffic between data science cohorts is classification/overview. Darden viewed it the most while bayes viewed it the least. For the lesson that has a large differnce in traffic between web development cohorts is over the toc lesson. Juipter acessed this lesson the most while mammoth only acessed it once.
4. Question four: 
    - Suspicious acitivy occurs in users: 341, 138, 526. The accsessed a high volume of paths in a short amount of time. 
    - Users with more suspicious activity over a longer period of time are 18, 146, and 18. 


# Anything Else?
- Some things that I found that were interesting:
    - The duration of cohorts for both programs rarley meet the time frame listed on the code up website. Web development runs for 20 weeks while data science runs for 22. There are some cohorts that ran up too 26 weeks. 
    - Program 4 looks like administration as they did not have many panths acessed. They also only had one user. 
    - Web development seem to have a higher number of drop outs or supcious activity. There are 4 users: 567, 385, 589, 549 have only accessed the curriculum once. I would consider indiciuduals who acessed the curriculum less than 50 times to be students who have dropped the program. 



# Recomendations:
1. Question one:
    - These lessons could be the most common if they are the most challenging for students, or are lessons that have more learning time associated with them. 
    - I would spend more time during these lesssons helping and assisting students making sure they understand the content and material.
2. Question two: 
    - The large difference between lessons could be attributed to a difference in class size. 
    - To make lessons more balanced across cohorts it may be benificial to similarly sized classes. This may not always be the case, but this a resolutioin if the issue needs to be resolved.
4. Question four: 
    - To find a user that may have suspicious activity I would recomended looking at to things:
        - Does the user look at large volume of paths during a short period of time?
        - Does the user look at a many paths sporadically over a longer period of time?
    - These could be users who are performing harmfull activities.

    
# Next Steps:
- I would like to furthure explore and more time to answer all the questions that were asked from the data.
- I would also like to include future discoveries in this notebook.