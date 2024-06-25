create function a2(l_name text) returns text
    language plpgsql
as
$$
    DECLARE
        F_NAME TEXT;
    BEGIN
        SELECT
            people2.first_name into F_NAME
        FROM people2
        WHERE people2.last_name = L_NAME;
        raise notice 'found % and %', L_NAME, F_NAME;
        return F_NAME;
    END;
    $$;

alter function a2(text) owner to postgres;

