--First, define your directory and grant the required privileges:

create directory log_dir as 'c:\tmp\';
grant read on directory log_dir to dba;
grant write on directory log_dir to dba;

--Next, we create our external table:

create table my_txt
(txt_line varchar2(512)) -- all the file's data will be inserted in a single column, not divided into several columns
organization external
(type ORACLE_LOADER
  default directory log_dir
  access parameters (records delimited by newline
  fields
   (txt_line char(512))
)
location ('x1.txt')
);

-- there all the data will be stored in TXT_LINE column (not separated)