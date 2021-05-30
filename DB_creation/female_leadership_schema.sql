
CREATE TABLE sorted_occupation (
    occupation VARCHAR   ,
    all_workers INT   ,
    all_salary INT   ,
    male_workers INT   ,
    male_salary INT   ,
    female_workers INT   ,
    female_salary INT   ,
    female_to_male_salary FLOAT   ,
    female_to_male_workers_ratio FLOAT   ,
    male_worker_percent FLOAT   ,
    female_worker_percent FLOAT   ,
    representation_gap INT   ,
    male_probability BOOL   ,
    Category VARCHAR   
     
);

CREATE TABLE national_data (
    Index INT	,
    Location VARCHAR   ,
    SUBJECT VARCHAR   ,
    Time INT   ,
    WageGap FLOAT   ,
    CONSTRAINT pk_national_data PRIMARY KEY (
        Index
     )
);

CREATE TABLE states_data (
    Year INT   ,
    Label VARCHAR   ,
    US_Total VARCHAR   ,
    US_Male_Percent FLOAT   ,
    US_Female_Percent FLOAT   
);

CREATE TABLE gender_parity (
    State VARCHAR   ,
    Ranking_1993 INT   ,
    Points_1993 FLOAT   ,
    Grades_1993 VARCHAR   ,
    Ranking_2003 INT   ,
    Points_2003 FLOAT   ,
    Grades_2003 VARCHAR   ,
    Ranking_2014 INT   ,
    Points_2014 FLOAT   ,
    Grades_2014 VARCHAR   ,
    Ranking_2015 INT   ,
    Points_2015 FLOAT   ,
    Grades_2015 VARCHAR   ,
    Ranking_2016 INT   ,
    Points_2016 FLOAT   ,
    Grades_2016 VARCHAR   ,
    Ranking_2017 INT   ,
    Points_2017 FLOAT   ,
    Grades_2017 VARCHAR   ,
    Ranking_2018 INT   ,
    Points_2018 FLOAT   ,
    Grades_2018 VARCHAR   ,
    Ranking_2019 INT   ,
    Points_2019 FLOAT   ,
    Grades_2019 VARCHAR   ,
    Ranking_2020 INT   ,
    Points_2020 FLOAT   ,
    Grades_2020 VARCHAR   ,
    CONSTRAINT pk_gender_parity PRIMARY KEY (
        State
     )
);


