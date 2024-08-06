DB2 install and access:
=======================

· Install db2 using rthe setup for windows within the .zip file

· Take notes of the configurations during the installation:
instance: DB2
user: db2admin
password: 12345678
SID: SAMPLE

Notes:
· Check that the "DB2-0"/"DB2 - DB2COPY1 - DB2-0" service name is Manual and running

· Check the ODBC 64 bits in windows/System DNS tab, the instance ("SAMPLE") exists

· DB2 comes with a SQLPlus-like CLI called "db2". Use as follows:
$> cd C:\Program Files\IBM\SQLLIB\BIN
$> db2
db1=> <enter here your one-liner SQL commands>
Eg.:
# Querying in db2:
# create a var/alias to address the database in cmd (C:\Program Files\IBM\SQLLIB\BIN)
set db2instance=DB2 # optional
db2cmd -i -w db2clpsetcp # mandatory: this must be executed in order to access db2 tool
# to start and stop instance called SAMPLE in "db2" (these do nor seem to affect the DB2's windows Services; they are independent):
db2start 
db2stop 

# to connect using the command "db2" to the DB instance:
Eg.:
db2 => connect to SAMPLE user db2admin using 12345678
Output:
-------
   Database Connection Information

 Database server        = DB2/NT64 11.5.7.0
 SQL authorization ID   = DB2ADMIN
 Local database alias   = SAMPLE

db2 => create table t1 (a int);
db2 => commit;
db2 => select * from t1;

# to quit the db2:
$> quit

Note: dual object activation:
db2set DB2_COMPATIBILITY_VECTOR=02
db2stop
db2start

Notes: 

-In order to activate DUAL, log out of "DB2", execute the above three commands and restart the service: "DB2"/"DB2 - DB2COPY1 - DB2-0" and re-connect.
Eg.:
db2 => select * from dual;
Output:
-------
DUMMY
-----
X

  1 record(s) selected.


-DESC command works differently:
db2 => describe output select * from t1;
Output:
-------
 Column Information

 Number of columns: 1

 SQL type              Type length  Column name                     Name length
 --------------------  -----------  ------------------------------  -----------
 497   INTEGER                   4  A                                         1

db2 => describe output call give_bonus(123456, 987, ?, 15000.) -- this descs a store procedure's objects
db2 => describe table t3 show detail -- this is the ORA's regular function

-Comments: are -- or /* */ for blocks:
db2 => describe select * from t1;   -- holaq32cbr9pq832y23ryoqcei7tybcqp3786yqc v3c7qy23o74326ocvq
 Column Information

 Number of columns: 1

 SQL type              Type length  Column name                     Name length
 --------------------  -----------  ------------------------------  -----------
 497   INTEGER                   4  A                                         1


Other operations:

db2 select inst_name from sysibmadm.env_inst_info

db2 "catalog system odbc all data sources"

db2 SELECT RAND() AS RANDOM_NUMBER FROM DUAL 


-- https://github.com/ibmdb/python-ibmdb/wiki/APIs#ibm_dbconnect
