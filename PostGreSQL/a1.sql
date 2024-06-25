create function a1(last_name text) returns text
    language plpgsql
as
$$
    DECLARE
        F_NAME TEXT;
    BEGIN
        SELECT
            people2.first_name into F_NAME
        FROM people2
        WHERE people2.last_name = $1;
        raise notice 'found % and %', $1, F_NAME;
        return F_NAME;
    END;
    $$;

alter function a1(text) owner to postgres;

