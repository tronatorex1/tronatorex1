create function f_random_between(low integer, high integer) returns integer
    strict
    language plpgsql
as
$$
BEGIN
   RETURN floor(random()* (high-low + 1) + low);
END;
$$;

alter function f_random_between(integer, integer) owner to postgres;

