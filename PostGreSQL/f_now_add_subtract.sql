create function f_now_add_subtract(texto text) returns text
    language plpgsql
as
$$
    declare
        res text;
    begin
        select now() + (texto)::INTERVAL into res;
        return res;
    end;
    $$;

alter function f_now_add_subtract(text) owner to postgres;

