/*

Creates database named coaes

If a table is associated with other tables (relies on them) then I have listed them in a format such as:
    * table_1
        * table_1_dependent_table
    * table_2
    
Every row of each table in the database is tied to a combined two components:
    1. The userid that is stored with the student's account in the database
    2. The formid that is tied to the unique form that the user submitted
    
    This allows for easy retrival of a student's information based on the form they are submitting.
    userid and formid are likely to be session variables (or some equivalent functionality)

Contains the following tables:

 * users (table for student users)
 
 * form_postbac (table for post bac form)
    * endorsement
    * practicumhistory
        * practicum_grades
    * postbac_relationships
    
 * form_fifthyear (table for fifth year form)
    * endorsement
    * fifthyear_examsneeded
    * fifthyear_masters 
    * practicumhistory
        * practicum_grades

 * form_undergradadmission (table for undergraduate admission form)
    * endorsement
    * testscores
        * testscores_praxis
        * testscores_sat
        * testscores_act
        * testscores_vcla
        * testscores_actmath
    * studentinfo
        * transferinfo
        * leadershiphistory
        * youthhistory
*/

\c postgres

drop database if exists coeas;
\c postgres;


create database coeas;
\c coeas;

CREATE TABLE users (
    userid SERIAL,
    firstname VARCHAR(35) NOT NULL,
    lastname VARCHAR(35) NOT NULL,
    email VARCHAR(254) NOT NULL,
    password text NOT NULL,
    lastlogindate date,
    
    PRIMARY KEY (userid)
);



/*  POST BAC FORM TABLES */



CREATE TABLE userform (
    userid int references users(userid),
    formid SERIAL,
    
    PRIMARY KEY(userid, formid)
);

/*CREATE TABLE postbac_endorsement(
    formid int,
    endorsementid serial,
    elementary_preK6 boolean,
    english boolean,
    mathematics boolean,
    socialstudies boolean,
    biology boolean,
    chemistry boolean,
    earthscience boolean,
    physics boolean,
    latin boolean,
    spanish boolean,
    german boolean,
    french boolean,
    visualarts boolean,
    instrumentalmusic boolean,
    vocalmusic boolean,
    english_SPED boolean,
    mathematics_SPED boolean,
    socialstudies_SPED boolean,
    science_SPED boolean,
    adaptedcurriculum_SPED boolean,
    
    PRIMARY KEY(endorsementid)
); */

CREATE TABLE endorsement (
    userid int NOT NULL,
    formid int NOT NULL,
    endorsementid serial,
    endorsementarea text,
    
    PRIMARY KEY(endorsementid)
);

CREATE TABLE practicum_grades(
    userid int NOT NULL,
    formid int NOT NULL,
    practicumgradesid serial,
    subject text,
    grade int,
    
    PRIMARY KEY(practicumgradesid)
);

CREATE TABLE practicumhistory(
    userid int NOT NULL,
    formid int NOT NULL,
    practicumid serial,
    schooldivision text,
    schoolname text,
    gradeandsubject int references practicum_grades(practicumgradesid),
    
    PRIMARY KEY(practicumid)
);

CREATE TABLE postbac_relationships(
    userid int NOT NULL,
    formid int NOT NULL,
    relationshipid serial,
    personname text,
    schoolname text,
    relationshiptype text,
    
    PRIMARY KEY(relationshipid)
);

CREATE TABLE form_postbac (
    userid int NOT NULL,
    formid int NOT NULL,
    endorsementarea int references endorsement(endorsementid),
    requirementssatisfied boolean,
    practicuminfo int references practicumhistory(practicumid),
    relationships int references postbac_relationships(relationshipid),
    preferedcountry text,
    preferedgradelevel int,
    
    PRIMARY KEY(formid)
);



/* 5th YEAR FORM TABLES */



CREATE TABLE fifthyear_examsneeded (
    userid int NOT NULL,
    formid int NOT NULL,
    examsid SERIAL,
    examname text,
    examdate date,
    
    PRIMARY KEY (examsid)
);

CREATE TABLE fifthyear_masters (
    userid int NOT NULL,
    formid int NOT NULL,
    mastersid SERIAL, 
    continuestudy boolean,
    reasonfordiscontinue text,
    
    PRIMARY KEY (mastersid)
);

