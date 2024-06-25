create procedure p_auto_fill()
    language plpgsql
as
$$
    BEGIN
        FOR I IN 1..10 LOOP
            perform pg_sleep(0.25);
            INSERT INTO proc_auto_fill (f1, f2) VALUES ('aaa','BBB');
            raise notice 'I: %', I;
            --commit;
        END LOOP;
        COMMIT;
    END;
    $$;

alter procedure p_auto_fill() owner to postgres;

