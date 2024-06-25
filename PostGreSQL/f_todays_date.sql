create function f_todays_date() returns text
    language plpgsql
as
$$
    DECLARE
        t text = '';
    BEGIN
            SELECT TO_CHAR(NOW(), 'YYYYMMDD') INTO t;
            return t;
    END;
    $$;

alter function f_todays_date() owner to postgres;

