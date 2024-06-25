create function f_todays_time() returns text
    language plpgsql
as
$$
    declare
    t text = '';
        begin
            select to_char(now(), 'HH:MI:SS') INTO t;
            return t;
    end;
    $$;

alter function f_todays_time() owner to postgres;

