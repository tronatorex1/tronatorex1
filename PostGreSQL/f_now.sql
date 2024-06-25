create function f_now() returns text
    language plpgsql
as
$$
declare
	t TEXT;
begin
	select TO_CHAR(NOW(),'YYYYMMDD HH:MI:SS') into t;
	return t; 
end; 
$$;

alter function f_now() owner to postgres;

