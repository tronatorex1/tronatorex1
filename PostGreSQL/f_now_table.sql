create function f_now_table()
    returns TABLE(date_ text, time_ text)
    language plpgsql
as
$$
declare
begin
	return query
	select TO_CHAR(NOW(),'YYYYMMDD'), TO_CHAR(NOW(),'HH:MI:SS');
end; 
$$;

alter function f_now_table() owner to postgres;

