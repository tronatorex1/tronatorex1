create function f_sysdate() returns timestamp without time zone
    language plpgsql
as
$$
    declare
    out timestamp;
        begin
        select current_date || ' ' || current_time into out;
        raise notice ' - out : [ % ]', out;
        return out;
    end;
    $$;

alter function f_sysdate() owner to postgres;

