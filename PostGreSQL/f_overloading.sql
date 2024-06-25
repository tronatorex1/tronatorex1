create function f_overloading(text character varying) returns text
    language plpgsql
as
$$
    declare
        res text;
    begin
        select upper(text) into res;
        return res;
    end;
    $$;

alter function f_overloading(varchar) owner to postgres;

create function f_overloading(number integer) returns text
    language plpgsql
as
$$
    declare
        res text;
    begin
        select number into res;
        return res;
    end;
    $$;

alter function f_overloading(integer) owner to postgres;

