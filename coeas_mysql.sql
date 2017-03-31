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

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone="+00:00";

CREATE TABLE users (
    userid SERIAL,
    firstname VARCHAR(35) NOT NULL,
    lastname VARCHAR(35) NOT NULL,
    email VARCHAR(254) NOT NULL,
    password text NOT NULL,
    lastlogindate date,
    
    PRIMARY KEY (userid)
) ENGINE = MyISAM;

CREATE TABLE userform (
    userid int references users(userid),
    formid SERIAL,
    
    PRIMARY KEY(userid, formid)
) ENGINE = MyISAM;

CREATE TABLE endorsement (
    userid int NOT NULL,
    formid int NOT NULL,
    endorsementid serial,
    endorsementarea text,
    
    PRIMARY KEY(endorsementid)
) ENGINE = MyISAM;

CREATE TABLE practicum_grades(
    userid int NOT NULL,
    formid int NOT NULL,
    practicumgradesid serial,
    subject text,
    grade int,
    
    PRIMARY KEY(practicumgradesid)
) ENGINE = MyISAM;

CREATE TABLE practicumhistory(
    userid int NOT NULL,
    formid int NOT NULL,
    practicumid serial,
    schooldivision text,
    schoolname text,
    gradeandsubject int references practicum_grades(practicumgradesid),
    
    PRIMARY KEY(practicumid)
) ENGINE = MyISAM;

CREATE TABLE postbac_relationships(
    userid int NOT NULL,
    formid int NOT NULL,
    relationshipid serial,
    personname text,
    schoolname text,
    relationshiptype text,
    
    PRIMARY KEY(relationshipid)
) ENGINE = MyISAM;

CREATE TABLE form_postbac (
    userid int NOT NULL,
    formid int NOT NULL,
    endorsementarea int references endorsement(endorsementid),
    requirementssatisfied bool,
    practicuminfo int references practicumhistory(practicumid),
    relationships int references postbac_relationships(relationshipid),
    preferedcountry text,
    preferedgradelevel int,
    
    PRIMARY KEY(formid)
) ENGINE = MyISAM;

CREATE TABLE fifthyear_examsneeded (
    userid int NOT NULL,
    formid int NOT NULL,
    examsid SERIAL,
    examname text,
    examdate date,
    
    PRIMARY KEY (examsid)
) ENGINE = MyISAM;

CREATE TABLE fifthyear_masters (
    userid int NOT NULL,
    formid int NOT NULL,
    mastersid SERIAL, 
    continuestudy bool,
    reasonfordiscontinue text,
    
    PRIMARY KEY (mastersid)
) ENGINE = MyISAM;

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
    
) ENGINE = MyISAM;

CREATE TABLE testscores_praxis (
    userid int NOT NULL,
    formid int NOT NULL,
    praxisid serial,
    reading int,
    writing int,
    mathematics int,
    composite int,
    
    PRIMARY KEY (praxisid)
) ENGINE = MyISAM;

CREATE TABLE testscores_sat (
    userid int NOT NULL,
    formid int NOT NULL,
    satid serial,
    verbal int,
    mathematics int,
    total int,
    
    PRIMARY KEY (satid)
) ENGINE = MyISAM;

CREATE TABLE testscores_act (
    userid int NOT NULL,
    formid int NOT NULL,
    actid serial,
    reading int,
    mathematics int,
    composite int,
    
    PRIMARY KEY (actid)
) ENGINE = MyISAM;

CREATE TABLE testscores_vcla (
    userid int NOT NULL,
    formid int NOT NULL,
    vclaid serial,
    reading int,
    writing int,
    
    PRIMARY KEY (vclaid)
) ENGINE = MyISAM;

CREATE TABLE testscores_actmath (
    userid int NOT NULL,
    formid int NOT NULL,
    actmathid serial,
    math int,
    
    PRIMARY KEY (actmathid)
) ENGINE = MyISAM;

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
) ENGINE = MyISAM;

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
) ENGINE = MyISAM;

CREATE TABLE leadershiphistory (
    userid int NOT NULL,
    formid int NOT NULL,
    leadershipid serial,
    positionheld text,
    positiondescription text,
    
    PRIMARY KEY (leadershipid)
) ENGINE = MyISAM;

CREATE TABLE youthhistory (
    userid int NOT NULL,
    formid int NOT NULL,
    youthid serial,
    positionheld text,
    positiondescription text,
    
    PRIMARY KEY (youthid)
) ENGINE = MyISAM;

CREATE TABLE studentinfo (
    userid int NOT NULL,
    formid int NOT NULL,
    studentinfoid serial,
    umwstatus text,
    studenttype text,
    majorprogram text,
    declared bool,
    majoradvisor text,
    monthyeargrad text,
    currentgpa float,
    accumulatedcredithours int,
    informationsessionattendancedate date,
    transferstudentinfo int references transferinfo(transferinfoid),
    applieddate date,
    convictbool bool,
    felonybool bool,
    misdemeanorbool bool,
    anothercountrycrimebool bool,
    preferedgender text,
    birthday date,
    preferedrace text,
    leadershiphistory int references leadershiphistory(leadershipid),
    youthhistory int references youthhistory(youthid),
    
    PRIMARY KEY (studentinfoid)
    
) ENGINE = MyISAM;

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
) ENGINE = MyISAM;

