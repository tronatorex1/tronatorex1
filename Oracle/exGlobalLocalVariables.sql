<<main>>
DECLARE
  n NUMBER := 6; -- this n belongs in main only
BEGIN
  FOR n IN 1..4 LOOP
    DBMS_OUTPUT.PUT_LINE ('local n: ' || TO_CHAR(n) || ', main n: ' || TO_CHAR(main.n));
    main.n := 1 + main.n; -- this only refers to the main's n variable
  END LOOP;
END main;
/