CREATE TABLE form_fifthyear (
    userid int NOT NULL,
    formid int NOT NULL,
    endorsementarea int references endorsement(endorsementid),
    examsneeded int references fifthyear_examsneeded(examsid),
    termgraduating text,
    mastersinfo int references fifthyear_masters(mastersid),
    practicuminfo int references practicumhistory(practicumid),
    preferedcountry text,
    preferedgradelevel int,
    
    PRIMARY KEY (formid)
    
);


/* UNDERGRADUATE ADMISSION FORM TABLES */


CREATE TABLE testscores_praxis (
    userid int NOT NULL,
    formid int NOT NULL,
    praxisid serial,
    reading int,
    writing int,
    mathematics int,
    composite int,
    
    PRIMARY KEY (praxisid)
);

CREATE TABLE testscores_sat (
    userid int NOT NULL,
    formid int NOT NULL,
    satid serial,
    verbal int,
    mathematics int,
    total int,
    
    PRIMARY KEY (satid)
);

CREATE TABLE testscores_act (
    userid int NOT NULL,
    formid int NOT NULL,
    actid serial,
    reading int,
    mathematics int,
    composite int,
    
    PRIMARY KEY (actid)
);

CREATE TABLE testscores_vcla (
    userid int NOT NULL,
    formid int NOT NULL,
    vclaid serial,
    reading int,
    writing int,
    
    PRIMARY KEY (vclaid)
);

CREATE TABLE testscores_actmath (
    userid int NOT NULL,
    formid int NOT NULL,
    actmathid serial,
    math int,
    
    PRIMARY KEY (actmathid)
);

CREATE TABLE testscores (
    userid int NOT NULL,
    formid int NOT NULL,
    testscoresid SERIAL,
    praxis int references testscores_praxis(praxisid),
    sat int references testscores_sat(satid),
    act int references testscores_act(actid),
    vcla int references testscores_vcla(vclaid),
    actmath int references testscores_actmath(actmathid),
    
    PRIMARY KEY (testscoresid)
);

CREATE TABLE transferinfo (
    userid int NOT NULL,
    formid int NOT NULL,
    transferinfoid serial,
    collegename text,
    collegecity text,
    collegestate text,
    startdate date,
    enddate date,
    degreeearned text,
    gpa float,
    enrolledname text,
    
    PRIMARY KEY (transferinfoid)
);

CREATE TABLE leadershiphistory (
    userid int NOT NULL,
    formid int NOT NULL,
    leadershipid serial,
    positionheld text,
    positiondescription text,
    
    PRIMARY KEY (leadershipid)
);

CREATE TABLE youthhistory (
    userid int NOT NULL,
    formid int NOT NULL,
    youthid serial,
    positionheld text,
    positiondescription text,
    
    PRIMARY KEY (youthid)
);

CREATE TABLE studentinfo (
    userid int NOT NULL,
    formid int NOT NULL,
    studentinfoid serial,
    umwstatus text,
    studenttype text,
    majorprogram text,
    declared boolean,
    majoradvisor text,
    monthyeargrad text,
    currentgpa float,
    accumulatedcredithours int,
    informationsessionattendancedate date,
    transferstudentinfo int references transferinfo(transferinfoid),
    applieddate date,
    convictbool boolean,
    felonybool boolean,
    misdemeanorbool boolean,
    anothercountrycrimebool boolean,
    preferedgender text,
    birthday date,
    preferedrace text,
    leadershiphistory int references leadershiphistory(leadershipid),
    youthhistory int references youthhistory(youthid),
    
    PRIMARY KEY (studentinfoid)
    
);

CREATE TABLE form_undergradadmission (
    userid int NOT NULL,
    formid int NOT NULL,
    bannerid varchar(9),
    localaddress text,
    campusphonenumber varchar(12),
    permanentaddress text,
    permanentphonenumber varchar(12),
    endorsementarea int references endorsement(endorsementid),
    testscore int references testscores(testscoresid),
    studentinfo int references studentinfo(studentinfoid),
    
    PRIMARY KEY(formid)
);