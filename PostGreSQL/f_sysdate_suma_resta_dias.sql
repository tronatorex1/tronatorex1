create function f_sysdate_suma_resta_dias(i integer) returns timestamp without time zone
    language plpgsql
as
$$
    declare
    out timestamp;
        begin
        select current_date + (i) into out;
        raise notice ' - res : [ % ]', out;
        return out;
    end;
    $$;

alter function f_sysdate_suma_resta_dias(integer) owner to postgres;

